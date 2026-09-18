#!/usr/bin/env python3
"""Turn persisted Webflow CMS batch JSON into flat <slug>.html + metadata records."""
import json, os, sys, re

BASE = os.path.dirname(os.path.abspath(__file__))
LOOK = json.load(open(os.path.join(BASE, "extract/reports/lookups.json")))
CATS, AUTHS = LOOK["categories"], LOOK["authors"]

def process(batch_files, outdir, collection, url_prefix):
    os.makedirs(outdir, exist_ok=True)
    records = []
    for bf in batch_files:
        raw = open(bf).read()
        d = json.loads(raw)
        # two wrapper shapes: bare result object, or MCP content-block array
        if isinstance(d, list):
            d = json.loads(d[0]["text"])
        for it in d["result"]["items"]:
            fd = it["fieldData"]
            slug = fd.get("slug")
            if not slug:
                continue
            body = fd.get("post-body") or ""
            # main image can be dict {url,alt,fileId} or None
            mi = fd.get("main-image") or {}
            th = fd.get("thumbnail-image") or {}
            rec = {
                "slug": slug,
                "title": fd.get("name"),
                "url": f"{url_prefix}/{slug}",
                "collection": collection,
                "seo_title": fd.get("seo-title"),
                "meta_description": fd.get("meta-description"),
                "focus_keyword": fd.get("focus-keyword"),
                "summary": fd.get("post-summary"),
                "category": CATS.get(fd.get("category-2") or "", {}).get("slug"),
                "category_name": CATS.get(fd.get("category-2") or "", {}).get("name"),
                "author": AUTHS.get(fd.get("author-2") or "", {}).get("name"),
                "featured": fd.get("featured"),
                "main_image": mi.get("url") if isinstance(mi, dict) else None,
                "main_image_alt": mi.get("alt") if isinstance(mi, dict) else None,
                "thumbnail_image": th.get("url") if isinstance(th, dict) else None,
                "draft": it.get("isDraft"),
                "archived": it.get("isArchived"),
                "created_on": it.get("createdOn"),
                "last_updated": it.get("lastUpdated"),
                "last_published": it.get("lastPublished"),
                "webflow_item_id": it.get("id"),
                "body_chars": len(body),
                "inline_images": sorted(set(re.findall(r'<img[^>]+src="([^"]+)"', body))),
            }
            records.append(rec)
            with open(os.path.join(outdir, f"{slug}.html"), "w") as f:
                f.write(body)
    return records

if __name__ == "__main__":
    outdir = sys.argv[1]; collection = sys.argv[2]; prefix = sys.argv[3]
    recs = process(sys.argv[4:], outdir, collection, prefix)
    meta_path = os.path.join(BASE, "extract/reports", f"{collection}-metadata.json")
    # merge with any existing records from earlier batches
    existing = {}
    if os.path.exists(meta_path):
        existing = {r["slug"]: r for r in json.load(open(meta_path))}
    for r in recs:
        existing[r["slug"]] = r
    out = sorted(existing.values(), key=lambda r: r["slug"])
    json.dump(out, open(meta_path, "w"), indent=2)
    print(f"processed {len(recs)} items this batch; {len(out)} total in {collection}-metadata.json")
    print(f"with main_image: {sum(1 for r in out if r['main_image'])}/{len(out)}")
    print(f"drafts: {sum(1 for r in out if r['draft'])}")
