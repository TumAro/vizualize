"""Linear algebra & geometry pictures (stdlib only; 3D by orthographic projection, no WebGL). Each carries numeric certificates and refuses degenerate input.
  mv.py linmap a b c d              A=[[a,b],[c,d]]: grid image, SVD ellipse, eigenlines, det = area  (A V = U Σ asserted)
  mv.py basis b11 b12 b21 b22 x1 x2   coordinates of x in basis (b1, b2); P c = x asserted
  mv.py solid tetra|cube|octa|dodeca|icosa [az el]   Platonic solids: hull faces, Euler V-E+F=2, dihedral angle, hidden edges dashed
  mv.py surface "x**2-y**2" [R az el]                z=f(x,y) wireframe
  mv.py ga rotate x y deg | reflect x y line_deg | wedge a1 a2 b1 b2 | rotate3 x y z ax ay az deg    geometric algebra Cl(2)/Cl(3)
  mv.py triangle "0,0 6,0 2,4"       circumcircle, Euler line, nine-point circle (9 points verified)"""
import math, html, itertools
from base import *
from fa import view, clipline, poly_d, line_d, txt, wrap_svg
C1, C2, C3, C4 = "#3b82f6", "#f43f5e", "#22c55e", "#f59e0b"
def circ_pts(cx, cy, r, n=72): return [(cx + r*math.cos(2*math.pi*k/n), cy + r*math.sin(2*math.pi*k/n)) for k in range(n)]
def polyline(X, Y, pts, c, w=1.5, dash=""):
    return f'<polyline fill="none" stroke="{c}" stroke-width="{w}"' + (f' stroke-dasharray="{dash}"' if dash else "") + ' points="%s"/>' % " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in pts)

# ---------- 2x2 linear maps ----------
def svd2(a, b, c, d):
    p, q, r = a*a + c*c, a*b + c*d, b*b + d*d; m, h = (p + r)/2, math.hypot((p - r)/2, q)
    s1, s2 = math.sqrt(max(m + h, 0)), math.sqrt(max(m - h, 0)); th = .5*math.atan2(2*q, p - r)
    v1, v2 = (math.cos(th), math.sin(th)), (-math.sin(th), math.cos(th)); A = lambda v: (a*v[0] + b*v[1], c*v[0] + d*v[1])
    u1 = tuple(x/s1 for x in A(v1)) if s1 > 1e-12 else None; u2 = tuple(x/s2 for x in A(v2)) if s2 > 1e-12 else None
    return s1, s2, v1, v2, u1, u2
def linmap(a, b, c, d):
    a, b, c, d = map(float, (a, b, c, d)); s1, s2, v1, v2, u1, u2 = svd2(a, b, c, d); det, tr = a*d - b*c, a + d
    A = lambda v: (a*v[0] + b*v[1], c*v[0] + d*v[1])
    for s, v, u in ((s1, v1, u1), (s2, v2, u2)):                               # A v_i = σ_i u_i
        if u: assert math.dist(A(v), (s*u[0], s*u[1])) < 1e-9
    if u1 and u2: assert abs(u1[0]*u2[0] + u1[1]*u2[1]) < 1e-9
    assert abs(s1*s2 - abs(det)) < 1e-9*(1 + s1*s1) and abs(max(math.hypot(*A((math.cos(t*math.pi/1800), math.sin(t*math.pi/1800)))) for t in range(3600)) - s1) < 1e-4*(1 + s1)
    disc = tr*tr/4 - det; ev = None
    if disc >= 0:
        l = [tr/2 + math.sqrt(disc), tr/2 - math.sqrt(disc)]; ev = []
        for x in l:
            v = (b, x - a) if abs(b) > 1e-9 else ((x - d, c) if abs(c) > 1e-9 else ((1, 0) if abs(x - a) < 1e-9 else (0, 1))); n = math.hypot(*v); ev.append((x, (v[0]/n, v[1]/n)))
        for x, v in ev: assert math.dist(A(v), (x*v[0], x*v[1])) < 1e-8*(1 + abs(x))
    R2 = max(1.6, 1.1*s1*1.25); o = []
    def panel(ox, f, R, title, vecs, circ):
        X = lambda x: ox + 100 + 100*x/R; Y = lambda y: 112 - 100*y/R; cid = "p%d" % ox
        s = [f'<clipPath id="{cid}"><rect x="{ox}" y="12" width="200" height="200"/></clipPath><rect x="{ox}" y="12" width="200" height="200" fill="none" stroke="#888"/>', T(ox + 100, 228, title, sz=11), f'<g clip-path="url(#{cid})">']
        for k in range(-3, 4):
            for e0, e1 in (((k, -1.6), (k, 1.6)), ((-1.6, k), (1.6, k))):
                p, q = f(e0), f(e1); s.append(f'<line x1="{X(p[0]):.0f}" y1="{Y(p[1]):.0f}" x2="{X(q[0]):.0f}" y2="{Y(q[1]):.0f}" stroke="#888" stroke-width="{1 if k == 0 else .5}" opacity=".6"/>')
        sq = [f((0, 0)), f((1, 0)), f((1, 1)), f((0, 1))]; s.append(f'<polygon points="{" ".join(f"{X(x):.0f},{Y(y):.0f}" for x, y in sq)}" fill="{C4}44" stroke="{C4}"/>')
        s.append(polyline(X, Y, [f(p) for p in circ_pts(0, 0, 1)] + [f((1, 0))], C1, 1.8))
        for (x, y), col, lab in vecs: s.append(f'<line x1="{X(0):.0f}" y1="{Y(0):.0f}" x2="{X(x):.0f}" y2="{Y(y):.0f}" stroke="{col}" stroke-width="2.2" marker-end="url(#ac)"/>' + T(X(x*1.12), Y(y*1.12) + 4, lab, sz=11, c=col))
        if ev:
            for x, v in ev: s.append(f'<line x1="{X(-R*v[0]):.0f}" y1="{Y(-R*v[1]):.0f}" x2="{X(R*v[0]):.0f}" y2="{Y(R*v[1]):.0f}" stroke="{C3}" stroke-width="1.2" stroke-dasharray="5 3"/>')
        return s + ['</g>']
    I = lambda v: v
    o += panel(5, I, 1.6, "domain: unit circle, v₁ v₂", [(v1, C2, "v₁"), (v2, C2, "v₂")], 1)
    o += panel(215, A, R2, f"image: ellipse, σ₁u₁ σ₂u₂", [((s1*u1[0], s1*u1[1]) if u1 else (0, 0), C2, "σ₁u₁"), ((s2*u2[0], s2*u2[1]) if u2 else (0, 0), C2, "σ₂u₂")], 1)
    ln = [f"A = [[{a:g}, {b:g}], [{c:g}, {d:g}]]: det = {det:g} = signed area of the image of the unit square (orange), trace {tr:g}",
          "eigenvalues " + (", ".join(f"{x:.3f}" for x, _ in ev) + " (green dashed lines = eigenlines, unchanged in direction)" if ev else f"{tr/2:.3f} ± {math.sqrt(-disc):.3f}i: no real eigenline"),
          f"σ₁ = {s1:.4f}, σ₂ = {s2:.4f}, rank {2 if s2 > 1e-9 else 1 if s1 > 1e-9 else 0}" + (f", condition number {s1/s2:.3f}" if s2 > 1e-9 else ", singular") + " · A V = U Σ, σ₁σ₂ = |det|, ‖A‖ = σ₁ ✓"]
    from fgroups import wrap
    ls = [l for x in ln for l in wrap(x, 66)]
    return svg(420, 236 + 14*len(ls), o + [T(10, 236 + 14*(k+1), html.escape(l, quote=False), "start", sz=11) for k, l in enumerate(ls)], "c")

def basis(b11, b12, b21, b22, x1, x2):
    b1, b2, x = (float(b11), float(b12)), (float(b21), float(b22)), (float(x1), float(x2)); det = b1[0]*b2[1] - b1[1]*b2[0]
    assert abs(det) > 1e-9, "b1, b2 are linearly dependent: not a basis"
    c1, c2 = (x[0]*b2[1] - x[1]*b2[0])/det, (b1[0]*x[1] - b1[1]*x[0])/det
    assert math.dist((c1*b1[0] + c2*b2[0], c1*b1[1] + c2*b2[1]), x) < 1e-9
    pts = [(0, 0), b1, b2, x, (c1*b1[0], c1*b1[1])]; X, Y = view(pts, .35); box = X.box; o = []
    for k in range(-6, 7):                                                             # standard grid (grey) and skew grid (blue)
        seg = clipline(1, 0, k, box); seg2 = clipline(0, 1, k, box)
        for sg in (seg, seg2):
            if sg: o.append(line_d(X, Y, *sg, c="#888", w=.4))
        for (u, w) in ((b1, b2), (b2, b1)):
            nrm = (-w[1], w[0]); sg = clipline(nrm[0], nrm[1], k*(nrm[0]*u[0] + nrm[1]*u[1]), box)
            if sg: o.append(line_d(X, Y, *sg, c=C1, w=.8))
    o.append(line_d(X, Y, (0, 0), b1, C1, 2.5, "", True) + line_d(X, Y, (0, 0), b2, C3, 2.5, "", True) + txt(X, Y, b1[0]*1.1, b1[1]*1.1, "b₁", "middle", C1) + txt(X, Y, b2[0]*1.1, b2[1]*1.1, "b₂", "middle", C3))
    p1 = (c1*b1[0], c1*b1[1]); o.append(line_d(X, Y, (0, 0), p1, C1, 1.5, "") + line_d(X, Y, p1, x, C3, 1.5, "4 3") + line_d(X, Y, (0, 0), x, C2, 2.5, "", True) + txt(X, Y, x[0]*1.08, x[1]*1.08, "x", "middle", C2))
    Pm = f"P = [b₁ b₂] = [[{b1[0]:g}, {b2[0]:g}], [{b1[1]:g}, {b2[1]:g}]]"
    return wrap_svg(o, [f"x = ({x[0]:g}, {x[1]:g}) in the standard basis has coordinates [x]_B = ({c1:.4g}, {c2:.4g}) in B = (b₁, b₂): x = c₁b₁ + c₂b₂ ✓", Pm + f", det P = {det:g} ≠ 0, [x]_B = P⁻¹x (blue/green grid = coordinate lines of B)"])

# ---------- 3D helpers ----------
def proj(p, az, el):
    x1, y1 = p[0]*math.cos(az) - p[1]*math.sin(az), p[0]*math.sin(az) + p[1]*math.cos(az)
    return x1, p[2]*math.cos(el) + y1*math.sin(el), y1*math.cos(el) - p[2]*math.sin(el)
def sub(a, b): return (a[0]-b[0], a[1]-b[1], a[2]-b[2])
def cross(a, b): return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])
def dot(a, b): return sum(x*y for x, y in zip(a, b))
PHI = (1 + 5**.5)/2
def verts(name):
    P = list(itertools.product((1, -1), repeat=3))
    if name == "cube": return [tuple(map(float, p)) for p in P]
    if name == "tetra": return [(1., 1., 1.), (1., -1., -1.), (-1., 1., -1.), (-1., -1., 1.)]
    if name == "octa": return [(s*(i == 0), s*(i == 1), s*(i == 2)) for i in range(3) for s in (1., -1.)]
    if name == "icosa": return [tuple(float(v) for v in (c if k == 0 else (c[2], c[0], c[1]) if k == 1 else (c[1], c[2], c[0]))) for k in range(3) for c in [(0, s1, s2*PHI) for s1 in (1, -1) for s2 in (1, -1)]]
    if name == "dodeca":
        V = [tuple(map(float, p)) for p in P]
        for s1 in (1, -1):
            for s2 in (1, -1): V += [(0., s1/PHI, s2*PHI), (s1/PHI, s2*PHI, 0.), (s2*PHI, 0., s1/PHI)]
        return V
    raise SystemExit("solid: tetra | cube | octa | dodeca | icosa")
def hull_faces(V):
    faces = set()
    for i, j, k in itertools.combinations(range(len(V)), 3):
        n = cross(sub(V[j], V[i]), sub(V[k], V[i]))
        if math.sqrt(dot(n, n)) < 1e-9: continue
        side = [dot(n, sub(V[m], V[i])) for m in range(len(V))]
        if all(s <= 1e-9 for s in side) or all(s >= -1e-9 for s in side): faces.add(frozenset(m for m in range(len(V)) if abs(side[m]) < 1e-9))
    out = []
    for f in faces:
        pts = list(f); c = tuple(sum(V[m][t] for m in pts)/len(pts) for t in range(3)); n = cross(sub(V[pts[1]], V[pts[0]]), sub(V[pts[2]], V[pts[0]]))
        if dot(n, c) < 0: n = tuple(-x for x in n)                                             # outward normal (solids are centred at 0)
        e1 = sub(V[pts[0]], c); e2 = cross(n, e1)
        pts.sort(key=lambda m: math.atan2(dot(sub(V[m], c), e2), dot(sub(V[m], c), e1))); nn = math.sqrt(dot(n, n)); out.append((pts, tuple(x/nn for x in n)))
    return out
DIH = {"tetra": 70.5288, "cube": 90.0, "octa": 109.4712, "dodeca": 116.5651, "icosa": 138.1897}; NF = {"tetra": 4, "cube": 6, "octa": 8, "dodeca": 12, "icosa": 20}
def solid(name, az=35, el=25):
    az, el = math.radians(float(az)), math.radians(float(el)); V = verts(name); F = hull_faces(V)
    edges = {}
    for fi, (pts, n) in enumerate(F):
        for a, b in zip(pts, pts[1:] + pts[:1]): edges.setdefault(frozenset((a, b)), []).append(fi)
    assert len(V) - len(edges) + len(F) == 2, "Euler V-E+F=2 failed"
    assert all(len(v) == 2 for v in edges.values()) and len(F) == NF[name]
    L_ = {round(math.dist(V[tuple(e)[0]], V[tuple(e)[1]]), 6) for e in edges}; assert len(L_) == 1, "edges not equal: not regular"
    ang = math.degrees(math.acos(-dot(F[next(iter(edges.values()))[0]][1], F[next(iter(edges.values()))[1]][1]))); assert abs(ang - DIH[name]) < 1e-3, (ang, DIH[name])
    P = [proj(v, az, el) for v in V]; vis = [proj(n, az, el)[2] > 1e-9 for _, n in F]
    s = 210/(max(abs(p[0]) for p in P)*1.15 + 1e-9); s = min(s, 140/(max(abs(p[1]) for p in P)*1.15)); X = lambda x: 210 + s*x; Y = lambda y: 150 - s*y; o = []
    for fi, (pts, n) in enumerate(F):
        if vis[fi]: o.append(poly_d(lambda x: X(x), lambda y: Y(y), [(P[m][0], P[m][1]) for m in pts], C1 + "22", "none"))
    for e, fs in edges.items():
        a, b = tuple(e); show = any(vis[f] for f in fs)
        o.append(f'<line x1="{X(P[a][0]):.0f}" y1="{Y(P[a][1]):.0f}" x2="{X(P[b][0]):.0f}" y2="{Y(P[b][1]):.0f}" stroke="{C1 if show else "#888"}" stroke-width="{2 if show else 1}"' + ("" if show else ' stroke-dasharray="3 3" opacity=".6"') + "/>")
    return wrap_svg(o, [f"{name}: V = {len(V)}, E = {len(edges)}, F = {len(F)}; V − E + F = 2 ✓ (faces from the convex hull, not typed in)", f"all {len(edges)} edges equal (regular ✓); dihedral angle {ang:.4f}° ✓; solid = visible edges (back-face culling), dashed = hidden; drag-free: re-run with az, el"])
SAFE = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
def surface(expr, R=2.0, az=40, el=30, N=14):
    R, az, el = float(R), math.radians(float(az)), math.radians(float(el)); code = compile(expr, "f", "eval")
    f = lambda x, y: eval(code, {"__builtins__": {}}, {**SAFE, "x": x, "y": y})
    g = [-R + 2*R*i/N for i in range(N+1)]; Z = [[f(x, y) for x in g] for y in g]
    assert all(isinstance(z, float) and math.isfinite(z) for r in Z for z in r), "f is not finite/real on the grid"
    zmax = max(abs(z) for r in Z for z in r) or 1; sc = R/zmax if zmax > R else 1
    P = [[proj((x, y, Z[j][i]*sc), az, el) for i, x in enumerate(g)] for j, y in enumerate(g)]; allp = [p for r in P for p in r]
    s = min(190/max(abs(p[0]) for p in allp), 130/max(abs(p[1]) for p in allp)); X = lambda x: 210 + s*x; Y = lambda y: 150 - s*y; o = []
    ax = [proj(p, az, el) for p in ((-R, 0, 0), (R, 0, 0), (0, -R, 0), (0, R, 0), (0, 0, -R*.6), (0, 0, R*.6))]
    for a, b in ((0, 1), (2, 3), (4, 5)): o.append(f'<line x1="{X(ax[a][0]):.0f}" y1="{Y(ax[a][1]):.0f}" x2="{X(ax[b][0]):.0f}" y2="{Y(ax[b][1]):.0f}" stroke="#888" stroke-width=".8"/>')
    for rows, col in ((P, C1), ([list(c) for c in zip(*P)], C2)):
        for r in rows: o.append('<polyline fill="none" stroke="%s" stroke-width="1" points="%s"/>' % (col, " ".join(f"{X(p[0]):.0f},{Y(p[1]):.0f}" for p in r)))
    return wrap_svg(o, [f"z = {expr} on [−{R:g}, {R:g}]², view az {math.degrees(az):g}°, el {math.degrees(el):g}°" + (f" (z scaled by {sc:.3g})" if sc != 1 else ""), f"wireframe from {N+1}×{N+1} evaluated points, no hidden-line removal; blue = lines of constant y, red = constant x; z range [{min(min(r) for r in Z):.3g}, {max(max(r) for r in Z):.3g}]"])

# ---------- geometric algebra Cl(3) (Cl(2) = grades on e1,e2) ----------
def _sign(a, b):
    s, x = 1, a >> 1
    while x:
        if bin(x & b).count("1") & 1: s = -s
        x >>= 1
    return s
def gp(A, B):
    out = {}
    for ma, ca in A.items():
        for mb, cb in B.items(): out[ma ^ mb] = out.get(ma ^ mb, 0) + _sign(ma, mb)*ca*cb
    return {k: v for k, v in out.items() if abs(v) > 1e-15}
def rev(A): return {m: c*(-1 if (bin(m).count("1")*(bin(m).count("1") - 1)//2) & 1 else 1) for m, c in A.items()}
vec = lambda *c: {1 << i: x for i, x in enumerate(c) if x}
def sandwich(R, v): return gp(gp(R, v), rev(R))
def ga(cmd, *a):
    a = [float(x) for x in a]; o, notes = [], []
    if cmd in ("rotate", "reflect", "wedge"):
        if cmd == "rotate": x, y, deg = a; th = math.radians(deg); v = vec(x, y); R = {0: math.cos(th/2), 3: -math.sin(th/2)}      # R = cos(θ/2) − e12 sin(θ/2)
        elif cmd == "reflect": x, y, deg = a; ph = math.radians(deg); n = vec(-math.sin(ph), math.cos(ph)); v = vec(x, y)
        else: a1, a2, b1, b2 = a
        if cmd == "rotate":
            w = sandwich(R, v); w1, w2 = w.get(1, 0), w.get(2, 0); exp = (x*math.cos(th) - y*math.sin(th), x*math.sin(th) + y*math.cos(th))
            assert math.dist((w1, w2), exp) < 1e-12 and abs(math.hypot(w1, w2) - math.hypot(x, y)) < 1e-12 and set(w) <= {1, 2}
            pts = [(0, 0), (x, y), (w1, w2)]; X, Y = view(pts + [(-1, -1), (1, 1)], .35)
            r = math.hypot(x, y); a0 = math.atan2(y, x); arc = [(r*.5*math.cos(a0 + th*k/30), r*.5*math.sin(a0 + th*k/30)) for k in range(31)]
            o = [line_d(X, Y, (X.box[0], 0), (X.box[1], 0), "#888", .8), line_d(X, Y, (0, X.box[2]), (0, X.box[3]), "#888", .8), line_d(X, Y, (0, 0), (x, y), C1, 2.5, "", True), line_d(X, Y, (0, 0), (w1, w2), C2, 2.5, "", True), polyline(X, Y, arc, C4, 1.5), txt(X, Y, x*1.08, y*1.08, "v", "middle", C1), txt(X, Y, w1*1.08, w2*1.08, "RvR̃", "middle", C2)]
            notes = [f"rotor R = cos(θ/2) − e₁₂ sin(θ/2) with θ = {deg:g}°: R = {R[0]:.4f} {R[3]:+.4f} e₁₂", f"v' = R v R̃ = ({w1:.4f}, {w2:.4f}) = counter-clockwise rotation by θ ✓, |v'| = |v| ✓ (only grade-1 terms remain)"]
        elif cmd == "reflect":
            nv = n; w = gp(gp(nv, v), nv); w = {k: -c for k, c in w.items()}; w1, w2 = w.get(1, 0), w.get(2, 0)
            u = (math.cos(ph), math.sin(ph)); k_ = x*u[0] + y*u[1]; exp = (2*k_*u[0] - x, 2*k_*u[1] - y); assert math.dist((w1, w2), exp) < 1e-12 and set(w) <= {1, 2}
            X, Y = view([(0, 0), (x, y), (w1, w2), (-1, -1), (1, 1)], .35); seg = clipline(-u[1], u[0], 0, X.box)
            o = [line_d(X, Y, *seg, c=C3, w=2, dash="6 4"), line_d(X, Y, (0, 0), (x, y), C1, 2.5, "", True), line_d(X, Y, (0, 0), (w1, w2), C2, 2.5, "", True), line_d(X, Y, (x, y), (w1, w2), "#888", 1, "2 3")]
            notes = [f"reflection in the line at {deg:g}° (green): v' = −n v n with unit normal n = (−sin φ, cos φ)", f"v' = ({w1:.4f}, {w2:.4f}) = 2(v·u)u − v ✓ (|v'| = |v|); two reflections compose to a rotation by twice the angle between the lines"]
        else:
            ab = gp(vec(a1, a2), vec(b1, b2)); dt, wd = ab.get(0, 0), ab.get(3, 0); assert abs(dt - (a1*b1 + a2*b2)) < 1e-12 and abs(wd - (a1*b2 - a2*b1)) < 1e-12
            pts = [(0, 0), (a1, a2), (a1 + b1, a2 + b2), (b1, b2)]; X, Y = view(pts, .3)
            o = [poly_d(X, Y, pts, C4 + "44", C4), line_d(X, Y, (0, 0), (a1, a2), C1, 2.5, "", True), line_d(X, Y, (0, 0), (b1, b2), C2, 2.5, "", True), txt(X, Y, a1*1.08, a2*1.08 - .05, "a", "middle", C1), txt(X, Y, b1*1.08, b2*1.08, "b", "middle", C2)]
            notes = [f"geometric product ab = a·b + a∧b = {dt:.4f} + {wd:.4f} e₁₂", f"a∧b = signed area of the parallelogram (orange) = |a||b| sin θ, a·b = |a||b| cos θ ✓ (computed from the product, checked against the formulas)"]
        return wrap_svg(o, notes)
    assert cmd == "rotate3", "ga: rotate | reflect | wedge | rotate3"
    x, y, z, nx, ny, nz, deg = a; nn = math.sqrt(nx*nx + ny*ny + nz*nz); assert nn > 1e-9; n = (nx/nn, ny/nn, nz/nn); th = math.radians(deg)
    B = {6: n[0], 5: -n[1], 3: n[2]}                       # bivector dual to the axis: n1 e23 + n2 e31 + n3 e12  (e31 = -e13, mask 5)
    R = {0: math.cos(th/2), **{m: -math.sin(th/2)*c for m, c in B.items()}}
    w = sandwich(R, vec(x, y, z)); wv = (w.get(1, 0), w.get(2, 0), w.get(4, 0))
    k = (n[0]*x + n[1]*y + n[2]*z); cr = cross(n, (x, y, z)); rod = tuple((x, y, z)[i]*math.cos(th) + cr[i]*math.sin(th) + n[i]*k*(1 - math.cos(th)) for i in range(3))
    assert math.dist(wv, rod) < 1e-12 and abs(math.sqrt(dot(wv, wv)) - math.sqrt(x*x + y*y + z*z)) < 1e-12 and set(w) <= {1, 2, 4}
    az, el = math.radians(35), math.radians(25); Pj = lambda p: proj(p, az, el); L = max(1.3, math.sqrt(x*x + y*y + z*z)*1.2)
    ptsall = [Pj(p) for p in ((L, 0, 0), (-L, 0, 0), (0, L, 0), (0, -L, 0), (0, 0, L), (0, 0, -L))]; s = min(190/max(abs(p[0]) for p in ptsall), 125/max(abs(p[1]) for p in ptsall))
    X = lambda p: 210 + s*Pj(p)[0]; Y = lambda p: 150 - s*Pj(p)[1]; seg = lambda p, q, c, w_=1.5, d="": f'<line x1="{X(p):.0f}" y1="{Y(p):.0f}" x2="{X(q):.0f}" y2="{Y(q):.0f}" stroke="{c}" stroke-width="{w_}"' + (f' stroke-dasharray="{d}"' if d else "") + (' marker-end="url(#ac)"' if d == "A" else "") + "/>"
    o = [seg((-L, 0, 0), (L, 0, 0), "#888", .8), seg((0, -L, 0), (0, L, 0), "#888", .8), seg((0, 0, -L), (0, 0, L), "#888", .8), seg((-n[0]*L, -n[1]*L, -n[2]*L), (n[0]*L, n[1]*L, n[2]*L), C3, 2, "5 3")]
    steps = [tuple((x, y, z)[i]*math.cos(t) + cross(n, (x, y, z))[i]*math.sin(t) + n[i]*k*(1 - math.cos(t)) for i in range(3)) for t in [th*q/30 for q in range(31)]]
    o.append('<polyline fill="none" stroke="%s" stroke-width="1.5" points="%s"/>' % (C4, " ".join(f"{X(p):.0f},{Y(p):.0f}" for p in steps)))
    o += [seg((0, 0, 0), (x, y, z), C1, 2.5, "A"), seg((0, 0, 0), wv, C2, 2.5, "A"), T(X((x, y, z)), Y((x, y, z)) - 6, "v", sz=11, c=C1), T(X(wv), Y(wv) - 6, "RvR̃", sz=11, c=C2)]
    return wrap_svg(o, [f"rotation of v by {deg:g}° about the axis n = ({n[0]:.3f}, {n[1]:.3f}, {n[2]:.3f}) (green) via the rotor R = cos(θ/2) − B sin(θ/2), B = n₁e₂₃ + n₂e₃₁ + n₃e₁₂", f"v' = R v R̃ = ({wv[0]:.4f}, {wv[1]:.4f}, {wv[2]:.4f}) = Rodrigues' formula ✓, |v'| = |v| ✓ (isometric view; arc = path of v)"])

def triangle(spec):
    A, B, Cc = [tuple(map(float, t.split(","))) for t in spec.split()]; d = 2*(A[0]*(B[1]-Cc[1]) + B[0]*(Cc[1]-A[1]) + Cc[0]*(A[1]-B[1])); assert abs(d) > 1e-9, "degenerate triangle"
    ux = ((A[0]**2 + A[1]**2)*(B[1]-Cc[1]) + (B[0]**2 + B[1]**2)*(Cc[1]-A[1]) + (Cc[0]**2 + Cc[1]**2)*(A[1]-B[1]))/d; uy = ((A[0]**2 + A[1]**2)*(Cc[0]-B[0]) + (B[0]**2 + B[1]**2)*(A[0]-Cc[0]) + (Cc[0]**2 + Cc[1]**2)*(B[0]-A[0]))/d
    O = (ux, uy); R = math.dist(O, A); assert abs(R - math.dist(O, B)) < 1e-9 and abs(R - math.dist(O, Cc)) < 1e-9
    G = tuple((A[i] + B[i] + Cc[i])/3 for i in range(2)); H = tuple(A[i] + B[i] + Cc[i] - 2*O[i] for i in range(2)); N = tuple((O[i] + H[i])/2 for i in range(2))
    for P_, Q_, S_ in ((A, B, Cc), (B, Cc, A), (Cc, A, B)): assert abs((H[0]-P_[0])*(Q_[0]-S_[0]) + (H[1]-P_[1])*(Q_[1]-S_[1])) < 1e-8      # AH ⟂ BC
    assert abs((H[0]-O[0])*(G[1]-O[1]) - (H[1]-O[1])*(G[0]-O[0])) < 1e-9 and math.dist(H, G) - 2*math.dist(G, O) < 1e-9                    # Euler line, HG = 2 GO
    foot = lambda P_, Q_, S_: (lambda t: (Q_[0] + t*(S_[0]-Q_[0]), Q_[1] + t*(S_[1]-Q_[1])))(((P_[0]-Q_[0])*(S_[0]-Q_[0]) + (P_[1]-Q_[1])*(S_[1]-Q_[1]))/((S_[0]-Q_[0])**2 + (S_[1]-Q_[1])**2))
    nine = [((P_[0]+Q_[0])/2, (P_[1]+Q_[1])/2) for P_, Q_ in ((A, B), (B, Cc), (Cc, A))] + [foot(A, B, Cc), foot(B, Cc, A), foot(Cc, A, B)] + [((P_[0]+H[0])/2, (P_[1]+H[1])/2) for P_ in (A, B, Cc)]
    assert all(abs(math.dist(N, p) - R/2) < 1e-8 for p in nine), "nine-point circle check failed"
    pts = [A, B, Cc, H, (O[0]+R, O[1]), (O[0]-R, O[1]), (O[0], O[1]+R), (O[0], O[1]-R)]; X, Y = view(pts, .12); o = []
    o += [f'<circle cx="{X(O[0]):.1f}" cy="{Y(O[1]):.1f}" r="{R*X.s:.1f}" fill="none" stroke="{C1}" stroke-width="1.4"/>', f'<circle cx="{X(N[0]):.1f}" cy="{Y(N[1]):.1f}" r="{R/2*X.s:.1f}" fill="none" stroke="{C3}" stroke-width="1.4"/>', poly_d(X, Y, [A, B, Cc], C4 + "22", C4)]
    seg = clipline(H[1]-O[1], O[0]-H[0], H[1]*O[0]-H[0]*O[1], X.box) if math.dist(O, H) > 1e-9 else None
    if seg: o.append(line_d(X, Y, *seg, c=C2, w=1.2, dash="5 3"))
    for p in nine: o.append(f'<circle cx="{X(p[0]):.1f}" cy="{Y(p[1]):.1f}" r="2.8" fill="{C3}"/>')
    for p, l, c in ((O, "O", C1), (G, "G", C2), (H, "H", C2), (N, "N", C3)): o.append(f'<circle cx="{X(p[0]):.1f}" cy="{Y(p[1]):.1f}" r="3.5" fill="{c}"/>' + T(X(p[0]) + 6, Y(p[1]) - 5, l, "start", c, 11))
    for p, l in ((A, "A"), (B, "B"), (Cc, "C")): o.append(T(X(p[0]), Y(p[1]) + 14*(1 if p[1] < G[1] else -1), l, sz=11))
    return wrap_svg(o, [f"circumcircle (blue, centre O, R = {R:.4f}), nine-point circle (green, centre N = midpoint of OH, radius R/2)", f"Euler line O–G–H (red dashed): collinear ✓, HG = 2·GO ✓; the 9 green points (3 midpoints, 3 altitude feet, 3 midpoints of vertex–H) all lie on the nine-point circle ✓ (distances to N checked)"])
