"""Redrawn Regency Foods van (high-roof panel van, side profile facing right, light from upper left)."""
HN = 'font-family="Helvetica Neue RF, Helvetica, Arial"'


def wheel(cx, cy, r=58):
    holes = ''.join(
        f'<circle cx="{cx + 20 * __import__("math").cos(a):.1f}" cy="{cy + 20 * __import__("math").sin(a):.1f}" r="5" fill="#2a2d2b"/>'
        for a in [i * 1.0472 for i in range(6)])
    return f'''<g>
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="#181a19"/>
  <circle cx="{cx}" cy="{cy}" r="{r - 6}" fill="none" stroke="#2b2e2c" stroke-width="3"/>
  {''.join(f'<line x1="{cx}" y1="{cy - r + 2}" x2="{cx}" y2="{cy - r + 9}" stroke="#2f3331" stroke-width="3" transform="rotate({k * 15} {cx} {cy})"/>' for k in range(24))}
  <circle cx="{cx}" cy="{cy}" r="{r * .6:.1f}" fill="url(#vrim)"/>
  <circle cx="{cx}" cy="{cy}" r="{r * .6:.1f}" fill="none" stroke="#5d625f" stroke-width="2"/>
  {holes}
  <circle cx="{cx}" cy="{cy}" r="11" fill="#8e9590"/><circle cx="{cx}" cy="{cy}" r="5" fill="#3a3e3c"/>
  <path d="M{cx - r * .45:.1f} {cy - r * .3:.1f} A{r * .55:.1f} {r * .55:.1f} 0 0 1 {cx + r * .1:.1f} {cy - r * .54:.1f}" fill="none" stroke="#fff" stroke-opacity=".45" stroke-width="3" stroke-linecap="round"/>
</g>'''


BODY = ('M92 404 L92 150 Q92 116 126 113 L616 100 Q652 99 676 116 L700 134 '
        'L792 246 Q800 256 814 260 L888 280 Q912 287 914 312 L916 398 '
        'L800 400 A64 64 0 0 0 676 400 L296 404 A64 64 0 0 0 168 404 Z')

svg = f'''<svg class="redraw-van" viewBox="40 60 920 460" role="img" aria-label="The yellow Regency Foods delivery van" xmlns="http://www.w3.org/2000/svg">
<defs>
  <linearGradient id="vbody" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#F7D06A"/><stop offset=".08" stop-color="#F0C24A"/><stop offset=".55" stop-color="#E7B53C"/>
    <stop offset=".86" stop-color="#C99A2B"/><stop offset="1" stop-color="#A97F22"/></linearGradient>
  <linearGradient id="vsheen" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".35" stop-color="#fff" stop-opacity=".28"/><stop offset=".55" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <linearGradient id="vglass" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5d6f78"/><stop offset=".45" stop-color="#2a363c"/><stop offset="1" stop-color="#1a2226"/></linearGradient>
  <linearGradient id="vglare" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".35"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  <radialGradient id="vrim" cx=".42" cy=".38" r=".7"><stop offset="0" stop-color="#e6eae7"/><stop offset=".6" stop-color="#a9b0ab"/><stop offset="1" stop-color="#6c736e"/></radialGradient>
  <radialGradient id="vshadow"><stop offset="0" stop-color="#3b0f05" stop-opacity=".45"/><stop offset=".65" stop-color="#3b0f05" stop-opacity=".16"/><stop offset="1" stop-color="#3b0f05" stop-opacity="0"/></radialGradient>
  <linearGradient id="vtrim" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3a3d3b"/><stop offset="1" stop-color="#1c1e1d"/></linearGradient>
  <clipPath id="vclip"><path d="{BODY}"/></clipPath>
  <mask id="vlogo" style="mask-type:alpha" maskUnits="userSpaceOnUse"><image href="assets/logo/logo-horizontal.png" x="150" y="196" width="300" height="54.4"/></mask>
</defs>

<ellipse cx="505" cy="470" rx="470" ry="30" fill="url(#vshadow)"/>
<ellipse cx="232" cy="466" rx="92" ry="12" fill="#3b0f05" opacity=".35"/>
<ellipse cx="738" cy="466" rx="92" ry="12" fill="#3b0f05" opacity=".35"/>

<!-- far-side wheels peeking under the body -->
<rect x="190" y="400" width="80" height="44" rx="8" fill="#141615"/>
<rect x="700" y="398" width="80" height="44" rx="8" fill="#141615"/>

<!-- body -->
<path d="{BODY}" fill="url(#vbody)"/>
<g clip-path="url(#vclip)">
  <!-- roof edge and rain gutter -->
  <path d="M100 134 L640 118" stroke="#fff" stroke-opacity=".45" stroke-width="3"/>
  <path d="M96 150 L652 136" stroke="#9d7a1e" stroke-opacity=".35" stroke-width="2"/>
  <!-- long reflection band -->
  <rect x="92" y="262" width="830" height="26" fill="url(#vsheen)"/>
  <!-- swage line -->
  <path d="M96 312 L900 304" stroke="#9d7a1e" stroke-opacity=".45" stroke-width="2"/>
  <path d="M96 314 L900 306" stroke="#fff" stroke-opacity=".35" stroke-width="1.5"/>
  <!-- panel seams: sliding door and cab door -->
  <path d="M416 120 V392 M418 120 V392" stroke="#7d5f16" stroke-opacity=".55" stroke-width="1.6"/>
  <path d="M606 112 V396" stroke="#7d5f16" stroke-opacity=".6" stroke-width="2"/>
  <path d="M609 112 V396" stroke="#fff" stroke-opacity=".25" stroke-width="1"/>
  <path d="M420 288 H600" stroke="#7d5f16" stroke-opacity=".5" stroke-width="2"/>
  <!-- sliding door rail -->
  <rect x="120" y="282" width="290" height="5" rx="2.5" fill="#cfd4d0"/><rect x="120" y="282" width="290" height="2" rx="1" fill="#fff" opacity=".7"/>
  <!-- lower black trim -->
  <path d="M92 370 L916 362 L916 420 L92 420 Z" fill="url(#vtrim)"/>
  <path d="M92 371 L916 363" stroke="#fff" stroke-opacity=".18"/>
  <!-- rear lamp -->
  <rect x="92" y="300" width="9" height="46" rx="3" fill="#B3261E"/><rect x="92" y="300" width="9" height="12" rx="3" fill="#E39A2B"/>
</g>

<!-- windows -->
<path d="M614 138 L688 136 Q696 136 702 144 L782 244 Q786 250 778 250 L614 250 Z" fill="url(#vglass)"/>
<path d="M628 142 L690 141 L752 222 L700 222 Z" fill="url(#vglare)" opacity=".7"/>
<path d="M614 138 L688 136 Q696 136 702 144 L782 244 Q786 250 778 250 L614 250 Z" fill="none" stroke="#1a1d1c" stroke-width="5"/>
<path d="M704 132 L798 248 L806 256 L790 256 L700 140 Z" fill="#1d2629"/>
<!-- wing mirror -->
<path d="M770 236 h26 q8 0 8 8 v30 q0 8 -8 8 h-20 q-6 0 -6 -6 Z" fill="#1d201f"/>
<rect x="778" y="244" width="5" height="26" rx="2" fill="#fff" opacity=".18"/>
<!-- door handles -->
<rect x="572" y="272" width="26" height="7" rx="3.5" fill="#2a2d2b"/><rect x="640" y="272" width="26" height="7" rx="3.5" fill="#2a2d2b"/>
<!-- front: headlamp, grille, bumper -->
<path d="M866 292 L906 300 Q912 302 912 310 L912 326 L870 320 Q862 318 862 310 Z" fill="#dfe5e9"/>
<path d="M870 296 L904 303 L904 312 L872 307 Z" fill="#fff" opacity=".9"/>
<path d="M872 330 L916 334 L916 362 L874 360 Z" fill="#1b1d1c"/>
{''.join(f'<line x1="874" y1="{336 + k * 6}" x2="915" y2="{339 + k * 6}" stroke="#4a4f4c" stroke-width="1.5"/>' for k in range(4))}
<rect x="880" y="372" width="34" height="10" rx="3" fill="#cfd4d0" opacity=".8"/>
<!-- indicator on wing -->
<rect x="826" y="300" width="14" height="5" rx="2.5" fill="#E39A2B"/>

<!-- the Regency Foods logo on the side -->
<rect x="150" y="198" width="300" height="54.4" fill="#000" opacity=".12" mask="url(#vlogo)" transform="translate(1.5 1.5)"/>
<rect x="150" y="196" width="300" height="54.4" fill="#1a1a1a" mask="url(#vlogo)"/>
<text x="300" y="340" text-anchor="middle" {HN} font-size="13" letter-spacing="2" fill="#5a4410" opacity=".85">NEXT-DAY DELIVERY · REGENCYFOODS.COM</text>

<!-- arch liners -->
<path d="M168 404 A64 64 0 0 1 296 404" fill="none" stroke="#151716" stroke-width="10"/>
<path d="M676 400 A64 64 0 0 1 800 400" fill="none" stroke="#151716" stroke-width="10"/>
{wheel(232, 410)}
{wheel(738, 408)}
</svg>'''
open('van.svg', 'w').write(svg)
print('ok')
