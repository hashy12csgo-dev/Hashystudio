"""
Builds the GitHub Pages version of the HASAN portfolio.

You never need to run this yourself: GitHub runs it automatically every time
you upload or change something (see .github/workflows/pages.yml).

What it does:
  * Reads template.html (the website design).
  * Finds every video in the videos/ folder. Folder name = category,
    file name = title, same-named .jpg/.png = thumbnail. A video inside
    videos/_Showreel becomes the big Brand Explainer video.
  * Writes the finished website to the _site/ folder, together with the videos.

To test it on your own computer:  python build_site.py   then open _site/index.html
"""

import json
import re
import shutil
import sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).parent
VIDEOS_DIR = ROOT / "videos"
TEMPLATE = ROOT / "template.html"
OUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "_site"

SHOWREEL_FOLDER = "_Showreel"
# Filter buttons appear in this order. Any new folder you create is added after these.
CATEGORY_ORDER = [
    "Commercial Ads",
    "Product Videos",
    "Social Media",
    "Brand Films",
    "YouTube",
    "Motion Graphics",
]
VIDEO_EXTS = {".mp4", ".webm", ".m4v", ".mov"}
IMAGE_EXTS = [".jpg", ".jpeg", ".png", ".webp"]
CARD_GRADIENTS = [
    "linear-gradient(135deg,#241636,#120a1e)",
    "linear-gradient(135deg,#1c2a45,#0a1120)",
    "linear-gradient(135deg,#1e2438,#0a0d18)",
    "linear-gradient(135deg,#2a1c38,#100a1a)",
]
NUMBER_PREFIX = re.compile(r"^\s*(\d+)\s*[-_.)]?\s*")


def file_url(path: Path) -> str:
    """Relative link, so the site works at any address (github.io or your own domain)."""
    return "/".join(quote(p) for p in path.relative_to(ROOT).parts)


def title_and_order(stem: str) -> tuple[str, int]:
    """'03 - Bliss Splash' -> ('Bliss Splash', 3). No number -> goes to the end."""
    match = NUMBER_PREFIX.match(stem)
    if match and match.group(1) and match.end() < len(stem):
        return stem[match.end():].replace("_", " ").strip(), int(match.group(1))
    return stem.replace("_", " ").strip(), 1_000_000


def find_thumbnail(video: Path) -> Path | None:
    for ext in IMAGE_EXTS:
        for candidate in (video.with_suffix(ext), video.with_suffix(ext.upper())):
            if candidate.exists():
                return candidate
    return None


def videos_in(folder: Path) -> list[Path]:
    return sorted(
        (p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in VIDEO_EXTS),
        key=lambda p: (title_and_order(p.stem)[1], p.name.lower()),
    )


def scan():
    projects, categories, showreel = [], [], None
    if not VIDEOS_DIR.exists():
        return projects, categories, showreel

    folders = [f for f in VIDEOS_DIR.iterdir() if f.is_dir() and not f.name.startswith(".")]
    rank = {name.lower(): i for i, name in enumerate(CATEGORY_ORDER)}
    folders.sort(key=lambda f: (rank.get(f.name.lower(), len(rank)), f.name.lower()))

    for folder in folders:
        files = videos_in(folder)
        if not files:
            continue
        if folder.name.lower() == SHOWREEL_FOLDER.lower():
            video = files[0]
            thumb = find_thumbnail(video)
            showreel = {
                "title": title_and_order(video.stem)[0],
                "video": file_url(video),
                "poster": file_url(thumb) if thumb else "",
            }
            continue
        categories.append(folder.name)
        for video in files:
            title, order = title_and_order(video.stem)
            thumb = find_thumbnail(video)
            projects.append({
                "title": title,
                "cat": folder.name,
                "video": file_url(video),
                "poster": file_url(thumb) if thumb else "",
                "order": order,
            })

    projects.sort(key=lambda p: p["order"])  # stable: same number keeps category order
    for i, p in enumerate(projects):
        p["grad"] = CARD_GRADIENTS[i % len(CARD_GRADIENTS)]
    return projects, categories, showreel


def to_js(value) -> str:
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


def html_attr(value: str) -> str:
    return (value.replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))


def build_page() -> str:
    projects, categories, showreel = scan()
    page = TEMPLATE.read_text("utf-8")

    if showreel:
        poster = f' poster="{html_attr(showreel["poster"])}"' if showreel["poster"] else ""
        page = (page.replace("__SHOWREEL_SRC__", html_attr(showreel["video"]))
                    .replace("__SHOWREEL_POSTER_ATTR__", poster)
                    .replace("__SHOWREEL_TITLE__", html_attr(showreel["title"])))
    else:
        page = re.sub(r"<!--SHOWREEL_START-->.*?<!--SHOWREEL_END-->", "", page, flags=re.S)

    page = (page.replace("__PROJECTS_JSON__", to_js(projects))
                .replace("__CATEGORIES_JSON__", to_js(categories)))
    return page, projects, showreel


def main():
    page, projects, showreel = build_page()
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)
    (OUT / "index.html").write_text(page, "utf-8")
    (OUT / ".nojekyll").write_text("")  # serve folders starting with _ (like _Showreel) as-is
    if VIDEOS_DIR.exists():
        shutil.copytree(VIDEOS_DIR, OUT / "videos")
    print(f"Built {OUT / 'index.html'}: {len(projects)} videos"
          f"{' + showreel' if showreel else ''}.")


if __name__ == "__main__":
    main()
