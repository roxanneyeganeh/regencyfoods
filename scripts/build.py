"""Mix & match preview: every favourite section variant on one page, switched by a panel."""
import re, html

SRC = "/home/claude/regency-docket"
OUT = "/home/claude/regency-mix"
page = open(f"{SRC}/index.html").read()

def block(name):
    m = re.search(r"<!-- =+ " + re.escape(name) + r".*?=+ -->(.*?)(?=<!-- =+ |\Z)", page, re.S)
    return m.group(1)

head = page[: page.index("<!-- ============ Announcement")]
announce = block("Announcement")
header = block("Header")
shelf = block("Our own range")
trade_underline = block("Trade").replace('class="trade" id="trade"', 'class="trade"')
news = block("Newsletter").replace("</main>", "").replace('id="news" ', "")
footer = block("Footer")
basket = block("Basket").replace('<script src="app.js"></script>', "")

CRED = {l.split("\t")[0]: l.rstrip("\n").split("\t")[3] for l in open("/tmp/claude-0/-home-claude/d0a19366-6672-59fb-a77b-6d5132b4e39d/scratchpad/unsplash/opts.tsv")}
ALT = {
    "H1": "Pizza slices on a bright orange background", "H2": "A tomato with basil and cheese on yellow",
    "H3": "Vine tomatoes on a blue and yellow background", "H4": "Oranges on colour-blocked paper",
    "H5": "Pastries, pizza and salad on a blue background", "H6": "Mango and a red pepper on pink and yellow",
    "H7": "Crates of fresh vegetables at a market stall", "H8": "Fresh ingredients laid out on a wooden table",
    "K1": "A chef cooking under copper lamps", "K2": "Chefs plating dishes on the pass", "K3": "A chef plating a dish",
    "K4": "A chef at work in a professional kitchen", "K5": "A plated dish being finished",
}

# ---------------------------------------------------------------- image map (each file referenced once, in JS)
IMG = {f"{c}": f"assets/img/opts/{c}.jpg" for c in ["H1","H2","H3","H4","H5","H6","H7","H8","K1","K2","K3","K4","K5","D4","P3"]}
IMG.update({
    "packs": "assets/img/hero-set.jpg", "box": "assets/img/yours/hero-stack.jpg", "pouch": "assets/img/yours/pecan-hero.jpg",
    "kitchen": "assets/img/yours/kitchen.jpg",
    "y-meat": "assets/img/yours/cat-meat.jpg", "y-frozen": "assets/img/yours/cat-frozen.jpg", "y-drinks": "assets/img/yours/cat-drinks.jpg",
    "y-alcohol": "assets/img/yours/cat-wine.jpg", "y-snacks": "assets/img/yours/choice.jpg",
    "n-meat": "assets/img/u-meat.jpg", "n-frozen": "assets/img/u-frozen.jpg", "n-alcohol": "assets/img/u-alcohol.jpg",
    "van": "assets/img/van.jpg", "vancut": "assets/img/van-cut.png",
})
ALT.update({"packs": "Regency Foods Almond, Pecan and Pistachio packs", "box": "A Regency Foods box filled with store-cupboard favourites",
            "pouch": "A Regency Foods pecan pouch", "kitchen": "Chefs at work in a busy restaurant kitchen"})

# ---------------------------------------------------------------- categories
CATS = [  # key, name, bento name, bento sub, note, yours, new, aisle?
    ("meat", "Meat &amp; Seafood", "Meat &amp; Seafood", "Fresh and frozen cuts", "Fresh &amp; frozen", "y-meat", "n-meat", True),
    ("frozen", "Frozen Foods", "Frozen Foods", "", "&minus;18&deg;C", "y-frozen", "n-frozen", True),
    ("drinks", "Soft Drinks", "Soft Drinks", "", "Juices &amp; sodas", "y-drinks", "D4", True),
    ("alcohol", "Alcohol &amp; Spirits", "Alcohol &amp; Spirits", "", "By the case", "y-alcohol", "n-alcohol", True),
    ("nuts", "Nuts &amp; Seeds", "Nuts &amp; Seeds", "", "1 kg bags", "pouch", "packs", False),
    ("snacks", "Snacks &amp; Store Cupboard", "Snacks, Sweets &amp; Store Cupboard", "The everyday range", "Everyday range", "y-snacks", "P3", True),
]
CAT_ALT = {"meat": "Meat and seafood", "frozen": "Frozen foods", "drinks": "Soft drinks", "alcohol": "Wine and spirits",
           "nuts": "Regency Foods nuts", "snacks": "Snacks and store-cupboard goods"}
def href(c):
    name = re.sub("<[^>]+>", "", html.unescape(c[1]))
    return 'href="#range"' if not c[7] else f'href="#shop" data-aisle="{html.escape(name)}"'
def cimg(c, cls=""):
    return f'<img{(" class=%s" % chr(34) + cls + chr(34)) if cls else ""} data-cat="{c[0]}" alt="{CAT_ALT[c[0]]}" loading="lazy">'

ARROW = '<span class="mx-arw" aria-hidden="true"><svg viewBox="0 0 24 24" width="16" height="16"><path d="M5 12h13M13 6l6 6-6 6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'

SEC_HEAD = '<div class="sec-head"><h2 id="{id}">Shop by category</h2><p>{p}</p></div>'

bento = "".join(
    f'<li class="bn-{c[0]}"><a class="bn-tile" {href(c)}>{cimg(c)}<span class="bn-pill"><span><b>{c[2]}</b>'
    + (f'<small>{c[3]}</small>' if c[3] else "") + f'</span>{ARROW}</span></a></li>' for c in CATS)
cat_bento = f"""
<section class="mx-cats mx-bento" aria-labelledby="catT1">
  <div class="wrap">
    {SEC_HEAD.format(id="catT1", p="One supplier for the whole kitchen. Browse the shelves, or tell us what your menu needs and we will stock it.")}
    <ul class="bn-grid">{bento}</ul>
  </div>
</section>"""

ing_words = ", ".join(
    (f'<a {href(c)}><u>{c[1]}</u></a>' if c[0] == "nuts" else f'<a {href(c)}>{c[1] if c[0] != "snacks" else "Snacks, Sweets, Store Cupboard"}</a>')
    for c in CATS)
ing_cells = "".join(
    f'<li><a class="ig-cell" {href(c)}><span class="ig-img">{cimg(c)}</span><span class="ig-cap"><b>{c[1].replace(" &amp; Store", " &amp;<br>Store") if c[0]=="snacks" else c[1]}</b><small>{c[4]}</small></span></a></li>' for c in CATS)
cat_ing = f"""
<section class="mx-cats mx-ing" aria-labelledby="catT2">
  <div class="wrap">
    <h2 class="ig-list" id="catT2"><span class="ig-k">Ingredients:</span> {ing_words}.</h2>
    <p class="ig-small">For allergens, see ingredients in <b>bold</b>. May contain everything your menu needs.</p>
    <ul class="ig-grid">{ing_cells}</ul>
  </div>
</section>"""

tall = "".join(f'<li><a class="a-cat" {href(c)}>{cimg(c)}<span class="a-cat-name"><span>{c[1]}</span><span aria-hidden="true">→</span></span></a></li>' for c in CATS)
cat_tall = f"""
<section class="a-cats" aria-labelledby="catT3">
  <div class="wrap">
    {SEC_HEAD.format(id="catT3", p="One supplier for the whole kitchen, from fresh cuts to the store cupboard.")}
    <ul class="a-cat-grid">{tall}</ul>
  </div>
</section>"""

rows = "".join(f'<li><a class="b-row" {href(c)} data-pv="{c[0]}"><span class="b-num">0{i+1}</span><span class="b-name">{c[1]}</span>{cimg(c, "b-thumb")}<span class="b-go">{"See our range" if not c[7] else "Shop the aisle"} <span aria-hidden="true">→</span></span></a></li>' for i, c in enumerate(CATS))
cat_index = f"""
<section class="b-cats" aria-labelledby="catT4">
  <div class="wrap b-cats-grid">
    <div><h2 id="catT4">Shop by category</h2><ol class="b-list">{rows}</ol></div>
    <div class="b-preview" aria-hidden="true"><img id="bPreview" data-cat="meat" alt=""></div>
  </div>
</section>"""

# ---------------------------------------------------------------- hero
hero = """
<section class="b-hero mx-hero" aria-labelledby="heroTitle">
  <div class="b-hero-copy"><div class="b-hero-in">
    <span class="est" role="img" aria-label="est. 1995"></span>
    <h1 id="heroTitle">Premium quality goods, at your door tomorrow.</h1>
    <p class="lead">From everyday essentials to premium ingredients, we supply professional kitchens and home cooks across the UK, next day from our North London hub.</p>
    <div class="ctas">
      <a class="btn btn--cream" href="#shop">Shop by category <span aria-hidden="true">→</span></a>
      <a class="btn btn--line-cream" href="#trade">Supply my kitchen</a>
    </div>
  </div></div>
  <div class="b-hero-img"><img data-hero alt="" fetchpriority="high"></div>
</section>"""

# ---------------------------------------------------------------- trust strip
CLIENTS = ["Balans", "Park Chinois", "Meta", "Lush", "Smoky Boys"]
STARS = '<span class="mx-stars" aria-hidden="true">' + "".join('<i><svg viewBox="0 0 24 24" width="14" height="14"><path d="M12 2.8l2.8 6 6.5.7-4.9 4.4 1.4 6.4L12 17l-5.8 3.3 1.4-6.4L2.7 9.5l6.5-.7z" fill="currentColor"/></svg></i>' for _ in range(5)) + "</span>"
trust = f"""
<section class="mx-trust" aria-label="Some of our customers">
  <div class="wrap">
    <p class="mx-trust-k">Trusted by 1,000+ leading venues, restaurants and caterers across the UK</p>
    <ul class="mx-trust-grid">{"".join(f"<li>{c.upper() if c in ('Balans','Lush') else c}</li>" for c in CLIENTS)}</ul>
    <p class="mx-trust-score">{STARS}<b>4.9</b> · Excellent on Trustpilot</p>
  </div>
</section>"""

# ---------------------------------------------------------------- delivery
STEPS = """
      <ol class="steps3">
        <li><h3>Today</h3><p>You order online or through your trade account, from a single bag to a full weekly restock.</p></li>
        <li><h3>Tonight</h3><p>Your order is picked, checked and packed at our North London hub.</p></li>
        <li><h3>Tomorrow</h3><p>It arrives at your door, so your kitchen is never left waiting.</p></li>
      </ol>"""
TIMER = '<p class="timer-line"><span class="dot" aria-hidden="true"></span>Tomorrow starts in <span class="t" data-timer>00:00:00</span></p>'
del_salmon = """
<section class="mx-salmon" aria-labelledby="delT1">
  <div class="wrap mx-salmon-grid">
    <div>
      <p class="mx-tag">Service</p>
      <h2 id="delT1">Ordered today. Served tomorrow.</h2>
      <ol class="mx-course">
        <li><span>Order in</span><div><h3>You place the order</h3><p>Online, from a single bag to a full weekly restock.</p></div></li>
        <li><span>Prep</span><div><h3>Picked &amp; packed</h3><p>Checked at our North London hub.</p></div></li>
        <li><span>Service</span><div><h3>On your doorstep tomorrow</h3><p>Fast, next-day delivery nationwide, so you are never left waiting.</p></div></li>
      </ol>
    </div>
    <div class="mx-salmon-van"><img data-k="van" alt="The yellow Regency Foods delivery van" loading="lazy"></div>
  </div>
</section>"""
del_green = f"""
<section class="a-deliv" aria-labelledby="delT2">
  <div class="wrap a-deliv-grid">
    <div class="a-deliv-copy">
      <h2 id="delT2">Need it tomorrow? Consider it done.</h2>
      <p>Our North London hub ensures fast, next-day delivery nationwide, so you're never left waiting.</p>
      {TIMER}
    </div>
    <div class="a-van" data-drive><img data-k="vancut" alt="The yellow Regency Foods delivery van" loading="lazy"></div>
  </div>
  <div class="wrap">{STEPS}
  </div>
</section>"""
del_blue = f"""
<section class="c-deliv" aria-labelledby="delT3">
  <div class="wrap c-deliv-in">
    <h2 id="delT3">Need it tomorrow? <span>Consider it done.</span></h2>
    <img class="c-van" data-k="vancut" alt="The yellow Regency Foods delivery van" loading="lazy">
    <p class="c-deliv-lead">Our North London hub ensures fast, next-day delivery nationwide, so you're never left waiting.</p>
    {TIMER}{STEPS}
  </div>
</section>"""

# ---------------------------------------------------------------- story
pills = lambda: '<ul class="mx-pills">' + "".join(f"<li>{c}</li>" for c in CLIENTS) + "</ul>"
story_light = f"""
<section class="mx-story-light" aria-labelledby="stT1">
  <div class="wrap mx-sl-grid">
    <figure class="mx-sl-photo"><img data-story alt="" loading="lazy"><figcaption>Designed for busy kitchens</figcaption></figure>
    <div class="mx-sl-copy">
      <p class="mx-tag mx-tag--orange">Since 1995</p>
      <h2 id="stT1">Founded by a restaurateur. <em>We speak kitchen.</em></h2>
      <p>We understand the importance of quality, efficiency and reliability in every kitchen, because we ran one. Today Regency Foods delivers high-quality products at competitive prices to restaurants, hotels, pubs and more.</p>
      <p class="mx-small">Some of our regulars</p>
      {pills()}
      <p class="mx-score"><b>4.9</b> Excellent on Trustpilot · trusted by 1,000+ venues</p>
    </div>
  </div>
</section>"""
story_dark = f"""
<section class="mx-story-dark" aria-labelledby="stT2">
  <div class="wrap mx-sd-grid">
    <div class="mx-sd-copy">
      <p class="mx-tag mx-tag--yellow">Supplying kitchens since 1995</p>
      <h2 id="stT2">Designed for busy kitchens.</h2>
      <p>Founded by a former restaurateur, we understand the importance of quality, efficiency and reliability in every kitchen. Today we deliver high-quality products at competitive prices to restaurants, hotels, pubs and more.</p>
      {pills()}
      <p class="mx-score">Trusted by 1,000+ venues · 4.9 Excellent on Trustpilot</p>
    </div>
    <div class="mx-sd-photo"><img data-story alt="" loading="lazy"></div>
  </div>
</section>"""

# ---------------------------------------------------------------- trade
TYPES = "<option>Restaurant</option><option>Hotel</option><option>Pub or bar</option><option>Caterer</option><option>Café</option><option>Retailer</option><option>Other</option>"
trade_table = f"""
<section class="mx-table" aria-labelledby="trT1">
  <div class="wrap mx-table-grid">
    <div class="mx-table-copy">
      <p class="mx-tag">For restaurants, hotels &amp; pubs</p>
      <h2 id="trT1">Book a table at the trade counter.</h2>
      <p>Open a trade account for wholesale pricing and next-day delivery from our North London hub. Or just leave your email for new arrivals and offers.</p>
    </div>
    <form class="mx-card" data-mx-form novalidate aria-labelledby="trT1">
      <div class="mx-card-top mx-tag-row"><span class="mx-tag">Reservation</span><span class="mx-tag">Trade account</span></div>
      <div class="mx-two">
        <div class="field"><label for="t1n">Name</label><input id="t1n" autocomplete="name" required></div>
        <div class="field"><label for="t1b">Business</label><input id="t1b" autocomplete="organization" required data-biz></div>
      </div>
      <div class="field"><label for="t1e">Work email</label><input id="t1e" type="email" autocomplete="email" required></div>
      <div class="field"><label for="t1v">Venue</label><select id="t1v">{TYPES}</select></div>
      <p class="err" aria-live="polite"></p>
      <button class="mx-wide" type="submit">Request my account <span aria-hidden="true">→</span></button>
    </form>
  </div>
</section>"""

# boxed + numbered version of the green trade section
trade_boxed = (trade_underline
    .replace('class="trade"', 'class="trade trade--boxed"')
    .replace('aria-labelledby="tradeTitle"', 'aria-labelledby="tradeTitle2"').replace('id="tradeTitle"', 'id="tradeTitle2"')
    .replace('<h2 id="tradeTitle2">', '<p class="mx-tag mx-tag--yellow">Trade</p><h2 id="tradeTitle2">')
    .replace('id="apply"', "")
    .replace('class="form-ticket" id="tradeForm"', 'class="form-ticket" data-mx-form').replace('aria-labelledby="tfTitle"', 'aria-labelledby="tfTitle2"').replace('id="tfTitle"', 'id="tfTitle2"')
    .replace('id="tfErr"', "")
    .replace("Tell us about your kitchen. An account manager", "Tell us about your kitchen and an account manager")
    .replace('<label for="tfBiz">Business</label>', '<label for="tfBiz">Business name</label>')
    .replace('class="btn btn--green" type="submit">Request an account', 'class="btn btn--green mx-wide-btn" type="submit">Request a trade account')
    .replace("For example: meat, frozen and dry goods", "For example: weekly nuts and dry goods")
    .replace("Trusted by 1,000+ venues, including", "Trusted by 1,000+ venues, restaurants and caterers, including"))
for f in ["tfName", "tfBiz", "tfEmail", "tfPhone", "tfType", "tfMsg"]:
    trade_boxed = trade_boxed.replace(f'"{f}"', f'"{f}2"')
trade_boxed = trade_boxed.replace('id="tfBiz2"', 'id="tfBiz2" data-biz')
trade_boxed = re.sub(r'<ul class="perks">.*?</ul>', """<ul class="perks perks--num">
          <li><b>Next-day delivery</b><span>Order today and it arrives tomorrow, from our North London hub to kitchens across the UK.</span></li>
          <li><b>An account manager who knows your menu</b><span>We work closely with you to keep orders smooth, stock consistent and kitchens running.</span></li>
          <li><b>Built for the fusion kitchen</b><span>Flavour, flexibility and fast turnaround, so you can create modern menus without compromise.</span></li>
        </ul>""", trade_boxed, flags=re.S)

trade_cards = """
<section class="mx-cards" aria-label="Trade accounts and newsletter">
  <div class="wrap mx-cards-grid">
    <form class="mx-c mx-c--green" data-mx-form novalidate aria-labelledby="trT4">
      <p class="mx-tag">Trade accounts</p>
      <h2 id="trT4">Make tomorrow a standing order.</h2>
      <p>Wholesale pricing for restaurants, hotels, pubs and caterers, plus 10% off when you subscribe to a repeat order.</p>
      <div class="mx-two">
        <label class="sr" for="t4n">Your name</label><input id="t4n" placeholder="Your name" autocomplete="name" required>
        <label class="sr" for="t4b">Business name</label><input id="t4b" placeholder="Business name" autocomplete="organization" required data-biz>
      </div>
      <label class="sr" for="t4e">Work email</label><input id="t4e" type="email" placeholder="Work email" autocomplete="email" required>
      <p class="err" aria-live="polite"></p>
      <button class="mx-c-btn" type="submit">Request a trade account <span aria-hidden="true">→</span></button>
    </form>
    <form class="mx-c mx-c--orange" data-mx-news novalidate aria-labelledby="trT5">
      <p class="mx-tag">Get the latest</p>
      <h2 id="trT5">Subscribe now.</h2>
      <p>Discover the finest selection of quality foods, stay up to date with our newest arrivals, and enjoy exclusive offers.</p>
      <label class="sr" for="t5e">Email address</label><input id="t5e" type="email" placeholder="Email address" autocomplete="email" required>
      <p class="err" aria-live="polite"></p>
      <button class="mx-c-btn" type="submit">Subscribe</button>
    </form>
  </div>
</section>"""

def slot(name, anchor, variants):
    inner = "".join(f'\n<div class="mx-v" data-slot="{name}" data-v="{k}" hidden>{v}</div>' for k, v in variants)
    return f'\n<!-- ===== {name} -->\n<div class="mx-slot" id="{anchor}" data-slot-wrap="{name}">{inner}\n</div>'

body = (
    slot("hero", "top", [("split", hero)])
    + slot("cats", "shop", [("bento", cat_bento), ("ingredients", cat_ing), ("tall", cat_tall), ("index", cat_index)])
    + slot("trust", "trust", [("on", trust), ("off", "")])
    + shelf
    + slot("deliv", "delivery", [("salmon", del_salmon), ("green", del_green), ("blue", del_blue)])
    + slot("story", "story", [("light", story_light), ("dark", story_dark)])
    + slot("trade", "trade", [("table", trade_table), ("boxed", trade_boxed), ("underline", trade_underline), ("cards", trade_cards)])
    + f'\n<div data-news-wrap>{news}</div>'
)

names = ["Tamas Pap"]  # placeholder replaced below
used = [c for c in IMG if c in CRED]
credit_names = list(dict.fromkeys(["AM FL", "Anita Austvika", "Shourav Sheikh"] + [CRED[c] for c in used]))
foot = re.sub(r'<p class="credits">.*?</p><div hidden></div>',
              f'<p class="credits">Photography: Regency Foods, and Unsplash ({", ".join(credit_names)}).</p>', footer, flags=re.S)

panel = open(f"{OUT}/panel.html").read()
imgjs = "window.MX_IMG = {\n" + ",\n".join(f'  "{k}": "{v}"' for k, v in IMG.items()) + "\n};\nwindow.MX_ALT = " + repr({k: v for k, v in ALT.items()}).replace("'", '"') + ";"

h = head.replace('<link rel="stylesheet" href="styles.css">',
                 '<link rel="stylesheet" href="styles.css">\n<link rel="stylesheet" href="layouts.css">\n<link rel="stylesheet" href="mix.css">')
h = re.sub(r"<title>.*?</title>", "<title>Regency Mix &amp; Match</title>", h)
out = (h + announce + header + '\n<main id="main">' + body + "\n</main>\n" + foot + basket + panel
       + f"\n<script>\n{imgjs}\n</script>\n<script src=\"mix.js\"></script>\n<script src=\"app.js\"></script>\n</body>\n</html>\n")
open(f"{OUT}/index.html", "w").write(out)
print(len(out), "used credits:", credit_names)
