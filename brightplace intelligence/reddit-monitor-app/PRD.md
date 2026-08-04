# brightplace Reddit Monitor — Product Requirements

## What This Is

A web app that monitors Reddit for renter-relevant posts, drafts expert answers using Claude, and surfaces opportunities for brightplace to engage authentically in Reddit communities.

## Core Features

### 1. Reddit Scout
- Fetches recent posts from 28 target subreddits via RSS
- Filters by 80+ renter-relevant keyword patterns
- Skips legal/dispute posts via negative keyword filter
- Runs on schedule (daily at 6 AM) or manually via dashboard button
- Limits to last 15 posts per subreddit to control API costs

### 2. AI Draft Engine
- Sends each matched post to Claude for answer drafting
- Generates ONE draft per post (with regenerate button)
- Rates each post: RELEVANCE (HIGH/MEDIUM/LOW/SKIP) and LINK_OPPORTUNITY (HIGH/MEDIUM/LOW/NONE)
- Auto-matches the best brightplace article from the knowledge base
- Enforces promotional ratio (default 20% — only 1 in 5 answers includes a link)

### 3. Knowledge Base
- Pre-loaded with all brightplace articles (guides + resources)
- Each article has: title, URL, keywords for matching
- Add/edit/remove articles through the dashboard
- Auto-match algorithm finds the best article for each Reddit post

### 4. Tone Profile
- System prompt defining how answers should sound
- Pre-loaded with brightplace's Reddit voice rules
- Example responses for Claude to match
- Editable through dashboard

### 5. Dashboard
- **Opportunities page:** List of matched Reddit posts with drafts, sorted by relevance
- **Each opportunity shows:** Subreddit, post title, link, relevance rating, link opportunity rating, drafted answer, suggested article link
- **Actions per opportunity:** Copy answer, regenerate, mark as posted, dismiss
- **Run Scout button:** Manually trigger a scan
- **Run History:** See past scout runs with counts

### 6. Trend Detection
- Track keyword frequency across monitored subreddits
- Show trending topics (nouns/terms with increased mentions)
- Help identify content opportunities for new brightplace articles

### 7. Daily Email Digest
- Morning email with top opportunities from overnight scan
- Includes: post count by subreddit, top 5 opportunities with drafts, trending topics

### 8. Settings
- Subreddit list management (add/remove/enable/disable)
- Promotional ratio slider (0-50%)
- Confidence threshold
- Email notification settings
- API key management

## Tech Stack

- **Backend:** Python FastAPI
- **Database:** SQLite (simple, no external DB needed)
- **Frontend:** HTML + Tailwind CSS + Alpine.js (no build step)
- **AI:** Anthropic Claude API (claude-sonnet)
- **RSS:** feedparser library
- **Deploy:** Modal (free tier) or local

## File Structure

```
reddit-monitor-app/
├── app.py              # FastAPI main app + routes
├── database.py         # SQLite models and queries
├── scout.py            # Reddit RSS fetching + filtering
├── drafter.py          # Claude AI drafting engine
├── knowledge.py        # Knowledge base management
├── trends.py           # Trend detection
├── email_digest.py     # Daily email sender
├── config.py           # Settings and defaults
├── seed_data.py        # Pre-load brightplace articles
├── templates/
│   ├── base.html       # Layout template
│   ├── dashboard.html  # Main opportunities view
│   ├── knowledge.html  # Knowledge base management
│   ├── trends.html     # Trend detection view
│   ├── settings.html   # Settings page
│   └── history.html    # Run history
├── static/
│   └── style.css       # Custom styles (minimal, Tailwind handles most)
├── requirements.txt    # Python dependencies
└── README.md           # Setup instructions
```

## Seed Data (pre-loaded)

### Subreddits (28)
Tier 1 (high): ApartmentHunting, renting, personalfinance, FirstTimeRenter, Frugal
Tier 2 (city): AskNYC, askdfw, Denver, Charlotte, Austin, phoenix, Philadelphia, nashville, SanDiego, houston, Tampa, Chicago, Atlanta, Seattle, MinneapolisMN, SaltLakeCity, kansascity, Columbus, Knoxville, raleigh
Tier 3 (topical): dogs, RemoteWork, RealEstate

### Knowledge Base Articles (40+)
All brightplace guides and resources with keyword mappings.

### Tone Profile
brightplace Reddit voice: knowledgeable friend, specific numbers, honest tradeoffs, never promotional, never say "brightplace" in answers.

## Non-Goals
- No auto-posting to Reddit (human always posts manually)
- No Reddit API integration (uses RSS only)
- No user authentication system (single-user tool, password-protected)
- No mobile app
