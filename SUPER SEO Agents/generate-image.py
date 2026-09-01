#!/usr/bin/env python3
"""
SUPER SEO Agents — Image Generator
Generates a blog featured image using DALL-E 3, resizes to 1200x628, compresses to WebP under 200KB.

Usage:
  python3 generate-image.py --prompt "Your image prompt here" --output /path/to/output.webp --alt "Alt text"

Requires: OPENAI_API_KEY in .env or environment
"""

import argparse
import os
import sys
import io
import json
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


def generate_image(prompt, output_path, alt_text="", max_size_kb=200):
    """Generate image with DALL-E 3, resize to 1200x628, compress to WebP."""

    load_env()

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("ERROR: OPENAI_API_KEY not found in environment or .env file")
        sys.exit(1)

    client = OpenAI(api_key=api_key)

    print(f"Generating image with GPT Image 2...")
    print(f"Prompt: {prompt[:100]}...")

    response = client.images.generate(
        model="gpt-image-2",
        prompt=prompt,
        size="1536x1024",
        quality="medium",
        n=1,
    )

    image_data_response = response.data[0]
    revised_prompt = getattr(image_data_response, "revised_prompt", "") or ""

    # Handle both URL and b64_json response formats
    image_url = getattr(image_data_response, "url", None)
    b64_data = getattr(image_data_response, "b64_json", None)

    print(f"Image generated. Downloading...")

    # Download or decode the image
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

    # Resize to 1200x628 (16:9 blog featured image)
    target_width, target_height = 1200, 628

    # Crop to 16:9 first, then resize
    img_ratio = img.width / img.height
    target_ratio = target_width / target_height

    if img_ratio > target_ratio:
        # Image is wider — crop sides
        new_width = int(img.height * target_ratio)
        left = (img.width - new_width) // 2
        img = img.crop((left, 0, left + new_width, img.height))
    else:
        # Image is taller — crop top/bottom
        new_height = int(img.width / target_ratio)
        top = (img.height - new_height) // 2
        img = img.crop((0, top, img.width, top + new_height))

    img = img.resize((target_width, target_height), Image.LANCZOS)

    # Compress to WebP under max_size_kb
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    quality = 85
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
            print(f"DALL-E revised prompt: {revised_prompt[:150]}...")

            # Save metadata alongside the image
            meta_path = output_path.with_suffix(".json")
            meta = {
                "original_prompt": prompt,
                "revised_prompt": revised_prompt,
                "alt_text": alt_text,
                "dimensions": f"{target_width}x{target_height}",
                "size_kb": round(size_kb, 1),
                "quality": quality,
                "format": "webp",
                "model": "gpt-image-2",
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
    parser = argparse.ArgumentParser(description="Generate SEO blog featured image with DALL-E 3")
    parser.add_argument("--prompt", required=True, help="Image generation prompt")
    parser.add_argument("--output", required=True, help="Output file path (.webp)")
    parser.add_argument("--alt", default="", help="Alt text for the image")
    parser.add_argument("--max-size", type=int, default=200, help="Max file size in KB (default: 200)")
    args = parser.parse_args()

    generate_image(args.prompt, args.output, args.alt, args.max_size)
