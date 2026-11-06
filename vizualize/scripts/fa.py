"""Analysis / functional-analysis pictures in R^2 (honest finite-dimensional analogues). stdlib only; every picture carries a numeric certificate.
  mv.py separate "0,0 2,0 2,1 0,1" "3,3"     Hahn-Banach separation: polygon/disc/point vs polygon/disc/point (disc: "c:1,1,.8")
  mv.py extension l1|l2|linf t               norm-preserving extensions of f(x)=t*x1 from the x-axis M to R^2 (wedge of valid s)
  mv.py riesz y1 y2                          phi(x)=<x,y>: level lines, kernel, ||phi||=||y||
  mv.py dual p a b                           phi=(a,b) on (R^2,l_p): where ||phi|| is attained, ||phi||=||(a,b)||_q
  mv.py project x1 x2 d1 d2                  orthogonal projection onto span(d), Pythagoras
  mv.py fourier square|saw|tri N             partial sums, Gibbs, Parseval check
  mv.py cobweb "cos(x)" x0 [a b]             fixed-point iteration, Banach bound checked"""
import math, cmath, html
from base import *
def view(pts, pad=.18):
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]; x0, x1, y0, y1 = min(xs), max(xs), min(ys), max(ys)
    w, h = (x1-x0) or 1, (y1-y0) or 1; x0 -= pad*w; x1 += pad*w; y0 -= pad*h; y1 += pad*h
    s = min(368/(x1-x0), 268/(y1-y0)); cx, cy = (x0+x1)/2, (y0+y1)/2
    X = lambda x: 210 + s*(x-cx); Y = lambda y: 160 - s*(y-cy)
    X.box = (cx-210/s, cx+210/s, cy-160/s, cy+160/s); X.s = s
    return X, Y
def clipline(a, b, c, box):
    """endpoints of {a x + b y = c} inside box (x0,x1,y0,y1)"""
    x0, x1, y0, y1 = box; P = []
    if abs(b) > 1e-12:
        for x in (x0, x1):
            y = (c - a*x)/b
            if y0 - 1e-9 <= y <= y1 + 1e-9: P.append((x, y))
    if abs(a) > 1e-12:
        for y in (y0, y1):
            x = (c - b*y)/a
            if x0 - 1e-9 <= x <= x1 + 1e-9: P.append((x, y))
    return (P[0], P[-1]) if len(P) >= 2 else None
def poly_d(X, Y, pts, fill, stroke):
    pts = pts[::max(1, len(pts)//90)]
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.5"/>' % (" ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in pts), fill, stroke)
def line_d(X, Y, p, q, c="#888", w=1.5, dash="", arrow=False):
    return f'<line x1="{X(p[0]):.1f}" y1="{Y(p[1]):.1f}" x2="{X(q[0]):.1f}" y2="{Y(q[1]):.1f}" stroke="{c}" stroke-width="{w}"' + (f' stroke-dasharray="{dash}"' if dash else "") + (' marker-end="url(#ac)"' if arrow else "") + "/>"
def txt(X, Y, x, y, s, a="middle", c="currentColor"): return T(X(x), Y(y), html.escape(s, quote=False), a, c, 11)
def wrap_svg(body, notes):
    from fgroups import wrap
    ls = [l for n in notes for l in wrap(n, 58)]
    return svg(420, 320 + 14*len(ls), body + [T(10, 316 + 14*(k+1), html.escape(l, quote=False), "start", sz=11) for k, l in enumerate(ls)], "c")

# ---------- convex sets ----------
def parse_set(s):
    s = s.strip()
    if s.startswith("c:"): cx, cy, r = map(float, s[2:].split(",")); return ("disc", (cx, cy), r)
    pts = [tuple(map(float, t.split(","))) for t in s.split()]
    return ("pt", pts[0]) if len(pts) == 1 else ("poly", _hull(pts))
def _hull(P):
    P = sorted(set(P)); cr = lambda o, a, b: (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lo, up = [], []
    for p in P:
        while len(lo) >= 2 and cr(lo[-2], lo[-1], p) <= 0: lo.pop()
        lo.append(p)
    for p in reversed(P):
        while len(up) >= 2 and cr(up[-2], up[-1], p) <= 0: up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]
def h(S, n):
    """support function max_{x in S} <n,x> (exact)"""
    if S[0] == "pt": return S[1][0]*n[0] + S[1][1]*n[1]
    if S[0] == "disc": return S[1][0]*n[0] + S[1][1]*n[1] + S[2]*math.hypot(*n)
    return max(p[0]*n[0] + p[1]*n[1] for p in S[1])
def nearest(S, p):
    if S[0] == "pt": return S[1]
    if S[0] == "disc":
        d = math.hypot(p[0]-S[1][0], p[1]-S[1][1]); return p if d <= S[2] else (S[1][0] + S[2]*(p[0]-S[1][0])/d, S[1][1] + S[2]*(p[1]-S[1][1])/d)
    V = S[1]; inside = all((V[(i+1) % len(V)][0]-V[i][0])*(p[1]-V[i][1]) - (V[(i+1) % len(V)][1]-V[i][1])*(p[0]-V[i][0]) >= -1e-12 for i in range(len(V)))
    if inside: return p
    best = None
    for i in range(len(V)):
        a, b = V[i], V[(i+1) % len(V)]; dx, dy = b[0]-a[0], b[1]-a[1]; t = max(0, min(1, ((p[0]-a[0])*dx + (p[1]-a[1])*dy)/(dx*dx+dy*dy)))
        q = (a[0]+t*dx, a[1]+t*dy)
        if best is None or math.dist(p, q) < math.dist(p, best): best = q
    return best
def pts_of(S):
    if S[0] == "pt": return [S[1]]
    if S[0] == "disc": return [(S[1][0] + S[2]*math.cos(t*math.pi/24), S[1][1] + S[2]*math.sin(t*math.pi/24)) for t in range(48)]
    return S[1]
def separate(a, b):
    A, B = parse_set(a), parse_set(b)
    pa = pts_of(A)[0]; pb = pts_of(B)[0]
    for _ in range(4000): pa = nearest(A, pb); pb = nearest(B, pa)        # alternating projections -> closest pair
    d = math.dist(pa, pb); assert d > 1e-6, "the sets intersect or touch: Hahn-Banach separation needs disjoint convex sets (strict separation: positive gap)"
    n = ((pb[0]-pa[0])/d, (pb[1]-pa[1])/d); hA = h(A, n); lB = -h(B, (-n[0], -n[1]))   # certificate: sup_A <n,.> <= c <= inf_B <n,.>
    assert hA <= lB - 1e-9 and abs((lB - hA) - d) < 1e-5, "separation certificate failed"
    c = (hA + lB)/2
    X, Y = view(pts_of(A) + pts_of(B)); box = X.box; o = []
    for S, col in ((A, "#3b82f6"), (B, "#f43f5e")):
        if S[0] == "pt": o.append(f'<circle cx="{X(S[1][0]):.1f}" cy="{Y(S[1][1]):.1f}" r="5" fill="{col}"/>')
        elif S[0] == "disc": o.append(f'<circle cx="{X(S[1][0]):.1f}" cy="{Y(S[1][1]):.1f}" r="{S[2]*X.s:.1f}" fill="{col}33" stroke="{col}" stroke-width="1.5"/>')
        else: o.append(poly_d(X, Y, S[1], col + "33", col))
    seg = clipline(n[0], n[1], c, box)
    if seg: o.append(line_d(X, Y, *seg, c="#22c55e", w=2, dash="6 4"))
    m = ((pa[0]+pb[0])/2, (pa[1]+pb[1])/2); o.append(line_d(X, Y, m, (m[0]+n[0]*40/X.s, m[1]+n[1]*40/X.s), "#22c55e", 2, "", True))
    o.append(txt(X, Y, m[0]+n[0]*46/X.s, m[1]+n[1]*46/X.s, "f", "middle", "#22c55e"))
    o.append(line_d(X, Y, pa, pb, "#888", 1, "2 3"))
    return wrap_svg(o, [f"hyperplane {{f = c}} with f = ({n[0]:.3f}, {n[1]:.3f}), c = {c:.3f}", f"certificate: sup_A f = {hA:.4f} < c < inf_B f = {lB:.4f}; gap = distance = {d:.4f} (support functions, exact)"])

# ---------- Hahn-Banach extension ----------
def ball(norm, N=720):
    if norm == "l1": return [(1, 0), (0, 1), (-1, 0), (0, -1)]
    if norm == "linf": return [(1, 1), (-1, 1), (-1, -1), (1, -1)]
    assert norm == "l2", "norm: l1 | l2 | linf"
    return [(math.cos(2*math.pi*k/N), math.sin(2*math.pi*k/N)) for k in range(N)]
def extension(norm, t):
    t = float(t); assert 0 < abs(t) <= 5, "t must be non-zero"
    V = [(v[0]/abs(t), v[1]/abs(t)) for v in ball(norm)]                  # {p <= 1} for p = |t|*norm, so that f <= p on M with equality at q
    lo, hi = -math.inf, math.inf
    for v in V:                                                            # F(x) = t x1 + s x2 <= 1 on the ball  <=>  F <= p
        r = 1 - t*v[0]
        if abs(v[1]) < 1e-12: assert r >= -1e-9, "f is not dominated by p on M"
        elif v[1] > 0: hi = min(hi, r/v[1])
        else: lo = max(lo, r/v[1])
    theory = {"l1": (-abs(t), abs(t)), "linf": (0, 0), "l2": (0, 0)}[norm]    # unit ball of the dual norm: l-inf / l1 / l2
    tol = 5e-3 if norm == "l2" else 1e-9
    assert abs(lo - theory[0]) < tol and abs(hi - theory[1]) < tol, f"computed [{lo},{hi}] disagrees with dual-ball theory {theory}"
    for s in (lo, hi):
        assert max(t*v[0] + s*v[1] for v in V) <= 1 + 1e-9 and abs(max(t*v[0] + s*v[1] for v in V) - 1) < 1e-6   # F <= p everywhere, touching
    q = (1/t, 0); X, Y = view(V + [q, (-1/t, 0)]); box = X.box; o = []
    o.append(poly_d(X, Y, V, "#3b82f622", "#3b82f6")); o.append(line_d(X, Y, (box[0], 0), (box[1], 0), "#888", 1.2))
    for s, col in ((lo, "#f43f5e"), (hi, "#22c55e")):
        seg = clipline(t, s, 1, box)
        if seg: o.append(line_d(X, Y, *seg, c=col, w=2))
    if hi - lo > 1e-2:                                                     # shade the wedge of admissible lines {F=1}
        w1, w2 = clipline(t, lo, 1, box), clipline(t, hi, 1, box)
        if w1 and w2: o.append(f'<polygon points="{X(q[0]):.1f},{Y(0):.1f} {X(w1[0][0]):.1f},{Y(w1[0][1]):.1f} {X(w2[0][0]):.1f},{Y(w2[0][1]):.1f}" fill="#f59e0b33" stroke="none"/>')
    o.append(f'<circle cx="{X(q[0]):.1f}" cy="{Y(0):.1f}" r="5" fill="#f59e0b"/>' + txt(X, Y, q[0], -26/X.s, "q = (1/t, 0)"))
    unique = hi - lo < 1e-2; res = "unique extension (s = 0)" if unique else f"s ∈ [{lo:.3f}, {hi:.3f}] — infinitely many norm-preserving extensions"
    return wrap_svg(o, [f"f(x) = {t:g}·x1 on M = x-axis, norm {norm}; ball {{p ≤ 1}} with p = ‖f‖·‖·‖ is drawn (blue)", "lines {F = 1} (F = t·x1 + s·x2) through q that keep the ball on one side = norm-preserving extensions F", res, "matches the unit ball of the dual norm (ℓ1→ℓ∞ square: wedge; ℓ2→ℓ2, ℓ∞→ℓ1: single point) ✓"])

# ---------- Riesz / duality / projection ----------
def riesz(y1, y2):
    y = (float(y1), float(y2)); ny = math.hypot(*y); assert ny > 1e-9
    best = max(math.cos(t*math.pi/1800)*y[0] + math.sin(t*math.pi/1800)*y[1] for t in range(3600)); assert abs(best - ny) < 1e-4*ny
    u0 = (y[0]/ny, y[1]/ny)
    X, Y = view([(-1.3, -1.3), (1.3, 1.3), y, (-y[0], -y[1])]); box = X.box; o = []
    o.append(f'<circle cx="{X(0):.1f}" cy="{Y(0):.1f}" r="{X.s:.1f}" fill="none" stroke="#888" stroke-width="1.2" stroke-dasharray="4 3"/>')
    for c in (-2, -1, 1, 2):
        seg = clipline(y[0], y[1], c, box)
        if seg: o.append(line_d(X, Y, *seg, c="#3b82f6", w=1.2) + txt(X, Y, c*y[0]/ny**2 + .22*y[1]/ny*0 - 0.12*u0[1]*0 + 0.0, c*y[1]/ny**2 - 14/X.s, f"φ={c}", "middle", "#3b82f6"))
    seg = clipline(y[0], y[1], 0, box); o.append(line_d(X, Y, *seg, c="#f43f5e", w=2) + txt(X, Y, 0, -14/X.s, "ker φ", "middle", "#f43f5e"))
    o.append(line_d(X, Y, (0, 0), y, "#22c55e", 2.5, "", True) + txt(X, Y, y[0]*1.04, y[1]*1.04+.1, "y", "middle", "#22c55e"))
    u = (y[0]/ny, y[1]/ny); o.append(f'<circle cx="{X(u[0]):.1f}" cy="{Y(u[1]):.1f}" r="4.5" fill="#f59e0b"/>')
    return wrap_svg(o, [f"φ(x) = ⟨x, y⟩ with y = ({y[0]:g}, {y[1]:g}) on the Hilbert space ℝ² (analogue of ℓ² / L²)", f"level lines {{φ = c}} ⟂ y, spaced 1/‖y‖ = {1/ny:.3f}; ker φ ⟂ y", f"‖φ‖ = sup over the unit circle = {best:.4f} = ‖y‖ = {ny:.4f} ✓, attained at y/‖y‖ (orange)"])
def dual(p, a, b):
    p = math.inf if p in ("inf", "linf") else float(p); a, b = float(a), float(b); assert p >= 1, "p must be >= 1"
    q = math.inf if p == 1 else 1.0 if p == math.inf else p/(p-1)
    nq = max(abs(a), abs(b)) if q == math.inf else (abs(a) + abs(b) if q == 1 else (abs(a)**q + abs(b)**q)**(1/q))
    B = ball("l1") if p == 1 else ball("linf") if p == math.inf else [(math.copysign(abs(math.cos(t))**(2/p), math.cos(t)), math.copysign(abs(math.sin(t))**(2/p), math.sin(t))) for t in [k*math.pi/180 for k in range(360)]]
    best = max(a*x + b*y for x, y in B); assert abs(best - nq) < 2e-3*nq + 1e-9, f"sup = {best} but dual norm formula gives {nq}"
    mx = max(B, key=lambda v: a*v[0] + b*v[1]); X, Y = view(B + [(-1.2, -1.2), (1.2, 1.2)]); box = X.box; o = []
    o.append(poly_d(X, Y, B, "#3b82f622", "#3b82f6"))
    for c, col, w in ((nq, "#22c55e", 2), (-nq, "#22c55e", 1), (0, "#f43f5e", 1.5)):
        seg = clipline(a, b, c, box)
        if seg: o.append(line_d(X, Y, *seg, c=col, w=w, dash="" if c else "4 3"))
    o.append(f'<circle cx="{X(mx[0]):.1f}" cy="{Y(mx[1]):.1f}" r="5" fill="#f59e0b"/>' + txt(X, Y, mx[0]*1.1, mx[1]*1.1 + .1, "x*"))
    qs = "∞" if q == math.inf else f"{q:g}"; ps = "∞" if p == math.inf else f"{p:g}"
    return wrap_svg(o, [f"space (ℝ², ‖·‖_{ps}); functional φ = ({a:g}, {b:g}); unit ball blue, line {{φ = ‖φ‖}} green touches it at x* (attained)", f"‖φ‖ = sup over the ball = {best:.4f} = ‖(a,b)‖_{qs} = {nq:.4f} with 1/{ps} + 1/{qs} = 1 ✓", "swap p ↔ q: the dual ball of ℓ1 is the ℓ∞ square (and vice versa); ℓ2 is self-dual (Riesz)"])
def project(x1, x2, d1, d2):
    x, d = (float(x1), float(x2)), (float(d1), float(d2)); nd = math.hypot(*d); assert nd > 1e-9; u = (d[0]/nd, d[1]/nd)
    k = x[0]*u[0] + x[1]*u[1]; P = (k*u[0], k*u[1]); r = (x[0]-P[0], x[1]-P[1])
    assert abs(r[0]*u[0] + r[1]*u[1]) < 1e-12 and abs((x[0]**2 + x[1]**2) - (P[0]**2 + P[1]**2 + r[0]**2 + r[1]**2)) < 1e-9
    best = min(math.hypot(x[0]-t*u[0], x[1]-t*u[1]) for t in [k + dt/1000 for dt in range(-3000, 3001)]); assert abs(best - math.hypot(*r)) < 1e-5
    X, Y = view([x, (0, 0), (-1.2*u[0]*max(1, abs(k)), -1.2*u[1]*max(1, abs(k))), (1.2*u[0]*max(1, abs(k)), 1.2*u[1]*max(1, abs(k)))]); box = X.box; o = []
    seg = clipline(-u[1], u[0], 0, box); o.append(line_d(X, Y, *seg, c="#3b82f6", w=2) + txt(X, Y, seg[1][0], seg[1][1], "M", "end", "#3b82f6"))
    o.append(line_d(X, Y, (0, 0), x, "#888", 1.5, "", True) + line_d(X, Y, x, P, "#f43f5e", 1.5, "4 3") + line_d(X, Y, (0, 0), P, "#22c55e", 3))
    sq = .12/X.s*40; a = (P[0] + u[0]*sq*(-1 if k > 0 else 1), P[1] + u[1]*sq*(-1 if k > 0 else 1)); n_ = (r[0]/math.hypot(*r)*sq if math.hypot(*r) > 1e-9 else 0, r[1]/math.hypot(*r)*sq if math.hypot(*r) > 1e-9 else 0)
    o.append(f'<polyline fill="none" stroke="#888" points="{X(a[0]):.1f},{Y(a[1]):.1f} {X(a[0]+n_[0]):.1f},{Y(a[1]+n_[1]):.1f} {X(P[0]+n_[0]):.1f},{Y(P[1]+n_[1]):.1f}"/>')
    o.append(f'<circle cx="{X(x[0]):.1f}" cy="{Y(x[1]):.1f}" r="4" fill="currentColor"/>' + txt(X, Y, x[0], x[1] + .12, "x") + txt(X, Y, P[0], P[1] - .2, "Px", "middle", "#22c55e"))
    return wrap_svg(o, [f"orthogonal projection of x onto M = span{d}", f"x − Px ⟂ M ✓ (⟨x−Px, u⟩ = 0); ‖x‖² = ‖Px‖² + ‖x−Px‖² = {x[0]**2+x[1]**2:.4f} ✓; ‖x−Px‖ = {math.hypot(*r):.4f} = min over M (brute force) ✓"])

# ---------- Fourier ----------
FS = {"square": lambda x: (1 if x > 0 else -1) if x != 0 else 0, "saw": lambda x: x, "tri": lambda x: abs(x)}
def coeffs(f, N, M=6000):
    xs = [-math.pi + (i + .5)*2*math.pi/M for i in range(M)]; dx = 2*math.pi/M
    a = [sum(f(x)*math.cos(k*x) for x in xs)*dx/math.pi for k in range(N+1)]; b = [0] + [sum(f(x)*math.sin(k*x) for x in xs)*dx/math.pi for k in range(1, N+1)]
    return a, b
def fourier(kind, N):
    N = int(N); assert kind in FS and 1 <= N <= 80; f = FS[kind]; a, b = coeffs(f, N)
    exact = {"square": lambda k: (0, 4/(math.pi*k) if k % 2 else 0), "saw": lambda k: (0, 2*(-1)**(k+1)/k), "tri": lambda k: (2*((-1)**k - 1)/(math.pi*k*k), 0)}[kind]
    for k in range(1, N+1): assert abs(a[k] - exact(k)[0]) < 2e-3 and abs(b[k] - exact(k)[1]) < 2e-3, f"coefficient {k} disagrees with closed form"
    S = lambda x: a[0]/2 + sum(a[k]*math.cos(k*x) + b[k]*math.sin(k*x) for k in range(1, N+1))
    M = 3000; xs = [-math.pi + (i + .5)*2*math.pi/M for i in range(M)]; dx = 2*math.pi/M
    err2 = sum((f(x) - S(x))**2 for x in xs)*dx; nf2 = sum(f(x)**2 for x in xs)*dx; par = math.pi*(a[0]**2/2 + sum(a[k]**2 + b[k]**2 for k in range(1, N+1)))
    assert abs((nf2 - par) - err2) < 5e-3*(1 + nf2) and par <= nf2 + 1e-3                # Parseval/Bessel: ‖f−S_N‖² = ‖f‖² − π(a0²/2+Σ(a²+b²))
    gibbs = max(S(x) for x in [i*math.pi/800 for i in range(1, 800)]) if kind == "square" else None
    ys = [S(x) for x in xs]; lim = max(abs(min(ys)), abs(max(ys)), 1)*1.15; W, H = 420, 270
    X = lambda x: 30 + (W-60)*(x + math.pi)/(2*math.pi); Yf = lambda y: H/2 + 10 - (H/2-30)*y/lim
    o = [f'<path d="M30 {Yf(0):.0f}H{W-30}M{X(0):.0f} 20V{H-10}" stroke="#888"/>']
    o.append('<polyline fill="none" stroke="#888" stroke-dasharray="4 3" points="%s"/>' % " ".join(f"{X(x):.1f},{Yf(f(x)):.1f}" for x in [-math.pi + i*2*math.pi/160 for i in range(161)] if not (kind == "square" and abs(x) < 0.02)))
    o.append('<polyline fill="none" stroke="#3b82f6" stroke-width="2" points="%s"/>' % " ".join(f"{X(x):.1f},{Yf(S(x)):.1f}" for x in [-math.pi + i*2*math.pi/220 for i in range(221)]))
    notes = [f"{kind}: dashed = f on [−π, π], blue = Fourier partial sum S_{N}", f"‖f − S_N‖₂² = {err2:.4f}; Bessel/Parseval: ‖f‖² − π(a₀²/2+Σ(aₖ²+bₖ²)) = {nf2-par:.4f} ✓; coefficients match the closed forms ✓"]
    if gibbs: notes.append(f"Gibbs: max S_N near the jump = {gibbs:.4f} → 1.1790 as N→∞ (does not vanish)")
    return svg(W, H + 14*(len(notes)+1), o + [T(10, H + 14*(k+1), html.escape(l, quote=False), "start", sz=11) for k, l in enumerate(notes)])

# ---------- Banach fixed point ----------
def cobweb(expr, x0, a=0.0, b=2.0, steps=12):
    import mv
    f = mv.f1(expr); x0, a, b = float(x0), float(a), float(b); steps = int(steps); assert a < b and a <= x0 <= b
    xs = [x0 + 0*i for i in range(1)]
    for _ in range(5000): xs.append(f(xs[-1]))
    star = xs[-1]; conv = abs(f(star) - star) < 1e-9
    g = [a + (b-a)*i/2000 for i in range(2001)]; maps_in = all(a - 1e-9 <= f(x) <= b + 1e-9 for x in g)
    Lc = max(abs((f(x + 1e-6) - f(x - 1e-6))/2e-6) for x in g)
    seq = [x0]
    for _ in range(steps): seq.append(f(seq[-1]))
    if maps_in and Lc < 1 and conv:
        for n in range(steps+1): assert abs(seq[n] - star) <= Lc**n/(1-Lc)*abs(seq[1]-seq[0]) + 1e-9, "Banach a-priori bound violated"
        cap = f"f maps [{a:g},{b:g}] into itself, L = max|f'| = {Lc:.4f} < 1 ⇒ contraction: unique fixed point x* = {star:.6f}; bound |xₙ − x*| ≤ Lⁿ/(1−L)·|x₁−x₀| checked for n = 0…{steps} ✓"
    else:
        cap = f"NOT certified as a contraction on [{a:g},{b:g}] ({'does not map into itself' if not maps_in else f'L = {Lc:.3f} ≥ 1'}): Banach's theorem does not apply — iteration may still converge" + (f" (here it does: x* ≈ {star:.6f})" if conv else " (here it does not settle)")
    ymin, ymax = min(a, min(f(x) for x in g)), max(b, max(f(x) for x in g)); X, Y = view([(a, ymin), (b, ymax)], .06); o = []
    o.append(line_d(X, Y, (a, a), (b, b), "#888", 1.2) + '<polyline fill="none" stroke="#3b82f6" stroke-width="2" points="%s"/>' % " ".join(f"{X(x):.1f},{Y(f(x)):.1f}" for x in g[::10]))
    path = [(x0, 0)]
    for v in seq[:-1]: path += [(v, f(v)), (f(v), f(v))]
    o.append('<polyline fill="none" stroke="#f43f5e" stroke-width="1.4" points="%s"/>' % " ".join(f"{X(x):.1f},{Y(y):.1f}" for x, y in path))
    if conv: o.append(f'<circle cx="{X(star):.1f}" cy="{Y(star):.1f}" r="4.5" fill="#22c55e"/>')
    return wrap_svg(o, [f"y = {expr} (blue), y = x (grey), iteration from x₀ = {x0:g} (red)", cap])
