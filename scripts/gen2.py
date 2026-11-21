"""Realistic-leaning vector redraw of the Regency Foods box hero (two compositions).
Light comes from the upper left; the viewer is slightly above and to the right."""
import math

HN = 'font-family="Helvetica Neue RF, Helvetica, Arial"'
CD = 'font-family="Caviar Dreams, Futura, sans-serif" font-weight="700"'
_id = [0]


def uid(p, s):
    _id[0] += 1
    return f'{p}{s}{_id[0]}'


def defs(p):
    return f'''<defs>
  <radialGradient id="{p}cs"><stop offset="0" stop-color="#0b1f17" stop-opacity=".45"/><stop offset=".6" stop-color="#0b1f17" stop-opacity=".14"/><stop offset="1" stop-color="#0b1f17" stop-opacity="0"/></radialGradient>
  <linearGradient id="{p}cyl" x1="0" x2="1">
    <stop offset="0" stop-color="#000" stop-opacity=".42"/><stop offset=".12" stop-color="#000" stop-opacity=".12"/>
    <stop offset=".28" stop-color="#fff" stop-opacity=".22"/><stop offset=".34" stop-color="#fff" stop-opacity=".42"/>
    <stop offset=".42" stop-color="#fff" stop-opacity=".05"/><stop offset=".7" stop-color="#000" stop-opacity=".08"/>
    <stop offset=".9" stop-color="#000" stop-opacity=".3"/><stop offset="1" stop-color="#000" stop-opacity=".5"/></linearGradient>
  <linearGradient id="{p}lab" x1="0" x2="1">
    <stop offset="0" stop-color="#000" stop-opacity=".32"/><stop offset=".18" stop-color="#000" stop-opacity="0"/>
    <stop offset=".32" stop-color="#fff" stop-opacity=".28"/><stop offset=".42" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".8" stop-color="#000" stop-opacity=".06"/><stop offset="1" stop-color="#000" stop-opacity=".36"/></linearGradient>
  <linearGradient id="{p}face" x1="0" y1="0" x2=".35" y2="1">
    <stop offset="0" stop-color="#fff" stop-opacity=".16"/><stop offset=".5" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".16"/></linearGradient>
  <linearGradient id="{p}pouch" x1="0" x2="1">
    <stop offset="0" stop-color="#000" stop-opacity=".28"/><stop offset=".1" stop-color="#000" stop-opacity="0"/>
    <stop offset=".22" stop-color="#fff" stop-opacity=".22"/><stop offset=".3" stop-color="#fff" stop-opacity="0"/>
    <stop offset=".75" stop-color="#000" stop-opacity=".04"/><stop offset="1" stop-color="#000" stop-opacity=".32"/></linearGradient>
  <linearGradient id="{p}pouchv" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#000" stop-opacity=".18"/><stop offset=".08" stop-color="#000" stop-opacity="0"/>
    <stop offset=".86" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".26"/></linearGradient>
  <filter id="{p}grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="3" seed="4" result="n"/>
    <feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .09 0" result="g"/>
    <feComposite in="g" in2="SourceGraphic" operator="in" result="gm"/>
    <feMerge><feMergeNode in="SourceGraphic"/><feMergeNode in="gm"/></feMerge>
  </filter>
  <filter id="{p}soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>
  <filter id="{p}drop" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="6" dy="10" stdDeviation="8" flood-color="#0b1f17" flood-opacity=".25"/></filter>
  <pattern id="{p}fus" width="24" height="20" patternUnits="userSpaceOnUse"><path d="M2 10c4-7 7 7 11 0s7 7 11 0" fill="none" stroke="#E9B43F" stroke-width="5" stroke-linecap="round"/><path d="M2 10c4-7 7 7 11 0s7 7 11 0" fill="none" stroke="#FFE7A3" stroke-width="1.6" stroke-linecap="round" transform="translate(0 -1.4)"/></pattern>
  <pattern id="{p}rice" width="9" height="9" patternUnits="userSpaceOnUse"><ellipse cx="4.5" cy="4.5" rx="3.3" ry="1.25" fill="#FFFCF8" transform="rotate(35 4.5 4.5)"/></pattern>
</defs>'''


def contact(p, cx, cy, rx, ry=None, o=1):
    ry = ry or rx * .16
    return f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="url(#{p}cs)" opacity="{o}"/>'


def cuboid(p, x, y, w, h, d, front, side, top, content='', rot=0, grain=False):
    """Front face at (x,y,w,h); depth goes up-right."""
    dx, dy = d * .46, d * .32
    cp = uid(p, 'c')
    g = f'<g transform="rotate({rot} {x + w / 2:.1f} {y + h:.1f})">'
    g += f'<polygon points="{x},{y} {x + w},{y} {x + w + dx:.1f},{y - dy:.1f} {x + dx:.1f},{y - dy:.1f}" fill="{top}"/>'
    g += f'<polygon points="{x + w},{y} {x + w + dx:.1f},{y - dy:.1f} {x + w + dx:.1f},{y + h - dy:.1f} {x + w},{y + h}" fill="{side}"/>'
    g += f'<polygon points="{x + w},{y} {x + w + dx:.1f},{y - dy:.1f} {x + w + dx:.1f},{y + h - dy:.1f} {x + w},{y + h}" fill="url(#{p}face)" opacity=".6"/>'
    g += f'<clipPath id="{cp}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>'
    g += f'<g clip-path="url(#{cp})"{" filter=" + chr(34) + "url(#" + p + "grain)" + chr(34) if grain else ""}><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{front}"/>{content}</g>'
    g += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{p}face)"/>'
    g += f'<line x1="{x}" y1="{y + .5}" x2="{x + w}" y2="{y + .5}" stroke="#fff" stroke-opacity=".28"/>'
    g += f'<line x1="{x + w - .5}" y1="{y}" x2="{x + w - .5}" y2="{y + h}" stroke="#000" stroke-opacity=".18"/>'
    return g + '</g>'


def tin(p, cx, by, r, h, body, band, ink, word, fs=16):
    ry = r * .24
    cp = uid(p, 't')
    return f'''<g>
  {contact(p, cx + 6, by + 2, r * 1.25)}
  <clipPath id="{cp}"><path d="M{cx - r} {by - h} V{by} A{r} {ry} 0 0 0 {cx + r} {by} V{by - h} Z"/></clipPath>
  <g clip-path="url(#{cp})">
    <rect x="{cx - r}" y="{by - h - ry}" width="{2 * r}" height="{h + 2 * ry}" fill="{body}"/>
    <rect x="{cx - r}" y="{by - h * .74}" width="{2 * r}" height="{h * .5}" fill="{band}"/>
    <text x="{cx}" y="{by - h * .43}" text-anchor="middle" {CD} font-size="{fs}" fill="{ink}">{word}</text>
    {''.join(f'<line x1="{cx - r}" y1="{by - h + k}" x2="{cx + r}" y2="{by - h + k}" stroke="#000" stroke-opacity=".12"/>' for k in (6, 10, h - 8, h - 4))}
    <rect x="{cx - r}" y="{by - h - ry}" width="{2 * r}" height="{h + 2 * ry}" fill="url(#{p}cyl)"/>
  </g>
  <ellipse cx="{cx}" cy="{by - h}" rx="{r}" ry="{ry}" fill="#B9BFBA"/>
  <ellipse cx="{cx}" cy="{by - h}" rx="{r - 4}" ry="{ry - 2}" fill="#DCE1DC"/>
  <ellipse cx="{cx - r * .2}" cy="{by - h - ry * .2}" rx="{r * .45}" ry="{ry * .4}" fill="#fff" opacity=".5"/>
</g>'''


def bottle(p, cx, by, s=1):
    w = 34 * s; sh = 252 * s; nk = 14 * s; top = 340 * s
    body = f'M{cx - w} {by} V{by - sh} Q{cx - w} {by - sh - 34 * s} {cx - nk} {by - sh - 48 * s} V{by - top} H{cx + nk} V{by - sh - 48 * s} Q{cx + w} {by - sh - 34 * s} {cx + w} {by - sh} V{by} Q{cx} {by + 7 * s} {cx - w} {by} Z'
    cp = uid(p, 'b')
    lt, lb = by - 200 * s, by - 76 * s
    curve = 7 * s
    return f'''<g>
  {contact(p, cx + 8, by + 2, w * 1.45)}
  <clipPath id="{cp}"><path d="{body}"/></clipPath>
  <g clip-path="url(#{cp})">
    <rect x="{cx - w}" y="{by - top}" width="{2 * w}" height="{top + 10}" fill="#20402F"/>
    <rect x="{cx - w}" y="{by - sh + 20 * s}" width="{2 * w}" height="{sh}" fill="#6E7A2A" opacity=".55"/>
    <path d="M{cx - w} {lt} Q{cx} {lt + curve} {cx + w} {lt} V{lb} Q{cx} {lb + curve} {cx - w} {lb} Z" fill="#F2C44B"/>
    <path d="M{cx - w} {lt + 7 * s} Q{cx} {lt + 7 * s + curve} {cx + w} {lt + 7 * s}" fill="none" stroke="#193429" stroke-width="1.2"/>
    <text x="{cx}" y="{lt + 34 * s}" text-anchor="middle" {HN} font-weight="700" font-size="{8 * s:.1f}" fill="#193429" letter-spacing="1">EXTRA VIRGIN</text>
    <text x="{cx}" y="{lt + 62 * s}" text-anchor="middle" {CD} font-size="{21 * s:.1f}" fill="#193429">Olive</text>
    <text x="{cx}" y="{lt + 84 * s}" text-anchor="middle" {CD} font-size="{21 * s:.1f}" fill="#193429">Oil</text>
    <path d="M{cx - 6 * s} {lt + 104 * s} q{6 * s} {-12 * s} {12 * s} 0 q{-6 * s} {8 * s} {-12 * s} 0z" fill="#6E7A2A"/>
    <rect x="{cx - w}" y="{by - top}" width="{2 * w}" height="{top + 10}" fill="url(#{p}cyl)"/>
    <rect x="{cx - w * .52}" y="{by - sh - 10 * s}" width="{4 * s}" height="{sh - 20 * s}" rx="2" fill="#fff" opacity=".38"/>
  </g>
  <rect x="{cx - nk - 3 * s}" y="{by - top - 30 * s}" width="{2 * nk + 6 * s}" height="{34 * s}" rx="{4 * s}" fill="#193429"/>
  {''.join(f'<line x1="{cx - nk - 3 * s + k * s}" y1="{by - top - 28 * s}" x2="{cx - nk - 3 * s + k * s}" y2="{by - top + 2 * s}" stroke="#000" stroke-opacity=".3"/>' for k in range(4, 34, 4))}
  <rect x="{cx - nk - 3 * s}" y="{by - top - 30 * s}" width="{2 * nk + 6 * s}" height="{34 * s}" rx="{4 * s}" fill="url(#{p}cyl)"/>
</g>'''


def jar(p, cx, by, s=1):
    r = 40 * s; h = 150 * s; ry = r * .22
    cp = uid(p, 'j')
    lt, lb = by - 112 * s, by - 46 * s
    return f'''<g>
  {contact(p, cx + 6, by + 2, r * 1.3)}
  <clipPath id="{cp}"><path d="M{cx - r} {by - h + 12 * s} Q{cx - r} {by - h} {cx - r + 10 * s} {by - h} H{cx + r - 10 * s} Q{cx + r} {by - h} {cx + r} {by - h + 12 * s} V{by - 8 * s} Q{cx + r} {by} {cx + r - 12 * s} {by + ry * .4} Q{cx} {by + ry} {cx - r + 12 * s} {by + ry * .4} Q{cx - r} {by} {cx - r} {by - 8 * s} Z"/></clipPath>
  <g clip-path="url(#{cp})">
    <rect x="{cx - r}" y="{by - h}" width="{2 * r}" height="{h + ry}" fill="#A92A12"/>
    <rect x="{cx - r}" y="{by - h}" width="{2 * r}" height="{14 * s}" fill="#D9D2C2" opacity=".55"/>
    <path d="M{cx - r} {lt} Q{cx} {lt + 6 * s} {cx + r} {lt} V{lb} Q{cx} {lb + 6 * s} {cx - r} {lb} Z" fill="#FFFCF8"/>
    <text x="{cx}" y="{lt + 30 * s}" text-anchor="middle" {CD} font-size="{17 * s:.1f}" fill="#B3301A">Passata</text>
    <text x="{cx}" y="{lt + 48 * s}" text-anchor="middle" {HN} font-size="{7.2 * s:.1f}" fill="#193429" letter-spacing=".8">ITALIAN TOMATO</text>
    <circle cx="{cx}" cy="{lt + 58 * s}" r="{3 * s}" fill="#44AF5D"/>
    <rect x="{cx - r}" y="{by - h}" width="{2 * r}" height="{h + ry}" fill="url(#{p}cyl)"/>
    <rect x="{cx - r * .5}" y="{by - h + 18 * s}" width="{5 * s}" height="{h - 36 * s}" rx="2" fill="#fff" opacity=".4"/>
  </g>
  <path d="M{cx - r + 3 * s} {by - h + 2 * s} V{by - h - 26 * s} H{cx + r - 3 * s} V{by - h + 2 * s} Z" fill="#193429"/>
  {''.join(f'<line x1="{cx - r + 3 * s + k * s}" y1="{by - h - 24 * s}" x2="{cx - r + 3 * s + k * s}" y2="{by - h}" stroke="#000" stroke-opacity=".28"/>' for k in range(5, 76, 5))}
  <path d="M{cx - r + 3 * s} {by - h + 2 * s} V{by - h - 26 * s} H{cx + r - 3 * s} V{by - h + 2 * s} Z" fill="url(#{p}cyl)"/>
  <ellipse cx="{cx}" cy="{by - h - 26 * s}" rx="{r - 3 * s}" ry="{ry * .8}" fill="#2E5646"/>
  <ellipse cx="{cx - 8 * s}" cy="{by - h - 27 * s}" rx="{r * .4}" ry="{ry * .3}" fill="#fff" opacity=".25"/>
</g>'''


def rice_front(p, x, y, w, h):
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h * .07}" fill="#F2C44B"/>'
            f'<text x="{x + w / 2}" y="{y + h * .26}" text-anchor="middle" {HN} font-weight="700" font-size="11" fill="#F2C44B" letter-spacing="2">BASMATI</text>'
            f'<text x="{x + w / 2}" y="{y + h * .38}" text-anchor="middle" {CD} font-size="30" fill="#FFFCF8">Rice</text>'
            f'<rect x="{x + w / 2 - 36}" y="{y + h * .44}" width="72" height="88" rx="36" fill="#E9E2CF"/>'
            f'<rect x="{x + w / 2 - 36}" y="{y + h * .44}" width="72" height="88" rx="36" fill="url(#{p}rice)"/>'
            f'<rect x="{x + w / 2 - 36}" y="{y + h * .44}" width="72" height="88" rx="36" fill="none" stroke="#FFFCF8" stroke-width="3"/>'
            f'<text x="{x + w / 2}" y="{y + h * .93}" text-anchor="middle" {HN} font-size="10" fill="#FFFCF8" letter-spacing="1">1 KG</text>')


def pasta_front(p, x, y, w, h):
    return (f'<text x="{x + w / 2}" y="{y + h * .22}" text-anchor="middle" {CD} font-size="38" fill="#FFFCF8">Fusilli</text>'
            f'<text x="{x + w / 2}" y="{y + h * .31}" text-anchor="middle" {HN} font-weight="700" font-size="9.5" fill="#FFFCF8" letter-spacing="1.5">DURUM WHEAT PASTA</text>'
            f'<rect x="{x + w / 2 - 56}" y="{y + h * .38}" width="112" height="102" rx="51" fill="#F6E2AE"/>'
            f'<rect x="{x + w / 2 - 56}" y="{y + h * .38}" width="112" height="102" rx="51" fill="url(#{p}fus)"/>'
            f'<rect x="{x + w / 2 - 56}" y="{y + h * .38}" width="112" height="102" rx="51" fill="#fff" opacity=".12"/>'
            f'<rect x="{x + w / 2 - 56}" y="{y + h * .38}" width="112" height="102" rx="51" fill="none" stroke="#FFFCF8" stroke-width="4"/>'
            f'<text x="{x + w / 2}" y="{y + h * .93}" text-anchor="middle" {HN} font-size="10.5" fill="#FFFCF8" letter-spacing="1">500 G</text>')


def pouch(p, name, x, by, w, rot=0):
    h = w * 918 / 600
    y = by - h
    cp = uid(p, 'p')
    shape = (f'M{x + 6} {y + 10} Q{x + w / 2} {y + 4} {x + w - 6} {y + 10} '
             f'L{x + w - 2} {by - 18} Q{x + w} {by} {x + w - 16} {by} L{x + 16} {by} Q{x} {by} {x + 2} {by - 18} Z')
    seal = ''.join(f'<line x1="{x + 8}" y1="{y + 14 + k}" x2="{x + w - 8}" y2="{y + 14 + k}" stroke="#000" stroke-opacity=".14"/>' for k in (0, 3, 6, 9))
    crinkle = (f'<path d="M{x + w * .18} {y + h * .3} q{w * .06} {h * .2} {-w * .02} {h * .45}" fill="none" stroke="#fff" stroke-opacity=".22" stroke-width="3"/>'
               f'<path d="M{x + w * .86} {y + h * .2} q{-w * .05} {h * .25} {w * .02} {h * .55}" fill="none" stroke="#000" stroke-opacity=".12" stroke-width="3"/>')
    return f'''<g transform="rotate({rot} {x + w / 2:.1f} {by:.1f})">
  {contact(p, x + w / 2 + 8, by + 2, w * .62)}
  <clipPath id="{cp}"><path d="{shape}"/></clipPath>
  <g clip-path="url(#{cp})">
    <image href="assets/img/pack-{name}.png" x="{x}" y="{y}" width="{w}" height="{h:.1f}" preserveAspectRatio="none"/>
    <rect x="{x}" y="{y}" width="{w}" height="{h:.1f}" fill="url(#{p}pouch)"/>
    <rect x="{x}" y="{y}" width="{w}" height="{h:.1f}" fill="url(#{p}pouchv)"/>
    {seal}{crinkle}
  </g>
</g>'''


def regency_box(p, x, y, w, h, d, logo_at=.36, logo_w=.62, open_=False):
    dx, dy = d * .46, d * .32
    lw = w * logo_w; lh = lw * 254 / 1400; lx = x + (w - lw) / 2; ly = y + h * logo_at
    mid = uid(p, 'm')
    front = f'''<mask id="{mid}" style="mask-type:alpha" maskUnits="userSpaceOnUse"><image href="assets/logo/logo-horizontal.png" x="{lx:.1f}" y="{ly:.1f}" width="{lw:.1f}" height="{lh:.1f}"/></mask>
  <rect x="{lx:.1f}" y="{ly + 1.2:.1f}" width="{lw:.1f}" height="{lh:.1f}" fill="#000" opacity=".35" mask="url(#{mid})"/>
  <rect x="{lx:.1f}" y="{ly:.1f}" width="{lw:.1f}" height="{lh:.1f}" fill="#D6B65C" mask="url(#{mid})"/>
  <line x1="{x}" y1="{y + h - 14}" x2="{x + w}" y2="{y + h - 14}" stroke="#000" stroke-opacity=".2"/>'''
    if open_:
        top = '#0E1F17'
    else:
        top = '#2D5443'
    g = cuboid(p, x, y, w, h, d, '#1B3A2D', '#122A20', top, front, grain=True)
    if not open_:
        # tape along the lid seam
        g += (f'<polygon points="{x + w * .5 - 22},{y} {x + w * .5 + 22},{y} {x + w * .5 + 22 + dx:.1f},{y - dy:.1f} {x + w * .5 - 22 + dx:.1f},{y - dy:.1f}" fill="#C7A55A" opacity=".55"/>'
              f'<line x1="{x + dx * .5:.1f}" y1="{y - dy * .5:.1f}" x2="{x + w + dx * .5:.1f}" y2="{y - dy * .5:.1f}" stroke="#000" stroke-opacity=".25"/>')
    return g, (dx, dy)


def wrap(p, body, label, vb='0 150 900 730'):
    return (f'<svg class="redraw" viewBox="{vb}" preserveAspectRatio="xMidYMax meet" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">'
            + defs(p) + body + '</svg>')


# ======================= A: closed box, groceries stacked on the lid ======================
p = 'a'
bx, by_, bw, bh, bd = 230, 600, 440, 250, 120
box_svg, (dx, dy) = regency_box(p, bx, by_, bw, bh, bd, logo_at=.36)
lid_back, lid_front = by_ - dy * .75, by_ - dy * .18
A = (contact(p, 470, 856, 360, 26, 1.1)
     + box_svg
     # back row on the lid
     + contact(p, 492, lid_back + 2, 70, 9)
     + cuboid(p, 440, lid_back - 240, 104, 240, 40, '#1A3256', '#122440', '#2A4670', rice_front(p, 440, lid_back - 240, 104, 240))
     + contact(p, 612, lid_back + 4, 90, 10)
     + cuboid(p, 548, lid_back - 230, 160, 230, 36, '#E85A10', '#B8450B', '#F27A3A', pasta_front(p, 548, lid_back - 230, 160, 230), rot=11)
     # front row on the lid
     + jar(p, 296, lid_front - 2)
     + bottle(p, 378, lid_front)
     + tin(p, 640, lid_front, 38, 86, '#F2C44B', '#193429', '#F2C44B', 'Corn', 15)
     # on the floor
     + pouch(p, 'almond', 36, 850, 132, -9)
     + pouch(p, 'pecan', 132, 860, 130, 3)
     + pouch(p, 'pistachio', 700, 860, 126, 5)
     + tin(p, 846, 860, 36, 84, '#44AF5D', '#FFFCF8', '#2F8A47', 'Beans', 14))
open('redraw-a.svg', 'w').write(wrap(p, A, 'A Regency Foods box stacked with olive oil, passata, rice, pasta and a tin of corn, with the Regency nut pouches beside it'))

# ======================= B: open box, groceries rising out, pouches in front ======================
p = 'b'
bx, by_, bw, bh, bd = 190, 560, 470, 290, 120
box_svg, (dx, dy) = regency_box(p, bx, by_, bw, bh, bd, logo_at=.09, logo_w=.5, open_=True)
# flaps: back flap rises from the back edge, side flaps fold outwards
fl = (f'<polygon points="{bx + dx:.1f},{by_ - dy:.1f} {bx + bw + dx:.1f},{by_ - dy:.1f} {bx + bw + dx + 14:.1f},{by_ - dy - 120:.1f} {bx + dx - 10:.1f},{by_ - dy - 112:.1f}" fill="#24493A"/>'
      f'<polygon points="{bx + dx:.1f},{by_ - dy:.1f} {bx + bw + dx:.1f},{by_ - dy:.1f} {bx + bw + dx + 14:.1f},{by_ - dy - 120:.1f} {bx + dx - 10:.1f},{by_ - dy - 112:.1f}" fill="url(#{p}face)" opacity=".7"/>'
      f'<polygon points="{bx + bw + dx:.1f},{by_ - dy:.1f} {bx + bw:.1f},{by_:.1f} {bx + bw + 112:.1f},{by_ - 52:.1f} {bx + bw + dx + 104:.1f},{by_ - dy - 66:.1f}" fill="#2E5646"/>')
fl_left = f'<polygon points="{bx},{by_} {bx + dx:.1f},{by_ - dy:.1f} {bx + dx - 118:.1f},{by_ - dy - 40:.1f} {bx - 112},{by_ - 18}" fill="#2E5646"/><polygon points="{bx},{by_} {bx + dx:.1f},{by_ - dy:.1f} {bx + dx - 118:.1f},{by_ - dy - 40:.1f} {bx - 112},{by_ - 18}" fill="url(#{p}face)"/>'
inside = f'<polygon points="{bx},{by_} {bx + bw},{by_} {bx + bw + dx:.1f},{by_ - dy:.1f} {bx + dx:.1f},{by_ - dy:.1f}" fill="#0B1912"/>'
base = by_ + 70  # items stand inside, below the rim
B = (contact(p, 450, 856, 380, 26, 1.1)
     + fl + inside
     + cuboid(p, 300, base - 300, 160, 230, 34, '#E85A10', '#B8450B', '#F27A3A', pasta_front(p, 300, base - 300, 160, 230), rot=-8)
     + cuboid(p, 470, base - 300, 104, 240, 40, '#1A3256', '#122440', '#2A4670', rice_front(p, 470, base - 300, 104, 240))
     + bottle(p, 262, base, 1.04) + jar(p, 612, base - 12, 1.04)
     + box_svg + fl_left
     + pouch(p, 'almond', 200, 858, 120, -5) + pouch(p, 'pecan', 362, 852, 124, 0) + pouch(p, 'pistachio', 524, 858, 120, 5)
     + tin(p, 92, 860, 38, 88, '#E85A10', '#FFFCF8', '#C24B0E', 'Chickpeas', 12)
     + tin(p, 790, 860, 38, 88, '#44AF5D', '#FFFCF8', '#2F8A47', 'Beans', 14))
open('redraw-b.svg', 'w').write(wrap(p, B, 'An open Regency Foods box with olive oil, pasta, rice and passata, and the three Regency nut pouches in front'))
print('ok')
