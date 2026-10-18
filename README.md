# jacobgershon.com

Plain HTML/CSS personal site served by GitHub Pages. No build step.

- `index.html` — home page: bio, experience (with the CV PDF link) and contact
- `publications.html` — publications and talks
- `almondz.html` — the Centurion Bag and its order form; photos go in `images/almondz/`
- `style.css` — shared styles
- `cv/` — LaTeX source for the resume; build with `cd cv && pdflatex main.tex`, then copy `main.pdf` to `files/cv.pdf`
- `files/` — downloadable files (`cv.pdf`)

The menu bar is copied into the top of every page, so update all of them when adding a link.

Preview locally: `python3 -m http.server` then open http://localhost:8000

## almondz orders

The order form on `almondz.html` posts to FormSubmit (https://formsubmit.co), which
emails each request to almondzmail@gmail.com and then sends the visitor to
`thanks.html`. The first submission triggers a one-time activation email to that
inbox; click the link in it, or no orders get delivered.

GitHub Pages serves the `gh-pages` branch; `.github/workflows/mirror-gh-pages.yml`
copies `main` onto it on every push.
