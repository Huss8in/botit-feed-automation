# Level 1: shoppingCategory
shoppingCategory = [
    "stationary", "restaurants", "electronics", "pharmacies", "pet care", "home and garden",
    "beauty", "entertainment", "health and nutrition", "groceries", "fashion",
    "automotive", "sports", "kids", "flowers and gifts"
]
# ------------------------------------------------------------------------------------------------------------------------------ #
# Level 2: shoppingSubcategory
fashion_shoppingSubcategory = ["sportswear", "casual wear", "beach wear", "maternity", "undergarments", "designer wear", "plus sizes", "medical wear", "sleepwear", "swimwear", "footwear", "jewelry", "eyewear", "religious wear", "baby clothes", "accessories"]
beauty_shoppingSubcategory = ["skincare", "haircare", "fragrances", "cosmetics"]
stationary_shoppingSubcategory = ["arts and crafts", "stationary accessories", "office supplies", "stationary supplies", "school supplies"]
automotive_shoppingSubcategory = ["auto care", "auto accessories", "motorcycle care"]
pharmacies_shoppingSubcategory = ["women's care", "men's care", "eye care", "dental care", "incontinence", "medicine", "first aid and medical equipment"]
health_nutrition_shoppingSubcategory = ["vitamins", "natural solutions", "protein products", "preformance supplements", "dietary supplements", "weight management"]
sports_shoppingSubcategory = ["outdoor sports", "water sports", "fitness and training", "team sports", "winter sports", "recreational activities", "martial arts"]
home_garden_shoppingSubcategory = ["kitchenwear", "bakeware", "tableware", "drinkware", "household products", "storage and organization", "bed and bath", "home decor", "appliances", "lighting", "furniture", "gardening and outdoor", "hardware and home improvement"]
flowers_gifts_shoppingSubcategory = ["flowers", "gifts"]
groceries_shoppingSubcategory = ["supermarkets", "specialty foods", "mini marts", "farm to table"]
electronics_shoppingSubcategory = ["electronics", "computers", "phones", "photography"]
entertainment_shoppingSubcategory = ["books", "musical instruments", "musical equipment", "movies", "music", "gaming"]
kids_shoppingSubcategory = ["kids furniture", "baby care", "baby furniture", "baby travel", "baby safety products", "toys and games"]
petcare_shoppingSubcategory = ["dogs", "cats", "birds", "horses", "aquatic animals", "small pet supplies", "cows"]
restaurants_shoppingSubcategory = [
    "burgers", "fast food", "pizza", "pasta", "sandwiches", "grills", "juices and drinks", "desserts", "cafes",
    "international", "bakery and cakes", "salads", "italian", "egyptian", "middle eastern", "sushi", "chinese",
    "japanese", "vegan", "vegetarian", "seafood", "asian", "mediterranean", "mexican", "american", "lebanese",
    "thai", "korean", "indian", "vietnamese", "french", "street food", "keto", "healthy"
]

shoppingSubcategory_map = {
    "fashion": fashion_shoppingSubcategory,
    "beauty": beauty_shoppingSubcategory,
    "stationary": stationary_shoppingSubcategory,
    "automotive": automotive_shoppingSubcategory,
    "pharmacies": pharmacies_shoppingSubcategory,
    "health and nutrition": health_nutrition_shoppingSubcategory,
    "sports": sports_shoppingSubcategory,
    "home and garden": home_garden_shoppingSubcategory,
    "flowers and gifts": flowers_gifts_shoppingSubcategory,
    "groceries": groceries_shoppingSubcategory,
    "electronics": electronics_shoppingSubcategory,
    "entertainment": entertainment_shoppingSubcategory,
    "kids": kids_shoppingSubcategory,
    "pet care": petcare_shoppingSubcategory,
    "restaurants": restaurants_shoppingSubcategory
}
# ------------------------------------------------------------------------------------------------------------------------------ #
# Level 3: itemCategory
fashion_itemCategory = {
    # Shared mapping for multiple fashion subcategories
    **dict.fromkeys(
        [
            "sportswear", "casual wear", "beach wear", "maternity",
            "undergarments", "designer wear", "plus sizes",
            "medical wear", "sleepwear"
        ],
        [
            "top", "outerwear", "trousers", "skirt", "underwear",
            "suit", "robe", "uniform", "pajamas", "dress", "outfit"
        ]
    ),

    # Unique mappings for other categories
    "swimwear": ["bathing cover", "swimsuit"],

    "footwear": [
        "sandal", "slipper", "stocking", "sock", "shoe accessory",
        "boot", "sports shoe", "shoe"
    ],

    "jewelry": [
        "earring", "necklace", "bracelet", "ring", "broche",
        "tie pin", "pendant", "cufflink", "jewelry set",
        "head ornament", "jewelry box"
    ],

    "eyewear": ["glasses", "sunglasses"],

    "religious wear": [
        "islamic religious wear", "christian religious wear"
    ],

    "baby clothes": [
        "onesie", "baby gown", "bloomers", "diaper cover",
        "babygrow", "baby sock", "diaper shirt", "baby mitten",
        "romper", "baby accessory", "lap tee", "baby leggings",
        "baby shoe", "jumpsuit"
    ],

    "accessories": [
        "umbrella", "wallet", "hand fan", "watch", "belt",
        "neckwear and scarf", "bag", "headwear",
        "hair accessory", "glove"
    ]
}

beauty_itemCategory = {
    "skincare": ["foot care", "hair removal", "acne", "face soap", "face cleanser", "bath soap", "body moisturizer", "hand care", "face treatment", "skin whitening", "face scrub", "face mask", "bath salt", "body oil", "injectables", "loofah and sponge", "anti-aging", "dark spot", "face toner", "hand soap", "bath cream", "face roller", "skincare set", "cotton", "eye treatment", "sunscreen", "face moisturizer", "body scrub", "shower gel", "skincare accessory"],
    "haircare": ["hair gel", "hair mousse", "hair wax", "hair spray", "hair cream", "hair conditioner", "hair mask", "haircare set", "hair brush and comb", "hair styling tool", "hair dye", "hair loss", "hair shampoo", "hair oil", "hair serum", "hair treatment"],
    "fragrances": ["body spray", "cologne", "perfume"],
    "cosmetics": ["eye make-up", "lip make-up", "face make-up", "nailcare", "cosmetic accessory", "make-up tool", "body make-up", "cosmetic set"]
}

stationary_itemCategory = {
    "arts and crafts": ["craft supply", "knitting", "sewing", "jewelry making", "painting", "drawing", "pottery", "sculpting", "candle making", "doll making", "craft fabric", "floral arranging", "weaving", "print making", "basket making", "arts and crafts set"],
    "stationary accessories": ["keychain", "document holder"],
    "office supplies": ["scissors", "tape", "glue", "pencil", "pen", "marker", "sharpener", "eraser", "stapler", "tack", "paper clip", "office supply accessories"],
    "stationary supplies": ["desk organizer", "desk planner", "calendar", "agenda", "diary", "paper puncher", "white board", "sticky note", "sheet protector", "photo album", "compass"],
    "school supplies": ["notebook", "writing pad", "folder", "pencil case", "pencil holder", "book cover", "chalk board", "chalk", "crayon", "clip board", "cork board", "bookmark", "ruler", "school supply accessories"]
}

automotive_itemCategory = {
    "auto care": ["auto lighting", "oil and fluid", "auto paint", "auto part", "auto finishing", "auto tire", "auto tool", "auto cleaning kit", "auto sealant"],
    "auto accessories": ["interior accessory", "exterior accessory"],
    "motorcycle care": ["motorcycle accessory", "motorcycle gear", "motorcycle part", "mopeds", "motorcycle tire", "motorcycle tool", "motorcycle oil and fluid"]
}

pharmacies_itemCategory = {
    "women's care": ["feminine hygiene", "women's deodorant", "women's sexual health"],
    "men's care": ["men's sexual health", "men's shaving products", "men's hygiene", "men's deodorant", "men's hair product", "men's skin product"],
    "eye care": ["lenses", "lens solution", "eye drop"],
    "dental care": ["toothpaste", "toothbrush", "dental floss", "mouth wash", "teeth whitener"],
    "incontinence": ["adult diaper", "bed protection"],
    "medicine": ["critical care medicine", "first aid medicine", "immune system medicine", "urinary tract disorder medicine", "hemorrhoid and varicose medicine", "blood disorder medicine", "antibiotic", "women's health medicine", "prescription", "cold medicine", "stomach medicine", "sleep medicine", "pain medicine", "sinus medicine", "allergy medicine", "pediatrics medicine", "oral care", "ear medicine", "eye medicine", "skin medicine", "foot medicine", "heart and blood pressure medicine", "anti-infective medicine", "addiction disorder medicine", "hormone medicine", "cns medicine", "fever medicine", "vaccine and serum medicine", "asthma medicine", "diabetes medicine", "anti cancer medicine", "bone disorder medicine"],
    "first aid and medical equipment": ["monitor", "thermometer", "bandage", "alcohol", "home test", "gauze", "ppe", "plaster", "brace", "medical accessory", "sanitizer", "sleeping aid"]
}

health_nutrition_itemCategory = {
    "vitamins": ["multivitamin", "hair vitamin", "skin vitamin", "baby vitamin", "kid vitamin", "pregnancy vitamin", "mineral", "basic vitamin"],
    "natural solutions": ["herbal supplement", "detox product", "cleansing product", "essential oils"],
    "protein products": ["whey", "casein", "animal protein", "plant protein", "protein bar", "protein drink"],
    "preformance supplements": ["pre-workout supplement", "post-workout supplement", "muscle builder", "mass gainer", "energy supplement"],
    "dietary supplements": ["royal jelly", "probiotic", "prebiotic", "antioxidant", "enzyme", "collagen", "omega", "digestive supplement", "joint supplement", "specialty supplement"],
    "weight management": ["appetite suppressant", "fat burner", "diuretic", "diet system", "meal replacement"]
}

sports_itemCategory = {
    "outdoor sports": ["cycling", "golf", "fishing", "hunting", "horse riding", "climbing", "hiking", "camping", "boating"],
    "water sports": ["windsurfing", "swimming", "surfing", "kayaking", "scuba diving", "snorkeling", "water polo", "kitesurfing"],
    "fitness and training": ["running", "yoga", "dance", "weight training", "boxing", "kickboxing", "cardio machines", "gym equipment", "cross-training"],
    "team sports": ["rugby", "gymnastics", "football", "basketball", "american football", "baseball", "volleyball", "wrestling", "track and field", "field hockey", "handball"],
    "winter sports": ["ice skating", "skiing", "snowboarding", "ice hockey"],
    "recreational activities": ["table tennis", "billiards", "archery", "darts", "scooter", "frisbie", "tennis", "badminton", "kite", "bowling", "croquet", "rollerblading", "skateboarding", "squash", "recreational games"],
    "martial arts": ["judo", "jujitsu", "taekwondo", "aikido", "karate"]
}

home_garden_itemCategory = {
    "kitchenwear": ["cooking utensil", "cooking tool", "speciality cookwear", "ovenware", "pot and pan", "kitchen accessory"],
    "bakeware": ["baking pan", "bakeware utensil", "bakeware accessory"],
    "tableware": ["cutlery", "plate and bowl", "table linen"],
    "drinkware": ["cup", "wine glass", "beer glass", "shot glass", "brandy glass", "tumbler", "coaster", "jar", "trembleuse", "glass", "champagne flute", "sake cup", "cognac glass", "whisky glass", "teacup", "pitcher", "wine opener", "straw", "mug", "martini glass", "sherry glass", "margarita glass", "rummer", "beaker", "carafe", "flask", "drinkware accessory"],
    "household products": ["cleaning tool", "cleaning product", "house supply"],
    "storage and organization": ["office storage and organization", "clothing storage and organization", "bathroom storage and organization", "bedroom storage and organization", "kitchen storage and organization", "outdoor storage and organization", "kids storage and organization", "garage storage and organization", "trash bin", "basket", "food container", "rack", "drawer", "shelf", "hook", "recycling"],
    "bed and bath": ["bath linen", "bathroom accessory", "bathroom hardware", "bedding"],
    "home decor": ["wallpaper", "candle", "tapestery", "picture frame", "home scent", "mirror", "home decor accessory", "clock", "vase", "wall art", "decorative plate", "incense", "potpurri"],
    "appliances": ["personal appliance", "kitchen appliance", "home appliance", "heating and cooling unit", "cleaning appliance"],
    "lighting": ["wall lighting", "lighting accessory", "lamp", "ceiling lighting", "chandelier", "floor lighting", "light bulb", "outdoor lighting", "underwater lighting", "lighting system"],
    "furniture": ["bedroom furniture", "kitchen furniture", "bathroom furniture", "dining room furniture", "living room furniture", "office furniture", "outdoor furniture", "furniture accessory"],
    "gardening and outdoor": ["gardening tool", "gardening equipment", "gardening care", "pool equipment"],
    "hardware and home improvement": ["home tool", "measuring tool", "plumbing tool", "electrical tool"]
}

flowers_gifts_itemCategory = {
    "flowers": ["bouquet", "seasonal flower", "floral decoration", "plant"],
    "gifts": ["gift wrapping", "greeting card", "gift card"]
}

groceries_itemCategory = {
    "supermarkets": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "specialty foods": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "mini marts": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "farm to table": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"]
}

electronics_itemCategory = {
    "electronics": ["electronic accessory", "gps system", "vehicle electronic", "office electronic", "portable electronic", "wearable technology", "security and surveillance", "headphone and speaker", "sound system", "tv and video"],
    "computers": ["laptop", "cpu and data processor", "hard drive and sdd", "motherboard", "computer monitor", "software", "networking product", "video graphic card", "data memory", "data storage", "tablet"],
    "phones": ["smart phone", "feature phone"],
    "photography": ["binocular and optics", "digital camera", "film photography", "camera case", "flash", "video security", "lens", "studio", "video camera", "photo printer", "photo scanner", "camera stand", "underwater photography"]
}

entertainment_itemCategory = {
    "books": ["art book", "biography", "business book", "finance book", "magazine", "newspaper", "architecture book", "music book", "photography book", "fashion book", "young adult book", "comic book", "children book", "technology book", "science book", "graphic novel", "culinary book", "general reference book", "health book", "home and garden book", "psychology book", "travel book", "outdoor book", "craft and hobby book", "literature and fiction", "spirituality book", "textbook", "medical book", "parenting book", "relationship book", "political science book", "social science book", "nature book", "game book", "educational book", "engineering book", "history book", "geography book", "science fiction book", "humor book", "nutrition book", "how to book", "sports book", "poetry", "foreign language book", "culture book", "society book", "study guide", "self-help book", "philosophy book", "religion book"],
    "musical instruments": ["folklore instrument", "synthesizer", "amplifier", "guitar", "bass", "ukelele", "electric keyboard", "organ", "piano", "electronic instrument", "percussion", "wind instrument", "brass instrument", "string instrument", "organ accessory", "piano accessory", "musical set", "percussion accessory", "wind accessory", "guitar accessory", "bass accessory", "string accessory"],
    "musical equipment": ["karaoke equipment", "music microphone", "mixer", "computer recording", "pa system", "stage lighting", "studio mixer", "studio monitor", "multitrack record", "controller", "wireless mic system", "audio interface", "dj headphone", "dj turntable", "drum machine", "karaoke", "speaker and sub", "musical equipment accessory"],
    "movies": ["hd movie", "rental movie", "dvd movie", "blu ray movie"],
    "music": ["cd", "record"],
    "gaming": ["video game console", "video game accessory", "video game"]
}

kids_itemCategory = {
    "kids furniture": ["kids bed", "kids table", "kids desk", "kids mattress", "kids nightstand", "kids couch", "kids chair", "kids furniture accessory"],
    "baby care": ["baby diaper", "baby food", "baby formula", "baby wipe", "baby skincare", "baby haircare", "baby bottle", "pacifier", "teether", "baby bib", "breastfeeding aid", "nursing product", "baby food maker", "bottle sterilizer", "baby utensil", "baby care accessory"],
    "baby furniture": ["playpen", "crib", "bassinet", "changing table", "nursery center", "baby swing", "baby mattress", "baby furniture accessory"],
    "baby travel": ["stroller", "car seat", "baby sling", "diaper bag"],
    "baby safety products": ["cabinet safety", "corner and edge safety", "safety cover", "appliance latch", "electrical safety", "bathroom safety", "baby monitor"],
    "toys and games": ["educational game", "toddler toy", "doll", "game", "collectible", "toy vehicle", "outdoor toy", "toy figure", "pretend play", "party supply", "puppet", "building set"]
}

petcare_itemCategory = {
    "dogs": ["dry dog food", "wet dog food", "dog toy", "dog treat", "dog accessory", "dog flea and tick", "dog supplement", "dog grooming", "dog cage", "dog carrier", "dog clothes", "dog supply"],
    "cats": ["dry cat food", "wet cat food", "cat toy", "cat litter", "cat accessory", "cat flea and tick", "cat supplement", "cat grooming", "cat cage", "cat carrier", "cat clothes", "cat supply", "cat treat"],
    "birds": ["bird food", "bird accesory", "bird supplement", "bird cage", "bird supply"],
    "horses": ["horse food", "horse accessory", "horse treat", "horse supplement", "horse grooming", "stable supply"],
    "aquatic animals": ["fish food", "fish accesory", "fish supplement", "aquarium", "aquarium supply"],
    "small pet supplies": ["reptile supply", "hamster supply", "rabbit supply", "small pet accessory"],
    "cows": ["cow supplement"]
}

restaurants_itemCategory = {
    "burgers": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "fast food": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "pizza": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "pasta": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "sandwiches": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "grills": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "juices and drinks": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "desserts": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "cafes": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "international": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "bakery and cakes": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "salads": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "italian": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "egyptian": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "middle eastern": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "sushi": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "chinese": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "japanese": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "vegan": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "vegetarian": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "seafood": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "asian": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "mediterranean": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "mexican": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "american": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "lebanese": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "thai": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "korean": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "indian": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "vietnamese": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "french": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "street food": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "keto": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"],
    "healthy": ["beverage", "produce", "tobacco product", "pantry", "pasta", "dairy", "grain", "snacks", "baking", "bakery", "recharge card", "seafood", "meat and poultry", "condiment", "sweet", "deli"]
}

itemCategory_map = {
    "fashion": fashion_itemCategory,
    "beauty": beauty_itemCategory,
    "stationary": stationary_itemCategory,
    "automotive": automotive_itemCategory,
    "pharmacies": pharmacies_itemCategory,
    "health and nutrition": health_nutrition_itemCategory,
    "sports": sports_itemCategory,
    "home and garden": home_garden_itemCategory,
    "flowers and gifts": flowers_gifts_itemCategory,
    "groceries": groceries_itemCategory,
    "electronics": electronics_itemCategory,
    "entertainment": entertainment_itemCategory,
    "kids": kids_itemCategory,
    "pet care": petcare_itemCategory,
    "restaurants": restaurants_itemCategory
}
# ------------------------------------------------------------------------------------------------------------------------------ #
# level 4: itemSubcategory 

fashion_itemSubcategory = {
    "top": ["kimono", "sweatshirt", "sweater", "tank top", "blouse", "t-shirt", "shirt"],
    "outerwear": ["jacket", "blazer", "coat", "vest"],
    "trousers": ["overalls", "pants", "jeans", "shorts", "leggings"],
    "skirt": ["skort"],
    "underwear": ["undershirt", "bra", "panty", "boxers", "briefs", "nightgown", "camisole", "babydoll", "slip", "corset"],
    "boot": ["work boot", "riding boot", "sports boot", "combat boot", "snow boot", "rain boot"],
    "sports shoe": ["tennis shoe", "cycling shoe", "cleats", "golf shoe", "walking shoe", "basketball shoe", "cross trainers", "running shoe"],
    "shoe": ["dress shoe", "casual shoe", "heels", "flats"],
    "belt": ["suspender"],
    "neckwear and scarf": ["tie", "ascot", "boa", "handkerchief", "shawl", "pashmina", "scarf", "bandana"],
    "bag": ["purse", "luggage", "trunk", "backpack", "briefcase", "laptop case"],
    "headwear": ["cap", "visor", "beanie", "hat", "beret", "fedora", "fascinator"],
    "hair accessory": ["hairpin", "barrette", "headband", "shower cap", "hairband", "scrunchie", "hair extension", "sweatband", "wig", "hair clip", "hair piece"],
    "glove": ["mitten"]
}

stationary_itemSubcategory = {
    "craft supply": ["adhesive", "fastener", "clock kit", "craft bell", "craft foam", "craft stick", "cutting tool", "face paint", "glitter and feather", "gold leaf", "metal leaf"],
    "knitting": ["yarn", "knitting needle", "knitting kit", "knitting accessory"],
    "sewing": ["sewing machine", "sewing fabric", "sewing thread", "sewing needle", "button", "zipper", "sewing pattern", "sewing kit", "embroidery", "sewing accessory"],
    "jewelry making": ["bead", "charm", "engraving tool", "jewelry casting", "jewelry kit", "polishing tool", "stamping tool", "jewelry making accessory"],
    "painting": ["paint tool", "paint", "paint thinner", "paint brush", "paint roller", "primer and stain", "paint cleaner", "easel", "canvas", "palette", "paint accessory"],
    "drawing": ["drawing tool", "sketch pad", "art paper", "drawing accessory", "portfolio case", "poster tube"],
    "pottery": ["clay mixer", "clay presser", "pottery glaze", "pottery mold", "kiln and firing", "pottery wheel", "pug mill", "slab roller", "ready to paint", "pottery accessory"],
    "sculpting": ["clay", "modeling tool", "modeling compound", "sculpting mold", "release agent", "wire and armature", "sculpting accessory"],
    "candle making": ["candle dye", "candle kit", "candle mold", "candle scent", "candle wax", "candle wick"],
    "doll making": ["doll eye", "doll nose", "doll hair", "doll making kit", "doll lash", "doll body", "doll making tool", "doll making accessory", "doll head"],
    "craft fabric": ["ribbon", "mesh", "fabric glue", "fabric kit", "fabric paint", "fabric supply"],
    "floral arranging": ["floral foam", "floral moss", "floral pick", "floral tape", "vase filler", "floral arranging supply"],
    "weaving": ["weaving loom", "ball winder", "wool roving", "weaving accessory"],
    "print making": ["etching tool", "heat press machine", "printing press", "printing ink", "print making accessory"]
}

beauty_itemSubcategory = {
    "eye make-up": ["eyeliner", "mascara", "eyebrow", "eyelash", "eye shadow", "eye primer"],
    "lip make-up": ["lip gloss", "lipstick", "lip liner", "lip balm"],
    "face make-up": ["foundation", "face powder", "bronzer", "blush", "corrector", "concealer", "face primer", "setting powder", "make-up set"],
    "nailcare": ["nail polish", "nail polish remover", "nail clipper", "nail file", "nail buffer", "nail kit", "nail accessory"],
    "cosmetic accessory": ["cosmetic mirror", "make-up remover", "make-up towel", "make-up bag"],
    "make-up tool": ["tweezers", "eyeliner brush", "eyeshadow brush", "blush brush", "powder brush", "face brush", "fan brush", "make-up sponge", "powder puff"]
}

pharmacies_itemSubcategory = {"women's sexual health": ["lubricant"]}

home_garden_itemSubcategory = {
    "cooking utensil": ["spatula", "ladle", "strainer", "colander", "measuring cup", "whisk", "cutting board", "measuring spoon", "meat thermometer", "timer", "pizza cutter", "cheesecloth", "kitchen scale", "knife"],
    "cooking tool": ["grater", "can opener", "corer", "pitter", "eggs slicer", "kitchen shears", "zester", "cooking torch", "spiralizer", "salad spinner", "vegetable peeler", "tongs", "mallet"],
    "speciality cookwear": ["wok", "fondue set", "poacher", "chafing", "crepe maker", "turkish coffee pot", "french press", "vietnamese coffee pot", "teapot", "bamboo steamer", "frying basket", "steamer insert", "tagine", "smoker", "italian coffee pot", "percolator", "siphon coffee pot", "tea strainer"],
    "ovenware": ["casserole dish", "pizza stone", "terrine", "timbale", "rotisserie", "pyrex", "souffle dish", "quiche dish"],
    "pot and pan": ["skillet", "griddle", "cookware set", "dutch oven", "french oven", "saucier", "double boiler", "braiser"],
    "kitchen accessory": ["kitchen towel", "apron", "oven mitt"],
    "baking pan": ["pie dish", "cake pan", "bread pan", "cake ring", "muffin pan", "cake mold", "springform", "ramkin"],
    "bakeware utensil": ["rolling pin", "cookie cutter", "pastry brush", "pastry board", "cake decorating", "cake tester", "sifter", "pastry bag", "piping tip", "icing comb", "pie marker", "pastry cutter", "dough cutter", "baking mold", "cake marker", "pastry cloth", "dough board"],
    "bakeware accessory": ["cake turntable", "baking mat", "silicon mold", "donut dispenser", "cupcake cases", "oil brush", "rolling mat", "cake stencil", "pastry mat", "cake dummy", "cake smoother", "parchment paper"],
    "cutlery": ["dinner fork", "serving spoon", "steak knife", "dessert fork", "dinner spoon", "serving fork", "fish fork", "dessert spoon", "dinner knife", "soup spoon", "fruit spoon", "chopstick", "salad spoon", "teaspoon", "fruit knife", "skewer", "salad fork", "table spoon", "carving fork", "cocktail stick", "salt shaker", "pepper shaker", "butter knife", "crab cracker", "fish knife", "fondue fork", "grapefruit knife", "grapefruit spoon", "lobster pick", "honey dipper", "nutcracker", "escargot tong"],
    "plate and bowl": ["gravy bowl", "dessert plate", "appetizer plate", "luncheon plate", "serving bowl", "serving dish", "soup bowl", "rice bowl", "finger bowl", "dinner plate", "bread and butter plate"],
    "table linen": ["table cloth", "napkin", "dry bar cover", "chair cover", "table runner", "placemat", "table skirting", "table padding", "skirting clip"],
    "cleaning tool": ["mop", "duster", "bucket", "dustpan", "floor scrubber", "stepladder", "broom", "toilet brush", "cleaning cloth", "feather duster", "carpet sweeper", "lint remover", "squeegee", "scrubbing brush", "sponge", "rubber gloves", "microfiber cloth", "spray bottle", "scaffold", "hataki", "soap shaker"],
    "cleaning product": ["glass cleaner", "oven cleaner", "furniture cleaner", "furniture polish", "disinfectant", "laundry detergent", "stain remover", "bathroom cleaner", "stove top cleaner", "floor cleaner", "silver polish", "dishwasher detergent", "kitchen soap"],
    "house supply": ["freezer bag", "tissue and paper towel", "cling wrap and foil", "insect repellent", "garbage bag", "toilet paper", "air freshener"],
    "bath linen": ["bath towel", "beach towel", "bath rug", "bathrobe", "bath linen set"],
    "bathroom accessory": ["soap dispenser", "soap dish", "toothbrush holder", "tissue paper dispenser"],
    "bathroom hardware": ["towel holder", "bathroom rack", "toilet paper dispenser", "bathroom hook", "showerhead"],
    "bedding": ["duvet", "blanket", "comforter and quilt", "bed sheet", "pillow case", "bed linen set", "pillow"],
    "personal appliance": ["styling iron", "blowdryer", "electric shaver"],
    "kitchen appliance": ["blender", "microwave", "food processor", "cooker", "mixer", "bread machine", "kitchen grill", "specialty appliance", "fryer", "toaster", "food steamer", "juicer", "coffee maker", "kettle", "pasta maker"],
    "home appliance": ["oven", "stove", "refrigerator", "freezer", "cooler", "iron", "water filter", "water dispenser", "air purifier", "scale", "water heater"],
    "heating and cooling unit": ["air conditioner", "heater", "fan", "air cooler", "ventilation"],
    "cleaning appliance": ["dishwasher", "washer", "dryer", "vacuum"],
    "bedroom furniture": ["bedroom closet", "bedside table", "bedroom chair", "bed", "mattres", "headboard", "dresser", "bedroom furniture set"],
    "kitchen furniture": ["kitchen closet", "kitchen table", "kitchen bench", "kitchen cabinet", "kitchen countertop", "kitchen sink", "kitchen faucet", "kitchen chair", "barstool", "kitchen fixture", "kitchen furniture set"],
    "bathroom furniture": ["bathroom closet", "bathroom table", "bathroom cabinet", "bathroom countertop", "bathroom sink", "bathroom faucet", "bathroom fixture", "bathtub"],
    "dining room furniture": ["dining room cabinet", "dining room table", "dining room chair", "dining room buffet", "dining room bar", "dining room cart", "dining room furniture set"],
    "living room furniture": ["living room bookcase", "coffee table", "side table", "sofa and loveseat", "lazyboy", "poof", "beanbag", "ottoman", "living room chair", "media console", "TV stand", "living room furniture set"],
    "office furniture": ["office cabinet", "desk", "desk chair", "office table"],
    "outdoor furniture": ["outdoor table", "outdoor chair", "outdoor bar", "outdoor kitchen", "outdoor furniture set", "outdoor umbrella", "outdoor rug", "doormat", "bench", "outdoor cookware"],
    "furniture accessory": ["curtain", "rug", "blinds", "shades", "furniture fabric", "room divider"],
    "gardening tool": ["rake", "hoe", "shovel", "wheelbarrow", "garden sprayer", "clipper", "spade", "trowel", "fork"],
    "gardening equipment": ["gardening fence", "planter", "gardening accessory", "hose", "sprinkler", "irrigation", "aquaponics", "watering system", "lawnmower"],
    "gardening care": ["fertilizer", "fungicide", "gardening nutrient", "growing kit", "root stimulator", "soil tester", "soil", "gardening seed"],
    "pool equipment": ["chlorine", "pool pump", "pool vacuum", "pool brush", "leaf skimmer", "pool ladder", "pool testing", "pool thermometer"],
    "home tool": ["power tool", "hand tool", "welding", "duct tape", "cord", "flashlight", "nail and screw", "fastener and snap", "padlock", "shelf support", "window hardware"],
    "measuring tool": ["linear measuring", "carpentry square", "measuring wheel", "protractor"],
    "plumbing tool": ["caulking", "sealing tape", "plumbing wire", "plumbing pipe", "plumbing valve", "faucet part", "garbage disposal part", "toilet part", "water heater part", "water pump part"],
    "electrical tool": ["plug socket", "electrical outlet", "electrical box", "electrical connector", "electrical motor", "home automation device", "dimmer", "switch", "wall plate", "circuit breaker", "electrical insulation", "light socket", "electrical tape", "electrical wire"]
}

flowers_gifts_itemSubcategory = {"gift wrapping": ["gift wrap paper", "gift box", "gift bag", "gift wrap cellophane", "gift wrapping accessory", "gift basket", "gift box filling", "gift wrap set", "gift wrap ribbon", "gift wrap tag"]}

groceries_itemSubcategory = {
    "beverage": ["water", "coffee", "tea", "soda", "juice", "smoothie", "shake", "hot cocoa"],
    "produce": ["fruit", "vegetable", "herb", "bean", "lentil", "chickpea", "soybean"],
    "pantry": ["vinegar", "oil", "seasoning", "broth", "sugar", "salt", "sweetener"],
    "dairy": ["milk", "cream", "yogurt", "egg", "margarine", "butter", "ghee", "cheese"],
    "grain": ["granola", "oats", "rice", "quinoa", "couscous", "cereal", "seeds"],
    "snacks": ["popcorn", "pretzel", "rice cake", "chip", "nuts", "dried fruit"],
    "baking": ["flour", "topping", "dessert mix", "cocoa powder"],
    "bakery": ["pastry", "bread", "breadstick", "cracker", "crouton", "bread crumbs", "bagel"],
    "seafood": ["fish", "shrimp", "crab", "lobster", "mussels", "clam", "oyster", "calamari", "octopus", "caviar"],
    "meat and poultry": ["chicken", "turkey", "duck", "quail", "pigeon", "lamb", "veal", "sirloin", "t-bone", "kebab", "kobeba", "burger", "steak", "sausage", "hotdog", "fillet", "kofta", "ground meat", "ribeye", "shank", "piccata", "roast", "escalope", "meatballs", "paupiette", "ossobuco", "ribs", "liver", "tongue", "beef strip", "shish tawook", "shawerma"],
    "condiment": ["mustard", "ketchup", "spread", "dressing", "sauce", "honey", "jam", "mayonnaise", "relish", "chutney", "syrup", "salsa", "paste"],
    "sweet": ["cake", "waffle", "pancake", "gateau", "doughnut", "gum", "oriental sweets", "brownie", "muffin", "cupcake", "pie", "tart", "biscuit", "ice cream", "chocolate", "candy"],
    "deli": ["soup", "dolmas", "spring roll", "fries", "baked potato", "readymade food", "mombar", "koshari", "falafel", "fatta", "sushi", "pickle", "dip", "salad", "cold cut", "sandwich", "pizza", "olive", "hawawshi", "molokhia", "fava beans", "sashimi", "crepe"]
}

electronics_itemSubcategory = {
    "electronic accessory": ["audio-video accessory", "photography accessory", "phone accessory", "computer accessory", "tablet accessory", "laptop accessory", "headphone and speaker accessory", "sound system accessory", "office equipment accessory", "vehicle electronics accessory", "battery", "power surge protector", "tv accessory", "cable", "power adaptor", "microphone", "video game console accessory", "charger and power bank"],
    "gps system": ["boats gps", "gps tracker", "item finder", "handheld gps", "sports gps", "vehicle gps"],
    "vehicle electronic": ["aviation electronic", "automotive electronic", "marine electronic", "power sport electronic"],
    "office electronic": ["calculator", "copier", "document camera", "electrical translator", "pda", "pos equipment", "video projector", "printer and scanner"],
    "portable electronic": ["portable tv", "portable player", "portable radio"],
    "wearable technology": ["body-mounted camera", "arm band", "smart glasses", "smart watch", "virtual reality"],
    "security and surveillance": ["biometric", "home security system", "horn and siren", "motion detector", "radio scanner", "surveillance camera", "surveillance video equipment"],
    "headphone and speaker": ["wireless headphone", "wireless speaker", "portable speaker"],
    "sound system": ["home theater", "stereo speaker", "wireless and audio streaming", "stereo system component", "turntable", "stereo"],
    "tv and video": ["av receiver and av amplifier", "blu ray player", "dvd player", "projector screen", "led and lcd", "satellite system", "streaming media player"]
}

entertainment_itemSubcategory = {
    "video game console": ["playstation", "xbox", "wii", "nintendo"],
    "video game accessory": ["playstation accessory", "xbox accessory", "wii accessory", "nintendo accessory"],
    "video game": ["pc game", "playstation game", "xbox game", "wii game", "nintendo game"]
}

kids_itemSubcategory = {
    "educational game": ["math", "counting", "flashcard", "science", "reading", "writing", "educational electronic"],
    "toddler toy": ["bath toy", "indoor climber", "musical toy", "building block", "activity center", "stuffed animal"],
    "doll": ["fashion doll", "baby doll", "doll house", "doll playset", "doll accessory"],
    "game": ["puzzle", "card game", "dice game", "floor game", "boardgame", "electronic game", "travel game", "sports game"],
    "collectible": ["sticker", "card", "stamp"],
    "toy vehicle": ["electric vehicle", "remote control vehicle", "toy train", "train set", "toy boat", "toy plane", "toy rocket", "toy car", "drone", "race car", "race set"],
    "outdoor toy": ["water toy", "playhouse", "sandbox", "playground equipment", "inflatable bouncer", "ball", "wagon", "hover board", "bubble", "beach toy"],
    "toy figure": ["action figure", "animal figure", "dinosaur", "fantasy creature", "hero figure", "celebrity figure", "toy figure playset", "robot"],
    "pretend play": ["pretend tool", "cooking", "housekeeping", "costume", "role playing"],
    "party supply": ["balloon", "party hat", "banner", "party favor", "party toy", "party decoration"],
    "puppet": ["hand puppet", "finger puppet", "marionette", "ventriloquist", "puppet theater"],
    "building set": ["model kit", "construction toy", "stacking block", "pre-built vehicle"]
}
restaurants_itemSubcategory = {
    "beverage": ["water", "coffee", "tea", "soda", "juice", "smoothie", "shake", "hot cocoa"],
    "produce": ["fruit", "vegetable", "herb", "bean", "lentil", "chickpea", "soybean"],
    # "tobacco product": [],
    "pantry": ["vinegar", "oil", "seasoning", "broth", "sugar", "salt", "sweetener"],
    # "pasta": [],
    "dairy": ["milk", "cream", "yogurt", "egg", "margarine", "butter", "ghee", "cheese"],
    "grain": ["granola", "oats", "rice", "quinoa", "couscous", "cereal", "seeds"],
    "snacks": ["popcorn", "pretzel", "rice cake", "chip", "nuts", "dried fruit"],
    "baking": ["flour", "topping", "dessert mix", "cocoa powder"],
    "bakery": ["pastry", "bread", "breadstick", "cracker", "crouton", "bread crumbs", "bagel"],
    # "recharge card": [],
    "seafood": ["fish", "shrimp", "crab", "lobster", "mussels", "clam", "oyster", "calamari", "octopus", "caviar"],
    "meat and poultry": ["chicken", "turkey", "duck", "quail", "pigeon", "lamb", "veal", "sirloin", "t-bone", "kebab", "kobeba", "burger", "steak", "sausage", "hotdog", "fillet", "kofta", "ground meat", "ribeye", "shank", "piccata", "roast", "escalope", "meatballs", "paupiette", "ossobuco", "ribs", "liver", "tongue", "beef strip", "shish tawook", "shawerma"],
    "condiment": ["mustard", "ketchup", "spread", "dressing", "sauce", "honey", "jam", "mayonnaise", "relish", "chutney", "syrup", "salsa", "paste"],
    "sweet": ["cake", "waffle", "pancake", "gateau", "doughnut", "gum", "oriental sweets", "brownie", "muffin", "cupcake", "pie", "tart", "biscuit", "ice cream", "chocolate", "candy"],
    "deli": ["soup", "dolmas", "spring roll", "fries", "baked potato", "readymade food", "mombar", "koshari", "falafel", "fatta", "sushi", "pickle", "dip", "salad", "cold cut", "sandwich", "pizza", "olive", "hawawshi", "molokhia", "fava beans", "sashimi", "crepe"],
}


itemSubcategory_map = {
    "fashion": fashion_itemSubcategory,
    "beauty": beauty_itemSubcategory,
    "restaurants": restaurants_itemSubcategory,
    "stationary": stationary_itemSubcategory,
    "pharmacies": pharmacies_itemSubcategory,
    "home and garden": home_garden_itemSubcategory,
    "flowers and gifts": flowers_gifts_itemSubcategory,
    "groceries": groceries_itemSubcategory,
    "electronics": electronics_itemSubcategory,
    "entertainment": entertainment_itemSubcategory,
    "kids": kids_itemSubcategory
}