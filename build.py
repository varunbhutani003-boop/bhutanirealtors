#!/usr/bin/env python3
"""Builds the Bhutani Realtors static site into docs/ for GitHub Pages.

Content lives in content/<slug>.md (first line '# Title'); page metadata in pages.json.
Run: python3 build.py   (needs: pip install markdown)
"""
import json, os, re, html, datetime
import markdown

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "docs")
DOMAIN = "https://www.bhutanirealtors.in"
TODAY = datetime.date.today().isoformat()

BIZ = {
    "name": "Bhutani Realtors",
    "street": "325 H, Sector 38",
    "city": "Gurugram",
    "region": "Haryana",
    "pin": "122001",
    "phone": "+91-9611235897",
    "tel": "+919611235897",
    "wa": "https://wa.me/919611235897",
    "wa_visit": "https://wa.me/919611235897?text=Hi%2C%20I%27d%20like%20to%20book%20a%20site%20visit%20for%20the%20builder%20floors%20at%20Emaar%20Marbella%2C%20Gurugram",
    "instagram": "https://www.instagram.com/bhutani_realtors/",
    "linkedin": "https://www.linkedin.com/company/bhutani-realtors",
    "review": "https://g.page/r/CShjbtNN5dwYEAI/review",
    "directions": "https://www.google.com/maps/search/?api=1&query=Emaar+Marbella+Sector+66+Golf+Course+Extension+Road+Gurugram",
    "map_embed": "https://maps.google.com/maps?ll=28.397074,77.061822&q=28.397073,77.06178&z=16&output=embed",
    "varun": "https://www.millenniumchambers.in/varun-bhutani-advocate-gurugram",
    "lat": 28.397073, "lng": 77.06178,
}

NAV = [
    ("/", "Home"),
    ("/emaar-marbella-builder-floors-gurugram", "The Floors"),
    ("/emaar-marbella-builder-floors-construction-progress", "Site Progress"),
    ("/golf-course-extension-road-gurugram-guide", "Area Guide"),
    ("/builder-floor-buying-checklist-gurugram", "Buyer Checklist"),
    ("/property-pulse", "Property Pulse"),
]

IMG = "/assets/img/"
GALLERY = [
    ("emaar-marbella-gated-entrance-golf-course-extension-road", "The Address", "Emaar Marbella's gated entrance on Golf Course Extension Road"),
    ("emaar-marbella-palm-avenue-gurugram", "Palm Avenues", "Landscaped, tree-lined streets inside the community"),
    ("emaar-marbella-villas-diwali-lights", "The Neighbourhood", "The villa community, lit up for Diwali"),
    ("emaar-marbella-lamp-lit-lanes-evening", "Evening Walks", "Lamp-lit, tree-shaded lanes inside the gated community"),
    ("golf-course-extension-road-aerial-view", "From Above", "Golf Course Extension Road beside the Marbella community"),
    ("gurugram-skyline-palms-golf-course-extension-road", "The Skyline", "Palms in Marbella with the new towers of Golf Course Extension Road beyond"),
]
NATURE = [
    ("emaar-marbella-topiary-lawns-sector-65", "Topiary Lanes", "Sculpted greens and quiet villa lanes inside Emaar Marbella"),
    ("peacock-emaar-marbella-gurugram", "Peacock Neighbours", "Peacocks stroll the garden walls of the community"),
    ("emaar-marbella-peacock-garden-wall", "Nature Next Door", "Green lawns minutes from Golf Course Extension Road"),
]
PROGRESS = [
    ("plot-21-bhoomi-pujan-4-nov-2026", "4 November 2026", "Bhoomi Pujan at Plot 21"),
    ("plot-21-emaar-marbella-basement-excavation", "October 2026", "Basement excavation at Plot 21"),
]

DISCLAIMER = ("Photographs show the Emaar Marbella community and its surroundings; they do not depict the actual units, "
              "finishes or specifications. Project details are indicative and subject to change. This website is for "
              "general information and does not constitute an offer, contract or commitment of any kind. Please verify "
              "all details, approvals and RERA status where applicable before making any decision.")


def esc(s):
    return html.escape(s, quote=True)


def biz_schema():
    return {
        "@type": "RealEstateAgent",
        "@id": DOMAIN + "/#business",
        "name": BIZ["name"],
        "url": DOMAIN + "/",
        "telephone": BIZ["tel"],
        "image": DOMAIN + IMG + "emaar-marbella-gated-entrance-golf-course-extension-road.webp",
        "logo": DOMAIN + "/assets/apple-touch-icon.png",
        "address": {"@type": "PostalAddress", "streetAddress": BIZ["street"], "addressLocality": BIZ["city"],
                    "addressRegion": BIZ["region"], "postalCode": BIZ["pin"], "addressCountry": "IN"},
        "areaServed": ["Gurugram", "Golf Course Extension Road", "Sector 65", "Sector 66"],
        "sameAs": [BIZ["instagram"], BIZ["linkedin"]],
        "founder": {"@type": "Person", "name": "Varun Bhutani", "url": BIZ["varun"]},
    }


def residence_schema():
    return {
        "@type": "Residence",
        "@id": DOMAIN + "/#plot21",
        "name": "Independent builder floors, Plot 21, Emaar Marbella Phase-II",
        "description": "Four independent builder floors (one home per floor) with basement and stilt parking on a park-facing corner plot in Emaar Marbella, Sectors 65-66, Golf Course Extension Road, Gurugram.",
        "address": {"@type": "PostalAddress", "streetAddress": "Plot 21, Emaar Marbella Phase-II, Sector 65-66, Golf Course Extension Road",
                    "addressLocality": "Gurugram", "addressRegion": "Haryana", "addressCountry": "IN"},
        "geo": {"@type": "GeoCoordinates", "latitude": BIZ["lat"], "longitude": BIZ["lng"]},
    }


def page(slug, title, description, body, h1, *, schema_extra=None, image=None, kind="page", lead=None, hero=None):
    url = DOMAIN + "/" + slug if slug else DOMAIN + "/"
    img = DOMAIN + (image or IMG + "emaar-marbella-gated-entrance-golf-course-extension-road.webp")
    graph = [biz_schema()] + (schema_extra or [])
    if slug:
        graph.append({"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": DOMAIN + "/"},
            {"@type": "ListItem", "position": 2, "name": h1, "item": url}]})
    if kind == "article":
        graph.append({"@type": "Article", "headline": h1, "description": description, "image": img,
                      "dateModified": TODAY, "mainEntityOfPage": url, "inLanguage": "en-IN",
                      "author": {"@type": "Person", "name": "Varun Bhutani", "url": BIZ["varun"]},
                      "publisher": {"@id": DOMAIN + "/#business"}})
    ld = json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False, indent=1)
    here = "/" + slug
    nav = "".join(f'<a href="{h}"{" aria-current=page" if h == here else ""}>{esc(t)}</a>' for h, t in NAV)
    head_block = hero or (f'<section class="pagehead"><div class="wrap"><p class="crumbs"><a href="/">Home</a> / {esc(h1)}</p>'
                          f'<h1>{esc(h1)}</h1>{f"<p class=lead>{esc(lead)}</p>" if lead else ""}</div></section>')
    return f"""<!doctype html>
<html lang="en-IN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(description)}">
<link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta name="theme-color" content="#14213d">
<meta property="og:type" content="{'article' if kind == 'article' else 'website'}">
<meta property="og:site_name" content="Bhutani Realtors">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(description)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{img}">
<meta property="og:locale" content="en_IN">
<meta name="twitter:card" content="summary_large_image">
<meta name="geo.region" content="IN-HR">
<meta name="geo.placename" content="Gurugram">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png">
<link rel="stylesheet" href="/assets/site.css">
<script type="application/ld+json">
{ld}
</script>
</head>
<body class="{'home' if slug == '' else 'inner'}">
<a class="skip" href="#main">Skip to main content</a>
<header class="site">
  <div class="wrap bar">
    <a class="brand" href="/" aria-label="Bhutani Realtors home"><span class="mark" aria-hidden="true"><svg viewBox="0 0 24 24" width="22" height="22"><path d="M3 11 12 4l9 7" fill="none" stroke="currentColor" stroke-width="2"/><path d="M6 10v9h12v-9" fill="none" stroke="currentColor" stroke-width="2"/></svg></span><span class="bn"><b>BHUTANI</b> REALTORS</span></a>
    <button class="menu" aria-expanded="false" aria-controls="nav" onclick="var n=document.getElementById('nav');var o=n.classList.toggle('open');this.setAttribute('aria-expanded',o)">Menu</button>
    <nav id="nav" aria-label="Main">{nav}</nav>
  </div>
</header>
{head_block}
<main id="main">
{body}
</main>
<section class="cta-band" aria-labelledby="visit">
  <div class="wrap">
    <h2 id="visit">Book a private site visit</h2>
    <p>Only four homes will ever be available here. Call or WhatsApp to arrange a visit.</p>
    <p class="cta"><a class="btn" href="{BIZ['wa_visit']}">WhatsApp {BIZ['phone']}</a> <a class="btn ghost" href="tel:{BIZ['tel']}">Call now</a> <a class="btn ghost" href="{BIZ['directions']}">Get directions</a></p>
  </div>
</section>
<footer class="site">
  <div class="wrap cols">
    <div>
      <p class="fbrand"><b>BHUTANI</b> REALTORS</p>
      <address>{BIZ['street']}, {BIZ['city']}, {BIZ['region']} {BIZ['pin']}<br>
      Call / WhatsApp: <a href="{BIZ['wa']}">{BIZ['phone']}</a><br>
      <a href="{BIZ['instagram']}">Instagram @bhutani_realtors</a> · <a href="{BIZ['linkedin']}">LinkedIn</a></address>
      <p><a href="{BIZ['review']}">Visited us? Review Bhutani Realtors on Google</a></p>
    </div>
    <div>
      <p class="fhead">Explore</p>
      <ul>{''.join(f'<li><a href="{h}">{esc(t)}</a></li>' for h, t in NAV[1:])}
      <li><a href="{BIZ['varun']}">About Varun Bhutani</a></li></ul>
    </div>
    <div>
      <p class="fhead">Plot 21, Emaar Marbella Phase-II</p>
      <p>Sector 65–66, Golf Course Extension Road, Gurugram. Four independent luxury builder floors, construction under way.</p>
    </div>
  </div>
  <div class="wrap fine">{esc(DISCLAIMER)}</div>
</footer>
<a class="wa-fab" href="{BIZ['wa_visit']}" aria-label="Chat on WhatsApp to book a site visit"><svg viewBox="0 0 32 32" width="26" height="26" aria-hidden="true"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.6c-2 0-3.9-.5-5.6-1.5l-.4-.2-3.9 1 1-3.8-.3-.4A10.6 10.6 0 1 1 16 26.6zm5.8-7.9c-.3-.2-1.9-.9-2.2-1s-.5-.2-.7.2-.8 1-1 1.2-.4.2-.7 0a8.7 8.7 0 0 1-4.3-3.8c-.3-.6.3-.5.9-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6a1.2 1.2 0 0 0-.9.4 3.6 3.6 0 0 0-1.1 2.7 6.3 6.3 0 0 0 1.3 3.3 14.4 14.4 0 0 0 5.5 4.9c2 .9 2.8.9 3.8.8.6-.1 1.9-.8 2.2-1.5s.3-1.3.2-1.5-.3-.2-.6-.4z"/></svg><span>Book a visit</span></a>
</body>
</html>
"""


MD = markdown.Markdown(extensions=["extra", "sane_lists"])


def render_md(text):
    MD.reset()
    return MD.convert(text)


def write(slug, content):
    d = os.path.join(OUT, slug) if slug else OUT
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(content)


def fig(name, title, cap, cls=""):
    return (f'<figure class="{cls}"><img src="{IMG}{name}.webp" alt="{esc(cap)}" loading="lazy">'
            f'<figcaption><strong>{esc(title)}</strong> {esc(cap)}</figcaption></figure>')


def build_inner(slug, meta):
    text = open(os.path.join(ROOT, "content", slug + ".md")).read()
    h1 = text.split("\n", 1)[0].lstrip("# ").strip()
    body_md = text.split("\n", 1)[1]
    article = render_md(body_md)
    extra_top = ""
    schema = []
    if slug == "emaar-marbella-builder-floors-gurugram":
        extra_top = '<div class="gallery three">' + "".join(fig(*g) for g in NATURE) + "</div>"
        schema.append(residence_schema())
        faqs = re.findall(r"\*\*(.+?\?)\*\*\s*\n(.+?)(?:\n\n|$)", body_md, flags=re.S)
        if faqs:
            schema.append({"@type": "FAQPage", "mainEntity": [
                {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer",
                 "text": re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", a).strip()}} for q, a in faqs]})
    if slug == "emaar-marbella-builder-floors-construction-progress":
        extra_top = '<div class="gallery two">' + "".join(fig(*g) for g in PROGRESS) + "</div>"
    body = f"""<div class="wrap content">
{extra_top}
<article class="prose">
{article}
</article>
</div>"""
    write(slug, page(slug, meta["title"], meta["description"], body, h1, schema_extra=schema,
                     image=meta.get("image"), kind=meta.get("type", "page"), lead=meta.get("lead")))
    return h1


def latest_pulse():
    t = open(os.path.join(ROOT, "content", "property-pulse.md")).read()
    m = re.search(r"^## (Gurugram Property Pulse[^\n]*)", t, flags=re.M)
    return m.group(1) if m else "Gurugram Property Pulse"


def build_home():
    title = "Luxury Builder Floors in Emaar Marbella, Golf Course Extension Road, Gurugram | Bhutani Realtors"
    desc = ("Four independent luxury builder floors on a park-facing corner plot in Emaar Marbella, Sectors 65-66, "
            "Golf Course Extension Road, Gurugram. Gated community next to Golf Estate. Book a private site visit.")
    hero = f"""<section class="hero" style="background-image:linear-gradient(90deg,rgba(10,20,40,.88),rgba(10,20,40,.45)),url({IMG}emaar-marbella-palm-avenue-gurugram.webp)">
  <div class="wrap">
    <p class="eyebrow">Luxury builder floors · Golf Course Extension Road</p>
    <h1>Where Gurugram's leaders will live</h1>
    <p class="lead">Four exclusive independent floors on a park-facing corner plot inside Emaar Marbella, a gated community in Sectors 65–66, Gurugram. Moments from Golf Estate and the city's newest corporate corridor, this is a rare chance to own one of only four homes in the building.</p>
    <p class="cta"><a class="btn" href="{BIZ['wa_visit']}">Book a site visit</a> <a class="btn ghost" href="/emaar-marbella-builder-floors-gurugram">Project details &amp; FAQs</a></p>
  </div>
</section>"""
    feats = [
        ("Only four homes", "One independent floor per family, never more than four households in the building."),
        ("Corner plot, park-facing", "A park-facing corner plot with its own private car-park lane."),
        ("Basement + stilt parking", "Basement, stilt parking and four residential floors with a terrace above."),
        ("Gated Emaar community", "Marbella's own residents' club is under construction, plus access to the Marbella Phase-1 villas club."),
        ("Next to Golf Estate", "On Golf Course Extension Road, close to Gurugram's growing corporate and office corridor."),
        ("Construction under way", "Bhoomi Pujan done on 4 November 2026; basement work in progress."),
    ]
    feat_html = "".join(f"<li><h3>{esc(a)}</h3><p>{esc(b)}</p></li>" for a, b in feats)
    gal = "".join(fig(*g) for g in GALLERY)
    pulse = latest_pulse()
    body = f"""
<section class="band" aria-labelledby="res">
  <div class="wrap">
    <h2 id="res">The residences</h2>
    <ul class="feats">{feat_html}</ul>
    <p><a class="more" href="/emaar-marbella-builder-floors-gurugram">Project details &amp; FAQs</a> · <a class="more" href="/emaar-marbella-builder-floors-construction-progress">Construction progress (site photos)</a></p>
  </div>
</section>

<section class="band alt" aria-labelledby="gal">
  <div class="wrap">
    <h2 id="gal">Life in Emaar Marbella</h2>
    <p class="sub">Golf Course Extension Road, Sectors 65–66 · Next to Golf Estate · Gated, landscaped Emaar community</p>
    <div class="gallery">{gal}</div>
  </div>
</section>

<section class="band" aria-labelledby="loc">
  <div class="wrap two">
    <div>
      <h2 id="loc">Find us on the map</h2>
      <p><strong>Plot 21, Emaar Marbella Phase-II</strong>, Sector 65–66, Golf Course Extension Road, Gurugram.</p>
      <p>Office: {BIZ['street']}, {BIZ['city']}, {BIZ['region']} {BIZ['pin']}.</p>
      <p><a class="more" href="{BIZ['directions']}">Get directions in Google Maps</a> · <a class="more" href="/golf-course-extension-road-gurugram-guide">Golf Course Extension Road area guide</a></p>
      <h3>Latest from Gurugram</h3>
      <p>{esc(pulse)}</p>
      <p><a class="more" href="/property-pulse">Read the Gurugram Property Pulse</a> · <a class="more" href="/builder-floor-buying-checklist-gurugram">Builder floor buying checklist</a></p>
    </div>
    <div class="map"><iframe title="Map of Emaar Marbella, Golf Course Extension Road, Gurugram" src="{BIZ['map_embed']}" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe></div>
  </div>
</section>
"""
    write("", page("", title, desc, body, "Home", schema_extra=[residence_schema(),
                   {"@type": "WebSite", "@id": DOMAIN + "/#site", "url": DOMAIN + "/", "name": "Bhutani Realtors",
                    "publisher": {"@id": DOMAIN + "/#business"}, "inLanguage": "en-IN"}], hero=hero))
    return title, desc


def build_extras(pages, titles):
    urls = [("", "1.0")] + [(s, "0.8") for s in pages]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for s, pr in urls:
        sm.append(f"  <url><loc>{DOMAIN}/{s}</loc><lastmod>{TODAY}</lastmod><priority>{pr}</priority></url>")
    sm.append("</urlset>")
    open(os.path.join(OUT, "sitemap.xml"), "w").write("\n".join(sm) + "\n")
    open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\n\nSitemap: {DOMAIN}/sitemap.xml\n")
    lines = ["# Bhutani Realtors", "",
             "> Gurugram real-estate firm (325 H, Sector 38, Gurugram, Haryana 122001) offering four independent luxury builder "
             "floors on Plot 21, Emaar Marbella Phase-II, Sectors 65-66, Golf Course Extension Road, Gurugram. "
             f"Site visits: call or WhatsApp {BIZ['phone']}.", "", "## Key pages", ""]
    for s, m in pages.items():
        lines.append(f"- [{titles[s]}]({DOMAIN}/{s}): {m['description']}")
    open(os.path.join(OUT, "llms.txt"), "w").write("\n".join(lines) + "\n")
    open(os.path.join(OUT, ".nojekyll"), "w").write("")
    open(os.path.join(OUT, "CNAME"), "w").write("www.bhutanirealtors.in\n")
    # the old Google Site used /home
    os.makedirs(os.path.join(OUT, "home"), exist_ok=True)
    open(os.path.join(OUT, "home", "index.html"), "w").write(
        f'<!doctype html><meta charset="utf-8"><title>Bhutani Realtors</title><link rel="canonical" href="{DOMAIN}/">'
        f'<meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=/"><a href="/">Continue to Bhutani Realtors</a>')
    nf = page("404", "Page not found | Bhutani Realtors", "This page could not be found.",
              '<div class="wrap prose"><p>The page you were looking for has moved or does not exist. Try the '
              '<a href="/">home page</a> or the <a href="/emaar-marbella-builder-floors-gurugram">Emaar Marbella builder floors</a>.</p></div>',
              "Page not found")
    open(os.path.join(OUT, "404.html"), "w").write(nf.replace('content="index, follow, max-image-preview:large"', 'content="noindex"'))
    open(os.path.join(OUT, "assets", "site.css"), "w").write(open(os.path.join(ROOT, "assets-src", "site.css")).read())


def main():
    pages = json.load(open(os.path.join(ROOT, "pages.json")))
    titles = {}
    build_home()
    for slug, meta in pages.items():
        titles[slug] = build_inner(slug, meta)
    build_extras(pages, titles)
    print(f"built {len(pages) + 1} pages")


if __name__ == "__main__":
    main()
