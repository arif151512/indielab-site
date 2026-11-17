#!/usr/bin/env python3
"""IndieLab (indielab.online) — static blog generator.
Build: python3 build.py  →  dist/  (deploy dist/ to Vercel)
Design: editorial paper-and-ink, quiet chrome, real photos carry the colour (unslop pass).
"""
import os, json, html, datetime, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
SITE = "https://indielab.online"
SITE_NAME = "IndieLab"
TAGLINE = "Gift ideas and home finds worth your money"
GA_ID = "G-XXXXXXXXXX"  # <-- replace with the real GA4 measurement ID, then rebuild
DATE = "2026-11-18"

PRODUCTS = {
    "blanket": {
        "name": "Electric Heated Throw Blanket",
        "short": "Heated Blanket",
        "link": "https://link.amazon/B069CSpVFU",
        "img": "blanket-1",
        "blurb": "A plush electric throw that warms up in minutes — for sofas, beds and anyone who is always cold.",
        "points": ["Adjustable warmth for sofas, beds and reading chairs", "Costs pennies to run compared with heating a whole room", "The gift that gets used every single night of winter"],
        "pair": "a favourite paperback and a box of good tea",
    },
    "mask": {
        "name": "BIODANCE Bio-Collagen Face Mask Set",
        "short": "Collagen Mask Set",
        "link": "https://link.amazon/B09nPdyVm",
        "img": "mask-1",
        "blurb": "The viral overnight hydrogel mask — wear it while you sleep, wake up with firmer, glowing skin.",
        "points": ["Hydrogel mask that turns transparent as skin absorbs it", "Made for overnight wear or a 3–4 hour spa session", "Gift-ready set that fits in a stocking"],
        "pair": "a silk pillowcase or a scented candle for a full spa-night kit",
    },
    "thermo": {
        "name": "Digital Meat Thermometer",
        "short": "Meat Thermometer",
        "link": "https://link.amazon/B0flxAzBs",
        "img": "thermo-1",
        "blurb": "An instant-read digital probe that ends the guesswork — perfect steak, chicken and roasts, every time.",
        "points": ["Reads the temperature in seconds, right at the grill", "Ends dry turkey and undercooked chicken for good", "Small, practical and genuinely appreciated by home cooks"],
        "pair": "a jar of smoked sea salt or a set of grill tongs",
    },
    "fairy": {
        "name": "Fairy Lights — 12 Pack",
        "short": "Fairy Lights 12-Pack",
        "link": "https://link.amazon/B0hbdqlz5",
        "img": "fairy-3",
        "blurb": "Twelve strands of warm copper-wire fairy lights for jars, wreaths, shelves, mirrors and beds.",
        "points": ["Battery powered — no outlets, no visible cords", "One pack decorates a whole room (or a whole house)", "Works all year: Christmas, bedrooms, weddings, patios"],
        "pair": "a set of glass mason jars for instant lantern gifts",
    },
    "lamp": {
        "name": "Electric Candle Warmer Lamp (Black)",
        "short": "Candle Warmer Lamp",
        "link": "https://link.amazon/B05Fm6zjo",
        "img": "lamp-3",
        "blurb": "Melts jar candles from the top with warm light — full scent, no flame, no smoke, no soot. Timer and adjustable height, 2 bulbs included.",
        "points": ["Flame-free fragrance — safer around kids and pets", "Built-in timer and adjustable height for any jar candle", "Candles last far longer than burning, with no tunnelling"],
        "pair": "her favourite jar candle so she can use it the same night",
    },
    "chopper": {
        "name": "Fullstar Vegetable Chopper",
        "short": "Vegetable Chopper",
        "link": "https://link.amazon/B0ih0f76O",
        "img": "chopper-1",
        "blurb": "The viral kitchen chopper that dices onions, salads and meal prep in seconds — no tears, no knife skills.",
        "points": ["Dices, slices and chops with interchangeable blades", "Meal prep for the week in a fraction of the time", "The kitchen gift home cooks actually keep using"],
        "pair": "a set of glass meal-prep containers",
    },
}

CATEGORIES = {
    "gifts-for-mom": ("Christmas Gifts for Mom", "blanket-1"),
    "gifts-for-her": ("Christmas Gifts for Her", "mask-3"),
    "gifts-for-him": ("Gifts for Him", "thermo-2"),
    "cozy-home": ("Cozy Christmas Home", "fairy-1"),
    "stocking-stuffers": ("Stocking Stuffers", "mask-1"),
    "kitchen-gadgets": ("Kitchen Gadgets & Tools", "thermo-3"),
}

# (title, product, category, hero, angle)
POSTS = [
    ("Christmas Gifts for Mom: A Cozy Heated Blanket", "blanket", "gifts-for-mom", "blanket-1", "gift"),
    ("A Cozy Gift She'll Use Every Single Night", "blanket", "gifts-for-mom", "blanket-2", "gift"),
    ("Christmas Gifts for Grandma: Warm, Soft & Snuggly", "blanket", "gifts-for-mom", "blanket-1", "gift"),
    ("Stay Warm All Winter: Electric Heated Throw", "blanket", "cozy-home", "blanket-3", "guide"),
    ("Heated Blanket Gift Idea for Cold Sleepers", "blanket", "cozy-home", "blanket-2", "guide"),
    ("Cozy Winter Gift Ideas for Her", "blanket", "gifts-for-her", "blanket-1", "roundup"),
    ("Best Heated Blanket for Winter Nights", "blanket", "cozy-home", "blanket-2", "guide"),
    ("Affordable Christmas Gifts for Mom", "blanket", "gifts-for-mom", "blanket-3", "roundup"),
    ("Warm Gifts for People Who Are Always Cold", "blanket", "gifts-for-mom", "blanket-1", "roundup"),
    ("Heated Blanket: This Year's Gift Pick", "blanket", "cozy-home", "blanket-2", "guide"),
    ("Christmas Gifts for Her: The Viral Collagen Mask", "mask", "gifts-for-her", "mask-1", "gift"),
    ("The Overnight Mask Everyone's Talking About", "mask", "gifts-for-her", "mask-2", "guide"),
    ("Self Care Gift Ideas: Overnight Glow Mask", "mask", "gifts-for-her", "mask-2", "care"),
    ("Stocking Stuffers for Her: Glow-Up Edition", "mask", "stocking-stuffers", "mask-3", "roundup"),
    ("Beauty Gifts Under $25 She'll Actually Love", "mask", "stocking-stuffers", "mask-1", "roundup"),
    ("The Viral Korean Mask Everyone Wants", "mask", "gifts-for-her", "mask-3", "guide"),
    ("Skincare Christmas Gifts for Women", "mask", "gifts-for-her", "mask-1", "roundup"),
    ("Overnight Face Mask for Glowing Skin", "mask", "gifts-for-her", "mask-2", "care"),
    ("Cute Stocking Stuffers for Beauty Lovers", "mask", "stocking-stuffers", "mask-1", "roundup"),
    ("Self Care Sunday Essentials", "mask", "gifts-for-her", "mask-2", "care"),
    ("Christmas Gifts for Dad: The Grill Master's Secret", "thermo", "gifts-for-him", "thermo-1", "gift"),
    ("Perfect Steak Every Time: No More Guessing", "thermo", "gifts-for-him", "thermo-2", "howto"),
    ("Gifts for Men Who Love to Grill", "thermo", "gifts-for-him", "thermo-2", "roundup"),
    ("Stocking Stuffers for Him: Useful & Under $25", "thermo", "stocking-stuffers", "thermo-1", "roundup"),
    ("Never Serve Dry Turkey Again", "thermo", "kitchen-gadgets", "thermo-3", "howto"),
    ("Best Meat Thermometer for Grilling", "thermo", "gifts-for-him", "thermo-2", "guide"),
    ("Christmas Gifts for Husbands Who BBQ", "thermo", "gifts-for-him", "thermo-1", "gift"),
    ("Cook Steak Perfectly Every Single Time", "thermo", "kitchen-gadgets", "thermo-3", "howto"),
    ("Kitchen Gadgets Every Home Cook Needs", "thermo", "kitchen-gadgets", "thermo-1", "roundup"),
    ("Instant Read Thermometer: A Grill Essential", "thermo", "gifts-for-him", "thermo-2", "guide"),
    ("Bedroom Glow-Up: Fairy Lights Edition", "fairy", "cozy-home", "fairy-1", "decor"),
    ("Cozy Christmas Home: Fairy Light Magic", "fairy", "cozy-home", "fairy-1", "decor"),
    ("Mason Jar Fairy Lights: 5-Minute Christmas Decor", "fairy", "cozy-home", "fairy-2", "decor"),
    ("12 Fairy Light Strands for Every Corner", "fairy", "cozy-home", "fairy-3", "guide"),
    ("Stocking Stuffer Idea: Twinkle Lights 12-Pack", "fairy", "stocking-stuffers", "fairy-3", "roundup"),
    ("Fairy Light Decor Ideas for Christmas", "fairy", "cozy-home", "fairy-2", "decor"),
    ("Battery Fairy Lights for Jars & Wreaths", "fairy", "cozy-home", "fairy-3", "guide"),
    ("Cozy Room Decor Ideas on a Budget", "fairy", "cozy-home", "fairy-1", "decor"),
    ("Christmas Table Decor Ideas That Glow", "fairy", "cozy-home", "fairy-2", "decor"),
    ("Twinkle Lights for Cozy Girls' Rooms", "fairy", "cozy-home", "fairy-1", "decor"),
    ("All the Candle Glow, None of the Flame", "lamp", "cozy-home", "lamp-1", "guide"),
    ("The Cozy Candle Corner Every Home Needs", "lamp", "cozy-home", "lamp-2", "decor"),
    ("Make Your Candles Last 4x Longer", "lamp", "cozy-home", "lamp-1", "howto"),
    ("Christmas Gifts for Mom: The Candle Warmer Lamp", "lamp", "gifts-for-mom", "lamp-3", "gift"),
    ("The Perfect Gift for Candle Lovers", "lamp", "gifts-for-her", "lamp-3", "gift"),
    ("Candle Warmer Lamp: This Year's Gift Pick", "lamp", "gifts-for-her", "lamp-3", "guide"),
    ("Cozy Home Gifts for Candle Lovers", "lamp", "cozy-home", "lamp-2", "roundup"),
    ("Flameless Candle Ideas for Every Room", "lamp", "cozy-home", "lamp-1", "decor"),
    ("Thoughtful Gifts for Candle Lovers", "lamp", "gifts-for-her", "lamp-3", "roundup"),
    ("Wax Warmer Lamp Decor Ideas", "lamp", "cozy-home", "lamp-2", "decor"),
]

def slugify(t):
    s = t.lower()
    for ch in ":,&'’":
        s = s.replace(ch, "")
    s = "-".join(s.split())
    while "--" in s:
        s = s.replace("--", "-")
    return s

POSTS = [dict(title=t, product=p, cat=c, hero=h, angle=a, slug=slugify(t)) for (t, p, c, h, a) in POSTS]

CSS = """
:root{--paper:#FAF6F0;--ink:#20241F;--muted:#6E7268;--line:#E4DCCE;--accent:#C24914;--accent-ink:#9A3A0E;--soft:#F2EADF;--card:#FFFDF9}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--paper);color:var(--ink);font-family:Inter,system-ui,-apple-system,'Segoe UI',sans-serif;font-size:17px;line-height:1.65;-webkit-font-smoothing:antialiased}
img{display:block;max-width:100%}
a{color:var(--accent-ink);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1120px;margin:0 auto;padding:0 22px}
header.site{border-bottom:1px solid var(--line);background:var(--paper);position:sticky;top:0;z-index:10}
.bar{display:flex;align-items:center;justify-content:space-between;padding:16px 0;gap:16px}
.wordmark{font-family:Fraunces,Georgia,serif;font-size:30px;font-weight:700;color:var(--ink);letter-spacing:-.5px}
.wordmark span{color:var(--accent)}
nav.main{display:flex;gap:22px;flex-wrap:wrap}
nav.main a{color:var(--ink);font-size:15px;font-weight:500}
nav.main a:hover{color:var(--accent-ink);text-decoration:none}
.masthead{padding:56px 0 8px;text-align:left}
.masthead h1{font-family:Fraunces,Georgia,serif;font-size:clamp(38px,5.4vw,62px);line-height:1.08;font-weight:700;letter-spacing:-1px;max-width:16ch}
.masthead p{color:var(--muted);font-size:19px;margin-top:16px;max-width:56ch}
.kicker{font-size:13px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-ink);margin-bottom:14px}
h2.sec{font-family:Fraunces,Georgia,serif;font-size:30px;letter-spacing:-.5px;margin:52px 0 20px;padding-top:28px;border-top:1px solid var(--line)}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:26px}
@media(max-width:900px){.grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.grid{grid-template-columns:1fr}nav.main{display:none}}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden}
.card a{color:var(--ink)}
.card a:hover{text-decoration:none}
.card img{aspect-ratio:4/3.4;object-fit:cover;width:100%}
.card .pad{padding:18px 20px 20px}
.card h3{font-family:Fraunces,Georgia,serif;font-size:21px;line-height:1.25;letter-spacing:-.3px}
.card p{color:var(--muted);font-size:15px;margin-top:8px}
.tag{display:inline-block;font-size:12.5px;font-weight:600;color:var(--accent-ink);background:var(--soft);border-radius:999px;padding:3px 10px;margin-bottom:10px}
.feature{display:grid;grid-template-columns:1.15fr 1fr;gap:34px;align-items:center;margin-top:26px}
@media(max-width:800px){.feature{grid-template-columns:1fr}}
.feature img{border-radius:18px;aspect-ratio:4/3.6;object-fit:cover;width:100%}
.feature h2{font-family:Fraunces,Georgia,serif;font-size:clamp(28px,3.6vw,42px);line-height:1.12;letter-spacing:-.6px}
.feature p{color:var(--muted);margin-top:14px;font-size:18px}
.btn{display:inline-block;background:var(--ink);color:#FFF8F0;font-weight:600;font-size:16px;padding:13px 26px;border-radius:999px;margin-top:22px}
.btn:hover{background:var(--accent-ink);text-decoration:none;color:#fff}
.btn.light{background:var(--soft);color:var(--ink)}
.picks{display:grid;grid-template-columns:repeat(3,1fr);gap:26px}
@media(max-width:900px){.picks{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.picks{grid-template-columns:1fr}}
.pick{display:flex;gap:16px;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:16px;align-items:center}
.pick img{width:86px;height:86px;border-radius:12px;object-fit:cover}
.pick h3{font-size:17px;font-family:Fraunces,Georgia,serif;line-height:1.3}
.pick p{color:var(--muted);font-size:14px;margin-top:4px}
.pick .price{color:var(--accent-ink);font-weight:600;font-size:14.5px}
article.post{max-width:760px;margin:0 auto;padding:44px 22px 10px}
article.post h1{font-family:Fraunces,Georgia,serif;font-size:clamp(32px,4.6vw,48px);line-height:1.12;letter-spacing:-.8px}
article.post .meta{color:var(--muted);font-size:14.5px;margin:14px 0 24px}
article.post img.hero{border-radius:18px;width:100%;aspect-ratio:16/10.5;object-fit:cover}
article.post h2{font-family:Fraunces,Georgia,serif;font-size:27px;letter-spacing:-.4px;margin:36px 0 12px}
article.post p{margin:12px 0}
article.post ul{margin:12px 0 12px 22px}
article.post li{margin:7px 0}
.disc{font-size:13.5px;color:var(--muted);background:var(--soft);border-radius:10px;padding:10px 14px;margin:18px 0}
.buybox{display:grid;grid-template-columns:180px 1fr;gap:22px;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:22px;margin:30px 0;align-items:center}
@media(max-width:600px){.buybox{grid-template-columns:1fr}}
.buybox img{border-radius:12px;aspect-ratio:1/1.15;object-fit:cover;width:100%}
.buybox h3{font-family:Fraunces,Georgia,serif;font-size:23px}
.buybox ul{margin:10px 0 0 20px;font-size:15.5px}
.faq{border-top:1px solid var(--line);padding:16px 0}
.faq h3{font-size:18px;font-family:Fraunces,Georgia,serif}
footer.site{border-top:1px solid var(--line);margin-top:70px;padding:38px 0 46px;color:var(--muted);font-size:14.5px}
footer.site .cols{display:flex;gap:44px;flex-wrap:wrap;justify-content:space-between}
footer.site a{color:var(--ink)}
table.admin{width:100%;border-collapse:collapse;font-size:14.5px}
table.admin th,table.admin td{border-bottom:1px solid var(--line);padding:9px 10px;text-align:left;vertical-align:top}
table.admin th{font-size:12.5px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
.stat{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin:26px 0}
@media(max-width:800px){.stat{grid-template-columns:repeat(2,1fr)}}
.stat .box{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px}
.stat .num{font-family:Fraunces,Georgia,serif;font-size:34px}
.stat .lab{color:var(--muted);font-size:13.5px}
.note{background:var(--soft);border-radius:12px;padding:16px 18px;font-size:15px;margin:18px 0}
"""

def head(title, desc, path, extra=""):
    ga = ""
    if GA_ID != "G-XXXXXXXXXX":
        ga = f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}");</script>'
    else:
        ga = f'<!-- Google Analytics: replace GA_ID in build.py with your G- ID and rebuild. Placeholder: {GA_ID} -->'
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{path}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
{ga}
{extra}
</head>
<body>
<header class="site"><div class="wrap bar">
<a class="wordmark" href="/">Indie<span>Lab</span></a>
<nav class="main">
<a href="/category/gifts-for-mom/">For Mom</a>
<a href="/category/gifts-for-her/">For Her</a>
<a href="/category/gifts-for-him/">For Him</a>
<a href="/category/cozy-home/">Cozy Home</a>
<a href="/category/stocking-stuffers/">Stocking Stuffers</a>
<a href="/products/">Top Picks</a>
</nav>
</div></header>
"""

FOOT = f"""
<footer class="site"><div class="wrap cols">
<div style="max-width:420px">
<div class="wordmark" style="font-size:24px">Indie<span>Lab</span></div>
<p style="margin-top:8px">{TAGLINE}. Every pick is researched from what shoppers actually search for and buy.</p>
</div>
<div>
<p><strong style="color:var(--ink)">Explore</strong></p>
<p><a href="/products/">Top picks</a><br><a href="/category/cozy-home/">Cozy Christmas home</a><br><a href="/category/stocking-stuffers/">Stocking stuffers</a></p>
</div>
<div>
<p><strong style="color:var(--ink)">About</strong></p>
<p><a href="/about/">About IndieLab</a><br><a href="/affiliate-disclosure/">Affiliate disclosure</a><br><a href="/privacy-policy/">Privacy policy</a></p>
</div>
</div>
<div class="wrap" style="margin-top:26px;font-size:13px">
<p>IndieLab is a participant in the Amazon Services LLC Associates Program. As an Amazon Associate, IndieLab earns from qualifying purchases. Prices and availability on Amazon change often — check the product page for the current price.</p>
<p style="margin-top:8px">© 2026 IndieLab · indielab.online</p>
</div></footer>
</body></html>
"""

def card(post):
    cat_name = CATEGORIES[post["cat"]][0]
    prod = PRODUCTS[post["product"]]
    return f"""<div class="card"><a href="/blog/{post['slug']}/">
<img src="/img/{post['hero']}.jpg" alt="{html.escape(post['title'])}" loading="lazy">
<div class="pad"><span class="tag">{cat_name}</span>
<h3>{html.escape(post['title'])}</h3>
<p>{html.escape(prod['blurb'])}</p></div></a></div>"""

INTROS = {
    "gift": [
        "Some gifts get opened, smiled at, and quietly forgotten by January. This is not one of them. {blurb}",
        "The best Christmas gifts share one trait: the person uses them the same week they receive them — and keeps using them. This pick earns its place on that list. {blurb}",
    ],
    "guide": [
        "If you have been going back and forth on this one, here is the short version: it solves a real, everyday annoyance, and it does it simply. {blurb}",
        "There are dozens of versions of this product on Amazon. This is the one that keeps showing up in gift guides and carts — for good reason. {blurb}",
    ],
    "howto": [
        "The difference between a disappointing result and a perfect one is usually one small tool and thirty seconds of patience. {blurb}",
        "Nobody teaches you this part — you learn it after the first dry turkey or the first overcooked steak. Here is the shortcut. {blurb}",
    ],
    "decor": [
        "Good decor is rarely about buying more things. It is about one change that makes the whole room feel different the moment the light drops. {blurb}",
        "This is the kind of small upgrade guests notice without being able to name it. {blurb}",
    ],
    "care": [
        "Self-care gifts work when they turn an ordinary evening into a small ritual. This one does exactly that. {blurb}",
        "The products people rave about to their friends are rarely the expensive ones — they are the ones that make a Tuesday night feel like a spa booking. {blurb}",
    ],
    "roundup": [
        "Every gift list needs at least one pick that is small, affordable and genuinely exciting to open. This is that pick. {blurb}",
        "We keep this list honest: if it is here, it is because people search for it, buy it, and buy it again as a gift. {blurb}",
    ],
}

FAQS = [
    ("Is it a good gift for someone I don't know well?", "Yes — it is useful without being personal, which makes it a safe pick for in-laws, colleagues, Secret Santa draws and hosts."),
    ("When should I order it for Christmas?", "Order by mid-December to be safe. Amazon delivery speeds up and slows down through the season, and popular gift items do sell out."),
    ("What if they don't like it?", "Amazon's standard return window applies, and practical gifts like this are among the least returned — they get used instead."),
    ("Can I pair it with something else?", "Absolutely — see the pairing idea in the box above. A small add-on turns a good gift into a themed one."),
]

def post_body(post):
    prod = PRODUCTS[post["product"]]
    cat_name = CATEGORIES[post["cat"]][0]
    intro = INTROS[post["angle"]][hash(post["slug"]) % 2].format(blurb=prod["blurb"])
    points = "".join(f"<li>{p}</li>" for p in prod["points"])
    faqs = "".join(f'<div class="faq"><h3>{q}</h3><p>{a}</p></div>' for q, a in FAQS[:3])
    return f"""
<p class="kicker">{cat_name}</p>
<h1>{html.escape(post['title'])}</h1>
<p class="meta">By the IndieLab editors · Updated {DATE} · Gift guides</p>
<img class="hero" src="/img/{post['hero']}.jpg" alt="{html.escape(post['title'])}">
<div class="disc">This post contains affiliate links. If you buy through them, IndieLab may earn a commission at no extra cost to you. <a href="/affiliate-disclosure/">How this works</a></div>
<p>{intro}</p>
<h2>Why this one makes the list</h2>
<ul>{points}</ul>
<p>It also photographs beautifully and wraps easily — two underrated qualities in December, when the gift has to look as good as it works.</p>
<h2>How to gift it well</h2>
<p>Wrap it simply, and pair it with {prod['pair']}. Add a short note saying why you picked it — one honest sentence ("you're always cold", "your steaks deserve this", "spa night, on me") does more than any gift tag.</p>
<div class="buybox">
<img src="/img/{prod['img']}.jpg" alt="{html.escape(prod['name'])}">
<div>
<h3>{html.escape(prod['name'])}</h3>
<p>{html.escape(prod['blurb'])}</p>
<a class="btn" href="{prod['link']}" rel="nofollow sponsored noopener" target="_blank">Check price on Amazon</a>
<p style="font-size:13px;color:var(--muted);margin-top:10px">As an Amazon Associate, IndieLab earns from qualifying purchases.</p>
</div></div>
<h2>Good to know before you buy</h2>
<p>Check the size, colour and pack options on the Amazon page before ordering — several of our picks come in variants, and the most-gifted one is not always the default. Prices move during the holiday season, so the price you see today may not be the price tomorrow. Order earlier rather than later: delivery windows stretch in the last two weeks of December.</p>
<h2>Questions, answered</h2>
{faqs}
"""

def page(path, content):
    full = os.path.join(DIST, path.strip("/"), "index.html") if path != "/" else os.path.join(DIST, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)

def build():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)
    shutil.copytree(os.path.join(ROOT, "assets", "img"), os.path.join(DIST, "img"))
    with open(os.path.join(DIST, "styles.css"), "w") as f:
        f.write(CSS)

    # Home
    feat = POSTS[0]
    cards = "\n".join(card(p) for p in POSTS[1:13])
    picks = "\n".join(
        f"""<div class="pick"><img src="/img/{v['img']}.jpg" alt="{html.escape(v['name'])}"><div>
        <h3>{html.escape(v['name'])}</h3><p>{html.escape(v['blurb'][:64])}…</p>
        <a class="price" href="{v['link']}" rel="nofollow sponsored noopener" target="_blank">See it on Amazon</a></div></div>"""
        for v in PRODUCTS.values())
    cats = "\n".join(
        f"""<div class="card"><a href="/category/{slug}/"><img src="/img/{img}.jpg" alt="{name}" loading="lazy">
        <div class="pad"><h3>{name}</h3><p>{sum(1 for p in POSTS if p['cat']==slug)} gift guides</p></div></a></div>"""
        for slug, (name, img) in CATEGORIES.items())
    home = head(f"{SITE_NAME} — {TAGLINE}", "Gift ideas and home finds: heated blankets, viral skincare, grill gadgets, fairy lights and cozy home picks — researched from what shoppers actually search for.", "/") + f"""
<main class="wrap">
<section class="masthead">
<p class="kicker">Gift guides · Cozy home · Kitchen finds</p>
<h1>Gifts people actually use, found without the doom-scroll.</h1>
<p>IndieLab tracks what shoppers search for on Pinterest and Amazon, then writes the short, honest guide for each find — who it suits, how to gift it, and where to get it.</p>
</section>
<section class="feature">
<img src="/img/{feat['hero']}.jpg" alt="{html.escape(feat['title'])}">
<div>
<span class="tag">Featured guide</span>
<h2>{html.escape(feat['title'])}</h2>
<p>{html.escape(PRODUCTS[feat['product']]['blurb'])}</p>
<a class="btn" href="/blog/{feat['slug']}/">Read the guide</a>
</div>
</section>
<h2 class="sec">This season's top picks</h2>
<div class="picks">{picks}</div>
<h2 class="sec">Latest gift guides</h2>
<div class="grid">{cards}</div>
<p style="margin-top:26px"><a class="btn light" href="/products/">Browse all picks</a></p>
<h2 class="sec">Browse by list</h2>
<div class="grid">{cats}</div>
</main>
""" + FOOT
    page("/", home)

    # Posts
    for post in POSTS:
        related = [p for p in POSTS if p is not post and (p["cat"] == post["cat"] or p["product"] == post["product"])][:3]
        rel = "\n".join(card(p) for p in related)
        body = head(f"{post['title']} — {SITE_NAME}", PRODUCTS[post["product"]]["blurb"], f"/blog/{post['slug']}/") \
            + f'<main><article class="post">{post_body(post)}</article>' \
            + f'<div class="wrap"><h2 class="sec">Keep reading</h2><div class="grid">{rel}</div></div></main>' + FOOT
        page(f"/blog/{post['slug']}/", body)

    # Categories
    for slug, (name, img) in CATEGORIES.items():
        posts = [p for p in POSTS if p["cat"] == slug]
        grid = "\n".join(card(p) for p in posts) or "<p>No guides yet — new ones land daily.</p>"
        body = head(f"{name} — {SITE_NAME}", f"{name}: gift guides and honest picks from IndieLab.", f"/category/{slug}/") + f"""
<main class="wrap">
<section class="masthead"><p class="kicker">Gift guides</p><h1>{name}</h1>
<p>{len(posts)} guides, updated through the season.</p></section>
<div class="grid" style="margin-top:30px">{grid}</div>
</main>""" + FOOT
        page(f"/category/{slug}/", body)

    # Products page
    rows = "\n".join(
        f"""<div class="buybox"><img src="/img/{v['img']}.jpg" alt="{html.escape(v['name'])}"><div>
        <h3>{html.escape(v['name'])}</h3><p>{html.escape(v['blurb'])}</p>
        <a class="btn" href="{v['link']}" rel="nofollow sponsored noopener" target="_blank">Check price on Amazon</a>
        <p style="font-size:13px;color:var(--muted);margin-top:10px">As an Amazon Associate, IndieLab earns from qualifying purchases.</p></div></div>"""
        for v in PRODUCTS.values())
    body = head(f"Top Picks — {SITE_NAME}", "The IndieLab shortlist: six finds that anchor this season's gift guides.", "/products/") + f"""
<main class="wrap"><section class="masthead"><p class="kicker">The shortlist</p>
<h1>Top picks</h1><p>Six finds that anchor this season's guides — each one researched, photographed and written up below.</p></section>
{rows}</main>""" + FOOT
    page("/products/", body)

    # Static pages
    about = head(f"About — {SITE_NAME}", "About IndieLab: gift guides and home finds, researched from real search demand.", "/about/") + f"""
<main><article class="post"><p class="kicker">About</p><h1>About IndieLab</h1>
<p>IndieLab is a small, independent gift-guide and home-finds publication. We start from what people are actually searching for — on Pinterest, Google and Amazon — then write the guide we would want to read: who the gift suits, how to present it, what to check before buying, and an honest link to where it sells.</p>
<p>We publish through the holiday season and beyond: cozy home finds, beauty gifts, kitchen gadgets and the occasional viral product that turns out to be genuinely good.</p>
<h2>How we make money</h2>
<p>Guides contain Amazon affiliate links. If you buy through one, we may earn a commission at no extra cost to you. That is the whole business model — no paid placements, no sponsored rankings. See the <a href="/affiliate-disclosure/">affiliate disclosure</a>.</p>
</article></main>""" + FOOT
    page("/about/", about)

    disc = head(f"Affiliate Disclosure — {SITE_NAME}", "IndieLab's affiliate disclosure: Amazon Associates participation and how commissions work.", "/affiliate-disclosure/") + f"""
<main><article class="post"><p class="kicker">Disclosure</p><h1>Affiliate disclosure</h1>
<p>IndieLab (indielab.online) is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. As an Amazon Associate, IndieLab earns from qualifying purchases.</p>
<p>Product links on this site are affiliate links. If you click one and make a purchase, we may receive a small commission — at no additional cost to you. Prices and availability shown on Amazon at the time of purchase apply.</p>
<p>Commissions never change which products we feature or what we say about them.</p>
</article></main>""" + FOOT
    page("/affiliate-disclosure/", disc)

    priv = head(f"Privacy Policy — {SITE_NAME}", "IndieLab privacy policy: analytics, cookies and your data.", "/privacy-policy/") + f"""
<main><article class="post"><p class="kicker">Privacy</p><h1>Privacy policy</h1>
<p>IndieLab keeps data collection minimal. This site does not require accounts and does not sell personal information.</p>
<h2>Analytics</h2>
<p>We use Google Analytics to understand which guides readers find useful. Google Analytics uses cookies to measure visits in aggregate. You can opt out with the Google Analytics opt-out browser add-on.</p>
<h2>Advertising & affiliate links</h2>
<p>Outbound product links go to Amazon and carry an affiliate tag so purchases can be attributed. Amazon's own privacy policy governs what happens on their site. If advertising (such as Google AdSense) is enabled in future, this policy will be updated before it runs.</p>
<h2>Contact</h2>
<p>Questions about this policy: reach us through the Pinterest profile linked from our guides.</p>
</article></main>""" + FOOT
    page("/privacy-policy/", priv)

    # Admin dashboard (static overview — noindex)
    rows_admin = "\n".join(
        f"<tr><td>{html.escape(p['title'])}</td><td>{PRODUCTS[p['product']]['short']}</td><td>{CATEGORIES[p['cat']][0]}</td><td>Published</td><td>{DATE}</td></tr>"
        for p in POSTS)
    prod_rows = "\n".join(
        f"<tr><td>{html.escape(v['name'])}</td><td><a href=\"{v['link']}\">{v['link']}</a></td><td>{sum(1 for p in POSTS if PRODUCTS[p['product']] is v)} posts</td></tr>"
        for v in PRODUCTS.values())
    admin = head(f"Admin — {SITE_NAME}", "IndieLab admin overview.", "/admin/", '<meta name="robots" content="noindex,nofollow">') + f"""
<main class="wrap">
<section class="masthead"><p class="kicker">Admin</p><h1 style="font-size:40px">Publishing overview</h1>
<p>Static snapshot generated at build time ({DATE}). This dashboard is an overview, not a CMS — new posts are added by the daily build.</p></section>
<div class="stat">
<div class="box"><div class="num">{len(POSTS)}</div><div class="lab">Published posts</div></div>
<div class="box"><div class="num">{len(PRODUCTS)}</div><div class="lab">Products tracked</div></div>
<div class="box"><div class="num">{len(CATEGORIES)}</div><div class="lab">Categories</div></div>
<div class="box"><div class="num">{'Connected' if GA_ID != 'G-XXXXXXXXXX' else 'Not set'}</div><div class="lab">Google Analytics ({GA_ID})</div></div>
</div>
<div class="note"><strong>To finish setup:</strong> 1) Create the GA4 property and replace GA_ID in build.py, rebuild. 2) Push this repo to GitHub and import it in Vercel. 3) Add the DNS records for indielab.online from DEPLOY.md. 4) Once live, point daily Pinterest pins at blog URLs instead of direct Amazon links.</div>
<h2 class="sec">Products & affiliate links</h2>
<table class="admin"><tr><th>Product</th><th>Affiliate link</th><th>Coverage</th></tr>{prod_rows}</table>
<h2 class="sec">All posts</h2>
<table class="admin"><tr><th>Title</th><th>Product</th><th>Category</th><th>Status</th><th>Date</th></tr>{rows_admin}</table>
</main>""" + FOOT
    page("/admin/", admin)

    # robots + sitemap
    with open(os.path.join(DIST, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: {SITE}/sitemap.xml\n")
    urls = ["/", "/products/", "/about/", "/affiliate-disclosure/", "/privacy-policy/"] \
        + [f"/category/{s}/" for s in CATEGORIES] + [f"/blog/{p['slug']}/" for p in POSTS]
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"<url><loc>{SITE}{u}</loc><lastmod>{DATE}</lastmod></url>")
    sm.append("</urlset>")
    with open(os.path.join(DIST, "sitemap.xml"), "w") as f:
        f.write("\n".join(sm))
    with open(os.path.join(DIST, "vercel.json"), "w") as f:
        json.dump({"cleanUrls": True}, f, indent=2)
    print(f"Built {len(POSTS)} posts, {len(CATEGORIES)} categories, home, products, about, disclosure, privacy, admin → dist/")

if __name__ == "__main__":
    build()
