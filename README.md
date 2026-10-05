# stuetz.wiki

Static wiki for [stuetz.wiki](https://stuetz.wiki), built from `content/*.md` and deployed to GitHub Pages by `.github/workflows/pages.yml` on every push to `main`.

- **Add or edit an article:** create or change `content/<Title>.md` (spaces as `_`). The article format and markup are described at the top of `build.py`.
- **Navigation boxes:** `content/_navboxes.toml`.
- **Build locally:** `python3 build.py` (Python 3.11+, no dependencies) writes the site to `_site/`.
