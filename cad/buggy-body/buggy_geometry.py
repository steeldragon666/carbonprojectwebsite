"""Parametric geometry for the two-seat off-road buggy body ("Flattop Buggy").

Pure Python (math + random only) so it imports unchanged inside Autodesk
Fusion's embedded interpreter and inside a cadquery build in the cloud.

Design frame (all values in millimetres):
    +X forward (nose), +Y left, +Z up.  Z = 0 is the ground plane.
    Origin: centre of the wheelbase on the vehicle centreline.
The chassis spine (batteries, diesel range extender, motors) is treated as a
sealed box L x W x H sitting at Z = ground_clearance, centred on the origin.
Everything else is derived from that box, the wheel package and the occupant.

Structural intent (generative-design informed):
  * Primary load paths are the roll cage: two hoops (A and B), roof rails,
    rear stays to the deck, front nudge structure to the bumper. Every hoop
    plane carries a diagonal so each face of the safety cell is triangulated.
  * Secondary structure is an organic strut lattice (side ribs, rear canopy,
    front grille) generated from seeded nodes joined to their nearest
    neighbours - the same "material only where load flows" logic Fusion's
    Generative Design produces, in a form that stays fully parametric.
  * Skins are thin shells (4 mm CFRP) hung between the tubes; they carry
    aero and splash load, not crash load.
"""
import math
import random

# ---------------------------------------------------------------------------
# Parameters
# ---------------------------------------------------------------------------
DEFAULT_PARAMS = dict(
    # chassis spine (overridden by the Fusion script from the live document)
    spine_length=3200.0,
    spine_width=600.0,
    spine_height=550.0,
    ground_clearance=400.0,   # ground -> spine belly
    spine_clearance=30.0,     # air gap body -> spine
    # wheel package (35 x 12.5 tyre on 17" wheel)
    tyre_od=890.0,
    tyre_width=320.0,
    rim_diameter=432.0,
    track=1900.0,             # wheel centre to wheel centre
    wheelbase=None,           # None -> max(0.9 * spine_length, 2700)
    wheel_travel=150.0,       # +/- for the generative-design obstacle zones
    # occupant
    driver_side="right",      # Australian market: RHD
    seat_pitch=1200.0,        # seat centre to seat centre (across)
    # skins
    skin_thickness=4.0,
    # tubes (radius, mm)
    r_hoop=22.25,             # 44.5 mm OD (1.75") 4130
    r_brace=19.0,             # 38 mm OD
    r_diag=16.0,              # 32 mm OD
    r_stay=12.0,
    r_lattice=7.0,
    r_canopy=9.0,
    r_grille=8.0,
    lattice_seed=7,
    # aesthetic
    superellipse_n=3.4,       # squareness of the lofted sections
    tub_flare=45.0,           # outward lean of the tub flanks, floor -> sill (mm)
)

# Material data for the analytical mass estimate
STEEL_4130_DENSITY = 7.85e-6   # kg / mm^3
CFRP_DENSITY = 1.55e-6         # kg / mm^3
TUBE_WALL = {"hoop": 2.4, "brace": 2.0, "diag": 1.6, "stay": 1.2,
             "lattice": 1.0, "canopy": 1.0, "grille": 1.0}


def _v(a, b):
    return (b[0] - a[0], b[1] - a[1], b[2] - a[2])


def _dist(a, b):
    d = _v(a, b)
    return math.sqrt(d[0] ** 2 + d[1] ** 2 + d[2] ** 2)


def superellipse(hw, zb, zt, n, count=28, corner_pull=1.0):
    """Closed point loop (y, z) of a superellipse spanning +/-hw, zb..zt.

    corner_pull < 1 flattens the top (visor look) by scaling the upper half's
    exponent.  Returned as a list of (y, z) starting at the top centre going
    anti-clockwise (left first), no duplicated end point."""
    cy, cz = 0.0, 0.5 * (zb + zt)
    a, b = hw, 0.5 * (zt - zb)
    pts = []
    for i in range(count):
        t = 2.0 * math.pi * i / count + math.pi / 2.0
        c, s = math.cos(t), math.sin(t)
        nn = n * (corner_pull if s > 0 else 1.0)
        y = cy + a * math.copysign(abs(c) ** (2.0 / nn), c)
        z = cz + b * math.copysign(abs(s) ** (2.0 / nn), s)
        pts.append((y, z))
    return pts


class BuggyBody:
    """All derived geometry. Construct with a dict of parameter overrides."""

    def __init__(self, **overrides):
        p = dict(DEFAULT_PARAMS)
        p.update({k: v for k, v in overrides.items() if v is not None})
        self.p = p
        L, W, H = p["spine_length"], p["spine_width"], p["spine_height"]
        self.L, self.W, self.H = L, W, H
        self.gc = p["ground_clearance"]
        self.tyre_r = 0.5 * p["tyre_od"]
        self.wheelbase = p["wheelbase"] or max(0.9 * L, 2700.0)
        self.half_track = 0.5 * p["track"]
        self.wheel_inner_y = self.half_track - 0.5 * p["tyre_width"]
        # scale factor used to stretch the cabin fore/aft with the spine
        self.k = self.wheelbase / 2880.0
        self.floor_z = self.gc - 10.0          # top of belly pan
        self.sill_z = self.gc + 600.0          # top edge of the tub
        self.roof_z = self.sill_z + 680.0      # roof rails
        self.seat_y = 0.5 * p["seat_pitch"]
        self.driver_sign = -1.0 if p["driver_side"] == "right" else 1.0
        self._build()

    # -- helpers ------------------------------------------------------------
    def kx(self, x):
        """Scale a nominal (2880 mm wheelbase) x-station to this wheelbase."""
        return x * self.k

    def tub_wall_y(self, z):
        """Half-width of the flat flank (x between the tub corners) at height z."""
        z0, z1 = self.floor_z - self.p["skin_thickness"], self.sill_z
        f = max(0.0, min(1.0, (z - z0) / (z1 - z0)))
        return 920.0 + self.p["tub_flare"] * f

    def _build(self):
        self.nodes = {}
        self.tubes = []       # (name, group, p1, p2, radius)
        self._frame()
        self._lattices()
        self._panels()
        self._fenders()
        self._seats_and_fittings()
        self._wheels()
        self._generative_design_setup()

    # -- primary structure --------------------------------------------------
    def _node(self, name, x, y, z):
        self.nodes[name] = (float(x), float(y), float(z))
        return self.nodes[name]

    def _tube(self, name, group, a, b, r=None):
        r = r or self.p["r_" + group]
        self.tubes.append((name, group, a, b, float(r)))

    def _frame(self):
        kx, sz, rz = self.kx, self.sill_z, self.roof_z
        gc = self.gc
        floor_tube_z = gc + 20.0
        for s, tag in ((1.0, "L"), (-1.0, "R")):
            self._node("A1" + tag, kx(850), 900 * s, sz)
            self._node("A2" + tag, kx(250), 760 * s, rz - 20)
            self._node("B1" + tag, kx(-450), 900 * s, sz)
            self._node("B2" + tag, kx(-450), 820 * s, rz)
            self._node("R1" + tag, kx(-1500), 620 * s, sz + 10)
            self._node("F1" + tag, kx(2000), 430 * s, gc + 240)
            self._node("F0" + tag, kx(2050), 340 * s, gc + 30)
            self._node("FT" + tag, kx(1300), 380 * s, floor_tube_z)
            self._node("RB" + tag, kx(-1950), 480 * s, gc + 240)
            self._node("RB0" + tag, kx(-1950), 480 * s, gc + 30)
            self._node("R0" + tag, kx(-1500), 620 * s, floor_tube_z)
            self._node("RT" + tag, kx(-700), 900 * s, floor_tube_z)
            self._node("D1" + tag, kx(600), 820 * s, sz + 300)
            self._node("D2" + tag, kx(-450), 860 * s, sz + 300)
        n = self.nodes
        for tag in ("L", "R"):
            self._tube("Apillar" + tag, "hoop", n["A1" + tag], n["A2" + tag])
            self._tube("RoofRail" + tag, "hoop", n["A2" + tag], n["B2" + tag])
            self._tube("Bupright" + tag, "hoop", n["B1" + tag], n["B2" + tag])
            self._tube("RearStay" + tag, "hoop", n["B2" + tag], n["R1" + tag])
            self._tube("Sill" + tag, "brace", n["A1" + tag], n["B1" + tag])
            self._tube("DoorBar" + tag, "diag", n["D1" + tag], n["D2" + tag])
            self._tube("DoorBarF" + tag, "diag", n["A1" + tag], n["D1" + tag])
            self._tube("DoorBarR" + tag, "diag", n["D2" + tag], n["B1" + tag])
            self._tube("FrontDown" + tag, "brace", n["A1" + tag], n["F1" + tag])
            self._tube("FrontLower" + tag, "diag", n["F1" + tag], n["F0" + tag])
            self._tube("FrontFloor" + tag, "diag", n["F0" + tag], n["FT" + tag])
            self._tube("RearDown" + tag, "brace", n["R1" + tag], n["RB" + tag])
            self._tube("RearLower" + tag, "diag", n["RB" + tag], n["RB0" + tag])
            self._tube("RearFloor" + tag, "diag", n["RB0" + tag], n["R0" + tag])
            self._tube("DeckFloor" + tag, "diag", n["R0" + tag], n["RT" + tag])
            self._tube("R1down" + tag, "diag", n["R1" + tag], n["R0" + tag])
            self._tube("FloorSide" + tag, "diag", n["RT" + tag], n["FT" + tag])
        # cross members
        self._tube("DashBar", "brace", n["A1L"], n["A1R"])
        self._tube("RoofFront", "hoop", n["A2L"], n["A2R"])
        self._tube("HoopTop", "hoop", n["B2L"], n["B2R"])
        self._tube("RearCross", "brace", n["R1L"], n["R1R"])
        self._tube("FrontBumper", "brace", n["F1L"], n["F1R"])
        self._tube("FrontBumperLo", "diag", n["F0L"], n["F0R"])
        self._tube("RearBumper", "brace", n["RBL"], n["RBR"])
        self._tube("RearBumperLo", "diag", n["RB0L"], n["RB0R"])
        # diagonals - every plane of the safety cell triangulated
        self._tube("RoofX1", "diag", n["A2L"], n["B2R"])
        self._tube("RoofX2", "diag", n["A2R"], n["B2L"])
        self._tube("HoopDiag", "diag", n["B2L"], n["B1R"])
        self._tube("RearX1", "diag", n["B2L"], n["R1R"])
        self._tube("RearX2", "diag", n["B2R"], n["R1L"])
        self._tube("FrontX", "diag", n["F1L"], n["F0R"])

    # -- generative lattices --------------------------------------------------
    def _lattice(self, name, group, seeds, boundary, max_len, k=3, rng=None):
        """Join each seed node to its k nearest neighbours (within max_len),
        then tie the outer nodes to the supplied boundary anchor points."""
        pts = list(seeds)
        edges = set()
        for i, a in enumerate(pts):
            near = sorted(((_dist(a, b), j) for j, b in enumerate(pts) if j != i))
            added = 0
            for d, j in near:
                if d > max_len:
                    break
                e = (min(i, j), max(i, j))
                if e not in edges:
                    edges.add(e)
                    added += 1
                if added >= k:
                    break
        out = []
        for idx, (i, j) in enumerate(sorted(edges)):
            out.append(("%s_%03d" % (name, idx), group, pts[i], pts[j], self.p["r_" + group]))
        for bi, bp in enumerate(boundary):
            near = sorted(((_dist(bp, a), j) for j, a in enumerate(pts)))[:2]
            for d, j in near:
                if d <= max_len * 1.4:
                    out.append(("%s_b%02d_%d" % (name, bi, j), group, bp, pts[j], self.p["r_" + group]))
        return out

    @staticmethod
    def _jitter_grid(rng, x0, x1, y0, y1, dx, dy, jitter):
        pts = []
        nx = max(2, int(round((x1 - x0) / dx)) + 1)
        ny = max(2, int(round((y1 - y0) / dy)) + 1)
        for i in range(nx):
            for j in range(ny):
                u = x0 + (x1 - x0) * i / (nx - 1)
                v = y0 + (y1 - y0) * j / (ny - 1)
                edge = i in (0, nx - 1) or j in (0, ny - 1)
                jf = 0.0 if edge else jitter
                pts.append((u + rng.uniform(-jf, jf) * dx, v + rng.uniform(-jf, jf) * dy))
        return pts

    def _lattices(self):
        rng = random.Random(self.p["lattice_seed"])
        kx, gc = self.kx, self.gc
        self.lattice_tubes = []
        # 1. side ribs: exoskeleton web on the tub flanks below the door notch
        r_l = self.p["r_lattice"]
        for s in (1.0, -1.0):
            g = self._jitter_grid(rng, kx(-620), kx(620), gc + 40, gc + 330, 190, 140, 0.35)
            seeds = [(u, (self.tub_wall_y(v) + r_l) * s, v) for u, v in g]
            anchors = [self.nodes["RT" + ("L" if s > 0 else "R")], self.nodes["FT" + ("L" if s > 0 else "R")]]
            self.lattice_tubes += self._lattice("SideRib" + ("L" if s > 0 else "R"), "lattice", seeds,
                                                anchors, max_len=300)
        # 2. rear canopy: domed strut lattice over the range-extender bay vent
        x0, x1 = kx(-1520), kx(-780)
        y0, y1 = -600.0, 600.0
        base_z = gc + 600.0
        g = self._jitter_grid(rng, x0, x1, y0, y1, 185, 200, 0.3)
        seeds = []
        for u, v in g:
            fx = 1.0 - ((u - 0.5 * (x0 + x1)) / (0.5 * (x1 - x0))) ** 2
            fy = 1.0 - (v / (0.5 * (y1 - y0))) ** 2
            seeds.append((u, v, base_z + 230.0 * max(0.0, fx) ** 0.7 * max(0.0, fy) ** 0.7))
        self.canopy_opening = (x0 + 60, x1 - 60, y0 + 60, y1 - 60)
        self.lattice_tubes += self._lattice("Canopy", "canopy", seeds, [], max_len=330, k=4)
        # 3. front grille: organic web between the bumper tubes
        gx = kx(1975)
        g = self._jitter_grid(rng, -360, 360, gc + 60, gc + 210, 150, 110, 0.35)
        seeds = [(gx, u, v) for u, v in g]
        anchors = [self.nodes[n] for n in ("F1L", "F1R", "F0L", "F0R")]
        self.lattice_tubes += self._lattice("Grille", "grille", seeds, anchors, max_len=260)

    # -- skins ----------------------------------------------------------------
    def _panels(self):
        kx, gc, n = self.kx, self.gc, self.p["superellipse_n"]
        fz, sz = self.floor_z, self.sill_z
        # tub floor plan (x, half-width) front to rear, mirrored for the closed polygon
        self.tub_outline_half = [(kx(1300), 400), (kx(1100), 560), (kx(800), 920), (kx(-700), 920)]
        # sill outline is flared outward so the flanks lean out (tumblehome in reverse)
        fl = self.p["tub_flare"]
        self.tub_sill_half = [(x, hw + fl * (hw / 920.0)) for (x, hw) in self.tub_outline_half]
        self.tub_z = (fz - self.p["skin_thickness"], sz)
        self.door_notch = dict(x0=kx(-300), x1=kx(650), y_min=700.0, z0=sz - 240.0, z1=sz + 30.0)
        # lofted sections: (x, half-width, z_bottom, z_top)
        self.hood_sections = [
            (kx(1300), 400, fz, sz),
            (kx(1650), 350, fz, sz - 100),
            (kx(1950), 290, fz + 10, gc + 360),
            (kx(2150), 200, fz + 40, gc + 220),
        ]
        self.deck_sections = [
            (kx(-700), 920, fz, sz),
            (kx(-1050), 760, fz, sz + 60),
            (kx(-1450), 700, fz + 10, sz + 20),
            (kx(-1800), 520, fz + 40, sz - 140),
            (kx(-1950), 380, fz + 70, sz - 280),
        ]
        self.section_points = {}
        for name, secs in (("Hood", self.hood_sections), ("Deck", self.deck_sections)):
            self.section_points[name] = []
            for (x, hw, zb, zt) in secs:
                loop = superellipse(hw, zb, zt, n, count=28, corner_pull=0.8)
                self.section_points[name].append((x, [(x, y, z) for (y, z) in loop]))
        # spine clearance channel cut through every skin
        c = self.p["spine_clearance"]
        self.spine_channel = dict(x0=-0.5 * self.L - c, x1=0.5 * self.L + c,
                                  hy=0.5 * self.W + c, z0=gc - 1.0, z1=gc + self.H + c)

    # -- wheels / fenders -----------------------------------------------------
    def _fenders(self):
        self.wheel_centres = {}
        for s, tag in ((1.0, "L"), (-1.0, "R")):
            self.wheel_centres["F" + tag] = (0.5 * self.wheelbase, self.half_track * s, self.tyre_r)
            self.wheel_centres["R" + tag] = (-0.5 * self.wheelbase, self.half_track * s, self.tyre_r)
        self.fenders = []
        r_in = self.tyre_r + 70.0
        r_out = r_in + 6.0
        width = self.p["tyre_width"] + 90.0
        for key, c in self.wheel_centres.items():
            a0, a1 = (-55.0, 45.0) if key[0] == "F" else (-50.0, 58.0)
            self.fenders.append(dict(name="Fender" + key, centre=c, r_in=r_in, r_out=r_out,
                                     width=width, a0=a0, a1=a1))
        # fender stays: tube from frame node to a point on the fender
        n = self.nodes
        def on_fender(c, ang):
            a = math.radians(ang)
            return (c[0] + r_in * math.sin(a), c[1], c[2] + r_in * math.cos(a))
        for tag in ("L", "R"):
            cf, cr = self.wheel_centres["F" + tag], self.wheel_centres["R" + tag]
            self._tube("FStayFront" + tag, "stay", n["F1" + tag], on_fender(cf, 35))
            self._tube("FStayRear" + tag, "stay", n["A1" + tag], on_fender(cf, -40))
            self._tube("RStayFront" + tag, "stay", n["R1" + tag], on_fender(cr, 0))
            self._tube("RStayRear" + tag, "stay", n["RB" + tag], on_fender(cr, -40))

    # -- occupant items ---------------------------------------------------------
    def _seats_and_fittings(self):
        kx, gc = self.kx, self.gc
        self.seats = []
        cushion_z = gc + 180.0
        for s in (1.0, -1.0):
            y = self.seat_y * s
            self.seats.append(dict(
                name="Seat" + ("L" if s > 0 else "R"), y=y, width=500.0,
                cushion=[(kx(380), cushion_z), (kx(380), cushion_z + 90), (kx(-60), cushion_z + 110),
                         (kx(-110), cushion_z + 40), (kx(-110), cushion_z)],
                back=self._backrest(kx(-90), cushion_z + 30, 22.0, 720.0, 90.0),
            ))
        d = self.driver_sign
        self.steering_wheel = dict(centre=(kx(620), self.seat_y * d, gc + 610),
                                   axis=(-math.cos(math.radians(25)), 0.0, math.sin(math.radians(25))),
                                   major_r=170.0, minor_r=16.0)
        self.light_bar = dict(centre=(kx(250), 0.0, self.roof_z - 20 + self.p["r_hoop"] + 26), size=(60.0, 1000.0, 55.0))

    @staticmethod
    def _backrest(x0, z0, angle_deg, length, thickness):
        a = math.radians(angle_deg)
        d = (-math.sin(a), math.cos(a))
        nrm = (math.cos(a), math.sin(a))
        p0 = (x0, z0)
        p1 = (x0 + d[0] * length, z0 + d[1] * length)
        p2 = (p1[0] + nrm[0] * thickness, p1[1] + nrm[1] * thickness)
        p3 = (p0[0] + nrm[0] * thickness, p0[1] + nrm[1] * thickness)
        return [p0, p1, p2, p3]

    def _wheels(self):
        self.wheels = []
        for key, c in self.wheel_centres.items():
            s = 1.0 if c[1] > 0 else -1.0
            self.wheels.append(dict(name="Wheel" + key, centre=c, axis=(0.0, s, 0.0),
                                    tyre_r=self.tyre_r, tyre_w=self.p["tyre_width"],
                                    rim_r=0.5 * self.p["rim_diameter"], rim_w=self.p["tyre_width"] - 30))

    # -- Fusion Generative Design study inputs ---------------------------------
    def _generative_design_setup(self):
        """Obstacle bodies (space that must stay empty) and preserve bodies
        (hard points the optimiser must connect) for a Fusion GD study of the
        cage / gusset structure."""
        kx, gc, t = self.kx, self.gc, self.p["wheel_travel"]
        self.gd_obstacles = [
            dict(name="Obstacle_Spine", box=(-0.5 * self.L - 30, 0.5 * self.L + 30, -0.5 * self.W - 30,
                                             0.5 * self.W + 30, gc - 1, gc + self.H + 30)),
        ]
        for s, tag in ((1.0, "L"), (-1.0, "R")):
            y = self.seat_y * s
            self.gd_obstacles.append(dict(name="Obstacle_Occupant" + tag,
                                          box=(kx(-450), kx(900), y - 330, y + 330, gc + 100, self.roof_z - 60)))
        for key, c in self.wheel_centres.items():
            self.gd_obstacles.append(dict(name="Obstacle_" + key + "Wheel", cylinder=dict(
                centre=c, axis=(0.0, 1.0, 0.0), r=self.tyre_r + 60, width=self.p["tyre_width"] + 120,
                z_travel=t)))
        self.gd_preserves = [dict(name="Preserve_" + k, centre=self.nodes[k], r=self.p["r_hoop"] * 1.6)
                             for k in ("F1L", "F1R", "F0L", "F0R", "A1L", "A1R", "B1L", "B1R",
                                       "R1L", "R1R", "RBL", "RBR")]

    # -- reporting ------------------------------------------------------------
    def all_tubes(self):
        return self.tubes + self.lattice_tubes

    def mass_estimate(self):
        """Analytical mass: hollow 4130 tubes + CFRP skins (area x thickness)."""
        out = {}
        for name, group, a, b, r in self.all_tubes():
            wall = TUBE_WALL[group]
            area = math.pi * (r ** 2 - (r - wall) ** 2)
            out[group] = out.get(group, 0.0) + _dist(a, b) * area * STEEL_4130_DENSITY
        return out

    def summary(self):
        m = self.mass_estimate()
        tube_len = sum(_dist(a, b) for _, _, a, b, _ in self.all_tubes())
        return dict(
            wheelbase_mm=self.wheelbase, track_mm=2 * self.half_track,
            overall_length_mm=self.kx(2150) - self.kx(-1950) + 0.0,
            overall_width_mm=2 * (self.half_track + 0.5 * self.p["tyre_width"]),
            roof_height_mm=self.roof_z + self.p["r_hoop"],
            ground_clearance_mm=self.floor_z - self.p["skin_thickness"],
            n_frame_tubes=len(self.tubes), n_lattice_struts=len(self.lattice_tubes),
            tube_length_m=tube_len / 1000.0, tube_mass_kg=m,
            tube_mass_total_kg=sum(m.values()),
        )


if __name__ == "__main__":
    import json
    b = BuggyBody()
    print(json.dumps(b.summary(), indent=2))
