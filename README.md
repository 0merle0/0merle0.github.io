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

## Instagram sync

`.github/workflows/sync-instagram.yml` runs `scripts/sync_instagram.py` every Monday
(or on demand from the Actions tab). It pulls the 30 most recent posts from
@__almondz__ into `images/almondz/ig/` and rewrites the collage in `almondz.html`
between the `GALLERY START` / `GALLERY END` markers. Don't hand-edit between them.
The job skips itself until `INSTAGRAM_TOKEN` is set.

Because the bot commits to `main`, run `git pull` before editing locally.

One-time setup:

1. Make the Instagram account a professional account (Instagram app → Settings →
   Account type and tools → Switch to professional account → Creator).
2. At https://developers.facebook.com create an app of type **Business** and add the
   **Instagram** product.
3. In the app dashboard: Instagram → **API setup with Instagram business login** →
   **Generate token** next to @__almondz__, log in, and copy the token (valid 60 days).
4. In this repo on GitHub: Settings → Secrets and variables → Actions →
   **New repository secret** named `INSTAGRAM_TOKEN` with that token.
5. Create a fine-grained personal access token (GitHub → Settings → Developer
   settings → Fine-grained tokens) limited to this repository with
   **Secrets: Read and write** permission, and save it as a secret named
   `GH_SECRETS_TOKEN`. The workflow uses it to store the refreshed Instagram token.
   Fine-grained tokens expire too; pick the longest expiry you're comfortable with.
6. Actions tab → **Sync Instagram** → **Run workflow** to do the first sync.

Each run refreshes the Instagram token, so as long as the job runs at least once
every 60 days it stays valid.
