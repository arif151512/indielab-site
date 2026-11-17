# IndieLab — Deploy Guide (indielab.online)

The site is a static build. `build.py` generates `dist/` (62 pages). Rebuild after any content change: `python3 build.py`

## 1. Push to GitHub
1. Go to https://github.com/new — create a repo named `indielab-site` (Public or Private, no README).
2. In this folder, run:
   ```
   git remote add origin https://github.com/<YOUR-USERNAME>/indielab-site.git
   git push -u origin main
   ```
   (The local repo is already initialised with a first commit.)

## 2. Host on Vercel (free)
1. https://vercel.com/new → Import the `indielab-site` repo.
2. Framework Preset: **Other**. Build Command: leave empty (dist/ is committed). Output Directory: `dist`.
3. Deploy. You get a `*.vercel.app` URL first — check the site there.

## 3. Connect the domain indielab.online
In Vercel: Project → Settings → Domains → add `indielab.online` and `www.indielab.online`.
Then at your domain registrar (where you bought the domain), set these DNS records:
- Type **A**, Name `@` → Value `76.76.21.21`
- Type **CNAME**, Name `www` → Value `cname.vercel-dns.com`
DNS usually goes live in 5–30 minutes. Vercel issues the SSL certificate automatically.

## 4. Google Analytics
1. https://analytics.google.com → Admin → Create property → "IndieLab" → Web stream for `https://indielab.online`.
2. Copy the Measurement ID (looks like `G-AB12CD34EF`).
3. In `build.py`, set `GA_ID = "G-..."`, run `python3 build.py`, commit and push — Vercel redeploys automatically.
   (Until then the site carries a placeholder comment instead of the GA script.)

## 5. After the site is live
- Daily Pinterest pins switch their destination from direct Amazon links to the matching blog post URLs (`https://indielab.online/blog/<slug>/`) — tell Muse "site live" and the daily job gets updated.
- Apply for Google AdSense once traffic is steady (needs the Privacy Policy page — already included).
- Product descriptions/reviews from Arif get added into each post's buy box section on the next build.
