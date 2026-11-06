"""Graphs, algorithms, proofs and automata (stdlib only). Every algorithm run is cross-checked against an independent method.
  mv.py bfs|dfs|prim|kruskal|maxflow "A-B:4,A-C:1,..." [start]    ("A>B:3" = directed, weight/capacity after ':')
  mv.py proofdag "ax=Axiom;L1=Lemma 1;T=Theorem" "ax>L1,L1>T"       dependency DAG, refuses circular reasoning
  mv.py comm "A B;C D" "A>B:f,A>C:g,B>D:h,C>D:k" "f h = g k"        commutative diagram, composability + endpoints checked
  mv.py dfa "q0 q1" "a b" "q0 a q1;q0 b q0;q1 a q1;q1 b q0" q0 "q1" abab   DFA, completeness, trace, minimal size
(Dijkstra lives in mv.py: dijkstra "A-B:4,..." A)"""
import math, html, itertools
from collections import deque
from base import *
from fgroups import wrap
C1, C2, C3, C4 = "#3b82f6", "#f43f5e", "#22c55e", "#f59e0b"
esc = lambda s: html.escape(str(s), quote=False)
def parse(spec):
    nodes, E = [], []
    for e in spec.split(","):
        e = e.strip()
        if not e: continue
        d = ">" in e; head, _, w = e.partition(":"); a, b = head.split(">" if d else "-"); a, b = a.strip(), b.strip(); w = float(w) if w else 1.0
        for v in (a, b):
            if v not in nodes: nodes.append(v)
        E.append((a, b, w, d))
    return nodes, E
def spring(nodes, E):
    """circular layout; for n <= 8 the node order is chosen to minimise edge crossings (exhaustive, fixing the first node)."""
    n = len(nodes); ed = [(nodes.index(a), nodes.index(b)) for a, b, *_ in E if a != b]
    def cross(order):
        p = {v: i for i, v in enumerate(order)}; c = 0
        for (a, b), (x, y) in itertools.combinations(ed, 2):
            if len({a, b, x, y}) < 4: continue
            lo, hi = sorted((p[a], p[b])); c += (lo < p[x] < hi) != (lo < p[y] < hi)
        return c
    best = list(range(n))
    if n <= 8:
        best = min(((0,) + q for q in itertools.permutations(range(1, n))), key=lambda o: (cross(o), o)); best = list(best)
    return {nodes[v]: (.5 + .5*math.cos(2*math.pi*i/n - math.pi/2), .5 + .5*math.sin(2*math.pi*i/n - math.pi/2)) for i, v in enumerate(best)}
def layered(nodes, E, src):
    adj = {v: [] for v in nodes}
    for a, b, w, d in E: adj[a].append(b); (None if d else adj[b].append(a))
    depth = {src: 0}; q = deque([src])
    while q:
        u = q.popleft()
        for v in sorted(adj[u]):
            if v not in depth: depth[v] = depth[u] + 1; q.append(v)
    for v in nodes: depth.setdefault(v, max(depth.values()) + 1)
    cols = {}
    for v in nodes: cols.setdefault(depth[v], []).append(v)
    m = max(cols); return {v: ((depth[v]/m) if m else .5, (i + 1)/(len(c) + 1)) for c in cols.values() for i, v in enumerate(sorted(c))}
def frame_svg(ox, oy, pos, E, title, node_fill=None, node_stroke=None, edge_style=None, node_note=None, edge_label=None, fw=140, fh=135, mode="full", base_label=True):
    """mode 'skeleton': grey edges + nodes + node names (drawn once, reused via <use>); 'overlay': only what differs from the skeleton; 'full': everything."""
    X = lambda p: ox + 16 + (fw - 32)*p[0]; Y = lambda p: oy + 28 + (fh - 46)*p[1]; o = [] if mode == "skeleton" else [T(ox + fw/2, oy + 13, esc(title), sz=11)]
    if mode == "overlay": o.insert(0, f'<use href="#sk" x="{ox}" y="{oy}"/>')
    for k, (a, b, w, d) in enumerate(E):
        st = (edge_style or {}).get(k, ("#888", 1.2, "")); x1, y1, x2, y2 = X(pos[a]), Y(pos[a]), X(pos[b]), Y(pos[b]); n = math.hypot(x2-x1, y2-y1) or 1
        lab = edge_label(k, (a, b, w, d)) if edge_label else (f"{w:g}" if w != 1 else "")
        if mode == "overlay" and st == ("#888", 1.2, "") and not lab: continue
        if mode == "skeleton": lab = (f"{w:g}" if w != 1 and base_label else "")
        if mode != "overlay" or st != ("#888", 1.2, ""):
            sx, sy, ex, ey = x1 + (x2-x1)*11/n, y1 + (y2-y1)*11/n, x2 - (x2-x1)*11/n, y2 - (y2-y1)*11/n
            o.append(f'<line x1="{sx:.0f}" y1="{sy:.0f}" x2="{ex:.0f}" y2="{ey:.0f}" stroke="{st[0]}" stroke-width="{st[1]}"' + (f' stroke-dasharray="{st[2]}"' if st[2] else "") + (' marker-end="url(#ac)"' if d else "") + "/>")
        if lab and not (mode == "overlay" and base_label and lab == f"{w:g}"): o.append(T((x1+x2)/2 + 4*(y2-y1)/n, (y1+y2)/2 - 4*(x2-x1)/n + 4, esc(lab), sz=11, c="#888"))
    for v in pos:
        fill = (node_fill or {}).get(v); stroke = (node_stroke or {}).get(v)
        if mode == "overlay" and fill is None and stroke is None and not (node_note and v in node_note): continue
        if mode != "overlay" or fill or stroke:
            o.append(f'<circle cx="{X(pos[v]):.0f}" cy="{Y(pos[v]):.0f}" r="11" fill="{fill or "none"}" fill-opacity=".35" stroke="{stroke or "#888"}" stroke-width="{2.4 if stroke else 1}"/>')
        if mode != "overlay": o.append(T(X(pos[v]), Y(pos[v]) + 4, esc(v), sz=11))
        if node_note and v in node_note: o.append(T(X(pos[v]), Y(pos[v]) + 25, esc(node_note[v]), sz=11, c=C1))
    return o
def strip(frames, notes, cols=3, fw=140, fh=135, sk=None):
    rows = -(-len(frames)//cols); ls = [l for n in notes for l in wrap(n, 62)]; body = []
    if sk: body.append('<g id="sk">' + "".join(sk()) + "</g>")
    for k, f in enumerate(frames): body += f(k % cols*fw, k//cols*fh)
    return svg(cols*fw, rows*fh + 14*len(ls) + 8, body + [T(8, rows*fh + 14*(k+1), esc(l), "start", sz=11) for k, l in enumerate(ls)], "c")
def adjacency(nodes, E):
    adj = {v: [] for v in nodes}
    for k, (a, b, w, d) in enumerate(E): adj[a].append((b, w, k)); (None if d else adj[b].append((a, w, k)))
    return adj
def hops(nodes, E):                                       # independent check: Floyd-Warshall on hop counts
    D = {(u, v): (0 if u == v else math.inf) for u in nodes for v in nodes}
    for a, b, w, d in E: D[a, b] = min(D[a, b], 1); (None if d else D.__setitem__((b, a), min(D[b, a], 1)))
    for k in nodes:
        for i in nodes:
            for j in nodes: D[i, j] = min(D[i, j], D[i, k] + D[k, j])
    return D
def bfs(spec, start=None):
    nodes, E = parse(spec); s = start or nodes[0]; adj = adjacency(nodes, E); pos = spring(nodes, E)
    dist = {s: 0}; q = deque([s]); order = []; tree = set(); steps = [(dict(dist), set(), None, set(tree))]
    while q:
        u = q.popleft(); order.append(u)
        for v, w, k in sorted(adj[u]):
            if v not in dist: dist[v] = dist[u] + 1; q.append(v); tree.add(k)
        steps.append((dict(dist), set(order), u, set(tree)))
    D = hops(nodes, E); assert all(dist.get(v, math.inf) == D[s, v] for v in nodes), "BFS distances disagree with Floyd–Warshall"
    fr = []
    for dd, done, cur, tr in steps:
        fr.append((lambda dd, done, cur, tr: lambda ox, oy: frame_svg(ox, oy, pos, E, "start" if cur is None else f"dequeue {cur}", {v: "#22c55e" for v in done}, {cur: C2} if cur else {s: C2}, {k: (C2, 2.4, "") for k in tr}, {v: str(x) for v, x in dd.items()}, lambda k, e: "", mode="overlay"))(dd, done, cur, tr))
    return strip(fr, sk=lambda: frame_svg(0, 0, pos, E, "", mode="skeleton"), notes=[f"BFS from {s}: red node = being expanded, green = finished, blue number = hop distance, red edges = BFS tree", "distances checked against Floyd–Warshall on hop counts ✓ (BFS gives shortest paths in unweighted graphs)"])
def dfs(spec, start=None):
    nodes, E = parse(spec); s = start or nodes[0]; adj = adjacency(nodes, E); pos = spring(nodes, E); t = [0]; d, f, kind = {}, {}, {}
    def go(u, pk):
        t[0] += 1; d[u] = t[0]
        for v, w, k in sorted(adj[u]):
            if k == pk: continue
            if v not in d: kind[k] = "tree"; go(v, k)
            elif v not in f: kind[k] = kind.get(k, "back")
            else: kind[k] = kind.get(k, "forward/cross")
        t[0] += 1; f[u] = t[0]
    go(s, None)
    for u, v in itertools.combinations(d, 2): assert d[u] < f[u] and d[v] < f[v] and (f[u] < d[v] or f[v] < d[u] or (d[u] < d[v] and f[v] < f[u]) or (d[v] < d[u] and f[u] < f[v])), "parenthesis theorem violated"
    cs = {"tree": (C2, 2.4, ""), "back": (C4, 1.6, "4 3"), "forward/cross": (C1, 1.4, "2 3")}
    fr = [lambda ox, oy: frame_svg(ox, oy, pos, E, f"DFS from {s}", {v: "#22c55e" for v in d}, {s: C2}, {k: cs[x] for k, x in kind.items()}, {v: f"{d[v]}/{f[v]}" for v in d}, lambda k, e: "", fw=420, fh=270, mode="overlay")]
    return strip(fr, [f"DFS from {s}: label = discovery/finish time; red = tree edges, orange dashed = back edges" + (", blue dotted = forward/cross" if "forward/cross" in kind.values() else ""), "parenthesis theorem verified for every pair: intervals [d, f] are nested or disjoint ✓" + (" · an undirected graph has only tree and back edges" if not any(e[3] for e in E) else "")], 1, 420, 270, sk=lambda: frame_svg(0, 0, pos, E, "", fw=420, fh=270, mode="skeleton"))
class UF:
    def __init__(self): self.p = {}
    def find(self, x):
        self.p.setdefault(x, x)
        while self.p[x] != x: self.p[x] = self.p[self.p[x]]; x = self.p[x]
        return x
    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb: return False
        self.p[ra] = rb; return True
def mst(spec, algo="kruskal", start=None):
    nodes, E = parse(spec); assert not any(e[3] for e in E), "MST needs an undirected graph"; pos = spring(nodes, E); n = len(nodes)
    def kruskal():
        uf, chosen, steps = UF(), [], []
        for k in sorted(range(len(E)), key=lambda k: (E[k][2], k)):
            ok = uf.union(E[k][0], E[k][1])
            if ok: chosen.append(k)
            steps.append((k, ok, list(chosen)))
        return chosen, steps
    def prim(s):
        seen, chosen, steps = {s}, [], []
        while len(seen) < n:
            cand = [(E[k][2], k) for k in range(len(E)) if (E[k][0] in seen) != (E[k][1] in seen)]
            if not cand: break
            w, k = min(cand); v = E[k][1] if E[k][0] in seen else E[k][0]; seen.add(v); chosen.append(k); steps.append((k, True, list(chosen), set(seen)))
        return chosen, steps
    ck, ks = kruskal(); pk, ps = prim(start or nodes[0]); W = lambda ch: sum(E[k][2] for k in ch)
    assert len(ck) == n - 1 and len(pk) == n - 1, "graph is not connected"; assert abs(W(ck) - W(pk)) < 1e-9, "Kruskal and Prim disagree"
    if math.comb(len(E), n - 1) <= 30000:                                  # brute force over all (n-1)-edge subsets
        best = math.inf
        for sub in itertools.combinations(range(len(E)), n - 1):
            uf = UF()
            if all(uf.union(E[k][0], E[k][1]) for k in sub): best = min(best, W(sub))
        assert abs(best - W(ck)) < 1e-9, "MST weight is not optimal"
    steps = ks if algo == "kruskal" else ps; fr = []
    for st in steps:
        k, ok, ch = st[0], st[1], st[2]
        es = {j: (C3, 2.6, "") for j in ch}
        if algo == "kruskal" and not ok: es[k] = (C2, 2, "4 3")
        elif algo == "kruskal": es[k] = (C3, 3.2, "")
        else: es[k] = (C3, 3.2, "")
        fr.append((lambda k, ok, es: lambda ox, oy: frame_svg(ox, oy, pos, E, (f"{'add' if ok else 'skip (cycle)'} {E[k][0]}-{E[k][1]} ({E[k][2]:g})"), None, None, es, mode="overlay"))(k, ok, es))
    return strip(fr, sk=lambda: frame_svg(0, 0, pos, E, "", mode="skeleton"), notes=[f"{algo.capitalize()}: green = tree edges, red dashed = rejected (would close a cycle). MST weight = {W(ck):g}", "Kruskal and Prim give the same weight ✓" + (", and it equals the minimum over all spanning trees (brute force) ✓" if math.comb(len(E), n - 1) <= 30000 else "")])
def maxflow(spec, s=None, t=None):
    nodes, E = parse(spec); assert all(e[3] for e in E), "max-flow needs directed edges 'A>B:cap'"; s = s or nodes[0]; t = t or nodes[-1]; pos = layered(nodes, E, s)
    cap = {}; fl = {}
    for k, (a, b, w, _) in enumerate(E): cap[k] = w; fl[k] = 0.0
    def residual_path():
        par = {s: None}; q = deque([s])
        while q:
            u = q.popleft()
            for k, (a, b, w, _) in enumerate(E):
                for (x, y, fwd) in ((a, b, True), (b, a, False)):
                    if x == u and y not in par and ((fwd and cap[k] - fl[k] > 1e-12) or (not fwd and fl[k] > 1e-12)): par[y] = (k, fwd, u); q.append(y)
            if t in par: break
        if t not in par: return None, par
        path, v = [], t
        while par[v]: k, fwd, u = par[v]; path.append((k, fwd)); v = u
        return path[::-1], par
    frames = [dict(fl)]; paths = [[]]
    while True:
        p, par = residual_path()
        if p is None: break
        b = min(cap[k] - fl[k] if f else fl[k] for k, f in p)
        for k, f in p: fl[k] += b if f else -b
        frames.append(dict(fl)); paths.append(p)
    val = sum(fl[k] for k, e in enumerate(E) if e[0] == s) - sum(fl[k] for k, e in enumerate(E) if e[1] == s)
    for v in nodes:                                                      # conservation + capacity
        if v not in (s, t): assert abs(sum(fl[k] for k, e in enumerate(E) if e[1] == v) - sum(fl[k] for k, e in enumerate(E) if e[0] == v)) < 1e-9
    assert all(-1e-9 <= fl[k] <= cap[k] + 1e-9 for k in cap)
    S = set(par); cutv = sum(cap[k] for k, e in enumerate(E) if e[0] in S and e[1] not in S); assert abs(cutv - val) < 1e-9, "max-flow ≠ min-cut: not optimal"
    fr = []
    for i, (f_, p) in enumerate(zip(frames, paths)):
        es = {k: ((C2, 2.8, "") if any(k == j for j, _ in p) else ("#888", 1.4, "")) for k in cap}
        fr.append((lambda f_, es, i, p: lambda ox, oy: frame_svg(ox, oy, pos, E, "start" if i == 0 else f"augment +{min(cap[k] - frames[i-1][k] if fw_ else frames[i-1][k] for k, fw_ in p):g}", {s: "#3b82f6", t: "#22c55e"}, None, es, None, lambda k, e: f"{f_[k]:g}/{e[2]:g}", fw=210, mode="overlay", base_label=False))(f_, es, i, p))
    es = {k: ((C4, 2.4, "4 3") if (E[k][0] in S and E[k][1] not in S) else ("#888", 1.4, "")) for k in cap}
    fr.append(lambda ox, oy: frame_svg(ox, oy, pos, E, f"min cut = {cutv:g}", {v: "#f59e0b" for v in S}, {s: C1, t: C3}, es, None, lambda k, e: f"{frames[-1][k]:g}/{e[2]:g}", fw=210, mode="overlay", base_label=False))
    return strip(fr, cols=2, fw=210, fh=135, sk=lambda: frame_svg(0, 0, pos, E, "", fw=210, mode="skeleton", base_label=False), notes=[f"Edmonds–Karp from {s} to {t}: labels flow/capacity, red = augmenting path (BFS in the residual graph). Max flow = {val:g}", f"capacity and conservation verified ✓; max-flow = min-cut: orange set S = nodes reachable in the residual graph, edges leaving S (dashed) have total capacity {cutv:g} = flow ✓"])

def proofdag(nodespec, edgespec):
    lab = {}
    for it in nodespec.split(";"):
        if it.strip(): k, _, v = it.partition("="); lab[k.strip()] = v.strip() or k.strip()
    E = [tuple(x.strip() for x in e.split(">")) for e in edgespec.split(",") if e.strip()]
    for a, b in E: assert a in lab and b in lab, f"unknown node in {a}>{b}"
    out = {v: [b for a, b in E if a == v] for v in lab}; color = {}; stack = []
    def go(u):
        color[u] = 1; stack.append(u)
        for v in out[u]:
            if color.get(v) == 1: i = stack.index(v); raise AssertionError("circular reasoning: " + " → ".join(stack[i:] + [v]))
            if v not in color: go(v)
        stack.pop(); color[u] = 2
    for v in lab:
        if v not in color: go(v)
    lv = {}
    def level(v):
        if v not in lv: ps = [a for a, b in E if b == v]; lv[v] = 0 if not ps else 1 + max(level(p) for p in ps)
        return lv[v]
    for v in lab: level(v)
    rows = {}
    for v in lab: rows.setdefault(lv[v], []).append(v)
    W = max(420, 130*max(len(r) for r in rows.values())); H = 90*len(rows) + 30; pos = {v: (W*(i+1)/(len(r)+1), 40 + 90*l) for l, r in rows.items() for i, v in enumerate(r)}
    srcs = {v for v in lab if not any(b == v for a, b in E)}; sinks = {v for v in lab if not out[v]}; o = []
    for a, b in E:
        (x1, y1), (x2, y2) = pos[a], pos[b]; o.append(f'<line x1="{x1:.0f}" y1="{y1+16:.0f}" x2="{x2:.0f}" y2="{y2-18:.0f}" stroke="#888" stroke-width="1.3" marker-end="url(#ac)"/>')
    for v, (x, y) in pos.items():
        w = max(60, 7*len(lab[v]) + 16); col = C3 if v in srcs else C2 if v in sinks else C1
        o.append(f'<rect x="{x-w/2:.0f}" y="{y-16}" width="{w}" height="32" rx="6" fill="{col}22" stroke="{col}"/>' + T(x, y + 4, esc(lab[v]), sz=11))
    ls = wrap(f"acyclic ✓ ({len(lab)} statements, {len(E)} dependencies) · green = starting points (axioms/hypotheses) · red = final result · arrow = 'is used to prove'", int(W/6.4))
    return svg(W, H + 14*len(ls) + 8, o + [T(10, H + 14*(k+1), esc(l), "start", sz=11) for k, l in enumerate(ls)], "c")
def comm(grid, arrows, paths=""):
    rows = [r.split() for r in grid.split(";")]; pos = {}
    for j, r in enumerate(rows):
        for i, v in enumerate(r):
            if v != ".": pos[v] = (60 + 130*i, 45 + 95*j)
    AR = {}
    for it in arrows.split(","):
        head, _, nm = it.strip().partition(":"); dashed = nm.endswith("!"); nm = nm.rstrip("!") or head; a, b = head.split(">")
        assert a in pos and b in pos, f"unknown object in {head}"; assert nm not in AR, f"duplicate arrow name {nm}"; AR[nm] = (a.strip(), b.strip(), dashed)
    notes = []
    for p in [x for x in paths.split(";") if x.strip()]:
        sides = [s.split() for s in p.split("=")]; ends = []
        for sd in sides:
            for nm in sd: assert nm in AR, f"unknown arrow {nm}"
            for f, g in zip(sd, sd[1:]): assert AR[f][1] == AR[g][0], f"not composable: cod({f}) = {AR[f][1]} ≠ dom({g}) = {AR[g][0]}"
            ends.append((AR[sd[0]][0], AR[sd[-1]][1]))
        assert all(e == ends[0] for e in ends), f"paths have different endpoints: {ends}"
        notes.append(" = ".join(" ; ".join(s) for s in sides) + f" : {ends[0][0]} → {ends[0][1]} ✓")
    o = []
    for nm, (a, b, dsh) in AR.items():
        (x1, y1), (x2, y2) = pos[a], pos[b]
        if a == b: o.append(f'<path d="M{x1-8:.0f} {y1-16:.0f}c-20 -30 40 -30 16 0" fill="none" stroke="#888" stroke-width="1.4" marker-end="url(#ac)"/>' + T(x1, y1 - 38, esc(nm), sz=11, c=C1)); continue
        n = math.hypot(x2-x1, y2-y1); ux, uy = (x2-x1)/n, (y2-y1)/n
        o.append(f'<line x1="{x1+ux*20:.0f}" y1="{y1+uy*18:.0f}" x2="{x2-ux*20:.0f}" y2="{y2-uy*18:.0f}" stroke="{C3 if dsh else "#888"}" stroke-width="1.6"' + (' stroke-dasharray="5 3"' if dsh else "") + ' marker-end="url(#ac)"/>' + T((x1+x2)/2 - 11*uy - (6 if abs(uy) > .5 else 0), (y1+y2)/2 + 11*ux + 4 - (14 if abs(ux) > .5 else 0) , esc(nm), sz=11, c=C1))
    for v, (x, y) in pos.items(): o.append(T(x, y + 4, esc(v), sz=13))
    for p in [x for x in paths.split(";") if x.strip()]:
        sd = p.split("=")[0].split(); vs = [AR[sd[0]][0]] + [AR[n][1] for n in sd]; cx_ = sum(pos[v][0] for v in vs)/len(vs); cy_ = sum(pos[v][1] for v in vs)/len(vs)
        o.append(T(cx_, cy_ + 5, "⟳", sz=16, c=C4))
    W = 60 + 130*max(len(r) for r in rows); H = 45 + 95*len(rows); ls = [l for n in notes for l in wrap(n, 60)] + ["dashed green = induced/unique arrow (∃!)"] * any(v[2] for v in AR.values())
    return svg(W, H + 14*len(ls) + 10, o + [T(8, H + 14*(k+1), esc(l), "start", sz=11) for k, l in enumerate(ls)], "c")
def dfa(states, alpha, trans, start, acc, word=""):
    Q, A = states.split(), alpha.split(); acc = set(acc.split()); delta = {}
    for t_ in trans.split(";"):
        if not t_.strip(): continue
        q, a, r = t_.split(); assert q in Q and r in Q and a in A, f"bad transition {t_}"; assert (q, a) not in delta or delta[q, a] == r, f"nondeterministic: {q} on {a}"; delta[q, a] = r
    miss = [(q, a) for q in Q for a in A if (q, a) not in delta]; assert not miss, f"transition function is not total; missing {miss[:4]} (add a trap state)"
    assert start in Q and acc <= set(Q)
    reach = {start}; fr = [start]
    while fr:
        q = fr.pop()
        for a in A:
            if delta[q, a] not in reach: reach.add(delta[q, a]); fr.append(delta[q, a])
    part = {q: (q in acc) for q in reach}                                    # Moore partition refinement
    while True:
        sig = {q: (part[q], tuple(part[delta[q, a]] for a in A)) for q in reach}; ids = {s_: i for i, s_ in enumerate(sorted(set(sig.values()), key=str))}; new = {q: ids[sig[q]] for q in reach}
        if len(set(new.values())) == len(set(part.values())): break
        part = new
    nmin = len(set(part.values())); run = [start]
    for ch in word: assert ch in A, f"symbol {ch!r} not in alphabet"; run.append(delta[run[-1], ch])
    n = len(Q); pos = {q: (210 + 120*math.cos(2*math.pi*i/n - math.pi/2), 135 + 95*math.sin(2*math.pi*i/n - math.pi/2)) for i, q in enumerate(Q)}
    lab = {}
    for (q, a), r in delta.items(): lab.setdefault((q, r), []).append(a)
    used = set(zip(run, run[1:])); o = []
    for (q, r), as_ in lab.items():
        col = C2 if (q, r) in used else "#888"; w = 2.4 if (q, r) in used else 1.2; tx = ",".join(as_)
        if q == r: x, y = pos[q]; o.append(f'<path d="M{x-8:.0f} {y-17:.0f}c-10 -26 26 -26 16 0" fill="none" stroke="{col}" stroke-width="{w}" marker-end="url(#ac)"/>' + T(x, y - 34, esc(tx), sz=11, c=C1)); continue
        (x1, y1), (x2, y2) = pos[q], pos[r]; mx, my = (x1+x2)/2, (y1+y2)/2; n_ = math.hypot(x2-x1, y2-y1); bend = 18 if (r, q) in lab else 0; cx_, cy_ = mx - (y2-y1)/n_*bend, my + (x2-x1)/n_*bend
        sx, sy = x1 + (cx_-x1)*18/math.hypot(cx_-x1, cy_-y1), y1 + (cy_-y1)*18/math.hypot(cx_-x1, cy_-y1); ex, ey = x2 + (cx_-x2)*20/math.hypot(cx_-x2, cy_-y2), y2 + (cy_-y2)*20/math.hypot(cx_-x2, cy_-y2)
        o.append(f'<path d="M{sx:.0f} {sy:.0f}Q{cx_:.0f} {cy_:.0f} {ex:.0f} {ey:.0f}" fill="none" stroke="{col}" stroke-width="{w}" marker-end="url(#ac)"/>' + T(cx_ + (4 if bend else 0), cy_ - 4, esc(tx), sz=11, c=C1))
    for q, (x, y) in pos.items():
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="16" fill="{C3 + "33" if q == run[-1] and word else "none"}" stroke="#888" stroke-width="1.4"/>' + (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="20" fill="none" stroke="#888"/>' if q in acc else "") + T(x, y + 4, esc(q), sz=12))
    sx, sy = pos[start]; o.append(f'<line x1="{sx-48:.0f}" y1="{sy:.0f}" x2="{sx-22:.0f}" y2="{sy:.0f}" stroke="#888" stroke-width="1.4" marker-end="url(#ac)"/>')
    notes = [f"DFA: {n} states ({len(reach)} reachable), alphabet {{{', '.join(A)}}}, total & deterministic ✓; minimal equivalent DFA has {nmin} state(s) (Moore partition refinement)"]
    if word: notes.append(f"input '{word}': " + " → ".join(run) + f" — {'ACCEPT' if run[-1] in acc else 'REJECT'} (path in red)")
    ls = [l for x in notes for l in wrap(x, 62)]
    return svg(420, 270 + 14*len(ls), o + [T(8, 262 + 14*(k+1), esc(l), "start", sz=11) for k, l in enumerate(ls)], "c")
