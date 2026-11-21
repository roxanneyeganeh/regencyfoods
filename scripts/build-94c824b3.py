"""Builds three layout options (a.html, b.html, c.html) from the current site.
Shared sections are sliced from the live page; each layout supplies its own
hero, category, delivery (van) and story sections."""
import re, shutil, os

SRC = "/home/claude/regency-docket"
OUT = "/home/claude/regency-layouts"
shutil.copy(f"{SRC}/styles.css", f"{OUT}/styles.css")
shutil.copy(f"{SRC}/app.js", f"{OUT}/app.js")
page = open(f"{SRC}/index.html").read()

def block(name):
    m = re.search(r"<!-- =+ " + re.escape(name) + r".*?=+ -->(.*?)(?=<!-- =+ |\Z)", page, re.S)
    return m.group(1)

head = page[: page.index("<!-- ============ Announcement")]
announce = "<!-- announce -->" + block("Announcement")
header = block("Header")
shelf = block("Our own range")
trade = block("Trade")
news = block("Newsletter").replace("</main>", "")
footer = block("Footer")
basket = block("Basket").replace('<script src="app.js"></script>', "")

CATS = [
    ("Meat &amp; Seafood", "Meat & Seafood", "assets/img/u-meat.jpg", "Prawns on blue crushed ice"),
    ("Frozen Foods", "Frozen Foods", "assets/img/u-frozen.jpg", "An ice lolly against a bright blue sky"),
    ("Soft Drinks", "Soft Drinks", "{drinks}", "{drinks_alt}"),
    ("Alcohol &amp; Spirits", "Alcohol & Spirits", "assets/img/u-alcohol.jpg", "Three layered cocktails on an orange background"),
    ("Nuts &amp; Seeds", None, "assets/img/hero-set.jpg", "Regency Foods Almond, Pecan and Pistachio packs"),
    ("Snacks &amp; Store Cupboard", "Snacks & Store Cupboard", "{pantry}", "{pantry_alt}"),
]
ALT = {
    "H1": "Pizza slices on a bright orange background", "H2": "A tomato with basil and cheese on yellow",
    "H3": "Vine tomatoes on a blue and yellow background", "H4": "Oranges on colour-blocked paper",
    "H5": "Pastries, pizza and salad on a blue background", "H6": "Mango and a red pepper on pink and yellow",
    "H7": "Crates of fresh vegetables at a market stall", "H8": "Fresh ingredients laid out on a wooden table",
    "D1": "Rows of colourful drinks", "D2": "Fruit-infused drinks in glass jars", "D3": "A row of colourful frozen drinks",
    "D4": "A glass of lemonade on blue and pink", "D5": "Orange juice with a slice of lemon", "D6": "Three summer drinks outdoors",
    "P1": "Colourful pasta bows", "P2": "Spaghetti, tagliatelle and rigatoni", "P3": "Olive oil bottles on violet",
    "P4": "Spices piled high at a market", "P5": "Rigatoni close up", "P6": "Pasta in glass jars",
    "P7": "Pantry jars on open shelves", "P8": "A bottle of olive oil in sunlight",
    "K1": "A chef cooking under copper lamps", "K2": "Chefs plating dishes on the pass", "K3": "A chef plating a dish",
    "K4": "A chef at work in a professional kitchen", "K5": "A plated dish being finished",
    "M1": "Green crates of fresh vegetables", "M2": "Radishes and carrots at a market", "M3": "A street market stall",
    "M4": "Crates of vegetables at a market", "M5": "Wooden crates of squash and courgettes",
}
def img(code): return f"assets/img/opts/{code}.jpg"

def cats(drinks, pantry):
    out = []
    for i, (label, aisle, src, alt) in enumerate(CATS):
        src = src.format(drinks=img(drinks), pantry=img(pantry))
        alt = alt.format(drinks_alt=ALT[drinks], pantry_alt=ALT[pantry])
        out.append(dict(label=label, aisle=aisle, src=src, alt=alt, href="#range" if aisle is None else "#shop",
                        go="See our range" if aisle is None else "Shop the aisle"))
    return out

def a_attr(c):
    return f'href="{c["href"]}"' + (f' data-aisle="{c["label"]}"' if c["aisle"] else "")

STORY_TEXT = """
        <p class="big">Regency Foods started in 1995 with a simple goal: to deliver high-quality ingredients, reliably and quickly, to professional kitchens.</p>
        <div class="cols">
          <div>
            <p>Founded by a former restaurateur, we understand what chefs need: not just good products, but consistent service and support behind the scenes.</p>
            <p>Today, we supply restaurants, hotels, pubs and caterers across the UK, with next-day delivery from our North London hub.</p>
          </div>
          <div>
            <p>We've grown with the industry, expanding our range and embracing the rise of fusion cuisine. Our focus is on flavour, flexibility and fast turnaround.</p>
            <p>Now the same promise comes home: a bold, generous range for the pantry as well as the pass.</p>
          </div>
        </div>"""
VMP = """
    <div class="vmp">
      <div><h3>Vision</h3><p>To lead the UK wholesale food sector in delivering diverse, high-quality ingredients, with a specialty in fusion food, that inspire innovation and elevate culinary standards.</p></div>
      <div><h3>Mission</h3><p>To provide chefs and food businesses with fast, reliable access to premium ingredients and tailored support, blending tradition and modernity in every product we deliver.</p></div>
      <div><h3>How we work</h3><p>Generous, dependable and quietly playful. Professional in what we promise; joyful in how we show it. A trade supplier with the warmth of a family kitchen.</p></div>
    </div>"""
STEPS = """
      <ol class="steps3">
        <li><h3>Today</h3><p>You order online or through your trade account, from a single bag to a full weekly restock.</p></li>
        <li><h3>Tonight</h3><p>Your order is picked, checked and packed at our North London hub.</p></li>
        <li><h3>Tomorrow</h3><p>It arrives at your door, so your kitchen is never left waiting.</p></li>
      </ol>"""
HERO_COPY = """
        <span class="est" role="img" aria-label="est. 1995"></span>
        <h1 id="heroTitle">Premium quality goods, at your door tomorrow.</h1>
        <p class="lead">From everyday essentials to premium ingredients, we supply professional kitchens and home cooks across the UK, next day from our North London hub.</p>
        <div class="ctas">
          <a class="btn {primary}" href="#shop">Shop by category <span aria-hidden="true">→</span></a>
          <a class="btn {secondary}" href="#trade">Supply my kitchen</a>
        </div>"""
TIMER = '<p class="timer-line"><span class="dot" aria-hidden="true"></span>Tomorrow starts in <span class="t" data-timer>00:00:00</span></p>'

# ------------------------------------------------------------------ Layout A
def layout_a():
    c = cats("D4", "P3")
    hero = f"""
<section class="a-hero" aria-labelledby="heroTitle">
  <img class="a-hero-img" src="{img('H3')}" alt="{ALT['H3']}" fetchpriority="high">
  <div class="wrap a-hero-inner">
    <div class="a-hero-card">{HERO_COPY.format(primary='btn--green', secondary='')}
    </div>
  </div>
</section>"""
    cards = "".join(f'<li><a class="a-cat" {a_attr(x)}><img src="{x["src"]}" alt="{x["alt"]}" loading="lazy"><span class="a-cat-name"><span>{x["label"]}</span><span aria-hidden="true">→</span></span></a></li>' for x in c)
    catsec = f"""
<section class="a-cats" id="shop" aria-labelledby="shopTitle">
  <div class="wrap">
    <div class="sec-head"><h2 id="shopTitle">Shop by category</h2><p>One supplier for the whole kitchen, from fresh cuts to the store cupboard.</p></div>
    <ul class="a-cat-grid">{cards}</ul>
  </div>
</section>"""
    deliv = f"""
<section class="a-deliv" id="delivery" aria-labelledby="delTitle">
  <div class="wrap a-deliv-grid">
    <div class="a-deliv-copy">
      <h2 id="delTitle">Need it tomorrow? Consider it done.</h2>
      <p>Our North London hub ensures fast, next-day delivery nationwide, so you're never left waiting.</p>
      {TIMER}
    </div>
    <div class="a-van" data-drive><img src="assets/img/van-cut.png" alt="The yellow Regency Foods delivery van" loading="lazy"></div>
  </div>
  <div class="wrap">{STEPS}
  </div>
</section>"""
    story = f"""
<section class="story" id="story" aria-labelledby="storyTitle">
  <div class="wrap">
    <div class="story-grid"><div><h2 id="storyTitle">Thirty years on, the same promise.</h2></div><div>{STORY_TEXT}</div></div>
    <div class="a-story-photos">
      <img src="{img('K1')}" alt="{ALT['K1']}" loading="lazy">
      <img src="{img('M1')}" alt="{ALT['M1']}" loading="lazy">
    </div>{VMP}
  </div>
</section>"""
    return hero + catsec + shelf + deliv + trade + story + news, ["H3", "D4", "P3", "K1", "M1"]

# ------------------------------------------------------------------ Layout B
def layout_b():
    c = cats("D1", "P1")
    hero = f"""
<section class="b-hero" aria-labelledby="heroTitle">
  <div class="b-hero-copy"><div class="b-hero-in">{HERO_COPY.format(primary='btn--cream', secondary='btn--line-cream')}
  </div></div>
  <div class="b-hero-img"><img src="{img('H1')}" alt="{ALT['H1']}" fetchpriority="high"></div>
</section>"""
    rows = "".join(f'<li><a class="b-row" {a_attr(x)} data-preview="{x["src"]}" data-alt="{x["alt"]}"><span class="b-num">0{i+1}</span><span class="b-name">{x["label"]}</span><img class="b-thumb" src="{x["src"]}" alt="" loading="lazy"><span class="b-go">{x["go"]} <span aria-hidden="true">→</span></span></a></li>' for i, x in enumerate(c))
    catsec = f"""
<section class="b-cats" id="shop" aria-labelledby="shopTitle">
  <div class="wrap b-cats-grid">
    <div>
      <h2 id="shopTitle">Shop by category</h2>
      <ol class="b-list">{rows}</ol>
    </div>
    <div class="b-preview" aria-hidden="true"><img id="bPreview" src="{c[0]['src']}" alt=""></div>
  </div>
</section>"""
    deliv = f"""
<section class="b-deliv" id="delivery" aria-labelledby="delTitle">
  <div class="wrap">
    <div class="b-deliv-head">
      <h2 id="delTitle">Need it tomorrow? Consider it done.</h2>
      <div><p>Our North London hub ensures fast, next-day delivery nationwide, so you're never left waiting.</p>{TIMER}</div>
    </div>
  </div>
  <div class="b-road">
    <div class="b-word" aria-hidden="true">Tomorrow.</div>
    <img class="b-van" src="assets/img/van-cut.png" alt="The yellow Regency Foods delivery van" loading="lazy">
    <div class="b-tarmac" aria-hidden="true"></div>
  </div>
  <div class="wrap">{STEPS}
  </div>
</section>"""
    story = f"""
<section class="story b-story" id="story" aria-labelledby="storyTitle">
  <div class="wrap b-story-grid">
    <img class="b-s1" src="{img('K2')}" alt="{ALT['K2']}" loading="lazy">
    <div class="b-story-text"><h2 id="storyTitle">Thirty years on, the same promise.</h2>{STORY_TEXT}</div>
    <img class="b-s2" src="{img('M2')}" alt="{ALT['M2']}" loading="lazy">
  </div>
  <div class="wrap">{VMP}</div>
</section>"""
    return hero + catsec + shelf + deliv + trade + story + news, ["H1", "D1", "P1", "K2", "M2"]

# ------------------------------------------------------------------ Layout C
def layout_c():
    c = cats("D3", "P2")
    hero = f"""
<section class="c-hero" aria-labelledby="heroTitle">
  <div class="wrap">
    <div class="c-hero-copy">{HERO_COPY.format(primary='btn--green', secondary='')}
    </div>
    <div class="c-mosaic">
      <img class="m1" src="{img('H2')}" alt="{ALT['H2']}" fetchpriority="high">
      <img class="m2" src="{img('H4')}" alt="{ALT['H4']}">
      <img class="m3" src="assets/img/hero-set.jpg" alt="Regency Foods Almond, Pecan and Pistachio packs">
      <img class="m4" src="{img('H6')}" alt="{ALT['H6']}">
      <img class="m5" src="{img('H5')}" alt="{ALT['H5']}">
    </div>
  </div>
</section>"""
    tiles = "".join(f'<li class="t{i+1}"><a class="c-tile" {a_attr(x)}><img src="{x["src"]}" alt="{x["alt"]}" loading="lazy"><span class="c-name">{x["label"]}</span></a></li>' for i, x in enumerate(c))
    catsec = f"""
<section class="c-cats" id="shop" aria-labelledby="shopTitle">
  <div class="wrap">
    <div class="sec-head"><h2 id="shopTitle">Shop by category</h2><p>One supplier for the whole kitchen, from fresh cuts to the store cupboard.</p></div>
    <ul class="c-bento">{tiles}</ul>
  </div>
</section>"""
    deliv = f"""
<section class="c-deliv" id="delivery" aria-labelledby="delTitle">
  <div class="wrap c-deliv-in">
    <h2 id="delTitle">Need it tomorrow? <span>Consider it done.</span></h2>
    <img class="c-van" src="assets/img/van-cut.png" alt="The yellow Regency Foods delivery van" loading="lazy">
    <p class="c-deliv-lead">Our North London hub ensures fast, next-day delivery nationwide, so you're never left waiting.</p>
    {TIMER}{STEPS}
  </div>
</section>"""
    story = f"""
<section class="story" id="story" aria-labelledby="storyTitle">
  <div class="wrap">
    <div class="c-story-photos"><img src="{img('M5')}" alt="{ALT['M5']}" loading="lazy"><img src="{img('K3')}" alt="{ALT['K3']}" loading="lazy"></div>
    <div class="story-grid"><div><h2 id="storyTitle">Thirty years on, the same promise.</h2></div><div>{STORY_TEXT}</div></div>{VMP}
  </div>
</section>"""
    return hero + catsec + shelf + deliv + trade + story + news, ["H2", "H4", "H6", "H5", "D3", "P2", "K3", "M5"]

CREDITS = {l.split("\t")[0]: l.rstrip("\n").split("\t")[3] for l in open("/tmp/claude-0/-home-claude/d0a19366-6672-59fb-a77b-6d5132b4e39d/scratchpad/unsplash/opts.tsv")}
BASE_CREDITS = ["AM FL", "Anita Austvika", "Shourav Sheikh"]

for key, (title, fn) in {"a": ("Layout A", layout_a), "b": ("Layout B", layout_b), "c": ("Layout C", layout_c)}.items():
    body, used = fn()
    names = BASE_CREDITS + [CREDITS[u] for u in used]
    names = list(dict.fromkeys(names))
    foot = re.sub(r'<p class="credits">.*?</p><div hidden></div>', f'<p class="credits">Photography: Regency Foods, and Unsplash ({", ".join(names)}).</p>', footer, flags=re.S)
    h = head.replace('<link rel="stylesheet" href="styles.css">', '<link rel="stylesheet" href="styles.css">\n<link rel="stylesheet" href="layouts.css">')
    h = h.replace("<body>", f'<body class="lay-{key}">')
    html = (h + announce + "\n<!-- header -->" + header + '\n<main id="main">\n' + body + "\n</main>\n" + foot + basket +
            '\n<script src="app.js"></script>\n<script src="layouts.js"></script>\n</body>\n</html>\n')
    open(f"{OUT}/{key}.html", "w").write(html)
    print(key, len(html), used)
