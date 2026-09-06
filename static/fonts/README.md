# Vazirmatn

`main.css` declares the face twice: the self-hosted file first, jsDelivr as a
fallback. Serve it yourself — Google Fonts and several CDNs are slow or blocked
for visitors inside Iran, and a webfont that fails to load costs you the whole
typographic identity.

Download the variable font into this folder:

```bash
curl -L -o "static/fonts/Vazirmatn[wght].woff2" \
  https://cdn.jsdelivr.net/npm/vazirmatn@33.0.3/fonts/webfonts/Vazirmatn%5Bwght%5D.woff2
```

One variable file covers weights 100–900, so there is nothing else to fetch.
After `collectstatic`, WhiteNoise/Nginx serve it with the same one-year
immutable cache header as the rest of the static tree.

If you prefer Persian numerals to render as ۰۱۲۳ everywhere without the JS
converter in `main.js`, use the `Farsi-Digits` build instead:
`vazirmatn@33.0.3/misc/Farsi-Digits/fonts/webfonts/Vazirmatn-FD[wght].woff2`
