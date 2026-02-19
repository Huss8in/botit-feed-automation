import os
import json
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId
import openai

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.get_database("botitprod")

# Local MongoDB connection (for pre-computed seasonality cache)
local_mongo_uri = os.getenv("LOCAL_MONGO_URI", "mongodb://localhost:27017/")
local_client = MongoClient(local_mongo_uri)
local_db = local_client.get_database("botitprod")
seasonality_results_collection = local_db["seasonality"]
tiktok_hashtags_collection = local_db["tiktok-hashtags"]

# OpenAI configuration
openai.api_key = os.getenv("OPENAI_API_KEY")

# Collections
items_collection = db["Items"]
orders_collection = db["Orders"]
vendors_collection = db["Vendors"]

# -------------------------------------------------------------------------------------------------------------- #
def get_top_vendors_pipeline(start_date, end_date):
    """
    Aggregation pipeline to get top vendors based on orders within date range.
    Returns: vendor_id, vendor_name, vendor_image, vendor_shoppingCategory, total_qty, orders_count, users_count, items_count
    """
    pipeline = [
        {
            "$match": {
                "createdAt": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
        },
        {
            "$unwind": "$items"
        },
        {
            "$group": {
                "_id": "$_vendor",
                "total_qty": {"$sum": "$items.quantity"},
                "orders_count": {"$addToSet": "$_id"},
                "users_count": {"$addToSet": "$_user"},
                "items_count": {"$addToSet": "$items._item"}
            }
        },
        {
            "$lookup": {
                "from": "Vendors",
                "localField": "_id",
                "foreignField": "_id",
                "as": "vendor"
            }
        },
        {
            "$unwind": {
                "path": "$vendor",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "_id": 0,
                "start_date": {"$literal": start_date.strftime('%Y-%m-%d')},
                "end_date": {"$literal": end_date.strftime('%Y-%m-%d')},
                "vendor_id": "$vendor._id",
                "vendor_name": "$vendor.name.en",
                "vendor_image": "$vendor.image",
                "vendor_shoppingCategory": "$vendor.shoppingCategory",
                "total_qty": 1,
                "orders_count": {"$size": "$orders_count"},
                "users_count": {"$size": "$users_count"},
                "items_count": {"$size": "$items_count"}
            }
        },
        {
            "$sort": {"orders_count": -1}
        },
        {
            "$limit": 50
        }
    ]
    return pipeline

# -------------------------------------------------------------------------------------------------------------- #
def get_top_items_pipeline(start_date, end_date):
    """
    Aggregation pipeline to get top items based on orders within date range.
    Returns: item_id, item_name, vendor_id, vendor_name, vendor_image, vendor_shoppingCategory, price, total_qty, orders_count, users_count
    """
    pipeline = [
        {
            "$match": {
                "createdAt": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
        },
        {
            "$unwind": "$items"
        },
        {
            "$group": {
                "_id": {
                    "item_id": "$items._item",
                    "vendor_id": "$_vendor"
                },
                "item_name": {"$first": "$items.name.en"},
                "item_image": {"$first": "$items.image.large"},
                "price": {"$first": "$items.price"},
                "total_qty": {"$sum": "$items.quantity"},
                "orders_count": {"$addToSet": "$_id"},
                "users_count": {"$addToSet": "$_user"}
            }
        },
        {
            "$lookup": {
                "from": "Items",
                "localField": "_id.item_id",
                "foreignField": "_id",
                "as": "item"
            }
        },
        {
            "$unwind": {
                "path": "$item",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$lookup": {
                "from": "Vendors",
                "localField": "_id.vendor_id",
                "foreignField": "_id",
                "as": "vendor"
            }
        },
        {
            "$unwind": {
                "path": "$vendor",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "_id": 0,
                "start_date": {"$literal": start_date.strftime('%Y-%m-%d')},
                "end_date": {"$literal": end_date.strftime('%Y-%m-%d')},
                "item_id": "$item._id",
                "item_name": {"$ifNull": ["$item_name", "$item.name.en"]},
                "item_image": {"$ifNull": ["$item_image", {"$arrayElemAt": ["$item.images.large", 0]}]},
                "vendor_id": "$vendor._id",
                "vendor_name": "$vendor.name.en",
                "vendor_image": "$vendor.image",
                "vendor_shoppingCategory": "$vendor.shoppingCategory",
                "item_shoppingCategory": "$item.data.shoppingCategory.en",
                "item_shoppingSubcategory": "$item.data.shoppingSubcategory.en",
                "item_itemCategory": "$item.data.itemCategory.en",
                "item_itemSubcategory": "$item.data.itemSubcategory.en",
                "price": {"$ifNull": ["$price", "$item.price"]},
                "total_qty": 1,
                "orders_count": {"$size": "$orders_count"},
                "users_count": {"$size": "$users_count"}
            }
        },
        {
            "$sort": {"total_qty": -1}
        },
        {
            "$limit": 50
        }
    ]
    return pipeline

# -------------------------------------------------------------------------------------------------------------- # 
# -------------------------------------------------------------------------------------------------------------- # 
# -------------------------------------------------------------------------------------------------------------- # 
def get_seasonality_vendors_pipeline(start_date, end_date, categories=None, subcategories=None):
    """
    Aggregation pipeline for seasonality page to get vendors filtered by shopping categories.
    Filters at the database level for efficiency.

    Args:
        start_date: Start date for order filtering
        end_date: End date for order filtering
        categories: List of shoppingCategory values to filter by (e.g., ['fashion', 'beauty'])
        subcategories: List of shoppingSubcategory values to filter by (e.g., ['casual wear', 'skincare'])

    Returns: vendor_id, vendor_name, vendor_image, vendor_shoppingCategory, vendor_shopsubcat, total_qty, orders_count, users_count, items_count
    """
    pipeline = [
        {
            "$match": {
                "createdAt": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
        },
        {
            "$unwind": "$items"
        },
        {
            "$group": {
                "_id": "$_vendor",
                "total_qty": {"$sum": "$items.quantity"},
                "orders_count": {"$addToSet": "$_id"},
                "users_count": {"$addToSet": "$_user"},
                "items_count": {"$addToSet": "$items._item"}
            }
        },
        {
            "$lookup": {
                "from": "Vendors",
                "localField": "_id",
                "foreignField": "_id",
                "as": "vendor"
            }
        },
        {
            "$unwind": {
                "path": "$vendor",
                "preserveNullAndEmptyArrays": True
            }
        }
    ]

    # Add category filtering after lookup (filter on vendor's shoppingCategory)
    match_conditions = {}
    if categories and len(categories) > 0:
        match_conditions["vendor.shoppingCategory"] = {"$in": categories}
    if subcategories and len(subcategories) > 0:
        match_conditions["vendor.shoppingSubcategory"] = {"$in": subcategories}

    if match_conditions:
        pipeline.append({"$match": match_conditions})

    # Add projection and sorting
    pipeline.extend([
        {
            "$project": {
                "_id": 0,
                "start_date": {"$literal": start_date.strftime('%Y-%m-%d')},
                "end_date": {"$literal": end_date.strftime('%Y-%m-%d')},
                "vendor_id": "$vendor._id",
                "vendor_name": "$vendor.name.en",
                "vendor_image": "$vendor.image",
                "vendor_shoppingCategory": "$vendor.shoppingCategory",
                "total_qty": 1,
                "orders_count": {"$size": "$orders_count"},
                "users_count": {"$size": "$users_count"},
                "items_count": {"$size": "$items_count"}
            }
        },
        {
            "$sort": {"orders_count": -1}
        },
        {
            "$limit": 50
        }
    ])

    return pipeline


def get_seasonality_items_pipeline(start_date, end_date, categories=None, subcategories=None):
    """
    Aggregation pipeline for seasonality page to get items filtered by vendor's shopping categories.
    Filters at the database level for efficiency.

    Args:
        start_date: Start date for order filtering
        end_date: End date for order filtering
        categories: List of shoppingCategory values to filter by (e.g., ['fashion', 'beauty'])
        subcategories: List of shoppingSubcategory values to filter by (e.g., ['casual wear', 'skincare'])

    Returns: item_id, item_name, item_image, vendor_id, vendor_name, vendor_image, vendor_shoppingCategory, vendor_shopsubcat, price, total_qty, orders_count, users_count
    """
    pipeline = [
        {
            "$match": {
                "createdAt": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
        },
        {
            "$unwind": "$items"
        },
        {
            "$group": {
                "_id": {
                    "item_id": "$items._item",
                    "vendor_id": "$_vendor"
                },
                "item_name": {"$first": "$items.name.en"},
                "item_image": {"$first": "$items.image.large"},
                "price": {"$first": "$items.price"},
                "total_qty": {"$sum": "$items.quantity"},
                "orders_count": {"$addToSet": "$_id"},
                "users_count": {"$addToSet": "$_user"}
            }
        },
        {
            "$lookup": {
                "from": "Items",
                "localField": "_id.item_id",
                "foreignField": "_id",
                "as": "item"
            }
        },
        {
            "$unwind": {
                "path": "$item",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$lookup": {
                "from": "Vendors",
                "localField": "_id.vendor_id",
                "foreignField": "_id",
                "as": "vendor"
            }
        },
        {
            "$unwind": {
                "path": "$vendor",
                "preserveNullAndEmptyArrays": True
            }
        }
    ]

    # Add category filtering after lookup (filter on vendor's shoppingCategory)
    match_conditions = {}
    if categories and len(categories) > 0:
        match_conditions["vendor.shoppingCategory"] = {"$in": categories}
    if subcategories and len(subcategories) > 0:
        match_conditions["vendor.shoppingSubcategory"] = {"$in": subcategories}

    if match_conditions:
        pipeline.append({"$match": match_conditions})

    # Add projection and sorting
    pipeline.extend([
        {
            "$project": {
                "_id": 0,
                "start_date": {"$literal": start_date.strftime('%Y-%m-%d')},
                "end_date": {"$literal": end_date.strftime('%Y-%m-%d')},
                "item_id": "$item._id",
                "item_name": {"$ifNull": ["$item_name", "$item.name.en"]},
                "item_image": {"$ifNull": ["$item_image", {"$arrayElemAt": ["$item.images.large", 0]}]},
                "vendor_id": "$vendor._id",
                "vendor_name": "$vendor.name.en",
                "vendor_image": "$vendor.image",
                "vendor_shoppingCategory": "$vendor.shoppingCategory",
                "item_shoppingCategory": "$item.data.shoppingCategory.en",
                "item_shoppingSubcategory": "$item.data.shoppingSubcategory.en",
                "item_itemCategory": "$item.data.itemCategory.en",
                "item_itemSubcategory": "$item.data.itemSubcategory.en",
                "price": {"$ifNull": ["$price", "$item.price"]},
                "total_qty": 1,
                "orders_count": {"$size": "$orders_count"},
                "users_count": {"$size": "$users_count"}
            }
        },
        {
            "$sort": {"total_qty": -1}
        },
        {
            "$limit": 50
        }
    ])

    return pipeline

# -------------------------------------------------------------------------------------------------------------- #
def get_seasonality_items_by_event_pipeline(start_date, end_date, category_paths=None):
    """
    Aggregation pipeline for seasonality page to get items filtered by event category paths.
    Filters on item-level categories (shoppingCategory, shoppingSubcategory, itemCategory, itemSubcategory).

    Args:
        start_date: Start date for order filtering
        end_date: End date for order filtering
        category_paths: List of category path dicts from seasonal_event_category_mapping.py
                       Each dict can have: shoppingCategory, shoppingSubcategory, itemCategory, itemSubcategory

    Returns: item_id, item_name, item_image, vendor_id, vendor_name, vendor_image, all category fields, price, total_qty, orders_count, users_count
    """
    pipeline = [
        {
            "$match": {
                "createdAt": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
        },
        {
            "$unwind": "$items"
        },
        {
            "$group": {
                "_id": {
                    "item_id": "$items._item",
                    "vendor_id": "$_vendor"
                },
                "item_name": {"$first": "$items.name.en"},
                "item_image": {"$first": "$items.image.large"},
                "price": {"$first": "$items.price"},
                "total_qty": {"$sum": "$items.quantity"},
                "orders_count": {"$addToSet": "$_id"},
                "users_count": {"$addToSet": "$_user"}
            }
        },
        {
            "$lookup": {
                "from": "Items",
                "localField": "_id.item_id",
                "foreignField": "_id",
                "as": "item"
            }
        },
        {
            "$unwind": {
                "path": "$item",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$lookup": {
                "from": "Vendors",
                "localField": "_id.vendor_id",
                "foreignField": "_id",
                "as": "vendor"
            }
        },
        {
            "$unwind": {
                "path": "$vendor",
                "preserveNullAndEmptyArrays": True
            }
        }
    ]

    # Add category path filtering (using $or for multiple paths)
    if category_paths:
        or_conditions = []

        for path in category_paths:
            and_conditions = []

            if path.get("shoppingCategory"):
                and_conditions.append({"item.data.shoppingCategory.en": path["shoppingCategory"]})

            if path.get("shoppingSubcategory"):
                and_conditions.append({"item.data.shoppingSubcategory.en": path["shoppingSubcategory"]})

            if path.get("itemCategory"):
                and_conditions.append({"item.data.itemCategory.en": path["itemCategory"]})

            if path.get("itemSubcategory"):
                and_conditions.append({"item.data.itemSubcategory.en": path["itemSubcategory"]})

            if and_conditions:
                or_conditions.append({"$and": and_conditions})

        if or_conditions:
            pipeline.append({"$match": {"$or": or_conditions}})

    # Add projection and sorting
    pipeline.extend([
        {
            "$project": {
                "_id": 0,
                "start_date": {"$literal": start_date.strftime('%Y-%m-%d')},
                "end_date": {"$literal": end_date.strftime('%Y-%m-%d')},
                "item_id": "$item._id",
                "item_name": {"$ifNull": ["$item_name", "$item.name.en"]},
                "item_image": {"$ifNull": ["$item_image", {"$arrayElemAt": ["$item.images.large", 0]}]},
                "vendor_id": "$vendor._id",
                "vendor_name": "$vendor.name.en",
                "vendor_image": "$vendor.image",
                "vendor_shoppingCategory": "$vendor.shoppingCategory",
                "item_shoppingCategory": "$item.data.shoppingCategory.en",
                "item_shoppingSubcategory": "$item.data.shoppingSubcategory.en",
                "item_itemCategory": "$item.data.itemCategory.en",
                "item_itemSubcategory": "$item.data.itemSubcategory.en",
                "price": {"$ifNull": ["$price", "$item.price"]},
                "total_qty": 1,
                "orders_count": {"$size": "$orders_count"},
                "users_count": {"$size": "$users_count"}
            }
        },
        {
            "$sort": {"total_qty": -1}
        },
        {
            "$limit": 50
        }
    ])

    return pipeline


# -------------------------------------------------------------------------------------------------------------- #
def get_seasonality_vendors_by_event_pipeline(start_date, end_date, category_paths=None):
    """
    Aggregation pipeline for seasonality page to get vendors filtered by event category paths.
    Aggregates items by vendor, filtering on item-level categories.

    Args:
        start_date: Start date for order filtering
        end_date: End date for order filtering
        category_paths: List of category path dicts from seasonal_event_category_mapping.py

    Returns: vendor_id, vendor_name, vendor_image, vendor_shoppingCategory, total_qty, orders_count, users_count, items_count
    """
    pipeline = [
        {
            "$match": {
                "createdAt": {
                    "$gte": start_date,
                    "$lte": end_date
                }
            }
        },
        {
            "$unwind": "$items"
        },
        # First lookup items to get item-level categories
        {
            "$lookup": {
                "from": "Items",
                "localField": "items._item",
                "foreignField": "_id",
                "as": "item_doc"
            }
        },
        {
            "$unwind": {
                "path": "$item_doc",
                "preserveNullAndEmptyArrays": True
            }
        }
    ]

    # Add category path filtering on items
    if category_paths and len(category_paths) > 0:
        or_conditions = []
        for path in category_paths:
            condition = {}
            if "shoppingCategory" in path:
                condition["item_doc.data.shoppingCategory.en"] = path["shoppingCategory"]
            if "shoppingSubcategory" in path:
                condition["item_doc.data.shoppingSubcategory.en"] = path["shoppingSubcategory"]
            if "itemCategory" in path:
                condition["item_doc.data.itemCategory.en"] = path["itemCategory"]
            if "itemSubcategory" in path:
                condition["item_doc.data.itemSubcategory.en"] = path["itemSubcategory"]

            if condition:
                or_conditions.append(condition)

        if or_conditions:
            pipeline.append({"$match": {"$or": or_conditions}})

    # Group by vendor
    pipeline.extend([
        {
            "$group": {
                "_id": "$_vendor",
                "total_qty": {"$sum": "$items.quantity"},
                "orders_count": {"$addToSet": "$_id"},
                "users_count": {"$addToSet": "$_user"},
                "items_count": {"$addToSet": "$items._item"}
            }
        },
        {
            "$lookup": {
                "from": "Vendors",
                "localField": "_id",
                "foreignField": "_id",
                "as": "vendor"
            }
        },
        {
            "$unwind": {
                "path": "$vendor",
                "preserveNullAndEmptyArrays": True
            }
        },
        {
            "$project": {
                "_id": 0,
                "start_date": {"$literal": start_date.strftime('%Y-%m-%d')},
                "end_date": {"$literal": end_date.strftime('%Y-%m-%d')},
                "vendor_id": "$vendor._id",
                "vendor_name": "$vendor.name.en",
                "vendor_image": "$vendor.image",
                "vendor_shoppingCategory": "$vendor.shoppingCategory",
                "total_qty": 1,
                "orders_count": {"$size": "$orders_count"},
                "users_count": {"$size": "$users_count"},
                "items_count": {"$size": "$items_count"}
            }
        },
        {
            "$sort": {"orders_count": -1}
        },
        {
            "$limit": 50
        }
    ])

    return pipeline

# -------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------------------- #
def serialize_doc(doc):
    """Convert ObjectId and datetime fields to strings for JSON serialization."""
    if isinstance(doc, dict):
        return {k: serialize_doc(v) for k, v in doc.items()}
    elif isinstance(doc, list):
        return [serialize_doc(item) for item in doc]
    elif isinstance(doc, ObjectId):
        return str(doc)
    elif isinstance(doc, datetime):
        return doc.strftime('%Y-%m-%d')
    else:
        return doc


@app.route('/')
def index():
    """Main dashboard page."""
    default_end = datetime.now()
    default_start = default_end - timedelta(days=30)
    return render_template('index.html',
                         default_start=default_start.strftime('%Y-%m-%d'),
                         default_end=default_end.strftime('%Y-%m-%d'))


@app.route('/feed')
def feed_page():
    """Feed generator page - AI-powered feed recommendations."""
    return render_template('feed.html')


@app.route('/api/top-vendors', methods=['GET'])
def api_top_vendors():
    """API endpoint to get top vendors by date range."""
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)

        pipeline = get_top_vendors_pipeline(start_date, end_date)
        results = list(orders_collection.aggregate(pipeline))
        results = serialize_doc(results)

        display_pipeline = serialize_doc(pipeline)

        return jsonify({
            'success': True,
            'data': results,
            'pipeline': display_pipeline,
            'count': len(results),
            'date_range': {
                'start': start_date_str,
                'end': end_date_str
            }
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


@app.route('/api/top-items', methods=['GET'])
def api_top_items():
    """API endpoint to get top items by date range."""
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)

        pipeline = get_top_items_pipeline(start_date, end_date)
        results = list(orders_collection.aggregate(pipeline))
        results = serialize_doc(results)

        display_pipeline = serialize_doc(pipeline)

        return jsonify({
            'success': True,
            'data': results,
            'pipeline': display_pipeline,
            'count': len(results),
            'date_range': {
                'start': start_date_str,
                'end': end_date_str
            }
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


@app.route('/api/seasonality/vendors', methods=['GET'])
def api_seasonality_vendors():
    """
    API endpoint for seasonality page to get vendors filtered by shopping categories.
    Query params:
        - start_date: YYYY-MM-DD
        - end_date: YYYY-MM-DD
        - categories: Comma-separated list of shoppingCategory values (e.g., 'fashion,beauty')
        - subcategories: Comma-separated list of shoppingSubcategory values (e.g., 'casual wear,skincare')
    """
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        categories_str = request.args.get('categories', '')
        subcategories_str = request.args.get('subcategories', '')

        if not start_date_str or not end_date_str:
            return jsonify({'success': False, 'error': 'start_date and end_date are required'}), 400

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)

        # Parse categories and subcategories from comma-separated strings
        categories = [c.strip() for c in categories_str.split(',') if c.strip()] if categories_str else None
        subcategories = [s.strip() for s in subcategories_str.split(',') if s.strip()] if subcategories_str else None

        pipeline = get_seasonality_vendors_pipeline(start_date, end_date, categories, subcategories)
        results = list(orders_collection.aggregate(pipeline))
        results = serialize_doc(results)

        display_pipeline = serialize_doc(pipeline)

        return jsonify({
            'success': True,
            'data': results,
            'pipeline': display_pipeline,
            'count': len(results),
            'date_range': {
                'start': start_date_str,
                'end': end_date_str
            },
            'filters': {
                'categories': categories,
                'subcategories': subcategories
            }
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


@app.route('/api/seasonality/items', methods=['GET'])
def api_seasonality_items():
    """
    API endpoint for seasonality page to get items filtered by vendor's shopping categories.
    Query params:
        - start_date: YYYY-MM-DD
        - end_date: YYYY-MM-DD
        - categories: Comma-separated list of shoppingCategory values (e.g., 'fashion,beauty')
        - subcategories: Comma-separated list of shoppingSubcategory values (e.g., 'casual wear,skincare')
    """
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        categories_str = request.args.get('categories', '')
        subcategories_str = request.args.get('subcategories', '')

        if not start_date_str or not end_date_str:
            return jsonify({'success': False, 'error': 'start_date and end_date are required'}), 400

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)

        # Parse categories and subcategories from comma-separated strings
        categories = [c.strip() for c in categories_str.split(',') if c.strip()] if categories_str else None
        subcategories = [s.strip() for s in subcategories_str.split(',') if s.strip()] if subcategories_str else None

        pipeline = get_seasonality_items_pipeline(start_date, end_date, categories, subcategories)
        results = list(orders_collection.aggregate(pipeline))
        results = serialize_doc(results)

        display_pipeline = serialize_doc(pipeline)

        return jsonify({
            'success': True,
            'data': results,
            'pipeline': display_pipeline,
            'count': len(results),
            'date_range': {
                'start': start_date_str,
                'end': end_date_str
            },
            'filters': {
                'categories': categories,
                'subcategories': subcategories
            }
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


@app.route('/api/seasonality/event/items', methods=['GET'])
def api_seasonality_event_items():
    """
    API endpoint for seasonality page to get items filtered by seasonal event category paths.
    Uses the seasonal_event_category_mapping.py to filter items based on event.

    Query params:
        - start_date: YYYY-MM-DD
        - end_date: YYYY-MM-DD
        - event_key: Event identifier (e.g., 'valentines_day', 'ramadan', 'mothers_day')
        - category_paths: JSON array of category path objects (alternative to event_key)
    """
    try:
        from seasonal_event_category_mapping import get_event_category_paths, get_event_name

        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        event_key = request.args.get('event_key', '')
        category_paths_str = request.args.get('category_paths', '')

        if not start_date_str or not end_date_str:
            return jsonify({'success': False, 'error': 'start_date and end_date are required'}), 400

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)

        # Get category paths from event_key or directly from parameter
        category_paths = None
        event_name = None

        if event_key:
            category_paths = get_event_category_paths(event_key)
            event_name = get_event_name(event_key)
        elif category_paths_str:
            import json
            category_paths = json.loads(category_paths_str)

        pipeline = get_seasonality_items_by_event_pipeline(start_date, end_date, category_paths)
        results = list(orders_collection.aggregate(pipeline))
        results = serialize_doc(results)

        display_pipeline = serialize_doc(pipeline)

        return jsonify({
            'success': True,
            'data': results,
            'pipeline': display_pipeline,
            'count': len(results),
            'date_range': {
                'start': start_date_str,
                'end': end_date_str
            },
            'event': {
                'key': event_key,
                'name': event_name,
                'category_paths': category_paths
            }
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


@app.route('/api/seasonality/event/vendors', methods=['GET'])
def api_seasonality_event_vendors():
    """
    API endpoint for seasonality page to get vendors filtered by seasonal event category paths.
    Uses the seasonal_event_category_mapping.py to filter vendors based on event.

    Query params:
        - start_date: YYYY-MM-DD
        - end_date: YYYY-MM-DD
        - event_key: Event identifier (e.g., 'valentines_day', 'ramadan', 'mothers_day')
        - category_paths: JSON array of category path objects (alternative to event_key)
    """
    try:
        from seasonal_event_category_mapping import get_event_category_paths, get_event_name

        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        event_key = request.args.get('event_key', '')
        category_paths_str = request.args.get('category_paths', '')

        if not start_date_str or not end_date_str:
            return jsonify({'success': False, 'error': 'start_date and end_date are required'}), 400

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)

        # Get category paths from event_key or directly from parameter
        category_paths = None
        event_name = None

        if event_key:
            category_paths = get_event_category_paths(event_key)
            event_name = get_event_name(event_key)
        elif category_paths_str:
            import json
            category_paths = json.loads(category_paths_str)

        pipeline = get_seasonality_vendors_by_event_pipeline(start_date, end_date, category_paths)
        results = list(orders_collection.aggregate(pipeline))
        results = serialize_doc(results)

        display_pipeline = serialize_doc(pipeline)

        return jsonify({
            'success': True,
            'data': results,
            'pipeline': display_pipeline,
            'count': len(results),
            'date_range': {
                'start': start_date_str,
                'end': end_date_str
            },
            'event': {
                'key': event_key,
                'name': event_name,
                'category_paths': category_paths
            }
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


@app.route('/api/seasonality/event/historical-items', methods=['GET'])
def api_seasonality_event_historical_items():
    """
    Get best-selling items for an event in previous years.
    Uses per-year event dates from the mapping to query correct date ranges.

    Query params:
        - event_key: Event identifier (required)
        - current_year: Current year to exclude (optional, default=current year)
    """
    try:
        from seasonal_event_category_mapping import (
            get_event_category_paths, get_event_name, get_event_dates
        )

        event_key = request.args.get('event_key', '')
        current_year = int(request.args.get('current_year', datetime.now().year))

        if not event_key:
            return jsonify({'success': False, 'error': 'event_key is required'}), 400

        event_name = get_event_name(event_key)
        category_paths = get_event_category_paths(event_key)
        dates = get_event_dates(event_key)

        if not dates:
            return jsonify({
                'success': True,
                'event_key': event_key,
                'event_name': event_name,
                'years': {},
                'message': 'No date mapping available for this event'
            })

        years_data = {}
        for year, date_info in sorted(dates.items()):
            if year >= current_year:
                continue

            event_start = datetime.strptime(date_info["start"], '%Y-%m-%d')
            duration = date_info.get("duration_days", 1)

            range_start = event_start - timedelta(days=30)
            range_end = event_start + timedelta(days=duration + 7)

            pipeline = get_seasonality_items_by_event_pipeline(
                range_start, range_end, category_paths
            )
            # Override limit to 10
            for stage in pipeline:
                if "$limit" in stage:
                    stage["$limit"] = 10
                    break

            results = list(orders_collection.aggregate(pipeline))
            results = serialize_doc(results)

            years_data[str(year)] = {
                'date_range': {
                    'start': range_start.strftime('%Y-%m-%d'),
                    'end': range_end.strftime('%Y-%m-%d')
                },
                'event_start': date_info["start"],
                'items': results
            }

        return jsonify({
            'success': True,
            'event_key': event_key,
            'event_name': event_name,
            'years': years_data
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


@app.route('/api/seasonality/events', methods=['GET'])
def api_seasonality_events():
    """
    API endpoint to get all available seasonal events and their category mappings.
    """
    try:
        from seasonal_event_category_mapping import EVENT_CATEGORY_MAPPING, get_events_by_category

        category_filter = request.args.get('category', '')

        if category_filter:
            # Filter events by category
            event_keys = get_events_by_category(category_filter)
            events = {k: EVENT_CATEGORY_MAPPING[k] for k in event_keys if k in EVENT_CATEGORY_MAPPING}
        else:
            events = EVENT_CATEGORY_MAPPING

        return jsonify({
            'success': True,
            'events': events,
            'count': len(events)
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


# -------------------------------------------------------------------------------------------------------------- #
def get_top_item_for_path(start_date, end_date, category_path, return_pipeline=False):
    """
    Get the TOP 1 selling item for a specific category path.
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
                "users_count": {"$addToSet": "$_user"}
            }
        },
        {"$lookup": {"from": "Items", "localField": "_id.item_id", "foreignField": "_id", "as": "item"}},
        {"$unwind": "$item"},
        {"$lookup": {"from": "Vendors", "localField": "_id.vendor_id", "foreignField": "_id", "as": "vendor"}},
        {"$unwind": "$vendor"}
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
                "users_count": {"$size": "$users_count"}
            }
        },
        {"$sort": {"total_qty": -1}},
        {"$limit": 1}
    ])

    if return_pipeline:
        return serialize_doc(pipeline)

    result = list(orders_collection.aggregate(pipeline))
    return serialize_doc(result[0]) if result else None


@app.route('/api/seasonality/top-items-per-path', methods=['GET'])
def api_top_items_per_path():
    """
    Get TOP 1 item for each category path across all events.

    Query params:
        - start_date: YYYY-MM-DD
        - end_date: YYYY-MM-DD
        - events: Comma-separated event keys (optional)
    """
    try:
        from seasonal_event_category_mapping import EVENT_CATEGORY_MAPPING

        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        events_str = request.args.get('events', '')

        if not start_date_str or not end_date_str:
            return jsonify({'success': False, 'error': 'start_date and end_date are required'}), 400

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)

        # Filter events if specified
        event_keys = [e.strip() for e in events_str.split(',') if e.strip()] if events_str else None
        events = {k: EVENT_CATEGORY_MAPPING[k] for k in event_keys} if event_keys else EVENT_CATEGORY_MAPPING

        results = []
        for event_key, event_data in events.items():
            event_name = event_data.get("name", event_key)

            for path in event_data.get("category_paths", []):
                top_item = get_top_item_for_path(start_date, end_date, path)

                path_label = " > ".join(filter(None, [
                    path.get("shoppingCategory"),
                    path.get("shoppingSubcategory"),
                    path.get("itemCategory"),
                    path.get("itemSubcategory")
                ]))

                results.append({
                    "event_key": event_key,
                    "event_name": event_name,
                    "category_path": path,
                    "path_label": path_label,
                    "top_item": top_item
                })

        return jsonify({
            'success': True,
            'data': results,
            'count': len(results),
            'items_found': sum(1 for r in results if r['top_item']),
            'date_range': {'start': start_date_str, 'end': end_date_str}
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


@app.route('/api/seasonality/top-items-cached', methods=['GET'])
def api_top_items_cached():
    """
    Read pre-computed top items per category path from local MongoDB.
    Results are written by run_seasonality_pipeline.py.

    Query params:
        - events: Comma-separated event keys (optional filter)
    """
    try:
        events_str = request.args.get('events', '')

        query = {}
        if events_str:
            event_keys = [e.strip() for e in events_str.split(',') if e.strip()]
            query['event_key'] = {'$in': event_keys}

        docs = list(
            seasonality_results_collection.find(query, {'_id': 0})
            .sort([('event_key', 1), ('path_label', 1)])
        )
        docs = serialize_doc(docs)

        return jsonify({
            'success': True,
            'data': docs,
            'count': len(docs),
            'items_found': sum(1 for d in docs if d.get('top_item')),
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


@app.route('/api/seasonality/pipeline-status', methods=['GET'])
def api_seasonality_pipeline_status():
    """
    Return status info about the pre-computed seasonality cache.
    """
    try:
        total = seasonality_results_collection.count_documents({})

        # Get last updated timestamp
        last_doc = seasonality_results_collection.find_one(
            {}, {'updated_at': 1, 'date_range': 1},
            sort=[('updated_at', -1)]
        )
        last_updated = None
        date_range = None
        if last_doc:
            last_updated = serialize_doc(last_doc.get('updated_at'))
            date_range = last_doc.get('date_range')

        # Per-event breakdown
        pipeline = [
            {'$group': {
                '_id': '$event_key',
                'count': {'$sum': 1},
                'items_found': {'$sum': {'$cond': [{'$ne': ['$top_item', None]}, 1, 0]}},
                'event_name': {'$first': '$event_name'},
            }},
            {'$sort': {'_id': 1}},
        ]
        breakdown = list(seasonality_results_collection.aggregate(pipeline))
        breakdown = serialize_doc(breakdown)

        return jsonify({
            'success': True,
            'total_docs': total,
            'last_updated': last_updated,
            'date_range': date_range,
            'events': breakdown,
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


@app.route('/api/seasonality/debug-path', methods=['GET'])
def api_debug_path():
    """
    DEBUG: Test a single category path and show the pipeline.

    Query params:
        - start_date: YYYY-MM-DD
        - end_date: YYYY-MM-DD
        - shoppingCategory: e.g., 'kids'
        - shoppingSubcategory: e.g., 'toys and games' (optional)
        - itemCategory: e.g., 'toy figure' (optional)
        - itemSubcategory: (optional)
    """
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        if not start_date_str or not end_date_str:
            return jsonify({'success': False, 'error': 'start_date and end_date are required'}), 400

        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)

        # Build category path from query params
        category_path = {}
        if request.args.get('shoppingCategory'):
            category_path['shoppingCategory'] = request.args.get('shoppingCategory')
        if request.args.get('shoppingSubcategory'):
            category_path['shoppingSubcategory'] = request.args.get('shoppingSubcategory')
        if request.args.get('itemCategory'):
            category_path['itemCategory'] = request.args.get('itemCategory')
        if request.args.get('itemSubcategory'):
            category_path['itemSubcategory'] = request.args.get('itemSubcategory')

        # Get pipeline for debugging
        pipeline = get_top_item_for_path(start_date, end_date, category_path, return_pipeline=True)

        # Get actual result
        top_item = get_top_item_for_path(start_date, end_date, category_path)

        # Also count how many orders exist in date range (without category filter)
        orders_count_pipeline = [
            {"$match": {"createdAt": {"$gte": start_date, "$lte": end_date}}},
            {"$count": "total"}
        ]
        orders_count = list(orders_collection.aggregate(orders_count_pipeline))
        total_orders = orders_count[0]['total'] if orders_count else 0

        return jsonify({
            'success': True,
            'debug': {
                'category_path_used': category_path,
                'date_range': {
                    'start': start_date_str,
                    'end': end_date_str,
                    'start_parsed': start_date.isoformat(),
                    'end_parsed': end_date.isoformat()
                },
                'total_orders_in_date_range': total_orders,
                'pipeline': pipeline
            },
            'result': top_item
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


@app.route('/vendors')
def vendors_page():
    """Vendor-level view page."""
    default_end = datetime.now()
    default_start = default_end - timedelta(days=30)
    return render_template('vendors.html',
                         default_start=default_start.strftime('%Y-%m-%d'),
                         default_end=default_end.strftime('%Y-%m-%d'))


@app.route('/items')
def items_page():
    """Item-level view page."""
    default_end = datetime.now()
    default_start = default_end - timedelta(days=30)
    return render_template('items.html',
                         default_start=default_start.strftime('%Y-%m-%d'),
                         default_end=default_end.strftime('%Y-%m-%d'))


@app.route('/seasonality')
def seasonality_page():
    """Egypt seasonality trends page."""
    current_year = datetime.now().year
    return render_template('seasonality.html', current_year=current_year)


@app.route('/trends')
def trends_page():
    """TikTok trends and product suggestions page."""
    default_end = datetime.now()
    default_start = default_end - timedelta(days=30)
    return render_template('trends.html',
                         default_start=default_start.strftime('%Y-%m-%d'),
                         default_end=default_end.strftime('%Y-%m-%d'))


@app.route('/api/trends/suggestions', methods=['GET'])
def api_trends_suggestions():
    """
    API endpoint to get product suggestions based on TikTok trending hashtags.
    Query params:
        - days_back: Number of days to analyze (default: 30)
        - top_categories: Number of top categories to return (default: 5)
        - items_per_category: Items per category (default: 10)
        - vendors_per_category: Vendors per category (default: 10)
    """
    try:
        from test_tiktok_trends import get_tiktok_trend_suggestions

        days_back = int(request.args.get('days_back', 30))
        top_categories = int(request.args.get('top_categories', 5))
        items_per_category = int(request.args.get('items_per_category', 10))
        vendors_per_category = int(request.args.get('vendors_per_category', 10))

        suggestions = get_tiktok_trend_suggestions(
            days_back=days_back,
            top_categories=top_categories,
            items_per_category=items_per_category,
            vendors_per_category=vendors_per_category
        )

        return jsonify({
            'success': True,
            'data': suggestions
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400

# -------------------------------------------------------------------------------------------------------------- #
@app.route('/api/trends/hashtags', methods=['GET'])
def api_trends_hashtags():
    """
    API endpoint to get trending hashtags mapped to categories.
    """
    try:
        from test_tiktok_trends import (
            get_trending_hashtags_from_api,
            analyze_trending_hashtags,
            get_trending_categories
        )

        # Get trending hashtags (will use mock data if API fails)
        hashtags = get_trending_hashtags_from_api()

        # Analyze and map to categories
        analyzed = analyze_trending_hashtags(hashtags)

        # Get aggregated trending categories
        trending = get_trending_categories(analyzed)

        # Transform categories dict to array format for frontend
        categories_list = [
            {
                'category': cat_name,
                'score': round(cat_data['score'], 2),
                'hashtags': cat_data['hashtags'][:5],
                'views': cat_data['views']
            }
            for cat_name, cat_data in trending['categories'].items()
        ]

        subcategories_list = [
            {
                'subcategory': subcat_name,
                'score': round(subcat_data['score'], 2),
                'hashtags': subcat_data['hashtags'][:5]
            }
            for subcat_name, subcat_data in trending['subcategories'].items()
        ]

        # Transform analyzed hashtags for frontend
        hashtags_list = [
            {
                'hashtag': h['hashtag'],
                'views': h.get('views', 0),
                'mapped_category': h['categories'][0] if h['categories'] else None,
                'categories': h['categories'],
                'confidence': h.get('confidence', 0)
            }
            for h in analyzed[:20]
        ]

        return jsonify({
            'success': True,
            'data': {
                'hashtags': hashtags_list,
                'trending_categories': categories_list,
                'trending_subcategories': subcategories_list
            }
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


@app.route('/api/trends/refresh', methods=['POST'])
def api_trends_refresh():
    """
    Fetch fresh TikTok trending data, save to local MongoDB, and return it.
    This is the only endpoint that calls the live TikTok API.
    """
    try:
        from test_tiktok_trends import (
            get_trending_hashtags_from_api,
            analyze_trending_hashtags,
            get_trending_categories
        )

        # Get trending hashtags (will use mock data if API fails)
        hashtags = get_trending_hashtags_from_api()

        # Analyze and map to categories
        analyzed = analyze_trending_hashtags(hashtags)

        # Get aggregated trending categories
        trending = get_trending_categories(analyzed)

        # Transform for storage/response
        categories_list = [
            {
                'category': cat_name,
                'score': round(cat_data['score'], 2),
                'hashtags': cat_data['hashtags'][:5],
                'views': cat_data['views']
            }
            for cat_name, cat_data in trending['categories'].items()
        ]

        subcategories_list = [
            {
                'subcategory': subcat_name,
                'score': round(subcat_data['score'], 2),
                'hashtags': subcat_data['hashtags'][:5]
            }
            for subcat_name, subcat_data in trending['subcategories'].items()
        ]

        hashtags_list = [
            {
                'hashtag': h['hashtag'],
                'views': h.get('views', 0),
                'mapped_category': h['categories'][0] if h['categories'] else None,
                'categories': h['categories'],
                'confidence': h.get('confidence', 0)
            }
            for h in analyzed[:20]
        ]

        # Save to local MongoDB
        doc = {
            'hashtags': hashtags_list,
            'trending_categories': categories_list,
            'trending_subcategories': subcategories_list,
            'updated_at': datetime.now(),
        }

        tiktok_hashtags_collection.update_one(
            {'_id': 'latest'},
            {'$set': doc},
            upsert=True
        )

        return jsonify({
            'success': True,
            'data': {
                'hashtags': hashtags_list,
                'trending_categories': categories_list,
                'trending_subcategories': subcategories_list
            },
            'updated_at': datetime.now().isoformat(),
            'source': 'fresh'
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


@app.route('/api/trends/hashtags-cached', methods=['GET'])
def api_trends_hashtags_cached():
    """
    Read pre-cached TikTok trending data from local MongoDB.
    Returns the latest saved snapshot without calling any external API.
    """
    try:
        doc = tiktok_hashtags_collection.find_one({'_id': 'latest'})

        if not doc:
            return jsonify({
                'success': True,
                'data': {'hashtags': [], 'trending_categories': [], 'trending_subcategories': []},
                'updated_at': None,
                'source': 'cache',
                'message': 'No cached data. Click "Analyze Trends" to fetch fresh data.'
            })

        return jsonify({
            'success': True,
            'data': {
                'hashtags': doc.get('hashtags', []),
                'trending_categories': doc.get('trending_categories', []),
                'trending_subcategories': doc.get('trending_subcategories', [])
            },
            'updated_at': serialize_doc(doc.get('updated_at')),
            'source': 'cache'
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


@app.route('/api/trends/category/<category>', methods=['GET'])
def api_trends_by_category(category):
    """
    API endpoint to get vendors and items for a specific trending category.
    Query params:
        - days_back: Number of days to analyze (default: 30)
        - limit: Maximum results (default: 20)
    """
    try:
        from test_tiktok_trends import get_trending_vendors, get_trending_items

        days_back = int(request.args.get('days_back', 30))
        limit = int(request.args.get('limit', 20))

        vendors = get_trending_vendors(
            categories=[category],
            days_back=days_back,
            limit=limit
        )

        items = get_trending_items(
            categories=[category],
            days_back=days_back,
            limit=limit
        )

        return jsonify({
            'success': True,
            'data': {
                'category': category,
                'vendors': vendors,
                'items': items,
                'vendor_count': len(vendors),
                'item_count': len(items)
            }
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


@app.route('/api/feed/nearest-event', methods=['GET'])
def api_feed_nearest_event():
    """
    Get the nearest upcoming or currently active seasonal event.
    Drives the Event Picks and Previously Worked sections of the feed dashboard.
    """
    try:
        from seasonal_event_category_mapping import get_nearest_upcoming_event

        event = get_nearest_upcoming_event()

        return jsonify({
            'success': True,
            'event': event
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


@app.route('/api/feed/trending-up', methods=['GET'])
def api_feed_trending_up():
    """
    Get items with growing momentum by comparing two consecutive periods.
    Compares last N days vs previous N days, returns items with >=20% growth
    or new entrants with >=3 qty.

    Query params:
        - days: Period length in days (default: 7)
        - limit: Max items to return (default: 20)
    """
    try:
        days = int(request.args.get('days', 7))
        limit = int(request.args.get('limit', 20))

        now = datetime.now()
        recent_end = now
        recent_start = now - timedelta(days=days)
        prev_end = recent_start
        prev_start = prev_end - timedelta(days=days)

        # Run pipelines for both periods
        recent_pipeline = get_top_items_pipeline(recent_start, recent_end)
        prev_pipeline = get_top_items_pipeline(prev_start, prev_end)

        recent_results = list(orders_collection.aggregate(recent_pipeline))
        recent_results = serialize_doc(recent_results)

        prev_results = list(orders_collection.aggregate(prev_pipeline))
        prev_results = serialize_doc(prev_results)

        # Build lookup of previous period by item_id
        prev_map = {}
        for item in prev_results:
            if item.get('item_id'):
                prev_map[item['item_id']] = item

        # Compare and find trending up items
        trending = []
        for item in recent_results:
            item_id = item.get('item_id')
            if not item_id:
                continue

            current_qty = item.get('total_qty', 0)
            prev_item = prev_map.get(item_id)

            if prev_item:
                prev_qty = prev_item.get('total_qty', 0)
                if prev_qty > 0:
                    delta_pct = round(((current_qty - prev_qty) / prev_qty) * 100, 1)
                else:
                    delta_pct = 100.0
                delta_qty = current_qty - prev_qty
                is_new = False

                # Only include if >=20% growth
                if delta_pct < 20:
                    continue
            else:
                # New entrant - not in previous period
                if current_qty < 3:
                    continue
                prev_qty = 0
                delta_qty = current_qty
                delta_pct = 100.0
                is_new = True

            item['prev_qty'] = prev_qty
            item['delta_qty'] = delta_qty
            item['delta_pct'] = delta_pct
            item['is_new'] = is_new
            trending.append(item)

        # Sort by delta_pct descending
        trending.sort(key=lambda x: x['delta_pct'], reverse=True)
        trending = trending[:limit]

        return jsonify({
            'success': True,
            'data': trending,
            'count': len(trending),
            'periods': {
                'recent': {
                    'start': recent_start.strftime('%Y-%m-%d'),
                    'end': recent_end.strftime('%Y-%m-%d')
                },
                'previous': {
                    'start': prev_start.strftime('%Y-%m-%d'),
                    'end': prev_end.strftime('%Y-%m-%d')
                }
            }
        })
    except Exception as e:
        import traceback
        return jsonify({'success': False, 'error': str(e), 'trace': traceback.format_exc()}), 400


@app.route('/api/generate-feed', methods=['POST'])
def api_generate_feed():
    """
    API endpoint to generate AI-powered feed recommendations.
    Uses OpenAI to analyze top vendors, items, events, and TikTok trends
    to create personalized feed suggestions.
    """
    try:
        data = request.get_json()

        include_vendors = data.get('include_vendors', True)
        include_items = data.get('include_items', True)
        include_events = data.get('include_events', True)
        include_trends = data.get('include_trends', True)

        vendors = data.get('vendors', [])
        items = data.get('items', [])
        hashtags = data.get('hashtags', [])
        trending_categories = data.get('trending_categories', [])
        seasonality = data.get('seasonality', [])
        date_range = data.get('date_range', {})

        # Build context for AI
        context_parts = []
        today = datetime.now().strftime('%Y-%m-%d')
        context_parts.append(f"Today's date: {today}")

        # Date range info
        start_date = date_range.get('start', 'N/A')
        end_date = date_range.get('end', 'N/A')
        days = date_range.get('days', 7)
        date_label = f"{start_date} to {end_date} ({days} days)"

        if include_vendors and vendors:
            vendor_info = []
            for v in vendors[:10]:
                vendor_info.append(f"- {v.get('vendor_name', 'Unknown')} ({v.get('vendor_shoppingCategory', 'N/A')}): {v.get('orders_count', 0)} orders")
            context_parts.append(f"TOP PERFORMING VENDORS ({date_label}):\n" + "\n".join(vendor_info))

        if include_items and items:
            item_info = []
            for it in items[:10]:
                item_info.append(f"- {it.get('item_name', 'Unknown')[:50]}: {it.get('total_qty', 0)} sold, {it.get('price', 0)} EGP")
            context_parts.append(f"TOP SELLING ITEMS ({date_label}):\n" + "\n".join(item_info))

        if include_events:
            # Egypt events calendar
            egypt_events = [
                {"name": "Ramadan", "date": "2025-02-28", "categories": ["fashion", "food", "home"]},
                {"name": "Eid al-Fitr", "date": "2025-03-30", "categories": ["fashion", "beauty", "food"]},
                {"name": "Mother's Day", "date": "2025-03-21", "categories": ["beauty", "fashion", "jewelry"]},
                {"name": "Eid al-Adha", "date": "2025-06-06", "categories": ["fashion", "food", "home"]},
                {"name": "Back to School", "date": "2025-09-01", "categories": ["fashion", "electronics", "stationery"]},
                {"name": "Singles Day", "date": "2025-11-11", "categories": ["all"]},
                {"name": "Black Friday", "date": "2025-11-28", "categories": ["all"]},
                {"name": "Valentine's Day", "date": "2026-02-14", "categories": ["beauty", "fashion", "jewelry"]},
            ]
            upcoming = [e for e in egypt_events if e['date'] >= today][:3]
            if upcoming:
                event_info = [f"- {e['name']} ({e['date']}): Focus on {', '.join(e['categories'])}" for e in upcoming]
                context_parts.append("UPCOMING EVENTS IN EGYPT:\n" + "\n".join(event_info))

        if include_events and seasonality:
            # Add cached seasonality top items per event
            seasonality_info = []
            by_event = {}
            for s in seasonality:
                event_name = s.get('event_name', 'Unknown')
                if event_name not in by_event:
                    by_event[event_name] = []
                if s.get('top_item'):
                    by_event[event_name].append(s)
            for event_name, items_list in list(by_event.items())[:5]:
                if items_list:
                    item_strs = [f"  - {it['top_item'].get('item_name', 'Unknown')[:40]} ({it.get('path_label', '')})" for it in items_list[:3]]
                    seasonality_info.append(f"{event_name}:\n" + "\n".join(item_strs))
            if seasonality_info:
                context_parts.append("TOP SELLING ITEMS PER SEASONAL EVENT (cached):\n" + "\n".join(seasonality_info))

        if include_trends and (hashtags or trending_categories):
            trend_info = []
            if trending_categories:
                for cat in trending_categories[:5]:
                    trend_info.append(f"- {cat.get('category', 'Unknown')}: score {cat.get('score', 0)}")
            if hashtags:
                top_tags = [f"#{h.get('hashtag', h.get('name', ''))}" for h in hashtags[:10]]
                trend_info.append(f"Trending hashtags: {', '.join(top_tags)}")
            context_parts.append("TIKTOK TRENDS:\n" + "\n".join(trend_info))

        context = "\n\n".join(context_parts)

        # Generate feed with OpenAI
        prompt = f"""You are a feed curation expert for Botit, an e-commerce platform in Egypt.
Based on the following data, create TODAY'S FEED RECOMMENDATIONS for the Botit app.

{context}

Generate a structured feed plan with these sections:
1. **Featured Vendors** - Which vendors to highlight and why
2. **Hero Products** - Top items to feature prominently
3. **Trending Now** - Products aligned with TikTok trends
4. **Seasonal Picks** - Products relevant to upcoming events/seasons
5. **Feed Mix Strategy** - Recommended ratio and placement strategy

Be specific with vendor/product names from the data provided. Keep it actionable and concise.
Format with clear headers and bullet points."""

        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a feed curation expert for an Egyptian e-commerce platform. Create actionable, specific feed recommendations."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=1500,
            temperature=0.7
        )

        feed_content = response.choices[0].message.content

        return jsonify({
            'success': True,
            'feed': feed_content,
            'generated_at': datetime.now().isoformat(),
            'sources': {
                'vendors': len(vendors),
                'items': len(items),
                'hashtags': len(hashtags),
                'events_included': include_events
            }
        })

    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'trace': traceback.format_exc()
        }), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
