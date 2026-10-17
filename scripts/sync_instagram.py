"""Sync recent Instagram posts into the almondz collage.

Fetches posts with the Instagram API (Instagram Login), downloads one image
per post into images/almondz/ig/, and rewrites the collage in almondz.html
between the GALLERY markers. Uses only the standard library.

Environment:
  INSTAGRAM_TOKEN   long-lived Instagram user access token (required)
  REFRESHED_TOKEN_FILE  optional path; the refreshed token is written here

Run from the repository root: python3 scripts/sync_instagram.py
"""

import html
import json
import os
import pathlib
import sys
import urllib.parse
import urllib.request

API = "https://graph.instagram.com"
VERSION = "v25.0"
MAX_POSTS = 30
BIG_EVERY = 7  # every 7th tile (starting with the first) is a 2x2 block

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "almondz.html"
IMG_DIR = ROOT / "images" / "almondz" / "ig"
START = "<!-- GALLERY START: filled in by scripts/sync_instagram.py -->"
END = "<!-- GALLERY END -->"


def get_json(url, params):
    query = urllib.parse.urlencode(params)
    with urllib.request.urlopen(f"{url}?{query}", timeout=30) as resp:
        return json.load(resp)


def refresh_token(token):
    """Extend the token's life by 60 days; returns the (possibly new) token."""
    try:
        data = get_json(f"{API}/refresh_access_token",
                        {"grant_type": "ig_refresh_token", "access_token": token})
        print(f"Token refreshed; expires in {data.get('expires_in', '?')} seconds.")
        return data.get("access_token", token)
    except Exception as e:  # A refresh failure shouldn't stop the sync itself.
        print(f"::warning::Token refresh failed: {e}")
        return token


def fetch_posts(token):
    fields = ("id,caption,media_type,media_url,thumbnail_url,permalink,timestamp,"
              "children{media_type,media_url,thumbnail_url}")
    url, params = f"{API}/{VERSION}/me/media", {"fields": fields, "limit": 50,
                                               "access_token": token}
    posts = []
    while url and len(posts) < MAX_POSTS:
        data = get_json(url, params)
        posts.extend(data.get("data", []))
        url, params = data.get("paging", {}).get("next"), {}
    return posts[:MAX_POSTS]


def image_url(post):
    """One still image per post: the photo, a video's thumbnail, or a carousel's first item."""
    item = post
    if post.get("media_type") == "CAROUSEL_ALBUM":
        children = post.get("children", {}).get("data", [])
        item = children[0] if children else post
    if item.get("media_type") == "VIDEO":
        return item.get("thumbnail_url")
    return item.get("media_url")


def download(url, dest):
    with urllib.request.urlopen(url, timeout=60) as resp:
        dest.write_bytes(resp.read())


def tile(i, post, filename):
    caption = (post.get("caption") or "").strip()
    first_line = caption.splitlines()[0] if caption else ""
    alt = html.escape(first_line[:120] or "almondz project", quote=True)
    big = ' class="big"' if i % BIG_EVERY == 0 else ""
    return (f'    <a{big} href="{html.escape(post["permalink"], quote=True)}">'
            f'<img src="images/almondz/ig/{filename}" alt="{alt}" loading="lazy"></a>')


def main():
    token = os.environ.get("INSTAGRAM_TOKEN", "").strip()
    if not token:
        print("::notice::INSTAGRAM_TOKEN is not set; skipping Instagram sync.")
        return

    new_token = refresh_token(token)
    if out := os.environ.get("REFRESHED_TOKEN_FILE"):
        pathlib.Path(out).write_text(new_token)

    posts = fetch_posts(new_token)
    IMG_DIR.mkdir(parents=True, exist_ok=True)

    tiles, keep = [], set()
    for post in posts:
        url = image_url(post)
        if not url or not post.get("permalink"):
            continue
        filename = f"{post['id']}.jpg"
        dest = IMG_DIR / filename
        if not dest.exists():  # Instagram images don't change once posted.
            download(url, dest)
        keep.add(filename)
        tiles.append(tile(len(tiles), post, filename))

    # Remove images for posts that were deleted or fell out of the window.
    for old in IMG_DIR.glob("*.jpg"):
        if old.name not in keep:
            old.unlink()

    if tiles:
        body = '  <div class="collage">\n' + "\n".join(tiles) + "\n  </div>"
    else:
        body = "  <p>Under construction. Check back soon!</p>"

    page = PAGE.read_text()
    if START not in page or END not in page:
        sys.exit(f"Gallery markers not found in {PAGE.name}")
    before, rest = page.split(START, 1)
    _, after = rest.split(END, 1)
    PAGE.write_text(f"{before}{START}\n{body}\n  {END}{after}")
    print(f"Collage updated with {len(tiles)} posts.")


if __name__ == "__main__":
    main()
