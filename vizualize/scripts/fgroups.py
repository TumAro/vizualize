"""Finite groups as permutation groups: Cayley graphs, quotients, subgroup lattices. stdlib only."""
import math, sys, re
from itertools import product
from collections import Counter
from base import *

def mul(p, q): return tuple(p[i] for i in q)            # (p*q)(i)=p(q(i)): apply q first
def idn(n): return tuple(range(n))
def closure(gens, n):
    G = {idn(n)}; fr = [idn(n)]
    while fr:
        x = fr.pop()
        for g in gens:
            y = mul(x, g)
            if y not in G: G.add(y); fr.append(y)
    return G
def order(g):
    k, x = 1, g
    while x != idn(len(g)): x = mul(x, g); k += 1
    return k
def cyc(n): return tuple((i+1) % n for i in range(n))
def refl(n): return tuple((-i) % n for i in range(n))

_Q = {("1", "1"): (1, "1"), ("i", "i"): (-1, "1"), ("j", "j"): (-1, "1"), ("k", "k"): (-1, "1"), ("i", "j"): (1, "k"), ("j", "k"): (1, "i"), ("k", "i"): (1, "j"),
      ("j", "i"): (-1, "k"), ("k", "j"): (-1, "i"), ("i", "k"): (-1, "j")}
def _q8():
    U = [(s, u) for u in "1ijk" for s in (1, -1)]
    def prod(a, b):
        s, u = _Q.get((a[1], b[1]), (1, b[1] if a[1] == "1" else a[1]))
        return (s*a[0]*b[0], u)
    idx = {q: k for k, q in enumerate(U)}
    perm = lambda q: tuple(idx[prod(q, y)] for y in U)             # left multiplication = regular representation
    nm = lambda q: ("-" if q[0] < 0 else "") + q[1]
    return 8, {"i": perm((1, "i")), "j": perm((1, "j"))}, {perm(q): nm(q) for q in U}
def _factor(f):
    m = re.fullmatch(r"([CDQSA])(\d+)", f)
    if not m: sys.exit("unknown group " + f + "  (C<n> D<n> Q8 S<n> A4 and products like C2xC4)")
    k, m = m.group(1), int(m.group(2))
    if k == "C": return m, {"a": cyc(m)}, "ring", None
    if k == "D": return m, {"r": cyc(m), "s": refl(m)}, "dih", None
    if k == "Q" and m == 8: n, g, nm = _q8(); return n, g, "bfs", nm
    if k == "S" and m == 3: return 3, {"r": (1, 2, 0), "s": (0, 2, 1)}, "dih", None
    if k == "S" and 2 <= m <= 5: return m, {"a": cyc(m), "b": (1, 0) + tuple(range(2, m))}, "bfs", None
    if k == "A" and m == 4: return 4, {"a": (1, 2, 0, 3), "b": (1, 0, 3, 2)}, "bfs", None
    sys.exit("unsupported group " + f)
def preset(name):
    parts = name.split("x")
    if len(parts) == 1: return _factor(name)
    off, gens, n, letters = 0, {}, 0, iter("abcdefghkmnpqrstuvwyz")
    for f in parts:
        m, g, _, _ = _factor(f)
        for gn, p in g.items(): gens[next(letters)] = tuple(range(off)) + tuple(off + x for x in p) + tuple(range(off + m, 0 + off + m))
        off += m
    return off, {k: v + tuple(range(len(v), off)) for k, v in gens.items()}, "bfs", None
def build(name):
    n, gens, lay, names = preset(name)
    G = closure(gens.values(), n); assert len(G) <= 60, f"|G|={len(G)} > 60: too large to draw"
    words = {idn(n): "e"}; fr = [idn(n)]
    while fr:                                           # shortest-word naming by BFS
        x = fr.pop(0)
        for gn, g in gens.items():
            y = mul(x, g)
            if y not in words: words[y] = (words[x] if words[x] != "e" else "") + gn; fr.append(y)
    if names: words = {p: ("e" if names[p] == "1" else names[p]) for p in G}
    if lay == "dih":
        r, s = gens["r"], gens["s"]; x = idn(n)
        for k in range(n):
            words[x] = "e" if k == 0 else f"r{k}"; words[mul(s, x)] = "s" if k == 0 else f"sr{k}"; x = mul(x, r)
    return n, gens, lay, G, words
def check_group(G, n):
    e = idn(n); L_ = list(G)[:14]
    assert all(mul(a, e) == a == mul(e, a) for a in G)
    assert all(mul(mul(a, b), c) == mul(a, mul(b, c)) for a, b, c in product(L_, repeat=3))
    assert all(mul(a, b) in G for a in G for b in G)
def identify(G):
    """name small groups from invariants (order, abelian?, element-order histogram); else say so."""
    N = len(G); c = Counter(order(g) for g in G); ab = all(mul(a, b) == mul(b, a) for a in G for b in G)
    if N == 1: return "trivial"
    if max(c) == N: return f"C{N}"
    if ab:
        if max(c) <= 2: return "C2^%d" % round(math.log2(N))
        return {8: "C2×C4", 9: "C3×C3", 12: "C2×C6", 16: "abelian (16)", 18: "C3×C6"}.get(N, f"abelian, order {N}")
    return {6: "S3", 10: "D5", 14: "D7", 18: "D9"}.get(N) or ({8: ("Q8" if c[2] == 1 else "D4"), 12: ("A4" if c[3] == 8 else "D6" if c[2] == 7 else "Dic3"), 16: "non-abelian (16)", 24: ("S4" if c[2] == 9 else "non-abelian (24)")}.get(N, f"non-abelian, order {N}"))

def wrap(note, w=62):
    """wrap at ' · ' first, then at spaces, so no caption line exceeds w characters"""
    out, cur = [], ""
    for part in note.split(" · "):
        for k, word in enumerate(part.split(" ")):
            sep = " · " if (cur and k == 0) else " "
            if cur and len(cur) + len(sep) + len(word) > w: out.append(cur); cur = word
            else: cur = word if not cur else cur + sep + word
    return out + [cur]
def _spring(ps, ed, m):
    P = [[math.cos(2.4*i)*(1+i*.15), math.sin(2.4*i)*(1+i*.15)] for i in range(m)]
    for it in range(300):
        F = [[0, 0] for _ in range(m)]
        for i in range(m):
            for j in range(i+1, m):
                dx, dy = P[i][0]-P[j][0], P[i][1]-P[j][1]; f = 1.0/(dx*dx+dy*dy+1e-6)
                F[i][0] += dx*f; F[i][1] += dy*f; F[j][0] -= dx*f; F[j][1] -= dy*f
        for i, j in ed:
            dx, dy = P[i][0]-P[j][0], P[i][1]-P[j][1]; d = math.hypot(dx, dy)+1e-9
            F[i][0] -= dx*d*.5; F[i][1] -= dy*d*.5; F[j][0] += dx*d*.5; F[j][1] += dy*d*.5
        t = .1*(1-it/300)+.002
        for i in range(m):
            n_ = math.hypot(*F[i])+1e-9; P[i][0] += F[i][0]/n_*min(n_, t*5); P[i][1] += F[i][1]/n_*min(n_, t*5)
    xs, ys = [p[0] for p in P], [p[1] for p in P]; sx, sy = max(xs)-min(xs) or 1, max(ys)-min(ys) or 1
    return {p: (30+360*(q[0]-min(xs))/sx, 25+250*(q[1]-min(ys))/sy) for p, q in zip(ps, P)}

def cayley_draw(n, gens, lay, G, words, col=None, note=""):
    pos, cx, cy = {}, 210, 145
    els = sorted(G, key=lambda p: (len(words[p]), words[p]))
    ring = next((g for g in gens.values() if order(g) == len(G)), None)
    if ring is not None and (lay == "ring" or len(G) > 2 and lay != "dih"):
        x = idn(n)
        for k in range(len(G)):
            t = math.radians(90 - 360*k/len(G)); pos[x] = (cx+120*math.cos(t), cy-120*math.sin(t)); x = mul(x, ring)
    elif lay == "dih":
        x = idn(n)
        for k in range(n):
            t = math.radians(90 - 360*k/n)
            pos[x] = (cx+120*math.cos(t), cy-120*math.sin(t)); pos[mul(gens["s"], x)] = (cx+65*math.cos(t), cy-65*math.sin(t)); x = mul(x, gens["r"])
    else:
        idx = {p: i for i, p in enumerate(els)}
        pos = _spring(els, [(idx[p], idx[mul(p, g)]) for g in gens.values() for p in els if mul(p, g) != p], len(els))
    out = []
    for gi, (gn, g) in enumerate(gens.items()):
        c = C[gi % len(C)]; o = order(g); drawn = set()
        for p in G:
            q = mul(p, g)
            if o == 2:
                if frozenset((p, q)) in drawn: continue
                drawn.add(frozenset((p, q))); out.append(L(*cut(pos[p], pos[q], 13), c=c, w=2))
            elif q != p: out.append(L(*cut(pos[p], pos[q], 13), c=c, w=2, arrow="c"))
    pal = ["#fdd", "#def", "#dfd", "#fe9", "#edf", "#cef", "#fcf", "#cfc"]
    for p, (x, y) in pos.items():
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{pal[col[p] % 8] if col else "none"}" fill-opacity=".8" stroke="#888"/>' + T(x, y+4, words[p], c="#000" if col else "currentColor"))
    x = 10
    for i, (gn, g) in enumerate(gens.items()):
        out.append(f'<rect x="{x}" y="302" width="14" height="4" fill="{C[i % 5]}"/>' + T(x+18, 308, f"{gn} (order {order(g)})", "start", sz=11)); x += 110
    for k, ln_ in enumerate(wrap(note, 70)): out.append(T(10, 326 + 14*k, ln_, "start", sz=11))
    return svg(420, 330 + 14*len(wrap(note, 70)), out, "c")
def cayley(name, sub=""):
    n, gens, lay, G, words = build(name); check_group(G, n); inv = {w: p for p, w in words.items()}
    col = None; note = f"{name} ≅ {identify(G)}"
    if sub:
        N = _normal(G, inv, sub, n, name)
        cos = _cosets(G, N, words); col = {g: i for i, c in enumerate(cos) for g in c}
        note = f"fill = coset of ⟨{sub}⟩ · |G/N|={len(cos)}"
    return cayley_draw(n, gens, lay, G, words, col, note)
def _normal(G, inv, sub, n, name):
    bad = [x for x in sub.split(",") if x not in inv]
    assert not bad, f"unknown element {bad}; valid: {sorted(inv)}"
    N = closure([inv[x] for x in sub.split(",")], n)
    for g in G: assert {mul(g, h) for h in N} == {mul(h, g) for h in N}, f"<{sub}> is NOT normal in {name}: no quotient group"
    return N
def _cosets(G, N, words):
    cos = []
    for g in sorted(G, key=lambda p: (len(words[p]), words[p])):
        c = frozenset(mul(g, h) for h in N)
        if c not in cos: cos.append(c)
    assert len(cos)*len(N) == len(G); return cos
def quotient(name, sub):
    """Cayley graph of G/N itself: nodes = cosets (labelled by shortest representative), arrows = coset·generator. Well-definedness is asserted."""
    sub = sub.replace("sub=", ""); n, gens, lay, G, words = build(name); inv = {w: p for p, w in words.items()}
    N = _normal(G, inv, sub, n, name); cos = _cosets(G, N, words); ci = {g: i for i, c in enumerate(cos) for g in c}; m = len(cos)
    qg = {}
    for gn, g in gens.items():
        perm = [None]*m
        for i, c in enumerate(cos):
            tgt = {ci[mul(x, g)] for x in c}; assert len(tgt) == 1, "right multiplication does not respect cosets"; perm[i] = tgt.pop()
        qg[gn] = tuple(perm)
    img = {idn(n): idn(m)}; fr = [idn(n)]                # homomorphism G -> G/N on every element
    while fr:
        x = fr.pop(0)
        for gn, g in gens.items():
            y = mul(x, g); v = mul(img[x], qg[gn])
            if y in img: assert img[y] == v, "homomorphism not well defined"
            else: img[y] = v; fr.append(y)
    Q = set(img.values()); assert len(Q) == m and closure(qg.values(), m) == Q
    assert all(img[a] == img[b] for c in cos for a in c for b in c) and {g for g in G if img[g] == idn(m)} == set(N)   # kernel = N
    qw = {}
    for g in sorted(G, key=lambda p: (len(words[p]), words[p])): qw.setdefault(img[g], words[g])
    qlay = "ring" if any(order(p) == m for p in qg.values()) else "bfs"
    s = cayley_draw(m, qg, qlay, Q, qw, None, f"G/N ≅ {identify(Q)} · N=⟨{sub}⟩ (normal ✓) · label = shortest coset rep")
    return s

def subgroups(G, n):
    cycs = {frozenset(closure([a], n)) for a in G}; subs = set(cycs); ch = True
    while ch:
        ch = False
        for A in list(subs):
            for B in cycs:
                if not B <= A:
                    J = frozenset(closure(list(A | B), n))
                    if J not in subs: subs.add(J); ch = True
        assert len(subs) <= 60, "too many subgroups to draw"
    return subs
def draw_lattice(nodes, covers, W=460, edge=None, note="", dense=False):
    """nodes {id: (lines[list], bold)}; covers [(low, high)]. Level = longest chain from the bottom."""
    lv = {}
    def level(x):
        if x not in lv: lv[x] = 0 if not any(h == x for _, h in covers) else 1 + max(level(l) for l, h in covers if h == x)
        return lv[x]
    for x in nodes: level(x)
    top = max(lv.values()); gap = 84 if not dense else 70
    rows = {}
    for x in sorted(nodes, key=str): rows.setdefault(lv[x], []).append(x)
    order_ = {}
    for l in range(top + 1):                                  # order each row by barycentre of its lower neighbours (fewer crossings)
        r = rows[l]
        if l: r.sort(key=lambda x: sum(order_[a] for a, h in covers if h == x) / max(1, sum(1 for a, h in covers if h == x)))
        for i, x in enumerate(r): order_[x] = (i + 1) / (len(r) + 1)
    if not dense: W = max(W, 150 * max(len(r) for r in rows.values()))
    nl = wrap(note, int(W / 6.4)); H = gap*top + 60 + 14*len(nl)
    pos = {x: (W*order_[x], H-35-14*len(nl)-gap*l) for l, r in rows.items() for x in r}
    out = [L(pos[a][0], pos[a][1]-12, pos[b][0], pos[b][1]+12, w=1.2) for a, b in covers]
    if edge: out += [T((pos[a][0]+pos[b][0])/2+7, (pos[a][1]+pos[b][1])/2+3, edge[(a, b)], "start", "#888", 11) for a, b in covers if (a, b) in edge and not dense]
    for x, (px, py) in pos.items():
        lines, bold = nodes[x]
        if dense: out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="9" fill="{"#fdd" if bold else "none"}" stroke="#888"/>' + T(px, py+4, lines[-1], sz=11))
        else:
            for k, ln_ in enumerate(lines): out.append(T(px, py + 4 + 14*(k - (len(lines)-1)/2), f'<tspan font-weight="{700 if bold and k == 0 else 400}">{ln_}</tspan>', c="currentColor" if k == 0 else "#2a7"))
    return svg(W, H, out + [T(10, H-6-14*(len(nl)-1-k), ln_, "start", sz=11) for k, ln_ in enumerate(nl)])
def lattice_data(name):
    n, gens, lay, G, words = build(name); inv = {w: p for p, w in words.items()}
    subs = sorted(subgroups(G, n), key=lambda s: (len(s), sorted(map(words.get, s))))
    assert any(len(s) == len(G) for s in subs) and all(len(G) % len(s) == 0 for s in subs)   # Lagrange
    covers = [(a, b) for a in subs for b in subs if a < b and not any(a < c < b for c in subs)]
    nm = lambda g: tuple(sorted(range(n), key=lambda i: g[i]))
    normal = {s for s in subs if all({mul(mul(g, h), nm(g)) for h in s} == set(s) for g in G)}
    return n, G, words, inv, subs, covers, normal
def hasse(name):
    n, G, words, inv, subs, covers, normal = lattice_data(name)
    nodes = {}
    for s in subs:
        if len(s) == 1: lab = "{e}"
        elif len(s) == len(G): lab = "G"
        else:
            gs, cur = [], {idn(n)}
            for p in sorted(s, key=lambda p: (len(words[p]), words[p])):
                if p not in cur: gs.append(words[p]); cur = closure([inv[w] for w in gs], n)
            lab = "⟨" + ",".join(gs) + "⟩"
        nodes[s] = ([lab + f" {len(s)}"], s in normal)
    dense = len(subs) > 14
    if dense: nodes = {s: ([str(len(s))], s in normal) for s in subs}
    return draw_lattice(nodes, covers, 460, None, f"{name} ≅ {identify(G)} · {len(subs)} subgroups · bold/pink = normal · number = |H|", dense)
