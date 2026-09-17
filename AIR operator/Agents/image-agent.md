# AIR Operator — Image Agent

**Role:** Generate production-ready featured images for AIR community blog posts. This agent reads the article, classifies its visual subject, and generates an image that is specific to that article's content — not a generic apartment photo.

**Trigger:** After stage 08 (image prompts) is saved, or when Claude needs a featured image for CMS upload.

---

## How the Prompt Engine Works

The script does NOT just dump headings into a template. It runs 4 analysis steps:

1. **Subject classification** — reads the title to determine the article's visual category:
   - `pet_friendly` → dog park as focal point, dog visible, pet amenities
   - `location` → elevated angle showing surrounding area and neighborhood context
   - `floor_plans` → buildings at dusk with glowing interiors, balconies, amenity in foreground
   - `luxury` → upscale pool, modern architecture, premium materials
   - `value` → welcoming, bright, approachable community
   - `family` → playground, green spaces, safe walkways
   - `community` → wide establishing shot, signature amenity as hero

2. **Visual element extraction** — scans the full article body for specific amenities mentioned (dog park, zero-entry pool, cabanas, lakefront, jogging trail, gazebo, spin studio, fire pit, etc.) and includes only those actually referenced in the article

3. **Geographic setting detection** — identifies Florida palms, Georgia magnolias, Virginia hardwoods, etc. Also detects lakefront, waterfront, and entertainment corridor proximity

4. **Differentiator extraction** — finds the single most visually distinctive feature of the community (two-lake campus, zero-entry resort pool, rooftop terrace, etc.)

Each article gets a DIFFERENT composition based on what it's actually about.

---

## How to Run

### Option A: Content-aware mode (PREFERRED)

```bash
python3 "SUPER SEO Agents/generate-image.py" \
  --title "Article Title Here" \
  --content "[community]-intelligence/[keyword-slug]/09-[keyword-slug]-final-enriched.md" \
  --output "[community]-intelligence/[keyword-slug]/[keyword-slug]-featured.webp" \
  --alt "[Descriptive alt text with primary keyword]"
```

The script reads the full article, classifies it, and builds a subject-specific prompt automatically.

### Option B: Direct prompt (manual override)

```bash
python3 "SUPER SEO Agents/generate-image.py" \
  --prompt "Your specific image prompt here" \
  --output "[community]-intelligence/[keyword-slug]/[keyword-slug]-featured.webp" \
  --alt "[Alt text]"
```

Use Option B only when you need full manual control over the prompt.

---

## What Each Subject Type Produces

| Subject | Focal Point | Background | Example Article |
|---------|------------|------------|-----------------|
| `pet_friendly` | Fenced dog park with a dog, pet wash station | Apartment buildings | "Pet-Friendly Apartments Orlando" |
| `location` | Neighborhood context, surrounding area | Community from elevated angle | "Apartments Near SeaWorld Orlando" |
| `floor_plans` | Glowing windows at dusk showing interiors | Signature amenity (pool/courtyard) | "2 Bedroom Apartments Orlando" |
| `luxury` | Premium pool, modern architecture | High-end landscaping | "Luxury Apartments Downtown" |
| `value` | Well-kept green space, practical amenities | Bright welcoming buildings | "Affordable Apartments Orlando" |
| `family` | Playground, open green areas | Safe walkways, community feel | "Family-Friendly Apartments" |
| `community` | Signature amenity (lake, pool, etc.) | Wide establishing shot | "Citi Lakes Apartments Orlando" |

---

## Image Requirements

- **Dimensions:** 1200 x 628px (CMS featured image spec)
- **Format:** WebP
- **Max file size:** 200KB
- **Model:** gpt-image-1 at high quality
- **No people visible** (Fair Housing compliance)
- **No text, logos, or watermarks**

---

## CMS Upload Flow After Generation

### Step 1: Create media record
```
media_save(
  filename: "[keyword-slug]-featured.webp",
  content_type: "image/webp",
  size_bytes: [file size from stat],
  community_id: "[community-id]",
  operation: "create",
  request_key: [uuid]
)
```
Returns: `upload_url` (S3 presigned URL) and `media_id`.

### Step 2: Upload bytes to S3
```bash
curl -X PUT \
  -H "Content-Type: image/webp" \
  -H "Content-Length: [size_bytes]" \
  --data-binary @"[path-to-image.webp]" \
  "[upload_url]"
```

### Step 3: Trigger processing
```
media_save(
  community_id: "[community-id]",
  operation: "process",
  media_id: "[media_id]",
  if_match: "[media etag]"
)
```

### Step 4: Wait for ready status
```
media_get(community_id: "[community-id]", media_id: "[media_id]")
```
Poll until `status: "ready"`. Usually 3-5 seconds.

### Step 5: Attach to article revision
```
featured_image_asset_id: "[media_id]"
featured_image_alt: "[alt text with primary keyword]"
```

---

## Alt Text Rules

- Include the primary keyword naturally
- Include the community/property name
- Describe what is ACTUALLY in the generated image
- Under 125 characters
- Match the visual subject: "Fenced dog park at Citi Lakes Orlando apartment community" not "Orlando apartment community"

---

## Output Files

| File | Location |
|------|----------|
| Image | `[community]-intelligence/[keyword-slug]/[keyword-slug]-featured.webp` |
| Metadata | `[community]-intelligence/[keyword-slug]/[keyword-slug]-featured.json` |
| Prompts | `[community]-intelligence/[keyword-slug]/08-image-prompts.md` |
