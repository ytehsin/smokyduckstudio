# Editing the smokyDuck site

Folders starting with `_` are not published.

| To change | Edit |
|---|---|
| WhatsApp number, form endpoint, Google Analytics, social links | `assets/js/config.js` |
| Voices | `data/artists.json` (shown only when `published` and `consentOnFile` are true; `example` profiles never show) |
| Work samples | `data/portfolio.json` (`kind`: video with `embed`, or audio with `audio`; `featured: true` = on the home page) |
| Page text | the page's .html file, or `_tools/build.py` then `python3 build.py` |

Pages: index, services, voices, work, contact, legal (privacy + terms), 404.

Samples point to the renamed copies in Drive ▸ "smokyDuck — Website samples (renamed copies)". Each file must be shared as "Anyone with the link: Viewer" to play on the site.

Deploy: upload everything to the GitHub repo ytehsin/smokyduckstudio (replace the old index.html). The old page is in `_guides/backup/` and in git history.
