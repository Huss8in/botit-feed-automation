"""
Seasonal Event to Category Path Mapping

This file maps seasonal events to their corresponding category paths based on business logic.
Each event is mapped to one or more category chains following the 4-level hierarchy:
    Level 1: shoppingCategory
    Level 2: shoppingSubcategory
    Level 3: itemCategory
    Level 4: itemSubcategory (optional)

Structure:
    event_key: {
        "name": "Display Name",
        "category_paths": [
            {
                "shoppingCategory": "...",
                "shoppingSubcategory": "...",
                "itemCategory": "...",
                "itemSubcategory": "..." (optional)
            },
            ...
        ]
    }

This file references category keys from category_mapping.py
"""

# Import category definitions for validation (optional)
# from category_mapping import (
#     shoppingCategory,
#     shoppingSubcategory_map,
#     itemCategory_map,
#     itemSubcategory_map
# )

# =============================================================================
# SEASONAL EVENT CATEGORY MAPPINGS
# =============================================================================

EVENT_CATEGORY_MAPPING = {

    # -------------------------------------------------------------------------
    # RELIGIOUS HOLIDAYS
    # -------------------------------------------------------------------------

    "ramadan": {
        "name": "Ramadan",
        "category_paths": [
            # Dates and dried fruits
            {
                "shoppingCategory": "groceries",
                "shoppingSubcategory": "supermarkets",
                "itemCategory": "produce",
                "itemSubcategory": "dried fruit"
            },
            {
                "shoppingCategory": "groceries",
                "shoppingSubcategory": "supermarkets",
                "itemCategory": "snacks",
                "itemSubcategory": "nuts"
            },
            # Juices and beverages
            {
                "shoppingCategory": "groceries",
                "shoppingSubcategory": "supermarkets",
                "itemCategory": "beverage",
                "itemSubcategory": "juice"
            },
            # Oriental sweets
            {
                "shoppingCategory": "groceries",
                "shoppingSubcategory": "supermarkets",
                "itemCategory": "sweet",
                "itemSubcategory": "oriental sweets"
            },
            # Restaurants - desserts
            {
                "shoppingCategory": "restaurants",
                "shoppingSubcategory": "desserts",
                "itemCategory": "sweet",
                "itemSubcategory": "oriental sweets"
            },
            # Home decorations (lanterns)
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "home decor",
                "itemCategory": "candle"
            },
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "lighting",
                "itemCategory": "lamp"
            },
            # Tableware for iftar
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "tableware",
                "itemCategory": "plate and bowl"
            },
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "drinkware",
                "itemCategory": "glass"
            },
            # Religious wear
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "religious wear",
                "itemCategory": "islamic religious wear"
            }
        ]
    },

    "eid_al_fitr": {
        "name": "Eid al-Fitr",
        "category_paths": [
            # Kahk and sweets
            {
                "shoppingCategory": "groceries",
                "shoppingSubcategory": "supermarkets",
                "itemCategory": "sweet",
                "itemSubcategory": "oriental sweets"
            },
            {
                "shoppingCategory": "groceries",
                "shoppingSubcategory": "specialty foods",
                "itemCategory": "bakery",
                "itemSubcategory": "pastry"
            },
            # New clothes - casual wear
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "casual wear",
                "itemCategory": "dress"
            },
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "casual wear",
                "itemCategory": "top",
                "itemSubcategory": "shirt"
            },
            # Footwear
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "footwear",
                "itemCategory": "shoe",
                "itemSubcategory": "dress shoe"
            },
            # Jewelry
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "jewelry",
                "itemCategory": "necklace"
            },
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "jewelry",
                "itemCategory": "bracelet"
            },
            # Gifts
            {
                "shoppingCategory": "flowers and gifts",
                "shoppingSubcategory": "gifts",
                "itemCategory": "gift card"
            },
            # Kids toys
            {
                "shoppingCategory": "kids",
                "shoppingSubcategory": "toys and games",
                "itemCategory": "toy figure"
            },
            # Perfumes
            {
                "shoppingCategory": "beauty",
                "shoppingSubcategory": "fragrances",
                "itemCategory": "perfume"
            }
        ]
    },

    "eid_al_adha": {
        "name": "Eid al-Adha",
        "category_paths": [
            # Fresh meat
            {
                "shoppingCategory": "groceries",
                "shoppingSubcategory": "supermarkets",
                "itemCategory": "meat and poultry",
                "itemSubcategory": "lamb"
            },
            {
                "shoppingCategory": "groceries",
                "shoppingSubcategory": "farm to table",
                "itemCategory": "meat and poultry"
            },
            # Kitchen knives
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "kitchenwear",
                "itemCategory": "cooking utensil",
                "itemSubcategory": "knife"
            },
            # Cookware
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "kitchenwear",
                "itemCategory": "pot and pan"
            },
            # Food storage
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "storage and organization",
                "itemCategory": "food container"
            },
            # Freezer
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "appliances",
                "itemCategory": "home appliance",
                "itemSubcategory": "freezer"
            },
            # BBQ/Grill
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "gardening and outdoor",
                "itemCategory": "outdoor furniture",
                "itemSubcategory": "outdoor cookware"
            }
        ]
    },

    "mawlid": {
        "name": "Prophet's Birthday (Mawlid)",
        "category_paths": [
            # Traditional sweets (halawet el-moulid)
            {
                "shoppingCategory": "groceries",
                "shoppingSubcategory": "supermarkets",
                "itemCategory": "sweet",
                "itemSubcategory": "candy"
            },
            {
                "shoppingCategory": "groceries",
                "shoppingSubcategory": "specialty foods",
                "itemCategory": "sweet",
                "itemSubcategory": "oriental sweets"
            },
            {
                "shoppingCategory": "restaurants",
                "shoppingSubcategory": "desserts",
                "itemCategory": "sweet"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # NATIONAL HOLIDAYS
    # -------------------------------------------------------------------------

    "coptic_christmas": {
        "name": "Coptic Christmas",
        "category_paths": [
            # Christmas decorations
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "home decor",
                "itemCategory": "home decor accessory"
            },
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "lighting",
                "itemCategory": "outdoor lighting"
            },
            # Gifts
            {
                "shoppingCategory": "flowers and gifts",
                "shoppingSubcategory": "gifts",
                "itemCategory": "gift wrapping"
            },
            {
                "shoppingCategory": "flowers and gifts",
                "shoppingSubcategory": "flowers",
                "itemCategory": "bouquet"
            },
            # Toys for kids
            {
                "shoppingCategory": "kids",
                "shoppingSubcategory": "toys and games",
                "itemCategory": "toy figure"
            }
        ]
    },

    "sham_el_nessim": {
        "name": "Sham El-Nessim (Spring Festival)",
        "category_paths": [
            # Traditional foods (feseekh, colored eggs)
            {
                "shoppingCategory": "groceries",
                "shoppingSubcategory": "supermarkets",
                "itemCategory": "seafood",
                "itemSubcategory": "fish"
            },
            {
                "shoppingCategory": "groceries",
                "shoppingSubcategory": "supermarkets",
                "itemCategory": "dairy",
                "itemSubcategory": "egg"
            },
            # Outdoor/picnic items
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "storage and organization",
                "itemCategory": "food container"
            },
            {
                "shoppingCategory": "sports",
                "shoppingSubcategory": "outdoor sports",
                "itemCategory": "camping"
            },
            # Outdoor toys
            {
                "shoppingCategory": "kids",
                "shoppingSubcategory": "toys and games",
                "itemCategory": "outdoor toy",
                "itemSubcategory": "ball"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # SHOPPING SEASONS
    # -------------------------------------------------------------------------

    "valentines_day": {
        "name": "Valentine's Day",
        "category_paths": [
            # Flowers
            {
                "shoppingCategory": "flowers and gifts",
                "shoppingSubcategory": "flowers",
                "itemCategory": "bouquet"
            },
            # Chocolates
            {
                "shoppingCategory": "groceries",
                "shoppingSubcategory": "supermarkets",
                "itemCategory": "sweet",
                "itemSubcategory": "chocolate"
            },
            {
                "shoppingCategory": "groceries",
                "shoppingSubcategory": "specialty foods",
                "itemCategory": "sweet",
                "itemSubcategory": "chocolate"
            },
            # Perfumes
            {
                "shoppingCategory": "beauty",
                "shoppingSubcategory": "fragrances",
                "itemCategory": "perfume"
            },
            # Jewelry
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "jewelry",
                "itemCategory": "ring"
            },
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "jewelry",
                "itemCategory": "necklace"
            },
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "jewelry",
                "itemCategory": "bracelet"
            },
            # Greeting cards
            {
                "shoppingCategory": "flowers and gifts",
                "shoppingSubcategory": "gifts",
                "itemCategory": "greeting card"
            },
            # Teddy bears / stuffed animals
            {
                "shoppingCategory": "kids",
                "shoppingSubcategory": "toys and games",
                "itemCategory": "toddler toy",
                "itemSubcategory": "stuffed animal"
            },
            # Watches
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "accessories",
                "itemCategory": "watch"
            },
            # Cakes
            {
                "shoppingCategory": "restaurants",
                "shoppingSubcategory": "bakery and cakes",
                "itemCategory": "sweet",
                "itemSubcategory": "cake"
            }
        ]
    },

    "mothers_day": {
        "name": "Mother's Day",
        "category_paths": [
            # Flowers
            {
                "shoppingCategory": "flowers and gifts",
                "shoppingSubcategory": "flowers",
                "itemCategory": "bouquet"
            },
            # Perfumes
            {
                "shoppingCategory": "beauty",
                "shoppingSubcategory": "fragrances",
                "itemCategory": "perfume"
            },
            # Skincare
            {
                "shoppingCategory": "beauty",
                "shoppingSubcategory": "skincare",
                "itemCategory": "skincare set"
            },
            {
                "shoppingCategory": "beauty",
                "shoppingSubcategory": "skincare",
                "itemCategory": "face moisturizer"
            },
            # Gold jewelry
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "jewelry",
                "itemCategory": "necklace"
            },
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "jewelry",
                "itemCategory": "bracelet"
            },
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "jewelry",
                "itemCategory": "earring"
            },
            # Handbags
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "accessories",
                "itemCategory": "bag",
                "itemSubcategory": "purse"
            },
            # Kitchen appliances
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "appliances",
                "itemCategory": "kitchen appliance",
                "itemSubcategory": "blender"
            },
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "appliances",
                "itemCategory": "kitchen appliance",
                "itemSubcategory": "coffee maker"
            },
            # Smartphones
            {
                "shoppingCategory": "electronics",
                "shoppingSubcategory": "phones",
                "itemCategory": "smart phone"
            },
            # Watches
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "accessories",
                "itemCategory": "watch"
            }
        ]
    },

    "back_to_school": {
        "name": "Back to School",
        "category_paths": [
            # School bags/backpacks
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "accessories",
                "itemCategory": "bag",
                "itemSubcategory": "backpack"
            },
            # Notebooks
            {
                "shoppingCategory": "stationary",
                "shoppingSubcategory": "school supplies",
                "itemCategory": "notebook"
            },
            # Pencil cases
            {
                "shoppingCategory": "stationary",
                "shoppingSubcategory": "school supplies",
                "itemCategory": "pencil case"
            },
            # Pens and pencils
            {
                "shoppingCategory": "stationary",
                "shoppingSubcategory": "office supplies",
                "itemCategory": "pen"
            },
            {
                "shoppingCategory": "stationary",
                "shoppingSubcategory": "office supplies",
                "itemCategory": "pencil"
            },
            # Rulers and geometry sets
            {
                "shoppingCategory": "stationary",
                "shoppingSubcategory": "school supplies",
                "itemCategory": "ruler"
            },
            # Laptops
            {
                "shoppingCategory": "electronics",
                "shoppingSubcategory": "computers",
                "itemCategory": "laptop"
            },
            # Tablets
            {
                "shoppingCategory": "electronics",
                "shoppingSubcategory": "computers",
                "itemCategory": "tablet"
            },
            # Calculators
            {
                "shoppingCategory": "electronics",
                "shoppingSubcategory": "electronics",
                "itemCategory": "office electronic",
                "itemSubcategory": "calculator"
            },
            # School uniforms
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "casual wear",
                "itemCategory": "uniform"
            },
            # School shoes
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "footwear",
                "itemCategory": "shoe",
                "itemSubcategory": "casual shoe"
            }
        ]
    },

    "black_friday": {
        "name": "Black Friday / White Friday",
        "category_paths": [
            # Smartphones
            {
                "shoppingCategory": "electronics",
                "shoppingSubcategory": "phones",
                "itemCategory": "smart phone"
            },
            # Laptops
            {
                "shoppingCategory": "electronics",
                "shoppingSubcategory": "computers",
                "itemCategory": "laptop"
            },
            # TVs
            {
                "shoppingCategory": "electronics",
                "shoppingSubcategory": "electronics",
                "itemCategory": "tv and video",
                "itemSubcategory": "led and lcd"
            },
            # Headphones
            {
                "shoppingCategory": "electronics",
                "shoppingSubcategory": "electronics",
                "itemCategory": "headphone and speaker",
                "itemSubcategory": "wireless headphone"
            },
            # Fashion
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "casual wear",
                "itemCategory": "top"
            },
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "casual wear",
                "itemCategory": "trousers"
            },
            # Home appliances
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "appliances",
                "itemCategory": "home appliance"
            },
            # Perfumes
            {
                "shoppingCategory": "beauty",
                "shoppingSubcategory": "fragrances",
                "itemCategory": "perfume"
            },
            # Toys
            {
                "shoppingCategory": "kids",
                "shoppingSubcategory": "toys and games",
                "itemCategory": "toy vehicle"
            }
        ]
    },

    "singles_day": {
        "name": "Singles' Day (11.11)",
        "category_paths": [
            # Electronics
            {
                "shoppingCategory": "electronics",
                "shoppingSubcategory": "phones",
                "itemCategory": "smart phone"
            },
            {
                "shoppingCategory": "electronics",
                "shoppingSubcategory": "electronics",
                "itemCategory": "wearable technology",
                "itemSubcategory": "smart watch"
            },
            # Fashion accessories
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "accessories",
                "itemCategory": "bag"
            },
            # Skincare
            {
                "shoppingCategory": "beauty",
                "shoppingSubcategory": "skincare",
                "itemCategory": "face moisturizer"
            },
            # Home decor
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "home decor",
                "itemCategory": "candle"
            }
        ]
    },

    "year_end_sales": {
        "name": "Year-End Sales",
        "category_paths": [
            # Fashion clearance
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "casual wear",
                "itemCategory": "outerwear",
                "itemSubcategory": "jacket"
            },
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "casual wear",
                "itemCategory": "outerwear",
                "itemSubcategory": "coat"
            },
            # Electronics
            {
                "shoppingCategory": "electronics",
                "shoppingSubcategory": "phones",
                "itemCategory": "smart phone"
            },
            # Home furniture
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "furniture",
                "itemCategory": "living room furniture"
            },
            # Toys
            {
                "shoppingCategory": "kids",
                "shoppingSubcategory": "toys and games",
                "itemCategory": "game"
            },
            # Party supplies (New Year)
            {
                "shoppingCategory": "kids",
                "shoppingSubcategory": "toys and games",
                "itemCategory": "party supply",
                "itemSubcategory": "balloon"
            }
        ]
    },

    # -------------------------------------------------------------------------
    # SEASONAL EVENTS
    # -------------------------------------------------------------------------

    "summer_season": {
        "name": "Summer Season",
        "category_paths": [
            # Swimwear
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "swimwear",
                "itemCategory": "swimsuit"
            },
            # Beach wear
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "beach wear",
                "itemCategory": "dress"
            },
            # Sunglasses
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "eyewear",
                "itemCategory": "sunglasses"
            },
            # Sandals
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "footwear",
                "itemCategory": "sandal"
            },
            # Sunscreen
            {
                "shoppingCategory": "beauty",
                "shoppingSubcategory": "skincare",
                "itemCategory": "sunscreen"
            },
            # Air conditioners
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "appliances",
                "itemCategory": "heating and cooling unit",
                "itemSubcategory": "air conditioner"
            },
            # Fans
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "appliances",
                "itemCategory": "heating and cooling unit",
                "itemSubcategory": "fan"
            },
            # Water sports
            {
                "shoppingCategory": "sports",
                "shoppingSubcategory": "water sports",
                "itemCategory": "swimming"
            },
            # Beach toys
            {
                "shoppingCategory": "kids",
                "shoppingSubcategory": "toys and games",
                "itemCategory": "outdoor toy",
                "itemSubcategory": "beach toy"
            }
        ]
    },

    "winter_season": {
        "name": "Winter Season",
        "category_paths": [
            # Jackets and coats
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "casual wear",
                "itemCategory": "outerwear",
                "itemSubcategory": "jacket"
            },
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "casual wear",
                "itemCategory": "outerwear",
                "itemSubcategory": "coat"
            },
            # Sweaters
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "casual wear",
                "itemCategory": "top",
                "itemSubcategory": "sweater"
            },
            # Boots
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "footwear",
                "itemCategory": "boot"
            },
            # Scarves
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "accessories",
                "itemCategory": "neckwear and scarf",
                "itemSubcategory": "scarf"
            },
            # Blankets
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "bed and bath",
                "itemCategory": "bedding",
                "itemSubcategory": "blanket"
            },
            # Heaters
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "appliances",
                "itemCategory": "heating and cooling unit",
                "itemSubcategory": "heater"
            },
            # Hot beverages
            {
                "shoppingCategory": "groceries",
                "shoppingSubcategory": "supermarkets",
                "itemCategory": "beverage",
                "itemSubcategory": "hot cocoa"
            }
        ]
    },

    "wedding_season": {
        "name": "Wedding Season (Spring/Summer)",
        "category_paths": [
            # Wedding dresses
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "designer wear",
                "itemCategory": "dress"
            },
            # Suits
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "designer wear",
                "itemCategory": "suit"
            },
            # Jewelry
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "jewelry",
                "itemCategory": "ring"
            },
            {
                "shoppingCategory": "fashion",
                "shoppingSubcategory": "jewelry",
                "itemCategory": "jewelry set"
            },
            # Flowers
            {
                "shoppingCategory": "flowers and gifts",
                "shoppingSubcategory": "flowers",
                "itemCategory": "bouquet"
            },
            # Cosmetics
            {
                "shoppingCategory": "beauty",
                "shoppingSubcategory": "cosmetics",
                "itemCategory": "face make-up",
                "itemSubcategory": "foundation"
            },
            # Perfumes
            {
                "shoppingCategory": "beauty",
                "shoppingSubcategory": "fragrances",
                "itemCategory": "perfume"
            },
            # Home appliances (gifts)
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "appliances",
                "itemCategory": "kitchen appliance"
            },
            # Furniture
            {
                "shoppingCategory": "home and garden",
                "shoppingSubcategory": "furniture",
                "itemCategory": "bedroom furniture"
            }
        ]
    }
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_event_category_paths(event_key: str) -> list:
    """
    Get category paths for a specific event.

    Args:
        event_key: The event identifier (e.g., 'valentines_day', 'ramadan')

    Returns:
        List of category path dictionaries, or empty list if not found
    """
    event = EVENT_CATEGORY_MAPPING.get(event_key)
    if event:
        return event.get("category_paths", [])
    return []


def get_event_name(event_key: str) -> str:
    """
    Get the display name for an event.

    Args:
        event_key: The event identifier

    Returns:
        Display name string, or the key itself if not found
    """
    event = EVENT_CATEGORY_MAPPING.get(event_key)
    if event:
        return event.get("name", event_key)
    return event_key


def get_all_events() -> list:
    """
    Get list of all event keys.

    Returns:
        List of event key strings
    """
    return list(EVENT_CATEGORY_MAPPING.keys())


def get_events_by_category(shopping_category: str) -> list:
    """
    Get all events that include a specific shopping category.

    Args:
        shopping_category: The shoppingCategory to filter by (e.g., 'fashion', 'groceries')

    Returns:
        List of event keys that include this category
    """
    matching_events = []
    for event_key, event_data in EVENT_CATEGORY_MAPPING.items():
        for path in event_data.get("category_paths", []):
            if path.get("shoppingCategory") == shopping_category:
                matching_events.append(event_key)
                break
    return matching_events


def build_mongo_match_conditions(event_key: str, item_prefix: str = "item") -> list:
    """
    Build MongoDB $match conditions for an event's category paths.

    Args:
        event_key: The event identifier
        item_prefix: The field prefix for item document (default: "item", can be "item_doc" etc.)

    Returns:
        List of $or conditions for MongoDB query

    Example output:
        [
            {"item.data.shoppingCategory.en": "groceries", "item.data.shoppingSubcategory.en": "supermarkets"},
            {"item.data.shoppingCategory.en": "fashion", "item.data.shoppingSubcategory.en": "jewelry"}
        ]
    """
    paths = get_event_category_paths(event_key)
    conditions = []

    for path in paths:
        condition = {}
        if "shoppingCategory" in path:
            condition[f"{item_prefix}.data.shoppingCategory.en"] = path["shoppingCategory"]
        if "shoppingSubcategory" in path:
            condition[f"{item_prefix}.data.shoppingSubcategory.en"] = path["shoppingSubcategory"]
        if "itemCategory" in path:
            condition[f"{item_prefix}.data.itemCategory.en"] = path["itemCategory"]
        if "itemSubcategory" in path:
            condition[f"{item_prefix}.data.itemSubcategory.en"] = path["itemSubcategory"]

        if condition:
            conditions.append(condition)

    return conditions


# =============================================================================
# CATEGORY PATH VALIDATION (optional - uncomment to enable)
# =============================================================================

# def validate_category_paths():
#     """
#     Validate that all category paths reference valid categories from category_mapping.py
#     """
#     from category_mapping import (
#         shoppingCategory,
#         shoppingSubcategory_map,
#         itemCategory_map,
#         itemSubcategory_map
#     )
#
#     errors = []
#
#     for event_key, event_data in EVENT_CATEGORY_MAPPING.items():
#         for i, path in enumerate(event_data.get("category_paths", [])):
#             shop_cat = path.get("shoppingCategory")
#             shop_subcat = path.get("shoppingSubcategory")
#             item_cat = path.get("itemCategory")
#             item_subcat = path.get("itemSubcategory")
#
#             if shop_cat and shop_cat not in shoppingCategory:
#                 errors.append(f"{event_key}[{i}]: Invalid shoppingCategory '{shop_cat}'")
#
#             if shop_subcat and shop_cat:
#                 valid_subcats = shoppingSubcategory_map.get(shop_cat, [])
#                 if shop_subcat not in valid_subcats:
#                     errors.append(f"{event_key}[{i}]: Invalid shoppingSubcategory '{shop_subcat}' for '{shop_cat}'")
#
#     return errors


if __name__ == "__main__":
    # Example usage
    print("=== Seasonal Event Category Mapping ===\n")

    # List all events
    print("Available events:")
    for event_key in get_all_events():
        print(f"  - {event_key}: {get_event_name(event_key)}")

    print("\n" + "="*50 + "\n")

    # Example: Get Valentine's Day paths
    print("Valentine's Day category paths:")
    for path in get_event_category_paths("valentines_day"):
        parts = [f"{k}: {v}" for k, v in path.items()]
        print(f"  -> {' | '.join(parts)}")

    print("\n" + "="*50 + "\n")

    # Example: Get events with 'fashion' category
    print("Events with 'fashion' category:")
    for event_key in get_events_by_category("fashion"):
        print(f"  - {get_event_name(event_key)}")
