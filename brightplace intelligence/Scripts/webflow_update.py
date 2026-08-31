#!/usr/bin/env python3
"""
Script to update Webflow CMS items via the Webflow API.
Reads HTML files and updates the post-body field for each item.
"""
import os
import json
import requests
import sys
import time

# Webflow API configuration
SITE_ID = "69d6907887b739e09622100f"
COLLECTION_ID = "69fcfcef26d35b66ba874f9d"

# Get API token from environment
API_TOKEN = os.environ.get("WEBFLOW_API_TOKEN")
if not API_TOKEN:
    print("ERROR: WEBFLOW_API_TOKEN environment variable not set")
    print("Set it with: export WEBFLOW_API_TOKEN='your-token-here'")
    sys.exit(1)

BASE_URL = "https://api.webflow.com/v2"
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json",
    "accept": "application/json"
}

HTML_DIR = "/Users/matiullahkhan/Desktop/brightplace/brightplace intelligence/Webflow CMS Data"

# Item ID to slug mapping
ITEMS = {
    "6a54c2b9d898441bf7cd8c5d": "rent-affordability-18-an-hour",
    "6a5e186b054610c32642f67f": "one-bedroom-apartment-nyc",
    "6a27147d93c67b54880685f1": "sublet-apartments-nyc",
    "6a0ed978b3d8eb020c335aac": "homes-for-rent-no-deposit",
    "6a54bcb49bdfc24c3e617a12": "apartments-near-university-of-texas-san-antonio",
    "6a2bd71d2368135db7b42848": "apartments-with-dog-parks",
    "6a4637d513cc8f1ee8fc47ad": "move-in-specials-apartments",
    "6a4cea50e06c2c679d94112b": "prorated-rent",
    "6a5e1c5e51ee9110b659b832": "questions-to-ask-when-touring-an-apartment",
    "6a5e1e4030e30e0a4f550747": "redstone-ranch-denver",
    "6a3121e2cb5926fc57d37eb3": "renters-insurance-with-roommates",
    "6a0ad7173a34ea6ec6614e34": "restaurants-for-lease-near-me",
    "6a0eda23e083ed0bdd682182": "rooms-for-rent-huntsville-al",
    "69fd146ffd5a74740356f7af": "parkside-at-legacy-plano",
    "6a305d08b38618f0a9ef5283": "venice-lofts-apartments-philadelphia-pa",
    "6a8c1b81476b166c5ab3614d": "brooklyn-neighborhoods",
    "6a0ad6d3bebf586226adaf3f": "pet-friendly-apartments-greenville-sc",
    "6a0ad6d3a34f95d83248080a": "pet-friendly-vacation-rentals-st-augustine-fl",
    "69fd14b5532875401949a8ac": "2nd-chance-apartments-houston",
    "6a284826c1f756079d775310": "apartments-with-attached-garages",
    "69fd13b4712edf6b02f3ac0f": "4-bedroom-apartments-orlando",
    "6a68f284a0021ef41ca28f39": "income-based-homes-charlotte-nc",
}

def update_item(item_id, slug):
    """Update a single CMS item's post-body field."""
    html_path = os.path.join(HTML_DIR, f"{slug}.html")

    if not os.path.exists(html_path):
        print(f"  SKIP: HTML file not found: {html_path}")
        return False

    with open(html_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    url = f"{BASE_URL}/collections/{COLLECTION_ID}/items"
    payload = {
        "items": [
            {
                "id": item_id,
                "fieldData": {
                    "post-body": html_content
                }
            }
        ]
    }

    response = requests.patch(url, headers=HEADERS, json=payload)

    if response.status_code == 200:
        print(f"  OK: {slug} (ID: {item_id})")
        return True
    else:
        print(f"  ERROR: {slug} - Status {response.status_code}: {response.text[:200]}")
        return False

def publish_items(item_ids):
    """Publish all items in one batch."""
    url = f"{BASE_URL}/collections/{COLLECTION_ID}/items/publish"
    payload = {
        "itemIds": item_ids
    }

    response = requests.post(url, headers=HEADERS, json=payload)

    if response.status_code in (200, 202):
        print(f"  PUBLISH OK: {len(item_ids)} items published")
        return True
    else:
        print(f"  PUBLISH ERROR: Status {response.status_code}: {response.text[:300]}")
        return False

def main():
    print(f"Updating {len(ITEMS)} items...")
    print()

    success_count = 0
    failed_items = []

    for item_id, slug in ITEMS.items():
        print(f"Updating: {slug}")
        if update_item(item_id, slug):
            success_count += 1
        else:
            failed_items.append(slug)
        # Small delay to avoid rate limiting
        time.sleep(0.5)

    print()
    print(f"Updated: {success_count}/{len(ITEMS)} items")
    if failed_items:
        print(f"Failed: {', '.join(failed_items)}")

    print()
    print("Script complete. Use Webflow CMS tool to publish all items.")

if __name__ == "__main__":
    main()
