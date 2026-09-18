#!/usr/bin/env python3
"""Build listing pages for each collection, in the AIR Stage-10 visual language.

Mirrors the live Webflow listing cards (image, category, date, title) and adds
the summary. Live items only; drafts are excluded and reported in a comment.
"""
import json, os, re, html
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
CSS  = open(os.path.join(BASE, "air-template.css.html")).read().strip()
SITE = "https://www.brightplace.ai"
ORG  = {"@type": "Organization", "name": "brightplace", "url": SITE}

META = {
 "guides":    ("Renter Guides",
               "City orientations, neighborhood breakdowns by renter cohort, student housing, and the financial side of renting."),
 "resources": ("Renter Resources",
               "Practical answers on applications, credit, deposits, leases, pet policies, and what renting actually costs."),
 "news":      ("News",
               "Product launches, press coverage, and what we are learning building an AI-native rental platform."),
}

LIST_CSS = """
    <style>
        body { max-width: 1120px; }
        .listing-header { margin-bottom: 48px; padding-bottom: 24px; border-bottom: 1px solid #e5e7eb; }
        .listing-header p { color: #4b5563; font-size: 1.0625rem; max-width: 60ch; }
        .listing-count { color: #6b7280; font-size: 0.875rem; margin-top: 12px; }
        .card-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 32px 28px;
            list-style: none;
        }
        .card { display: flex; flex-direction: column; }
        .card-image-link { display: block; border-radius: 10px; overflow: hidden; background: #f3f4f6; aspect-ratio: 16 / 9; }
        .card-image { width: 100%; height: 100%; object-fit: cover; display: block; }
        .card-image-placeholder {
            width: 100%; height: 100%; display: flex; align-items: center; justify-content: center;
            color: #9ca3af; font-size: 0.8125rem; letter-spacing: .02em;
        }
        .card-meta { display: flex; align-items: center; gap: 10px; margin: 16px 0 8px; font-size: 0.8125rem; color: #6b7280; }
        .card-category {
            background: #eef2ff; color: #4338ca; padding: 3px 10px; border-radius: 999px;
            font-weight: 600; font-size: 0.75rem; letter-spacing: .01em;
        }
        .card h2 { font-size: 1.125rem; line-height: 1.4; margin: 0 0 8px; }
        .card h2 a { color: #111827; text-decoration: none; }
        .card h2 a:hover { text-decoration: underline; }
        .card p { font-size: 0.9375rem; color: #4b5563; line-height: 1.6; margin: 0; }
        @media (max-width: 600px) {
            body { padding: 32px 16px; }
            .card-grid { grid-template-columns: 1fr; gap: 28px; }
        }
    </style>"""

def esc(s): return html.escape(s or "", quote=True)

def pretty(iso):
    if not iso: return ""
    try: return datetime.fromisoformat(iso.replace("Z","+00:00")).strftime("%B %-d, %Y")
    except Exception: return iso[:10]

def card(r, collection):
    img = r.get("main_image")
    slug = r["slug"]
    ext = None
    for e in ("jpg","jpeg","png","webp"):
        if os.path.exists(os.path.join(BASE,"extract",collection,f"{slug}.{e}")): ext=e; break
    thumb = (f'<img class="card-image" src="{slug}.{ext}" alt="{esc(r.get("main_image_alt") or r.get("title"))}" loading="lazy">'
             if ext else '<div class="card-image-placeholder">No featured image</div>')
    cat = r.get("category_name")
    cat_html = f'<span class="card-category">{esc(cat)}</span>' if cat else ""
    return f"""            <li class="card">
                <a class="card-image-link" href="{esc(r['url'])}">{thumb}</a>
                <div class="card-meta">{cat_html}<time datetime="{(r.get('created_on') or '')[:10]}">{pretty(r.get('created_on'))}</time></div>
                <h2><a href="{esc(r['url'])}">{esc(r.get('title'))}</a></h2>
                <p>{esc(r.get('summary'))}</p>
            </li>"""

def build(collection, live_slugs):
    recs = json.load(open(os.path.join(BASE,"extract/reports",f"{collection}-metadata.json")))
    live = sorted([r for r in recs if r["slug"] in live_slugs],
                  key=lambda r: r.get("created_on") or "", reverse=True)
    skipped = [r["slug"] for r in recs if r["slug"] not in live_slugs]
    name, desc = META[collection]
    url = f"{SITE}/{collection}"

    items_ld = {"@context":"https://schema.org","@type":"CollectionPage","@id":url,"url":url,
        "name":name,"description":desc,"isPartOf":ORG,
        "mainEntity":{"@type":"ItemList","numberOfItems":len(live),
            "itemListElement":[{"@type":"ListItem","position":i,"url":r["url"],"name":r.get("title")}
                               for i,r in enumerate(live,1)]}}
    crumb_ld = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE},
        {"@type":"ListItem","position":2,"name":name,"item":url}]}
    blocks = "\n".join(f'    <script type="application/ld+json">\n{json.dumps(b, indent=2)}\n    </script>'
                       for b in (items_ld, crumb_ld))
    cards = "\n".join(card(r, collection) for r in live)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>{esc(name)} | brightplace</title>

    <meta name="description" content="{esc(desc)}">
    <meta name="robots" content="index, follow, max-image-preview:large">
    <link rel="canonical" href="{url}">
    <link rel="alternate" hreflang="en-US" href="{url}">

    <meta property="og:type" content="website">
    <meta property="og:site_name" content="brightplace">
    <meta property="og:title" content="{esc(name)} | brightplace">
    <meta property="og:description" content="{esc(desc)}">
    <meta property="og:url" content="{url}">
    <meta property="og:locale" content="en_US">

    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{esc(name)} | brightplace">
    <meta name="twitter:description" content="{esc(desc)}">

    <!-- JSON-LD Structured Data -->
{blocks}

    {CSS}
{LIST_CSS}
</head>
<body>
    <!-- Listing template for {SITE}/{collection} · extracted 2026-09-17 -->
    <!-- Live items: {len(live)}. Excluded (draft/404): {', '.join(skipped) if skipped else 'none'} -->
    <header class="listing-header">
        <h1>{esc(name)}</h1>
        <p>{esc(desc)}</p>
        <div class="listing-count">{len(live)} articles</div>
    </header>

    <main>
        <ul class="card-grid">
{cards}
        </ul>
    </main>
</body>
</html>
"""

if __name__ == "__main__":
    for coll, slugfile in (("guides","live-guide-slugs.txt"),
                           ("resources","live-resource-slugs.txt"),
                           ("news","live-news-slugs.txt")):
        live = set(open(os.path.join(BASE,"extract/reports",slugfile)).read().split())
        out = os.path.join(BASE,"extract",coll,"_listing.page.html")
        open(out,"w").write(build(coll, live))
        print(f"{coll:10s} listing written ({len(live)} live items)")
