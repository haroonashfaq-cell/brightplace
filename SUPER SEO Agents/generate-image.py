#!/usr/bin/env python3
"""
SUPER SEO Agents — Image Generator
Generates a blog featured image using GPT Image 1 (gpt-image-1) at high quality,
resizes to 1200x628, compresses to WebP under 200KB.

Supports two modes:
  1. Direct prompt: --prompt "Your image prompt here"
  2. Content-aware: --title "Blog Title" --content /path/to/article.md
     Reads the article and builds a context-rich prompt automatically.

Usage:
  python3 generate-image.py --prompt "Your prompt" --output /path/to/output.webp --alt "Alt text"
  python3 generate-image.py --title "Blog Title" --content /path/to/09-final.md --output /path/to/output.webp

Requires: OPENAI_API_KEY in .env or environment
"""

import argparse
import os
import sys
import io
import json
import re
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("ERROR: openai package not installed. Run: pip3 install openai")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("ERROR: Pillow package not installed. Run: pip3 install Pillow")
    sys.exit(1)

import urllib.request


def load_env():
    """Load .env file from project root."""
    env_paths = [
        Path(__file__).parent.parent / ".env",
        Path.cwd() / ".env",
    ]
    for env_path in env_paths:
        if env_path.exists():
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#") and "=" in line:
                        key, value = line.split("=", 1)
                        os.environ.setdefault(key.strip(), value.strip())
            return True
    return False


def extract_content_context(title, content_path):
    """Read article markdown, classify the visual subject, and extract scene elements."""
    raw = Path(content_path).read_text(encoding="utf-8")

    if raw.startswith("---"):
        end = raw.find("---", 3)
        if end != -1:
            raw = raw[end + 3:].strip()

    full_text = (title + " " + raw).lower()

    return {
        "title": title,
        "subject": _detect_subject(title),
        "elements": _extract_visual_elements(full_text),
        "setting": _detect_setting(full_text),
        "differentiator": _extract_differentiator(full_text),
    }


def _detect_subject(title):
    """Classify the article's primary visual theme from the title."""
    t = title.lower()
    if any(w in t for w in ["pet", "dog", "cat"]):
        return "pet_friendly"
    if re.search(r"near\s+(seaworld|disney|universal|downtown|ucf)", t):
        return "location"
    if re.search(r"\d\s*-?\s*bed", t) or "studio" in t:
        return "floor_plans"
    if any(w in t for w in ["luxury", "upscale", "premium"]):
        return "luxury"
    if any(w in t for w in ["affordable", "cheap", "budget", "value"]):
        return "value"
    if any(w in t for w in ["family", "kid", "school"]):
        return "family"
    return "community"


_ELEMENT_MAP = {
    "fenced dog park with open grass": ["dog park", "bark park", "pet park"],
    "pet washing station": ["pet wash", "dog wash", "grooming station"],
    "resort pool with gradual beach-style entry": ["zero-entry pool", "beach-style pool", "zero entry"],
    "private poolside cabanas": ["cabana", "cabanas"],
    "lakefront with calm water reflections": ["lakefront", "waterfront", "lake view", "two lakes", "on a lake"],
    "scenic jogging trail along the water": ["jogging trail", "walking trail", "running trail"],
    "lakeside gazebo with string lights": ["gazebo"],
    "dedicated cycling spin studio": ["spin studio", "cycling studio"],
    "modern fitness center with large windows": ["fitness center", "gym", "workout room"],
    "children's playground": ["playground", "play area"],
    "outdoor grilling stations with seating": ["grill", "grilling", "bbq"],
    "courtyard fire pit": ["fire pit", "firepit"],
    "rooftop terrace with city views": ["rooftop", "roof deck", "sky lounge"],
    "balconies overlooking the grounds": ["balcon"],
    "gated community entrance": ["gated", "gated community"],
}


def _extract_visual_elements(text):
    """Find specific amenities mentioned in the article that should appear in the image."""
    found = []
    for element, keywords in _ELEMENT_MAP.items():
        if any(kw in text for kw in keywords):
            found.append(element)
    return found[:5]


def _detect_setting(text):
    """Identify geographic and environmental details for the scene."""
    parts = []
    if any(w in text for w in ["orlando", "florida", " fl "]):
        parts.append("Central Florida with tall palm trees, subtropical plants, and warm humid atmosphere")
    elif any(w in text for w in ["atlanta", "georgia", " ga "]):
        parts.append("Georgia with magnolia trees, red brick accents, and deciduous landscaping")
    elif any(w in text for w in ["virginia", " va "]):
        parts.append("Virginia with deciduous hardwood trees and colonial architectural influence")
    elif any(w in text for w in ["north carolina", "raleigh"]):
        parts.append("North Carolina with longleaf pines and Southern landscaping")

    if any(w in text for w in ["lakefront", "waterfront", "two lakes", "lake view"]):
        parts.append("a visible lake with reflections on the water surface in the scene")
    if any(w in text for w in ["seaworld", "i-drive", "international drive", "theme park"]):
        parts.append("near an entertainment and tourism corridor")

    return ". ".join(parts) if parts else "well-landscaped suburban apartment setting"


def _extract_differentiator(text):
    """Find the single most visually distinctive feature of the community."""
    candidates = [
        ("a two-lake waterfront campus with trails circling both lakes", ["two lakes"]),
        ("lakefront setting with direct water views from the property", ["lakefront", "lake view", "on a lake"]),
        ("a zero-entry resort pool with beach walk-in and private cabanas", ["zero-entry", "zero entry"]),
        ("a rooftop terrace or sky lounge with panoramic views", ["rooftop", "sky lounge"]),
        ("a prominent fenced dog park with pet amenities", ["dog park", "no weight limit"]),
        ("a resort-style pool and outdoor recreation area", ["resort pool", "resort-style"]),
        ("natural wooded setting with mature trees", ["wooded", "tree-lined", "nature preserve"]),
    ]
    for diff, keywords in candidates:
        if any(kw in text for kw in keywords):
            return diff
    return "manicured grounds with mature landscaping"


_SUBJECT_SCENES = {
    "pet_friendly": (
        "The image MUST prominently feature a fenced dog park with green grass as the "
        "MAIN FOCAL POINT occupying the center-foreground of the frame. Include a small "
        "friendly dog (golden retriever or similar) exploring the park — no people. "
        "A pet washing station or pet amenity area should be visible nearby. "
        "Apartment buildings are in the background, secondary to the dog park."
    ),
    "location": (
        "Show the apartment community from an elevated angle that reveals the surrounding "
        "neighborhood and area context. The buildings should be in the mid-ground with the "
        "surrounding area (roads, nearby landmarks, greenery) visible, conveying a sense "
        "of convenient location. Include the community's best amenity in the foreground."
    ),
    "floor_plans": (
        "Show apartment buildings at dusk with warm interior light glowing through large "
        "windows on multiple floors, suggesting spacious well-lit interiors. Include visible "
        "balconies at different levels. The community's signature amenity (pool, courtyard) "
        "should be prominent in the foreground, showing the lifestyle that comes with the unit."
    ),
    "luxury": (
        "Showcase the most upscale elements: a pristine pool area with elegant lounge "
        "furniture, modern architectural lines, premium exterior materials (stone, glass), "
        "and meticulous landscaping. The composition should feel aspirational and polished."
    ),
    "value": (
        "Show a welcoming, bright apartment community that feels approachable and livable. "
        "Emphasize well-kept green spaces, clean walkways, and practical amenities like "
        "a pool or picnic area. The scene should feel warm and inviting, not intimidating."
    ),
    "family": (
        "Feature family-oriented amenities as the focal point — a playground, wide open "
        "green spaces, safe well-lit walkways. Apartment buildings provide context in the "
        "background. The scene should feel safe and community-oriented."
    ),
    "community": (
        "Show a wide establishing shot of the apartment community with its single most "
        "distinctive amenity dominating the foreground."
    ),
}


def build_prompt_from_content(context):
    """Build a specific image prompt based on the article's visual subject and elements."""
    subject = context["subject"]
    elements = context["elements"]
    setting = context["setting"]
    diff = context["differentiator"]

    scene_direction = _SUBJECT_SCENES.get(subject, _SUBJECT_SCENES["community"])

    elements_str = ", ".join(elements) if elements else "pool area and landscaped grounds"

    prompt = (
        f"Professional editorial real estate photograph. "
        f"{scene_direction} "
        f"The community features: {elements_str}. "
        f"Its unique differentiator is {diff}. "
        f"Setting: {setting}. "
        f"Style: high-end real estate editorial photography, natural lighting at golden hour, "
        f"rich saturated colors, shot with a wide-angle lens at eye level. "
        f"16:9 landscape aspect ratio. "
        f"STRICT: No people visible anywhere (Fair Housing compliance). "
        f"No text, no logos, no watermarks, no graphic overlays."
    )
    return prompt


def generate_image(prompt, output_path, alt_text="", max_size_kb=200):
    """Generate image with GPT Image 1 at high quality, resize to 1200x628, compress to WebP."""

    load_env()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found in environment or .env file")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    print(f"Generating image with gpt-image-1 (high quality)...")
    print(f"Prompt: {prompt[:150]}...")

    response = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1536x1024",
        quality="high",
        n=1,
    )

    image_data_response = response.data[0]
    revised_prompt = getattr(image_data_response, "revised_prompt", "") or ""

    image_url = getattr(image_data_response, "url", None)
    b64_data = getattr(image_data_response, "b64_json", None)

    print(f"Image generated. Downloading...")

    if b64_data:
        import base64
        raw_image = base64.b64decode(b64_data)
    elif image_url:
        req = urllib.request.Request(image_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as resp:
            raw_image = resp.read()
    else:
        print("ERROR: No image URL or base64 data in response")
        sys.exit(1)

    img = Image.open(io.BytesIO(raw_image))

    # Resize to 1200x628 (blog featured image)
    target_width, target_height = 1200, 628

    # Crop to target aspect ratio first, then resize
    img_ratio = img.width / img.height
    target_ratio = target_width / target_height

    if img_ratio > target_ratio:
        new_width = int(img.height * target_ratio)
        left = (img.width - new_width) // 2
        img = img.crop((left, 0, left + new_width, img.height))
    else:
        new_height = int(img.width / target_ratio)
        top = (img.height - new_height) // 2
        img = img.crop((0, top, img.width, top + new_height))

    img = img.resize((target_width, target_height), Image.LANCZOS)

    # Compress to WebP under max_size_kb
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    quality = 90
    while quality >= 20:
        buffer = io.BytesIO()
        img.save(buffer, format="WEBP", quality=quality)
        size_kb = buffer.tell() / 1024

        if size_kb <= max_size_kb:
            with open(output_path, "wb") as f:
                f.write(buffer.getvalue())
            print(f"Saved: {output_path}")
            print(f"Dimensions: {target_width}x{target_height}")
            print(f"Size: {size_kb:.1f}KB (target: under {max_size_kb}KB)")
            print(f"Quality: {quality}")
            print(f"Format: WebP")
            if alt_text:
                print(f"Alt text: {alt_text}")
            if revised_prompt:
                print(f"Revised prompt: {revised_prompt[:150]}...")

            meta_path = output_path.with_suffix(".json")
            meta = {
                "original_prompt": prompt,
                "revised_prompt": revised_prompt,
                "alt_text": alt_text,
                "dimensions": f"{target_width}x{target_height}",
                "size_kb": round(size_kb, 1),
                "quality": quality,
                "format": "webp",
                "model": "gpt-image-1",
            }
            with open(meta_path, "w") as f:
                json.dump(meta, f, indent=2)
            print(f"Metadata: {meta_path}")
            return True

        quality -= 5

    print(f"WARNING: Could not compress below {max_size_kb}KB. Saved at {size_kb:.1f}KB with quality {quality}.")
    with open(output_path, "wb") as f:
        f.write(buffer.getvalue())
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate SEO blog featured image")
    parser.add_argument("--prompt", help="Direct image generation prompt")
    parser.add_argument("--title", help="Article title (used with --content for auto-prompt)")
    parser.add_argument("--content", help="Path to article markdown (used with --title)")
    parser.add_argument("--output", required=True, help="Output file path (.webp)")
    parser.add_argument("--alt", default="", help="Alt text for the image")
    parser.add_argument("--max-size", type=int, default=200, help="Max file size in KB (default: 200)")
    args = parser.parse_args()

    if args.prompt:
        final_prompt = args.prompt
    elif args.title and args.content:
        context = extract_content_context(args.title, args.content)
        final_prompt = build_prompt_from_content(context)
        print(f"Auto-generated prompt from article content.")
    else:
        print("ERROR: Provide either --prompt or both --title and --content")
        sys.exit(1)

    generate_image(final_prompt, args.output, args.alt, args.max_size)
