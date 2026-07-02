# Active Global Impex — Static Site

A pure HTML / CSS / JavaScript rebuild of the Active Global Impex marketing
site (originally a Next.js + next-intl + Tailwind + Framer Motion project).
No build step, no npm, no framework runtime — every file here is exactly
what gets deployed.

The content (copy, product catalogue, HS codes, legal text, contact details,
brand colours/fonts) is ported 1:1 from the original project's source files
(`messages/en.json`, `messages/id.json`, `src/config/site.ts`,
`src/app/[locale]/*/page.tsx`, `tailwind.config.ts`).

## File structure

```
/                       root redirect -> /en/
├── index.html
├── _headers            Cloudflare Pages response headers (security + caching)
├── _redirects          Cloudflare Pages redirect rules (www→apex, legacy paths)
├── robots.txt
├── sitemap.xml          8 URLs: {home,about,products,contact} × {en,id}
├── manifest.json
├── css/
│   ├── styles.css        design tokens + layout + components ("Kutch Earth" palette)
│   └── animations.css    IntersectionObserver-driven reveal classes + keyframes
├── js/
│   ├── i18n.js            EN/ID translation dictionary + data-i18n applier
│   ├── main.js            header scroll, mobile drawer, ticker, tabs, reveals, WhatsApp float
│   └── form.js            contact form validation + EmailJS submission
├── icons/
│   ├── favicon.svg
│   ├── icon-192.png
│   └── icon-512.png
├── images/
│   └── og-cover.jpg      Open Graph / Twitter card image
├── en/                   English pages
│   ├── index.html
│   ├── about/index.html
│   ├── products/index.html
│   ├── contact/index.html
│   ├── privacy-policy/index.html
│   ├── terms-of-use/index.html
│   └── disclaimer/index.html
├── id/                   Bahasa Indonesia pages (same 7 routes)
├── 404.html
└── tools/                reference only — the Python generator used to
    ├── build.py             build every HTML page from the ported content.
    ├── en_flat.json         Not required for deployment; delete this folder
    └── id_flat.json         if you don't plan to regenerate pages.
```

Everything **outside** `tools/` is the deployable site.

## How the pages are built

Rather than hand-duplicating near-identical markup across 14 files, all
pages share `js/i18n.js` for translated UI strings (header, footer, buttons,
form labels, page copy) via `data-i18n="key.path"` attributes — the key
paths match the original `messages/en.json` / `messages/id.json` structure
exactly. Page-unique structural content (product cards, team cards, legal
text) is written directly into each language's HTML file.

**Legal pages (Privacy Policy, Terms of Use, Disclaimer) are English-only
in both `/en/` and `/id/`** — this matches the original source exactly,
which never ran that copy through `next-intl`'s translator. The Indonesian
Privacy Policy page shows a small notice banner pointing readers to email
for a summary, exactly as in the source.

## ⚠️ Before deploying — configuration checklist

1. **EmailJS credentials** (`js/form.js`, top of file):
   ```js
   var EMAILJS_SERVICE_ID = "service_xxxxxxx";
   var EMAILJS_TEMPLATE_ID = "template_xxxxxxx";
   var EMAILJS_PUBLIC_KEY = "xxxxxxxxxxxxxxxx";
   ```
   These are placeholders — exactly as they were in the original project's
   `.env.example` (`NEXT_PUBLIC_EMAILJS_SERVICE_ID` etc. were never checked
   in with real values either). Sign up at [emailjs.com](https://www.emailjs.com/),
   create a service + template, and paste in your real IDs. The template
   must accept these variables: `{{from_name}} {{from_email}} {{phone}}
   {{company}} {{country}} {{product}} {{quantity}} {{message}} {{to_email}}`.
   Until configured, the form will validate correctly but show a "something
   went wrong" error on submit (with a console warning) instead of silently
   failing.

2. **Contact details** — real values already ported from the source
   (`src/config/site.ts`): Lokesh / Feroz / Javed's phone numbers and
   emails, the Gandhidham office address, and the WhatsApp CTA number
   (+91 84601 73319). Update `tools/build.py`'s `PERSONS` / `OFFICE`
   constants (and regenerate) if any of these change.

3. **Domain** — all canonical URLs, `sitemap.xml`, `robots.txt`, and
   `_redirects` assume `https://activeglobalimpex.com`. Update `SITE` in
   `tools/build.py` and regenerate, or find-and-replace across the static
   files, if the domain differs.

4. **OG image / icons** are simple generated placeholders (brand colours,
   no photography). Swap `images/og-cover.jpg`, `icons/icon-192.png`, and
   `icons/icon-512.png` for real designed assets when available.

## Deploying to Cloudflare Pages

**Option A — dashboard upload (no build step)**
1. Cloudflare dashboard → Workers & Pages → Create → Pages → *Upload assets*.
2. Upload this entire folder (everything except `tools/`, which is optional).
3. Framework preset: **None**. Build command: *(leave blank)*. Output
   directory: `/`.
4. Deploy. `_headers` and `_redirects` are picked up automatically.

**Option B — Git integration**
1. Push this folder to a GitHub/GitLab repo.
2. Cloudflare dashboard → Workers & Pages → Create → Pages → *Connect to Git*.
3. Build command: *(leave blank)* — Output directory: `/`.
4. Deploy on every push.

**Option C — Wrangler CLI**
```bash
npx wrangler pages deploy . --project-name=active-global-impex
```
(`npx` here just fetches the Wrangler CLI itself — the site remains a
zero-build static deploy; no bundler ever touches these files.)

After deploying, add your custom domain in the Pages project's
**Custom domains** tab and confirm `_redirects`' `www → apex` rule matches
whichever you set as canonical.

## Local preview

Any static file server works, e.g.:
```bash
python3 -m http.server 8080
# then open http://localhost:8080/en/
```

## Lighthouse / performance notes

- Fonts load via `<link rel=preconnect>` + Google Fonts `display=swap`.
- No JS framework runtime; `js/*.js` totals a few KB, no build/minify step
  is required but you may minify before deploy if you want a few extra
  points on Lighthouse's "unused JavaScript" audit.
- All animation is CSS transitions triggered by one shared
  `IntersectionObserver` in `js/main.js` — no animation library.
- Images are minimal (SVG logo mark, generated PNG icons, one JPG OG
  image) since the original project also shipped without photography
  (see `tools/` note above about swapping in real assets).
