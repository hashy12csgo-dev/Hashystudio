# Nayi video website pr kaise lagayein (bina coding ke)

Code ko haath lagane ki zaroorat **nahi**. Bas GitHub pr video upload karein, 1–2 minute mein website pr aa jayegi.

## Folder = Category

`videos` folder ke andar har folder ek category hai (website pr filter button):

| Folder | Website pr |
|---|---|
| `videos/Commercial Ads` | Commercial Ads |
| `videos/Product Videos` | Product Videos |
| `videos/Social Media` | Social Media |
| `videos/Brand Films` | Brand Films |
| `videos/YouTube` | YouTube |
| `videos/Motion Graphics` | Motion Graphics |
| `videos/_Showreel` | Upar wali bari "Brand Showreel" video (sirf 1 video rakhein) |

Jis folder mein video hogi, wahi category ka button dikhega. Khali folder ka button nahi dikhta.

## File ka naam = Title

```
11 - Nike Shoes Commercial.mp4
```

* `11 - ` number se order tay hota hai (chhota number pehle). Number website pr nazar **nahi** aata.
* Number na lagayein to video list ke aakhir mein aayegi.
* Baqi naam (`Nike Shoes Commercial`) website pr title ban jata hai.

## Thumbnail (optional)

Video ke **bilkul same naam** ki image usi folder mein daal dein:

```
11 - Nike Shoes Commercial.mp4
11 - Nike Shoes Commercial.jpg     <- thumbnail
```

`.jpg`, `.png`, `.webp` sab chalti hain. Thumbnail na ho to video ka pehla frame khud dikh jata hai.

Vertical (9:16 reels) videos khud pehchani jati hain — kuch karne ki zaroorat nahi.

## GitHub website se upload karna (step by step)

1. github.com pr login karein aur apni repository kholein.
2. `videos` folder pr click karein, phir category folder (maslan `Social Media`) pr click karein.
3. Upar right pr **Add file → Upload files** dabayein.
4. Video (aur thumbnail) drag karke daal dein.
5. Neeche **Commit changes** (hara button) dabayein.
6. 1–2 minute baad website refresh karein — video aa chuki hogi.

### Video hatani ho
Video file kholein → upar right `...` menu → **Delete file** → **Commit changes**.

### Nayi category banani ho
`videos` folder mein **Add file → Create new file** dabayein, naam ki jagah likhein
`Wedding Films/readme.txt` (slash `/` se folder ban jata hai), kuch bhi likh kar **Commit**.
Phir us naye folder mein video upload karein.

## ⚠️ Size ki limit — zaroor parhein

* GitHub website se ek file **25 MB** se bari upload **nahi** hoti.
* Website bhi choti video jaldi chalati hai.

Isliye video upload se pehle chhoti (compress) kar lein:

1. **HandBrake** free software install karein (handbrake.fr).
2. Video kholein → Preset: **General → Fast 1080p30**.
3. **Video** tab mein *Constant Quality* RF ko **26–28** kar dein.
4. **Start Encode** dabayein. Nayi file aam tor pr 10–25 MB ki hoti hai aur quality theek rehti hai.
5. Agar phir bhi 25 MB se bari ho to RF 30 kar dein ya preset **Fast 720p30** lein.
