"""Real nuts behind the window.

The window artwork is a photograph, so it reads as wallpaper behind a hole: no parallax, the
photo's own baked lighting fights the scene lighting, and the nuts are far too big for a 1 kg
pack. This builds actual nut geometry inside the bag and makes the pane transparent, so depth,
occlusion, inter-nut shadows and the falloff into the bag all come out of the render.
"""
import bpy, bmesh, math, random
from mathutils import Vector

# aperture measured from the artwork mask, converted to pack-local units
WIN_X = (-0.282, 0.291)
WIN_Z = (0.152, 0.490)

NUT_COL = {                      # sRGB, converted to linear at build time
    'pecan':     [(0.63, 0.36, 0.20), (0.55, 0.29, 0.15), (0.70, 0.43, 0.26), (0.48, 0.25, 0.13)],
    'almond':    [(0.68, 0.46, 0.29), (0.58, 0.37, 0.22), (0.74, 0.53, 0.35), (0.52, 0.31, 0.18)],
    'pistachio': [(0.84, 0.78, 0.63), (0.76, 0.70, 0.55), (0.88, 0.83, 0.70), (0.70, 0.63, 0.48)],
}
NUT_LEN = {'pecan': 0.072, 'almond': 0.052, 'pistachio': 0.060}


def _lin(c):
    return tuple(v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4 for v in c)


def nut_mesh(kind, name):
    bm = bmesh.new()
    try:
        bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=13, radius=0.5)
    except TypeError:
        bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=13, diameter=1.0)
    L = NUT_LEN[kind]
    for v in bm.verts:
        p = v.co
        x, y, z = p.x * 2, p.y * 2, p.z * 2          # back to unit sphere
        if kind == 'pecan':
            # elongated half-kernel: domed one side, central groove, longitudinal ridges
            sx, sy, sz = L * 0.50, L * 0.27, L * 0.19
            taper = 1.0 - 0.18 * x * x
            sy *= taper; sz *= taper
            nz = z
            if z > 0:
                nz -= 0.62 * math.exp(-((y / 0.34) ** 2)) * (1 - 0.6 * x * x)
            ridge = 0.085 * math.sin(y * 7.5) * (1 - x * x) * (1 if z > 0 else 0.5)
            p.x, p.y, p.z = x * sx, y * sy * (1 + ridge), nz * sz
        elif kind == 'almond':
            sx, sy, sz = L * 0.50, L * 0.30, L * 0.22
            taper = 1.0 - 0.30 * max(0.0, x) ** 1.4   # one pointed end
            p.x, p.y, p.z = x * sx, y * sy * taper, z * sz * taper
        else:                                          # pistachio: ovoid shell, split seam
            sx, sy, sz = L * 0.50, L * 0.34, L * 0.32
            seam = -0.10 * math.exp(-((y / 0.30) ** 2)) if z > 0 else 0.0
            p.x, p.y, p.z = x * sx, y * sy, (z + seam) * sz
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me); bm.free()
    for poly in me.polygons:
        poly.use_smooth = True
    return me


def nut_materials(kind):
    mats = []
    for i, c in enumerate(NUT_COL[kind]):
        m = bpy.data.materials.new(f'{kind}_nut_{i}')
        m.use_nodes = True
        b = m.node_tree.nodes['Principled BSDF']
        b.inputs['Base Color'].default_value = (*_lin(c), 1)
        b.inputs['Roughness'].default_value = 0.52
        if 'Specular IOR Level' in b.inputs:
            b.inputs['Specular IOR Level'].default_value = 0.3
        nt = m.node_tree
        noise = nt.nodes.new('ShaderNodeTexNoise')
        noise.inputs['Scale'].default_value = 190.0
        noise.inputs['Detail'].default_value = 8.0
        bump = nt.nodes.new('ShaderNodeBump')
        bump.inputs['Strength'].default_value = 0.35
        bump.inputs['Distance'].default_value = 0.0025
        nt.links.new(noise.outputs['Fac'], bump.inputs['Height'])
        nt.links.new(bump.outputs['Normal'], b.inputs['Normal'])
        mats.append(m)
    return mats


def fill_with_nuts(pack_obj, kind, seed=1, layers=3):
    """Scatter nuts in the volume behind the window, in the pack's own space."""
    rng = random.Random(seed)
    me = nut_mesh(kind, f'{kind}_nut_mesh')
    mats = nut_materials(kind)
    L = NUT_LEN[kind]
    step = L * 0.72
    x0, x1 = WIN_X[0] - L * 0.9, WIN_X[1] + L * 0.9
    z0, z1 = WIN_Z[0] - L * 0.9, WIN_Z[1] + L * 0.6
    nx = max(2, int((x1 - x0) / step))
    nz = max(2, int((z1 - z0) / (step * 0.78)))
    made = []
    for li in range(layers):
        depth = -0.195 + li * 0.052                  # front layer nearest the window
        for ix in range(nx):
            for iz in range(nz):
                if li > 0 and rng.random() < 0.25:
                    continue
                ob = bpy.data.objects.new(f'{kind}_n{li}_{ix}_{iz}', me)
                bpy.context.collection.objects.link(ob)
                ob.location = (
                    x0 + (ix + 0.5 + rng.uniform(-0.3, 0.3)) * step,
                    depth + rng.uniform(-0.012, 0.012),
                    z0 + (iz + 0.5 + rng.uniform(-0.3, 0.3)) * step * 0.78,
                )
                ob.rotation_euler = (rng.uniform(-0.5, 0.5),
                                     rng.uniform(-0.45, 0.45),
                                     rng.uniform(0, math.pi * 2))
                s = rng.uniform(0.84, 1.14)
                ob.scale = (s, s, s * rng.uniform(0.9, 1.1))
                made.append(ob)
    # The mesh is shared by every nut, so a mesh-level material would make them all identical.
    # One slot, linked to the OBJECT, lets each nut carry its own shade.
    me.materials.clear()
    me.materials.append(mats[0])
    for ob in made:
        ob.material_slots[0].link = 'OBJECT'
        ob.material_slots[0].material = rng.choice(mats)
        ob.parent = pack_obj
        ob.matrix_parent_inverse = pack_obj.matrix_world.inverted()
    return made
