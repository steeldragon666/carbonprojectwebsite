"""Flattop Buggy - body build script for Autodesk Fusion.

Run inside Fusion (Utilities > Add-Ins > Scripts, "+" and pick this file, Run)
with the chassis document (cp-proto-flattop) active.  The script:

  1. measures the bounding box of every visible solid in the active design
     (that is the chassis spine: batteries, range extender, motors);
  2. derives the body from that envelope (buggy_geometry.BuggyBody);
  3. builds the body as ONE new component "Buggy Body" placed around the
     chassis - nothing in the existing design is modified;
  4. writes fusion_report.json (volumes, bounding boxes, mass estimate)
     and exports the component as STEP + F3D next to this file.

Everything is undoable in one step (delete the "Buggy Body" component).

Coordinates: buggy_geometry works in mm, X forward, Z up, ground at Z = 0.
The Fusion API works in cm.  All conversion happens in the helpers below;
the placement matrix of the "Buggy Body" occurrence maps the design frame onto
the document's frame (Y-up or Z-up, chassis long axis = forward).
"""
import importlib
import json
import math
import os
import sys
import time
import traceback

import adsk.core
import adsk.fusion

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import buggy_geometry  # noqa: E402
importlib.reload(buggy_geometry)

# ---------------------------------------------------------------------------
# Configuration - edit here
# ---------------------------------------------------------------------------
CONFIG = dict(
    build_in_new_document=False,  # True: measure the chassis, then build in a fresh document
    chassis_bbox_mm=None,         # ((xmin, ymin, zmin), (xmax, ymax, zmax)) in document mm - overrides measurement
    up_axis=None,                 # "Y" or "Z"; None = read the modelling-orientation preference
    forward_sign=+1,              # flip to -1 if the nose comes out at the wrong end of the chassis
    ground_clearance_mm=400.0,    # ground plane sits this far below the chassis belly
    union_lattices=True,          # boolean each lattice into one body (slower, cleaner)
    export_step=True,
    export_f3d=True,
    geometry_overrides=dict(       # any buggy_geometry.DEFAULT_PARAMS key
        driver_side="right",
    ),
)

COMPONENT_NAME = "Buggy Body"
MM = 0.1  # mm -> cm

# ---------------------------------------------------------------------------
# Pure-Python placement maths (unit-tested outside Fusion)
# ---------------------------------------------------------------------------
def compute_placement(bbox_min, bbox_max, up_axis, forward_sign=1, ground_clearance=400.0):
    """Map the design frame (X fwd, Y left, Z up, ground z=0, origin under the
    chassis centre) onto the document frame.

    Returns (origin, x_axis, y_axis, z_axis, spine_L, spine_W, spine_H) with
    vectors in document coordinates, lengths in the caller's units."""
    axes = {"X": (1.0, 0.0, 0.0), "Y": (0.0, 1.0, 0.0), "Z": (0.0, 0.0, 1.0)}
    up_i = "XYZ".index(up_axis)
    ext = [bbox_max[i] - bbox_min[i] for i in range(3)]
    horiz = [i for i in range(3) if i != up_i]
    fwd_i = max(horiz, key=lambda i: ext[i])
    left_i = [i for i in horiz if i != fwd_i][0]
    up = axes["XYZ"[up_i]]
    fwd = tuple(forward_sign * c for c in axes["XYZ"[fwd_i]])
    # left = up x fwd (right-handed: Z x X = Y)
    left = (up[1] * fwd[2] - up[2] * fwd[1], up[2] * fwd[0] - up[0] * fwd[2], up[0] * fwd[1] - up[1] * fwd[0])
    centre = [0.5 * (bbox_min[i] + bbox_max[i]) for i in range(3)]
    origin = list(centre)
    origin[up_i] = bbox_min[up_i] - ground_clearance
    return (tuple(origin), fwd, left, up, ext[fwd_i], ext[left_i], ext[up_i])


# ---------------------------------------------------------------------------
# Fusion helpers
# ---------------------------------------------------------------------------
class Ctx:
    """Everything the stages share."""
    app = None
    ui = None
    design = None
    body = None          # BuggyBody
    root = None          # our top-level component
    comps = {}           # sub components by name
    tbm = None
    log_lines = []
    failures = []
    created = {}         # body name -> BRepBody
    placement = None
    t0 = 0.0


C = Ctx()


def log(msg):
    line = "[%6.1fs] %s" % (time.time() - C.t0, msg)
    C.log_lines.append(line)
    try:
        with open(os.path.join(HERE, "fusion_build.log"), "a") as fh:
            fh.write(line + "\n")
    except Exception:
        pass


def P(p):
    """mm design point -> cm Point3D."""
    return adsk.core.Point3D.create(p[0] * MM, p[1] * MM, p[2] * MM)


def Vec(v):
    return adsk.core.Vector3D.create(v[0], v[1], v[2])


def real(mm):
    return adsk.core.ValueInput.createByReal(mm * MM)


def sub_component(name):
    if name in C.comps:
        return C.comps[name]
    occ = C.root.occurrences.addNewComponent(adsk.core.Matrix3D.create())
    occ.component.name = name
    C.comps[name] = occ.component
    return occ.component


def offset_plane(comp, base_plane, offset_mm, name):
    """Construction plane parallel to a base plane at a signed design-frame
    offset.  Fusion's XZ plane normal points to -Y, so a positive offset can
    land on the wrong side: read the plane back and flip if needed."""
    def make(off):
        pi = comp.constructionPlanes.createInput()
        pi.setByOffset(base_plane, real(off))
        pl = comp.constructionPlanes.add(pi)
        pl.name = name
        return pl

    pl = make(offset_mm)
    try:
        n = base_plane.geometry.normal
        o = pl.geometry.origin
        along = (o.x * n.x + o.y * n.y + o.z * n.z) / MM   # mm along the base normal
        want = offset_mm
        if abs(along - want) > 0.5 and abs(along + want) <= 0.5:
            pl.deleteMe()
            pl = make(-offset_mm)
            log("plane %s: offset sign flipped to land at %.1f mm" % (name, want))
    except Exception:
        pass
    return pl


def sketch_points(sk, pts_mm):
    """Design points (mm) -> sketch-space Point3D via the sketch's own mapping."""
    return [sk.modelToSketchSpace(P(p)) for p in pts_mm]


def add_polyline(sk, pts_mm):
    sp = sketch_points(sk, pts_mm)
    lines = sk.sketchCurves.sketchLines
    n = len(sp)
    for i in range(n):
        lines.addByTwoPoints(sp[i], sp[(i + 1) % n])


def add_closed_spline(sk, pts_mm):
    sp = sketch_points(sk, pts_mm)
    col = adsk.core.ObjectCollection.create()
    for p in sp:
        col.add(p)
    col.add(sp[0])
    return sk.sketchCurves.sketchFittedSplines.add(col)


def temp_box(x0, x1, y0, y1, z0, z1):
    c = P(((x0 + x1) / 2.0, (y0 + y1) / 2.0, (z0 + z1) / 2.0))
    obb = adsk.core.OrientedBoundingBox3D.create(c, Vec((1, 0, 0)), Vec((0, 1, 0)),
                                                 (x1 - x0) * MM, (y1 - y0) * MM, (z1 - z0) * MM)
    return C.tbm.createBox(obb)


def temp_cylinder(p0, p1, r_mm):
    return C.tbm.createCylinderOrCone(P(p0), r_mm * MM, P(p1), r_mm * MM)


def add_temp_bodies(comp, bodies, names):
    """Add temporary BRep bodies to a component inside one base feature."""
    out = []
    bf = comp.features.baseFeatures.add()
    bf.startEdit()
    try:
        for b, n in zip(bodies, names):
            nb = comp.bRepBodies.add(b, bf)
            nb.name = n
            C.created[n] = nb
            out.append(nb)
    finally:
        bf.finishEdit()
    return out


def tube_body(tubes, name, union=True):
    """Solid cylinders + node spheres for a list of tubes -> temp BRep body(ies)."""
    solids, nodes = [], {}
    for tname, group, a, b, r in tubes:
        solids.append(temp_cylinder(a, b, r))
        for p in (a, b):
            key = tuple(round(c, 1) for c in p)
            nodes[key] = max(nodes.get(key, 0.0), r)
    for key, r in nodes.items():
        solids.append(C.tbm.createSphere(P(key), r * 1.02 * MM))
    if not union:
        return solids
    target = solids[0]
    leftovers = []
    for s in solids[1:]:
        try:
            if not C.tbm.booleanOperation(target, s, adsk.fusion.BooleanTypes.UnionBooleanType):
                leftovers.append(s)
        except Exception:
            leftovers.append(s)
    if leftovers:
        log("%s: %d pieces did not union, kept separate" % (name, len(leftovers)))
    return [target] + leftovers


def planar_face(body, score):
    best, best_s = None, None
    for f in body.faces:
        try:
            if f.geometry.surfaceType != adsk.core.SurfaceTypes.PlaneSurfaceType:
                continue
        except Exception:
            continue
        s = score(f.centroid)
        if best is None or s > best_s:
            best, best_s = f, s
    return best


def shell_body(comp, body, open_face, thickness_mm):
    col = adsk.core.ObjectCollection.create()
    col.add(open_face)
    si = comp.features.shellFeatures.createInput(col, False)
    si.insideThickness = real(thickness_mm)
    comp.features.shellFeatures.add(si)


def cut_with_box(comp, targets, box_mm):
    """Cut a design-frame box (x0,x1,y0,y1,z0,z1 mm) from each target body."""
    tool = add_temp_bodies(comp, [temp_box(*box_mm)], ["_cut_tool"])[0]
    for i, tgt in enumerate(targets):
        tools = adsk.core.ObjectCollection.create()
        tools.add(tool)
        ci = comp.features.combineFeatures.createInput(tgt, tools)
        ci.operation = adsk.fusion.FeatureOperations.CutFeatureOperation
        ci.isKeepToolBodies = i < len(targets) - 1
        comp.features.combineFeatures.add(ci)
    C.created.pop("_cut_tool", None)


def loft_solid(comp, section_points, name):
    li = comp.features.loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    for i, (x, pts) in enumerate(section_points):
        pl = offset_plane(comp, comp.yZConstructionPlane, x, "%s_sec%d" % (name, i))
        sk = comp.sketches.add(pl)
        sk.name = "%s_sec%d" % (name, i)
        add_closed_spline(sk, pts)
        if sk.profiles.count != 1:
            log("%s section %d has %d profiles (expected 1)" % (name, i, sk.profiles.count))
        li.loftSections.add(sk.profiles.item(0))
    li.isSolid = True
    f = comp.features.loftFeatures.add(li)
    b = f.bodies.item(0)
    b.name = name
    C.created[name] = b
    return b


def extrude_profile(comp, sketch, distance_mm, name, operation=None, symmetric=True, participants=None):
    op = operation or adsk.fusion.FeatureOperations.NewBodyFeatureOperation
    prof = sketch.profiles.item(0)
    ei = comp.features.extrudeFeatures.createInput(prof, op)
    if symmetric:
        ei.setSymmetricExtent(real(distance_mm), True)
    else:
        ei.setDistanceExtent(False, real(distance_mm))
    if participants:
        ei.participantBodies = participants
    f = comp.features.extrudeFeatures.add(ei)
    if f.bodies.count:
        b = f.bodies.item(0)
        if op == adsk.fusion.FeatureOperations.NewBodyFeatureOperation:
            b.name = name
            C.created[name] = b
        return b
    return None


def stage(fn):
    """Run a build stage, log failures, keep going."""
    def wrapper(*a, **kw):
        name = fn.__name__
        log("stage %s ..." % name)
        try:
            r = fn(*a, **kw)
            log("stage %s ok" % name)
            return r
        except Exception:
            tb = traceback.format_exc()
            C.failures.append((name, tb))
            log("stage %s FAILED\n%s" % (name, tb))
            return None
    return wrapper


# ---------------------------------------------------------------------------
# Stages
# ---------------------------------------------------------------------------
@stage
def stage_measure_chassis():
    design = C.design
    bb_min, bb_max = [1e9] * 3, [-1e9] * 3
    count = 0

    def take(body):
        nonlocal count
        try:
            if not body.isVisible:
                return
            bb = body.boundingBox
        except Exception:
            return
        lo, hi = bb.minPoint, bb.maxPoint
        for i, (a, b) in enumerate(((lo.x, hi.x), (lo.y, hi.y), (lo.z, hi.z))):
            bb_min[i] = min(bb_min[i], a)
            bb_max[i] = max(bb_max[i], b)
        count += 1

    root = design.rootComponent
    for b in root.bRepBodies:
        take(b)
    for occ in root.allOccurrences:
        if occ.component.name.startswith(COMPONENT_NAME) or (occ.isVisible is False):
            continue
        for b in occ.bRepBodies:      # proxies -> world coordinates
            take(b)

    if CONFIG["chassis_bbox_mm"]:
        lo, hi = CONFIG["chassis_bbox_mm"]
        bb_min = [v * MM for v in lo]
        bb_max = [v * MM for v in hi]
        log("chassis bbox taken from CONFIG")
    elif count == 0:
        log("WARNING: no visible solid bodies found - using default spine 3200x600x550 mm at origin")
        bb_min, bb_max = [-160.0, -30.0, 0.0], [160.0, 30.0, 55.0]
        if (CONFIG["up_axis"] or "Y") == "Y":
            bb_min, bb_max = [-160.0, 0.0, -30.0], [160.0, 55.0, 30.0]
    else:
        log("chassis bbox from %d bodies: min=%s max=%s (cm)" % (count, [round(v, 2) for v in bb_min], [round(v, 2) for v in bb_max]))

    up = CONFIG["up_axis"]
    if up is None:
        try:
            pref = C.app.preferences.generalPreferences.defaultModelingOrientation
            up = "Z" if pref == adsk.core.DefaultModelingOrientations.ZUpModelingOrientation else "Y"
        except Exception:
            up = "Y"
    gc_cm = CONFIG["ground_clearance_mm"] * MM
    origin, fwd, left, upv, L, W, H = compute_placement(bb_min, bb_max, up, CONFIG["forward_sign"], gc_cm)
    C.placement = dict(origin=origin, fwd=fwd, left=left, up=upv, up_axis=up)
    log("placement: up=%s fwd=%s left=%s origin(cm)=%s  spine LxWxH mm = %.0f x %.0f x %.0f"
        % (up, fwd, left, [round(v, 2) for v in origin], L / MM, W / MM, H / MM))

    ov = dict(CONFIG["geometry_overrides"])
    ov.update(spine_length=L / MM, spine_width=W / MM, spine_height=H / MM,
              ground_clearance=CONFIG["ground_clearance_mm"])
    C.body = buggy_geometry.BuggyBody(**ov)
    log("geometry: " + json.dumps(C.body.summary(), default=float))


@stage
def stage_create_component():
    if CONFIG["build_in_new_document"]:
        doc = C.app.documents.add(adsk.core.DocumentTypes.FusionDesignDocumentType)
        C.design = adsk.fusion.Design.cast(C.app.activeProduct)
        log("building in new document %s" % doc.name)
    design = C.design
    pl = C.placement
    m = adsk.core.Matrix3D.create()
    m.setWithCoordinateSystem(adsk.core.Point3D.create(*pl["origin"]), Vec(pl["fwd"]), Vec(pl["left"]), Vec(pl["up"]))
    name = COMPONENT_NAME
    existing = [o.component.name for o in design.rootComponent.occurrences]
    k = 2
    while name in existing:
        name = "%s (%d)" % (COMPONENT_NAME, k)
        k += 1
    occ = design.rootComponent.occurrences.addNewComponent(m)
    occ.component.name = name
    C.root = occ.component
    C.tbm = adsk.fusion.TemporaryBRepManager.get()
    # user parameters as documentation of the driving values
    b = C.body
    for pname, val, unit, comment in (
        ("buggy_wheelbase", b.wheelbase, "mm", "front to rear axle"),
        ("buggy_track", 2 * b.half_track, "mm", "wheel centre to wheel centre"),
        ("buggy_ground_clearance", b.floor_z - b.p["skin_thickness"], "mm", "belly pan to ground"),
        ("buggy_sill_height", b.sill_z, "mm", "tub top edge above ground"),
        ("buggy_roof_height", b.roof_z, "mm", "roof rail centreline above ground"),
        ("buggy_skin_thickness", b.p["skin_thickness"], "mm", "CFRP skin"),
        ("buggy_tube_od_hoop", 2 * b.p["r_hoop"], "mm", "4130 main hoop tube"),
    ):
        try:
            design.userParameters.add(pname, adsk.core.ValueInput.createByString("%.1f mm" % val), unit, comment)
        except Exception:
            pass


@stage
def stage_cage():
    comp = sub_component("Cage")
    tubes = C.body.tubes
    bodies = tube_body(tubes, "Cage", union=True)
    add_temp_bodies(comp, bodies, ["Cage"] + ["Cage_part%d" % i for i in range(1, len(bodies))])


@stage
def stage_lattices():
    comp = sub_component("Generative Lattice")
    for group, name in (("lattice", "SideRibs"), ("canopy", "Canopy"), ("grille", "Grille")):
        tubes = [t for t in C.body.lattice_tubes if t[1] == group]
        bodies = tube_body(tubes, name, union=CONFIG["union_lattices"])
        add_temp_bodies(comp, bodies, [name] + ["%s_part%d" % (name, i) for i in range(1, len(bodies))])


@stage
def stage_tub():
    comp = sub_component("Skins")
    b = C.body
    z0, z1 = b.tub_z
    li = comp.features.loftFeatures.createInput(adsk.fusion.FeatureOperations.NewBodyFeatureOperation)
    for half, z, tag in ((b.tub_outline_half, z0, "Floor"), (b.tub_sill_half, z1, "Sill")):
        pl = offset_plane(comp, comp.xYConstructionPlane, z, "Tub" + tag)
        sk = comp.sketches.add(pl)
        sk.name = "Tub" + tag
        poly = [(x, hw, z) for (x, hw) in half] + [(x, -hw, z) for (x, hw) in reversed(half)]
        add_polyline(sk, poly)
        li.loftSections.add(sk.profiles.item(0))
    li.isSolid = True
    tub = comp.features.loftFeatures.add(li).bodies.item(0)
    tub.name = "Tub"
    C.created["Tub"] = tub
    shell_body(comp, tub, planar_face(tub, lambda c: c.z), b.p["skin_thickness"])
    dn = b.door_notch
    for s in (1, -1):
        y0, y1 = (dn["y_min"], 2500.0) if s > 0 else (-2500.0, -dn["y_min"])
        cut_with_box(comp, [tub], (dn["x0"], dn["x1"], y0, y1, dn["z0"], dn["z1"]))


@stage
def stage_hood_deck():
    comp = sub_component("Skins")
    b = C.body
    hood = loft_solid(comp, b.section_points["Hood"], "Hood")
    shell_body(comp, hood, planar_face(hood, lambda c: -c.x), b.p["skin_thickness"])
    deck = loft_solid(comp, b.section_points["Deck"], "Deck")
    shell_body(comp, deck, planar_face(deck, lambda c: c.x), b.p["skin_thickness"])
    cx0, cx1, cy0, cy1 = b.canopy_opening
    cut_with_box(comp, [deck], (cx0, cx1, cy0, cy1, b.sill_z - 200, b.sill_z + 400))


@stage
def stage_spine_channel():
    comp = sub_component("Skins")
    sc = C.body.spine_channel
    targets = [C.created[k] for k in ("Tub", "Hood", "Deck") if k in C.created]
    if targets:
        cut_with_box(comp, targets, (sc["x0"], sc["x1"], -sc["hy"], sc["hy"], sc["z0"], sc["z1"]))


@stage
def stage_fenders():
    comp = sub_component("Skins")
    for f in C.body.fenders:
        c = f["centre"]
        a0, a1 = math.radians(f["a0"]), math.radians(f["a1"])
        am = 0.5 * (a0 + a1)

        def pt(r, a):
            return (c[0] + r * math.sin(a), c[1], c[2] + r * math.cos(a))

        pl = offset_plane(comp, comp.xZConstructionPlane, c[1], f["name"] + "_plane")
        sk = comp.sketches.add(pl)
        sk.name = f["name"]
        p_in0, p_inm, p_in1 = sketch_points(sk, [pt(f["r_in"], a0), pt(f["r_in"], am), pt(f["r_in"], a1)])
        p_out0, p_outm, p_out1 = sketch_points(sk, [pt(f["r_out"], a0), pt(f["r_out"], am), pt(f["r_out"], a1)])
        sk.sketchCurves.sketchArcs.addByThreePoints(p_in0, p_inm, p_in1)
        sk.sketchCurves.sketchLines.addByTwoPoints(p_in1, p_out1)
        sk.sketchCurves.sketchArcs.addByThreePoints(p_out1, p_outm, p_out0)
        sk.sketchCurves.sketchLines.addByTwoPoints(p_out0, p_in0)
        extrude_profile(comp, sk, f["width"], f["name"])


@stage
def stage_seats_fittings():
    comp = sub_component("Fittings")
    b = C.body
    for s in b.seats:
        pl = offset_plane(comp, comp.xZConstructionPlane, s["y"], s["name"] + "_plane")
        sk = comp.sketches.add(pl)
        sk.name = s["name"] + "_cushion"
        add_polyline(sk, [(x, s["y"], z) for (x, z) in s["cushion"]])
        cushion = extrude_profile(comp, sk, s["width"], s["name"])
        sk2 = comp.sketches.add(pl)
        sk2.name = s["name"] + "_back"
        add_polyline(sk2, [(x, s["y"], z) for (x, z) in s["back"]])
        extrude_profile(comp, sk2, s["width"], s["name"] + "Back",
                        operation=adsk.fusion.FeatureOperations.JoinFeatureOperation, participants=[cushion])
    sw = b.steering_wheel
    torus = C.tbm.createTorus(P(sw["centre"]), Vec(sw["axis"]), sw["major_r"] * MM, sw["minor_r"] * MM)
    lb = b.light_bar
    c, sz = lb["centre"], lb["size"]
    box = temp_box(c[0] - sz[0] / 2, c[0] + sz[0] / 2, c[1] - sz[1] / 2, c[1] + sz[1] / 2, c[2] - sz[2] / 2, c[2] + sz[2] / 2)
    add_temp_bodies(comp, [torus, box], ["SteeringWheel", "LightBar"])


@stage
def stage_reference_wheels():
    comp = sub_component("Reference Wheels")
    bodies, names = [], []
    for w in C.body.wheels:
        c, ax = w["centre"], w["axis"]
        for r, wd, suffix in ((w["tyre_r"], w["tyre_w"], ""), (w["rim_r"], w["rim_w"], "Rim")):
            p0 = (c[0], c[1] - ax[1] * 0.5 * wd, c[2])
            p1 = (c[0], c[1] + ax[1] * 0.5 * wd, c[2])
            bodies.append(temp_cylinder(p0, p1, r))
            names.append(w["name"] + suffix)
    add_temp_bodies(comp, bodies, names)


@stage
def stage_generative_design_setup():
    """Obstacle + preserve bodies for a Fusion Generative Design study."""
    comp = sub_component("GD Setup")
    b = C.body
    bodies, names = [], []
    for o in b.gd_obstacles:
        if "box" in o:
            bodies.append(temp_box(*o["box"]))
        else:
            cy = o["cylinder"]
            c = cy["centre"]
            p0 = (c[0], c[1] - 0.5 * cy["width"], c[2])
            p1 = (c[0], c[1] + 0.5 * cy["width"], c[2])
            bodies.append(temp_cylinder(p0, p1, cy["r"] + cy["z_travel"]))
        names.append(o["name"])
    for pr in b.gd_preserves:
        bodies.append(C.tbm.createSphere(P(pr["centre"]), pr["r"] * MM))
        names.append(pr["name"])
    added = add_temp_bodies(comp, bodies, names)
    for nb in added:
        nb.isVisible = False


@stage
def stage_finish():
    design = C.design
    try:
        if design.snapshots.hasPendingSnapshot:
            design.snapshots.add()
    except Exception:
        pass
    try:
        C.app.activeViewport.fit()
    except Exception:
        pass
    report = dict(config={k: v for k, v in CONFIG.items()}, placement=C.placement,
                  summary=C.body.summary(), volumes_mm3={}, bbox_mm={}, failures=[f[0] for f in C.failures])
    for name, body in C.created.items():
        try:
            report["volumes_mm3"][name] = round(body.volume / (MM ** 3), 1)
            bb = body.boundingBox
            report["bbox_mm"][name] = [round(v / MM, 1) for v in (bb.minPoint.x, bb.minPoint.y, bb.minPoint.z,
                                                                    bb.maxPoint.x, bb.maxPoint.y, bb.maxPoint.z)]
        except Exception:
            report["volumes_mm3"][name] = "n/a"
    skins = [k for k in ("Tub", "Hood", "Deck", "FenderFL", "FenderFR", "FenderRL", "FenderRR")
             if isinstance(report["volumes_mm3"].get(k), float)]
    skin_mass = sum(report["volumes_mm3"][k] for k in skins) * buggy_geometry.CFRP_DENSITY
    report["summary"]["skin_mass_kg"] = skin_mass
    report["summary"]["body_mass_estimate_kg"] = skin_mass + report["summary"]["tube_mass_total_kg"]
    with open(os.path.join(HERE, "fusion_report.json"), "w") as fh:
        json.dump(report, fh, indent=2, default=float)
    exp_dir = os.path.join(HERE, "exports")
    os.makedirs(exp_dir, exist_ok=True)
    em = design.exportManager
    if CONFIG["export_step"]:
        em.execute(em.createSTEPExportOptions(os.path.join(exp_dir, "buggy_body_fusion.step"), C.root))
    if CONFIG["export_f3d"]:
        em.execute(em.createFusionArchiveExportOptions(os.path.join(exp_dir, "buggy_body_fusion.f3d")))
    return report


def run(context):
    C.app = adsk.core.Application.get()
    C.ui = C.app.userInterface
    C.t0 = time.time()
    C.log_lines, C.failures, C.created, C.comps = [], [], {}, {}
    try:
        try:
            os.remove(os.path.join(HERE, "fusion_build.log"))
        except OSError:
            pass
        C.design = adsk.fusion.Design.cast(C.app.activeProduct)
        if not C.design:
            C.ui.messageBox("Open the chassis design (cp-proto-flattop) and run again.")
            return
        log("active document: %s" % C.app.activeDocument.name)
        stage_measure_chassis()
        if C.body is None:
            C.ui.messageBox("Could not derive the body - see fusion_build.log")
            return
        stage_create_component()
        if C.root is None:
            C.ui.messageBox("Could not create the component - see fusion_build.log")
            return
        stage_cage()
        stage_lattices()
        stage_tub()
        stage_hood_deck()
        stage_spine_channel()
        stage_fenders()
        stage_seats_fittings()
        stage_reference_wheels()
        stage_generative_design_setup()
        report = stage_finish()
        msg = ["Flattop Buggy body built in %.0f s" % (time.time() - C.t0),
               "bodies: %d" % len(C.created)]
        if report:
            s = report["summary"]
            msg.append("wheelbase %.0f mm, track %.0f mm, roof %.0f mm" % (s["wheelbase_mm"], s["track_mm"], s["roof_height_mm"]))
            msg.append("mass estimate: tubes %.0f kg + skins %.0f kg = %.0f kg"
                       % (s["tube_mass_total_kg"], s["skin_mass_kg"], s["body_mass_estimate_kg"]))
        if C.failures:
            msg.append("")
            msg.append("%d stage(s) failed: %s  (details in fusion_build.log)" % (len(C.failures), ", ".join(f[0] for f in C.failures)))
        C.ui.messageBox("\n".join(msg), "Buggy Body")
    except Exception:
        tb = traceback.format_exc()
        log("FATAL\n" + tb)
        if C.ui:
            C.ui.messageBox("Buggy body script failed:\n" + tb)


def stop(context):
    pass
