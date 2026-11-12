# bhutanirealtors.in

Source for the Bhutani Realtors website, served free by GitHub Pages from the `docs/` folder.

## Updating the site

1. Edit a page in `content/<url-slug>.md` (first line `# Page title`). Weekly news goes at the top of `content/property-pulse.md` as a new `## Gurugram Property Pulse — <date>: <headline>` section; the home page teaser picks up the newest one automatically.
2. Page SEO titles and descriptions live in `pages.json`; gallery photos and contact details in `build.py`.
3. Run `python3 build.py` (needs `pip install markdown`). This regenerates `docs/`, including `sitemap.xml` and `llms.txt`.
4. Commit and push to `main`. GitHub Pages publishes in about a minute.

Photos in `docs/assets/img/` are of the Emaar Marbella community and our own site at Plot 21.
