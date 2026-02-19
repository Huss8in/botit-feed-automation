# Botit Feed Automation

Analytics dashboard for the Botit e-commerce platform in Egypt. Analyzes order data, seasonal trends, and TikTok trends to help the feed team decide which items and vendors to feature on the app.

![Flask](https://img.shields.io/badge/Flask-2.x-blue) ![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green) ![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)

---

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables (or use .env file)
MONGO_URI=mongodb+srv://...          # Production MongoDB Atlas
LOCAL_MONGO_URI=mongodb://localhost:27017/  # Local cache (optional)
OPENAI_API_KEY=sk-...                # For AI feed generation

# Run the app
python app.py
# Open http://localhost:5000
```

---

## Pages

### 1. Today's Feed (`/feed`)

The main page for daily feed curation. Auto-loads on open — no buttons to click.

| Section | What It Shows | Data Source |
|---------|---------------|-------------|
| **Event Picks** | Items relevant to the nearest seasonal event (e.g. Ramadan, Eid, Mother's Day) | `/api/feed/nearest-event` + `/api/seasonality/event/items` |
| **Top Performers** | Best-selling items and vendors from the last 7 days, in two tabs | `/api/top-items` + `/api/top-vendors` |
| **Trending Up** | Items with growing momentum (7d vs previous 7d, >=20% growth) | `/api/feed/trending-up` |
| **Previously Worked** | Historical best sellers for the same event in past years (2024, 2025) | `/api/seasonality/event/historical-items` |
| **AI Feed Generator** | GPT-powered text recommendations (collapsed at bottom) | `/api/generate-feed` |

**Features:**
- **Sort controls** on every section — sort by Quantity, Orders, Category, Price, or Growth %
- **Copy ID buttons** — click to copy any Item ID or Vendor ID to clipboard
- **Detail modal** — click any card to see full details: large image, full name, category chain (4 levels), all stats, and copyable IDs
- **Feed type badges** — color-coded labels: Event Pick (green), Top Performer (blue), Trending Up (orange), Proven Seller (purple)
- **Delta badges** on trending items — shows "+80%" or "NEW" for new entrants

---

### 2. Dashboard (`/`)

Overview of top vendors and items with flexible date filtering.

**Features:**
- Quick date buttons: 2, 7, 14, 30, 60, 90, 180 days, or 1 year
- Custom date range picker
- Category filter dropdown
- Top Vendors table with rank badges (gold/silver/bronze)
- Top Items table with price, quantity, vendor info
- Collapsible MongoDB pipeline viewer (shows the exact aggregation query)

**Endpoints:** `/api/top-vendors`, `/api/top-items`

---

### 3. Seasonality (`/seasonality`)

Manages the 14 Egyptian seasonal events and their category mappings.

**Sections:**
- **Stats cards** — current season, next event, days until, peak period
- **Annual timeline** — visual horizontal timeline or monthly calendar view
- **Events table** — all events with dates, category, duration, business impact, recommended actions
- **Top items by category path** — pre-computed best sellers per event's category hierarchy (cached in local MongoDB)

**Events covered:**
| Type | Events |
|------|--------|
| Religious | Ramadan, Eid al-Fitr, Eid al-Adha, Mawlid |
| National | Coptic Christmas, Sham El-Nessim |
| Shopping | Valentine's Day, Mother's Day, Back to School, Singles' Day, Black Friday, Year-End Sales |
| Seasonal | Summer Season, Winter Season, Wedding Season |

**Features:**
- Year selector and event category filter
- Click any event for detailed impact analysis modal
- Refresh button to re-compute cached data from production DB
- Cache status badge showing last update time

**Endpoints:** `/api/seasonality/events`, `/api/seasonality/top-items-cached`, `/api/seasonality/pipeline-status`

---

### 4. TikTok Trends (`/trends`)

Maps trending TikTok hashtags in Egypt to product categories, then finds matching vendors and items.

**Sections:**
- **Trending hashtags** — color-coded chips by category with view counts
- **Trending categories** — bar chart of category scores based on hashtag analysis
- **Category details** — for each trending category: top 6 items + top 6 vendors + related hashtags

**Features:**
- Filters: days back, number of categories, items per category
- "Analyze Trends" button fetches live TikTok data and saves to local cache
- Page loads from cache by default (no external API call)
- View count formatting (B/M/K)

**Endpoints:** `/api/trends/hashtags-cached`, `/api/trends/refresh`, `/api/trends/suggestions`

---

## API Reference

### Feed & Dashboard

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/top-vendors?start_date&end_date` | Top vendors by orders in date range |
| `GET` | `/api/top-items?start_date&end_date` | Top items by quantity in date range |
| `GET` | `/api/feed/nearest-event` | Nearest upcoming or active seasonal event |
| `GET` | `/api/feed/trending-up?days=7&limit=20` | Items with >=20% growth between two periods |
| `POST` | `/api/generate-feed` | AI feed recommendations (sends data context to GPT) |

### Seasonality

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/seasonality/events` | All seasonal events with category mappings |
| `GET` | `/api/seasonality/items?start_date&end_date&categories&subcategories` | Items filtered by vendor category |
| `GET` | `/api/seasonality/vendors?start_date&end_date&categories&subcategories` | Vendors filtered by category |
| `GET` | `/api/seasonality/event/items?start_date&end_date&event_key` | Items matching event's category paths |
| `GET` | `/api/seasonality/event/vendors?start_date&end_date&event_key` | Vendors matching event's category paths |
| `GET` | `/api/seasonality/event/historical-items?event_key` | Past years' best sellers for an event |
| `GET` | `/api/seasonality/top-items-per-path?start_date&end_date&events` | Compute top item per category path |
| `GET` | `/api/seasonality/top-items-cached?events` | Read pre-computed results from local DB |
| `GET` | `/api/seasonality/pipeline-status` | Cache status and last update time |

### TikTok Trends

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/trends/hashtags-cached` | Cached TikTok hashtags from local DB |
| `POST` | `/api/trends/refresh` | Fetch fresh TikTok data and update cache |
| `GET` | `/api/trends/suggestions?days_back&top_categories&items_per_category` | Full trend analysis with vendor/item matches |
| `GET` | `/api/trends/category/<category>` | Vendors and items for a specific category |

---

## Architecture

```
Production MongoDB Atlas (MONGO_URI)
  ├── Orders        — order documents with items array
  ├── Items         — item catalog with category hierarchy
  └── Vendors       — vendor profiles with shoppingCategory

Local MongoDB (LOCAL_MONGO_URI)
  ├── seasonality   — pre-computed top items per event/category path
  └── tiktok-hashtags — cached TikTok trending data
```

### Data Flow

1. **Aggregation pipelines** run against production MongoDB (Orders -> unwind items -> group -> lookup Items/Vendors)
2. **Local cache** stores pre-computed results to avoid repeated heavy queries
3. **CLI script** (`run_seasonality_pipeline.py`) pre-computes seasonality data and writes to local DB
4. **Flask app** reads from both: production for live queries, local for cached results

### Category System

4-level hierarchy used for item classification:

```
shoppingCategory (e.g. "fashion")
  └── shoppingSubcategory (e.g. "casual wear")
       └── itemCategory (e.g. "dress")
            └── itemSubcategory (e.g. "maxi dress")
```

Each seasonal event maps to multiple category paths. The `seasonal_event_category_mapping.py` file defines these mappings for all 14 events.

---

## Key Files

| File | Purpose |
|------|---------|
| `app.py` | Flask app — all routes and API endpoints |
| `seasonal_event_category_mapping.py` | Event-to-category mappings + helper functions |
| `run_seasonality_pipeline.py` | CLI script to pre-compute seasonality cache |
| `templates/base.html` | Shared layout — sidebar, styles, utility JS functions |
| `templates/feed.html` | Today's Feed dashboard |
| `templates/index.html` | Main dashboard (top vendors/items) |
| `templates/seasonality.html` | Seasonality analysis page |
| `templates/trends.html` | TikTok trends page |

---

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `MONGO_URI` | Yes | MongoDB Atlas connection string |
| `LOCAL_MONGO_URI` | No | Local MongoDB for caching (defaults to `mongodb://localhost:27017/`) |
| `OPENAI_API_KEY` | No | OpenAI API key (only needed for AI feed generation) |
| `SECRET_KEY` | No | Flask secret key (defaults to `dev-secret-key`) |
