# Module 1: Keyword Research & Gap Analysis

**Priority:** MVP — ships first
**Depends on:** Project setup (domain + competitors stored)
**Feeds into:** Module 2 (Research Engine) → Module 3 (Writing Pipeline)

---

## What This Module Does

Takes a user's domain and competitor domains, finds keyword gaps (keywords competitors rank for that you don't), filters by opportunity (volume, KD, intent), and lets the user select keywords to write about.

---

## User Flow

```
Step 1: Enter your domain
         ↓
Step 2: System auto-detects competitors OR user adds manually
         ↓
Step 3: System pulls keyword gap data
         ↓
Step 4: User sees keyword table (filterable, sortable)
         ↓
Step 5: User clicks [Long-tail] on a keyword → expands related terms
         ↓
Step 6: User clicks [Select] → keyword moves to "Selected Keywords" queue
         ↓
Step 7: User clicks [Research & Write] → goes to Module 2
```

---

## Screen 1: Project Setup

First time user enters the app after signup:

```
┌─────────────────────────────────────────────────┐
│  SET UP YOUR PROJECT                             │
│                                                  │
│  Your website URL:                               │
│  ┌─────────────────────────────────────────┐    │
│  │ https://www.brightplace.ai              │    │
│  └─────────────────────────────────────────┘    │
│                                                  │
│  Your niche/industry:                            │
│  ┌─────────────────────────────────────────┐    │
│  │ Apartment rentals & renter education    │    │
│  └─────────────────────────────────────────┘    │
│                                                  │
│  Competitor URLs (optional — we can auto-detect): │
│  ┌─────────────────────────────────────────┐    │
│  │ https://www.apartmentguide.com          │    │
│  │ https://www.rentcafe.com                │    │
│  │ + Add another competitor                │    │
│  └─────────────────────────────────────────┘    │
│                                                  │
│  [Auto-Detect Competitors]  [Continue →]         │
└─────────────────────────────────────────────────┘
```

**Behind the scenes when user clicks "Continue":**
1. Crawl user's domain → extract indexed pages, existing keywords
2. If auto-detect: call DataForSEO competitors endpoint → find top 5 organic competitors
3. Store project config in database

---

## Screen 2: Keyword Gap Dashboard

```
┌─────────────────────────────────────────────────────────────────┐
│  KEYWORD OPPORTUNITIES                                          │
│                                                                  │
│  Your domain: brightplace.ai (12 indexed pages)                 │
│  vs. apartmentguide.com (8,400 pages) + rentcafe.com (6,100)   │
│                                                                  │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐            │
│  │   2,847      │ │     412      │ │      67      │            │
│  │ Total gaps   │ │  Winnable    │ │  Quick wins  │            │
│  │              │ │  (KD < 30)   │ │ (KD<15,V>500)│            │
│  └──────────────┘ └──────────────┘ └──────────────┘            │
│                                                                  │
│  Filters: [Intent ▼] [KD range ▼] [Volume range ▼] [Search]   │
│                                                                  │
│  ┌─────────────────────┬───────┬────┬──────────┬──────────────┐│
│  │ Keyword             │  Vol  │ KD │ Intent   │ Actions      ││
│  ├─────────────────────┼───────┼────┼──────────┼──────────────┤│
│  │ what does income     │ 2,400 │ 11 │ Info     │ [Long-tail]  ││
│  │ restricted mean      │       │    │          │ [Select]     ││
│  ├─────────────────────┼───────┼────┼──────────┼──────────────┤│
│  │ eviction friendly    │ 5,400 │ 19 │ Info     │ [Long-tail]  ││
│  │ apartments           │       │    │          │ [Select]     ││
│  ├─────────────────────┼───────┼────┼──────────┼──────────────┤│
│  │ furnished apartments │ 6,600 │ 17 │ Transact │ [Long-tail]  ││
│  │ near me              │       │    │          │ [Select]     ││
│  ├─────────────────────┼───────┼────┼──────────┼──────────────┤│
│  │ how to break a lease │ 4,800 │ 28 │ Info     │ [Long-tail]  ││
│  │                      │       │    │          │ [Select]     ││
│  └─────────────────────┴───────┴────┴──────────┴──────────────┘│
│                                                                  │
│  Showing 1-20 of 412 winnable keywords    [← Prev] [Next →]    │
└─────────────────────────────────────────────────────────────────┘
```

---

## Screen 3: Long-tail Expansion (inline)

When user clicks [Long-tail] on a keyword, it expands inline:

```
│ what does income      │ 2,400 │ 11 │ Info     │ [Collapse]   │
│ restricted mean       │       │    │          │ [Select All] │
│  ├─ income restricted │   880 │  8 │ Info     │ [Select]     │
│  │  apartments        │       │    │          │              │
│  ├─ income restricted │   720 │ 14 │ Info     │ [Select]     │
│  │  vs income based   │       │    │          │              │
│  ├─ what does 60% AMI │   590 │  6 │ Info     │ [Select]     │
│  │  mean              │       │    │          │              │
│  ├─ income restricted │   480 │ 12 │ Info     │ [Select]     │
│  │  qualifications    │       │    │          │              │
│  └─ what happens if   │   320 │  9 │ Info     │ [Select]     │
│     income increases  │       │    │          │              │
```

---

## Screen 4: Selected Keywords Sidebar

Right side of the screen shows selected keywords:

```
┌──────────────────────────┐
│  SELECTED (3)            │
│                          │
│  ✓ what does income      │
│    restricted mean       │
│    + 3 long-tail         │
│    [Remove]              │
│                          │
│  ✓ eviction friendly     │
│    apartments            │
│    [Remove]              │
│                          │
│  ✓ furnished apartments  │
│    near me               │
│    + 2 long-tail         │
│    [Remove]              │
│                          │
│  [Research & Write →]    │
│  [Save for Later]        │
└──────────────────────────┘
```

---

## API Endpoints (Backend)

```
POST   /api/projects
       → Create new project (domain, niche, competitors)
       → Triggers initial crawl + competitor detection

GET    /api/projects/{id}/competitors
       → Returns auto-detected or manually added competitors

POST   /api/projects/{id}/competitors
       → Add a competitor manually

GET    /api/projects/{id}/keyword-gaps
       → Returns keyword gap data (paginated, filterable)
       → Query params: ?kd_max=30&vol_min=500&intent=informational&page=1

GET    /api/projects/{id}/keywords/{keyword}/long-tail
       → Returns long-tail variants for a keyword

POST   /api/projects/{id}/selected-keywords
       → Save selected keywords to project queue

GET    /api/projects/{id}/selected-keywords
       → List all selected keywords in queue
```

---

## DataForSEO API Calls

### Auto-detect competitors
```python
# DataForSEO Labs → Competitors Domain
POST https://api.dataforseo.com/v3/dataforseo_labs/google/competitors_domain/live

{
    "target": "brightplace.ai",
    "location_code": 2840,  # United States
    "language_code": "en",
    "limit": 10
}
```

### Keyword gap analysis
```python
# DataForSEO Labs → Domain Intersection
POST https://api.dataforseo.com/v3/dataforseo_labs/google/domain_intersection/live

{
    "targets": {
        "1": "apartmentguide.com",
        "2": "rentcafe.com"
    },
    "exclude_targets": ["brightplace.ai"],
    "location_code": 2840,
    "language_code": "en",
    "limit": 100,
    "offset": 0,
    "filters": [
        ["keyword_data.keyword_info.search_volume", ">", 500],
        ["keyword_data.keyword_info.keyword_difficulty", "<", 30]
    ],
    "order_by": ["keyword_data.keyword_info.search_volume,desc"]
}
```

### Long-tail keyword suggestions
```python
# DataForSEO Labs → Keyword Suggestions
POST https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live

{
    "keyword": "what does income restricted mean",
    "location_code": 2840,
    "language_code": "en",
    "limit": 20,
    "filters": [
        ["keyword_info.search_volume", ">", 100],
        ["keyword_info.keyword_difficulty", "<", 30]
    ]
}
```

### Get search volume + KD for selected keywords
```python
# Keywords Data → Search Volume
POST https://api.dataforseo.com/v3/keywords_data/google_ads/search_volume/live

{
    "keywords": [
        "what does income restricted mean",
        "income restricted apartments",
        "income restricted vs income based"
    ],
    "location_code": 2840,
    "language_code": "en"
}
```

---

## Database Tables for This Module

```sql
-- Projects
CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    team_id UUID REFERENCES teams(id),
    domain TEXT NOT NULL,
    niche TEXT,
    brand_context JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Competitors
CREATE TABLE competitors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    domain TEXT NOT NULL,
    dr_score INTEGER,
    indexed_pages INTEGER,
    auto_detected BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Keyword Gaps (cached, refreshed weekly)
CREATE TABLE keyword_gaps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    keyword TEXT NOT NULL,
    volume INTEGER,
    kd INTEGER,
    intent TEXT,
    competitor_domains TEXT[],
    long_tail_keywords JSONB,
    fetched_at TIMESTAMPTZ DEFAULT NOW()
);

-- Selected Keywords (user's queue)
CREATE TABLE selected_keywords (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES projects(id),
    keyword TEXT NOT NULL,
    volume INTEGER,
    kd INTEGER,
    intent TEXT,
    long_tail_keywords JSONB,
    status TEXT DEFAULT 'queued',  -- queued, researching, briefed, writing, published
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## Acceptance Criteria

- [ ] User can enter domain and see auto-detected competitors
- [ ] User can add/remove competitors manually
- [ ] Keyword gap table loads with correct data (volume, KD, intent)
- [ ] Filters work (KD range, volume range, intent type)
- [ ] Sorting works (by volume, KD, intent)
- [ ] Pagination works (20 per page)
- [ ] Long-tail expansion shows related keywords inline
- [ ] User can select keywords and see them in sidebar
- [ ] "Research & Write" button passes selected keywords to Module 2
- [ ] Data caches for 7 days (avoids redundant API calls)
- [ ] Loading states show during API calls
- [ ] Error handling for DataForSEO failures
