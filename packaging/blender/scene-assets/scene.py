"""
Regency Foods - 3D pack mockups, built in Blender / Cycles.

Run from Blender's Python console:
    exec(open('/Users/roxanneyeganeh/Desktop/regency-blender/scene.py').read())

Builds a flat-bottom (block-bottom) 1 kg pouch as real geometry, wraps the brand artwork
onto it, lights it as a studio set and ray-traces it. Shadows, contact and gloss are all
solved by the renderer rather than painted on.
"""
import bpy, bmesh, math, os, sys
from mathutils import Vector


HERE = os.path.dirname(os.path.abspath(__file__)) if '__file__' in dir() else \
       '/Users/roxanneyeganeh/Desktop/regency-blender'
TEX = os.path.join(HERE, 'tex')
OUT = os.path.join(HERE, 'renders')
os.makedirs(OUT, exist_ok=True)

# ----------------------------------------------------------------- quality switches
PREVIEW = not globals().get('FINAL', False)   # set FINAL=True in the console for the final pass
RES     = (1100, 1375) if PREVIEW else (2600, 3250)
SAMPLES = 64 if PREVIEW else 150

NUTS = ['almond', 'pecan', 'pistachio']


def srgb_lin(c):
    """Blender base colours are LINEAR. Feeding sRGB values straight in makes a pale yellow
    render as near-white, which is exactly what happened on the first pass."""
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c)


BACKDROP = srgb_lin((0.9686, 0.9373, 0.7608))   # #F7EFC2, the approved pale yellow


# ----------------------------------------------------------------- scene reset
def wipe():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for blk in (bpy.data.meshes, bpy.data.materials, bpy.data.images,
                bpy.data.lights, bpy.data.cameras):
        for b in list(blk):
            if b.users == 0:
                blk.remove(b)


# ----------------------------------------------------------------- pouch profile
# ---- MEASURED off the approved 360 spin, frame by frame. The silhouette was keyed out of
# ---- all 102 frames: frame 0 gives the front profile, frame 25 (~88 deg) the side profile,
# ---- and fitting width-against-angle across the whole turn recovers the cross-section.
# ---- The fit came out at 3.4px RMS: half-width 129px, half-depth 86px, near-rectangular.
# ---- NB this overrides what I first took off the still photo, which perspective had skewed
# ---- into looking widest at the top. The real bag has STRAIGHT sides that taper slightly IN.
W_PROF = [0.908, 0.981, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000,
          1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000,
          1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000,
          1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000, 1.000,
          0.992, 0.992, 0.985, 0.985, 0.985, 0.981, 0.977, 0.969, 0.969, 0.969, 0.962,
          0.958, 0.954, 0.954, 0.954, 0.954, 0.954, 0.954, 0.954, 0.915]
D_PROF = [0.326, 1.000, 1.000, 1.000, 1.000, 1.000, 0.988, 0.988, 0.977, 0.977, 0.977,
          0.977, 0.977, 0.977, 0.977, 0.965, 0.953, 0.953, 0.953, 0.953, 0.953, 0.953,
          0.942, 0.930, 0.930, 0.930, 0.930, 0.930, 0.907, 0.907, 0.907, 0.907, 0.895,
          0.884, 0.872, 0.860, 0.849, 0.826, 0.814, 0.791, 0.767, 0.733, 0.698, 0.651,
          0.605, 0.558, 0.500, 0.442, 0.395, 0.349, 0.291, 0.256, 0.209, 0.174, 0.163,
          0.140, 0.116, 0.105, 0.093, 0.093, 0.070, 0.058, 0.035, 0.012]
PACK_W = 0.675        # width / height, measured
PACK_D = 0.662        # depth / width, measured — the bag is far deeper than I had it
PACK_N = 6.5          # cross-section exponent: the diagonal reads WIDER than the front
                      # across the turn, which only a near-rectangular section does


def _smooth_table(t, passes=3):
    """The measured tables are 64 straight segments. Interpolating them linearly leaves the
    surface normal jumping at every one of the 64 knots, and under a glossy coat those read
    as horizontal streaks across the window. Smoothing + smoothstep makes the normal continuous."""
    t = list(t)
    for _ in range(passes):
        t = [t[0]] + [(t[i - 1] + 2 * t[i] + t[i + 1]) * 0.25 for i in range(1, len(t) - 1)] + [t[-1]]
    return t


W_PROF = _smooth_table(W_PROF)
D_PROF = _smooth_table(D_PROF)


def _sample(tbl, v):
    x = max(0.0, min(1.0, v)) * (len(tbl) - 1)
    i = int(x)
    if i >= len(tbl) - 1:
        return tbl[-1]
    f = x - i
    f = f * f * (3 - 2 * f)                      # smoothstep: zero derivative at each knot
    return tbl[i] + (tbl[i + 1] - tbl[i]) * f


def width_profile(v):
    """v: 0 at the base, 1 at the top seal. Straight from the measured silhouette."""
    return _sample(W_PROF, v)


def depth_profile(v):
    """Straight from the measured side profile: deep and full low down, tapering steadily
    from mid-height into a thin seal. No invented shoulder."""
    return max(0.012, _sample(D_PROF, v))


def ring(v, n_side, W, D, H, expo=PACK_N):
    """One closed cross-section: a superellipse, so the front and back read flat
    and the corners roll off the way formed film does."""
    a = W * 0.5 * width_profile(v)
    b = D * 0.5 * depth_profile(v)
    pts = []
    for i in range(n_side):
        th = 2 * math.pi * i / n_side
        c, s = math.cos(th), math.sin(th)
        r = (abs(c) ** expo + abs(s) ** expo) ** (-1.0 / expo)
        pts.append(Vector((a * r * c, b * r * s, v * H)))
    return pts


def build_pouch(name, H=1.0, W=PACK_W, D=PACK_W*PACK_D, n_side=140, n_up=240):
    me = bpy.data.meshes.new(name)
    bm = bmesh.new()
    rings = []
    for j in range(n_up + 1):
        v = j / n_up
        rings.append([bm.verts.new(p) for p in ring(v, n_side, W, D, H)])
    bm.verts.ensure_lookup_table()
    for j in range(n_up):
        for i in range(n_side):
            i2 = (i + 1) % n_side
            bm.faces.new((rings[j][i], rings[j][i2], rings[j + 1][i2], rings[j + 1][i]))
    bm.faces.new(list(reversed(rings[0])))                 # flat base
    bm.faces.new(rings[-1])                                # top seal
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new(name, me)
    bpy.context.collection.objects.link(ob)
    return ob


# ----------------------------------------------------------------- uv + materials
def assign_uv_and_slots(ob, W, D, H):
    """Front and back get a planar projection so the artwork is never stretched;
    the rolled corners fall to the side panel, which is plain colour anyway."""
    me = ob.data
    me.uv_layers.new(name='UVMap')
    uv = me.uv_layers.active.data
    for p in me.polygons:
        n = p.normal
        if n.y < -0.55:
            slot, axis, flip = 0, 'x', False       # FRONT
        elif n.y > 0.55:
            slot, axis, flip = 1, 'x', True        # BACK
        else:
            slot, axis, flip = 2, 'y', False       # SIDE / gusset
        p.material_index = slot
        for li in p.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            if axis == 'x':
                u = (co.x + W * 0.5) / W
            else:
                u = (co.y + D * 0.5) / D
            if flip:
                u = 1.0 - u
            uv[li].uv = (min(max(u, 0.0), 1.0), min(max(co.z / H, 0.0), 1.0))


def _img(path, non_color=False):
    im = bpy.data.images.load(path, check_existing=True)
    try:
        im.colorspace_settings.name = 'Non-Color' if non_color else 'sRGB'
    except Exception:
        pass
    return im


def window_material(name, nut):
    """The window is a clear film panel over the product, not printed artwork. It gets its own
    glossiness, a recess so the aperture has a lip, and the shadow the lip casts inside."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    art = nt.nodes.new('ShaderNodeTexImage')
    art.image = _img(os.path.join(TEX, f'pouch-{nut}-front.png'))
    art.extension = 'EXTEND'
    mask = nt.nodes.new('ShaderNodeTexImage')
    mask.image = _img(os.path.join(TEX, f'window-mask-{nut}.png'), non_color=True)
    mask.extension = 'EXTEND'
    shade_t = nt.nodes.new('ShaderNodeTexImage')
    shade_t.image = _img(os.path.join(TEX, f'window-shade-{nut}.png'), non_color=True)
    shade_t.extension = 'EXTEND'

    # product darkened by the aperture lip
    mul = nt.nodes.new('ShaderNodeMixRGB'); mul.blend_type = 'MULTIPLY'
    mul.inputs['Fac'].default_value = 1.0
    nt.links.new(art.outputs['Color'], mul.inputs['Color1'])
    nt.links.new(shade_t.outputs['Color'], mul.inputs['Color2'])
    nt.links.new(mul.outputs['Color'], bsdf.inputs['Base Color'])

    def ramp(inp, a, b):
        r = nt.nodes.new('ShaderNodeMapRange')
        r.inputs['From Min'].default_value = 0.0
        r.inputs['From Max'].default_value = 1.0
        r.inputs['To Min'].default_value = a
        r.inputs['To Max'].default_value = b
        nt.links.new(inp, r.inputs['Value'])
        return r
    # printed film is matte; the window pane is glossy and strongly coated
    nt.links.new(ramp(mask.outputs['Color'], 0.30, 0.055).outputs['Result'], bsdf.inputs['Roughness'])
    for k in ('Coat Weight', 'Clearcoat'):
        if k in bsdf.inputs:
            nt.links.new(ramp(mask.outputs['Color'], 0.05, 0.85).outputs['Result'], bsdf.inputs[k])
            break
    for k in ('Coat Roughness', 'Clearcoat Roughness'):
        if k in bsdf.inputs:
            bsdf.inputs[k].default_value = 0.035
            break
    if 'Specular IOR Level' in bsdf.inputs:
        nt.links.new(ramp(mask.outputs['Color'], 0.24, 0.62).outputs['Result'],
                     bsdf.inputs['Specular IOR Level'])
    # recess the pane so the aperture reads as a cut hole with a lip
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.55
    bump.inputs['Distance'].default_value = 0.006
    bump.invert = True
    nt.links.new(mask.outputs['Color'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])

    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return m


def film_material(name, img_path):
    """Printed film: artwork as base colour, a clearcoat for the plastic sheen,
    and a whisper of noise-driven bump so highlights crawl like real film."""
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new('ShaderNodeOutputMaterial')
    bsdf = nt.nodes.new('ShaderNodeBsdfPrincipled')
    tex = nt.nodes.new('ShaderNodeTexImage')
    tex.image = bpy.data.images.load(img_path, check_existing=True)
    tex.extension = 'EXTEND'
    try:
        tex.image.colorspace_settings.name = 'sRGB'      # artwork is sRGB, not raw data
    except Exception:
        pass
    nt.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])

    def setin(key, val):
        if key in bsdf.inputs:
            bsdf.inputs[key].default_value = val
    setin('Roughness', 0.30)
    setin('Metallic', 0.0)
    setin('IOR', 1.45)
    setin('Specular IOR Level', 0.24)
    # A heavy coat under four big softboxes turns the whole face into a mirror of the lightbox
    # and washes the colour out. Keep it low: a highlight, not a veil.
    for k in ('Coat Weight', 'Clearcoat'):
        setin(k, 0.05)
    for k in ('Coat Roughness', 'Clearcoat Roughness'):
        setin(k, 0.07)

    noise = nt.nodes.new('ShaderNodeTexNoise')
    noise.inputs['Scale'].default_value = 26.0
    noise.inputs['Detail'].default_value = 6.0
    bump = nt.nodes.new('ShaderNodeBump')
    bump.inputs['Strength'].default_value = 0.055
    nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
    nt.links.new(bump.outputs['Normal'], bsdf.inputs['Normal'])
    nt.links.new(bsdf.outputs['BSDF'], out.inputs['Surface'])
    return m


def make_pack(nut, H=1.0, W=PACK_W, D=PACK_W*PACK_D, center=False):
    ob = build_pouch('pack_' + nut, H, W, D)
    ob.data.materials.append(window_material(f'{nut}_front', nut))      # front carries the window
    for v in ('back', 'side'):
        ob.data.materials.append(
            film_material(f'{nut}_{v}', os.path.join(TEX, f'pouch-{nut}-{v}.png')))
    assign_uv_and_slots(ob, W, D, H)
    for p in ob.data.polygons:
        p.use_smooth = True
    # auto-smooth was removed as a mesh flag in 4.1+; an edge split keeps the base and the
    # seal crisp while the body stays smooth, and it behaves the same on every version
    es = ob.modifiers.new('edgesplit', 'EDGE_SPLIT')
    es.split_angle = math.radians(34)
    bev = ob.modifiers.new('bevel', 'BEVEL')
    bev.width = 0.004
    bev.segments = 2
    if center:
        # Origin to the pack's middle so it can be laid flat and spun about itself.
        # Must come AFTER the UVs are assigned - those are driven off co.z / H.
        for v in ob.data.vertices:
            v.co.z -= H * 0.5
    return ob


# ----------------------------------------------------------------- set
def cyclorama(colour):
    """Seamless sweep: floor curving up into an infinite back wall, so there is no horizon."""
    me = bpy.data.meshes.new('cyc')
    bm = bmesh.new()
    prof = []
    for i in range(41):                      # floor running back
        prof.append((-2.2 + i * 0.11, 0.0))
    r, cz = 1.6, 1.6
    for i in range(1, 25):                   # radius sweeping up to vertical
        a = math.pi * 0.5 * i / 24
        prof.append((2.2 + r * math.sin(a), cz - r * math.cos(a)))
    prof.append((2.2 + r, cz + 6.0))
    rows = []
    for (y, z) in prof:
        rows.append([bm.verts.new((x, y, z)) for x in (-9.0, 9.0)])
    for j in range(len(rows) - 1):
        bm.faces.new((rows[j][0], rows[j][1], rows[j + 1][1], rows[j + 1][0]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(me)
    bm.free()
    ob = bpy.data.objects.new('cyc', me)
    bpy.context.collection.objects.link(ob)
    m = bpy.data.materials.new('backdrop')
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*colour, 1)
    b.inputs['Roughness'].default_value = 0.92
    if 'Specular IOR Level' in b.inputs:
        b.inputs['Specular IOR Level'].default_value = 0.22
    ob.data.materials.append(m)
    for p in ob.data.polygons:
        p.use_smooth = True
    return ob


def area_light(name, loc, rot, size, energy, colour=(1, 1, 1)):
    d = bpy.data.lights.new(name, 'AREA')
    d.shape = 'RECTANGLE'
    d.size, d.size_y = size
    d.energy = energy
    d.color = colour
    ob = bpy.data.objects.new(name, d)
    ob.location, ob.rotation_euler = loc, rot
    bpy.context.collection.objects.link(ob)
    return ob


def studio():
    # Energies are tuned for a STANDARD view transform: no filmic roll-off to hide clipping,
    # so the set is lit about a third as hard as a filmic grade would be.
    area_light('key', (-2.6, -3.0, 3.4), (math.radians(52), 0, math.radians(-40)),
               (4.0, 4.0), 285)        # trimmed again: backdrop was clipping at 255,255
    # fill is small and set wide, so it opens the shadow side without reflecting back at camera
    area_light('fill', (3.4, -1.6, 1.6), (math.radians(80), 0, math.radians(68)),
               (1.8, 2.4), 60, (0.93, 0.96, 1.0))
    # moved BEHIND the packs: overhead and in front it blew the shoulders and the backdrop
    # out to white. From behind it just lifts the top edge.
    area_light('top', (0, 1.1, 3.6), (math.radians(-28), 0, 0), (0.8, 4.0), 55)
    # Dedicated background light, facing the cyclorama from behind the packs. Measured: the
    # backdrop was a full 3/4 stop under the packs, so lifting global exposure would have
    # clipped the orange before the backdrop got there. A studio lights the sweep separately.
    area_light('bg', (0, 0.9, 1.9), (math.radians(90), 0, 0), (7.0, 4.5), 165)
    # and a second aimed UP the sweep: the first one lifted the floor to target but left the
    # back wall a full stop under, because it was pointing straight at the floor.
    # 300 overshot and clipped the wall; the unclipped blue channel put it 19% hot.
    # Kept well back and broad: close in it burned a hotspot high on the sweep and the top
    # of frame went pure white. Measured 300 and 238 were both blown; this lands it on target.
    # Solved from two measured passes rather than guessed: the sweep reads 0.00374 linear per
    # watt on the blue channel, and it needs +0.253 over the unlit case to sit on #F7EFC2.
    area_light('bgwall', (0, 0.2, 2.9), (math.radians(112), 0, 0), (9.0, 5.0), 70)
    w = bpy.context.scene.world
    if w is None:
        w = bpy.data.worlds.new('World')
        bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (*srgb_lin((0.86, 0.85, 0.80)), 1)
    w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.07


def camera(target_z=0.52, dist=6.2, lens=135):
    cam = bpy.data.cameras.new('cam')
    cam.lens = lens
    ob = bpy.data.objects.new('cam', cam)
    ob.location = (0.0, -dist, target_z + 0.30)
    ob.rotation_euler = (math.radians(87.2), 0, 0)
    bpy.context.collection.objects.link(ob)
    bpy.context.scene.camera = ob
    return ob


# ----------------------------------------------------------------- render
def configure():
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = SAMPLES
    sc.cycles.use_denoising = True
    sc.cycles.max_bounces = 8
    sc.cycles.transmission_bounces = 4
    sc.render.resolution_x, sc.render.resolution_y = RES
    sc.render.resolution_percentage = 100
    sc.render.film_transparent = False
    sc.render.image_settings.file_format = 'PNG'
    # Standard, not AgX: this is packaging, and AgX desaturates saturated brand colour badly —
    # it turned the pecan orange into pale pink. Keep the lights low enough not to clip instead.
    sc.view_settings.view_transform = 'Standard'
    try:
        sc.view_settings.look = 'None'
    except Exception:
        pass
    # measured: 79% of pixels had red clipped at 255. One global stop down is more reliable
    # than nudging four light energies, and it keeps the lighting ratios intact.
    sc.view_settings.exposure = -0.42
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        for t in ('METAL', 'OPTIX', 'CUDA', 'HIP'):
            try:
                prefs.compute_device_type = t
                prefs.get_devices()
                if any(d.use for d in prefs.devices):
                    sc.cycles.device = 'GPU'
                    break
            except Exception:
                continue
    except Exception:
        pass


def hero():
    wipe()
    cyclorama(BACKDROP)
    studio()
    camera()
    H = 1.0
    # back pair, turned slightly outward and set back
    for nut, x, y, rz, s in [('almond', -0.72, 0.62, 14, 0.88),
                             ('pistachio', 0.72, 0.62, -14, 0.88)]:
        ob = make_pack(nut)
        ob.scale = (s, s, s)
        ob.location = (x, y, 0.0)
        ob.rotation_euler = (0, 0, math.radians(rz))
    hero_ob = make_pack('pecan')
    hero_ob.location = (0.0, -0.22, 0.0)
    configure()
    path = os.path.join(OUT, 'hero_preview.png' if PREVIEW else 'hero.png')
    bpy.context.scene.render.filepath = path
    print('>>> rendering', path, RES, SAMPLES, 'samples')
    bpy.ops.render.render(write_still=True)
    print('>>> DONE', path)
    return path



# ----------------------------------------------------------------- pile (flat lay)
PILE_BG = srgb_lin((0.953, 0.761, 0.800))     # lifted pink, as in the approved still

# same arrangement as the approved 2D pile, in an 800x1000 space
PILE = [('almond', 470, 30, -8), ('pecan', 760, 20, 6), ('pistachio', 60, 120, 16),
        ('pecan', 225, 110, -18), ('pistachio', 740, 235, 22), ('almond', 130, 330, 14),
        ('pistachio', 610, 330, 9), ('almond', 790, 640, 20), ('pecan', 360, 465, -17),
        ('pistachio', 135, 740, 15), ('almond', 500, 760, -19), ('pistachio', 385, 1030, 4),
        ('pecan', 150, 965, -14), ('pecan', 735, 975, 10)]

# The approved 2D pile drew each pack at 0.345 of the frame width. Matching that exactly
# puts the frame at 1.957 wide - my first pass used 2.45, which made every pack 20% small
# and left far too much pink showing.
FRAME_W, FRAME_H = 1.957, 2.446


def _obb_overlap(a, b, W, H, pad=0.90):
    """Separating-axis test between two laid-flat packs, each a W x H rectangle rotated by
    its own angle. Needed because stacking on a fixed z step made packs interpenetrate."""
    (ax, ay, aa), (bx, by, ba) = a, b
    hw, hh = W * 0.5 * pad, H * 0.5 * pad
    for (cx, cy, ca), (ox, oy, oa) in ((a, b), (b, a)):
        c, s = math.cos(ca), math.sin(ca)
        for axis in ((c, s), (-s, c)):
            lo = hi = None
            for sx in (-hw, hw):
                for sy in (-hh, hh):
                    oc, os_ = math.cos(oa), math.sin(oa)
                    px = ox + sx * oc - sy * os_
                    py = oy + sx * os_ + sy * oc
                    d = (px - cx) * axis[0] + (py - cy) * axis[1]
                    lo = d if lo is None else min(lo, d)
                    hi = d if hi is None else max(hi, d)
            half = hw if axis == (c, s) else hh
            if lo > half or hi < -half:
                return False
    return True


def pile():
    wipe()
    # floor
    me = bpy.data.meshes.new('floor')
    bm = bmesh.new()
    vs = [bm.verts.new(v) for v in [(-9, -9, 0), (9, -9, 0), (9, 9, 0), (-9, 9, 0)]]
    bm.faces.new(vs)
    bm.to_mesh(me); bm.free()
    fl = bpy.data.objects.new('floor', me)
    bpy.context.collection.objects.link(fl)
    fm = bpy.data.materials.new('pink')
    fm.use_nodes = True
    fb = fm.node_tree.nodes['Principled BSDF']
    fb.inputs['Base Color'].default_value = (*PILE_BG, 1)
    fb.inputs['Roughness'].default_value = 0.92
    if 'Specular IOR Level' in fb.inputs:
        fb.inputs['Specular IOR Level'].default_value = 0.2
    me.materials.append(fm)

    # lighting: broad soft top light so the packs cast short, clean shadows onto each other
    area_light('key', (-1.9, -2.2, 4.6), (math.radians(26), 0, math.radians(-38)), (5.0, 5.0), 620)
    area_light('fill', (2.4, 1.8, 3.4), (math.radians(-30), 0, math.radians(46)), (4.0, 4.0), 230,
               (0.95, 0.97, 1.0))
    w = bpy.context.scene.world
    if w is None:
        w = bpy.data.worlds.new('World'); bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (*srgb_lin((0.88, 0.80, 0.82)), 1)
    w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.22

    cache = {}
    lie = PACK_W * PACK_D * 0.52                       # thickness once squashed
    placed = []                                        # (x, y, angle, layer)
    for i, (nut, cx, cy, ang) in enumerate(PILE):
        if nut not in cache:
            cache[nut] = make_pack(nut, center=True)
        ob = cache[nut].copy()
        ob.data = cache[nut].data
        bpy.context.collection.objects.link(ob)
        x = (cx / 800.0 - 0.5) * FRAME_W
        y = -(cy / 1000.0 - 0.5) * FRAME_H
        a = math.radians(ang)
        # a pack rests one thickness above the highest pack it actually overlaps, so it sits
        # ON the pile instead of through it. Packs that touch nothing lie flat on the floor.
        layer = 0
        for (px, py, pa, pl) in placed:
            if _obb_overlap((x, y, a), (px, py, pa), PACK_W, 1.0):
                layer = max(layer, pl + 1)
        placed.append((x, y, a, layer))
        ob.location = (x, y, lie * 0.5 + layer * lie)
        ob.rotation_euler = (math.radians(-90), 0, a)
        ob.scale = (1.0, 0.52, 1.0)                    # a filled pouch settles when laid down
    for nut in cache:
        cache[nut].hide_render = True
        cache[nut].hide_viewport = True

    # ORTHOGRAPHIC, looking straight down. With a lens, the stacked packs sit up to 1.5 units
    # nearer the camera and render ~18% larger than the ones on the floor, which the reference
    # never does. Orthographic keeps every pack identical in size, exactly like the flat layout,
    # and lets the overlaps and shadows carry the depth instead.
    cam = bpy.data.cameras.new('cam')
    cam.type = 'ORTHO'
    cam.ortho_scale = FRAME_H
    cob = bpy.data.objects.new('cam', cam)
    cob.location = (0.0, 0.0, 7.0)
    cob.rotation_euler = (0, 0, 0)
    bpy.context.collection.objects.link(cob)
    bpy.context.scene.camera = cob

    configure()
    # Measured: pink came out (255,209,222) against the approved (243,194,204) with red
    # clipped over 47% of frame. Blue is the only unclipped channel, and it puts the scene
    # 0.28 stops hot, so the flat lay sits lower than the hero.
    bpy.context.scene.view_settings.exposure = -0.70
    path = os.path.join(OUT, 'pile_preview.png' if PREVIEW else 'pile.png')
    bpy.context.scene.render.filepath = path
    print('>>> rendering', path, RES, SAMPLES, 'samples')
    bpy.ops.render.render(write_still=True)
    print('>>> DONE', path)
    return path



# ----------------------------------------------------------------- spin (360 film)
# Timing copied from the approved flip-spin: one unbroken linear 360 in 3.4s at 30fps,
# six cuts locked to the rotation (one every 60 degrees = 17 frames), pack and backdrop
# changing on the same frame. Three backdrops, one per pack, brand colours only.
SPIN_CYCLE = 3.4
SPIN_FPS = 30
SPIN_CUTS = 6
SPIN_ORDER = ['almond', 'pistachio', 'pecan']
SPIN_BG = {'almond': (0.102, 0.196, 0.337),      # navy   #1A3256
           'pistachio': (0.910, 0.353, 0.063),   # orange #E85A10
           'pecan': (0.267, 0.686, 0.365)}       # green  #44AF5D
SPIN_RES = (1280, 720)
SPIN_SAMPLES = 40


def spin(res=SPIN_RES, samples=SPIN_SAMPLES, out_sub='spin'):
    # overrides set in the console before exec; scene.py never assigns these, so they survive
    res = globals().get('SPIN_RES_OVERRIDE') or res
    out_sub = globals().get('SPIN_OUT_OVERRIDE') or out_sub
    wipe()
    frames = int(round(SPIN_CYCLE * SPIN_FPS))          # 102
    per_cut = frames // SPIN_CUTS                       # 17

    # Backdrop: pure emission at the exact brand colour, and visible ONLY to camera rays, so
    # it renders the colour exactly and throws no light or colour cast onto the pack.
    me = bpy.data.meshes.new('bd')
    bm = bmesh.new()
    vs = [bm.verts.new(v) for v in [(-14, 6, -9), (14, 6, -9), (14, 6, 9), (-14, 6, 9)]]
    bm.faces.new(vs)
    bm.to_mesh(me); bm.free()
    bd = bpy.data.objects.new('bd', me)
    bpy.context.collection.objects.link(bd)
    bdm = bpy.data.materials.new('bd_mat')
    bdm.use_nodes = True
    nt = bdm.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    emis = nt.nodes.new('ShaderNodeEmission')
    bdout = nt.nodes.new('ShaderNodeOutputMaterial')
    nt.links.new(emis.outputs['Emission'], bdout.inputs['Surface'])
    me.materials.append(bdm)
    for attr in ('visible_diffuse', 'visible_glossy', 'visible_transmission', 'visible_volume_scatter'):
        if hasattr(bd, attr):
            setattr(bd, attr, False)

    # three-point rig on the pack alone
    area_light('key', (-2.3, -2.9, 2.2), (math.radians(70), 0, math.radians(-38)), (3.2, 3.2), 300)
    area_light('fill', (2.8, -2.2, 0.9), (math.radians(84), 0, math.radians(56)), (2.0, 2.4), 95,
               (0.94, 0.97, 1.0))
    area_light('rim', (0.4, 2.6, 2.4), (math.radians(-50), 0, 0), (2.4, 1.6), 120)
    w = bpy.context.scene.world
    if w is None:
        w = bpy.data.worlds.new('World'); bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.05, 0.05, 0.05, 1)
    w.node_tree.nodes['Background'].inputs['Strength'].default_value = 0.30

    packs = {}
    for n in SPIN_ORDER:
        ob = make_pack(n, center=True)
        ob.location = (0, 0, 0)
        packs[n] = ob

    cam = bpy.data.cameras.new('cam')
    cam.lens = 115
    cob = bpy.data.objects.new('cam', cam)
    # Blender's AUTO sensor fit maps the 36mm sensor to the LARGER render dimension, so on a
    # 16:9 frame the distance is set by WIDTH. Solving it from height directly (as I first did)
    # left only 0.96 units of vertical coverage for a pack 1.0 tall, and it overflowed.
    vert = 1.0 / 0.58                      # pack occupies 58% of frame height
    horiz = vert * res[0] / float(res[1])
    cob.location = (0.0, -horiz * cam.lens / 36.0, 0.02)
    cob.rotation_euler = (math.radians(90), 0, 0)
    bpy.context.collection.objects.link(cob)
    bpy.context.scene.camera = cob

    configure()
    sc = bpy.context.scene
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.cycles.samples = samples
    # measured at -0.42: almond red clipped and reading 214 green against a 196 target,
    # which puts the pack 0.26 stops hot
    expo = -0.68
    sc.view_settings.exposure = expo
    # the backdrop is pure emission, so cancel the exposure on it and the brand colour lands exact
    emis.inputs['Strength'].default_value = 2.0 ** (-expo)

    d = os.path.join(OUT, out_sub)
    os.makedirs(d, exist_ok=True)
    # set SPIN_ONLY to a list of frame numbers to render a spot-check instead of the whole turn
    only = globals().get('SPIN_ONLY', None)
    print('>>> spin: %d frames at %dx%d, %d samples%s'
          % (frames, res[0], res[1], samples, '' if only is None else ' (only %s)' % (only,)))
    for f in range(frames):
        if only is not None and f not in only:
            continue
        beat = min(SPIN_CUTS - 1, f // per_cut)
        nut = SPIN_ORDER[beat % 3]
        emis.inputs['Color'].default_value = (*srgb_lin(SPIN_BG[nut]), 1)
        for n, ob in packs.items():
            ob.hide_render = (n != nut)
        ang = (f / float(frames)) * 360.0            # linear, exactly one turn
        packs[nut].rotation_euler = (0, 0, math.radians(-ang))
        sc.render.filepath = os.path.join(d, 'f%04d.png' % f)
        bpy.ops.render.render(write_still=True)
        if f % 10 == 0:
            print('>>> frame', f, '/', frames, flush=True)
    print('>>> SPIN DONE', d)
    return d


# ----------------------------------------------------------------- art-directed shots
# Four more set-ups in the same world as the hero and the flat lay: same geometry, same
# materials, same Standard view transform. Only the camera and the light change, which is
# where the art direction actually lives.
#
# Light energies are not invented per shot. The hero's rig (key 285 / fill 60 / top 55 at
# exposure -0.42) lands a correctly exposed pack, and the flat lay's rig (key 620 / fill 230
# at -0.70) reproduces a pale floor at its own albedo. Both are reused as-is; what varies is
# the dedicated sweep light, because a deep green backdrop wants a fraction of the light a
# near-white one does, and a saturated yellow or orange clips long before cream would.

def _keyrig(key_e=285, fill_e=60, top_e=55, fill_loc=(3.4, -1.6, 1.6), fill_size=(1.8, 2.4)):
    # fill_loc/fill_size are exposed because the fill is a RECTANGLE and the pack has a glossy
    # coat: on a pale set its reflection vanishes into the backdrop, but on a dark one it reads
    # as a hard-edged bright panel across the window. Bigger and further back softens it out.
    area_light('key', (-2.6, -3.0, 3.4), (math.radians(52), 0, math.radians(-40)),
               (4.0, 4.0), key_e)
    area_light('fill', fill_loc, (math.radians(80), 0, math.radians(68)),
               fill_size, fill_e, (0.93, 0.96, 1.0))
    area_light('top', (0, 1.1, 3.6), (math.radians(-28), 0, 0), (0.8, 4.0), top_e)


def _sweep_lights(bg_e, wall_e):
    area_light('bg', (0, 0.9, 1.9), (math.radians(90), 0, 0), (7.0, 4.5), bg_e)
    area_light('bgwall', (0, 0.2, 2.9), (math.radians(112), 0, 0), (9.0, 5.0), wall_e)


def _world(colour, strength):
    w = bpy.context.scene.world
    if w is None:
        w = bpy.data.worlds.new('World')
        bpy.context.scene.world = w
    w.use_nodes = True
    w.node_tree.nodes['Background'].inputs['Color'].default_value = (*srgb_lin(colour), 1)
    w.node_tree.nodes['Background'].inputs['Strength'].default_value = strength


def _aim(ob, target):
    """Point an object's -Z at a point. Hand-rolled eulers are where framing errors creep in."""
    d = Vector(target) - ob.location
    ob.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()


def _cam(loc, target, lens, fstop=None, focus=None):
    c = bpy.data.cameras.new('cam')
    c.lens = lens
    ob = bpy.data.objects.new('cam', c)
    ob.location = loc
    bpy.context.collection.objects.link(ob)
    _aim(ob, target)
    if fstop:
        c.dof.use_dof = True
        c.dof.aperture_fstop = fstop
        if focus is not None:
            c.dof.focus_object = focus
        else:
            c.dof.focus_distance = (Vector(target) - Vector(loc)).length
    bpy.context.scene.camera = ob
    return ob


def _flat_floor(colour):
    me = bpy.data.meshes.new('floor')
    bm = bmesh.new()
    bm.faces.new([bm.verts.new(v) for v in [(-9, -9, 0), (9, -9, 0), (9, 9, 0), (-9, 9, 0)]])
    bm.to_mesh(me)
    bm.free()
    fl = bpy.data.objects.new('floor', me)
    bpy.context.collection.objects.link(fl)
    m = bpy.data.materials.new('floor')
    m.use_nodes = True
    b = m.node_tree.nodes['Principled BSDF']
    b.inputs['Base Color'].default_value = (*colour, 1)
    b.inputs['Roughness'].default_value = 0.92
    if 'Specular IOR Level' in b.inputs:
        b.inputs['Specular IOR Level'].default_value = 0.2
    me.materials.append(m)
    return fl


def _shot_render(name, res, samples, exposure):
    configure()
    sc = bpy.context.scene
    if PREVIEW:                       # half size, fewer samples, for checking framing
        res = (res[0] // 2, res[1] // 2)
        samples = max(40, samples // 3)
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.cycles.samples = samples
    sc.view_settings.exposure = exposure
    path = os.path.join(OUT, name + ('_preview.png' if PREVIEW else '.png'))
    sc.render.filepath = path
    print('>>> rendering', path, res, samples, 'samples', flush=True)
    bpy.ops.render.render(write_still=True)
    print('>>> DONE', path, flush=True)
    return path


def shot_low():
    """Low three-quarter on deep brand green. The camera sits almost on the floor, so the
    pack towers and the gusset crease catches the key down its whole length. The sweep is
    lit at a sixth of the hero's level, so the green stays deep instead of going minty."""
    wipe()
    cyclorama(srgb_lin((0.098, 0.204, 0.161)))        # #193429
    _keyrig(300, 26, 60, fill_loc=(4.8, -2.9, 1.25), fill_size=(4.2, 4.2))
    _sweep_lights(28, 11)
    _world((0.25, 0.32, 0.28), 0.05)
    ob = make_pack('pecan')
    ob.rotation_euler = (0, 0, math.radians(32))
    _cam((1.35, -3.90, 0.30), (0.0, 0.0, 0.52), 100)
    return _shot_render('shot-low-threequarter', (2000, 2500), 150, -0.42)


def shot_row():
    """Three packs in one straight row, all turned the same way, shot square on. Yellow sweep,
    lit well under the hero's level because #F2C44B starts at 242 in red and would clip if it
    were lit like cream."""
    wipe()
    cyclorama(srgb_lin((0.949, 0.769, 0.294)))        # #F2C44B
    _keyrig()
    _sweep_lights(70, 28)
    _world((0.86, 0.85, 0.80), 0.07)
    # One straight line, one shared angle: every pack on the same y, every pack turned 24
    # degrees the same way, so the three read as a single row rather than a staggered group.
    # Spacing is 0.95 against a projected width of 0.80 (0.675 of face plus 0.182 of gusset
    # once turned), which leaves an even 0.15 of air between them.
    for nut, x in [('almond', -0.95), ('pecan', 0.0), ('pistachio', 0.95)]:
        ob = make_pack(nut)
        ob.location = (x, 0.0, 0.0)
        ob.rotation_euler = (0, 0, math.radians(24))
    # Dead centre and close to level. No depth of field now: with every pack at the same
    # distance there is nothing to throw out of focus, and softening the sweep would only
    # muddy it. 70mm at 6.2m covers 3.19 wide against a 2.70 line-up, so the air is even.
    _cam((0.0, -6.20, 0.80), (0.0, 0.0, 0.52), 70)
    return _shot_render('shot-row', (2800, 1750), 150, -0.42)


def shot_trio():
    """Flat lay, straight down, three packs evenly spaced on cream with real air around them -
    a banner crop. Orthographic for the same reason the pile is: a lens would make whichever
    pack sits nearest the camera render larger, and on a line-up that reads as a mistake.
    Lights and exposure are the flat lay's, which reproduce a pale floor at its own albedo."""
    wipe()
    _flat_floor(srgb_lin((0.973, 0.949, 0.886)))       # #F8F2E2
    area_light('key', (-1.9, -2.2, 4.6), (math.radians(26), 0, math.radians(-38)),
               (5.0, 5.0), 620)
    area_light('fill', (2.4, 1.8, 3.4), (math.radians(-30), 0, math.radians(46)),
               (4.0, 4.0), 230, (0.95, 0.97, 1.0))
    _world((0.88, 0.86, 0.80), 0.22)
    lie = PACK_W * PACK_D * 0.52
    for nut, x, ang in [('almond', -0.86, -6), ('pecan', 0.0, 3), ('pistachio', 0.86, -2)]:
        ob = make_pack(nut, center=True)
        ob.location = (x, 0.0, lie * 0.5)
        ob.rotation_euler = (math.radians(-90), 0, math.radians(ang))
        ob.scale = (1.0, 0.52, 1.0)
    cam = bpy.data.cameras.new('cam')
    cam.type = 'ORTHO'
    cam.ortho_scale = 3.25
    cob = bpy.data.objects.new('cam', cam)
    cob.location = (0.0, 0.0, 7.0)
    bpy.context.collection.objects.link(cob)
    bpy.context.scene.camera = cob
    # -0.70 is the flat lay's figure, tuned against a PINK floor. Cream is 0.34 stops
    # brighter in blue and bounces much more light back into the set: at -0.70 the floor
    # clipped to pure white across 55% of frame and the shadows under the packs vanished.
    return _shot_render('shot-trio-flatlay', (3000, 1500), 150, -1.05)


def shot_macro():
    """Tight on the window, the badge and the resealable pill - the craft shot. Shallow at
    f/4 so the far edge of the pack softens, which is what sells it as a photograph rather
    than a render. Framed to 0.69m across at 135mm, so the window fills about four fifths."""
    wipe()
    cyclorama(srgb_lin((0.910, 0.353, 0.063)))        # #E85A10
    _keyrig(285, 70, 55)
    _sweep_lights(60, 24)
    _world((0.86, 0.85, 0.80), 0.07)
    ob = make_pack('almond')
    ob.rotation_euler = (0, 0, math.radians(17))
    # Aim dropped 0.055 from the first pass: it sliced the word 'Almond' and the strapline
    # through the middle, which reads as a framing error rather than a deliberate crop.
    # Now the top edge sits just under the dotted rule and the base grounds the bottom.
    _cam((0.78, -2.55, 0.465), (0.0, -0.10, 0.275), 135, fstop=4.0)
    return _shot_render('shot-window-macro', (2200, 2200), 180, -0.42)


SHOTS = {'shot_low': shot_low, 'shot_row': shot_row,
         'shot_trio': shot_trio, 'shot_macro': shot_macro}


print('Blender', bpy.app.version_string)
SCENE = globals().get('SCENE', 'hero')
SCENES = {'hero': hero, 'pile': pile, 'spin': spin}
SCENES.update(SHOTS)
SCENES[SCENE]()
