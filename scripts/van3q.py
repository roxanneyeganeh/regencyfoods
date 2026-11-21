"""Regency Foods van redrawn at the same three-quarter front angle as the original photo (traced in its 1025x557 frame)."""
HN = 'font-family="Helvetica Neue RF, Helvetica, Arial"'


def wheel(cx, cy, rx, ry, rim=.6):
    return f'''<g>
  <ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="url(#qtyre)"/>
  <ellipse cx="{cx + rx * .08:.1f}" cy="{cy}" rx="{rx * rim:.1f}" ry="{ry * rim:.1f}" fill="url(#qrim)"/>
  <ellipse cx="{cx + rx * .08:.1f}" cy="{cy}" rx="{rx * rim:.1f}" ry="{ry * rim:.1f}" fill="none" stroke="#5d625f" stroke-width="2"/>
  <ellipse cx="{cx + rx * .08:.1f}" cy="{cy}" rx="{rx * rim * .72:.1f}" ry="{ry * rim * .72:.1f}" fill="none" stroke="#7d847f" stroke-width="1.5"/>
  {''.join(f'<ellipse cx="{cx + rx * .08 + rx * rim * .5 * __import__("math").cos(a):.1f}" cy="{cy + ry * rim * .5 * __import__("math").sin(a):.1f}" rx="{rx * .07:.1f}" ry="{ry * .08:.1f}" fill="#3a3e3c"/>' for a in [k * 1.0472 + .5 for k in range(6)])}
  <ellipse cx="{cx + rx * .08:.1f}" cy="{cy}" rx="{rx * .16:.1f}" ry="{ry * .16:.1f}" fill="#9aa19c"/>
  <path d="M{cx - rx * .4:.1f} {cy - ry * .3:.1f} A{rx * .5:.1f} {ry * .5:.1f} 0 0 1 {cx + rx * .15:.1f} {cy - ry * .5:.1f}" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="2.5" stroke-linecap="round"/>
</g>'''


SIDE = "160,110 452,68 520,148 546,250 645,300 652,388 642,456 590,462 150,402 146,250"
ROOF_TOP = "160,110 452,68 612,78 330,104"
ROOF_FRONT = "452,68 612,78 796,150 520,148"
SCREEN = "520,148 796,150 836,258 546,250"
BONNET = "546,250 836,258 886,298 645,300"
FRONT = "645,300 886,298 898,330 900,438 862,452 700,468 642,456 652,388"

svg = f'''<svg class="redraw-van" viewBox="90 40 860 500" role="img" aria-label="The yellow Regency Foods delivery van" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="qside" x1="0" y1="0" x2=".25" y2="1">
    <stop offset="0" stop-color="#F3CB5A"/><stop offset=".45" stop-color="#E8B83F"/><stop offset=".85" stop-color="#D6A533"/><stop offset="1" stop-color="#B98C26"/></linearGradient>
  <linearGradient id="qsideL" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".18"/><stop offset=".12" stop-color="#000" stop-opacity="0"/><stop offset=".85" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity=".12"/></linearGradient>
  <linearGradient id="qfront" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#E2B03A"/><stop offset="1" stop-color="#C2922A"/></linearGradient>
  <linearGradient id="qbonnet" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F0C552"/><stop offset="1" stop-color="#DBAA36"/></linearGradient>
  <linearGradient id="qroof" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F8D978"/><stop offset="1" stop-color="#EDC251"/></linearGradient>
  <linearGradient id="qglass" x1="0" y1="0" x2=".6" y2="1"><stop offset="0" stop-color="#6d7f88"/><stop offset=".5" stop-color="#34424a"/><stop offset="1" stop-color="#1b2428"/></linearGradient>
  <linearGradient id="qglare" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".32"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <linearGradient id="qtrim" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3b3e3c"/><stop offset="1" stop-color="#1a1c1b"/></linearGradient>
  <radialGradient id="qrim" cx=".42" cy=".36" r=".75"><stop offset="0" stop-color="#eef1ef"/><stop offset=".55" stop-color="#aeb5b0"/><stop offset="1" stop-color="#6a716c"/></radialGradient>
  <radialGradient id="qtyre"><stop offset=".6" stop-color="#2d302f"/><stop offset=".82" stop-color="#1c1e1d"/><stop offset="1" stop-color="#0d0e0e"/></radialGradient>
  <radialGradient id="qshadow"><stop offset="0" stop-color="#3b0f05" stop-opacity=".5"/><stop offset=".6" stop-color="#3b0f05" stop-opacity=".18"/><stop offset="1" stop-color="#3b0f05" stop-opacity="0"/></radialGradient>
  <linearGradient id="qlamp" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#cfd8de"/><stop offset="1" stop-color="#8d9aa2"/></linearGradient>
  <clipPath id="qsideclip"><polygon points="{SIDE}"/></clipPath>
  <clipPath id="qfrontclip"><polygon points="{FRONT}"/></clipPath>
  <mask id="qlogo" style="mask-type:alpha" maskUnits="userSpaceOnUse"><image href="assets/logo/logo-horizontal.png" x="0" y="0" width="222" height="40.3"/></mask>
</defs>

<!-- ground shadow -->
<ellipse cx="520" cy="478" rx="420" ry="44" fill="url(#qshadow)"/>
<ellipse cx="588" cy="510" rx="70" ry="12" fill="#3b0f05" opacity=".35"/>
<ellipse cx="828" cy="494" rx="54" ry="10" fill="#3b0f05" opacity=".3"/>
<ellipse cx="248" cy="466" rx="58" ry="10" fill="#3b0f05" opacity=".3"/>

<!-- far wheels under the body -->
<ellipse cx="440" cy="446" rx="36" ry="24" fill="#141615"/>
{wheel(828, 470, 42, 34, .55)}

<!-- side panel -->
<polygon points="{SIDE}" fill="url(#qside)"/>
<g clip-path="url(#qsideclip)">
  <polygon points="{SIDE}" fill="url(#qsideL)"/>
  <!-- gutter and roof edge -->
  <path d="M162 124 L456 84" stroke="#9d7a1e" stroke-opacity=".45" stroke-width="2"/>
  <path d="M162 126 L456 86" stroke="#fff" stroke-opacity=".35" stroke-width="1.2"/>
  <path d="M162 146 L462 108" stroke="#9d7a1e" stroke-opacity=".3" stroke-width="1.5"/>
  <!-- reflection band -->
  <polygon points="150,236 470,216 540,228 150,262" fill="#fff" opacity=".13"/>
  <!-- belt line -->
  <path d="M150 292 L548 274" stroke="#9d7a1e" stroke-opacity=".45" stroke-width="2"/>
  <path d="M150 294 L548 276" stroke="#fff" stroke-opacity=".3" stroke-width="1.2"/>
  <!-- panel seams -->
  <path d="M268 112 L262 392" stroke="#7d5f16" stroke-opacity=".5" stroke-width="1.8"/>
  <path d="M322 104 L318 398" stroke="#7d5f16" stroke-opacity=".45" stroke-width="1.6"/>
  <path d="M434 84 L434 416" stroke="#7d5f16" stroke-opacity=".6" stroke-width="2"/>
  <path d="M446 82 L448 420" stroke="#7d5f16" stroke-opacity=".6" stroke-width="2"/>
  <path d="M449 82 L451 420" stroke="#fff" stroke-opacity=".22" stroke-width="1"/>
  <!-- sliding door rail -->
  <polygon points="232,262 322,258 322,265 232,269" fill="#d7dcd8"/><polygon points="232,262 322,258 322,260 232,264" fill="#fff" opacity=".8"/>
  <!-- lower trim -->
  <polygon points="146,382 642,438 642,470 146,410" fill="url(#qtrim)"/>
  <!-- side markers -->
  <rect x="198" y="362" width="9" height="5" rx="2" fill="#E3862B"/><rect x="392" y="374" width="9" height="5" rx="2" fill="#E3862B"/>
  <!-- rear lamp edge -->
  <polygon points="146,262 156,262 156,338 146,338" fill="#A3241C"/>
</g>

<!-- logo on the side, following the panel's perspective -->
<g transform="matrix(1 -0.04 0 1 182 190)">
  <rect x="1.5" y="1.5" width="222" height="40.3" fill="#000" opacity=".12" mask="url(#qlogo)"/>
  <rect x="0" y="0" width="222" height="40.3" fill="#1c1c1c" mask="url(#qlogo)"/>
</g>

<!-- roof and windscreen -->
<polygon points="{ROOF_TOP}" fill="url(#qroof)"/>
<polygon points="{ROOF_FRONT}" fill="url(#qroof)"/>
<polygon points="{ROOF_FRONT}" fill="#000" opacity=".04"/>
<rect x="623" y="122" width="4" height="8" rx="1" fill="#2a2d2b" transform="rotate(-8 625 126)"/>
<polygon points="{SCREEN}" fill="#1a1e1d"/>
<polygon points="526,154 790,156 826,252 552,245" fill="url(#qglass)"/>
<polygon points="560,160 650,160 700,244 620,244" fill="url(#qglare)" opacity=".8"/>
<polygon points="694,162 730,162 772,246 742,246" fill="url(#qglare)" opacity=".45"/>
<!-- wipers -->
<path d="M600 244 L700 232 M700 246 L790 236" stroke="#111" stroke-width="3" stroke-linecap="round"/>

<!-- cab door window, mirror, handles -->
<polygon points="456,158 512,150 542,246 456,258" fill="url(#qglass)"/>
<polygon points="462,162 500,157 512,200 462,210" fill="url(#qglare)" opacity=".6"/>
<polygon points="456,158 512,150 542,246 456,258" fill="none" stroke="#1a1d1c" stroke-width="4" stroke-linejoin="round"/>
<path d="M494 226 h30 q8 0 8 8 v42 q0 8 -8 8 h-24 q-6 0 -6 -6 Z" fill="#1d201f"/>
<path d="M522 244 L546 252" stroke="#1d201f" stroke-width="7"/>
<rect x="500" y="234" width="5" height="40" rx="2" fill="#fff" opacity=".16"/>
<ellipse cx="410" cy="287" rx="13" ry="7" fill="#2a2d2b"/><ellipse cx="452" cy="285" rx="13" ry="7" fill="#2a2d2b"/>
<ellipse cx="560" cy="320" rx="6" ry="4" fill="#E3862B"/>

<!-- bonnet and front -->
<polygon points="{BONNET}" fill="url(#qbonnet)"/>
<path d="M548 252 L836 260" stroke="#fff" stroke-opacity=".35" stroke-width="1.5"/>
<polygon points="{FRONT}" fill="url(#qfront)"/>
<g clip-path="url(#qfrontclip)">
  <!-- black lower front and grille surround -->
  <polygon points="640,368 740,330 880,322 900,330 900,470 640,470" fill="url(#qtrim)"/>
  <polygon points="740,322 876,320 872,388 750,392" fill="#151716"/>
  {''.join(f'<path d="M{744 + k * .6:.1f} {330 + k * 11} L{872 - k * .3:.1f} {328 + k * 11}" stroke="#3f4441" stroke-width="2.5"/>' for k in range(6))}
  <polygon points="790,396 860,394 858,416 792,418" fill="#262928"/>
  <circle cx="690" cy="424" r="7" fill="#cfd4d0"/><circle cx="690" cy="424" r="3.5" fill="#fff"/>
  <path d="M652 455 L900 432" stroke="#000" stroke-opacity=".35" stroke-width="3"/>
</g>
<!-- headlamps -->
<polygon points="648,302 724,318 730,356 670,348 650,330" fill="url(#qlamp)"/>
<polygon points="648,302 724,318 730,356 670,348 650,330" fill="none" stroke="#5a6267" stroke-width="2"/>
<ellipse cx="700" cy="334" rx="12" ry="10" fill="#fff" opacity=".9"/>
<polygon points="874,302 888,306 892,350 882,348" fill="url(#qlamp)"/>
<!-- front edge highlight -->
<path d="M645 300 L652 388" stroke="#fff" stroke-opacity=".25" stroke-width="1.5"/>

<!-- arches and near wheels -->
<ellipse cx="244" cy="414" rx="48" ry="58" fill="#141615"/>
<ellipse cx="588" cy="446" rx="60" ry="72" fill="#141615"/>
{wheel(246, 420, 40, 52)}
{wheel(590, 452, 52, 66)}
</svg>'''
open('van3q.svg', 'w').write(svg)
print('ok')
