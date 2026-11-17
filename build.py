#!/usr/bin/env python3
"""IndieLab (indielab.online) — static blog generator v2.
Build: python3 build.py  →  dist/  (deploy dist/ to Vercel)
Design: editorial paper-and-ink, quiet chrome, real photos carry the colour.
Passes applied: unslop (tinted neutrals, one accent, no gradients/glows/emoji icons)
+ UI/UX Pro Max (mobile-first, 44px touch targets, reserved image space, density)
+ SEO/GEO (answer-first intros, question H2s, FAQ + Article + Breadcrumb schema,
  internal linking, unique per-post angles and meta).
"""
import os, json, html, shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DIST = os.path.join(ROOT, "dist")
IMG_SRC = os.path.join(ROOT, "assets", "img")
SITE = "https://indielab.online"
SITE_NAME = "IndieLab"
TAGLINE = "Gift ideas and home finds worth your money"
GA_ID = "G-RKPVDND4EG"
DATE = "2026-11-18"
DATE_HUMAN = "18 November 2026"

PRODUCTS = {
    "blanket": {
        "name": "Electric Heated Throw Blanket",
        "short": "Heated Blanket",
        "link": "https://link.amazon/B069CSpVFU",
        "blurb": "A plush electric throw that warms up in minutes — for sofas, beds and anyone who is always cold.",
        "points": ["Adjustable warmth for sofas, beds and reading chairs", "Costs pennies to run compared with heating a whole room", "The gift that gets used every single night of winter"],
        "pair": "a favourite paperback and a box of good tea",
        "who": "Moms, grandmas, cold sleepers, and anyone whose house runs colder than they like. It lands especially well with people who feel the cold but hate heating bills.",
        "facts": ["Electric throw blanket — plugs in, warms in minutes", "Made for sofas, beds, reading chairs and home offices", "Adjustable heat, so one blanket suits the whole sofa", "Throw size: made to cover one person generously, not a whole bed"],
        "checks": ["Check the heat settings and whether it has auto shut-off — most people want both", "Look at the washing instructions; most heated throws are hand-wash or gentle-cycle with the controller removed", "Measure your sofa or bed: a throw is smaller than a full electric blanket", "Check the cord length against where the nearest outlet sits"],
        "limits": "It needs a mains outlet nearby, and it warms one person, not a room. If the recipient's home has no spare outlet near the sofa, a non-electric sherpa throw may suit better.",
        "ideas": ["Drape it over the reading chair so it is warm before she sits down", "Use the lowest setting as a bed-warmer for twenty minutes before sleep", "Keep it on the sofa for film nights instead of turning the heating up", "Fold it at the foot of a guest bed in winter"],
        "faqs": [
            ("Is a heated blanket a good Christmas gift for mom?", "Yes — it is one of the most-used winter gifts there is. Moms who feel the cold use it daily from December to March, on the sofa and in bed."),
            ("How much does a heated throw cost to run?", "Very little — electric throws use roughly as much power as a bright light bulb, far less than heating a whole room for one person."),
            ("Can you wash an electric heated blanket?", "Most are washable on a gentle cycle once the controller is unplugged and removed. Always check the care label on the listing before the first wash."),
            ("Is a throw big enough for a bed?", "A throw is sized for one person on a sofa or across the foot of a bed. For full-bed coverage, look for a full-size electric blanket instead."),
            ("What if she is always cold but hates gadgets?", "That is exactly who this suits — there is one simple controller, no apps, no setup. Plug in, pick a heat level, done."),
        ],
    },
    "mask": {
        "name": "BIODANCE Bio-Collagen Face Mask Set",
        "short": "Collagen Mask Set",
        "link": "https://link.amazon/B09nPdyVm",
        "blurb": "The viral overnight hydrogel mask — wear it while you sleep, wake up with firmer, glowing skin.",
        "points": ["Hydrogel mask that turns transparent as skin absorbs it", "Made for overnight wear or a 3–4 hour spa session", "Gift-ready set that fits in a stocking"],
        "pair": "a silk pillowcase or a scented candle for a full spa-night kit",
        "who": "Skincare lovers, sisters, friends who follow beauty trends, and anyone with a big event coming up — photos, parties, weddings — who wants a glow the day before.",
        "facts": ["Overnight hydrogel sheet mask with collagen", "Turns transparent as the essence absorbs into the skin", "Wear it overnight, or 3–4 hours as a spa session", "Individually wrapped masks — easy to split into stockings or gift bags"],
        "checks": ["Check how many masks are in the pack before comparing prices — sets vary", "Patch-test first if the recipient has sensitive skin, as with any new skincare", "It is a single-use sheet mask; the glow is an event-prep boost, not a permanent change", "Buy from the listing with the brand name shown, so she gets the genuine product"],
        "limits": "Results are temporary — think of it as event prep, not a skincare routine in a box. Overnight wear also suits back-sleepers best; side-sleepers may prefer the 3–4 hour daytime session.",
        "ideas": ["The night before a party or photos, as the last step of her routine", "A Sunday self-care ritual: mask, candle, early night", "Split the set across several stockings — one mask each still feels luxe", "Pair two masks with a note for a sisters' spa night"],
        "faqs": [
            ("How does the BIODANCE collagen mask work?", "It is a hydrogel sheet soaked in collagen essence. As the skin absorbs the essence over several hours, the mask turns transparent — that is the sign it has done its work."),
            ("Do you sleep in the mask?", "You can — it is designed for overnight wear. If she prefers, a 3–4 hour session before bed gives a similar glow."),
            ("Is it a good stocking stuffer?", "One of the best beauty ones this year: small, light, individually wrapped, and it is the mask people have actually seen all over their feeds."),
            ("Is it suitable for sensitive skin?", "As with any new skincare, a patch test on the jawline first is the sensible move, especially for very sensitive skin."),
            ("How many masks should I gift?", "A full set for one recipient, or split a set between stockings — a single mask still reads as a treat, not a token."),
        ],
    },
    "thermo": {
        "name": "Digital Meat Thermometer",
        "short": "Meat Thermometer",
        "link": "https://link.amazon/B0flxAzBs",
        "blurb": "An instant-read digital probe that ends the guesswork — perfect steak, chicken and roasts, every time.",
        "points": ["Reads the temperature in seconds, right at the grill", "Ends dry turkey and undercooked chicken for good", "Small, practical and genuinely appreciated by home cooks"],
        "pair": "a jar of smoked sea salt or a set of grill tongs",
        "who": "Dads, husbands, BBQ obsessives, and home cooks who are tired of cutting into meat to check it. Also the person hosting Christmas dinner this year.",
        "facts": ["Instant-read digital probe thermometer", "Reads in seconds — no waiting while heat escapes the oven", "For grills, ovens, pans and smokers", "Small enough for a stocking or a kitchen drawer"],
        "checks": ["Check the probe style — fold-out probes store safest in a drawer", "Look for a backlit display if he grills after dark (most winter grilling is after dark)", "Water-resistant models rinse clean; fully waterproof ones can be washed properly", "It measures food temperature — for oven or grill air temperature you want a different gauge"],
        "limits": "An instant-read probe is not a leave-in thermometer: you open the oven or grill, take a reading, and close it again. For long smokes without opening the lid, a leave-in probe with a cable is the other tool for the job.",
        "ideas": ["Turkey: probe the thickest part of the thigh, away from bone — 74°C / 165°F and it is done", "Steak: pull it 3–5 degrees before target and rest it; the temperature coasts up", "Chicken breasts: the difference between juicy and dry is about four degrees", "Reheating leftovers: 74°C / 165°F all the way through, every time"],
        "faqs": [
            ("What temperature should chicken be cooked to?", "74°C (165°F) at the thickest part. A thermometer is the only reliable way to know — colour and clear juices both mislead."),
            ("Is a meat thermometer a good gift for men who grill?", "It is the classic useful gift for grillers: small, affordable, and it visibly improves every cook from the first steak onward."),
            ("Instant-read or leave-in thermometer?", "Instant-read for grilling, roasting and everyday cooking. Leave-in probes are for long, low smokes where the lid stays shut for hours."),
            ("Why does meat need resting?", "Resting lets juices redistribute and the temperature coast up a few degrees. Probe just before your target, rest, and it lands perfectly."),
            ("Can I use it for turkey at Christmas?", "That is its finest hour. One probe reading in the thigh ends the annual is-it-done debate — and the dry-turkey era."),
        ],
    },
    "fairy": {
        "name": "Fairy Lights — 12 Pack",
        "short": "Fairy Lights 12-Pack",
        "link": "https://link.amazon/B0hbdqlz5",
        "blurb": "Twelve strands of warm copper-wire fairy lights for jars, wreaths, shelves, mirrors and beds.",
        "points": ["Battery powered — no outlets, no visible cords", "One pack decorates a whole room (or a whole house)", "Works all year: Christmas, bedrooms, weddings, patios"],
        "pair": "a set of glass mason jars for instant lantern gifts",
        "who": "Teens and students decorating a first room, hosts who love a table setting, and anyone whose home needs warming up for winter evenings.",
        "facts": ["12 separate strands of copper-wire fairy lights", "Battery powered — place them anywhere, no outlet needed", "Warm-white glow for jars, wreaths, shelves, mirrors and headboards", "Flexible wire holds its shape around branches, rails and frames"],
        "checks": ["Check the strand length and LED count per strand — packs vary a lot", "See whether batteries are included or needed separately", "Check the rating if she wants them outdoors; not all strands are weatherproof", "Warm white vs bright white changes the whole mood — warm suits Christmas and bedrooms"],
        "limits": "Battery strands need battery changes, and a 12-pack spread across a whole house will still leave one corner unlit. For a permanent outdoor installation, solar or mains-powered lights are the longer-term answer.",
        "ideas": ["Fill mason jars and line them along the table as a centrepiece", "Weave one strand through the Christmas wreath on the door", "Run a strand along the headboard for a soft evening glow", "Wrap the banister or a mirror frame — five minutes, whole-room change"],
        "faqs": [
            ("Are battery fairy lights bright enough?", "They are mood lighting, not task lighting — perfect for glow and atmosphere in the evening, not for reading by."),
            ("How long do the batteries last?", "It depends on the batteries and hours per day; used for evenings only, a set typically lasts weeks. Switch them off overnight to stretch them further."),
            ("Can fairy lights go in jars?", "That is their best trick — the copper wire coils neatly into jars, bottles and lanterns with the small battery pack hidden behind."),
            ("Are they safe around fabric and bedding?", "LED fairy lights stay cool to the touch, which is why they are used on headboards and wreaths. Keep battery packs accessible and dry."),
            ("Why a 12-pack instead of one long strand?", "Twelve separate strands decorate twelve spots at once — jars, shelves, wreaths, mirrors — with no cords running between them."),
        ],
    },
    "lamp": {
        "name": "Electric Candle Warmer Lamp (Black)",
        "short": "Candle Warmer Lamp",
        "link": "https://link.amazon/B05Fm6zjo",
        "blurb": "Melts jar candles from the top with warm light — full scent, no flame, no smoke, no soot. Timer and adjustable height, 2 bulbs included.",
        "points": ["Flame-free fragrance — safer around kids and pets", "Built-in timer and adjustable height for any jar candle", "Candles last far longer than burning, with no tunnelling"],
        "pair": "her favourite jar candle so she can use it the same night",
        "who": "Candle lovers, moms with kids or pets, renters who cannot burn candles, and anyone with a shelf of half-burned jar candles tunnelling away.",
        "facts": ["Electric candle warmer lamp in black", "Melts jar candles from the top down with a warm bulb", "Built-in timer — set it and forget it", "Adjustable height to fit different jar candles", "2 bulbs included in the box"],
        "checks": ["Check her candle jars fit: the adjustable height suits most standard jar candles", "A timer matters — it is the feature owners say they use most", "Replacement bulbs are standard for this style; two are already included", "Place it where the cord reaches — it is a lamp, so it needs an outlet"],
        "limits": "You get scent and glow without a real flame's flicker — some candle lovers miss that. And it only works with jar candles; pillar candles and wax melts in open dishes are not what it is made for.",
        "ideas": ["On the nightstand with the timer set — scent while reading, off while sleeping", "In the hallway as a warm welcome-home glow", "Rescue a tunnelled candle: the lamp melts the wasted wax down the sides", "Kitchen counter corner, to keep cooking smells from winning"],
        "faqs": [
            ("How does a candle warmer lamp work?", "A warm bulb melts the top layer of a jar candle, releasing the fragrance without a flame — no smoke, no soot, and no tunnelling down the middle."),
            ("Do candles last longer with a warmer lamp?", "Yes, noticeably. Melting from the top uses the wax evenly instead of burning a tunnel, so the same jar gives far more hours of scent."),
            ("Is it safer than burning candles?", "There is no open flame, which is why it suits homes with kids, pets, or rental rules against candles. The bulb and melted wax still get warm, so treat it like a lamp."),
            ("What candles fit under it?", "Most standard jar candles. The height adjusts, so taller and shorter jars both fit — check the jar's height against the lamp's range on the listing."),
            ("Does it have a timer?", "Yes — this model has a built-in timer, plus adjustable height and 2 bulbs included."),
        ],
    },
    "chopper": {
        "name": "Fullstar Vegetable Chopper",
        "short": "Vegetable Chopper",
        "link": "https://link.amazon/B0ih0f76O",
        "blurb": "The viral kitchen chopper that dices onions, salads and meal prep in seconds — no tears, no knife skills.",
        "points": ["Dices, slices and chops with interchangeable blades", "Meal prep for the week in a fraction of the time", "The kitchen gift home cooks actually keep using"],
        "pair": "a set of glass meal-prep containers",
        "who": "Home cooks, meal-preppers, and anyone who hates chopping onions.",
        "facts": ["Manual vegetable chopper with interchangeable blades", "Dices, slices and chops into its own container", "Built for onions, salads and weekly meal prep"],
        "checks": ["Check the blade set included — configurations vary", "Container size matters if she meal-preps for a family"],
        "limits": "It is a prep tool, not a food processor — hard, large items still need a knife first.",
        "ideas": ["Sunday meal prep: a week of onions, peppers and cucumbers in minutes", "Salsa and pico de gallo with even dice, no tears"],
        "faqs": [
            ("Is the Fullstar chopper worth it?", "For anyone who cooks with onions and salads several times a week, yes — the time and tears it saves are the whole point."),
            ("Is it easy to clean?", "The parts separate for washing; a rinse right after use keeps the blades simple to clean."),
        ],
    },
}

CATEGORIES = {
    "gifts-for-mom": ("Christmas Gifts for Mom", "blanket-5", "Gift ideas for the woman who insists she doesn't need anything — warm, useful and quietly luxurious picks she will use every week, not shelve."),
    "gifts-for-her": ("Christmas Gifts for Her", "mask-4", "Beauty, self-care and cozy-home gifts for sisters, friends, partners and daughters — the ones already all over her feed, checked properly."),
    "gifts-for-him": ("Gifts for Him", "thermo-4", "Practical gifts for dads, husbands and brothers who say they want nothing: tools for the grill and kitchen that visibly improve the next cook."),
    "cozy-home": ("Cozy Christmas Home", "fairy-4", "Small changes that make a whole home feel warmer in December — light, warmth and scent, without a renovation or a big spend."),
    "stocking-stuffers": ("Stocking Stuffers", "mask-6", "Small, light and genuinely exciting stocking fillers — no joke gifts, no filler tat, everything here earns its place in the stocking."),
    "kitchen-gadgets": ("Kitchen Gadgets & Tools", "thermo-5", "Kitchen tools that solve one annoying job properly — for home cooks, Christmas-dinner hosts and anyone feeding a crowd this season."),
}

# (title, product, category, angle) — titles match the Pinterest pins exactly
POSTS = [
    ("Christmas Gifts for Mom: A Cozy Heated Blanket", "blanket", "gifts-for-mom", "gift"),
    ("A Cozy Gift She'll Use Every Single Night", "blanket", "gifts-for-mom", "gift"),
    ("Christmas Gifts for Grandma: Warm, Soft & Snuggly", "blanket", "gifts-for-mom", "gift"),
    ("Stay Warm All Winter: Electric Heated Throw", "blanket", "cozy-home", "guide"),
    ("Heated Blanket Gift Idea for Cold Sleepers", "blanket", "cozy-home", "guide"),
    ("Cozy Winter Gift Ideas for Her", "blanket", "gifts-for-her", "roundup"),
    ("Best Heated Blanket for Winter Nights", "blanket", "cozy-home", "guide"),
    ("Affordable Christmas Gifts for Mom", "blanket", "gifts-for-mom", "roundup"),
    ("Warm Gifts for People Who Are Always Cold", "blanket", "gifts-for-mom", "roundup"),
    ("Heated Blanket: This Year's Gift Pick", "blanket", "cozy-home", "guide"),
    ("Christmas Gifts for Her: The Viral Collagen Mask", "mask", "gifts-for-her", "gift"),
    ("The Overnight Mask Everyone's Talking About", "mask", "gifts-for-her", "guide"),
    ("Self Care Gift Ideas: Overnight Glow Mask", "mask", "gifts-for-her", "care"),
    ("Stocking Stuffers for Her: Glow-Up Edition", "mask", "stocking-stuffers", "roundup"),
    ("Beauty Gifts Under $25 She'll Actually Love", "mask", "stocking-stuffers", "roundup"),
    ("The Viral Korean Mask Everyone Wants", "mask", "gifts-for-her", "guide"),
    ("Skincare Christmas Gifts for Women", "mask", "gifts-for-her", "roundup"),
    ("Overnight Face Mask for Glowing Skin", "mask", "gifts-for-her", "care"),
    ("Cute Stocking Stuffers for Beauty Lovers", "mask", "stocking-stuffers", "roundup"),
    ("Self Care Sunday Essentials", "mask", "gifts-for-her", "care"),
    ("Christmas Gifts for Dad: The Grill Master's Secret", "thermo", "gifts-for-him", "gift"),
    ("Perfect Steak Every Time: No More Guessing", "thermo", "gifts-for-him", "howto"),
    ("Gifts for Men Who Love to Grill", "thermo", "gifts-for-him", "roundup"),
    ("Stocking Stuffers for Him: Useful & Under $25", "thermo", "stocking-stuffers", "roundup"),
    ("Never Serve Dry Turkey Again", "thermo", "kitchen-gadgets", "howto"),
    ("Best Meat Thermometer for Grilling", "thermo", "gifts-for-him", "guide"),
    ("Christmas Gifts for Husbands Who BBQ", "thermo", "gifts-for-him", "gift"),
    ("Cook Steak Perfectly Every Single Time", "thermo", "kitchen-gadgets", "howto"),
    ("Kitchen Gadgets Every Home Cook Needs", "thermo", "kitchen-gadgets", "roundup"),
    ("Instant Read Thermometer: A Grill Essential", "thermo", "gifts-for-him", "guide"),
    ("Bedroom Glow-Up: Fairy Lights Edition", "fairy", "cozy-home", "decor"),
    ("Cozy Christmas Home: Fairy Light Magic", "fairy", "cozy-home", "decor"),
    ("Mason Jar Fairy Lights: 5-Minute Christmas Decor", "fairy", "cozy-home", "decor"),
    ("12 Fairy Light Strands for Every Corner", "fairy", "cozy-home", "guide"),
    ("Stocking Stuffer Idea: Twinkle Lights 12-Pack", "fairy", "stocking-stuffers", "roundup"),
    ("Fairy Light Decor Ideas for Christmas", "fairy", "cozy-home", "decor"),
    ("Battery Fairy Lights for Jars & Wreaths", "fairy", "cozy-home", "guide"),
    ("Cozy Room Decor Ideas on a Budget", "fairy", "cozy-home", "decor"),
    ("Christmas Table Decor Ideas That Glow", "fairy", "cozy-home", "decor"),
    ("Twinkle Lights for Cozy Girls' Rooms", "fairy", "cozy-home", "decor"),
    ("All the Candle Glow, None of the Flame", "lamp", "cozy-home", "guide"),
    ("The Cozy Candle Corner Every Home Needs", "lamp", "cozy-home", "decor"),
    ("Make Your Candles Last 4x Longer", "lamp", "cozy-home", "howto"),
    ("Christmas Gifts for Mom: The Candle Warmer Lamp", "lamp", "gifts-for-mom", "gift"),
    ("The Perfect Gift for Candle Lovers", "lamp", "gifts-for-her", "gift"),
    ("Candle Warmer Lamp: This Year's Gift Pick", "lamp", "gifts-for-her", "guide"),
    ("Cozy Home Gifts for Candle Lovers", "lamp", "cozy-home", "roundup"),
    ("Flameless Candle Ideas for Every Room", "lamp", "cozy-home", "decor"),
    ("Thoughtful Gifts for Candle Lovers", "lamp", "gifts-for-her", "roundup"),
    ("Wax Warmer Lamp Decor Ideas", "lamp", "cozy-home", "decor"),
]

def slugify(t):
    s = t.lower()
    for ch in ":,&'’":
        s = s.replace(ch, "")
    s = "-".join(s.split())
    while "--" in s:
        s = s.replace("--", "-")
    return s

def image_pool(prod_key):
    """All images for a product, sorted — grows as new photos are added."""
    if not os.path.isdir(IMG_SRC):
        return [f"{prod_key}-1"]
    pool = sorted(f[:-4] for f in os.listdir(IMG_SRC) if f.startswith(prod_key + "-") and f.endswith(".jpg"))
    return pool or [f"{prod_key}-1"]

POSTS = [dict(title=t, product=p, cat=c, angle=a, slug=slugify(t)) for (t, p, c, a) in POSTS]
# Daily posts appended by the Pinterest workflow: posts_extra.json = [{title, product, cat, angle}]
_extra_path = os.path.join(ROOT, "posts_extra.json")
if os.path.exists(_extra_path):
    with open(_extra_path) as _f:
        for _e in json.load(_f):
            if slugify(_e["title"]) not in {p["slug"] for p in POSTS}:
                POSTS.append(dict(title=_e["title"], product=_e["product"], cat=_e["cat"],
                                  angle=_e["angle"], slug=slugify(_e["title"])))
_by_product = {}
for _p in POSTS:
    _by_product.setdefault(_p["product"], []).append(_p)
for _key, _plist in _by_product.items():
    _pool = image_pool(_key)
    for _i, _p in enumerate(_plist):
        _p["hero"] = _pool[_i % len(_pool)]
        _p["second"] = _pool[(_i + 2) % len(_pool)]
        _p["buyimg"] = _pool[(_i + 1) % len(_pool)]

def related(post, n=3):
    same = [p for p in POSTS if p["product"] == post["product"] and p["slug"] != post["slug"]]
    same.sort(key=lambda p: 0 if p["cat"] == post["cat"] else 1)
    return same[:n]

def meta_desc(post):
    prod = PRODUCTS[post["product"]]
    d = f"{post['title']} — {prod['blurb']} Who it's for, what to check before you buy, and how to gift it well."
    return d[:158].rsplit(" ", 1)[0] if len(d) > 158 else d

CSS = """
:root{--paper:#FAF6F0;--ink:#20241F;--muted:#64685C;--line:#E3DACA;--accent:#C24914;--accent-ink:#9A3A0E;--soft:#F2EADF;--card:#FFFDF9}
*{margin:0;padding:0;box-sizing:border-box}
html{scroll-behavior:smooth}
body{background:var(--paper);color:var(--ink);font-family:Inter,system-ui,-apple-system,'Segoe UI',sans-serif;font-size:17px;line-height:1.65;-webkit-font-smoothing:antialiased}
img{display:block;max-width:100%;height:auto}
a{color:var(--accent-ink);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1120px;margin:0 auto;padding:0 22px}
header.site{border-bottom:1px solid var(--line);background:var(--paper);position:sticky;top:0;z-index:10}
.bar{display:flex;align-items:center;justify-content:space-between;padding:13px 0;gap:16px}
.wordmark{font-family:Fraunces,Georgia,serif;font-size:29px;font-weight:700;color:var(--ink);letter-spacing:-.5px;display:inline-flex;align-items:center;gap:10px}
.wordmark .logo{width:32px;height:32px;border-radius:9px;flex:none}
.wordmark span{color:var(--accent)}
nav.main{display:flex;gap:20px;flex-wrap:wrap}
nav.main a{color:var(--ink);font-size:15px;font-weight:500;padding:6px 0}
nav.main a:hover{color:var(--accent-ink);text-decoration:none}
.masthead{padding:38px 0 4px}
.masthead h1{font-family:Fraunces,Georgia,serif;font-size:clamp(36px,5.2vw,58px);line-height:1.08;font-weight:700;letter-spacing:-1px;max-width:17ch}
.masthead p{color:var(--muted);font-size:18.5px;margin-top:13px;max-width:58ch}
.kicker{font-size:12.5px;font-weight:600;letter-spacing:.13em;text-transform:uppercase;color:var(--accent-ink);margin-bottom:12px}
.hero-grid{display:grid;grid-template-columns:1.12fr .88fr;gap:36px;align-items:center}
.hero-gif img{border-radius:18px;width:100%;aspect-ratio:3/2;object-fit:cover;border:1px solid var(--line)}
@media(max-width:800px){.hero-grid{grid-template-columns:1fr}.hero-gif{max-width:460px}}
.chips{display:flex;gap:9px;flex-wrap:wrap;margin-top:20px}
.chips a{display:inline-flex;align-items:center;min-height:42px;padding:8px 16px;border:1px solid var(--line);border-radius:999px;background:var(--card);color:var(--ink);font-size:14.5px;font-weight:500}
.chips a:hover{border-color:var(--accent);text-decoration:none}
h2.sec{font-family:Fraunces,Georgia,serif;font-size:28px;letter-spacing:-.5px;margin:38px 0 16px;padding-top:24px;border-top:1px solid var(--line)}
h2.sec:first-of-type{border-top:none;padding-top:0}
.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.card{background:var(--card);border:1px solid var(--line);border-radius:16px;overflow:hidden}
.card a{color:var(--ink)}
.card a:hover{text-decoration:none}
.card img{aspect-ratio:4/3.2;object-fit:cover;width:100%}
.card .pad{padding:15px 18px 17px}
.card h3{font-family:Fraunces,Georgia,serif;font-size:20px;line-height:1.25;letter-spacing:-.3px}
.card p{color:var(--muted);font-size:14.5px;margin-top:7px}
.tag{display:inline-block;font-size:12px;font-weight:600;color:var(--accent-ink);background:var(--soft);border-radius:999px;padding:3px 10px;margin-bottom:9px}
.feature{display:grid;grid-template-columns:1.12fr 1fr;gap:30px;align-items:center;margin-top:22px}
.feature img{border-radius:18px;aspect-ratio:4/3.4;object-fit:cover;width:100%}
.feature h2{font-family:Fraunces,Georgia,serif;font-size:clamp(27px,3.4vw,40px);line-height:1.12;letter-spacing:-.6px}
.feature p{color:var(--muted);margin-top:12px;font-size:17.5px}
.btn{display:inline-flex;align-items:center;min-height:48px;background:var(--ink);color:#FFF8F0;font-weight:600;font-size:16px;padding:12px 26px;border-radius:999px;margin-top:18px}
.btn:hover{background:var(--accent-ink);text-decoration:none;color:#fff}
.picks{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.pick{display:flex;gap:15px;background:var(--card);border:1px solid var(--line);border-radius:16px;padding:14px;align-items:center}
.pick img{width:82px;height:82px;border-radius:12px;object-fit:cover;flex:none}
.pick h3{font-size:16.5px;font-family:Fraunces,Georgia,serif;line-height:1.3}
.pick p{color:var(--muted);font-size:13.5px;margin-top:3px}
.cats{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}
.cat-card{position:relative;border-radius:16px;overflow:hidden;border:1px solid var(--line)}
.cat-card img{aspect-ratio:16/9.5;object-fit:cover;width:100%}
.cat-card .lbl{padding:13px 18px 15px;background:var(--card)}
.cat-card h3{font-family:Fraunces,Georgia,serif;font-size:20px}
.cat-card p{color:var(--muted);font-size:14px;margin-top:3px}
.cat-card a{color:var(--ink)}
.cat-card a:hover{text-decoration:none}
article.post{max-width:760px;margin:0 auto;padding:34px 22px 6px}
.crumbs{font-size:13.5px;color:var(--muted);margin-bottom:16px}
.crumbs a{color:var(--muted)}
article.post h1{font-family:Fraunces,Georgia,serif;font-size:clamp(31px,4.6vw,46px);line-height:1.13;letter-spacing:-.8px}
article.post .meta{color:var(--muted);font-size:14px;margin:12px 0 20px}
article.post img.hero{border-radius:18px;width:100%;aspect-ratio:16/10.5;object-fit:cover}
article.post img.mid{border-radius:16px;width:100%;aspect-ratio:16/9.5;object-fit:cover;margin:22px 0 6px}
article.post h2{font-family:Fraunces,Georgia,serif;font-size:26px;letter-spacing:-.4px;margin:32px 0 10px}
article.post p{margin:11px 0}
article.post ul{margin:11px 0 11px 22px}
article.post li{margin:6px 0}
.lede{font-size:19px;line-height:1.6}
.disc{font-size:13.5px;color:var(--muted);background:var(--soft);border-radius:10px;padding:10px 14px;margin:16px 0}
.facts{background:var(--card);border:1px solid var(--line);border-radius:16px;padding:18px 22px;margin:22px 0}
.facts h2{margin:0 0 8px;font-size:22px}
.facts ul{margin:6px 0 0 20px}
.buybox{display:grid;grid-template-columns:180px 1fr;gap:22px;background:var(--card);border:1px solid var(--line);border-radius:18px;padding:22px;margin:28px 0;align-items:center}
.buybox img{border-radius:12px;aspect-ratio:1/1.1;object-fit:cover;width:100%}
.buybox h3{font-family:Fraunces,Georgia,serif;font-size:23px}
.buybox ul{margin:10px 0 0 20px;font-size:15.5px}
.faq{border-top:1px solid var(--line);padding:14px 0}
.faq h3{font-size:17.5px;font-family:Fraunces,Georgia,serif}
.faq p{color:#3C4038}
.rel{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:6px}
footer.site{border-top:1px solid var(--line);margin-top:48px;padding:34px 0 42px;color:var(--muted);font-size:14.5px}
footer.site .cols{display:flex;gap:40px;flex-wrap:wrap;justify-content:space-between}
footer.site a{color:var(--ink)}
table.admin{width:100%;border-collapse:collapse;font-size:14.5px}
table.admin th,table.admin td{border-bottom:1px solid var(--line);padding:9px 10px;text-align:left;vertical-align:top}
table.admin th{font-size:12.5px;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}
.stat{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:22px 0}
.stat .box{background:var(--card);border:1px solid var(--line);border-radius:14px;padding:16px}
.stat .num{font-family:Fraunces,Georgia,serif;font-size:32px}
.stat .lab{color:var(--muted);font-size:13.5px}
.note{background:var(--soft);border-radius:12px;padding:15px 17px;font-size:15px;margin:16px 0}
@media(max-width:900px){.grid,.cats{grid-template-columns:repeat(2,1fr)}.picks{grid-template-columns:repeat(2,1fr)}.rel{grid-template-columns:1fr 1fr}}
@media(max-width:800px){.feature{grid-template-columns:1fr}.stat{grid-template-columns:repeat(2,1fr)}}
@media(max-width:640px){
 body{font-size:16px}
 .wrap{padding:0 16px}
 .bar{padding:10px 0 4px}
 header.site{position:static}
 nav.main{order:3;width:100%;flex-wrap:nowrap;overflow-x:auto;gap:8px;padding:6px 0 10px;-webkit-overflow-scrolling:touch;scrollbar-width:none}
 nav.main::-webkit-scrollbar{display:none}
 nav.main a{flex:none;display:inline-flex;align-items:center;min-height:42px;padding:8px 14px;border:1px solid var(--line);border-radius:999px;background:var(--card);font-size:14px}
 .masthead{padding:24px 0 0}
 .masthead h1{font-size:34px}
 .masthead p{font-size:16.5px}
 h2.sec{font-size:24px;margin:28px 0 13px;padding-top:20px}
 .grid,.cats,.picks,.rel{grid-template-columns:1fr}
 .card{display:flex}
 .card a{display:flex;width:100%}
 .card img{width:118px;height:100%;aspect-ratio:auto;flex:none}
 .card .pad{padding:12px 14px}
 .card h3{font-size:17.5px}
 .card p{display:none}
 .feature{gap:18px;margin-top:16px}
 .feature img{aspect-ratio:16/10}
 .pick img{width:72px;height:72px}
 .buybox{grid-template-columns:1fr;padding:18px}
 .buybox img{aspect-ratio:16/10}
 article.post{padding:22px 16px 4px}
 article.post h2{font-size:23px;margin:26px 0 8px}
 .lede{font-size:17.5px}
 footer.site{margin-top:36px}
}
"""

def head(title, desc, path, extra="", ogimg=None):
    ga = f'<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments)}}gtag("js",new Date());gtag("config","{GA_ID}");</script>'
    og = f"{SITE}/img/{ogimg}.jpg" if ogimg else f"{SITE}/img/blanket-1.jpg"
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="192x192" href="/favicon-192.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="theme-color" content="#FAF6F0">
<link rel="canonical" href="{SITE}{path}">
<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(desc)}">
<meta property="og:type" content="website">
<meta property="og:url" content="{SITE}{path}">
<meta property="og:image" content="{og}">
<meta name="twitter:card" content="summary_large_image">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/styles.css">
{ga}
{extra}
</head>
<body>
<header class="site"><div class="wrap bar">
<a class="wordmark" href="/"><img class="logo" src="/favicon-192.png" alt="IndieLab logo" width="32" height="32">Indie<span>Lab</span></a>
<nav class="main" aria-label="Categories">
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
<div class="wrap" style="margin-top:24px;font-size:13px">
<p>IndieLab is a participant in the Amazon Services LLC Associates Program. As an Amazon Associate, IndieLab earns from qualifying purchases. Prices and availability on Amazon change often — check the product page for the current price.</p>
<p style="margin-top:8px">© 2026 IndieLab · indielab.online</p>
</div></footer>
</body></html>
"""

def card(post):
    cat_name = CATEGORIES[post["cat"]][0]
    return f"""<div class="card"><a href="/blog/{post['slug']}/">
<img src="/img/{post['hero']}.jpg" alt="{html.escape(post['title'])} — {html.escape(PRODUCTS[post['product']]['short'])}" loading="lazy" width="640" height="512">
<div class="pad"><span class="tag">{cat_name}</span>
<h3>{html.escape(post['title'])}</h3>
<p>{html.escape(meta_desc(post))}</p></div></a></div>"""

# Answer-first ledes (GEO): one per angle, completed with product specifics below.
LEDES = {
    "gift": "Short answer: yes — this is one of those rare gifts that gets used the same week it is opened, and then all winter. {blurb}",
    "guide": "Short answer: if you want the version people keep recommending to each other, this is it. {blurb}",
    "howto": "Short answer: the fix is simpler than you think, and it is mostly about one small tool used at the right moment. {blurb}",
    "decor": "Short answer: yes, one small change really can make the whole room feel different — this is the change. {blurb}",
    "care": "Short answer: this is the self-care gift that actually feels like a treat, not a chore. {blurb}",
    "roundup": "Short answer: if you need one small, affordable pick that still feels thoughtful, start here. {blurb}",
}

ANGLE_SECTIONS = {
    "gift": ["who", "gift"],
    "guide": ["checks", "limits"],
    "howto": ["ideas", "checks"],
    "decor": ["ideas", "who"],
    "care": ["ideas", "limits"],
    "roundup": ["who", "facts"],
}

SECTION_TITLES = {
    "who": "Who is the {short} for?",
    "checks": "What should you check before buying?",
    "limits": "What are the honest downsides?",
    "ideas": "How do you get the most from it?",
    "facts": "Quick facts about the {short}",
    "gift": "How do you gift it well?",
}

def section_html(kind, prod):
    title = SECTION_TITLES[kind].format(short=prod["short"].lower())
    if kind == "who":
        body = f"<p>{prod['who']}</p>"
    elif kind == "checks":
        body = "<ul>" + "".join(f"<li>{c}</li>" for c in prod["checks"]) + "</ul>"
    elif kind == "limits":
        body = f"<p>{prod['limits']}</p>"
    elif kind == "ideas":
        body = "<ul>" + "".join(f"<li>{i}</li>" for i in prod["ideas"]) + "</ul>"
    elif kind == "facts":
        body = "<ul>" + "".join(f"<li>{f}</li>" for f in prod["facts"]) + "</ul>"
    elif kind == "gift":
        body = (f"<p>Wrap it simply, and pair it with {prod['pair']}. Add a short note saying why you picked it — "
                f"one honest sentence does more than any gift tag.</p>")
    return f"<h2>{title}</h2>\n{body}"

def post_body(post):
    prod = PRODUCTS[post["product"]]
    cat_name, _, _ = CATEGORIES[post["cat"]]
    lede = LEDES[post["angle"]].format(blurb=prod["blurb"])
    points = "".join(f"<li>{p}</li>" for p in prod["points"])
    pool = prod["faqs"]
    start = sum(post["slug"].encode()) % len(pool)
    faqs = [pool[(start + i) % len(pool)] for i in range(min(4, len(pool)))]
    faq_html = "".join(f'<div class="faq"><h3>{q}</h3><p>{a}</p></div>' for q, a in faqs)
    secs = "\n".join(section_html(k, prod) for k in ANGLE_SECTIONS[post["angle"]])
    rel = related(post)
    rel_html = "".join(f"""<div class="card"><a href="/blog/{r['slug']}/">
<img src="/img/{r['hero']}.jpg" alt="{html.escape(r['title'])}" loading="lazy" width="640" height="512">
<div class="pad"><h3>{html.escape(r['title'])}</h3></div></a></div>""" for r in rel)
    faq_ld = {"@context": "https://schema.org", "@type": "FAQPage",
              "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}
    art_ld = {"@context": "https://schema.org", "@type": "Article",
              "headline": post["title"], "description": meta_desc(post),
              "image": f"{SITE}/img/{post['hero']}.jpg", "datePublished": DATE, "dateModified": DATE,
              "author": {"@type": "Organization", "name": "IndieLab"},
              "publisher": {"@type": "Organization", "name": "IndieLab"},
              "mainEntityOfPage": f"{SITE}/blog/{post['slug']}/"}
    crumb_ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": cat_name, "item": f"{SITE}/category/{post['cat']}/"},
        {"@type": "ListItem", "position": 3, "name": post["title"]}]}
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in (art_ld, faq_ld, crumb_ld))
    body = f"""
<p class="crumbs"><a href="/">Home</a> · <a href="/category/{post['cat']}/">{cat_name}</a> · {html.escape(prod['short'])}</p>
<h1>{html.escape(post['title'])}</h1>
<p class="meta">By the IndieLab editors · Updated {DATE_HUMAN} · 3 min read</p>
<img class="hero" src="/img/{post['hero']}.jpg" alt="{html.escape(post['title'])} — {html.escape(prod['short'])}" width="1200" height="788">
<div class="disc">This post contains affiliate links. If you buy through them, IndieLab may earn a commission at no extra cost to you. <a href="/affiliate-disclosure/">How this works</a></div>
<p class="lede">{lede}</p>
<h2>Why does the {prod['short'].lower()} make the list?</h2>
<ul>{points}</ul>
{secs}
<img class="mid" src="/img/{post['second']}.jpg" alt="{html.escape(prod['name'])} in a home setting" loading="lazy" width="1200" height="713">
<div class="buybox">
<img src="/img/{post['buyimg']}.jpg" alt="{html.escape(prod['name'])}" loading="lazy" width="360" height="396">
<div>
<h3>{html.escape(prod['name'])}</h3>
<p>{html.escape(prod['blurb'])}</p>
<a class="btn" href="{prod['link']}" rel="nofollow sponsored noopener" target="_blank">Check price on Amazon</a>
<p style="font-size:13px;color:var(--muted);margin-top:10px">As an Amazon Associate, IndieLab earns from qualifying purchases.</p>
</div></div>
<h2>When should you order it?</h2>
<p>Order by mid-December to be safe — delivery windows stretch in the last two weeks, and popular gift picks do sell out. Prices also move through the season, so the price on the Amazon page today may not be the price tomorrow. Check the size, colour and pack options before ordering; the most-gifted variant is not always the default one.</p>
<h2>Questions, answered</h2>
{faq_html}
<h2>Keep exploring</h2>
<div class="rel">{rel_html}</div>
<p style="margin-top:18px">More in <a href="/category/{post['cat']}/">{cat_name}</a> · See all <a href="/products/">top picks</a></p>
"""
    return body, ld

def page(path, content):
    full = os.path.join(DIST, path.strip("/"), "index.html") if path != "/" else os.path.join(DIST, "index.html")
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w") as f:
        f.write(content)

def build():
    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(os.path.join(DIST, "img"))
    for f in os.listdir(IMG_SRC):
        if f.endswith((".jpg", ".gif")):
            shutil.copy(os.path.join(IMG_SRC, f), os.path.join(DIST, "img", f))
    with open(os.path.join(DIST, "styles.css"), "w") as f:
        f.write(CSS.strip())
    with open(os.path.join(DIST, "vercel.json"), "w") as f:
        json.dump({"cleanUrls": True}, f)
    for fav in ("favicon.ico", "favicon-32.png", "favicon-192.png", "favicon-512.png", "apple-touch-icon.png"):
        src_f = os.path.join(ROOT, fav)
        if os.path.exists(src_f):
            shutil.copy(src_f, os.path.join(DIST, fav))

    urls = ["/"]
    # ---- posts
    for post in POSTS:
        body, ld = post_body(post)
        content = head(f"{post['title']} — {SITE_NAME}", meta_desc(post), f"/blog/{post['slug']}/", extra=ld, ogimg=post["hero"]) \
            + f'<article class="post">{body}</article>' + FOOT
        page(f"/blog/{post['slug']}/", content)
        urls.append(f"/blog/{post['slug']}/")
    # ---- categories
    for cslug, (cname, cimg, cint) in CATEGORIES.items():
        posts = [p for p in POSTS if p["cat"] == cslug]
        cards = "".join(card(p) for p in posts)
        content = head(f"{cname} — {SITE_NAME}", f"{cname}: {cint}", f"/category/{cslug}/", ogimg=cimg) + f"""
<div class="wrap">
<div class="masthead"><p class="kicker">Gift guides</p><h1 style="font-size:clamp(32px,4.4vw,48px)">{cname}</h1>
<p>{cint}</p></div>
<div class="grid" style="margin-top:24px">{cards}</div>
</div>""" + FOOT
        page(f"/category/{cslug}/", content)
        urls.append(f"/category/{cslug}/")
    # ---- home (dense: feature, picks, categories, latest, trending)
    feat = POSTS[0]
    featprod = PRODUCTS[feat["product"]]
    picks_html = ""
    for key in ("blanket", "mask", "thermo", "fairy", "lamp", "chopper"):
        pr = PRODUCTS[key]
        pool = image_pool(key)
        picks_html += f"""<div class="pick"><img src="/img/{pool[0]}.jpg" alt="{html.escape(pr['name'])}" loading="lazy" width="164" height="164">
<div><h3>{html.escape(pr['name'])}</h3><p>{html.escape(pr['blurb'])}</p>
<p><a href="{pr['link']}" rel="nofollow sponsored noopener" target="_blank">Check price on Amazon</a></p></div></div>"""
    cats_html = ""
    for cslug, (cname, cimg, cint) in CATEGORIES.items():
        n = len([p for p in POSTS if p["cat"] == cslug])
        cats_html += f"""<div class="cat-card"><a href="/category/{cslug}/">
<img src="/img/{cimg}.jpg" alt="{cname}" loading="lazy" width="720" height="428">
<div class="lbl"><h3>{cname}</h3><p>{n} gift guides</p></div></a></div>"""
    latest = "".join(card(p) for p in POSTS[1:10])
    trend_posts = [POSTS[i] for i in (24, 11, 32, 40, 4, 15)]
    trend = "".join(f'<a href="/blog/{p["slug"]}/">{html.escape(p["title"])}</a>' for p in trend_posts)
    home = head(f"{SITE_NAME} — {TAGLINE}", "IndieLab tracks what shoppers search for on Pinterest and Amazon, then writes the short, honest guide for each find — who it suits, how to gift it, and where to get it.", "/") + f"""
<div class="wrap">
<div class="masthead hero-grid">
<div>
<p class="kicker">Gift guides · Cozy home · Kitchen finds</p>
<h1>Gifts people actually use, found without the doom-scroll.</h1>
<p>IndieLab tracks what shoppers search for on Pinterest and Amazon, then writes the short, honest guide for each find — who it suits, how to gift it, and where to get it.</p>
<div class="chips">
<a href="/category/gifts-for-mom/">For Mom</a><a href="/category/gifts-for-her/">For Her</a><a href="/category/gifts-for-him/">For Him</a><a href="/category/stocking-stuffers/">Under the tree: stocking stuffers</a><a href="/products/">Top picks</a>
</div>
</div>
<div class="hero-gif"><img src="/img/cozy.gif" alt="A cat asleep under a cozy plaid blanket while fairy lights twinkle" width="500" height="334"></div>
</div>
<div class="feature">
<img src="/img/{feat['hero']}.jpg" alt="{html.escape(feat['title'])}" width="980" height="833">
<div>
<p class="kicker">Featured guide</p>
<h2>{html.escape(feat['title'])}</h2>
<p>{html.escape(featprod['blurb'])} Who it suits, what to check before you buy, and how to gift it well — in one short read.</p>
<a class="btn" href="/blog/{feat['slug']}/">Read the guide</a>
</div>
</div>
<h2 class="sec">This season's top picks</h2>
<div class="picks">{picks_html}</div>
<h2 class="sec">Shop by who you're buying for</h2>
<div class="cats">{cats_html}</div>
<h2 class="sec">Trending searches</h2>
<div class="chips">{trend}</div>
<h2 class="sec">Latest gift guides</h2>
<div class="grid">{latest}</div>
<p style="margin-top:22px">Looking for something specific? Start with the <a href="/products/">top picks</a> or browse <a href="/category/cozy-home/">cozy home</a> and <a href="/category/kitchen-gadgets/">kitchen gadgets</a>.</p>
</div>""" + FOOT
    page("/", home)
    # ---- products
    rows = ""
    for key, pr in PRODUCTS.items():
        pool = image_pool(key)
        pts = "".join(f"<li>{p}</li>" for p in pr["points"])
        rows += f"""<div class="buybox">
<img src="/img/{pool[0]}.jpg" alt="{html.escape(pr['name'])}" loading="lazy" width="360" height="396">
<div><h3>{html.escape(pr['name'])}</h3><p>{html.escape(pr['blurb'])}</p><ul>{pts}</ul>
<a class="btn" href="{pr['link']}" rel="nofollow sponsored noopener" target="_blank">Check price on Amazon</a></div></div>"""
    page("/products/", head(f"Top Picks — {SITE_NAME}", "The IndieLab top picks: the gift and home finds our guides keep coming back to, each with an honest summary and a direct Amazon link.", "/products/") + f"""
<article class="post" style="max-width:860px">
<p class="kicker">Top picks</p>
<h1>The finds our guides keep coming back to</h1>
<p class="lede">Six products, one standard: we would gift every one of these ourselves. Each links straight to Amazon — prices there are the live ones.</p>
{rows}
</article>""" + FOOT)
    urls.append("/products/")
    # ---- about / disclosure / privacy
    page("/about/", head(f"About — {SITE_NAME}", "About IndieLab: how we pick the gift and home finds we write about.", "/about/") + """
<article class="post">
<p class="kicker">About</p>
<h1>What IndieLab is</h1>
<p>IndieLab is a small gift-guide publication. We watch what people actually search for and save on Pinterest and Amazon, then write the guide we would want before buying: who the product suits, what to check, what the honest downsides are, and how to gift it well.</p>
<h2>How we pick</h2>
<p>Every pick starts as a search trend — real people looking for a real problem to solve. We check the listing, the variants and the details that matter before writing. If a product has a limitation worth knowing, it goes in the guide, not under the rug.</p>
<h2>How we earn</h2>
<p>Guides contain Amazon affiliate links. If you buy through one, we may earn a commission at no extra cost to you. That is the whole business model — no paid placements, no sponsored rankings. See the <a href="/affiliate-disclosure/">affiliate disclosure</a>.</p>
</article>""" + FOOT)
    urls.append("/about/")
    page("/affiliate-disclosure/", head(f"Affiliate Disclosure — {SITE_NAME}", "IndieLab's affiliate disclosure: Amazon Associates participation and how commissions work.", "/affiliate-disclosure/") + """
<article class="post">
<p class="kicker">Disclosure</p>
<h1>Affiliate disclosure</h1>
<p>IndieLab (indielab.online) is a participant in the Amazon Services LLC Associates Program, an affiliate advertising program designed to provide a means for sites to earn advertising fees by advertising and linking to Amazon.com. As an Amazon Associate, IndieLab earns from qualifying purchases.</p>
<p>Product links on this site are affiliate links. If you click one and make a purchase, we may receive a small commission — at no additional cost to you. Prices and availability shown on Amazon at the time of purchase apply.</p>
<p>Commissions never decide what we recommend. Products appear in our guides because shoppers search for them and because they pass our checks; the honest limitations of every pick are printed in its guide.</p>
</article>""" + FOOT)
    urls.append("/affiliate-disclosure/")
    page("/privacy-policy/", head(f"Privacy Policy — {SITE_NAME}", "IndieLab privacy policy: analytics, cookies and affiliate links explained plainly.", "/privacy-policy/") + """
<article class="post">
<p class="kicker">Privacy</p>
<h1>Privacy policy</h1>
<p>This site is a static publication: it has no accounts, no comments and no forms, and it does not collect names or email addresses.</p>
<h2>Analytics</h2>
<p>We use Google Analytics to understand which guides get read, so we can write more of the useful kind. Google Analytics uses cookies and records anonymous usage data such as pages visited, device type and approximate region. You can block cookies in your browser settings at any time.</p>
<h2>Affiliate links</h2>
<p>Links to Amazon are affiliate links. When you follow one, Amazon's own privacy policy governs what happens on their site, including any purchase you make.</p>
<h2>Changes</h2>
<p>If this policy changes, the new version will be posted on this page.</p>
</article>""" + FOOT)
    urls.append("/privacy-policy/")
    # ---- admin (static overview)
    stat = f"""<div class="stat">
<div class="box"><div class="num">{len(POSTS)}</div><div class="lab">Published guides</div></div>
<div class="box"><div class="num">{len(PRODUCTS)}</div><div class="lab">Products tracked</div></div>
<div class="box"><div class="num">{len(CATEGORIES)}</div><div class="lab">Categories</div></div>
<div class="box"><div class="num">{'Live' if GA_ID != 'G-XXXXXXXXXX' else 'Not set'}</div><div class="lab">Google Analytics ({GA_ID})</div></div>
</div>"""
    prod_rows = "".join(f"<tr><td>{html.escape(pr['name'])}</td><td><a href=\"{pr['link']}\">{pr['link']}</a></td></tr>" for pr in PRODUCTS.values())
    post_rows = "".join(f"<tr><td><a href=\"/blog/{p['slug']}/\">{html.escape(p['title'])}</a></td><td>{CATEGORIES[p['cat']][0]}</td><td>{PRODUCTS[p['product']]['short']}</td></tr>" for p in POSTS)
    page("/admin/", head(f"Admin — {SITE_NAME}", "IndieLab admin overview.", "/admin/", extra='<meta name="robots" content="noindex,nofollow">') + f"""
<div class="wrap">
<div class="masthead"><p class="kicker">Admin</p><h1 style="font-size:40px">Site overview</h1></div>
{stat}
<div class="note">This dashboard is a static overview generated at build time. To publish or change content, edit <strong>build.py</strong>, rebuild, and push — Vercel redeploys automatically. GA4 reports live data at analytics.google.com.</div>
<h2 class="sec">Products &amp; affiliate links</h2>
<table class="admin"><tr><th>Product</th><th>Affiliate link</th></tr>{prod_rows}</table>
<h2 class="sec">All guides</h2>
<table class="admin"><tr><th>Title</th><th>Category</th><th>Product</th></tr>{post_rows}</table>
</div>""" + FOOT)
    # ---- sitemap + robots
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        sm.append(f"<url><loc>{SITE}{u}</loc><lastmod>{DATE}</lastmod></url>")
    sm.append("</urlset>")
    with open(os.path.join(DIST, "sitemap.xml"), "w") as f:
        f.write("\n".join(sm))
    with open(os.path.join(DIST, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /admin/\n\nSitemap: {SITE}/sitemap.xml\n")
    print(f"Built {len(POSTS)} posts, {len(CATEGORIES)} categories, home, products, about, disclosure, privacy, admin → dist/")

if __name__ == "__main__":
    build()
