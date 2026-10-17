# jacobgershon.com

Plain HTML/CSS personal site served by GitHub Pages. No build step.

- `index.html` — home page with a short bio and contact links
- `publications.html`, `cv.html` — one page each
- `almondz.html` — art gallery; photos go in `images/almondz/`
- `style.css` — shared styles
- `cv/` — LaTeX source for the resume; build with `cd cv && pdflatex main.tex`, then copy `main.pdf` to `files/cv.pdf`
- `files/` — downloadable files (`cv.pdf`)

The menu bar is copied into the top of every page, so update all of them when adding a link.

Preview locally: `python3 -m http.server` then open http://localhost:8000
