# GA4 Setup for AIR Community Subdomain Sites

**Handoff Date:** September 14, 2026
**For:** Developer setting up analytics on AIR community sites
**Measurement ID:** `G-DK6QHHS88K`
**Priority:** Set up before any content goes live

---

## Community Subdomain Sites (10 total)

| Community | Subdomain |
|---|---|
| Foxchase | `foxchase.brightplace.ai` |
| Citi Lakes | `citi-lakes.brightplace.ai` |
| Sorrel (LUX at Sorrel) | `sorrel.brightplace.ai` |
| Verdant Peachtree Creek | `verdant-peachtree-creek.brightplace.ai` |
| Villages at Raleigh Beach | `villages-at-raleigh-beach.brightplace.ai` |
| One Canal | `one-canal.brightplace.ai` |
| Indigo West | `indigo-west.brightplace.ai` |
| One Boynton | `one-boynton.brightplace.ai` |
| 3400 Avenue of the Arts | `3400-avenue-of-the-arts.brightplace.ai` |
| Citigate | `citigate.brightplace.ai` |

---

## GA4 Script (Add to Every Page)

Place this in the `<head>` of every HTML page, **before any other scripts**:

```html
<!-- Google Analytics (GA4) - brightplace - DO NOT REMOVE -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-DK6QHHS88K"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-DK6QHHS88K');
</script>
```

This is the same Measurement ID used across all brightplace properties. GA4 handles subdomain tracking natively since all sites are under `*.brightplace.ai`.

---

## Custom Events Script (Add to Blog Article Pages)

Place this before `</body>` on every blog/article page:

```html
<!-- brightplace Content Analytics - DO NOT REMOVE -->
<script>
  // Scroll depth tracking (25%, 50%, 75%, 90%)
  (function() {
    var thresholds = [25, 50, 75, 90];
    var fired = [];
    window.addEventListener('scroll', function() {
      var pct = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
      thresholds.forEach(function(t) {
        if (pct >= t && fired.indexOf(t) === -1) {
          fired.push(t);
          gtag('event', 'scroll_depth', {
            'percent_scrolled': t,
            'page_title': document.title,
            'community': document.querySelector('meta[name="author"]')?.content || 'unknown'
          });
        }
      });
    });
  })();

  // Engaged time tracking (30s, 60s, 120s, 300s)
  [30, 60, 120, 300].forEach(function(s) {
    setTimeout(function() {
      gtag('event', 'engaged_time', {
        'seconds_on_page': s,
        'page_title': document.title
      });
    }, s * 1000);
  });

  // Outbound link clicks
  document.addEventListener('click', function(e) {
    var link = e.target.closest('a[href]');
    if (link && link.hostname !== window.location.hostname) {
      gtag('event', 'outbound_click', {
        'link_url': link.href,
        'link_text': link.textContent.trim().substring(0, 100),
        'page_title': document.title
      });
    }
  });

  // CTA clicks (brightplace links)
  document.addEventListener('click', function(e) {
    var link = e.target.closest('a[href]');
    if (link && (link.href.indexOf('app.brightplace.ai') !== -1 || link.href.indexOf('brightplace.ai') !== -1)) {
      gtag('event', 'cta_click', {
        'cta_url': link.href,
        'cta_text': link.textContent.trim().substring(0, 100),
        'page_title': document.title,
        'community': document.querySelector('meta[name="author"]')?.content || 'unknown'
      });
    }
  });

  // FAQ section viewed
  var faq = document.querySelector('.faq-section');
  if (faq) {
    var obs = new IntersectionObserver(function(entries) {
      if (entries[0].isIntersecting) {
        gtag('event', 'faq_viewed', { 'page_title': document.title });
        obs.disconnect();
      }
    }, { threshold: 0.5 });
    obs.observe(faq);
  }
</script>
```

---

## GA4 Custom Dimensions (Set Up in GA4 Admin)

Go to GA4 > Admin > Custom definitions > Create custom dimensions:

| Dimension Name | Scope | Event Parameter |
|---|---|---|
| Community | Event | `community` |
| Scroll Depth | Event | `percent_scrolled` |
| CTA Text | Event | `cta_text` |
| CTA URL | Event | `cta_url` |
| Seconds on Page | Event | `seconds_on_page` |

---

## Google Search Console Setup

Each subdomain needs its own GSC property:

1. Go to [Google Search Console](https://search.google.com/search-console/)
2. Add property > URL prefix: `https://foxchase.brightplace.ai`
3. Verify via DNS (TXT record) or HTML file upload
4. Repeat for all 10 subdomains
5. Submit each subdomain's sitemap: `https://[subdomain].brightplace.ai/sitemap.xml`

Also add a domain-level property for `brightplace.ai` to see aggregate data across all subdomains.

---

## Checklist Before Go-Live

- [ ] GA4 `G-DK6QHHS88K` script in `<head>` of all pages on all subdomains
- [ ] Custom events script before `</body>` on blog article pages
- [ ] Custom dimensions registered in GA4 Admin
- [ ] Realtime report confirms data flowing from each subdomain
- [ ] No duplicate gtag scripts (causes double-counting)
- [ ] robots.txt on each subdomain allows Google crawling
- [ ] sitemap.xml submitted for each subdomain in Google Search Console
- [ ] GSC property created and verified for each subdomain

---

*All 34 stage-10 HTML article files already include GA4 + custom events. The developer only needs to ensure the site template/layout also includes these scripts for non-article pages.*
