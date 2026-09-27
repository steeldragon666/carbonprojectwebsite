"""Cloud reference build of the buggy body in cadquery (OpenCascade).

Builds the identical geometry that fusion_buggy_body.py builds in Fusion so
the two kernels can be cross-checked by volume, and produces the STEP / STL /
PNG deliverables without needing a Fusion seat.

    python build_reference.py [--out exports] [--fast]

--fast skips the boolean union of the lattices (keeps them as compounds).
"""
import argparse
import json
import math
import os
import sys
import time

import cadquery as cq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from buggy_geometry import BuggyBody  # noqa: E402


def V(p):
    return cq.Vector(*p)


def tube(a, b, r):
    d = V(b) - V(a)
    return cq.Solid.makeCylinder(r, d.Length, V(a), d.normalized())


def tube_group(tubes, union=True):
    solids = []
    nodes = {}
    for name, group, a, b, r in tubes:
        solids.append(tube(a, b, r))
        for p in (a, b):
            key = tuple(round(c, 1) for c in p)
            nodes[key] = max(nodes.get(key, 0.0), r)
    spheres = [cq.Solid.makeSphere(r * 1.02, V(k), angleDegrees1=-90, angleDegrees2=90) for k, r in nodes.items()]
    shape = cq.Compound.makeCompound(solids + spheres)
    if union:
        try:
            shape = cq.Workplane().add(solids + spheres).combine(glue=False).val()
        except Exception as exc:  # pragma: no cover - kernel dependent
            print("  union failed (%s); keeping compound" % exc)
    return shape


def loft_sections(section_points):
    wires = []
    for x, pts in section_points:
        w = cq.Workplane("YZ", origin=(x, 0, 0)).spline([(p[1], p[2]) for p in pts], periodic=True).close().wire().val()
        wires.append(w)
    return cq.Solid.makeLoft(wires, ruled=False)


def shell_open(solid, pick, thickness):
    """Shell a solid removing the face chosen by pick(face) -> score (max wins)."""
    faces = list(solid.Faces())
    face = max(faces, key=pick)
    try:
        return cq.Workplane().add(solid).faces(cq.selectors.NearestToPointSelector(face.Center().toTuple())).shell(-thickness).val()
    except Exception as exc:
        print("  shell failed (%s); keeping solid" % exc)
        return solid


def box(x0, x1, y0, y1, z0, z1):
    return cq.Solid.makeBox(x1 - x0, y1 - y0, z1 - z0, V((x0, y0, z0)))


def build(body, fast=False):
    t0 = time.time()
    out = {}
    p = body.p
    t = p["skin_thickness"]

    print("frame tubes ...")
    out["Cage"] = tube_group(body.tubes, union=not fast)
    print("lattices ...")
    for grp, key in (("lattice", "SideRibs"), ("canopy", "Canopy"), ("grille", "Grille")):
        out[key] = tube_group([tt for tt in body.lattice_tubes if tt[1] == grp], union=not fast)

    print("tub ...")
    z0, z1 = body.tub_z
    wires = []
    for half, z in ((body.tub_outline_half, z0), (body.tub_sill_half, z1)):
        poly = half + [(x, -hw) for (x, hw) in reversed(half)]
        wires.append(cq.Workplane("XY", origin=(0, 0, z)).polyline(poly).close().wire().val())
    tub = cq.Solid.makeLoft(wires, ruled=True)
    tub = shell_open(tub, lambda f: f.Center().z, t)
    dn = body.door_notch
    for s in (1, -1):
        y0, y1 = (dn["y_min"], 2000) if s > 0 else (-2000, -dn["y_min"])
        tub = tub.cut(box(dn["x0"], dn["x1"], y0, y1, dn["z0"], dn["z1"]))
    out["Tub"] = tub

    print("hood / deck lofts ...")
    hood = loft_sections(body.section_points["Hood"])
    hood = shell_open(hood, lambda f: -f.Center().x, t)
    deck = loft_sections(body.section_points["Deck"])
    deck = shell_open(deck, lambda f: f.Center().x, t)
    cx0, cx1, cy0, cy1 = body.canopy_opening
    deck = deck.cut(box(cx0, cx1, cy0, cy1, body.sill_z - 200, body.sill_z + 400))
    out["Hood"], out["Deck"] = hood, deck

    print("spine channel ...")
    sc = body.spine_channel
    chan = box(sc["x0"], sc["x1"], -sc["hy"], sc["hy"], sc["z0"], sc["z1"])
    for k in ("Tub", "Hood", "Deck"):
        out[k] = out[k].cut(chan)

    print("fenders ...")
    for f in body.fenders:
        c = f["centre"]
        a0, a1 = math.radians(f["a0"]), math.radians(f["a1"])
        am = 0.5 * (a0 + a1)
        def pt(r, a):
            return (c[0] + r * math.sin(a), c[2] + r * math.cos(a))
        wp = (cq.Workplane("XZ", origin=(0, c[1] + 0.5 * f["width"], 0))
              .moveTo(*pt(f["r_in"], a0)).threePointArc(pt(f["r_in"], am), pt(f["r_in"], a1))
              .lineTo(*pt(f["r_out"], a1)).threePointArc(pt(f["r_out"], am), pt(f["r_out"], a0))
              .close().extrude(f["width"]))
        out[f["name"]] = wp.val()

    print("seats / fittings ...")
    for s in body.seats:
        y0 = s["y"] - 0.5 * s["width"]
        cushion = cq.Workplane("XZ", origin=(0, y0 + s["width"], 0)).polyline(s["cushion"]).close().extrude(s["width"]).val()
        back = cq.Workplane("XZ", origin=(0, y0 + s["width"], 0)).polyline(s["back"]).close().extrude(s["width"]).val()
        out[s["name"]] = cushion.fuse(back)
    sw = body.steering_wheel
    out["SteeringWheel"] = cq.Solid.makeTorus(sw["major_r"], sw["minor_r"], V(sw["centre"]), V(sw["axis"]))
    lb = body.light_bar
    c, sz = lb["centre"], lb["size"]
    out["LightBar"] = box(c[0] - sz[0] / 2, c[0] + sz[0] / 2, c[1] - sz[1] / 2, c[1] + sz[1] / 2, c[2] - sz[2] / 2, c[2] + sz[2] / 2)

    print("reference wheels + chassis ...")
    for w in body.wheels:
        c, ax = w["centre"], w["axis"]
        inner = V((c[0], c[1] - ax[1] * 0.5 * w["tyre_w"], c[2]))
        out[w["name"]] = cq.Solid.makeCylinder(w["tyre_r"], w["tyre_w"], inner, V(ax))
        rin = V((c[0], c[1] - ax[1] * 0.5 * w["rim_w"], c[2]))
        out[w["name"] + "Rim"] = cq.Solid.makeCylinder(w["rim_r"], w["rim_w"], rin, V(ax))
    out["ChassisEnvelope"] = box(-body.L / 2, body.L / 2, -body.W / 2, body.W / 2, body.gc, body.gc + body.H)
    print("built in %.1fs" % (time.time() - t0))
    return out


GROUPS = {
    "structure": ["Cage", "SideRibs", "Canopy", "Grille"],
    "skins": ["Tub", "Hood", "Deck", "FenderFL", "FenderFR", "FenderRL", "FenderRR"],
    "fittings": ["SeatL", "SeatR", "SteeringWheel", "LightBar"],
    "reference": ["WheelFL", "WheelFLRim", "WheelFR", "WheelFRRim", "WheelRL", "WheelRLRim",
                  "WheelRR", "WheelRRRim", "ChassisEnvelope"],
}
COLOURS = {"structure": (0.20, 0.20, 0.22), "skins": (0.96, 0.77, 0.0), "fittings": (0.12, 0.12, 0.12),
           "reference": (0.45, 0.45, 0.42)}


def render(shapes, out_dir):
    """Software-rendered views with matplotlib (no GPU needed)."""
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection

    tris, cols = [], []
    for grp, names in GROUPS.items():
        for n in names:
            if n not in shapes or n == "ChassisEnvelope":
                continue
            verts, faces = shapes[n].tessellate(6.0, 0.6)
            vv = np.array([v.toTuple() for v in verts])
            for f in faces:
                tris.append(vv[list(f)])
                cols.append(COLOURS[grp])
    tris = np.array(tris)
    cols = np.array(cols)
    # crude directional shading
    n = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-9
    light = np.array([0.4, -0.5, 0.75]); light /= np.linalg.norm(light)
    shade = 0.45 + 0.55 * np.abs(n @ light)
    cols = np.clip(cols * shade[:, None], 0, 1)
    views = {"iso_front": (28, -50), "iso_rear": (24, 135), "side": (0, -90), "front": (0, 0), "top": (90, -90)}
    for name, (elev, azim) in views.items():
        fig = plt.figure(figsize=(14, 9), dpi=110)
        ax = fig.add_subplot(111, projection="3d")
        ax.add_collection3d(Poly3DCollection(tris, facecolors=cols, edgecolor="none"))
        lo, hi = tris.reshape(-1, 3).min(0), tris.reshape(-1, 3).max(0)
        c, ext = 0.5 * (lo + hi), (hi - lo)
        r = 0.5 * ext.max() * (0.62 if name in ("side", "front", "top") else 0.7)
        ax.set_xlim(c[0] - r, c[0] + r); ax.set_ylim(c[1] - r, c[1] + r); ax.set_zlim(c[2] - r, c[2] + r)
        ax.set_box_aspect((1, 1, 1)); ax.view_init(elev=elev, azim=azim); ax.set_axis_off()
        ax.set_proj_type("ortho" if name in ("side", "front", "top") else "persp")
        fig.subplots_adjust(0, 0, 1, 1)
        fig.savefig(os.path.join(out_dir, "render_%s.png" % name), facecolor="#f4f1ea")
        plt.close(fig)
        print("  render_%s.png" % name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "exports"))
    ap.add_argument("--fast", action="store_true")
    ap.add_argument("--no-render", action="store_true")
    args = ap.parse_args()
    os.makedirs(args.out, exist_ok=True)

    body = BuggyBody()
    shapes = build(body, fast=args.fast)

    report = {"summary": body.summary(), "volumes_mm3": {}, "bbox_mm": {}}
    for name, sh in shapes.items():
        try:
            report["volumes_mm3"][name] = round(sh.Volume(), 1)
            bb = sh.BoundingBox()
            report["bbox_mm"][name] = [round(v, 1) for v in (bb.xmin, bb.ymin, bb.zmin, bb.xmax, bb.ymax, bb.zmax)]
        except Exception as exc:
            report["volumes_mm3"][name] = "n/a (%s)" % exc
    skin_vol = sum(report["volumes_mm3"][k] for k in GROUPS["skins"] if isinstance(report["volumes_mm3"][k], float))
    report["summary"]["skin_mass_kg"] = skin_vol * 1.55e-6
    report["summary"]["body_mass_estimate_kg"] = report["summary"]["skin_mass_kg"] + report["summary"]["tube_mass_total_kg"]
    with open(os.path.join(args.out, "reference_report.json"), "w") as fh:
        json.dump(report, fh, indent=2)
    print(json.dumps(report["summary"], indent=2))

    print("exporting STEP / STL ...")
    asm = cq.Assembly(name="FlattopBuggyBody")
    for grp, names in GROUPS.items():
        for n in names:
            if n in shapes:
                asm.add(shapes[n], name=n, color=cq.Color(*COLOURS[grp]))
    asm.save(os.path.join(args.out, "buggy_body_reference.step"))
    vis = [shapes[n] for g in ("structure", "skins", "fittings") for n in GROUPS[g] if n in shapes]
    cq.exporters.export(cq.Workplane().add(cq.Compound.makeCompound(vis)), os.path.join(args.out, "buggy_body_reference.stl"), tolerance=1.0)
    if not args.no_render:
        print("rendering ...")
        render(shapes, args.out)
    print("done")


if __name__ == "__main__":
    main()
