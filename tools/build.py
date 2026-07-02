#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
REFERENCE ONLY — the static site in this repo has already been generated.
This is the Python script used to build it from the ported content
(messages/en.json + messages/id.json flattened to en_flat.json / id_flat.json,
plus the product catalogue / site config ported from the original
Next.js project's src/config/site.ts). Re-run with `python3 tools/build.py`
from the project root only if you need to regenerate the HTML after
editing product data, translations, or template markup below.
Requires Python 3.8+ only (stdlib json/os) — no other dependencies.
"""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # site root = parent of tools/
SITE = "https://activeglobalimpex.com"
FOUNDED = 2008

EN = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "en_flat.json"), encoding="utf-8"))
ID = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "id_flat.json"), encoding="utf-8"))
MSG = {"en": EN, "id": ID}

# ------------------------------------------------------------------
# site.ts ported verbatim
# ------------------------------------------------------------------
PERSONS = [
    {"id": "lokesh", "name": "Lokesh", "phone": "+918460173319", "phoneDisplay": "+91 84601 73319",
     "email": "lokesh@activeglobalimpex.com", "whatsapp": "https://wa.me/918460173319", "isPublicWhatsApp": True},
    {"id": "feroz", "name": "Feroz", "phone": "+919638563534", "phoneDisplay": "+91 96385 63534",
     "email": "feroz@activeglobalimpex.com", "whatsapp": "https://wa.me/919638563534", "isPublicWhatsApp": False},
    {"id": "javed", "name": "Javed", "phone": "+919727536686", "phoneDisplay": "+91 97275 36686",
     "email": None, "whatsapp": "https://wa.me/919727536686", "isPublicWhatsApp": False},
]
INQUIRY_EMAIL = "lokesh@activeglobalimpex.com"
WHATSAPP_CTA = "https://wa.me/918460173319"
WHATSAPP_CTA_MESSAGE = "Hello Active Global Impex,\nI would like to inquire about your products.\n(Sent from activeglobalimpex.com)"
OFFICE = {
    "id": "gandhidham", "label": "Head Office", "address": "Gandhidham, Kutch, Gujarat 370201, India",
    "mapUrl": "https://maps.google.com/?q=Gandhidham+Kutch+Gujarat+India",
}

PRODUCT_CATALOGUE = [
    {"id": "agro", "key": "agro", "items": [
        ("sesame-seeds", "Sesame Seeds", "1207.40", "Gujarat"),
        ("groundnuts", "Groundnuts", "1202.41", "Gujarat"),
        ("castor-seeds", "Castor Seeds", "1207.30", "Gujarat"),
        ("cumin", "Cumin", "0909.21", "Rajasthan / Gujarat"),
        ("coriander", "Coriander", "0909.31", "Rajasthan / Gujarat"),
        ("fennel", "Fennel", "0909.50", "Gujarat"),
        ("fenugreek", "Fenugreek", "0909.61", "Rajasthan / Gujarat"),
        ("psyllium-husk", "Psyllium Husk", "1211.90", "Gujarat"),
        ("dehydrated-onion", "Dehydrated Onion", "0712.20", "Maharashtra / Gujarat"),
        ("dehydrated-garlic", "Dehydrated Garlic", "0712.90", "Gujarat"),
        ("dehydrated-vegetables", "Dehydrated Vegetables", "0712.90", "India"),
        ("dehydrated-spices", "Dehydrated Spices", "0910.99", "India"),
    ]},
    {"id": "feed", "key": "feed", "items": [
        ("rapeseed-meal", "Rapeseed Meal", "2306.41", "India"),
        ("soybean-meal", "Soybean Meal", "2304.00", "India"),
        ("ddgs", "DDGS", "2303.30", "India"),
        ("guar-meal", "Guar Meal", "2302.50", "Rajasthan / Gujarat"),
        ("castor-meal", "Castor Meal", "2306.90", "Gujarat"),
        ("dorb", "DORB (De-Oiled Rice Bran)", "2302.40", "India"),
    ]},
    {"id": "minerals", "key": "minerals", "items": [
        ("potash-feldspar", "Potash Feldspar", "2529.10", "Rajasthan"),
        ("soda-feldspar", "Soda Feldspar", "2529.10", "Rajasthan"),
        ("quartz-powder", "Quartz Powder", "2506.10", "Rajasthan"),
        ("quartz-lumps", "Quartz Lumps", "2506.10", "Rajasthan"),
        ("quartz-grits", "Quartz Grits", "2506.10", "Rajasthan"),
        ("bentonite", "Bentonite", "2508.10", "Rajasthan"),
        ("china-clay", "China Clay", "2507.00", "Rajasthan / Gujarat"),
        ("industrial-salt", "Industrial Salt", "2501.00", "Gujarat"),
    ]},
]
TOTAL_PRODUCTS = sum(len(c["items"]) for c in PRODUCT_CATALOGUE)
assert TOTAL_PRODUCTS == 26
ALL_PRODUCTS_FLAT = [(item[1], cat["id"]) for cat in PRODUCT_CATALOGUE for item in cat["items"]]

print("Loaded config:", TOTAL_PRODUCTS, "products,", len(PERSONS), "persons")

# ------------------------------------------------------------------
# Inline icon set (lucide-equivalent strokes, 1:1 visual parity)
# ------------------------------------------------------------------
def icon(name, size=16, cls=""):
    paths = {
        "anchor": '<circle cx="12" cy="5" r="3"/><path d="M12 22V8M5 12H2a10 10 0 0 0 20 0h-3"/>',
        "arrow-right": '<path d="M5 12h14M12 5l7 7-7 7"/>',
        "shield-check": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10Z"/><path d="m9 12 2 2 4-4"/>',
        "globe2": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20Z"/>',
        "clock": '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
        "file-text": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8Z"/><path d="M14 2v6h6M8 13h8M8 17h8M8 9h2"/>',
        "leaf": '<path d="M11 20A7 7 0 0 1 4 13c0-4 3-8 10-11 1 5 3 8 3 11a7 7 0 0 1-6 7Z"/><path d="M11 20a13 13 0 0 1 3-9"/>',
        "wheat": '<path d="M11 2s3 1 3 4-3 4-3 4 3 1 3 4-3 4-3 4M9 4c1 1 1 3 0 4M9 12c1 1 1 3 0 4M4 20l7-7"/>',
        "mountain": '<path d="m8 21 4-13 4 13M2 21h20M14 10l3-4 5 8"/>',
        "package": '<path d="M21 8 12 3 3 8l9 5 9-5Z"/><path d="M3 8v8l9 5 9-5V8M12 13v8"/>',
        "info": '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>',
        "phone": '<path d="M4 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L14 13l5 2v4a2 2 0 0 1-2 2C9.5 21 3 14.5 3 6a2 2 0 0 1 1-2Z"/>',
        "mail": '<path d="M4 5h16v14H4z"/><path d="m4 6 8 7 8-7"/>',
        "map-pin": '<path d="M12 22s7-7.4 7-12.5A7 7 0 0 0 5 9.5C5 14.6 12 22 12 22Z"/><circle cx="12" cy="9.5" r="2.3"/>',
        "message-circle": '<path d="M21 11.5a8.4 8.4 0 0 1-9.8 8.3c-1 0-1.9-.2-2.7-.5L3 21l1.7-5.5A8.4 8.4 0 1 1 21 11.5Z"/>',
        "send": '<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
        "check-circle": '<path d="M22 11.1V12a10 10 0 1 1-6-9.2"/><path d="m9 11 3 3L22 4"/>',
        "alert-circle": '<circle cx="12" cy="12" r="10"/><path d="M12 8v5M12 16h.01"/>',
        "menu": '<path d="M4 6h16M4 12h16M4 18h16"/>',
        "x": '<path d="m18 6-12 12M6 6l12 12"/>',
        "globe": '<circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20Z"/>',
        "chevron-down": '<path d="m6 9 6 6 6-6"/>',
        "whatsapp": None,  # special-cased fill icon below
    }
    if name == "whatsapp":
        return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="currentColor" '
                f'aria-hidden="true" class="{cls}"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.273-.099-.471-.148-.67.15'
                '-.197.297-.767.966-.94 1.164-.173.199-.347.223-.644.075-.297-.15-1.255-.463-2.39-1.475-.883-.788-1.48-1.761'
                '-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.298-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05'
                '-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51-.173-.008-.371-.01-.57-.01-.198 0'
                '-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 '
                '4.487.709.306 1.262.489 1.694.625.712.227 1.36.195 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248'
                '-1.289.173-1.413-.074-.124-.272-.198-.57-.347m-5.421 7.403h-.004a9.87 9.87 0 0 1-5.031-1.378l-.361-.214-3.741'
                '.982.998-3.648-.235-.374a9.86 9.86 0 0 1-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884 2.64 0 5.122 1.03 6.988 '
                '2.898a9.825 9.825 0 0 1 2.893 6.994c-.003 5.45-4.437 9.884-9.885 9.884m8.413-18.297A11.815 11.815 0 0 0 12.05 '
                '0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 0 0 5.683 '
                '1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 0 0-3.48-8.413z"/></svg>')
    d = paths.get(name, "")
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" class="{cls}">{d}</svg>')

CATEGORY_ICON = {"agro": "leaf", "feed": "wheat", "minerals": "mountain"}
VALUE_ICON = ["shield-check", "globe2", "clock", "file-text"]
VALUE_KEYS = ["integrity", "reliability", "promptness", "transparency"]
PILLAR_ICON = ["shield-check", "globe2", "clock", "file-text"]
PILLAR_KEYS = ["docs", "export", "timelines", "fulldocs"]

# ------------------------------------------------------------------
# Path helpers — mirrors Next.js trailingSlash:true output structure
#   /en/index.html            (served at /en/)
#   /en/about/index.html      (served at /en/about/)
#   /en/products/index.html   (served at /en/products/)
#   ...
# ------------------------------------------------------------------
ROUTES = [
    ("index", ""),               # home
    ("about", "about"),
    ("products", "products"),
    ("contact", "contact"),
    ("privacy-policy", "privacy-policy"),
    ("terms-of-use", "terms-of-use"),
    ("disclaimer", "disclaimer"),
]
NAV_ROUTES = [("index", "nav.home"), ("about", "nav.about"), ("products", "nav.products"), ("contact", "nav.contact")]

def rel_prefix(slug):
    """CSS/JS/images are one level up from lang root, two levels up from sub-pages."""
    return "../" if slug == "index" else "../../"

def lang_switch_href(lang, slug):
    """Href to the same page in the other language."""
    other = "id" if lang == "en" else "en"
    prefix = rel_prefix(slug)
    if slug == "index":
        return f"{prefix}{other}/"
    return f"{prefix}{other}/{slug}/"

def canonical_url(lang, slug):
    return f"{SITE}/{lang}/" if slug == "index" else f"{SITE}/{lang}/{slug}/"

def nav_href(lang, current_slug, target_slug):
    if target_slug == "index":
        return "../" if current_slug != "index" else "./"
    if current_slug == "index":
        return f"{target_slug}/"
    return f"../{target_slug}/"

def header_html(lang, slug):
    other_lang = "id" if lang == "en" else "en"
    nav_items = []
    for target_slug, key in NAV_ROUTES:
        current = ' aria-current="page"' if target_slug == slug else ""
        nav_items.append(f'<a href="{nav_href(lang, slug, target_slug)}" data-i18n="{key}"{current}></a>')
    nav_items_html = "\n            ".join(nav_items)

    return f'''<header class="site-header" id="site-header">
    <div class="header-inner">
      <a class="brand" href="{nav_href(lang, slug, "index")}" aria-label="Active Global Impex — Home">
        <span class="brand-line1">ACTIVE</span>
        <span class="brand-line2">GLOBAL IMPEX</span>
      </a>

      <nav class="main-nav" aria-label="Main navigation">
        {nav_items_html}
      </nav>

      <div class="header-actions">
        <details class="lang-switch">
          <summary class="lang-toggle" aria-haspopup="listbox">
            {icon("globe", 13)}<span>{lang.upper()}</span>{icon("chevron-down", 11)}
          </summary>
          <div class="lang-menu" role="listbox">
            <a href="{'./' if lang=='en' else lang_switch_href(lang, slug)}" role="option" aria-selected="{'true' if lang=='en' else 'false'}" class="{'active' if lang=='en' else ''}">
              <span class="code">EN</span><span class="name">English</span>
            </a>
            <a href="{'./' if lang=='id' else lang_switch_href(lang, slug)}" role="option" aria-selected="{'true' if lang=='id' else 'false'}" class="{'active' if lang=='id' else ''}">
              <span class="code">ID</span><span class="name">Bahasa Indonesia</span>
            </a>
          </div>
        </details>
        <a href="{nav_href(lang, slug, 'contact')}" class="btn btn-gold-outline btn-sm" data-i18n="nav.getQuote"></a>
      </div>

      <button class="mobile-toggle" id="mobile-toggle" aria-label="Open navigation menu" aria-expanded="false" aria-controls="mobile-menu" data-i18n-attr="aria-label:nav.openMenu">
        {icon("menu", 22, "icon-menu")}
        {icon("x", 22, "icon-close")}
      </button>
    </div>
  </header>

  <div class="mobile-scrim" id="mobile-scrim"></div>
  <nav class="mobile-drawer" id="mobile-menu" aria-label="Mobile navigation">
    <div class="mobile-drawer-head">
      <span>Menu</span>
      <button class="mobile-drawer-close" aria-label="Close navigation menu" data-i18n-attr="aria-label:nav.closeMenu">{icon("x", 20)}</button>
    </div>
    <div class="mobile-nav-list">
      {"".join(f'<a href="{nav_href(lang, slug, t)}" data-i18n="{k}"{" aria-current=\"page\"" if t == slug else ""}></a>' for t, k in NAV_ROUTES)}
    </div>
    <div class="mobile-drawer-foot">
      <div class="mobile-lang-row">
        <a href="{'./' if lang=='en' else lang_switch_href(lang, slug)}" class="{'active' if lang=='en' else ''}">EN</a>
        <a href="{'./' if lang=='id' else lang_switch_href(lang, slug)}" class="{'active' if lang=='id' else ''}">ID</a>
      </div>
      <a href="{nav_href(lang, slug, 'contact')}" class="btn btn-gold btn-block" data-i18n="nav.getQuote"></a>
    </div>
  </nav>'''

def footer_html(lang, slug):
    wa_url = f"{WHATSAPP_CTA}?text={_url_enc(WHATSAPP_CTA_MESSAGE)}"
    persons_with_email = [p for p in PERSONS if p["email"]]
    persons_html = "\n".join(f'''            <div class="footer-person">
              <p class="pname">{p["name"]}</p>
              <a href="tel:{p["phone"]}">{icon("phone", 12)}{p["phoneDisplay"]}</a>
              <a href="mailto:{p["email"]}">{icon("mail", 12)}{p["email"]}</a>
            </div>''' for p in persons_with_email)

    cat_link_items = []
    for cat in PRODUCT_CATALOGUE:
        label = MSG[lang]["products.categories." + cat["key"] + ".label"]
        cat_link_items.append(f'<li><a href="{nav_href(lang, slug, "products")}#{cat["id"]}">{label}</a></li>')
    cat_links = "\n".join(cat_link_items)

    return f'''<footer class="site-footer" role="contentinfo">
    <div class="container-site" style="padding-block:4rem 0;">
      <div class="footer-grid">
        <div class="footer-brand">
          <a class="brand" href="{nav_href(lang, slug, "index")}" style="display:inline-flex;">
            <span class="brand-line1" style="font-size:1.5rem;">ACTIVE</span>
            <span class="brand-line2">GLOBAL IMPEX</span>
          </a>
          <p data-i18n="footer.tagline"></p>
          <p class="footer-est">Est. {FOUNDED}</p>
          <a href="{wa_url}" target="_blank" rel="noopener noreferrer" class="btn btn-sm footer-wa" style="background:rgba(42,92,69,.1); border:1px solid rgba(42,92,69,.3); color:var(--export-300);" aria-label="Chat with Active Global Impex on WhatsApp">
            {icon("whatsapp", 15)}<span>WhatsApp</span>
          </a>
        </div>

        <div class="footer-col">
          <h3 data-i18n="footer.quickLinks"></h3>
          <ul>
            {"".join(f'<li><a href="{nav_href(lang, slug, t)}" data-i18n="{k}"></a></li>' for t, k in NAV_ROUTES)}
          </ul>
        </div>

        <div class="footer-col">
          <h3 data-i18n="footer.products"></h3>
          <ul>
            {cat_links}
          </ul>
          <h3 class="footer-legal-h" data-i18n="footer.legal"></h3>
          <ul>
            <li><a href="{nav_href(lang, slug, 'privacy-policy')}" data-i18n="footer.privacy"></a></li>
            <li><a href="{nav_href(lang, slug, 'terms-of-use')}" data-i18n="footer.terms"></a></li>
            <li><a href="{nav_href(lang, slug, 'disclaimer')}" data-i18n="footer.disclaimer"></a></li>
          </ul>
        </div>

        <div class="footer-col footer-contact">
          <h3 data-i18n="footer.contact"></h3>
          <address>
{persons_html}
            <div class="footer-office">
              {icon("map-pin", 12)}
              <p>{OFFICE["address"]}</p>
            </div>
          </address>
        </div>
      </div>

      <div class="footer-disclaimer">
        <p><strong data-i18n="footer.disclaimerLabel"></strong> <span data-i18n="footer.disclaimerText"></span></p>
      </div>
    </div>

    <div class="footer-bottom">
      <div class="container-site footer-bottom-inner">
        <p>&copy; <span data-current-year></span> Active Global Impex. <span data-i18n="footer.rights"></span></p>
        <p class="footer-madein" data-i18n="footer.madeIn"></p>
      </div>
    </div>
  </footer>'''

def whatsapp_float_html():
    wa_url = f"{WHATSAPP_CTA}?text={_url_enc(WHATSAPP_CTA_MESSAGE)}"
    return f'''<div class="wa-float-wrap" role="complementary" aria-label="WhatsApp contact">
    <div class="wa-tooltip" id="wa-tooltip">
      <button class="wa-tooltip-dismiss" aria-label="Dismiss">{icon("x", 9)}</button>
      <p data-i18n="whatsapp.tooltip"></p>
      <p class="resp" data-i18n="whatsapp.responseTime"></p>
    </div>
    <a class="wa-fab" href="{wa_url}" target="_blank" rel="noopener noreferrer" data-i18n-attr="aria-label:whatsapp.ariaLabel" aria-label="Open WhatsApp chat">
      {icon("whatsapp", 26)}
      <span class="wa-fab-ping"></span>
    </a>
  </div>'''

def _url_enc(s):
    import urllib.parse
    return urllib.parse.quote(s)

def org_jsonld():
    return '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Active Global Impex",
  "url": "%SITE%",
  "foundingDate": "2008",
  "description": "Active Global Impex exports agro commodities, feed ingredients, and industrial minerals from Gujarat, India to buyers across Southeast Asia and the Middle East.",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Gandhidham",
    "addressRegion": "Kutch, Gujarat",
    "postalCode": "370201",
    "addressCountry": "IN"
  },
  "contactPoint": [
    {
      "@type": "ContactPoint",
      "telephone": "+918460173319",
      "contactType": "sales",
      "email": "lokesh@activeglobalimpex.com",
      "areaServed": ["ID","SG","MY","AE","SA","TH","VN","PH"],
      "availableLanguage": ["English", "Indonesian"]
    }
  ]
}
</script>'''.replace("%SITE%", SITE)

def _html_escape(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

def prerender_i18n(html, lang):
    """
    Bake real translated text into every data-i18n / data-i18n-html / data-i18n-attr
    element at build time (equivalent to the original's server-side rendering),
    so the shipped HTML is fully crawlable and readable with JavaScript disabled.
    js/i18n.js still runs on load and re-applies the same dictionary — harmless,
    and it's what makes the markup self-documenting — but the page no longer
    *depends* on JS execution for its text content.
    """
    dict_ = MSG[lang]

    def sub_plain(m):
        tag, pre, key, post = m.group(1), m.group(2), m.group(3), m.group(4)
        text = dict_.get(key)
        if text is None:
            return m.group(0)
        return f"<{tag}{pre}data-i18n=\"{key}\"{post}>{_html_escape(text)}</{tag}>"

    html = re.sub(
        r'<(\w+)([^>]*?)\bdata-i18n="([a-zA-Z0-9_.]+)"([^>]*?)></\1>',
        sub_plain, html
    )

    def sub_html(m):
        tag, pre, key, post = m.group(1), m.group(2), m.group(3), m.group(4)
        text = dict_.get(key)
        if text is None:
            return m.group(0)
        rendered = "<br>".join(_html_escape(line) for line in text.split("\n"))
        return f"<{tag}{pre}data-i18n-html=\"{key}\"{post}>{rendered}</{tag}>"

    html = re.sub(
        r'<(\w+)([^>]*?)\bdata-i18n-html="([a-zA-Z0-9_.]+)"([^>]*?)></\1>',
        sub_html, html
    )

    def sub_attr(m):
        full_attr_val = m.group(1)
        pairs = full_attr_val.split("|")
        rendered_pairs = []
        replacements = {}
        for pair in pairs:
            idx = pair.index(":")
            attr, key = pair[:idx], pair[idx + 1:]
            text = dict_.get(key, "")
            replacements[attr] = _html_escape(text)
        return replacements

    # data-i18n-attr="placeholder:key|aria-label:key2" -> also set the literal attrs
    def sub_attr_tag(m):
        tag_open = m.group(0)
        attr_match = re.search(r'data-i18n-attr="([^"]+)"', tag_open)
        if not attr_match:
            return tag_open
        pairs = attr_match.group(1).split("|")
        new_tag = tag_open
        for pair in pairs:
            idx = pair.index(":")
            attr, key = pair[:idx], pair[idx + 1:]
            text = dict_.get(key)
            if text is None:
                continue
            escaped = text.replace('"', "&quot;")
            if re.search(rf'\b{re.escape(attr)}="[^"]*"', new_tag):
                new_tag = re.sub(rf'\b{re.escape(attr)}="[^"]*"', f'{attr}="{escaped}"', new_tag)
            else:
                new_tag = new_tag[:-1] + f' {attr}="{escaped}">' if new_tag.endswith(">") else new_tag
        return new_tag

    html = re.sub(r'<\w+[^>]*\bdata-i18n-attr="[^"]+"[^>]*>', sub_attr_tag, html)
    return html

def layout(lang, slug, title, description, body, extra_scripts=""):
    prefix = rel_prefix(slug)
    canonical = canonical_url(lang, slug)
    en_url = canonical_url("en", slug)
    id_url = canonical_url("id", slug)
    og_locale = "en_US" if lang == "en" else "id_ID"
    html = f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<link rel="alternate" hreflang="en" href="{en_url}">
<link rel="alternate" hreflang="id" href="{id_url}">
<link rel="alternate" hreflang="x-default" href="{en_url}">
<meta name="robots" content="index, follow">
<meta name="theme-color" content="#0D1B2A">

<meta property="og:type" content="website">
<meta property="og:site_name" content="Active Global Impex">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{description}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE}/images/og-cover.jpg">
<meta property="og:locale" content="{og_locale}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{description}">
<meta name="twitter:image" content="{SITE}/images/og-cover.jpg">

<link rel="icon" href="{prefix}icons/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="{prefix}icons/icon-192.png">
<link rel="manifest" href="{prefix}manifest.json">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@500;600;700&family=Inter:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{prefix}css/styles.css">
<link rel="stylesheet" href="{prefix}css/animations.css">
{org_jsonld()}
</head>
<body>
<a class="skip-to-content" href="#main">Skip to main content</a>
{header_html(lang, slug)}
<main id="main">
{body}
</main>
{footer_html(lang, slug)}
{whatsapp_float_html()}
<script src="{prefix}js/i18n.js"></script>
<script src="{prefix}js/main.js"></script>
{extra_scripts}
</body>
</html>'''
    return prerender_i18n(html, lang)

# ------------------------------------------------------------------
# Reusable content blocks
# ------------------------------------------------------------------
def ticker_html():
    # JS (main.js initTicker) triples this list at runtime for a seamless -50% loop
    items = "\n        ".join(
        f'<span class="ticker-item"><span class="ticker-dot"></span><span>{name}</span></span>'
        for name, _cat in ALL_PRODUCTS_FLAT
    )
    return f'''<div class="ticker-wrap" role="region" aria-label="Product listing">
    <div class="ticker-track">
      {items}
    </div>
  </div>'''

def cta_section_html(lang, slug):
    wa_url = f"{WHATSAPP_CTA}?text={_url_enc(WHATSAPP_CTA_MESSAGE)}"
    return f'''<section class="section cta-banner grain" aria-labelledby="cta-heading">
    <div class="cta-banner-bg"></div>
    <div class="cta-rings"><div class="cta-ring-1"></div><div class="cta-ring-2"></div></div>
    <div class="container-site">
      <div class="cta-inner" data-animate="fade-up">
        <p class="eyebrow" style="justify-content:center;" data-i18n="cta.eyebrow"></p>
        <h2 id="cta-heading" data-i18n="cta.headline"></h2>
        <p data-i18n="cta.body"></p>
        <div class="cta-actions">
          <a href="{nav_href(lang, slug, 'contact')}" class="btn btn-gold">
            <span data-i18n="cta.primary"></span>{icon("arrow-right", 17)}
          </a>
          <a href="{wa_url}" target="_blank" rel="noopener noreferrer" class="btn btn-outline">
            {icon("message-circle", 17)}<span data-i18n="cta.secondary"></span>
          </a>
        </div>
        <p class="cta-fine" data-i18n="cta.fine"></p>
      </div>
    </div>
  </section>'''

def page_hero_html(eyebrow_key, headline_key, sub_key, extra_note="", anchor_icon=True):
    eyebrow_icon = icon("anchor", 11) if anchor_icon else ""
    return f'''<section class="page-hero grain">
    <div class="page-hero-bg"></div>
    <div class="container-site">
      <div data-animate-group>
        <p class="eyebrow" data-animate="fade-up">{eyebrow_icon}<span data-i18n="{eyebrow_key}"></span></p>
        <h1 data-animate="fade-up" data-i18n-html="{headline_key}"></h1>
        <p data-animate="fade-up" data-i18n="{sub_key}"></p>
        {extra_note}
      </div>
    </div>
  </section>'''

# ------------------------------------------------------------------
# HOME PAGE
# ------------------------------------------------------------------
def home_hero_html(lang, slug):
    return f'''<section class="hero grain" aria-label="Hero">
    <div class="hero-bg"></div>
    <div class="hero-rings"><div class="hero-ring-1"></div><div class="hero-ring-2"></div></div>
    <div class="hero-fade-bottom"></div>
    <div class="hero-inner">
      <div class="hero-spacer"></div>
      <div class="hero-content">
        <div class="hero-content-inner">
          <div class="hero-max" data-animate-group>
            <p class="eyebrow" data-animate="fade-up">{icon("anchor", 11)}<span data-i18n="hero.eyebrow"></span></p>
            <h1 data-animate="fade-up" data-i18n-html="hero.headline"></h1>
            <p class="hero-sub" data-animate="fade-up" data-i18n="hero.subheadline"></p>
            <div class="hero-actions" data-animate="fade-up">
              <a href="{nav_href(lang, slug, 'products')}" class="btn btn-gold">
                <span data-i18n="hero.ctaPrimary"></span>{icon("arrow-right", 15)}
              </a>
              <a href="{nav_href(lang, slug, 'contact')}" class="btn btn-outline" data-i18n="hero.ctaSecondary"></a>
            </div>
            <div class="hero-stats" data-animate="fade-up" role="list" aria-label="Key facts">
              <div class="hero-stat" role="listitem"><p data-i18n="stats.countries.value"></p><p data-i18n="stats.countries.label"></p></div>
              <div class="hero-stat" role="listitem"><p data-i18n="stats.founded.value"></p><p data-i18n="stats.founded.label"></p></div>
              <div class="hero-stat" role="listitem"><p>{TOTAL_PRODUCTS}</p><p data-i18n="stats.products.label"></p></div>
              <div class="hero-stat" role="listitem"><p data-i18n="stats.port.value"></p><p data-i18n="stats.port.label"></p></div>
            </div>
          </div>
        </div>
      </div>
      {ticker_html()}
    </div>
  </section>'''

def home_about_teaser_html(lang, slug):
    highlight_keys = ["about.highlights.iec", "about.highlights.mundra", "about.highlights.terms", "about.highlights.payment"]
    chips = "\n              ".join(f'<span data-i18n="{k}"></span>' for k in highlight_keys)
    pillars = ""
    for i, key in enumerate(PILLAR_KEYS):
        pillars += f'''<div class="card" data-animate="stagger-item">
              <div class="card-icon">{icon(PILLAR_ICON[i], 18)}</div>
              <h3 data-i18n="about.pillars.{key}.title"></h3>
              <p data-i18n="about.pillars.{key}.body"></p>
            </div>
            '''
    return f'''<section class="section section-alt" aria-labelledby="about-heading">
    <div class="container-site">
      <div class="grid grid-2" style="gap:4rem; align-items:center;">
        <div data-animate="fade-left">
          <p class="eyebrow" data-i18n="about.eyebrow"></p>
          <h2 id="about-heading" class="text-display" data-i18n-html="about.headline"></h2>
          <p style="margin-top:1.5rem; color:var(--cotton-60); line-height:1.7;" data-i18n="about.body"></p>
          <p class="pull-quote" style="margin-top:1.25rem; font-style:italic; color:rgba(200,146,42,.8); border-left:2px solid rgba(200,146,42,.3); padding-left:1rem; font-family:var(--font-display); font-size:1.125rem;" data-i18n="about.mission"></p>
          <div class="highlight-chips">
            {chips}
          </div>
          <a href="{nav_href(lang, slug, 'about')}" class="btn btn-gold-outline" style="margin-top:2rem;">
            <span data-i18n="about.cta"></span>{icon("arrow-right", 14)}
          </a>
        </div>
        <div class="grid grid-2" data-animate-group style="gap:1rem;">
          {pillars}
        </div>
      </div>
    </div>
  </section>'''

def home_products_teaser_html(lang, slug):
    tabs = ""
    panels = ""
    for i, cat in enumerate(PRODUCT_CATALOGUE):
        sel = "true" if i == 0 else "false"
        tabs += f'''<button role="tab" aria-selected="{sel}" aria-controls="home-panel-{cat['id']}" id="home-tab-{cat['id']}" data-target="{cat['id']}">
          {icon(CATEGORY_ICON[cat['id']], 14)}<span data-i18n="products.categories.{cat['key']}.label"></span>
        </button>
        '''
        items = ""
        for item_id, name, hs, origin in cat["items"]:
            items += f'''<a href="{nav_href(lang, slug, 'products')}#{item_id}" class="teaser-item">
            <div><p class="tname">{name}</p><p class="ths">HS {hs}*</p></div>
            {icon("arrow-right", 13)}
          </a>
          '''
        panels += f'''<div class="tab-panel{' active' if i == 0 else ''}" data-panel="{cat['id']}" id="home-panel-{cat['id']}" role="tabpanel"{'' if i == 0 else ' hidden'}>
          <p class="tab-tagline" data-i18n="products.categories.{cat['key']}.tagline"></p>
          <div class="grid grid-4">
            {items}
          </div>
        </div>
        '''
    return f'''<section class="section" aria-labelledby="products-heading">
    <div class="container-site">
      <div style="display:flex; flex-wrap:wrap; gap:1.5rem; align-items:flex-end; justify-content:space-between; margin-bottom:3rem;" data-animate="fade-up">
        <div style="max-width:42rem;">
          <p class="eyebrow" data-i18n="products.eyebrow"></p>
          <h2 id="products-heading" class="text-display" data-i18n-html="products.headline"></h2>
          <p style="margin-top:.75rem; color:var(--cotton-60);" data-i18n="products.subheadline"></p>
        </div>
        <a href="{nav_href(lang, slug, 'products')}" class="btn btn-gold-outline">
          <span data-i18n="products.cta"></span>{icon("arrow-right", 14)}
        </a>
      </div>
      <div class="tabs" role="tablist" aria-label="Product categories">
        {tabs}
      </div>
      {panels}
      <p class="hs-disclaimer">{icon("info", 10)}*<span data-i18n="products.hsDisclaimer"></span></p>
    </div>
  </section>'''

def build_home(lang):
    slug = "index"
    body = home_hero_html(lang, slug) + "\n" + home_about_teaser_html(lang, slug) + "\n" + home_products_teaser_html(lang, slug) + "\n" + cta_section_html(lang, slug)
    return layout(lang, slug, MSG[lang]["metadata.homeTitle"], MSG[lang]["metadata.homeDescription"], body)

# ------------------------------------------------------------------
# ABOUT PAGE
# ------------------------------------------------------------------
def build_about(lang):
    slug = "about"
    hero = page_hero_html("about.eyebrow", "about.headline", "about.body")

    highlight_keys = ["about.highlights.iec", "about.highlights.mundra", "about.highlights.terms", "about.highlights.payment"]
    highlights = "\n              ".join(
        f'<div class="highlight-item"><span class="dot"></span><span data-i18n="{k}"></span></div>' for k in highlight_keys
    )
    glance_rows_by_lang = {
        "en": [
            ("Founded", str(FOUNDED)),
            ("Headquarters", "Gandhidham, Kutch, Gujarat, India"),
            ("Export Port", "Mundra Port, Gujarat"),
            ("Product Lines", f"{TOTAL_PRODUCTS} across 3 categories"),
            ("Export Markets", "Southeast Asia · Middle East"),
            ("Languages", "English · Bahasa Indonesia"),
        ],
        "id": [
            ("Didirikan", str(FOUNDED)),
            ("Kantor Pusat", "Gandhidham, Kutch, Gujarat, India"),
            ("Pelabuhan Ekspor", "Pelabuhan Mundra, Gujarat"),
            ("Lini Produk", f"{TOTAL_PRODUCTS} produk dalam 3 kategori"),
            ("Pasar Ekspor", "Asia Tenggara · Timur Tengah"),
            ("Bahasa", "Inggris · Bahasa Indonesia"),
        ],
    }
    glance_rows = glance_rows_by_lang[lang]
    glance_html = "\n            ".join(
        f'<div class="glance-row"><span>{label}</span><span>{value}</span></div>' for label, value in glance_rows
    )

    mission_section = f'''<section class="section section-alt">
    <div class="container-site">
      <div class="grid grid-2" style="gap:4rem; align-items:center;">
        <div data-animate="fade-left">
          <p class="eyebrow" data-i18n="about.approach.eyebrow"></p>
          <h2 class="text-heading" data-i18n="about.approach.heading"></h2>
          <p style="margin-top:1.25rem; color:var(--cotton-60); line-height:1.7;" data-i18n="about.mission"></p>
          <div class="highlight-row">
            {highlights}
          </div>
        </div>
        <div class="glance" data-animate="fade-right">
          <p class="glance-title" data-i18n="about.approach.glance"></p>
          {glance_html}
        </div>
      </div>
    </div>
  </section>'''

    value_cards = ""
    for i, key in enumerate(VALUE_KEYS):
        value_cards += f'''<div class="value-card" data-animate="stagger-item">
          <div class="value-icon">{icon(VALUE_ICON[i], 20)}</div>
          <h3 data-i18n="about.values.{key}.title"></h3>
          <p data-i18n="about.values.{key}.body"></p>
        </div>
        '''
    values_section = f'''<section class="section" aria-labelledby="values-heading">
    <div class="container-site">
      <div class="section-head center" data-animate="fade-up">
        <p class="eyebrow" style="justify-content:center;" data-i18n="about.values.eyebrow"></p>
        <h2 id="values-heading" class="text-heading" data-i18n="about.values.heading"></h2>
      </div>
      <div class="grid grid-4" data-animate-group>
        {value_cards}
      </div>
    </div>
  </section>'''

    team_cards = ""
    for p in PERSONS:
        wa_url = f"{p['whatsapp']}?text={_url_enc(WHATSAPP_CTA_MESSAGE)}"
        email_line = f'<a href="mailto:{p["email"]}">{icon("mail", 13)}{p["email"]}</a>' if p["email"] else ""
        team_cards += f'''<div class="team-card" data-animate="stagger-item">
          <div class="team-avatar"><span>{p['name'][0]}</span></div>
          <h3>{p['name']}</h3>
          <div class="team-links">
            <a href="tel:{p['phone']}">{icon("phone", 13)}{p['phoneDisplay']}</a>
            {email_line}
            <a class="wa" href="{wa_url}" target="_blank" rel="noopener noreferrer">{icon("whatsapp", 13)}<span>WhatsApp</span></a>
          </div>
        </div>
        '''
    team_section = f'''<section class="section section-alt" aria-labelledby="team-heading">
    <div class="container-site">
      <div class="section-head" data-animate="fade-up">
        <p class="eyebrow" data-i18n="about.team.eyebrow"></p>
        <h2 id="team-heading" class="text-heading" data-i18n="about.team.heading"></h2>
        <p data-i18n="about.team.subheading"></p>
      </div>
      <div class="grid grid-3" data-animate-group>
        {team_cards}
      </div>
    </div>
  </section>'''

    # NOTE: In the original source this block is hardcoded English JSX (not
    # passed through next-intl's t()), so it renders in English on the /id/
    # locale too. Reproduced exactly as-is for fidelity.
    ready_title = "Ready to Start Trading?"
    ready_body = "Send us your product requirements and we will get back to you with availability and indicative pricing."
    ready_cta = "Contact Us"
    boxed_cta = f'''<section class="section">
    <div class="container-site">
      <div class="boxed-cta" data-animate="fade-up">
        <h2 class="text-heading">{ready_title}</h2>
        <p>{ready_body}</p>
        <a href="{nav_href(lang, slug, 'contact')}" class="btn btn-gold">
          <span>{ready_cta}</span>{icon("arrow-right", 15)}
        </a>
      </div>
    </div>
  </section>'''

    body = hero + "\n" + mission_section + "\n" + values_section + "\n" + team_section + "\n" + boxed_cta
    return layout(lang, slug, MSG[lang]["metadata.aboutTitle"], MSG[lang]["metadata.aboutDescription"], body)

# ------------------------------------------------------------------
# PRODUCTS PAGE
# ------------------------------------------------------------------
def build_products(lang):
    slug = "products"
    note = f'<p class="note">{icon("info", 11)}<span data-i18n="products.specsOnRequest"></span></p>'
    hero = page_hero_html("products.eyebrow", "products.headline", "products.subheadline", extra_note=note, anchor_icon=False)

    tabs = ""
    panels = ""
    for i, cat in enumerate(PRODUCT_CATALOGUE):
        sel = "true" if i == 0 else "false"
        tabs += f'''<button role="tab" aria-selected="{sel}" aria-controls="panel-{cat['id']}" id="tab-{cat['id']}" data-target="{cat['id']}">
          {icon(CATEGORY_ICON[cat['id']], 15)}<span data-i18n="products.categories.{cat['key']}.label"></span>
          <span class="count">({len(cat['items'])})</span>
        </button>
        '''
        cards = ""
        for item_id, name, hs, origin in cat["items"]:
            origin_label = "Origin" if lang == "en" else "Asal"
            cards += f'''<div class="product-card" id="{item_id}" data-animate="stagger-item">
            <div class="product-card-top">
              <div class="product-card-icon">{icon("package", 17)}</div>
              <span class="hs">HS {hs}*</span>
            </div>
            <h3>{name}</h3>
            <p class="origin">{origin_label}: {origin}</p>
            <div class="inquire">
              <a href="{nav_href(lang, slug, 'contact')}"><span data-i18n="products.inquire"></span>{icon("arrow-right", 11)}</a>
            </div>
          </div>
          '''
        panels += f'''<div class="tab-panel{' active' if i == 0 else ''}" data-panel="{cat['id']}" id="panel-{cat['id']}" role="tabpanel" aria-labelledby="tab-{cat['id']}"{'' if i == 0 else ' hidden'}>
          <p class="tab-tagline" data-i18n="products.categories.{cat['key']}.tagline"></p>
          <div class="grid grid-3" data-animate-group>
            {cards}
          </div>
        </div>
        '''

    products_section = f'''<section class="section">
    <div class="container-site">
      <div class="tabs" role="tablist" aria-label="Product categories">
        {tabs}
      </div>
      {panels}
      <p class="hs-disclaimer">{icon("info", 10)}*<span data-i18n="products.hsDisclaimer"></span></p>
    </div>
  </section>'''

    # NOTE: hardcoded English in the original source (not run through t()) —
    # reproduced verbatim on both locales for fidelity.
    need_title = "Need Specifications or a Quote?"
    need_body = "Contact us with your product requirements, destination, and quantity. We will provide specifications and indicative pricing."
    need_fine = "All pricing subject to written quotation and contract. Specifications may vary by batch and season."
    need_cta = "Request a Quote"
    boxed_cta = f'''<section class="section section-alt">
    <div class="container-site">
      <div class="boxed-cta" style="background:var(--void);" data-animate="fade-up">
        <h2 class="text-heading">{need_title}</h2>
        <p>{need_body}</p>
        <p class="fine">{need_fine}</p>
        <a href="{nav_href(lang, slug, 'contact')}" class="btn btn-gold">
          <span>{need_cta}</span>{icon("arrow-right", 15)}
        </a>
      </div>
    </div>
  </section>'''

    body = hero + "\n" + products_section + "\n" + boxed_cta
    return layout(lang, slug, MSG[lang]["metadata.productsTitle"], MSG[lang]["metadata.productsDescription"], body)

# ------------------------------------------------------------------
# CONTACT PAGE
# ------------------------------------------------------------------
def build_contact(lang):
    slug = "contact"
    hero = page_hero_html("contact.eyebrow", "contact.headline", "contact.subheadline")

    def field(name, type_, autocomplete, label_key, placeholder_key, full_width=False, required=True):
        req_mark = '<span class="req" aria-hidden="true">*</span>' if required else ""
        wrap_open = '<div class="form-field" style="grid-column:1/-1;">' if full_width else '<div class="form-field">'
        if type_ == "textarea":
            input_html = f'<textarea id="f-{name}" name="{name}" data-i18n-attr="placeholder:{placeholder_key}"></textarea>'
        else:
            input_html = (f'<input id="f-{name}" name="{name}" type="{type_}" autocomplete="{autocomplete}" '
                           f'data-i18n-attr="placeholder:{placeholder_key}"{" required" if required else ""}>')
        return f'''{wrap_open}
            <label for="f-{name}"><span data-i18n="{label_key}"></span>{req_mark}</label>
            {input_html}
            <span class="field-error" role="alert"></span>
          </div>'''

    form_fields = "\n          ".join([
        field("name", "text", "name", "contact.form.name", "contact.form.namePlaceholder"),
        field("company", "text", "organization", "contact.form.company", "contact.form.companyPlaceholder"),
        field("email", "email", "email", "contact.form.email", "contact.form.emailPlaceholder"),
        field("phone", "tel", "tel", "contact.form.phone", "contact.form.phonePlaceholder"),
        field("country", "text", "country-name", "contact.form.country", "contact.form.countryPlaceholder"),
        field("product", "text", "off", "contact.form.product", "contact.form.productPlaceholder"),
        field("quantity", "text", "off", "contact.form.quantity", "contact.form.quantityPlaceholder"),
        field("message", "textarea", "off", "contact.form.message", "contact.form.messagePlaceholder", full_width=True, required=False),
    ])

    privacy_link = nav_href(lang, slug, "privacy-policy")
    privacy_label = "Privacy Policy" if lang == "en" else "Kebijakan Privasi"
    privacy_note_text = ("By submitting this form you agree to our" if lang == "en"
                          else "Dengan mengirimkan formulir ini, Anda menyetujui")
    privacy_note_tail = ("Your data is used solely to respond to your inquiry and is not sold to third parties."
                          if lang == "en" else
                          "Data Anda hanya digunakan untuk menanggapi pertanyaan Anda dan tidak dijual kepada pihak ketiga.")

    form_html = f'''<form id="contact-form" novalidate aria-label="Product inquiry form">
        <div class="form-row form-row-2" style="grid-template-columns:repeat(2,1fr);">
          {form_fields}
        </div>
        <div class="form-error-banner" hidden role="alert">
          {icon("alert-circle", 16)}
          <div><strong></strong><span></span></div>
        </div>
        <p class="privacy-note">{privacy_note_text} <a href="{privacy_link}">{privacy_label}</a>. {privacy_note_tail}</p>
        <button type="submit" class="btn btn-gold" style="margin-top:1.5rem;">
          {icon("send", 15)}<span data-i18n="contact.form.submit"></span>
        </button>
      </form>
      <div id="form-success" class="form-success" hidden>
        {icon("check-circle", 44)}
        <h2 data-i18n="contact.form.successTitle"></h2>
        <p data-i18n="contact.form.successBody"></p>
        <button type="button" id="send-another" data-i18n="contact.form.sendAnother"></button>
      </div>'''

    wa_url = f"{WHATSAPP_CTA}?text={_url_enc(WHATSAPP_CTA_MESSAGE)}"
    wa_note = "Typically responded to within business hours (IST)." if lang == "en" else "Biasanya dibalas pada jam kerja (WIB/IST)."
    our_team_label = "Our Team" if lang == "en" else "Tim Kami"

    persons_html = ""
    for p in PERSONS:
        email_line = f'<a href="mailto:{p["email"]}">{icon("mail", 12)}{p["email"]}</a>' if p["email"] else ""
        wa_line = ""
        if p["isPublicWhatsApp"]:
            wa_line = f'<a href="{p["whatsapp"]}?text={_url_enc(WHATSAPP_CTA_MESSAGE)}" target="_blank" rel="noopener noreferrer" class="wa">{icon("whatsapp", 12)}WhatsApp</a>'
        persons_html += f'''<div class="team-card" style="padding:1.25rem;">
              <div style="display:flex; align-items:center; gap:.75rem; margin-bottom:.75rem;">
                <div class="team-avatar" style="margin-bottom:0; height:2.25rem; width:2.25rem;"><span style="font-size:1rem;">{p['name'][0]}</span></div>
                <span style="font-family:var(--font-display); font-size:1rem; font-weight:600; color:var(--cotton);">{p['name']}</span>
              </div>
              <div class="team-links">
                <a href="tel:{p['phone']}">{icon("phone", 12)}{p['phoneDisplay']}</a>
                {email_line}
                {wa_line}
              </div>
            </div>
            '''

    office_label = OFFICE['label'] if lang == 'en' else 'Kantor Pusat'
    offices_html = f'''<div class="office-card">
              {icon("map-pin", 14)}
              <div>
                <p class="label">{office_label}</p>
                <p>{OFFICE['address']}</p>
                <a href="{OFFICE['mapUrl']}" target="_blank" rel="noopener noreferrer">{'View on map →' if lang == 'en' else 'Lihat di peta →'}</a>
              </div>
            </div>'''

    sidebar = f'''<div class="contact-sidebar" data-animate="fade-right">
          <div class="wa-box">
            <p class="label" data-i18n="contact.direct.heading"></p>
            <a href="{wa_url}" target="_blank" rel="noopener noreferrer" class="btn" style="background:#25D366; color:#fff; width:100%;">
              {icon("whatsapp", 18)}<span data-i18n="contact.direct.whatsapp"></span>
            </a>
            <p class="note">{wa_note}</p>
          </div>
          <div style="margin-top:2rem;">
            <h2 class="sidebar-title">{our_team_label}</h2>
            <div style="display:flex; flex-direction:column; gap:1rem;">
              {persons_html}
            </div>
          </div>
          <div style="margin-top:2rem;">
            <h2 class="sidebar-title" data-i18n="contact.offices.heading"></h2>
            <div style="display:flex; flex-direction:column; gap:1rem;">
              {offices_html}
            </div>
          </div>
        </div>'''

    main_section = f'''<section class="section section-alt">
    <div class="container-site">
      <div class="contact-grid">
        <div data-animate="fade-left">
          {form_html}
        </div>
        {sidebar}
      </div>
    </div>
  </section>'''

    body = hero + "\n" + main_section
    emailjs_sdk = f'<script src="https://cdn.jsdelivr.net/npm/@emailjs/browser@4/dist/email.min.js"></script>\n<script src="{rel_prefix(slug)}js/form.js"></script>'
    return layout(lang, slug, MSG[lang]["metadata.contactTitle"], MSG[lang]["metadata.contactDescription"], body, extra_scripts=emailjs_sdk)

# ------------------------------------------------------------------
# LEGAL PAGES — text ported verbatim from src/app/[locale]/*/page.tsx
# These pages are English-only in the original source regardless of
# locale (no next-intl t() calls in their JSX) — reproduced exactly,
# with only the surrounding chrome (header/nav/footer) translated.
# Privacy Policy additionally shows an Indonesian-language notice
# banner on the /id/ version, exactly as in the source.
# ------------------------------------------------------------------
LEGAL_EFFECTIVE_DATE = "1 July 2026"

def legal_wrapper(lang, slug, eyebrow, h1, updated_label, notice_html, sections_html):
    return f'''<div style="padding-top:7rem;">
    <div class="container-site container-md" style="padding-block:4rem;">
      <div class="legal-eyebrow">{eyebrow}</div>
      <h1 class="legal-title">{h1}</h1>
      <p class="legal-updated">{updated_label}: {LEGAL_EFFECTIVE_DATE}</p>
      {notice_html}
      <div class="legal-body">
        {sections_html}
      </div>
    </div>
  </div>'''

def build_privacy(lang):
    slug = "privacy-policy"
    inquiry_link = f'<a href="mailto:{INQUIRY_EMAIL}">{INQUIRY_EMAIL}</a>'
    notice = ""
    if lang == "id":
        notice = f'''<div class="legal-notice">
        Kebijakan ini tersedia dalam Bahasa Inggris. Untuk ringkasan dalam Bahasa Indonesia, hubungi {inquiry_link}.
      </div>'''
    sections = f'''<section>
          <h2>1. Who We Are</h2>
          <p>Active Global Impex ("we", "us", "our") is a commodity export company registered in India, headquartered at {OFFICE['address']}. This Privacy Policy describes how we handle personal data collected through our website at <a href="{SITE}">{SITE}</a>.</p>
        </section>
        <section>
          <h2>2. Data We Collect</h2>
          <p>When you submit an inquiry through our contact form, we collect:</p>
          <ul>
            <li>Full name</li>
            <li>Company or organisation name</li>
            <li>Email address</li>
            <li>Phone number</li>
            <li>Country of residence or business</li>
            <li>Product of interest and quantity</li>
            <li>Any additional information you choose to provide in the message field</li>
          </ul>
        </section>
        <section>
          <h2>3. How We Use Your Data</h2>
          <p>We use the information you provide solely to respond to your product inquiry and communicate about potential trade. We do not use your data for marketing without explicit consent, and we do not sell or share your personal data with third parties for commercial purposes.</p>
        </section>
        <section>
          <h2>4. Third-Party Processors</h2>
          <p>Your inquiry data is transmitted via <strong>EmailJS</strong> (emailjs.com). Our website is hosted on <strong>Cloudflare Pages</strong>. See <a href="https://www.emailjs.com/legal/privacy-policy/" target="_blank" rel="noopener noreferrer">EmailJS Privacy Policy</a> and <a href="https://www.cloudflare.com/privacypolicy/" target="_blank" rel="noopener noreferrer">Cloudflare Privacy Policy</a>.</p>
        </section>
        <section>
          <h2>5. Data Retention</h2>
          <p>Inquiry data is retained for the duration of any resulting business relationship and for up to 5 years thereafter, or as required by applicable Indian tax and trade law.</p>
        </section>
        <section>
          <h2>6. Your Rights &amp; Applicable Law</h2>
          <p>Active Global Impex processes personal data as a Data Fiduciary under India's <strong>Digital Personal Data Protection Act 2023 (DPDP Act)</strong>. If you are in the EEA, GDPR rights apply. If you are in Indonesia, PP 71/2019 applies. To exercise data rights or raise a grievance, contact {inquiry_link}. We respond within 30 days.</p>
        </section>
        <section>
          <h2>7. Cookies</h2>
          <p>This website does not use tracking cookies. Cloudflare may set a technical <code>__cf_bm</code> cookie for bot management, which expires within 30 minutes.</p>
        </section>
        <section>
          <h2>8. Changes to This Policy</h2>
          <p>We may update this policy from time to time. The date at the top reflects the most recent revision.</p>
        </section>
        <section>
          <h2>9. Contact</h2>
          <p><strong>Active Global Impex</strong><br>{OFFICE['address']}<br>{inquiry_link}</p>
        </section>'''
    eyebrow = "Legal" if lang == "en" else "Hukum"
    updated_label = "Last updated" if lang == "en" else "Terakhir diperbarui"
    body = legal_wrapper(lang, slug, eyebrow, "Privacy Policy", updated_label, notice, sections)
    return layout(lang, slug, "Privacy Policy | Active Global Impex",
                   "How Active Global Impex collects, uses, and protects personal data submitted via this website.", body)

def build_terms(lang):
    slug = "terms-of-use"
    inquiry_link = f'<a href="mailto:{INQUIRY_EMAIL}">{INQUIRY_EMAIL}</a>'
    sections = f'''<section>
          <h2>1. Acceptance of Terms</h2>
          <p>By accessing or using the website at {SITE} ("Site"), you agree to be bound by these Terms of Use. If you do not agree, please do not use this Site.</p>
        </section>
        <section>
          <h2>2. Purpose of the Site</h2>
          <p>This Site is a business-to-business (B2B) information and inquiry platform operated by Active Global Impex. It is intended for use by registered businesses, traders, and procurement professionals. It is not a consumer marketplace.</p>
        </section>
        <section>
          <h2>3. No Binding Offer</h2>
          <p>All product descriptions, specifications, HS codes, trade terms, and other information on this Site are for <strong>general reference and inquiry purposes only</strong>. Nothing on this Site constitutes a binding offer, contract, quotation, or warranty of any kind. All sales are subject to a separate written contract agreed between the parties.</p>
        </section>
        <section>
          <h2>4. Product Information Disclaimer</h2>
          <p>Product specifications, grades, and HS codes shown on this Site are indicative only and may vary by batch, season, supplier, and agreed contract terms. Buyers are responsible for verifying all specifications and applicable customs codes with their own advisers before entering into any transaction.</p>
        </section>
        <section>
          <h2>5. Intellectual Property</h2>
          <p>All content on this Site is the property of Active Global Impex or its licensors and is protected by applicable intellectual property law. You may not reproduce, distribute, or create derivative works without our prior written consent.</p>
        </section>
        <section>
          <h2>6. Limitation of Liability</h2>
          <p>To the fullest extent permitted by applicable law, Active Global Impex shall not be liable for any direct, indirect, incidental, or consequential loss arising from your use of this Site or reliance on information contained herein.</p>
        </section>
        <section>
          <h2>7. Governing Law</h2>
          <p>These Terms are governed by the laws of India. Any disputes shall be subject to the exclusive jurisdiction of the courts of Kutch, Gujarat, India.</p>
        </section>
        <section>
          <h2>8. Changes</h2>
          <p>We reserve the right to modify these Terms at any time. Continued use of the Site after changes are posted constitutes your acceptance of the revised Terms.</p>
        </section>
        <section>
          <h2>9. Contact</h2>
          <p>Questions regarding these Terms: {inquiry_link}</p>
        </section>'''
    eyebrow = "Legal" if lang == "en" else "Hukum"
    updated_label = "Last updated" if lang == "en" else "Terakhir diperbarui"
    body = legal_wrapper(lang, slug, eyebrow, "Terms of Use", updated_label, "", sections)
    return layout(lang, slug, "Terms of Use | Active Global Impex",
                   "Terms governing your use of the Active Global Impex website.", body)

def build_disclaimer(lang):
    slug = "disclaimer"
    inquiry_link = f'<a href="mailto:{INQUIRY_EMAIL}">{INQUIRY_EMAIL}</a>'
    sections = f'''<section>
          <h2>General</h2>
          <p>The information provided on this website by Active Global Impex is for general business inquiry purposes only. It does not constitute a binding offer, firm quotation, contract, representation, or warranty of any kind — express or implied.</p>
        </section>
        <section>
          <h2>Product Specifications</h2>
          <p>Product descriptions, grades, quality parameters, and other technical details shown on this website are indicative only. Actual specifications may vary by batch, season, origin, processing method, and the specific terms agreed between the parties in a written sales contract.</p>
          <p style="margin-top:1rem;">Buyers are responsible for conducting their own due diligence, including requesting certificates of analysis, samples, and inspection reports, before entering into any purchase agreement.</p>
        </section>
        <section>
          <h2>HS Codes</h2>
          <p>Harmonised System (HS) codes shown on this website are indicative reference codes only. HS code classifications may differ by country, jurisdiction, and the applicable edition of the HS nomenclature. Buyers must verify the correct HS codes with their customs broker or customs authority. Active Global Impex accepts no liability for incorrect customs classification based on codes shown on this website.</p>
        </section>
        <section>
          <h2>Trade and Payment Terms</h2>
          <p>References to trade terms (FOB, CIF, etc.) are indicative of terms that may be available, subject to negotiation. All terms are confirmed only in a written contract.</p>
        </section>
        <section>
          <h2>Export Markets</h2>
          <p>References to export markets on this website reflect general market areas served and do not imply specific buyer relationships or guaranteed availability. Export of certain products may be subject to Indian government export restrictions or licensing requirements in force at the time of shipment.</p>
        </section>
        <section>
          <h2>No Guarantee of Response Time</h2>
          <p>While we aim to respond to inquiries in a timely manner, we do not guarantee specific response times. Response times may vary depending on inquiry volume, business hours, and public holidays in India.</p>
        </section>
        <section>
          <h2>Contact</h2>
          <p>For clarification on any information shown on this website: {inquiry_link}</p>
        </section>'''
    eyebrow = "Legal" if lang == "en" else "Hukum"
    effective_label = "Effective date" if lang == "en" else "Tanggal berlaku efektif"
    body = legal_wrapper(lang, slug, eyebrow, "Disclaimer", effective_label, "", sections)
    return layout(lang, slug, "Disclaimer | Active Global Impex",
                   "Important disclaimer regarding product information, HS codes, and trade terms on this website.", body)

# ------------------------------------------------------------------
# 404 — English-only in the original source (root-level not-found.tsx,
# outside the [locale] segment, so it never receives a locale param)
# ------------------------------------------------------------------
def build_404():
    body = f'''<div class="notfound">
    <p class="eyebrow" style="justify-content:center;">404 · Page Not Found</p>
    <h1>Lost at Port</h1>
    <p>The page you're looking for has sailed off. Let's get you back on course.</p>
    <a href="/en/" class="btn btn-gold-outline">← Back to Home</a>
    <p class="brandmark">Active Global Impex</p>
  </div>'''
    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Page Not Found | Active Global Impex</title>
<meta name="robots" content="noindex, follow">
<link rel="icon" href="/icons/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@600;700&family=Inter:wght@400;500&family=IBM+Plex+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/styles.css">
<link rel="stylesheet" href="/css/animations.css">
</head>
<body>
{body}
</body>
</html>'''
    return html

# ------------------------------------------------------------------
# WRITE ALL FILES
# ------------------------------------------------------------------
def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(content)

BUILDERS = {
    "index": build_home,
    "about": build_about,
    "products": build_products,
    "contact": build_contact,
    "privacy-policy": build_privacy,
    "terms-of-use": build_terms,
    "disclaimer": build_disclaimer,
}

def generate_pages():
    count = 0
    for lang in ("en", "id"):
        for key, slug in ROUTES:
            html = BUILDERS[key](lang)
            out_path = f"{lang}/index.html" if slug == "" else f"{lang}/{slug}/index.html"
            write(out_path, html)
            count += 1
    write("404.html", build_404())
    count += 1
    print(f"Generated {count} HTML pages")

if __name__ == "__main__":
    generate_pages()
