"""
HASAN portfolio website — Streamlit app.

How it works:
  * The website design lives in template.html.
  * Every video inside the videos/ folder is found automatically.
    The folder name is the category, the file name is the title.
  * Videos are played straight from your GitHub repository, so adding a
    video = uploading it to GitHub. No code changes needed.
    (See HOW-TO-ADD-VIDEOS.md.)
"""

import functools
import http.server
import json
import re
import threading
from pathlib import Path
from urllib.parse import quote

import streamlit as st
import streamlit.components.v1 as components

ROOT = Path(__file__).parent
VIDEOS_DIR = ROOT / "videos"
TEMPLATE = ROOT / "template.html"
SETTINGS = ROOT / "settings.toml"

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


st.set_page_config(
    page_title="HASAN — Video Editor & Animation Artist",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ---------------------------------------------------------------- where videos load from
def read_setting(name: str) -> str:
    """Read `name = "value"` from settings.toml (kept dead simple on purpose)."""
    if not SETTINGS.exists():
        return ""
    match = re.search(rf'^\s*{name}\s*=\s*"([^"]*)"', SETTINGS.read_text("utf-8"), re.M)
    return match.group(1).strip() if match else ""


def repo_from_git() -> tuple[str, str]:
    """Fallback: work out "owner/repo" and the branch from the local .git folder."""
    git = ROOT / ".git"
    try:
        config = (git / "config").read_text("utf-8")
        url = re.search(r'\[remote "origin"\][^\[]*?url\s*=\s*(\S+)', config, re.S).group(1)
        repo = re.search(r"github\.com[:/](.+?)(?:\.git)?/?$", url).group(1)
        head = (git / "HEAD").read_text("utf-8").strip()
        branch = head.rsplit("/", 1)[-1] if head.startswith("ref:") else "main"
        return repo, branch
    except (OSError, AttributeError):
        return "", ""


@st.cache_resource
def local_file_server() -> str:
    """For testing on your own computer before anything is on GitHub."""

    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass

    handler = functools.partial(QuietHandler, directory=str(ROOT))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{server.server_address[1]}"


def media_base_url() -> str:
    repo = read_setting("github_repo")
    branch = read_setting("github_branch") or "main"
    if not repo:
        repo, git_branch = repo_from_git()
        branch = read_setting("github_branch") or git_branch or "main"
    if repo:
        return f"https://raw.githubusercontent.com/{repo}/{branch}"
    return local_file_server()


def file_url(base: str, path: Path) -> str:
    parts = path.relative_to(ROOT).parts
    return base + "/" + "/".join(quote(p) for p in parts)


# ---------------------------------------------------------------- scan the videos folder
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


def scan(base: str):
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
                "video": file_url(base, video),
                "poster": file_url(base, thumb) if thumb else "",
            }
            continue
        categories.append(folder.name)
        for video in files:
            title, order = title_and_order(video.stem)
            thumb = find_thumbnail(video)
            projects.append({
                "title": title,
                "cat": folder.name,
                "video": file_url(base, video),
                "poster": file_url(base, thumb) if thumb else "",
                "order": order,
            })

    projects.sort(key=lambda p: p["order"])  # stable: same number keeps category order
    for i, p in enumerate(projects):
        p["grad"] = CARD_GRADIENTS[i % len(CARD_GRADIENTS)]
    return projects, categories, showreel


# ---------------------------------------------------------------- build the page
def to_js(value) -> str:
    return json.dumps(value, ensure_ascii=False).replace("</", "<\\/")


def html_attr(value: str) -> str:
    return (value.replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))


def build_page() -> str:
    base = media_base_url()
    projects, categories, showreel = scan(base)
    page = TEMPLATE.read_text("utf-8")

    if showreel:
        poster = f' poster="{html_attr(showreel["poster"])}"' if showreel["poster"] else ""
        page = (page.replace("__SHOWREEL_SRC__", html_attr(showreel["video"]))
                    .replace("__SHOWREEL_POSTER_ATTR__", poster)
                    .replace("__SHOWREEL_TITLE__", html_attr(showreel["title"])))
    else:
        page = re.sub(r"<!--SHOWREEL_START-->.*?<!--SHOWREEL_END-->", "", page, flags=re.S)

    return (page.replace("__PROJECTS_JSON__", to_js(projects))
                .replace("__CATEGORIES_JSON__", to_js(categories)))


# Make the site fill the whole browser window and hide Streamlit's own menus.
st.markdown(
    """
    <style>
      header[data-testid="stHeader"], [data-testid="stToolbar"], [data-testid="stDecoration"],
      [data-testid="stStatusWidget"], #MainMenu, footer { display: none !important; }
      html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
        background: #050505 !important; overflow: hidden !important;
      }
      .block-container, [data-testid="stMainBlockContainer"] {
        padding: 0 !important; max-width: 100% !important;
      }
      [data-testid="stVerticalBlock"] { gap: 0 !important; }
      [data-testid="stElementContainer"]:has(> .stMarkdown style),
      .element-container:has(style) { display: none !important; }
      iframe { display: block; width: 100% !important; border: 0;
               height: 100vh !important; height: 100dvh !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

components.html(build_page(), height=900, scrolling=True)
