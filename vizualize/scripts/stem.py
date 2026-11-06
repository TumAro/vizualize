"""STEM pictures beyond pure maths (stdlib only). Numerics are RK4 / exact sums, each checked against a closed form or a conserved quantity.
  mv.py phase  pendulum|lotka|vanderpol|damped|saddle   or   phase "y" "-sin(x)" [R]      ODE phase portrait (equilibria classified, nullclines, RK4 checked)
  mv.py charges "1,-1,0;-1,1,0"        point charges q,x,y: field lines (−∇φ = E checked)
  mv.py projectile v0 angle_deg [k]    projectile (linear drag k): RK4 vs closed form, optimal angle
  mv.py dist normal 0 1 [a b] | binom n p [a b] | poisson lam [a b] | exp lam [a b] | uniform lo hi [a b]   pmf/pdf, mean/var and P(a<=X<=b) checked
  mv.py clt n                          sum of n dice: exact pmf vs normal approximation
  mv.py rlc R L C [V]  |  rc R C [V]   step response, poles, damping class (RK4 vs analytic)
  mv.py lens f do h                    thin lens: image from two principal rays = lens equation"""
import math, html
from base import *
from fa import view, clipline, line_d, txt, wrap_svg
C1, C2, C3, C4, C5 = "#3b82f6", "#f43f5e", "#22c55e", "#f59e0b", "#a855f7"
SAFE = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
def rk4(f, y, h, n):
    for _ in range(n):
        k1 = f(y); k2 = f([a + h/2*b for a, b in zip(y, k1)]); k3 = f([a + h/2*b for a, b in zip(y, k2)]); k4 = f([a + h*b for a, b in zip(y, k3)])
        y = [a + h/6*(b + 2*c + 2*d + e) for a, b, c, d, e in zip(y, k1, k2, k3, k4)]
    return y
def thin(pts, d):
    out = [pts[0]]
    for p in pts[1:-1]:
        if math.hypot(p[0] - out[-1][0], p[1] - out[-1][1]) >= d: out.append(p)
    return out + [pts[-1]] if len(pts) > 1 else out
def poly(pts, c, w=1.5, dash="", arrow=True, d=0):
    if d: pts = thin(pts, d)
    s = '<polyline fill="none" stroke="%s" stroke-width="%s"%s points="%s"/>' % (c, w, f' stroke-dasharray="{dash}"' if dash else "", " ".join(f"{x:.1f},{y:.1f}" for x, y in pts))
    if arrow and len(pts) > 6:
        (x1, y1), (x2, y2) = pts[len(pts)//2 - 1], pts[len(pts)//2 + 1]; n = math.hypot(x2-x1, y2-y1) or 1; ux, uy = (x2-x1)/n, (y2-y1)/n; mx, my = pts[len(pts)//2]
        s += f'<path d="M{mx+5*ux:.1f} {my+5*uy:.1f}L{mx-3*ux-3.5*uy:.1f} {my-3*uy+3.5*ux:.1f}L{mx-3*ux+3.5*uy:.1f} {my-3*uy-3.5*ux:.1f}z" fill="{c}"/>'
    return s
def finish(body, W, H, notes, wrapw=58):
    from fgroups import wrap
    ls = [l for n in notes for l in wrap(n, wrapw)]
    return svg(W, H + 14*len(ls) + 6, body + [T(8, H + 14*(k+1), html.escape(l, quote=False), "start", sz=11) for k, l in enumerate(ls)], "c")

# ---------- phase portraits ----------
PRE = {"pendulum": ("y", "-sin(x)", (-7, 7, -3.4, 3.4), "0.5*y*y-cos(x)", "H = y²/2 − cos x", [(0, a) for a in (.6, 1.2, 1.8, 2.3, 2.8)] + [(0, -a) for a in (1.2, 2.3)] + [(math.pi + .5, 0), (-math.pi - .5, 0)]),
       "lotka": ("x*(1-y)", "y*(x-1)", (0, 4, 0, 4), "x-log(x)+y-log(y)", "V = x − ln x + y − ln y", [(1.5, 1), (2, 1), (2.7, 1), (.5, .5), (3.5, 1), (1, .2), (1, 3)]),
       "vanderpol": ("y", "(1-x*x)*y-x", (-4, 4, -4, 4), None, None, [(.1, 0), (3, 3), (-3, -2), (2, 0), (0, 3.5), (-1, -1)]),
       "damped": ("y", "-x-0.3*y", (-3, 3, -3, 3), None, None, [(2.5, 0), (-2, 2), (0, -2.5), (1, 1), (-2.5, -.5)]),
       "saddle": ("x", "-y", (-3, 3, -3, 3), None, None, [(.2, 2.5), (-.2, 2.5), (.2, -2.5), (-.2, -2.5), (2.5, .2), (2.5, -.2), (-2.5, .2), (-2.5, -.2), (1, 1), (-1, -1)])}
def phase(a, b=None, R=3):
    if b is None or a in PRE and b not in ("",):
        key = a; assert key in PRE, "presets: " + " ".join(PRE); fxs, fys, box, inv, invs, seeds = PRE[key]; title = key
    else:
        fxs, fys, R = a, b, float(R); box = (-R, R, -R, R); inv = invs = None; title = f"x' = {a}, y' = {b}"
        seeds = [(.7*R*math.cos(2*math.pi*k/8), .7*R*math.sin(2*math.pi*k/8)) for k in range(8)] + [(.3*R*math.cos(2*math.pi*k/4 + .3), .3*R*math.sin(2*math.pi*k/4 + .3)) for k in range(4)]
    cx_, cy_ = compile(fxs, "f", "eval"), compile(fys, "f", "eval")
    F = lambda v: [eval(cx_, {"__builtins__": {}}, {**SAFE, "x": v[0], "y": v[1]}), eval(cy_, {"__builtins__": {}}, {**SAFE, "x": v[0], "y": v[1]})]
    x0, x1, y0, y1 = box; sc = min(368/(x1 - x0), 268/(y1 - y0)); X = lambda x: 210 + sc*(x - (x0 + x1)/2); Y = lambda y: 150 - sc*(y - (y0 + y1)/2)
    ins = lambda v: x0 <= v[0] <= x1 and y0 <= v[1] <= y1
    h = (x1 - x0)/400; trajs = []; drift = 0.0
    for s in seeds:
        for sign in (1, -1):
            v, path = list(s), [list(s)]
            for _ in range(900):
                try: v = rk4(F, v, sign*h, 1)
                except (ValueError, OverflowError, ZeroDivisionError): break
                if not ins(v) or not all(math.isfinite(c) for c in v): break
                path.append(list(v))
            trajs.append(path)
        if inv:
            I = lambda v: eval(compile(inv, "i", "eval"), {"__builtins__": {}}, {**SAFE, "x": v[0], "y": v[1]}); p = trajs[-1]; q = trajs[-2]
            for path in (p, q):
                if len(path) > 2: vals = [I(v) for v in path]; drift = max(drift, max(vals) - min(vals))
    for s in seeds[:4]:                                                       # RK4 self-convergence: step h vs h/2 over the same time
        v1 = rk4(F, list(s), h*2, 40); v2 = rk4(F, list(s), h, 80)
        if ins(v1) and ins(v2): assert math.dist(v1, v2) < 1e-5*(1 + math.hypot(*v1)), "RK4 not converged (step halving changes the result)"
    if inv: assert drift < 2e-3, f"conserved quantity drifts by {drift}"
    jac = lambda p: [[(F([p[0] + 1e-6, p[1]])[i] - F([p[0] - 1e-6, p[1]])[i])/2e-6 for i in range(2)] if False else [(F([p[0] + 1e-6*(j == 0), p[1] + 1e-6*(j == 1)])[i] - F([p[0] - 1e-6*(j == 0), p[1] - 1e-6*(j == 1)])[i])/2e-6 for j in range(2)] for i in range(2)]
    eq = []
    for i in range(7):
        for j in range(7):
            p = [x0 + (x1 - x0)*(i + .5)/7, y0 + (y1 - y0)*(j + .5)/7]
            try:
                for _ in range(40):
                    f_ = F(p); J = jac(p); d = J[0][0]*J[1][1] - J[0][1]*J[1][0]
                    if abs(d) < 1e-12: break
                    p = [p[0] - (f_[0]*J[1][1] - f_[1]*J[0][1])/d, p[1] - (J[0][0]*f_[1] - J[1][0]*f_[0])/d]
            except (ValueError, OverflowError, ZeroDivisionError): continue
            if ins(p) and max(abs(c) for c in F(p)) < 1e-9 and all(math.dist(p, q) > 1e-5 for q in eq): eq.append(p)
    notes = []; marks = []
    for p in eq:
        J = jac(p); tr, det = J[0][0] + J[1][1], J[0][0]*J[1][1] - J[0][1]*J[1][0]; disc = tr*tr - 4*det
        kind, col = ("saddle", C2) if det < -1e-9 else (("centre (linear)" if abs(tr) < 1e-6 else ("stable spiral" if tr < 0 else "unstable spiral")), C5) if disc < -1e-9 and abs(det) > 1e-9 else (("stable node" if tr < 0 else "unstable node"), C3 if tr < 0 else C4) if det > 1e-9 else ("non-hyperbolic", "#888")
        if kind.startswith("stable") or kind.startswith("unstable"):                           # certify by simulation near the point
            d0 = 0.02; T_ = 6/max(1e-3, abs(tr/2)) if abs(tr) > 1e-6 else 6; q = rk4(F, [p[0] + d0, p[1]], T_/2000*0.5, 2000)
            if all(math.isfinite(c) for c in q): assert (math.dist(q, p) < d0) == kind.startswith("stable"), f"classification of {kind} at {p} contradicts simulation"
        marks.append((p, kind, col)); notes.append(f"({p[0]:.3g}, {p[1]:.3g}): {kind} (tr {tr:.3g}, det {det:.3g})")
    o = [f'<clipPath id="pc"><rect x="{X(x0):.0f}" y="{Y(y1):.0f}" width="{X(x1)-X(x0):.0f}" height="{Y(y0)-Y(y1):.0f}"/></clipPath><rect x="{X(x0):.0f}" y="{Y(y1):.0f}" width="{X(x1)-X(x0):.0f}" height="{Y(y0)-Y(y1):.0f}" fill="none" stroke="#888"/>', '<g clip-path="url(#pc)">']
    if x0 <= 0 <= x1: o.append(f'<line x1="{X(0):.0f}" y1="{Y(y0):.0f}" x2="{X(0):.0f}" y2="{Y(y1):.0f}" stroke="#888" stroke-width=".6"/>')
    if y0 <= 0 <= y1: o.append(f'<line x1="{X(x0):.0f}" y1="{Y(0):.0f}" x2="{X(x1):.0f}" y2="{Y(0):.0f}" stroke="#888" stroke-width=".6"/>')
    N = 20; gx = [x0 + (x1 - x0)*i/N for i in range(N+1)]; gy = [y0 + (y1 - y0)*j/N for j in range(N+1)]
    for k, col in ((0, C4), (1, C5)):                                           # nullclines by marching squares
        Z = [[F([x, y])[k] for x in gx] for y in gy]; d = []
        for j in range(N):
            for i in range(N):
                pts = []
                for (a, b, c_, e) in ((i, j, i+1, j), (i+1, j, i+1, j+1), (i, j+1, i+1, j+1), (i, j, i, j+1)):
                    za, zb = Z[b][a], Z[e][c_]
                    if za*zb < 0: t = za/(za - zb); pts.append((gx[a] + t*(gx[c_] - gx[a]), gy[b] + t*(gy[e] - gy[b])))
                if len(pts) >= 2 and (round(X(pts[0][0])), round(Y(pts[0][1]))) != (round(X(pts[1][0])), round(Y(pts[1][1]))): d.append(f"M{X(pts[0][0]):.0f} {Y(pts[0][1]):.0f}L{X(pts[1][0]):.0f} {Y(pts[1][1]):.0f}")
        if d: o.append(f'<path d="{"".join(d)}" fill="none" stroke="{col}" stroke-width="1" stroke-dasharray="3 3" opacity=".8"/>')
    for i in range(0, len(trajs), 2):                                         # backward (reversed) + forward = one oriented curve per seed
        full = trajs[i + 1][::-1] + trajs[i][1:]
        if len(full) > 3: o.append(poly([(X(a), Y(b)) for a, b in full], C1, 1.3, "", True, 13))
    if title == "pendulum":
        sep = [(x, 2*math.cos(x/2)) for x in [-math.pi*2 + 4*math.pi*i/160 for i in range(161)]]; assert all(abs(0.5*y*y - math.cos(x) - 1) < 1e-9 for x, y in sep)
        o.append(poly([(X(a), Y(b)) for a, b in sep], C2, 1.8, "6 3", False, 7) + poly([(X(a), Y(-b)) for a, b in sep], C2, 1.8, "6 3", False, 7))
    for p, kind, col in marks: o.append(f'<circle cx="{X(p[0]):.1f}" cy="{Y(p[1]):.1f}" r="4.5" fill="{col}" stroke="#fff" stroke-width="1"/>')
    o.append("</g>")
    extra = [f"{title}: blue = RK4 trajectories (forward and backward), orange / purple dashed = nullclines x' = 0 / y' = 0, dots = equilibria (Jacobian trace/determinant)"] + notes[:6]
    if title == "pendulum": extra.append("red dashed = separatrix H = 1 (checked): inside, oscillation; outside, rotation")
    extra.append("RK4 step-halving agreement ✓" + (f"; {invs} conserved to {drift:.1e} along every orbit ✓" if inv else "; no conserved quantity claimed") + "; each node/spiral classification confirmed by simulation ✓")
    return finish(o, 420, 306, extra)

# ---------- electrostatics ----------
def charges(spec):
    Q = [tuple(float(v) for v in t.split(",")) for t in spec.split(";") if t.strip()]; assert 1 <= len(Q) <= 6 and all(q != 0 for q, *_ in Q)
    def E(p):
        ex = ey = 0.0
        for q, a, b in Q: dx, dy = p[0] - a, p[1] - b; r3 = (dx*dx + dy*dy)**1.5 + 1e-18; ex += q*dx/r3; ey += q*dy/r3
        return [ex, ey]
    phi = lambda p: sum(q/(math.hypot(p[0] - a, p[1] - b) + 1e-12) for q, a, b in Q)
    for p in ((.37, 1.21), (-1.3, .4), (2.2, -1.7), (.05, .8), (3.1, 2.4)):               # E = −∇φ
        g = [-(phi([p[0] + 1e-6, p[1]]) - phi([p[0] - 1e-6, p[1]]))/2e-6, -(phi([p[0], p[1] + 1e-6]) - phi([p[0], p[1] - 1e-6]))/2e-6]; e = E(p)
        if all(math.hypot(p[0] - a, p[1] - b) > .1 for _, a, b in Q): assert math.dist(g, e) < 1e-5*(1 + math.hypot(*e)), "E ≠ −∇φ"
    Qt = sum(q for q, *_ in Q); far = 200.0; ef = E([far, 0.0])
    if abs(Qt) > 1e-9: assert abs(math.hypot(*ef)*far**2/abs(Qt) - 1) < 0.02, "far field is not the monopole field of the total charge"
    xs = [a for _, a, _ in Q]; ys = [b for _, _, b in Q]; pad = 2.2; bx = (min(xs) - pad, max(xs) + pad, min(ys) - pad*.9, max(ys) + pad*.9)
    sc = min(368/(bx[1] - bx[0]), 268/(bx[3] - bx[2])); X = lambda x: 210 + sc*(x - (bx[0] + bx[1])/2); Y = lambda y: 150 - sc*(y - (bx[2] + bx[3])/2)
    qmax = max(abs(q) for q, *_ in Q); lines = []; pos = [c for c in Q if c[0] > 0] or [c for c in Q if c[0] < 0]; sgn = 1 if any(c[0] > 0 for c in Q) else -1
    for q, a, b in pos:
        n = max(4, round(10*abs(q)/qmax))
        for k in range(n):
            t = 2*math.pi*(k + .5)/n; p = [a + .12*math.cos(t), b + .12*math.sin(t)]; path = [list(p)]
            for _ in range(500):
                e = E(p); nrm = math.hypot(*e); f = lambda v: (lambda ee: [sgn*ee[0]/math.hypot(*ee), sgn*ee[1]/math.hypot(*ee)])(E(v))
                p = rk4(f, p, .12, 1); path.append(list(p))
                if p[0] < bx[0] or p[0] > bx[1] or p[1] < bx[2] or p[1] > bx[3] or any(math.hypot(p[0] - c, p[1] - d) < .14 for _, c, d in Q if not (c == a and d == b and len(path) < 4)): break
            lines.append(path)
    o = [f'<clipPath id="ec"><rect x="{X(bx[0]):.0f}" y="{Y(bx[3]):.0f}" width="{X(bx[1])-X(bx[0]):.0f}" height="{Y(bx[2])-Y(bx[3]):.0f}"/></clipPath><g clip-path="url(#ec)">']
    o += [poly([(X(a), Y(b)) for a, b in path], "#888", 1.2) for path in lines]; o.append("</g>")
    for q, a, b in Q: o.append(f'<circle cx="{X(a):.1f}" cy="{Y(b):.1f}" r="{7 + 3*abs(q)/qmax:.1f}" fill="{C2 if q > 0 else C1}"/>' + T(X(a), Y(b) + 4, "+" if q > 0 else "−", sz=12, c="#fff"))
    return finish(o, 420, 306, [f"charges {[(q, a, b) for q, a, b in Q]}; field lines leave + and end on −; line count ∝ |q|", "E = −∇φ verified by finite differences at 5 points ✓" + (f"; far field ≈ monopole of total charge {Qt:g} (within 2%) ✓" if abs(Qt) > 1e-9 else "; total charge 0: far field falls faster than 1/r² (dipole or higher)"), "3D point charges, field drawn in the plane through them"])

# ---------- projectile ----------
def projectile(v0, ang, k=0.0):
    v0, ang, k = float(v0), float(ang), float(k); g = 9.81; th = math.radians(ang); vx, vy = v0*math.cos(th), v0*math.sin(th)
    def exact(t):
        if k == 0: return vx*t, vy*t - g*t*t/2
        return vx*(1 - math.exp(-k*t))/k, (vy + g/k)*(1 - math.exp(-k*t))/k - g*t/k
    def run(th_, dt=1e-3):
        s = [0.0, 0.0, v0*math.cos(th_), v0*math.sin(th_)]; pts = [(0.0, 0.0)]; t = 0.0
        F = lambda v: [v[2], v[3], -k*v[2], -g - k*v[3]]
        while True:
            n = rk4(F, s, dt, 1)
            if n[1] < 0: f = s[1]/(s[1] - n[1]); pts.append((s[0] + f*(n[0] - s[0]), 0.0)); return pts, t + f*dt
            s = n; t += dt
            if int(t/dt) % 20 == 0: pts.append((s[0], s[1]))
    pts, T_ = run(th); R = pts[-1][0]; ex, ey = exact(T_)
    assert abs(ey) < 1e-2 * (1 + v0) and abs(ex - R) < 1e-3*(1 + R), "RK4 and closed form disagree"
    H = max(p[1] for p in pts)
    if k == 0:
        assert abs(R - v0**2*math.sin(2*th)/g) < 2e-3*(1 + R) and abs(T_ - 2*vy/g) < 2e-3 and abs(H - vy**2/(2*g)) < 2e-3*(1 + H)
    best = max(range(5, 86), key=lambda a: run(math.radians(a), 2e-3)[0][-1][0])
    if k == 0: assert abs(best - 45) <= 1, "optimal angle should be 45° without drag"
    fam = [run(math.radians(a), 2e-3)[0] for a in (15, 30, 45, 60, 75)]; xs = [p[0] for tr in fam + [pts] for p in tr]; ys = [p[1] for tr in fam + [pts] for p in tr]
    sc = min(370/max(xs), 250/max(ys)); X = lambda x: 25 + sc*x; Y = lambda y: 280 - sc*y
    o = [f'<line x1="25" y1="280" x2="400" y2="280" stroke="#888"/>'] + [poly([(X(a), Y(b)) for a, b in tr[::3]], "#888", 1, "", False) for tr in fam] + [poly([(X(a), Y(b)) for a, b in pts[::2]], C2, 2.2)]
    o += [txt(X, Y, 0, 0, "", "middle")] if False else []
    return finish(o, 420, 290, [f"v₀ = {v0:g} m/s at {ang:g}°" + (f", linear drag k = {k:g} s⁻¹" if k else ", no drag") + f": range {R:.2f} m, apex {H:.2f} m, flight time {T_:.3f} s (red); grey = 15°, 30°, 45°, 60°, 75°", "RK4 landing point equals the closed form" + (" and the textbook formulas R = v²sin2θ/g, H = (v sinθ)²/2g, T = 2v sinθ/g ✓" if k == 0 else " (exponential-decay solution) ✓"), f"scanned optimal launch angle (max range) = {best}°" + (" ✓" if k == 0 else " — drag pushes it below 45°")])

# ---------- probability ----------
def Phi(x): return 0.5*(1 + math.erf(x/math.sqrt(2)))
def dist(kind, *a):
    a = [float(x) for x in a]; lo = hi = None
    if kind == "normal": mu, sg, *r = a; assert sg > 0; f = lambda x: math.exp(-(x-mu)**2/(2*sg*sg))/(sg*math.sqrt(2*math.pi)); xs = [mu - 4.5*sg + 9*sg*i/400 for i in range(401)]; mean, var = mu, sg*sg; cdf = lambda x: Phi((x - mu)/sg); disc = False
    elif kind == "exp": lam, *r = a; assert lam > 0; f = lambda x: lam*math.exp(-lam*x) if x >= 0 else 0.0; xs = [13/lam*i/400 for i in range(401)]; mean, var = 1/lam, 1/lam**2; cdf = lambda x: 1 - math.exp(-lam*x) if x > 0 else 0.0; disc = False
    elif kind == "uniform": u0, u1, *r = a; assert u1 > u0; f = lambda x: 1/(u1-u0) if u0 <= x <= u1 else 0.0; xs = [u0 - .2*(u1-u0) + 1.4*(u1-u0)*i/400 for i in range(401)]; mean, var = (u0+u1)/2, (u1-u0)**2/12; cdf = lambda x: min(1, max(0, (x-u0)/(u1-u0))); disc = False
    elif kind == "binom": n, p, *r = a; n = int(n); assert 0 < p < 1; f = lambda k: math.comb(n, int(k))*p**k*(1-p)**(n-k); xs = list(range(n+1)); mean, var = n*p, n*p*(1-p); disc = True
    elif kind == "poisson": lam, *r = a; assert lam > 0; f = lambda k: math.exp(-lam)*lam**int(k)/math.factorial(int(k)); xs = list(range(int(lam + 6*math.sqrt(lam) + 6))); mean, var = lam, lam; disc = True
    else: raise SystemExit("dist: normal | binom | poisson | exp | uniform")
    lo, hi = (r[0], r[1]) if len(r) >= 2 else (mean - math.sqrt(var), mean + math.sqrt(var))
    if disc:
        pm = [f(k) for k in xs]; tot = sum(pm); m = sum(k*p for k, p in zip(xs, pm)); v = sum((k - m)**2*p for k, p in zip(xs, pm)); Pab = sum(p for k, p in zip(xs, pm) if lo <= k <= hi)
        assert abs(tot - 1) < 1e-9 + (1e-6 if kind == "poisson" else 0) and abs(m - mean) < 1e-6*(1 + mean) and abs(v - var) < 1e-4*(1 + var)
    else:
        n = 4000; a0, a1 = xs[0], xs[-1]; h = (a1 - a0)/n; fx = [f(a0 + i*h) for i in range(n+1)]; tot = h/3*(fx[0] + fx[-1] + 4*sum(fx[1:-1:2]) + 2*sum(fx[2:-1:2]))
        m = h/3*sum(w*(a0 + i*h)*fx[i] for i, w in enumerate([1] + [4 if i % 2 else 2 for i in range(1, n)] + [1])); v = h/3*sum(w*((a0 + i*h) - m)**2*fx[i] for i, w in enumerate([1] + [4 if i % 2 else 2 for i in range(1, n)] + [1]))
        l2, h2 = max(lo, a0), min(hi, a1); nn = 2000; hh = (h2 - l2)/nn if h2 > l2 else 0; Pab = hh/3*(f(l2) + f(h2) + 4*sum(f(l2 + i*hh) for i in range(1, nn, 2)) + 2*sum(f(l2 + i*hh) for i in range(2, nn, 2))) if hh else 0.0
        assert abs(tot - 1) < 2e-3 and abs(m - mean) < 5e-3*(1 + abs(mean)) and abs(v - var) < 5e-3*(1 + var) and abs(Pab - (cdf(hi) - cdf(lo))) < 2e-3, "numerics disagree with closed form"
    ys = [f(x) for x in xs]; ymax = max(ys)*1.1; xa, xb = xs[0] - (.5 if disc else 0), xs[-1] + (.5 if disc else 0)
    X = lambda x: 30 + 360*(x - xa)/(xb - xa); Y = lambda y: 250 - 215*y/ymax; o = ['<line x1="30" y1="250" x2="390" y2="250" stroke="#888"/>']
    if disc:
        w = max(1.5, 360/(xb - xa)*.8)
        for x, y in zip(xs, ys): o.append(f'<rect x="{X(x)-w/2:.1f}" y="{Y(y):.1f}" width="{w:.1f}" height="{250-Y(y):.1f}" fill="{C2 + "aa" if lo <= x <= hi else C1 + "55"}"/>')
    else:
        sh = [(X(x), Y(f(x))) for x in xs if lo <= x <= hi]
        if len(sh) > 1: o.append('<polygon fill="%s33" points="%s"/>' % (C2, f"{sh[0][0]:.1f},250 " + " ".join(f"{a:.1f},{b:.1f}" for a, b in sh) + f" {sh[-1][0]:.1f},250"))
        o.append(poly([(X(x), Y(y)) for x, y in zip(xs, ys)][::3], C1, 2, "", False))
    o.append(f'<line x1="{X(mean):.1f}" y1="{Y(ymax*.95):.1f}" x2="{X(mean):.1f}" y2="250" stroke="{C3}" stroke-dasharray="4 3"/>')
    for x in (xs[0], xs[len(xs)//2], xs[-1]): o.append(T(X(x), 266, f"{x:.3g}", sz=11, c="#888"))
    return finish(o, 420, 270, [f"{kind}({', '.join(f'{x:g}' for x in a[:2 if kind in ('normal','binom','uniform') else 1])}): mean {mean:.4g}, variance {var:.4g}; green dashed = mean; P({lo:.4g} ≤ X ≤ {hi:.4g}) = {Pab:.5f} (red)", f"total probability = {tot:.6f} ✓; mean and variance recomputed from the {'pmf' if disc else 'density (Simpson)'} match the formulas ✓" + ("; P(a≤X≤b) = F(b) − F(a) with the closed-form CDF ✓" if not disc else "")])
def clt(n):
    n = int(n); assert 1 <= n <= 40; pm = {0: 1.0}
    for _ in range(n):
        new = {}
        for s, p in pm.items():
            for d in range(1, 7): new[s + d] = new.get(s + d, 0) + p/6
        pm = new
    ks = sorted(pm); tot = sum(pm.values()); m = sum(k*p for k, p in pm.items()); v = sum((k - m)**2*p for k, p in pm.items())
    assert abs(tot - 1) < 1e-9 and abs(m - 3.5*n) < 1e-9 and abs(v - 35*n/12) < 1e-8, "convolution moments disagree with n·(7/2), n·(35/12)"
    mu, sg = 3.5*n, math.sqrt(35*n/12); phi = lambda x: math.exp(-(x - mu)**2/(2*sg*sg))/(sg*math.sqrt(2*math.pi)); err = max(abs(pm[k] - phi(k)) for k in ks); ymax = max(max(pm.values()), phi(mu))*1.1
    ks_dist = max(abs(sum(p for j, p in pm.items() if j <= k) - Phi((k + .5 - mu)/sg)) for k in ks)
    xa, xb = ks[0] - .5, ks[-1] + .5; X = lambda x: 30 + 360*(x - xa)/(xb - xa); Y = lambda y: 250 - 215*y/ymax; w = max(1.2, 360/(xb - xa)*.85)
    o = ['<line x1="30" y1="250" x2="390" y2="250" stroke="#888"/>'] + [f'<rect x="{X(k)-w/2:.1f}" y="{Y(pm[k]):.1f}" width="{w:.1f}" height="{250-Y(pm[k]):.1f}" fill="{C1}66"/>' for k in ks]
    o.append(poly([(X(x), Y(phi(x))) for x in [xa + (xb - xa)*i/120 for i in range(121)]], C2, 2, "", False))
    return finish(o, 420, 270, [f"sum of {n} fair dice: exact distribution by convolution (bars) vs normal(μ = {mu:g}, σ = {sg:.4f}) (red)", f"mean and variance equal n·7/2 and n·35/12 exactly ✓; max |pmf − density| = {err:.5f}; max CDF gap (continuity-corrected) = {ks_dist:.5f} — shrinks like 1/√n as n grows (central limit theorem)"])

# ---------- circuits ----------
def rlc(R, L, Cc, V=1.0):
    R, L, Cc, V = map(float, (R, L, Cc, V)); assert min(R, L, Cc) > 0; al = R/(2*L); w0 = 1/math.sqrt(L*Cc); d = al*al - w0*w0
    if abs(d) < 1e-9*w0*w0: cls = "critically damped"; s = [complex(-al, 0)]*2
    elif d < 0: cls = "underdamped"; wd = math.sqrt(-d); s = [complex(-al, wd), complex(-al, -wd)]
    else: cls = "overdamped"; r = math.sqrt(d); s = [complex(-al + r, 0), complex(-al - r, 0)]
    def exact(t):
        if cls == "underdamped": return V*(1 - math.exp(-al*t)*(math.cos(wd*t) + al/wd*math.sin(wd*t)))
        if cls == "critically damped": return V*(1 - math.exp(-al*t)*(1 + al*t))
        s1, s2 = s[0].real, s[1].real; return V*(1 + (s2*math.exp(s1*t) - s1*math.exp(s2*t))/(s1 - s2))
    tmax = (6/al if cls != "overdamped" else 6/abs(s[0].real)) if al > 0 else 10/w0; F = lambda y: [y[1], (V - y[0])/(L*Cc) - R/L*y[1]]
    n = 600; h = tmax/n; y = [0.0, 0.0]; pts = []
    for i in range(n+1):
        t = i*h; pts.append((t, y[0])); 
        if i % 100 == 0: assert abs(y[0] - exact(t)) < 1e-6*(1 + V), f"RK4 vs closed form at t={t}"
        y = rk4(F, y, h, 1)
    ys = [p[1] for p in pts]; ymax = max(ys)*1.15; X = lambda t: 30 + 200*t/tmax; Y = lambda v: 160 - 130*v/ymax
    o = [f'<line x1="30" y1="160" x2="230" y2="160" stroke="#888"/><line x1="30" y1="30" x2="30" y2="165" stroke="#888"/>', f'<line x1="30" y1="{Y(V):.1f}" x2="230" y2="{Y(V):.1f}" stroke="{C3}" stroke-dasharray="4 3"/>', poly([(X(t), Y(v)) for t, v in pts][::6], C1, 2, "", False)]
    if cls == "underdamped": o += [poly([(X(t), Y(V*(1 + math.exp(-al*t)))) for t, _ in pts][::12], "#888", 1, "3 3", False), poly([(X(t), Y(V*(1 - math.exp(-al*t)))) for t, _ in pts][::12], "#888", 1, "3 3", False)]
    sx = 260; sc = 55/max(abs(z.real) for z in s + [complex(-w0)]) if True else 1; cxp, cyp = 330, 95; scl = 70/max(w0, abs(s[0].real), abs(s[0].imag), 1e-9)
    o += [f'<line x1="{sx}" y1="{cyp}" x2="410" y2="{cyp}" stroke="#888"/><line x1="{cxp}" y1="30" x2="{cxp}" y2="160" stroke="#888"/>', f'<circle cx="{cxp}" cy="{cyp}" r="{w0*scl:.1f}" fill="none" stroke="#888" stroke-dasharray="3 3"/>'] + [f'<path d="M{cxp + z.real*scl - 4:.1f} {cyp - z.imag*scl - 4:.1f}l8 8m0 -8l-8 8" stroke="{C2}" stroke-width="2.2"/>' for z in s]
    o += [T(130, 20, "v_C(t) (step input)", sz=11), T(340, 20, "poles in the s-plane", sz=11)]
    return finish(o, 420, 175, [f"series RLC, R = {R:g} Ω, L = {L:g} H, C = {Cc:g} F, step V = {V:g}: {cls}; α = R/2L = {al:.4g}, ω₀ = 1/√(LC) = {w0:.4g}" + (f", ω_d = {wd:.4g}" if cls == "underdamped" else ""), "poles s = " + ", ".join(f"{z.real:.4g}{z.imag:+.4g}i" if z.imag else f"{z.real:.4g}" for z in s) + "; RK4 solution equals the closed form at 7 times ✓; dashed circle |s| = ω₀"])
def rc(R, Cc, V=1.0):
    R, Cc, V = map(float, (R, Cc, V)); tau = R*Cc; F = lambda y: [(V - y[0])/tau]; y = [0.0]; n = 500; h = 5*tau/n; pts = []
    for i in range(n+1):
        t = i*h; pts.append((t, y[0])); assert abs(y[0] - V*(1 - math.exp(-t/tau))) < 1e-8*V; y = rk4(F, y, h, 1)
    X = lambda t: 30 + 360*t/(5*tau); Yv = lambda v: 220 - 190*v/V
    o = ['<line x1="30" y1="220" x2="390" y2="220" stroke="#888"/><line x1="30" y1="25" x2="30" y2="225" stroke="#888"/>', f'<line x1="30" y1="{Yv(V):.1f}" x2="390" y2="{Yv(V):.1f}" stroke="{C3}" stroke-dasharray="4 3"/>', poly([(X(t), Yv(v)) for t, v in pts][::8], C1, 2, "", False), poly([(X(t), Yv(V - v)) for t, v in pts][::8], C2, 2, "4 3", False),
         f'<circle cx="{X(tau):.1f}" cy="{Yv(V*(1 - math.exp(-1))):.1f}" r="4" fill="{C4}"/>', T(X(tau) + 6, Yv(V*(1 - math.exp(-1))) + 14, "t = τ: 63.2 %", "start", C4, 11)]
    return finish(o, 420, 235, [f"RC: R = {R:g} Ω, C = {Cc:g} F, τ = RC = {tau:g} s; blue = charging v_C = V(1 − e^(−t/τ)), red dashed = discharging", "RK4 equals the closed form at all 501 points (≤ 1e-8·V) ✓; at t = τ the capacitor reaches 1 − 1/e = 63.2 % ✓; after 5τ: 99.3 %"])

# ---------- thin lens ----------
def lens(f, do, h):
    f, do, h = float(f), float(do), float(h); assert do > 0 and f != 0 and h != 0 and abs(do - f) > 1e-9 or False, "object at the focal point: image at infinity"
    sg = 1 if f > 0 else -1; d = (sg*f, -sg*h)                                     # refracted principal ray direction from (0,h)
    # intersect  (0,h)+t*d  with  s*(do,-h)  (ray through the centre, unrefracted)
    A = [[d[0], -do], [d[1], h]]; det = A[0][0]*A[1][1] - A[0][1]*A[1][0]; rhs = [0.0, -h]
    t = (rhs[0]*A[1][1] - A[0][1]*rhs[1])/det; sx = (A[0][0]*rhs[1] - A[1][0]*rhs[0])/det; xi, yi = sx*do, -sx*h
    assert abs(1/do + 1/xi - 1/f) < 1e-9 and abs(yi/h + xi/do) < 1e-9, "ray construction disagrees with 1/f = 1/d_o + 1/d_i"
    real = xi > 0; xs = [-do, xi, f, -f, 0.0]; span = max(abs(v) for v in xs)*1.15; ys = max(abs(h), abs(yi))*1.6
    sc = min(190/span, 130/ys); X = lambda x: 210 + sc*x; Y = lambda y: 160 - sc*y; o = [f'<line x1="10" y1="160" x2="410" y2="160" stroke="#888"/>', f'<line x1="{X(0):.1f}" y1="{Y(ys):.1f}" x2="{X(0):.1f}" y2="{Y(-ys):.1f}" stroke="{C1}" stroke-width="2.5"/>']
    for fp in (f, -f): o.append(f'<circle cx="{X(fp):.1f}" cy="160" r="3" fill="#888"/>' + T(X(fp), 176, "F", sz=11, c="#888"))
    o.append(line_d(X, Y, (-do, 0), (-do, h), C2, 3, "", True)); o.append(line_d(X, Y, (xi, 0), (xi, yi), C3, 3, "" if real else "4 3", True))
    R_ = span*1.0
    o += [line_d(X, Y, (-do, h), (0, h), C4, 1.5), line_d(X, Y, (0, h), (d[0]/abs(d[0])*R_ if xi > 0 else R_, h + d[1]/d[0]*(d[0]/abs(d[0])*R_ if xi > 0 else R_)), C4, 1.5), line_d(X, Y, (-do, h), (R_*(1 if xi > 0 else 1), -h*R_/do), C5, 1.5)]
    if not real: o += [line_d(X, Y, (0, h), (xi, yi), C4, 1, "3 3"), line_d(X, Y, (0, 0), (xi, yi), C5, 1, "3 3")]
    return finish(o, 420, 190, [f"thin lens f = {f:g} ({'converging' if f > 0 else 'diverging'}), object distance {do:g}, height {h:g}: image at {xi:.4g} (" + ("real, inverted" if real and yi*h < 0 else "virtual, upright") + f"), height {yi:.4g}, magnification {yi/h:.4g}", "image found only from two principal rays (parallel→focus, through the centre) and then checked: 1/f = 1/dₒ + 1/dᵢ ✓ and m = hᵢ/hₒ = −dᵢ/dₒ ✓"])
