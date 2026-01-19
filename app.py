import os
from datetime import datetime, timedelta
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'dev-secret-key')

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.get_database("botitprod")

# Collections
items_collection = db["Items"]
orders_collection = db["Orders"]
vendors_collection = db["Vendors"]


def get_top_vendors_pipeline(start_date, end_date):
    """
    Aggregation pipeline to get top vendors based on orders within date range.
    Returns: vendor_id, vendor_name, vendor_image, vendor_shopcat, total_qty, orders_count, users_count, items_count
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
                "vendor_shopcat": "$vendor.shoppingCategory",
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


def get_top_items_pipeline(start_date, end_date):
    """
    Aggregation pipeline to get top items based on orders within date range.
    Returns: item_id, item_name, vendor_id, vendor_name, vendor_image, vendor_shopcat, price, total_qty, orders_count, users_count
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
                "vendor_shopcat": "$vendor.shoppingCategory",
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


if __name__ == '__main__':
    app.run(debug=True, port=5000)
