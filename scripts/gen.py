"""Two redrawn hero illustrations: a Regency Foods box with store-cupboard staples and the Regency nut pouches."""
DEFS = '''
<defs>
  <filter id="{p}sh" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="10" stdDeviation="9" flood-color="#0b1f17" flood-opacity=".22"/></filter>
  <filter id="{p}sh2" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="4" stdDeviation="4" flood-color="#0b1f17" flood-opacity=".25"/></filter>
  <mask id="{p}logo" style="mask-type:alpha" maskUnits="userSpaceOnUse"><image href="assets/logo/logo-horizontal.png" x="{lx}" y="{ly}" width="{lw}" height="{lh}"/></mask>
  <linearGradient id="{p}glass" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".25" stop-color="#fff" stop-opacity=".35"/><stop offset=".4" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <pattern id="{p}fus" width="26" height="22" patternUnits="userSpaceOnUse"><path d="M2 11c4-8 8 8 12 0s8 8 12 0" fill="none" stroke="#F2C44B" stroke-width="5" stroke-linecap="round"/></pattern>
  <pattern id="{p}rice" width="10" height="10" patternUnits="userSpaceOnUse"><ellipse cx="5" cy="5" rx="3.6" ry="1.4" fill="#FFFCF8" transform="rotate(35 5 5)"/></pattern>
</defs>'''
HN = 'font-family="Helvetica Neue RF, Helvetica, Arial"'
CD = 'font-family="Caviar Dreams, Futura, sans-serif" font-weight="700"'


def bottle(x, y, s=1):
    return f'''<g transform="translate({x} {y}) scale({s})" filter="url(#{{p}}sh)">
  <path d="M-34 0 V-250 Q-34 -282 -14 -296 V-338 H14 V-296 Q34 -282 34 -250 V0 Z" fill="#2E5646"/>
  <rect x="-16" y="-362" width="32" height="28" rx="5" fill="#193429"/>
  <rect x="-34" y="-200" width="68" height="120" fill="#F2C44B"/>
  <text x="0" y="-162" text-anchor="middle" {HN} font-weight="700" font-size="8.5" fill="#193429" letter-spacing="1">EXTRA VIRGIN</text>
  <text x="0" y="-134" text-anchor="middle" {CD} font-size="20" fill="#193429">Olive</text>
  <text x="0" y="-112" text-anchor="middle" {CD} font-size="20" fill="#193429">Oil</text>
  <circle cx="0" cy="-94" r="4" fill="#9E8F43"/>
  <path d="M-34 0 V-250 Q-34 -282 -14 -296 V-338 H14 V-296 Q34 -282 34 -250 V0 Z" fill="url(#{{p}}glass)"/>
</g>'''


def jar(x, y, s=1):
    return f'''<g transform="translate({x} {y}) scale({s})" filter="url(#{{p}}sh)">
  <rect x="-38" y="-150" width="76" height="150" rx="14" fill="#C33A1E"/>
  <rect x="-34" y="-176" width="68" height="30" rx="6" fill="#193429"/>
  <rect x="-38" y="-112" width="76" height="62" fill="#FFFCF8"/>
  <text x="0" y="-84" text-anchor="middle" {CD} font-size="17" fill="#C33A1E">Passata</text>
  <text x="0" y="-65" text-anchor="middle" {HN} font-size="7.5" fill="#193429" letter-spacing=".8">ITALIAN TOMATO</text>
  <rect x="-38" y="-150" width="76" height="150" rx="14" fill="url(#{{p}}glass)"/>
</g>'''


def rice(x, y, s=1):
    return f'''<g transform="translate({x} {y}) scale({s})" filter="url(#{{p}}sh)">
  <rect x="-55" y="-250" width="110" height="250" fill="#1A3256"/>
  <rect x="-55" y="-250" width="110" height="16" fill="#F2C44B"/>
  <text x="0" y="-196" text-anchor="middle" {HN} font-weight="700" font-size="11" fill="#F2C44B" letter-spacing="2">BASMATI</text>
  <text x="0" y="-168" text-anchor="middle" {CD} font-size="30" fill="#FFFCF8">Rice</text>
  <rect x="-38" y="-140" width="76" height="92" rx="38" fill="url(#{{p}}rice)" stroke="#FFFCF8" stroke-width="3"/>
  <text x="0" y="-20" text-anchor="middle" {HN} font-size="10" fill="#FFFCF8" letter-spacing="1">1 KG</text>
</g>'''


def pasta(x, y, rot, s=1):
    return f'''<g transform="translate({x} {y}) rotate({rot}) scale({s})" filter="url(#{{p}}sh)">
  <rect x="-85" y="-120" width="170" height="240" fill="#E85A10"/>
  <text x="0" y="-72" text-anchor="middle" {CD} font-size="40" fill="#FFFCF8">Fusilli</text>
  <text x="0" y="-48" text-anchor="middle" {HN} font-weight="700" font-size="10" fill="#FFFCF8" letter-spacing="1.6">DURUM WHEAT PASTA</text>
  <rect x="-58" y="-28" width="116" height="104" rx="52" fill="#FFF3D6"/>
  <rect x="-58" y="-28" width="116" height="104" rx="52" fill="url(#{{p}}fus)"/>
  <rect x="-58" y="-28" width="116" height="104" rx="52" fill="none" stroke="#FFFCF8" stroke-width="5"/>
  <text x="0" y="104" text-anchor="middle" {HN} font-size="11" fill="#FFFCF8" letter-spacing="1">500 G</text>
</g>'''


def tin(x, y, color, band, ink, word, s=1, fs=17):
    return f'''<g transform="translate({x} {y}) scale({s})" filter="url(#{{p}}sh2)">
  <rect x="-44" y="-96" width="88" height="96" rx="6" fill="{color}"/>
  <ellipse cx="0" cy="-96" rx="44" ry="9" fill="#C9CEC9"/><ellipse cx="0" cy="-96" rx="36" ry="6" fill="#E9ECE8"/>
  <rect x="-44" y="-74" width="88" height="50" fill="{band}"/>
  <text x="0" y="-43" text-anchor="middle" {CD} font-size="{fs}" fill="{ink}">{word}</text>
  <rect x="-44" y="-96" width="88" height="96" rx="6" fill="url(#{{p}}glass)"/>
</g>'''


def pouch(name, x, y, w, rot=0):
    h = w * 918 / 600
    return (f'<g filter="url(#{{p}}sh)" transform="rotate({rot} {x + w / 2:.1f} {y + h:.1f})">'
            f'<image href="assets/img/pack-{name}.png" x="{x}" y="{y}" width="{w}" height="{h:.1f}"/></g>')


def box(x, y, w, h, p, logo_at=.36, logo_w=.62):
    lw = w * logo_w; lh = lw * 254 / 1400; lx = x + (w - lw) / 2; ly = y + h * logo_at
    g = f'''<g filter="url(#{p}sh)">
  <rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#193429"/>
  <rect x="{x}" y="{y}" width="{w}" height="10" fill="#234538"/>
  <rect x="{x}" y="{y + h - 8}" width="{w}" height="8" fill="#12261d"/>
  <rect x="{lx:.1f}" y="{ly:.1f}" width="{lw:.1f}" height="{lh:.1f}" fill="#D9B95A" mask="url(#{p}logo)"/>
</g>'''
    return g, dict(lx=f'{lx:.1f}', ly=f'{ly:.1f}', lw=f'{lw:.1f}', lh=f'{lh:.1f}')


def svg(p, body, d, label):
    return (f'<svg class="redraw" viewBox="0 0 900 880" role="img" aria-label="{label}" xmlns="http://www.w3.org/2000/svg">'
            + DEFS.format(p=p, **d) + body.replace('{p}', p) + '</svg>')


# ---------- A: closed box with everything stacked on top, like the original photo
b, d = box(220, 560, 470, 290, 'a', logo_at=.40)
A = ('<ellipse cx="450" cy="858" rx="410" ry="16" fill="#0b1f17" opacity=".10"/>'
     + jar(280, 560) + bottle(364, 560) + rice(470, 560) + pasta(616, 410, 12)
     + b
     + pouch('almond', 16, 650, 128, -8) + pouch('pecan', 104, 662, 124, 3)
     + pouch('pistachio', 664, 662, 124, 4)
     + tin(836, 858, '#44AF5D', '#FFFCF8', '#44AF5D', 'Beans', .8) + tin(836, 781, '#F2C44B', '#193429', '#F2C44B', 'Corn', .72))
open('redraw-a.svg', 'w').write(svg('a', A, d, 'A Regency Foods box stacked with olive oil, passata, rice and pasta, with Regency nut pouches beside it'))

# ---------- B: open box, staples rising out of it, the three pouches lined up in front
b2, d2 = box(170, 520, 560, 330, 'b', logo_at=.10, logo_w=.5)
flaps = ('<polygon points="170,520 88,438 300,438 330,520" fill="#2E5646"/>'
         '<polygon points="730,520 812,438 600,438 570,520" fill="#2E5646"/>'
         '<polygon points="210,520 250,472 650,472 690,520" fill="#0f2219"/>')
B = ('<ellipse cx="450" cy="858" rx="420" ry="16" fill="#0b1f17" opacity=".10"/>' + flaps
     + bottle(298, 560, 1.05) + pasta(420, 402, -9, .95) + rice(560, 560, 1.05) + jar(662, 560, 1.05)
     + b2
     + pouch('almond', 196, 668, 118, -6) + pouch('pecan', 390, 652, 122, 0) + pouch('pistachio', 588, 668, 118, 6)
     + tin(92, 858, '#E85A10', '#FFFCF8', '#E85A10', 'Chickpeas', .9, 14) + tin(812, 858, '#44AF5D', '#FFFCF8', '#44AF5D', 'Beans', .9))
open('redraw-b.svg', 'w').write(svg('b', B, d2, 'An open Regency Foods box with olive oil, pasta, rice and passata, and the three Regency nut pouches in front'))
print('ok')
