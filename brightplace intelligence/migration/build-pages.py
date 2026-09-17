#!/usr/bin/env python3
"""Wrap each extracted Webflow body in the AIR operator Stage-10 page template.

Produces a self-contained <slug>.page.html per item: full SEO head, Open Graph,
Twitter card, server-rendered JSON-LD, inline styles, schema.org microdata.
"""
import json, os, re, html, sys, glob
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
CSS  = open(os.path.join(BASE, "air-template.css.html")).read().strip()
SITE = "https://www.brightplace.ai"
ORG  = {"@type": "Organization", "name": "brightplace",
        "url": SITE, "logo": f"{SITE}/favicon.png"}

def esc(s):
    return html.escape(s, quote=True) if s else ""

def sanitise(body: str) -> str:
    """Webflow embed blocks carry full mini-documents. Strip the document-level
    tags (which are invalid mid-page) but KEEP their contents, including <style>."""
    for tag in ("html", "head", "body"):
        body = re.sub(rf'</?{tag}[^>]*>', '', body, flags=re.I)
    body = re.sub(r'<!DOCTYPE[^>]*>', '', body, flags=re.I)
    # <title>/<meta>/<link> are head-only and invalid inside <body>; the Webflow
    # embeds carry their own. Drop them, keep everything else including <style>.
    body = re.sub(r'<title[^>]*>.*?</title>', '', body, flags=re.I | re.S)
    body = re.sub(r'<meta[^>]*>', '', body, flags=re.I)
    body = re.sub(r'<link[^>]*>', '', body, flags=re.I)
    return body

def pretty_date(iso):
    if not iso: return ""
    try: return datetime.fromisoformat(iso.replace("Z", "+00:00")).strftime("%B %-d, %Y")
    except Exception: return iso[:10]

def build(rec, body, collection):
    slug  = rec["slug"]
    url   = rec["url"]
    title = rec.get("seo_title") or rec.get("title") or slug
    desc  = rec.get("meta_description") or rec.get("summary") or ""
    img   = rec.get("main_image") or ""
    author= rec.get("author") or "brightplace"
    pub   = (rec.get("created_on") or "")[:10]
    mod   = (rec.get("last_updated") or rec.get("created_on") or "")[:10]
    kw    = rec.get("focus_keyword") or ""
    crumb = collection.capitalize()

    article_ld = {"@context":"https://schema.org","@type":"Article",
        "headline": rec.get("title"), "description": desc,
        "author": {"@type":"Person","name":author},
        "publisher": ORG, "datePublished": pub, "dateModified": mod,
        "mainEntityOfPage": {"@type":"WebPage","@id": url}}
    if img: article_ld["image"] = img

    breadcrumb_ld = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[
        {"@type":"ListItem","position":1,"name":"Home","item":SITE},
        {"@type":"ListItem","position":2,"name":crumb,"item":f"{SITE}/{collection}"},
        {"@type":"ListItem","position":3,"name":rec.get("title"),"item":url}]}

    webpage_ld = {"@context":"https://schema.org","@type":"WebPage","@id":url,
        "url":url,"name":title,"description":desc,"isPartOf":ORG,
        "speakable":{"@type":"SpeakableSpecification",
                     "cssSelector":[".article-intro","h1"]}}

    blocks = "\n".join(
        f'    <script type="application/ld+json">\n{json.dumps(b, indent=2)}\n    </script>'
        for b in (article_ld, breadcrumb_ld, webpage_ld))

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <!-- SEO Title (distinct from H1) -->
    <title>{esc(title)}</title>

    <!-- Core SEO Meta -->
    <meta name="description" content="{esc(desc)}">
    <meta name="keywords" content="{esc(kw)}">
    <meta name="author" content="{esc(author)}">
    <meta name="robots" content="index, follow, max-snippet:-1, max-image-preview:large, max-video-preview:-1">
    <link rel="canonical" href="{esc(url)}">
    <link rel="alternate" hreflang="en-US" href="{esc(url)}">

    <!-- Open Graph -->
    <meta property="og:type" content="article">
    <meta property="og:site_name" content="brightplace">
    <meta property="og:title" content="{esc(title)}">
    <meta property="og:description" content="{esc(desc)}">
    <meta property="og:url" content="{esc(url)}">
    <meta property="og:image" content="{esc(img)}">
    <meta property="og:locale" content="en_US">
    <meta property="article:published_time" content="{pub}">
    <meta property="article:modified_time" content="{mod}">
    <meta property="article:author" content="{esc(author)}">

    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{esc(title)}">
    <meta name="twitter:description" content="{esc(desc)}">
    <meta name="twitter:image" content="{esc(img)}">

    <!-- JSON-LD Structured Data -->
{blocks}

    {CSS}
</head>
<body>
    <!-- Source: Webflow CMS item {rec.get('webflow_item_id')} · extracted 2026-09-17 -->
    <article itemscope itemtype="https://schema.org/Article">
        <header>
            <div class="article-meta">
                <span>By <span itemprop="author">{esc(author)}</span></span>
                &middot;
                <time datetime="{pub}" itemprop="datePublished">{pretty_date(rec.get('created_on'))}</time>
            </div>
            <h1 itemprop="headline">{esc(rec.get('title'))}</h1>
        </header>

        <div itemprop="articleBody">
{sanitise(body)}
        </div>

        <footer class="article-footer">
            <p>Last reviewed: {pretty_date(rec.get('last_updated'))}</p>
            <meta itemprop="dateModified" content="{mod}">
        </footer>
    </article>
</body>
</html>
"""

if __name__ == "__main__":
    total = 0
    for collection in ("guides", "resources", "news"):
        d = os.path.join(BASE, "extract", collection)
        recs = {r["slug"]: r for r in json.load(
            open(os.path.join(BASE, "extract/reports", f"{collection}-metadata.json")))}
        n = 0
        for slug, rec in recs.items():
            src = os.path.join(d, f"{slug}.html")
            if not os.path.exists(src): continue
            page = build(rec, open(src).read(), collection)
            open(os.path.join(d, f"{slug}.page.html"), "w").write(page)
            n += 1
        print(f"{collection:10s} {n:3d} page.html written")
        total += n
    print(f"total: {total}")
