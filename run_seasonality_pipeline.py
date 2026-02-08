"""
Seasonality Pipeline: Pre-compute top selling items per category path per event.

Reads from production Atlas MongoDB, writes results to local MongoDB.
The dashboard then reads from local MongoDB instead of running live aggregations.

Usage:
    python run_seasonality_pipeline.py --start-date 2025-01-01 --end-date 2025-12-31
    python run_seasonality_pipeline.py --start-date 2025-01-01 --end-date 2025-12-31 --events ramadan,eid_al_fitr
    python run_seasonality_pipeline.py --start-date 2025-01-01 --end-date 2025-12-31 --dry-run
"""

import os
import argparse
import logging
from datetime import datetime

from pymongo import MongoClient, ASCENDING
from bson import ObjectId
from dotenv import load_dotenv

from seasonal_event_category_mapping import EVENT_CATEGORY_MAPPING

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Helpers (copied from app.py to avoid module-level side effects on import)
# ---------------------------------------------------------------------------

def serialize_doc(doc):
    """Convert ObjectId and datetime fields to strings for JSON serialization."""
    if isinstance(doc, dict):
        return {k: serialize_doc(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)
    elif isinstance(doc, datetime):
        return doc.strftime("%Y-%m-%d")
    else:
        return doc


def get_top_item_for_path(orders_collection, start_date, end_date, category_path):
    """
    Run the same aggregation as app.py:get_top_item_for_path() and return the
    top-1 selling item for a specific category path, or None.
    """
    pipeline = [
        {"$match": {"createdAt": {"$gte": start_date, "$lte": end_date}}},
        {"$unwind": "$items"},
        {
            "$group": {
                "_id": {"item_id": "$items._item", "vendor_id": "$_vendor"},
                "item_name": {"$first": "$items.name.en"},
                "item_image": {"$first": "$items.image.large"},
                "price": {"$first": "$items.price"},
                "total_qty": {"$sum": "$items.quantity"},
                "orders_count": {"$addToSet": "$_id"},
                "users_count": {"$addToSet": "$_user"},
            }
        },
        {"$lookup": {"from": "Items", "localField": "_id.item_id", "foreignField": "_id", "as": "item"}},
        {"$unwind": "$item"},
        {"$lookup": {"from": "Vendors", "localField": "_id.vendor_id", "foreignField": "_id", "as": "vendor"}},
        {"$unwind": "$vendor"},
    ]

    # Filter by category path
    match_condition = {}
    if category_path.get("shoppingCategory"):
        match_condition["item.data.shoppingCategory.en"] = category_path["shoppingCategory"]
    if category_path.get("shoppingSubcategory"):
        match_condition["item.data.shoppingSubcategory.en"] = category_path["shoppingSubcategory"]
    if category_path.get("itemCategory"):
        match_condition["item.data.itemCategory.en"] = category_path["itemCategory"]
    if category_path.get("itemSubcategory"):
        match_condition["item.data.itemSubcategory.en"] = category_path["itemSubcategory"]

    if match_condition:
        pipeline.append({"$match": match_condition})

    pipeline.extend([
        {
            "$project": {
                "_id": 0,
                "item_id": "$item._id",
                "item_name": {"$ifNull": ["$item_name", "$item.name.en"]},
                "item_image": {"$ifNull": ["$item_image", {"$arrayElemAt": ["$item.images.large", 0]}]},
                "vendor_id": "$vendor._id",
                "vendor_name": "$vendor.name.en",
                "price": {"$ifNull": ["$price", "$item.price"]},
                "total_qty": 1,
                "orders_count": {"$size": "$orders_count"},
                "users_count": {"$size": "$users_count"},
            }
        },
        {"$sort": {"total_qty": -1}},
        {"$limit": 1},
    ])

    result = list(orders_collection.aggregate(pipeline))
    return serialize_doc(result[0]) if result else None


def build_path_hash(category_path):
    """Deterministic string key for a category path dict."""
    parts = [
        category_path.get("shoppingCategory", ""),
        category_path.get("shoppingSubcategory", ""),
        category_path.get("itemCategory", ""),
        category_path.get("itemSubcategory", ""),
    ]
    return "|".join(parts)


def build_path_label(category_path):
    """Human-readable label like 'groceries > supermarkets > produce > dried fruit'."""
    return " > ".join(filter(None, [
        category_path.get("shoppingCategory"),
        category_path.get("shoppingSubcategory"),
        category_path.get("itemCategory"),
        category_path.get("itemSubcategory"),
    ]))


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_pipeline(start_date, end_date, event_keys=None, dry_run=False):
    # ---- Connections ----
    prod_uri = os.getenv("MONGO_URI")
    local_uri = os.getenv("LOCAL_MONGO_URI", "mongodb://localhost:27017/")

    if not prod_uri:
        log.error("MONGO_URI env var is not set. Cannot connect to production MongoDB.")
        return

    prod_client = MongoClient(prod_uri)
    prod_db = prod_client.get_database("botitprod")
    orders_collection = prod_db["Orders"]

    local_client = MongoClient(local_uri)
    local_db = local_client.get_database("botitprod")
    seasonality_col = local_db["seasonality"]

    # Ensure compound unique index
    if not dry_run:
        seasonality_col.create_index(
            [("event_key", ASCENDING), ("path_hash", ASCENDING)],
            unique=True,
            name="event_path_unique",
        )
        log.info("Ensured compound unique index on (event_key, path_hash)")

    # ---- Determine which events to process ----
    if event_keys:
        events = {k: EVENT_CATEGORY_MAPPING[k] for k in event_keys if k in EVENT_CATEGORY_MAPPING}
        missing = set(event_keys) - set(events.keys())
        if missing:
            log.warning("Unknown event keys (skipped): %s", ", ".join(missing))
    else:
        events = EVENT_CATEGORY_MAPPING

    total_paths = sum(len(e.get("category_paths", [])) for e in events.values())
    log.info(
        "Processing %d events, %d total paths  |  date range: %s to %s  |  dry_run=%s",
        len(events), total_paths,
        start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d"),
        dry_run,
    )

    upserted = 0
    found = 0
    empty = 0

    for event_key, event_data in events.items():
        event_name = event_data.get("name", event_key)
        paths = event_data.get("category_paths", [])
        log.info("  Event: %s (%d paths)", event_name, len(paths))

        for i, path in enumerate(paths, 1):
            path_hash = build_path_hash(path)
            path_label = build_path_label(path)

            if dry_run:
                log.info("    [DRY-RUN] %d/%d  %s", i, len(paths), path_label)
                continue

            top_item = get_top_item_for_path(orders_collection, start_date, end_date, path)

            doc = {
                "event_key": event_key,
                "event_name": event_name,
                "path_hash": path_hash,
                "category_path": path,
                "path_label": path_label,
                "top_item": top_item,
                "date_range": {
                    "start": start_date.strftime("%Y-%m-%d"),
                    "end": end_date.strftime("%Y-%m-%d"),
                },
                "updated_at": datetime.utcnow(),
            }

            seasonality_col.update_one(
                {"event_key": event_key, "path_hash": path_hash},
                {"$set": doc},
                upsert=True,
            )
            upserted += 1

            if top_item:
                found += 1
                log.info("    %d/%d  %s  ->  %s (qty=%s)",
                         i, len(paths), path_label,
                         top_item.get("item_name", "?"),
                         top_item.get("total_qty", 0))
            else:
                empty += 1
                log.info("    %d/%d  %s  ->  (no data)", i, len(paths), path_label)

    log.info(
        "Done. upserted=%d  items_found=%d  no_data=%d",
        upserted, found, empty,
    )

    prod_client.close()
    local_client.close()


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Pre-compute top selling items per category path per seasonal event.",
    )
    parser.add_argument("--start-date", required=True, help="Start date YYYY-MM-DD")
    parser.add_argument("--end-date", required=True, help="End date YYYY-MM-DD")
    parser.add_argument(
        "--events",
        default=None,
        help="Comma-separated event keys to process (default: all). E.g. ramadan,eid_al_fitr",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Iterate events/paths and log, but do not query prod or write to local.",
    )

    args = parser.parse_args()

    start_date = datetime.strptime(args.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(args.end_date, "%Y-%m-%d")

    event_keys = None
    if args.events:
        event_keys = [e.strip() for e in args.events.split(",") if e.strip()]

    run_pipeline(start_date, end_date, event_keys=event_keys, dry_run=args.dry_run)


if __name__ == "__main__":
    main()
