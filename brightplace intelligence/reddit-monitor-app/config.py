"""Configuration and defaults for the Reddit Monitor app."""
import os
from dotenv import load_dotenv

load_dotenv()

# API Keys
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
APP_PASSWORD = os.getenv("APP_PASSWORD", "brightplace2026")

# Email
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASS = os.getenv("SMTP_PASS", "")
NOTIFY_EMAIL = os.getenv("NOTIFY_EMAIL", "")

# Claude
CLAUDE_MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 250
TEMPERATURE = 0.90

# Reddit OAuth
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID", "")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET", "")

# Scout
POSTS_PER_SUBREDDIT = 15
PROMOTIONAL_RATIO = 0.20  # 20% of answers include a link
RSS_DELAY_SECONDS = 2

# Database
DB_PATH = os.path.join(os.path.dirname(__file__), "reddit_monitor.db")

# Subreddits
DEFAULT_SUBREDDITS = {
    "high": [
        "ApartmentHunting", "renting", "personalfinance",
        "FirstTimeRenter", "Frugal", "apartments"
    ],
    "city": [
        "AskNYC", "askdfw", "Denver", "Charlotte", "Austin", "phoenix",
        "Philadelphia", "nashville", "SanDiego", "houston", "Tampa",
        "Chicago", "Atlanta", "Seattle", "MinneapolisMN", "SaltLakeCity",
        "kansascity", "Columbus", "Knoxville", "raleigh"
    ],
    "topical": [
        "dogs", "RemoteWork", "RealEstate"
    ],
    "warmup": [
        "AskReddit", "NoStupidQuestions", "TooAfraidToAsk",
        "CasualConversation", "Showerthoughts", "LifeProTips",
        "mildlyinteresting", "todayilearned"
    ]
}

# Keywords
POSITIVE_KEYWORDS = [
    r"apartment hunt", r"finding an apartment", r"apartment search",
    r"how to find an apartment", r"apartment tour", r"touring apartment",
    r"what to ask", r"leasing office", r"leasing agent",
    r"move.in cost", r"move.in fee", r"security deposit",
    r"pet friendly", r"pet.friendly", r"pet deposit", r"pet rent",
    r"breed restriction", r"dog friendly", r"cat friendly",
    r"renters insurance", r"renter.s insurance", r"roommate insurance",
    r"sublet", r"subletting", r"sublease",
    r"short.term lease", r"month.to.month",
    r"lease break", r"break my lease", r"early termination",
    r"no credit check", r"bad credit apartment", r"second chance apartment",
    r"first apartment", r"first time renter",
    r"how much rent", r"afford rent", r"rent.to.income",
    r"30. rule", r"40x rule", r"rent budget", r"rent afford",
    r"cheap apartment", r"affordable apartment",
    r"under .1.000", r"under .1.500", r"under .2.000",
    r"one bedroom", r"1 bedroom", r"two bedroom", r"2 bedroom",
    r"studio apartment", r"furnished apartment",
    r"apartment with garage", r"attached garage",
    r"apartment dog park", r"apartment with pool",
    r"in.unit laundry", r"washer dryer",
    r"apartment parking", r"apartment amenities", r"apartment fees",
    r"application fee", r"broker fee", r"no.fee apartment",
    r"rent stabiliz", r"rent control",
    r"apartment scam", r"rental scam",
    r"moving to", r"relocating to", r"where should I live",
    r"neighborhood for", r"cost of living",
    r"apartment near", r"apartments in", r"renting in", r"rent in",
    r"looking for apartment", r"apartment advice",
    r"apartment question", r"apartment recommend",
    r"renters rights", r"tenant rights",
    r"security deposit return", r"utility cost", r"utilities included",
    r"apartment checklist", r"apartment vs", r"renting vs buying",
]

NEGATIVE_KEYWORDS = [
    r"eviction notice", r"eviction process", r"being evicted",
    r"lawsuit", r"suing", r"legal advice", r"legal action",
    r"attorney", r"lawyer", r"mold lawsuit",
    r"bed bug", r"cockroach", r"roach infestation",
    r"harassment", r"retaliation", r"discrimination complaint",
    r"fair housing complaint", r"restraining order",
    r"domestic violence", r"sex offender",
    r"illegal activity", r"drug bust", r"police report",
    r"code violation", r"health department", r"condemn",
]

# Tone Profile
DEFAULT_TONE = """You are a real person on Reddit who has rented in multiple cities. You type fast, you don't proofread, you help people because you've been there.

HARD LENGTH LIMIT: 40-80 words. This is NOT optional. Count your words. If your draft exceeds 80 words, delete sentences until it fits. A great Reddit comment is 2-4 sentences. Never write paragraphs.

FORMAT:
- All lowercase. no capitalization except proper nouns.
- Sentence fragments > full sentences. "deposit = refundable. fee = gone forever." is perfect.
- 1-2 Reddit slang per comment: ngl, tbh, imo, fwiw, ymmv, lowkey, fr, tbf
- ONE specific number or dollar figure
- ONE honest caveat ("but", "downside is", "heads up though")
- End with a short question to OP when natural
- No paragraph breaks. One continuous block of text.
- Do NOT say "brightplace" anywhere

BANNED — instant fail if you use these:
- "Great question!", "Hope this helps!", "Feel free to"
- "navigate", "leverage", "comprehensive", "delve", "streamline"
- Bold text, headers, bullet points, numbered lists
- Customer service empathy ("I understand how frustrating")
- Topic sentences, thesis statements, concluding sentences
- Any answer longer than 80 words
- "Here's the thing:", "A few things:", "Here's how it works:"

LINK RULES:
- If including a link, toss it at the END: "someone broke this down here: [URL]"
- ONE link max. never open with a link.

EXAMPLES (this is the exact length and energy you must match):
- "ngl $1,400 on $50K is tight but doable if no car payments. 30% rule puts you at ~$1,250 but landlords use gross so you'd qualify. budget $150-200 extra for utilities + renters insurance. what city are you looking at?"
- "deposit = refundable (in theory). fee = gone forever. pet rent = monthly on top of both. on a 12mo lease with a dog you're looking at $800-1,400 extra total. get all three numbers in writing before signing."
- "went through this in charlotte last year. toured 8 places and the one thing i wish i'd asked every time was about water pressure. ended up with a shower that was basically a drizzle. also ask about package theft -- lost two amazon orders in 6 months."
"""

# Knowledge Base - brightplace articles
DEFAULT_ARTICLES = [
    {"title": "How to Rent an Apartment", "url": "https://www.brightplace.ai/guides/how-to-rent-an-apartment", "keywords": "how to rent,first apartment,renting process,application"},
    {"title": "Your True Monthly Cost", "url": "https://www.brightplace.ai/guides/your-true-monthly-cost", "keywords": "rent,afford,budget,cost,monthly,true cost"},
    {"title": "Austin Young Professionals", "url": "https://www.brightplace.ai/guides/austin-young-professionals", "keywords": "austin,atx"},
    {"title": "Relocating to Austin", "url": "https://www.brightplace.ai/guides/relocating-to-austin", "keywords": "relocating austin,moving austin"},
    {"title": "Brooklyn Neighborhood Guide", "url": "https://www.brightplace.ai/guides/brooklyn-neighborhood-guide", "keywords": "brooklyn,williamsburg,park slope,bushwick"},
    {"title": "Charlotte Affordable Neighborhoods", "url": "https://www.brightplace.ai/guides/charlotte-affordable-neighborhoods", "keywords": "charlotte,university city,south end,noda"},
    {"title": "Chicago Pet Owners", "url": "https://www.brightplace.ai/guides/chicago-pet-owners", "keywords": "chicago pet,chicago dog"},
    {"title": "Dallas Families", "url": "https://www.brightplace.ai/guides/dallas-families", "keywords": "dallas,dfw,plano,frisco,mckinney"},
    {"title": "Denver City Orientation", "url": "https://www.brightplace.ai/guides/denver-city-orientation", "keywords": "denver,capitol hill,rino"},
    {"title": "Dog-Friendly San Diego", "url": "https://www.brightplace.ai/guides/dog-friendly-neighborhoods-san-diego", "keywords": "san diego dog,sd dog"},
    {"title": "Houston City Orientation", "url": "https://www.brightplace.ai/guides/houston-city-orientation", "keywords": "houston,woodlands,sugar land"},
    {"title": "Kansas City Young Professionals", "url": "https://www.brightplace.ai/guides/kansas-city-young-professionals", "keywords": "kansas city,kc"},
    {"title": "Nashville Corporate Relocation", "url": "https://www.brightplace.ai/guides/nashville-corporate-relocation-neighborhoods", "keywords": "nashville,music city"},
    {"title": "Philadelphia City Orientation", "url": "https://www.brightplace.ai/guides/philadelphia-city-orientation", "keywords": "philadelphia,philly,manayunk"},
    {"title": "Phoenix Renters Orientation", "url": "https://www.brightplace.ai/guides/phoenix-renters-orientation", "keywords": "phoenix,scottsdale,chandler,gilbert,tempe"},
    {"title": "Salt Lake City Orientation", "url": "https://www.brightplace.ai/guides/salt-lake-city-renters-orientation", "keywords": "salt lake,slc,utah"},
    {"title": "Tampa Renters Orientation", "url": "https://www.brightplace.ai/guides/tampa-renters-orientation", "keywords": "tampa,st pete"},
    {"title": "Pet-Friendly Apartments", "url": "https://www.brightplace.ai/resources/pet-friendly-apartments-greenville-sc", "keywords": "pet friendly,pet deposit,pet rent,breed restriction,dog friendly,cat friendly"},
    {"title": "Renters Insurance with Roommates", "url": "https://www.brightplace.ai/resources/renters-insurance-with-roommates", "keywords": "renters insurance,roommate insurance"},
    {"title": "Short-Term Lease Agreement", "url": "https://www.brightplace.ai/resources/short-term-lease-agreement", "keywords": "short term lease,month to month,temporary lease"},
    {"title": "Sublet Apartments NYC", "url": "https://www.brightplace.ai/resources/sublet-apartments-nyc", "keywords": "sublet,sublease,nyc sublet,subletting"},
    {"title": "Apartment Tour Questions", "url": "https://www.brightplace.ai/resources/questions-to-ask-when-touring-an-apartment", "keywords": "tour question,what to ask,apartment tour,touring"},
    {"title": "Apartments with Dog Parks", "url": "https://www.brightplace.ai/resources/apartments-with-dog-parks", "keywords": "dog park,bark park"},
    {"title": "Apartments with Attached Garages", "url": "https://www.brightplace.ai/resources/apartments-with-attached-garages", "keywords": "attached garage,garage apartment,private garage"},
    {"title": "One Bedroom Apartment NYC", "url": "https://www.brightplace.ai/resources/one-bedroom-apartment-nyc", "keywords": "nyc 1 bedroom,nyc one bedroom,1br nyc,manhattan rent,broker fee"},
    {"title": "Renting in Mission Beach SD", "url": "https://www.brightplace.ai/resources/renting-mission-beach-san-diego", "keywords": "mission beach,pacific beach,san diego rent"},
    {"title": "Bloomington-Normal IL", "url": "https://www.brightplace.ai/resources/one-bedroom-apartments-bloomington-normal-il", "keywords": "bloomington,normal il,isu"},
    {"title": "Venice Lofts Philadelphia", "url": "https://www.brightplace.ai/resources/venice-lofts-apartments-philadelphia-pa", "keywords": "venice lofts,apex manayunk"},
    {"title": "Century University City Charlotte", "url": "https://www.brightplace.ai/resources/century-university-city-apartments-charlotte", "keywords": "century university city,unc charlotte"},
    {"title": "Redstone Ranch Denver", "url": "https://www.brightplace.ai/resources/redstone-ranch-denver", "keywords": "redstone ranch,green valley ranch,dia apartments"},
    {"title": "Homes for Rent No Deposit", "url": "https://www.brightplace.ai/resources/homes-for-rent-no-deposit", "keywords": "no deposit,deposit alternative,waive deposit"},
    {"title": "Parkside at Legacy Plano", "url": "https://www.brightplace.ai/resources/parkside-at-legacy-plano", "keywords": "parkside legacy,legacy west,plano apartments"},
]
