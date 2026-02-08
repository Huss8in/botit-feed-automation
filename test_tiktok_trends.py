"""
TikTok Trending Hashtags Test File
==================================
This file tests the integration of TikTok trending hashtags to suggest
relevant items and vendors based on current trends.

Free API Options:
1. Mock data (default) - for testing the logic
2. Web scraping TikTok's discover page (may be blocked)
3. Free tier of RapidAPI TikTok APIs (limited requests)

To use a real API later, implement the get_trending_hashtags() function
with your preferred data source.
"""

import os
import re
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from pymongo import MongoClient
from dotenv import load_dotenv
from bson import ObjectId

# Load environment variables
load_dotenv()

# MongoDB connection
mongo_uri = os.getenv("MONGO_URI")
client = MongoClient(mongo_uri)
db = client.get_database("botitprod")
orders_collection = db["Orders"]
vendors_collection = db["Vendors"]
items_collection = db["Items"]

# Internal users to exclude from analytics
INTERNAL_USER_IDS = [
    ObjectId("6245a6f00db8496ee0636dec"),  # Adam Mowafi
    ObjectId("62bacade7566e0353cbe3f21"),  # Amr Nashaat
    ObjectId("62f14c968a41a318486e146a"),  # Gabriela Asquith
    ObjectId("630b4e0295e48e2c08a9e287"),  # Amy Mowafi
    ObjectId("638de14ea956cd18f4a95bf5"),  # Waleed Mowafi
    ObjectId("61e836019c9def2928a69cc0"),  # Farah Shadi
    ObjectId("65d9aaa83c7864113ca50c6c"),  # Habiba Ahmed
    ObjectId("62f0edda95b80b0628644f59"),  # Timmy Mowafi
    ObjectId("626a615cfde897251443d22b"),  # Tarek Hamdy
    ObjectId("62445d7f1fe1ba4c8ca13ff7"),  # Tests Ng Test
]


# ============================================================================
# HASHTAG TO CATEGORY MAPPING
# ============================================================================

# Keywords that map TikTok hashtags to shopping categories
# Includes English, Arabic transliteration, and Egypt-specific terms
HASHTAG_CATEGORY_MAPPING = {
    # Fashion keywords (Egypt-focused)
    "fashion": ["fashion", "ootd", "outfit", "style", "clothing", "dress", "clothes",
                "fashiontiktok", "fashiontrends", "streetwear", "mensfashion", "womensfashion",
                "hijabfashion", "hijabstyle", "hijab", "modestfashion", "modest", "abaya", "kaftan",
                "egyptianfashion", "ootdegypt", "arabfashion", "arabstyle", "eidoutfit",
                "موضة", "حجاب", "عباية", "ملابس", "ستايل"],

    # Beauty keywords
    "beauty": ["beauty", "makeup", "skincare", "cosmetics", "beautytips", "makeuptutorial",
               "skincareroutine", "beautyhacks", "glowup", "lipstick", "foundation",
               "skincaretiktok", "beautytiktok", "grwm", "getreadywithme",
               "makeupegypt", "arabicmakeup", "arabbeauty", "مكياج", "جمال", "عناية"],

    # Electronics keywords
    "electronics": ["tech", "technology", "gadgets", "iphone", "samsung", "laptop",
                    "gaming", "pc", "smartphone", "techreview", "unboxing", "techtok",
                    "techegypt", "iphoneegypt", "موبايل", "تكنولوجيا"],

    # Food/Groceries keywords (Egypt-focused)
    "groceries": ["food", "foodie", "cooking", "recipe", "healthy", "healthyfood",
                  "mealprep", "groceryhaul", "foodtiktok", "whatieatinaday",
                  "ramadan", "ramadanfood", "iftar", "suhoor", "سحور", "افطار",
                  "egyptfood", "اكل", "طبخ", "وصفات", "رمضان"],

    # Restaurants keywords (Egypt-focused)
    "restaurants": ["foodreview", "restaurant", "cafe", "coffee", "dessert", "burger",
                    "pizza", "sushi", "streetfood", "foodtour", "mukbang", "asmrfood",
                    "cairorestaurants", "streetfoodegypt", "egyptianfood", "مطاعم", "كافيه"],

    # Home & Garden keywords
    "home and garden": ["home", "homedecor", "interior", "furniture", "kitchen",
                        "organization", "cleaning", "cleaningtiktok", "homestyling",
                        "roomdecor", "apartmenttour", "hometour", "ramadandecor",
                        "organizewithme", "kitchenhacks", "ديكور", "منزل", "مطبخ"],

    # Kids keywords (Egypt-focused)
    "kids": ["kids", "baby", "parenting", "toys", "children", "momlife", "dadlife",
             "babytiktok", "toddler", "newborn", "pregnancy", "momtok",
             "kidsfashion", "toysreview", "eidgiftsforkids", "اطفال", "العاب", "امومة"],

    # Sports keywords
    "sports": ["fitness", "gym", "workout", "sports", "exercise", "fitnesstiktok",
               "gymtok", "running", "yoga", "crossfit", "bodybuilding", "health",
               "gymegypt", "proteinegypt", "رياضة", "جيم", "لياقة"],

    # Entertainment keywords
    "entertainment": ["gaming", "music", "books", "booktok", "movies", "netflix",
                      "spotify", "playstation", "xbox", "gamer", "bookclub", "reading",
                      "العاب", "موسيقى", "كتب", "افلام"],

    # Flowers & Gifts keywords (Egypt-focused)
    "flowers and gifts": ["gifts", "giftideas", "flowers", "bouquet", "valentines",
                          "mothersday", "birthday", "anniversary", "eidgifts", "ramadangifts",
                          "valentinesegypt", "هدايا", "ورد", "عيد"],

    # Pet Care keywords
    "pet care": ["pets", "dogs", "cats", "puppy", "kitten", "dogsoftiktok",
                 "catsoftiktok", "petcare", "pettok", "animals", "petsofegypt",
                 "حيوانات", "قطط", "كلاب"],

    # Pharmacies/Health keywords
    "pharmacies": ["health", "medicine", "pharmacy", "vitamins", "supplements",
                   "wellness", "selfcare", "mentalhealth", "healthcare", "صحة", "دواء"],

    # Health & Nutrition keywords
    "health and nutrition": ["nutrition", "protein", "diet", "weightloss", "keto",
                             "vegan", "supplements", "preworkout", "healthylifestyle",
                             "proteinegypt", "تغذية", "بروتين", "دايت"],

    # Automotive keywords
    "automotive": ["cars", "car", "auto", "driving", "cartok", "carreview",
                   "automotive", "motorcycle", "vehicle", "سيارات", "موتوسيكل"],

    # Stationary keywords (Egypt-focused)
    "stationary": ["stationary", "backtoschool", "school", "studying", "studytok",
                   "planner", "journaling", "bulletjournal", "aesthetic", "artsy",
                   "schoolsupplies", "studyegypt", "مدرسة", "ادوات", "دراسة"]
}

# Subcategory mapping for more specific matches
HASHTAG_SUBCATEGORY_MAPPING = {
    # Fashion subcategories
    "sportswear": ["activewear", "sportswear", "gymwear", "athleisure", "workout"],
    "casual wear": ["casualwear", "everyday", "streetstyle", "casual"],
    "footwear": ["shoes", "sneakers", "heels", "boots", "sandals", "footwear"],
    "jewelry": ["jewelry", "accessories", "necklace", "earrings", "bracelet", "rings"],
    "swimwear": ["swimwear", "bikini", "beach", "summer", "pool"],
    "religious wear": ["hijab", "abaya", "modest", "hijabstyle", "modestfashion"],

    # Beauty subcategories
    "skincare": ["skincare", "skincareroutine", "acne", "moisturizer", "serum", "sunscreen"],
    "cosmetics": ["makeup", "lipstick", "foundation", "mascara", "eyeshadow", "blush"],
    "haircare": ["haircare", "hairstyle", "hairgrowth", "shampoo", "conditioner"],
    "fragrances": ["perfume", "fragrance", "cologne", "scent"],

    # Restaurant subcategories
    "desserts": ["dessert", "cake", "chocolate", "icecream", "sweets", "cookies"],
    "cafes": ["coffee", "cafe", "latte", "espresso", "coffeelover"],
    "healthy": ["healthy", "salad", "vegan", "keto", "cleaneating"],

    # Home subcategories
    "kitchenwear": ["kitchen", "cooking", "kitchengadgets", "cookware"],
    "home decor": ["homedecor", "decor", "interior", "aesthetic", "cozy"],
    "furniture": ["furniture", "sofa", "bed", "desk", "chair"],

    # Kids subcategories
    "toys and games": ["toys", "games", "lego", "dolls", "puzzle", "playtime"],
    "baby care": ["baby", "newborn", "babygear", "nursery", "breastfeeding"]
}

# Egyptian/Regional specific hashtag mappings
REGIONAL_HASHTAGS = {
    "ramadan": {
        "categories": ["groceries", "restaurants", "home and garden", "fashion"],
        "subcategories": ["supermarkets", "desserts", "home decor", "religious wear"]
    },
    "eid": {
        "categories": ["fashion", "flowers and gifts", "groceries", "kids"],
        "subcategories": ["casual wear", "gifts", "desserts", "toys and games"]
    },
    "summer": {
        "categories": ["fashion", "beauty", "sports", "electronics"],
        "subcategories": ["swimwear", "skincare", "water sports", "phones"]
    },
    "backtoschool": {
        "categories": ["stationary", "fashion", "electronics", "kids"],
        "subcategories": ["school supplies", "casual wear", "computers", "baby care"]
    },
    "wedding": {
        "categories": ["fashion", "beauty", "flowers and gifts", "jewelry"],
        "subcategories": ["designer wear", "cosmetics", "flowers", "jewelry"]
    }
}


# ============================================================================
# TRENDING HASHTAGS DATA SOURCES
# ============================================================================

def get_mock_trending_hashtags() -> List[Dict]:
    """
    Returns mock trending hashtags for Egypt product trends.
    Based on popular Egyptian TikTok shopping trends.
    """
    return [
        # Seasonal/Religious - High Impact in Egypt
        {"hashtag": "رمضان", "views": 25000000000, "category": "seasonal"},
        {"hashtag": "ramadan2025", "views": 18000000000, "category": "seasonal"},
        {"hashtag": "عيد", "views": 12000000000, "category": "seasonal"},
        {"hashtag": "eidoutfit", "views": 8000000000, "category": "fashion"},

        # Fashion - Egypt specific
        {"hashtag": "hijabstyle", "views": 9500000000, "category": "fashion"},
        {"hashtag": "modestfashion", "views": 7500000000, "category": "fashion"},
        {"hashtag": "ootdegypt", "views": 4200000000, "category": "fashion"},
        {"hashtag": "abaya", "views": 3800000000, "category": "fashion"},
        {"hashtag": "egyptianfashion", "views": 2500000000, "category": "fashion"},

        # Beauty - Popular in Egypt
        {"hashtag": "skincareroutine", "views": 6200000000, "category": "beauty"},
        {"hashtag": "makeupegypt", "views": 3500000000, "category": "beauty"},
        {"hashtag": "grwm", "views": 5800000000, "category": "beauty"},
        {"hashtag": "arabicmakeup", "views": 2800000000, "category": "beauty"},

        # Food & Restaurants
        {"hashtag": "egyptfood", "views": 4500000000, "category": "food"},
        {"hashtag": "cairorestaurants", "views": 2200000000, "category": "food"},
        {"hashtag": "streetfoodegypt", "views": 1800000000, "category": "food"},
        {"hashtag": "iftar", "views": 3500000000, "category": "food"},
        {"hashtag": "سحور", "views": 2800000000, "category": "food"},

        # Home & Living
        {"hashtag": "homedecor", "views": 5800000000, "category": "home"},
        {"hashtag": "ramadandecor", "views": 2500000000, "category": "home"},
        {"hashtag": "organizewithme", "views": 1900000000, "category": "home"},
        {"hashtag": "kitchenhacks", "views": 1700000000, "category": "home"},

        # Kids & Family
        {"hashtag": "momtok", "views": 3200000000, "category": "kids"},
        {"hashtag": "kidsfashion", "views": 2100000000, "category": "kids"},
        {"hashtag": "toysreview", "views": 1500000000, "category": "kids"},
        {"hashtag": "eidgiftsforkids", "views": 1200000000, "category": "kids"},

        # Electronics & Tech
        {"hashtag": "techegypt", "views": 1800000000, "category": "tech"},
        {"hashtag": "unboxing", "views": 4500000000, "category": "tech"},
        {"hashtag": "iphoneegypt", "views": 1200000000, "category": "tech"},

        # Health & Fitness
        {"hashtag": "gymegypt", "views": 1500000000, "category": "fitness"},
        {"hashtag": "healthylifestyle", "views": 2800000000, "category": "fitness"},
        {"hashtag": "proteinegypt", "views": 900000000, "category": "fitness"},

        # Shopping & Hauls
        {"hashtag": "shoppinghaul", "views": 5500000000, "category": "shopping"},
        {"hashtag": "egypthaul", "views": 1800000000, "category": "shopping"},
        {"hashtag": "affordablefinds", "views": 2200000000, "category": "shopping"},
        {"hashtag": "amazonegypt", "views": 1500000000, "category": "shopping"},

        # Gifts & Flowers
        {"hashtag": "giftideas", "views": 3800000000, "category": "gifts"},
        {"hashtag": "eidgifts", "views": 2500000000, "category": "gifts"},
        {"hashtag": "valentinesegypt", "views": 1200000000, "category": "gifts"},

        # Pet Care
        {"hashtag": "petsofegypt", "views": 800000000, "category": "pets"},
        {"hashtag": "catsoftiktok", "views": 6500000000, "category": "pets"},

        # Back to School
        {"hashtag": "backtoschool", "views": 4200000000, "category": "education"},
        {"hashtag": "schoolsupplies", "views": 1800000000, "category": "education"},
        {"hashtag": "studyegypt", "views": 900000000, "category": "education"}
    ]


def get_trending_hashtags_from_api(api_key: Optional[str] = None, use_mock: bool = False) -> List[Dict]:
    """
    Fetch trending hashtags from RapidAPI TikTok APIs.

    Args:
        api_key: RapidAPI key (defaults to RAPIDAPI_KEY from .env)
        use_mock: If True, skip API and use mock data

    Returns:
        List of trending hashtags with views
    """
    if use_mock:
        print("Using mock trending hashtags data (forced)")
        return get_mock_trending_hashtags()

    import requests

    api_key = api_key or os.getenv("RAPIDAPI_KEY")

    if not api_key:
        print("No RAPIDAPI_KEY found, using mock data")
        return get_mock_trending_hashtags()

    # Try multiple TikTok API endpoints on RapidAPI
    api_endpoints = [
        {
            "name": "TikTok Scraper",
            "url": "https://tiktok-scraper7.p.rapidapi.com/challenge/search",
            "host": "tiktok-scraper7.p.rapidapi.com",
            "params": {"keywords": "trending", "count": "30", "cursor": "0"},
            "parser": parse_tiktok_scraper_response
        },
        {
            "name": "TikTok API (tiktok-api23)",
            "url": "https://tiktok-api23.p.rapidapi.com/api/challenge/search",
            "host": "tiktok-api23.p.rapidapi.com",
            "params": {"keywords": "trending"},
            "parser": parse_tiktok_api23_response
        },
        {
            "name": "TikTok Bulk Scraper",
            "url": "https://tiktok-bulk-scrape-hashtags.p.rapidapi.com/trending",
            "host": "tiktok-bulk-scrape-hashtags.p.rapidapi.com",
            "params": {"region": "EG"},  # Egypt
            "parser": parse_bulk_scraper_response
        }
    ]

    for endpoint in api_endpoints:
        try:
            print(f"   Trying {endpoint['name']}...")

            headers = {
                "X-RapidAPI-Key": api_key,
                "X-RapidAPI-Host": endpoint["host"]
            }

            response = requests.get(
                endpoint["url"],
                headers=headers,
                params=endpoint.get("params", {}),
                timeout=10
            )

            print(f"   Status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                hashtags = endpoint["parser"](data)

                if hashtags:
                    print(f"   Success! Found {len(hashtags)} hashtags from {endpoint['name']}")
                    return hashtags
                else:
                    print(f"   No hashtags parsed from response")

            elif response.status_code == 429:
                print(f"   Rate limited on {endpoint['name']}")
            else:
                print(f"   Failed: {response.status_code} - {response.text[:200]}")

        except requests.exceptions.Timeout:
            print(f"   Timeout on {endpoint['name']}")
        except Exception as e:
            print(f"   Error on {endpoint['name']}: {e}")

    # Fallback to mock data if all APIs fail
    print("   All APIs failed, using mock data")
    return get_mock_trending_hashtags()


def parse_tiktok_scraper_response(data: Dict) -> List[Dict]:
    """Parse response from tiktok-scraper7 API."""
    hashtags = []
    try:
        challenge_list = data.get("data", {}).get("challenge_list", [])
        if not challenge_list:
            challenge_list = data.get("challenge_list", [])

        for item in challenge_list:
            challenge_info = item.get("challenge_info", item)
            hashtags.append({
                "hashtag": challenge_info.get("cha_name", challenge_info.get("challenge_name", "")),
                "views": challenge_info.get("view_count", challenge_info.get("views", 0)),
                "use_count": challenge_info.get("user_count", 0)
            })
    except Exception as e:
        print(f"   Parse error: {e}")
    return hashtags


def parse_tiktok_api23_response(data: Dict) -> List[Dict]:
    """Parse response from tiktok-api23 API."""
    hashtags = []
    try:
        challenges = data.get("challengeInfoList", data.get("data", []))
        if isinstance(challenges, dict):
            challenges = challenges.get("challenge_list", [])

        for item in challenges:
            challenge = item.get("challengeInfo", item.get("challenge_info", item))
            stats = item.get("stats", {})
            hashtags.append({
                "hashtag": challenge.get("challengeName", challenge.get("cha_name", "")),
                "views": stats.get("viewCount", challenge.get("view_count", 0)),
                "use_count": stats.get("videoCount", 0)
            })
    except Exception as e:
        print(f"   Parse error: {e}")
    return hashtags


def parse_bulk_scraper_response(data: Dict) -> List[Dict]:
    """Parse response from bulk scraper API."""
    hashtags = []
    try:
        trending = data.get("trending", data.get("hashtags", data.get("data", [])))
        for item in trending:
            if isinstance(item, str):
                hashtags.append({"hashtag": item, "views": 0})
            elif isinstance(item, dict):
                hashtags.append({
                    "hashtag": item.get("name", item.get("hashtag", "")),
                    "views": item.get("views", item.get("view_count", 0))
                })
    except Exception as e:
        print(f"   Parse error: {e}")
    return hashtags


def search_tiktok_hashtags(keywords: List[str], api_key: Optional[str] = None) -> List[Dict]:
    """
    Search for specific hashtags on TikTok.

    Args:
        keywords: List of keywords to search (e.g., ["ramadan", "fashion", "beauty"])
        api_key: RapidAPI key

    Returns:
        List of hashtag data
    """
    import requests

    api_key = api_key or os.getenv("RAPIDAPI_KEY")
    all_hashtags = []

    for keyword in keywords:
        try:
            url = "https://tiktok-scraper7.p.rapidapi.com/challenge/search"
            headers = {
                "X-RapidAPI-Key": api_key,
                "X-RapidAPI-Host": "tiktok-scraper7.p.rapidapi.com"
            }
            params = {"keywords": keyword, "count": "10", "cursor": "0"}

            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                hashtags = parse_tiktok_scraper_response(data)
                all_hashtags.extend(hashtags)
                print(f"   Found {len(hashtags)} hashtags for '{keyword}'")

        except Exception as e:
            print(f"   Error searching '{keyword}': {e}")

    # Remove duplicates
    seen = set()
    unique_hashtags = []
    for h in all_hashtags:
        if h["hashtag"] not in seen:
            seen.add(h["hashtag"])
            unique_hashtags.append(h)

    return unique_hashtags


# ============================================================================
# HASHTAG ANALYSIS & CATEGORY MAPPING
# ============================================================================

def analyze_hashtag(hashtag: str) -> Dict:
    """
    Analyze a single hashtag and map it to shopping categories/subcategories.

    Returns:
        Dict with matched categories, subcategories, and confidence score
    """
    hashtag_lower = hashtag.lower().replace("#", "").replace("_", "")

    result = {
        "hashtag": hashtag,
        "categories": [],
        "subcategories": [],
        "regional_match": None,
        "confidence": 0.0
    }

    # Check regional/seasonal hashtags first (highest priority)
    for regional_key, mapping in REGIONAL_HASHTAGS.items():
        if regional_key in hashtag_lower:
            result["categories"].extend(mapping["categories"])
            result["subcategories"].extend(mapping["subcategories"])
            result["regional_match"] = regional_key
            result["confidence"] = 0.9
            return result

    # Check main category mappings
    for category, keywords in HASHTAG_CATEGORY_MAPPING.items():
        for keyword in keywords:
            if keyword in hashtag_lower or hashtag_lower in keyword:
                if category not in result["categories"]:
                    result["categories"].append(category)
                    result["confidence"] = max(result["confidence"], 0.7)

    # Check subcategory mappings for more specific matches
    for subcategory, keywords in HASHTAG_SUBCATEGORY_MAPPING.items():
        for keyword in keywords:
            if keyword in hashtag_lower or hashtag_lower in keyword:
                if subcategory not in result["subcategories"]:
                    result["subcategories"].append(subcategory)
                    result["confidence"] = max(result["confidence"], 0.8)

    # If no match found, try fuzzy matching
    if not result["categories"]:
        result["confidence"] = 0.0

    return result


def analyze_trending_hashtags(hashtags: List[Dict]) -> List[Dict]:
    """
    Analyze a list of trending hashtags and map them to categories.

    Returns:
        List of analyzed hashtags with category mappings
    """
    analyzed = []

    for tag_data in hashtags:
        hashtag = tag_data.get("hashtag", "")
        views = tag_data.get("views", 0)

        analysis = analyze_hashtag(hashtag)
        analysis["views"] = views
        analysis["original_data"] = tag_data

        # Only include if we found a match
        if analysis["categories"]:
            analyzed.append(analysis)

    # Sort by views (popularity)
    analyzed.sort(key=lambda x: x["views"], reverse=True)

    return analyzed


def get_trending_categories(analyzed_hashtags: List[Dict]) -> Dict:
    """
    Aggregate analyzed hashtags to get trending categories with scores.

    Returns:
        Dict with categories and their trend scores
    """
    category_scores = {}
    subcategory_scores = {}

    for analysis in analyzed_hashtags:
        # Weight by views and confidence
        weight = (analysis["views"] / 1000000000) * analysis["confidence"]

        for cat in analysis["categories"]:
            if cat not in category_scores:
                category_scores[cat] = {"score": 0, "hashtags": [], "views": 0}
            category_scores[cat]["score"] += weight
            category_scores[cat]["hashtags"].append(analysis["hashtag"])
            category_scores[cat]["views"] += analysis["views"]

        for subcat in analysis["subcategories"]:
            if subcat not in subcategory_scores:
                subcategory_scores[subcat] = {"score": 0, "hashtags": [], "views": 0}
            subcategory_scores[subcat]["score"] += weight
            subcategory_scores[subcat]["hashtags"].append(analysis["hashtag"])
            subcategory_scores[subcat]["views"] += analysis["views"]

    # Sort by score
    sorted_categories = dict(sorted(
        category_scores.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    ))

    sorted_subcategories = dict(sorted(
        subcategory_scores.items(),
        key=lambda x: x[1]["score"],
        reverse=True
    ))

    return {
        "categories": sorted_categories,
        "subcategories": sorted_subcategories
    }


# ============================================================================
# DATABASE QUERIES - GET VENDORS & ITEMS
# ============================================================================

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


def get_trending_vendors(categories: List[str], subcategories: List[str] = None,
                         days_back: int = 30, limit: int = 20) -> List[Dict]:
    """
    Get top vendors matching trending categories.

    Args:
        categories: List of shopping categories to filter by
        subcategories: Optional list of subcategories
        days_back: Number of days to look back for orders
        limit: Maximum number of vendors to return
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    pipeline = [
        {
            "$match": {
                "createdAt": {"$gte": start_date, "$lte": end_date},
                "_user": {"$nin": INTERNAL_USER_IDS}
            }
        },
        {"$unwind": "$items"},
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
        {"$unwind": {"path": "$vendor", "preserveNullAndEmptyArrays": True}}
    ]

    # Add category filtering
    match_conditions = {}
    if categories:
        match_conditions["vendor.shoppingCategory"] = {"$in": categories}
    if subcategories:
        match_conditions["vendor.shoppingSubcategory"] = {"$in": subcategories}

    if match_conditions:
        pipeline.append({"$match": match_conditions})

    pipeline.extend([
        {
            "$project": {
                "_id": 0,
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
        {"$sort": {"orders_count": -1}},
        {"$limit": limit}
    ])

    results = list(orders_collection.aggregate(pipeline))
    return serialize_doc(results)


def get_trending_items(categories: List[str], subcategories: List[str] = None,
                       days_back: int = 30, limit: int = 20) -> List[Dict]:
    """
    Get top items matching trending categories.

    Args:
        categories: List of shopping categories to filter by
        subcategories: Optional list of subcategories
        days_back: Number of days to look back for orders
        limit: Maximum number of items to return
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days_back)

    pipeline = [
        {
            "$match": {
                "createdAt": {"$gte": start_date, "$lte": end_date},
                "_user": {"$nin": INTERNAL_USER_IDS}
            }
        },
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
        {
            "$lookup": {
                "from": "Items",
                "localField": "_id.item_id",
                "foreignField": "_id",
                "as": "item"
            }
        },
        {"$unwind": {"path": "$item", "preserveNullAndEmptyArrays": True}},
        {
            "$lookup": {
                "from": "Vendors",
                "localField": "_id.vendor_id",
                "foreignField": "_id",
                "as": "vendor"
            }
        },
        {"$unwind": {"path": "$vendor", "preserveNullAndEmptyArrays": True}}
    ]

    # Add category filtering
    match_conditions = {}
    if categories:
        match_conditions["vendor.shoppingCategory"] = {"$in": categories}
    if subcategories:
        match_conditions["vendor.shoppingSubcategory"] = {"$in": subcategories}

    if match_conditions:
        pipeline.append({"$match": match_conditions})

    pipeline.extend([
        {
            "$project": {
                "_id": 0,
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
        {"$sort": {"total_qty": -1}},
        {"$limit": limit}
    ])

    results = list(orders_collection.aggregate(pipeline))
    return serialize_doc(results)


# ============================================================================
# MAIN TREND ANALYSIS FUNCTION
# ============================================================================

def get_tiktok_trend_suggestions(days_back: int = 30,
                                  top_categories: int = 5,
                                  items_per_category: int = 10,
                                  vendors_per_category: int = 10) -> Dict:
    """
    Main function to get product suggestions based on TikTok trends.

    Returns:
        Dict with trending categories and suggested vendors/items for each
    """
    print("=" * 60)
    print("TikTok Trend Analysis for Product Suggestions")
    print("=" * 60)

    # Step 1: Get trending hashtags
    print("\n1. Fetching trending hashtags...")
    hashtags = get_trending_hashtags_from_api()
    print(f"   Found {len(hashtags)} trending hashtags")

    # Step 2: Analyze and map to categories
    print("\n2. Analyzing hashtags and mapping to categories...")
    analyzed = analyze_trending_hashtags(hashtags)
    print(f"   Mapped {len(analyzed)} hashtags to shopping categories")

    # Step 3: Get trending categories
    print("\n3. Aggregating trending categories...")
    trending = get_trending_categories(analyzed)

    top_cats = list(trending["categories"].keys())[:top_categories]
    print(f"   Top {top_categories} categories: {', '.join(top_cats)}")

    # Step 4: Get vendors and items for each trending category
    print("\n4. Fetching vendors and items for trending categories...")

    suggestions = {
        "generated_at": datetime.now().isoformat(),
        "analysis_period_days": days_back,
        "trending_hashtags": [
            {
                "hashtag": h["hashtag"],
                "views": h["views"],
                "categories": h["categories"],
                "confidence": h["confidence"]
            }
            for h in analyzed[:10]  # Top 10 analyzed hashtags
        ],
        "trending_categories": {},
        "trending_subcategories": dict(list(trending["subcategories"].items())[:10]),
        "category_suggestions": {}
    }

    for category in top_cats:
        cat_data = trending["categories"][category]
        print(f"\n   Processing: {category}")
        print(f"   - Score: {cat_data['score']:.2f}")
        print(f"   - Related hashtags: {', '.join(cat_data['hashtags'][:3])}")

        # Get relevant subcategories for this category
        relevant_subcats = [
            subcat for subcat in trending["subcategories"].keys()
            if subcat in HASHTAG_SUBCATEGORY_MAPPING
        ][:3]

        # Fetch vendors
        vendors = get_trending_vendors(
            categories=[category],
            subcategories=relevant_subcats if relevant_subcats else None,
            days_back=days_back,
            limit=vendors_per_category
        )

        # Fetch items
        items = get_trending_items(
            categories=[category],
            subcategories=relevant_subcats if relevant_subcats else None,
            days_back=days_back,
            limit=items_per_category
        )

        suggestions["trending_categories"][category] = cat_data
        suggestions["category_suggestions"][category] = {
            "trend_score": cat_data["score"],
            "related_hashtags": cat_data["hashtags"],
            "total_views": cat_data["views"],
            "suggested_vendors": vendors,
            "suggested_items": items,
            "vendor_count": len(vendors),
            "item_count": len(items)
        }

        print(f"   - Found {len(vendors)} vendors, {len(items)} items")

    return suggestions


# ============================================================================
# TEST FUNCTIONS
# ============================================================================

def test_hashtag_analysis():
    """Test the hashtag analysis functionality."""
    print("\n" + "=" * 60)
    print("TEST: Hashtag Analysis")
    print("=" * 60)

    test_hashtags = [
        "ramadan2024", "ootd", "skincareroutine", "hijabfashion",
        "foodtiktok", "techreview", "eidgifts", "cleaningtiktok"
    ]

    for hashtag in test_hashtags:
        result = analyze_hashtag(hashtag)
        print(f"\n#{hashtag}:")
        print(f"  Categories: {result['categories']}")
        print(f"  Subcategories: {result['subcategories']}")
        print(f"  Regional match: {result['regional_match']}")
        print(f"  Confidence: {result['confidence']:.1%}")


def test_database_connection():
    """Test MongoDB connection and basic queries."""
    print("\n" + "=" * 60)
    print("TEST: Database Connection")
    print("=" * 60)

    try:
        # Test connection
        vendor_count = vendors_collection.count_documents({})
        item_count = items_collection.count_documents({})
        order_count = orders_collection.count_documents({})

        print(f"\nDatabase connected successfully!")
        print(f"  Vendors: {vendor_count:,}")
        print(f"  Items: {item_count:,}")
        print(f"  Orders: {order_count:,}")

        # Test a simple aggregation
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)

        recent_orders = orders_collection.count_documents({
            "createdAt": {"$gte": start_date, "$lte": end_date}
        })
        print(f"  Orders (last 7 days): {recent_orders:,}")

        return True
    except Exception as e:
        print(f"\nDatabase connection failed: {e}")
        return False


def test_trending_suggestions():
    """Test the full trend suggestions pipeline."""
    print("\n" + "=" * 60)
    print("TEST: Full Trending Suggestions Pipeline")
    print("=" * 60)

    suggestions = get_tiktok_trend_suggestions(
        days_back=30,
        top_categories=3,
        items_per_category=5,
        vendors_per_category=5
    )

    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)

    print(f"\nGenerated at: {suggestions['generated_at']}")
    print(f"Analysis period: {suggestions['analysis_period_days']} days")

    print("\nTop Trending Hashtags:")
    for h in suggestions["trending_hashtags"][:5]:
        print(f"  #{h['hashtag']}: {h['views']:,} views -> {', '.join(h['categories'])}")

    print("\nCategory Suggestions:")
    for cat, data in suggestions["category_suggestions"].items():
        print(f"\n  {cat.upper()}:")
        print(f"    Trend Score: {data['trend_score']:.2f}")
        print(f"    Vendors: {data['vendor_count']}, Items: {data['item_count']}")

        if data["suggested_vendors"]:
            print("    Top Vendors:")
            for v in data["suggested_vendors"][:3]:
                print(f"      - {v.get('vendor_name', 'N/A')} ({v.get('orders_count', 0)} orders)")

        if data["suggested_items"]:
            print("    Top Items:")
            for i in data["suggested_items"][:3]:
                print(f"      - {i.get('item_name', 'N/A')} ({i.get('total_qty', 0)} sold)")

    return suggestions


def save_suggestions_to_file(suggestions: Dict, filename: str = None):
    """Save suggestions to a JSON file."""
    if filename is None:
        filename = f"tiktok_suggestions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    filepath = os.path.join(os.path.dirname(__file__), filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(suggestions, f, indent=2, ensure_ascii=False)

    print(f"\nSuggestions saved to: {filepath}")
    return filepath


def get_egypt_trending_hashtags(api_key: Optional[str] = None) -> List[Dict]:
    """
    Get trending hashtags relevant to the Egyptian market.
    Searches for Egypt-specific and regional keywords.
    """
    # Keywords relevant to Egyptian e-commerce
    egypt_keywords = [
        "egypt", "cairo", "ramadan", "eid",
        "hijab", "modest", "arabic",
        "fashion", "beauty", "food",
        "shopping", "haul", "review"
    ]

    print("\n   Searching for Egypt-relevant hashtags...")
    hashtags = search_tiktok_hashtags(egypt_keywords, api_key)

    if not hashtags:
        print("   No results from API, using mock data")
        return get_mock_trending_hashtags()

    return hashtags


def test_live_api():
    """Test the live TikTok API with your RapidAPI key."""
    print("\n" + "=" * 60)
    print("TEST: Live TikTok API")
    print("=" * 60)

    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key:
        print("\nNo RAPIDAPI_KEY found in .env file")
        return False

    print(f"\nAPI Key found: {api_key[:20]}...")

    # Test 1: Get trending hashtags
    print("\n1. Fetching trending hashtags...")
    hashtags = get_trending_hashtags_from_api(api_key)

    if hashtags:
        print(f"\n   Retrieved {len(hashtags)} hashtags:")
        for h in hashtags[:10]:
            views = h.get('views', 0)
            views_str = f"{views:,}" if views else "N/A"
            hashtag_name = h['hashtag']
            # Handle Arabic characters for Windows console
            try:
                print(f"   - #{hashtag_name}: {views_str} views")
            except UnicodeEncodeError:
                print(f"   - #{hashtag_name.encode('ascii', 'replace').decode()}: {views_str} views")
        return True
    else:
        print("\n   Failed to retrieve hashtags")
        return False


def test_egypt_specific():
    """Test searching for Egypt-specific trending content."""
    print("\n" + "=" * 60)
    print("TEST: Egypt-Specific Hashtag Search")
    print("=" * 60)

    hashtags = get_egypt_trending_hashtags()

    if hashtags:
        print(f"\n   Found {len(hashtags)} Egypt-relevant hashtags:")

        # Analyze and map to categories
        analyzed = analyze_trending_hashtags(hashtags)

        print("\n   Mapped to categories:")
        for h in analyzed[:10]:
            print(f"   - #{h['hashtag']}: {', '.join(h['categories'])} (conf: {h['confidence']:.0%})")

        return analyzed
    return []


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == "__main__":
    import sys

    print("\n" + "=" * 60)
    print("TIKTOK TRENDS -> PRODUCT SUGGESTIONS TEST")
    print("=" * 60)

    # Check for command line arguments
    use_mock = "--mock" in sys.argv
    api_only = "--api-only" in sys.argv

    if use_mock:
        print("\n[MODE] Using mock data (--mock flag)")
    elif api_only:
        print("\n[MODE] Testing API only (--api-only flag)")

    # Run tests
    if api_only:
        # Just test the API connection
        print("\n[1/1] Testing live TikTok API...")
        test_live_api()
    else:
        print("\n[1/4] Testing hashtag analysis...")
        test_hashtag_analysis()

        print("\n[2/4] Testing database connection...")
        db_ok = test_database_connection()

        print("\n[3/4] Testing live TikTok API...")
        api_ok = test_live_api()

        if db_ok:
            print("\n[4/4] Testing full suggestions pipeline...")
            suggestions = get_tiktok_trend_suggestions(
                days_back=30,
                top_categories=5,
                items_per_category=10,
                vendors_per_category=10
            )

            # Print summary
            print("\n" + "=" * 60)
            print("RESULTS SUMMARY")
            print("=" * 60)

            print(f"\nGenerated at: {suggestions['generated_at']}")
            print(f"Analysis period: {suggestions['analysis_period_days']} days")

            print("\nTop Trending Hashtags:")
            for h in suggestions["trending_hashtags"][:5]:
                print(f"  #{h['hashtag']}: {h['views']:,} views -> {', '.join(h['categories'])}")

            print("\nCategory Suggestions:")
            for cat, data in suggestions["category_suggestions"].items():
                print(f"\n  {cat.upper()}:")
                print(f"    Trend Score: {data['trend_score']:.2f}")
                print(f"    Vendors: {data['vendor_count']}, Items: {data['item_count']}")

                if data["suggested_vendors"]:
                    print("    Top Vendors:")
                    for v in data["suggested_vendors"][:3]:
                        print(f"      - {v.get('vendor_name', 'N/A')} ({v.get('orders_count', 0)} orders)")

                if data["suggested_items"]:
                    print("    Top Items:")
                    for i in data["suggested_items"][:3]:
                        print(f"      - {i.get('item_name', 'N/A')} ({i.get('total_qty', 0)} sold)")

            # Save results
            save_suggestions_to_file(suggestions)
        else:
            print("\n[4/4] Skipping suggestions test (database not available)")

    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    print("\nUsage:")
    print("  python test_tiktok_trends.py           # Full test with API")
    print("  python test_tiktok_trends.py --mock    # Use mock data only")
    print("  python test_tiktok_trends.py --api-only # Test API connection only")
