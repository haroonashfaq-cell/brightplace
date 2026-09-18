#!/usr/bin/env python3
"""Minimal HTML->Markdown for Webflow post-body content (h1-h4, p, strong, em, a, ul/ol/li, blockquote, img)."""
import re, html, sys

def convert(s: str) -> str:
    s = re.sub(r'<(script|style)[^>]*>.*?</\1>', '', s, flags=re.S|re.I)
    # inline first
    s = re.sub(r'<img[^>]*?src="([^"]+)"[^>]*?alt="([^"]*)"[^>]*?>', r'![\2](\1)', s, flags=re.I)
    s = re.sub(r'<img[^>]*?src="([^"]+)"[^>]*?>', r'![](\1)', s, flags=re.I)
    s = re.sub(r'<a[^>]*?href="([^"]+)"[^>]*?>(.*?)</a>', r'[\2](\1)', s, flags=re.S|re.I)
    s = re.sub(r'<(strong|b)>(.*?)</\1>', r'**\2**', s, flags=re.S|re.I)
    s = re.sub(r'<(em|i)>(.*?)</\1>', r'*\2*', s, flags=re.S|re.I)
    s = re.sub(r'<code>(.*?)</code>', r'`\1`', s, flags=re.S|re.I)
    s = re.sub(r'<br\s*/?>', '\n', s, flags=re.I)
    # lists
    def li(m): return '- ' + m.group(1).strip() + '\n'
    s = re.sub(r'<li[^>]*>(.*?)</li>', li, s, flags=re.S|re.I)
    s = re.sub(r'</?(ul|ol)[^>]*>', '\n', s, flags=re.I)
    # blocks
    for n in (4,3,2,1):
        s = re.sub(rf'<h{n}[^>]*>(.*?)</h{n}>', lambda m,n=n: '\n'+'#'*n+' '+m.group(1).strip()+'\n', s, flags=re.S|re.I)
    s = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', lambda m: '\n> '+m.group(1).strip()+'\n', s, flags=re.S|re.I)
    s = re.sub(r'<p[^>]*>(.*?)</p>', lambda m: '\n'+m.group(1).strip()+'\n', s, flags=re.S|re.I)
    s = re.sub(r'<[^>]+>', '', s)            # strip anything left
    s = html.unescape(s)
    s = re.sub(r'[ \t]+\n', '\n', s)
    s = re.sub(r'\n{3,}', '\n\n', s)
    return s.strip() + '\n'

if __name__ == '__main__':
    sys.stdout.write(convert(open(sys.argv[1]).read()))
