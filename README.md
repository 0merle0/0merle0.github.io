# jacobgershon.com

Plain HTML/CSS personal site served by GitHub Pages. No build step.

- `index.html` — home page: bio, experience (with the CV PDF link) and contact
- `publications.html` — publications and talks
- `almondz.html` — the Centurion Bag (order by email); photos go in `images/almondz/`
- `style.css` — shared styles
- `cv/` — LaTeX source for the resume; build with `cd cv && pdflatex main.tex`, then copy `main.pdf` to `files/cv.pdf`
- `files/` — downloadable files (`cv.pdf`)

The menu bar is copied into the top of every page, so update all of them when adding a link.

Preview locally: `python3 -m http.server` then open http://localhost:8000

## almondz orders

The almondz page lists almondzmail@gmail.com for anyone who wants a bag; orders are
worked out over email.

GitHub Pages serves the `gh-pages` branch; `.github/workflows/mirror-gh-pages.yml`
copies `main` onto it on every push.
