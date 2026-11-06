#!/usr/bin/env python3
"""vizualize generators: deterministic, self-checking SVG. stdlib only, <50ms each.
  mv.py cayley  C6|D4|A4|S3 [sub=GEN,..]   Cayley graph (+ colour left cosets of <sub>, checks normality)
  mv.py hasse   D4|S3|A4|C12|S4            subgroup lattice (normal subgroups bold)
  mv.py plot    "sin(x)/x" xmin xmax [ymin ymax]
  mv.py conformal "z**2" [xmin xmax ymin ymax]   image of a grid under f(z)
  mv.py lp      [p ...]                    unit balls of l^p in R^2
  mv.py dijkstra "A-B:4,A-C:1,C-B:2" A     frame strip with real distances
  mv.py domain "f(z)" [R=2] | residue "f(z)" cx cy r | mobius a b c d | riemann z.. | julia [re im]   complex analysis (see cplx.py)
  mv.py separate|extension|riesz|dual|project|fourier|cobweb ...   analysis / functional analysis (see fa.py)
  mv.py linmap|basis|solid|surface|ga|triangle ...   linear algebra & geometry (see la.py)
  mv.py bfs|dfs|prim|kruskal|maxflow|proofdag|comm|dfa ...   graphs, algorithms, proofs, automata (see graphs.py)
  mv.py phase|charges|projectile|dist|clt|rlc|rc|lens ...   STEM: ODE phase portraits, fields, kinematics, probability, circuits, optics (see stem.py)
  mv.py quotient D4 sub=r2                 Cayley graph of G/N itself (well-definedness asserted)
  mv.py galois x^3-2|x^4-2|cyclo12|..   Galois correspondence lattice (subgroups <-> fixed fields)
  mv.py ideals 12                       ideal lattice of Z_n with quotients
  add --widget to any command: claude.ai inline-widget fragment (theme vars, lint-checked)
  mv.py slider  list|pythagoras|quadratic|sine|taylor|epsdelta|eigen|riemann   interactive HTML (offline, self-checking)
All output is a self-contained <svg> using currentColor; paste it inline."""
import sys, math, cmath
from itertools import product
from base import *
from fgroups import cayley, hasse, quotient, mul, idn, closure, order
# ---------- plot / conformal / lp ----------
SAFE = {k: getattr(math, k) for k in dir(math) if not k.startswith("_")}
def f1(expr):
    code = compile(expr, "f", "eval")
    return lambda x: eval(code, {"__builtins__": {}}, {**SAFE, "x": x, "abs": abs})
def plot(expr, x0, x1, y0=None, y1=None):
    f = f1(expr); N = 160; xs = [x0 + (x1-x0)*i/N for i in range(N+1)]; ys = []
    for x in xs:
        try: y = f(x); ys.append(y if isinstance(y, float) and math.isfinite(y) else None)
        except Exception: ys.append(None)
    fin = [y for y in ys if y is not None]
    if y0 is None: y0, y1 = min(fin), max(fin); pad = (y1-y0)*.08 or 1; y0, y1 = y0-pad, y1+pad
    W, H, m = 420, 300, 30
    X = lambda x: m + (W-2*m)*(x-x0)/(x1-x0); Y = lambda y: H-m - (H-2*m)*(y-y0)/(y1-y0)
    out = []
    if x0 <= 0 <= x1: out.append(L(X(0), m, X(0), H-m))
    if y0 <= 0 <= y1: out.append(L(m, Y(0), W-m, Y(0)))
    segs, cur = [], []
    for x, y in zip(xs, ys):
        if y is None or not (y0 <= y <= y1):
            if cur: segs.append(cur); cur = []
        else: cur.append(f"{X(x):.1f},{Y(y):.1f}")
    if cur: segs.append(cur)
    out += [f'<polyline points="{" ".join(s)}" fill="none" stroke="#27c" stroke-width="2"/>' for s in segs if len(s) > 1]
    out += [T(m, H-10, f"{x0:g}", "start", sz=10), T(W-m, H-10, f"{x1:g}", "end", sz=10), T(W/2, 16, f"y = {expr}", sz=12)]
    return svg(W, H, out)
def conformal(expr, x0=-2, x1=2, y0=-2, y1=2, K=6, P=24):
    code = compile(expr, "f", "eval"); env = {**{k: getattr(cmath, k) for k in dir(cmath) if not k.startswith("_")}}
    f = lambda z: eval(code, {"__builtins__": {}}, {**env, "z": z})
    def img(pts):
        out = []
        for z in pts:
            try: out.append(f(z))
            except Exception: out.append(None)
        return out
    lines = []
    for i in range(K+1):
        x = x0 + (x1-x0)*i/K; y = y0 + (y1-y0)*i/K
        lines.append(("v", [complex(x, y0+(y1-y0)*j/P) for j in range(P+1)]))
        lines.append(("h", [complex(x0+(x1-x0)*j/P, y) for j in range(P+1)]))
    imgs = [(k, img(p)) for k, p in lines]
    allv = [w for _, ws in imgs for w in ws if w is not None and abs(w) < 1e3]
    R = max(max(abs(w.real) for w in allv), max(abs(w.imag) for w in allv), 1e-9) * 1.05
    def box(ox, data, title, flat=False):
        s = [f'<rect x="{ox}" y="10" width="200" height="200" fill="none" stroke="#bbb"/>', T(ox+100, 226, title, sz=11)]
        for k, ws in data:
            ws = [ws[0], ws[-1]] if flat else ws
            pts = [f"{ox+100+100*w.real/Rr:.1f},{110-100*w.imag/Rr:.1f}" for w in ws if w is not None and abs(w) < 1e3]
            s.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{C[1] if k=="v" else C[0]}" stroke-width="1.2"/>')
        return s
    Rr = max(abs(x0), abs(x1), abs(y0), abs(y1)); a = box(5, [(k, ws) for (k, ws) in lines], "z-plane", True)
    Rr = R; b = box(215, imgs, f"w = {expr}")
    return svg(420, 235, a + b + [L(5, 110, 205, 110, "#ccc", .8), L(105, 10, 105, 210, "#ccc", .8), L(215, 110, 415, 110, "#ccc", .8), L(315, 10, 315, 210, "#ccc", .8)])
def lp(ps):
    out = [L(10, 150, 290, 150), L(150, 10, 150, 290)]; k = 120
    for i, p in enumerate(ps):
        pts = []
        if p == math.inf: pts = [f"{150+k*x:.1f},{150-k*y:.1f}" for x, y in ((1,1),(-1,1),(-1,-1),(1,-1),(1,1))]
        for j in range(201 if p != math.inf else 0):
            t = 2*math.pi*j/200; c, s = math.cos(t), math.sin(t)
            x = math.copysign(abs(c)**(2/p), c); y = math.copysign(abs(s)**(2/p), s)
            assert abs(abs(x)**p + abs(y)**p - 1) < 1e-9
            pts.append(f"{150+k*x:.1f},{150-k*y:.1f}")
        out.append(f'<polyline points="{" ".join(pts)}" fill="none" stroke="{C[i%5]}" stroke-width="2"/>')
        out.append(T(300, 40+18*i, f"p={p:g}".replace("inf","∞") + ("  (not convex: not a norm)" if p < 1 else ""), "start", C[i % 5], 12))
    out.append(T(150+k, 166, "1", sz=10)); out.append(T(138, 150-k+4, "1", sz=10))
    return svg(480, 300, out)

# ---------- dijkstra ----------
def dijkstra(spec, src):
    E = {}; 
    for e in spec.split(","):
        ab, w = e.split(":"); a, b = ab.split("-"); E.setdefault(a, {})[b] = float(w); E.setdefault(b, {})[a] = float(w)
    assert all(w >= 0 for d in E.values() for w in d.values()), "Dijkstra needs weights >= 0"
    nodes = sorted(E); n = len(nodes)
    pos = {v: (65+45*math.cos(2*math.pi*i/n - math.pi/2), 55+40*math.sin(2*math.pi*i/n - math.pi/2)) for i, v in enumerate(nodes)}
    dist = {v: math.inf for v in nodes}; dist[src] = 0; done = []; frames = []
    def snap(cur): frames.append((dict(dist), list(done), cur))
    snap(None)
    while len(done) < n:
        u = min((v for v in nodes if v not in done), key=lambda v: dist[v])
        if dist[u] == math.inf: break
        done.append(u)
        for v, w in E[u].items():
            if v not in done and dist[u] + w < dist[v]: dist[v] = dist[u] + w
        snap(u)
    for v in done: assert dist[v] <= min(dist[u] + E[u].get(v, math.inf) for u in done)   # optimality witness
    cols = 3; fw, fh = 140, 140; rows = -(-len(frames)//cols); out = []
    for k, (d, dn, cur) in enumerate(frames):
        ox, oy = (k % cols)*fw, (k//cols)*fh; seen = set()
        out.append(T(ox+fw/2, oy+12, f"step {k}" + (f": finalise {cur}" if cur else ": init"), sz=11))
        for a in E:
            for b in E[a]:
                if (b, a) in seen: continue
                seen.add((a, b)); x1, y1, x2, y2 = cut((ox+pos[a][0]+10, oy+pos[a][1]+20), (ox+pos[b][0]+10, oy+pos[b][1]+20), 11)
                out.append(L(x1, y1, x2, y2, w=1.2) + T((x1+x2)/2, (y1+y2)/2-2, f"{E[a][b]:g}", sz=9, c="#888"))
        for v in nodes:
            x, y = ox+pos[v][0]+10, oy+pos[v][1]+20
            f = "#2a7" if v in dn else "none"; s = "#e45" if v == cur else "#888"
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="{f}" fill-opacity=".35" stroke="{s}" stroke-width="{2.5 if v==cur else 1}"/>' + T(x, y+4, v, sz=11))
            out.append(T(x, y+22, "∞" if d[v] == math.inf else f"{d[v]:g}", sz=9, c="#27c"))
    return svg(cols*fw, rows*fh, out), dist

import re
def compact(s, widget=False):
    """shrink tokens: integer coords, <line>->path, shared classes for neutral stroke/fill, inherited text style."""
    rnd = lambda mo: mo.group(1) + re.sub(r"(\d+)\.\d+", lambda q: str(round(float(q.group(0)))), mo.group(2)) + '"'
    s = re.sub(r'((?:x1|y1|x2|y2|cx|cy|x|y|points|d)=")([^"]*)"', rnd, s)
    s = re.sub(r'<line x1="(-?\d+)" y1="(-?\d+)" x2="(-?\d+)" y2="(-?\d+)"', r'<path d="M\1 \2L\3 \4"', s)
    s = s.replace(' text-anchor="middle"', "").replace(' fill="currentColor"', "")
    s = re.sub(r'(<svg [^>]*?)( fill="[^"]*")?>', lambda mo: mo.group(1) + ' text-anchor="middle" fill="%s">' % ("var(--color-text-primary,currentColor)" if widget else "currentColor"), s, count=1)
    sec = "var(--color-border-secondary,#888)" if widget else "#888"; txt = "var(--color-text-secondary,#888)" if widget else "#888"
    for c in ("#888", "#bbb", "#ccc"): s = s.replace('stroke="%s"' % c, 'class="g"')
    s = s.replace('fill="#888"', 'class="m"')
    st = "<style>.g{stroke:%s}.m{fill:%s}</style>" % (sec, txt)
    return re.sub(r"(<svg [^>]*>)", lambda mo: mo.group(1) + st, s, count=1) if 'class="g"' in s or 'class="m"' in s else s
def widget_svg(s):
    """claude.ai inline-widget conformance: host theme vars (with fallbacks), weights 400/500, text >= 11px, no comments."""
    s = re.sub(r"<!--.*?-->", "", s, flags=re.S).replace(' font-family="sans-serif"', "")
    s = re.sub(r'font-size="(9|10)"', 'font-size="11"', s).replace('font-weight="700"', 'font-weight="500"')
    return compact(s, True)
def lint_widget(s):
    bad = []
    if re.search(r"<!--|/\*", s): bad.append("comment")
    if re.search(r"font-weight[=:]\s*\"?(6|7|8|9)00", s): bad.append("weight>500")
    if re.search(r"position\s*:\s*fixed", s): bad.append("fixed")
    if re.search(r"<(!doctype|html|head|body)", s, re.I): bad.append("document tags")
    if any(int(x) < 11 for x in re.findall(r'font-size[=:]\s*"?(\d+)', s)): bad.append("font<11")
    if re.search(r"[\U0001F300-\U0001FAFF\u2600-\u26FF]", s): bad.append("emoji")
    if re.search(r"gradient|box-shadow|filter\s*:\s*blur", s): bad.append("gradient/shadow")
    return bad
def render(c, r):
    if c == "cayley": return cayley(r[0], r[1].split("=")[1] if len(r) > 1 else "")
    if c in ("separate", "extension", "riesz", "dual", "project", "fourier", "cobweb"):
        import fa; return getattr(fa, c if c != "separate" else "separate")(*r)
    if c in ("linmap", "basis", "solid", "surface", "triangle", "ga"):
        import la; return getattr(la, c)(*r)
    if c in ("bfs", "dfs", "prim", "kruskal", "maxflow", "proofdag", "comm", "dfa"):
        import graphs
        if c in ("prim", "kruskal"): return graphs.mst(r[0], c, *r[1:2])
        return getattr(graphs, c)(*r)
    if c in ("phase", "charges", "projectile", "dist", "clt", "rlc", "rc", "lens"):
        import stem; return getattr(stem, c)(*r)
    if c == "quotient": return quotient(r[0], r[1])
    if c == "galois":
        import alg; return alg.galois(r[0])
    if c == "ideals":
        import alg; return alg.ideals(int(r[0]))
    if c == "hasse": return hasse(r[0])
    if c == "plot": return plot(r[0], *map(float, r[1:]))
    if c == "conformal": return conformal(r[0], *map(float, r[1:]))
    if c == "lp": return lp([float(x) for x in r] or [1, 2, 4, math.inf])
    if c == "dijkstra": s, d = dijkstra(r[0], r[1]); return s + "\n<!-- dist: %s -->" % d
    if c in ("domain", "residue", "mobius", "riemann", "julia"):
        import cplx
        if c == "domain": out = cplx.domain(r[0], float(r[1].split("=")[-1]) if len(r) > 1 else 2.0)
        elif c == "residue": out = cplx.residue(r[0], *map(float, r[1:4]))
        elif c == "mobius": out = cplx.mobius(*[complex(x.replace("i", "j")) for x in r[:4]])
        elif c == "riemann": out = cplx.riemann(r)
        else: out = cplx.julia(*map(float, r[:2]))
        if out.startswith("<div"):
            return out if WID else '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><body style="margin:0 auto;padding:16px;max-width:560px;font:15px system-ui;background:#fff;color:#111">' + out
        return out
    if c == "slider":
        import sliders
        if not r or r[0] == "list" or r[0] not in sliders.DEMOS and r[0] != "bundle": return "demos: " + " ".join(sliders.DEMOS) + " | bundle"
        if r[0] == "bundle": return sliders.bundle()
        pins = dict(x.split("=", 1) for x in r[1:] if "=" in x)
        for k in pins: assert k in [p.split(",")[0][4:-1] for p in sliders.DEMOS[r[0]]["params"]], f"unknown param {k}"
        return sliders.widget(r[0], pins, CDN) if WID else sliders.page(r[0], pins)
    sys.exit(__doc__)

WID = False; CDN = None
if __name__ == "__main__":
    a = sys.argv[1:]
    WID = "--widget" in a or "--cdn" in a
    if "--cdn" in a: i = a.index("--cdn"); CDN = a[i+1]; del a[i:i+2]
    a = [x for x in a if x != "--widget"]
    if not a: print(__doc__); sys.exit()
    out = render(a[0], a[1:])
    if WID:
        if a[0] != "slider" and not out.startswith("<div"): out = widget_svg(out)
        bad = lint_widget(out) if a[0] != "slider" or not CDN else []; assert not bad, "widget lint: " + ",".join(bad)
    elif a[0] != "slider" and not out.startswith(("<div", "<!doctype")):
        sv, _, tail = out.partition("\n<!--"); out = compact(sv) + ("\n<!--" + tail if tail else "")
    print(out)
