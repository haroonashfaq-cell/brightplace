import markdown
import re
import os

BASE_MD = "/Users/matiullahkhan/Desktop/brightplace/brightplace intelligence/Complete Articles"
BASE_HTML = "/Users/matiullahkhan/Desktop/brightplace/brightplace intelligence/Webflow CMS Data"

SLUGS = [
    "pet-deposit-vs-pet-fee",
    "cat-friendly-apartments",
    "rent-affordability-18-an-hour",
    "one-bedroom-apartment-nyc",
    "sublet-apartments-nyc",
    "homes-for-rent-no-deposit",
    "apartments-near-university-of-texas-san-antonio",
    "apartments-with-dog-parks",
    "move-in-specials-apartments",
    "prorated-rent",
    "questions-to-ask-when-touring-an-apartment",
    "redstone-ranch-denver",
    "renters-insurance-with-roommates",
    "restaurants-for-lease-near-me",
    "rooms-for-rent-huntsville-al",
    "parkside-at-legacy-plano",
    "venice-lofts-apartments-philadelphia-pa",
]

def convert_md_to_html(md_path, html_path, slug):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove frontmatter (between --- markers)
    content = re.sub(r'^---\n.*?\n---\n*', '', content, count=1, flags=re.DOTALL)

    # 2. Remove H1 line (# Title)
    content = re.sub(r'^# .+\n*', '', content, count=1, flags=re.MULTILINE)

    # 3. Remove "Last reviewed" italic lines
    content = re.sub(r'^\*Last reviewed.*?\*\n*', '', content, flags=re.MULTILINE)

    # 4. Remove HTML comments
    content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

    # 5. Remove everything from "## FAQ Schema" onwards (various forms)
    content = re.sub(r'\n## FAQ Schema.*', '', content, flags=re.DOTALL)
    content = re.sub(r'\n## Article Schema.*', '', content, flags=re.DOTALL)
    content = re.sub(r'\n## WebPage Schema.*', '', content, flags=re.DOTALL)
    content = re.sub(r'\n## Structured Data.*', '', content, flags=re.DOTALL)
    content = re.sub(r'\n## JSON-LD.*', '', content, flags=re.DOTALL)

    # 6. Convert markdown to HTML
    html = markdown.markdown(content, extensions=['tables', 'fenced_code'])

    # 7. Remove <h1> tags (shouldn't exist but safety)
    html = re.sub(r'<h1>.*?</h1>\n*', '', html, flags=re.DOTALL)

    # 8. Remove <script> tags
    html = re.sub(r'<script.*?</script>', '', html, flags=re.DOTALL)

    # 9. Convert <ul><li> to <p><strong>Label:</strong> text</p>
    def convert_ul_to_p(match):
        ul_content = match.group(1)
        items = re.findall(r'<li>(.*?)</li>', ul_content, flags=re.DOTALL)
        result = []
        for item in items:
            item = item.strip()
            # Check if item has bold label pattern
            m = re.match(r'^(<strong>.*?</strong>:?\s*)(.*)', item, flags=re.DOTALL)
            if m:
                label_part = m.group(1)
                rest = m.group(2)
                if not label_part.rstrip().endswith(':'):
                    label_part = label_part.rstrip()
                    if label_part.endswith('</strong>'):
                        label_part = label_part[:-9] + ':</strong>'
                    else:
                        label_part = label_part + ':'
                    label_part += ' '
                result.append(f'<p>{label_part}{rest}</p>')
            else:
                result.append(f'<p>{item}</p>')
        return '\n'.join(result)

    html = re.sub(r'<ul>\s*(.*?)\s*</ul>', convert_ul_to_p, html, flags=re.DOTALL)

    # 10. Remove empty code blocks that might remain from schema removal
    html = re.sub(r'<pre><code class="language-json">.*?</code></pre>', '', html, flags=re.DOTALL)
    html = re.sub(r'<pre><code>.*?</code></pre>', '', html, flags=re.DOTALL)

    # 11. Clean up excessive whitespace/newlines
    html = re.sub(r'\n{3,}', '\n', html)
    html = html.strip()

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html)

    return len(html)

if __name__ == "__main__":
    results = []
    for slug in SLUGS:
        md_path = os.path.join(BASE_MD, f"{slug}.md")
        html_path = os.path.join(BASE_HTML, f"{slug}.html")

        if not os.path.exists(md_path):
            results.append(f"MISSING: {slug}.md")
            continue

        try:
            size = convert_md_to_html(md_path, html_path, slug)
            results.append(f"OK: {slug}.html ({size:,} bytes)")
        except Exception as e:
            results.append(f"ERROR: {slug} - {str(e)}")

    for r in results:
        print(r)
