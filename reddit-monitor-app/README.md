# brightplace Reddit Monitor

An internal tool that monitors 29 Reddit subreddits for renter-relevant posts, drafts expert answers using Claude AI, and surfaces engagement opportunities for the brightplace team.

---

## How It Works

The system has two parts that work together:

```
Your Machine                           Modal (Cloud)
-----------                            -------------

fetcher.py                  --->       Web Dashboard
  - Reads Reddit RSS feeds             - Receives posts via webhook
  - Runs every 4 hours                 - Filters by 80+ keywords
  - Sends posts to Modal               - Drafts answers with Claude AI
                                       - Matches brightplace articles
                                       - Shows opportunities to review
```

**Why two parts?** Reddit blocks cloud server IPs from accessing their feeds. The fetcher runs on your machine (which Reddit allows) and pushes posts to the dashboard hosted on Modal.

---

## Access the Dashboard

**Live URL:** https://haroonashfaq0121--brightplace-reddit-monitor-web.modal.run

No login required. Bookmark this URL. Works on desktop and mobile.

### Dashboard Pages

| Page | URL Path | What It Does |
|------|----------|-------------|
| Dashboard | `/` | View all opportunities with AI-drafted answers |
| Knowledge Base | `/knowledge` | Manage brightplace articles used for link matching |
| Trends | `/trends` | See trending renter topics across subreddits |
| History | `/history` | View all past scout runs and their results |
| Settings | `/settings` | Manage subreddits, tone profile, promotional ratio |

---

## Setup (One-Time)

### Prerequisites
- Python 3.9+
- Terminal access on your machine

### Steps

```bash
# 1. Navigate to the app folder
cd "brightplace intelligence/reddit-monitor-app"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Verify it works (single run)
python fetcher.py
```

You should see output like:
```
============================================================
Scout run started at 2026-07-22 14:30:00
============================================================
  [1/28] r/apartments: 25 posts
  [2/28] r/renting: 25 posts
  ...
  Batch 1: 5 matched, 3 opportunities
Done in 240s - 8 matched, 5 new opportunities
Dashboard: https://haroonashfaq0121--brightplace-reddit-monitor-web.modal.run
```

---

## Running the Fetcher

### One-time scan
```bash
python fetcher.py
```
Scans all 29 subreddits once. Takes about 4-5 minutes.

### Continuous monitoring (recommended)
```bash
python fetcher.py --loop 4h
```
Runs a scan every 4 hours automatically. Keep the terminal window open or run in background.

### Run in background (Mac/Linux)
```bash
nohup python fetcher.py --loop 4h > fetcher.log 2>&1 &
```
This keeps running even if you close the terminal. Check `fetcher.log` for output.

### Other interval options
```bash
python fetcher.py --loop 30m    # Every 30 minutes
python fetcher.py --loop 1h     # Every hour
python fetcher.py --loop 6h     # Every 6 hours
```

### Stop the fetcher
Press `Ctrl+C` in the terminal, or if running in background:
```bash
pkill -f "fetcher.py"
```

---

## Using the Dashboard

### Reviewing Opportunities

Each opportunity card shows:
- **Relevance badge** (HIGH / MEDIUM / LOW) -- how relevant the post is to brightplace
- **Subreddit** -- where the post was found
- **Promotional tag** -- if this answer includes a brightplace link (20% of answers)
- **Post title and preview** -- click to open the original Reddit post
- **Drafted answer** -- AI-generated response ready to paste

### Actions on Each Opportunity

| Button | What It Does |
|--------|-------------|
| **Copy Answer** | Copies the drafted answer to your clipboard |
| **Regenerate** | Gets a fresh AI-drafted answer for the same post |
| **Mark Posted** | Marks as posted after you paste it on Reddit |
| **Dismiss** | Skips this opportunity |
| **Open on Reddit** | Opens the original post in a new tab |

### Posting Workflow

1. Open the dashboard
2. Review pending opportunities (yellow "Pending Review" count)
3. Click "Open on Reddit" to read the full post and comments
4. If the opportunity looks good, click "Copy Answer"
5. Paste the answer as a comment on Reddit
6. Come back and click "Mark Posted"
7. If the post isn't a good fit, click "Dismiss"

---

## What It Monitors

### 29 Subreddits (3 Tiers)

**High Priority** -- renter-focused communities
- r/apartments, r/renting, r/personalfinance, r/FirstTimeRenter, r/Frugal, r/ApartmentHunting

**City Subreddits** -- local community subs where people ask about apartments
- r/AskNYC, r/askdfw, r/Denver, r/Charlotte, r/Austin, r/phoenix, r/Philadelphia, r/nashville, r/SanDiego, r/houston, r/Tampa, r/Chicago, r/Atlanta, r/Seattle, r/MinneapolisMN, r/SaltLakeCity, r/kansascity, r/Columbus, r/Knoxville, r/raleigh

**Topical** -- related lifestyle subs
- r/dogs, r/RemoteWork, r/RealEstate

You can add or remove subreddits from the Settings page.

### 80+ Keyword Filters

Posts must match at least one positive keyword to be included. Examples:
- Apartment search: "apartment hunt", "finding an apartment", "apartment tour"
- Costs: "security deposit", "move-in cost", "application fee", "pet deposit"
- Affordability: "how much rent", "30% rule", "afford rent", "rent budget"
- Pet-related: "pet friendly", "breed restriction", "dog friendly"
- Insurance: "renters insurance", "roommate insurance"
- Relocation: "moving to", "relocating to", "cost of living"

Posts matching negative keywords (eviction, lawsuits, harassment, etc.) are automatically excluded.

### Knowledge Base (31 Articles)

The system auto-matches Reddit posts to brightplace articles. When a match is found and the promotional ratio triggers (20% of answers), the drafted answer includes a natural link to the relevant article.

Articles include city guides, renter resources, and topical content. Manage them on the Knowledge Base page.

---

## AI Answer Rules

The AI follows these rules for every drafted answer:
- **100-200 words maximum** -- concise and scannable
- **Opens with a direct answer** -- no filler or preamble
- **Includes specific numbers** -- dollar figures, percentages, timelines
- **Sounds like a real Reddit user** -- not a brand or company
- **Never says "brightplace"** -- the brand name never appears in answers
- **Links placed at the end** -- casual framing like "There's a solid breakdown here: [URL]"
- **Maximum one link per answer** -- and only in 20% of answers
- **Honest about tradeoffs** -- no marketing language

### Promotional Ratio

Only 20% of answers include a brightplace link. This keeps the engagement authentic and avoids looking spammy. You can adjust this ratio in Settings.

---

## Important Rules

- **You always post manually.** The app drafts answers. You decide what to post.
- **Never auto-post.** Reddit bans automated posting. Always copy-paste manually.
- **20% link rate.** Only 1 in 5 answers should include a brightplace link.
- **Read the post first.** Always open the Reddit post and read the full context before posting.
- **Check existing comments.** If someone already gave a similar answer, skip it.
- **Be genuine.** If the drafted answer doesn't fit the conversation, dismiss it or regenerate.

---

## Troubleshooting

### Fetcher shows "Rate limited, waiting..."
Reddit limits RSS requests. The fetcher handles this automatically by waiting and retrying. If you see many rate limits, increase the delay by running fewer scans (e.g., `--loop 6h` instead of `--loop 4h`).

### Dashboard shows 0 opportunities after a run
This means no posts matched the keyword filters, which is normal for some scans. City subreddits like r/Knoxville or r/kansascity have fewer apartment-related posts than r/apartments or r/renting.

### Fetcher can't connect to the webhook
Check that the Modal app is running. Visit the dashboard URL in your browser. If it's down, redeploy:
```bash
cd "brightplace intelligence/reddit-monitor-app"
python -m modal deploy modal_app.py
```

### Need to reset the database
The database is stored on Modal's persistent volume. To start fresh, delete the volume and redeploy:
```bash
python -m modal volume delete reddit-monitor-db
python -m modal deploy modal_app.py
```

---

## File Reference

| File | Purpose |
|------|---------|
| `fetcher.py` | Local RSS fetcher -- run this on your machine |
| `app.py` | FastAPI web app (dashboard, webhook, all routes) |
| `scout.py` | Reddit RSS parsing, keyword matching, post filtering |
| `drafter.py` | Claude AI integration for drafting answers |
| `database.py` | SQLite models and queries |
| `config.py` | All configuration: subreddits, keywords, tone, articles |
| `modal_app.py` | Modal deployment configuration |
| `templates/` | HTML templates for all dashboard pages |
| `.env` | Local environment variables (API keys) |

---

## Tech Stack

- **Dashboard:** FastAPI + Jinja2 + Tailwind CSS
- **AI:** Claude Sonnet 4.6 via Anthropic API
- **Database:** SQLite with WAL mode (persistent on Modal volume)
- **Hosting:** Modal (serverless, always-on)
- **RSS Parsing:** feedparser + requests
- **Data Flow:** Local fetcher --> webhook --> Modal app --> Claude --> Dashboard
