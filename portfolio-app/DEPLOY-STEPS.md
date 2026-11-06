# Website ko GitHub + Streamlit pr live karna

Ye sab ek hi dafa karna hai. Uske baad nayi videos sirf GitHub pr upload hongi (dekhein `HOW-TO-ADD-VIDEOS.md`).

---

## Step 0 — Pehle bari videos chhoti karein (zaroori)

GitHub **100 MB** se bari file bilkul accept nahi karta, aur website pr bari videos slow chalti hain.
In files ko HandBrake se compress karein (tareeqa `HOW-TO-ADD-VIDEOS.md` ke aakhir mein hai), aur compress wali file ko **usi naam** se wapis usi folder mein rakh dein:

| File | Abhi size | |
|---|---|---|
| `Product Videos/01 - LANOIR Cream ... .mp4` | 176 MB (4K) | ❌ 100 MB se bari — compress lazmi |
| `_Showreel/HASAN - Product Video Ads.mp4` | 158 MB | ❌ compress lazmi |
| `Product Videos/02 - Lanoir Serum.mp4` | 112 MB (4K) | ❌ compress lazmi |
| `Brand Films/08 - STORYTELLING.mp4` | 75 MB | ⚠️ compress behtar |
| `Social Media/09 - General Waste Collection.mp4` | 64 MB | ⚠️ |
| `Motion Graphics/07 - 2D Explainer Video Service.mp4` | 56 MB | ⚠️ |
| `Commercial Ads/04 - Flexive ... .mp4` | 51 MB | ⚠️ |
| `Commercial Ads/03 - Bliss Splash ... .mp4` | 47 MB | ⚠️ |
| `Social Media/10 - What Happens To Your Glass Waste.mp4` | 32 MB | ⚠️ |

Target: har video **25 MB se kam**. Original files `D:\WEBSITE\assets\video` mein safe hain.

---

## Step 1 — GitHub account aur repository

1. github.com pr account banayein (agar nahi hai).
2. Upar right **+ → New repository**.
3. Naam: `portfolio-app` · **Public** select karein (zaroori — videos isi se load hoti hain) · **Create repository**.

## Step 2 — Files GitHub pr daalna (GitHub Desktop se — sab se aasaan)

1. **GitHub Desktop** install karein (desktop.github.com) aur apne account se login karein.
2. **File → Add local repository** → folder chunein: `D:\WEBSITE\portfolio-app`.
   Agar likha aaye "this directory does not appear to be a Git repository" to **create a repository** pr click karein → **Create repository**.
3. Left side pr sari files dikhengi. Neeche Summary mein likhein `First upload` → **Commit to main**.
4. Upar **Publish repository** dabayein. "Keep this code private" ka tick **hata dein** → **Publish**.
   Agar repository Step 1 mein pehle bana chuke hain to naam same rakhein, ya Step 1 skip kar dein — GitHub Desktop khud bana dega.

## Step 3 — `settings.toml` mein apna naam likhna

GitHub pr wo folder kholein jis mein `app.py` hai, browser ke upar wala link copy karein. Phir `settings.toml` → ✏️ (Edit) button:

```toml
github_link = "https://github.com/APNA-USERNAME/REPO/tree/main/portfolio-app"
```

**Commit changes** dabayein. (Isi se website ko pata chalta hai videos kahan se uthani hain.)

## Step 4 — Streamlit pr deploy

1. share.streamlit.io kholein → **Continue with GitHub** se login karein (GitHub ko permission dein).
2. **Create app → Deploy a public app from GitHub**.
3. Repository: `APNA-USERNAME/portfolio-app` · Branch: `main` · Main file path: `app.py`.
4. **App URL** mein apni pasand ka naam likhein (maslan `hasan-portfolio` → `hasan-portfolio.streamlit.app`).
5. **Deploy** dabayein. 2–3 minute mein website live ho jayegi.

---

## Iske baad

* **Nayi video**: GitHub website pr category folder mein upload karein → 1–2 minute mein live. (`HOW-TO-ADD-VIDEOS.md`)
* **Text badalna** (About, Services, Testimonials, email): `template.html` mein wo text dhoond kar edit karein.
* Free Streamlit app kuch din koi na khole to "sleep" ho jati hai; pehla visitor "Yes, get this app back up" dabata hai to 30 second mein wapis chal parti hai.

## Apne computer pr chala kar dekhna (optional)

```bash
cd D:\WEBSITE\portfolio-app
```

```bash
python -m streamlit run app.py
```

Jab tak `settings.toml` mein `github_repo` khali hai, videos aap ke computer se hi chalti hain. Naam likhne ke baad GitHub se.
