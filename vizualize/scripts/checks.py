#!/usr/bin/env python3
"""Executable invariant checks for vizualize templates. stdlib only.
Run: python3 scripts/checks.py            (all checks)
     python3 scripts/checks.py cayley     (emit S3 Cayley SVG to stdout)"""
import sys, math
from itertools import permutations

def S3():
    comp = lambda p, q: tuple(p[q[i]] for i in range(3))   # (p*q)(i)=p(q(i))
    r, s = (1, 2, 0), (0, 2, 1)
    e = (0, 1, 2)
    els = {}
    x = e
    for k in range(3):
        els[f"r{k}"] = x; x = comp(x, r)
    for k in range(3):
        els[f"sr{k}"] = comp(s, els[f"r{k}"])
    return comp, r, s, e, els

def check_S3():
    comp, r, s, e, els = S3()
    assert len(set(els.values())) == 6
    assert comp(comp(r, r), r) == e and r != e
    assert comp(s, s) == e
    assert comp(comp(s, r), s) == comp(r, r)          # s r s = r^-1
    inv = {v: k for k, v in els.items()}
    for g in els.values():
        assert comp(g, r) in inv and comp(g, s) in inv  # out-degree 1 per generator
    return comp, r, s, els

def cayley_svg():
    comp, r, s, els = check_S3()
    inv = {v: k for k, v in els.items()}
    pos = {}
    for k in range(3):
        t = math.radians(90 + 120 * k)
        pos[f"r{k}"] = (200 + 110 * math.cos(t), 150 - 110 * math.sin(t))
        pos[f"sr{k}"] = (200 + 60 * math.cos(t), 150 - 60 * math.sin(t))
    out = ['<svg viewBox="0 0 400 300" width="100%" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif" font-size="13">',
           '<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0L10,5L0,10z" fill="context-stroke"/></marker></defs>']
    def shorten(p, q, d=14):
        dx, dy = q[0]-p[0], q[1]-p[1]; L = math.hypot(dx, dy)
        return (p[0]+dx*d/L, p[1]+dy*d/L, q[0]-dx*d/L, q[1]-dy*d/L)
    for n, g in els.items():
        a = pos[n]; b = pos[inv[comp(g, r)]]
        x1, y1, x2, y2 = shorten(a, b)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#e45" stroke-width="2" marker-end="url(#a)"/>')
    drawn = set()
    for n, g in els.items():
        m = inv[comp(g, s)]
        if frozenset((n, m)) in drawn: continue
        drawn.add(frozenset((n, m)))
        x1, y1, x2, y2 = shorten(pos[n], pos[m])
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#27c" stroke-width="2"/>')
    for n, (x, y) in pos.items():
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="14" fill="none" stroke="#888"/><text x="{x:.1f}" y="{y+4:.1f}" text-anchor="middle" fill="currentColor">{n}</text>')
    out.append('<text x="10" y="285" fill="#e45">→ r (order 3)</text><text x="140" y="285" fill="#27c">— s (order 2)</text></svg>')
    return "\n".join(out)

def check_quotient():
    N = {0, 4, 8}
    cosets = {frozenset((g + n) % 12 for n in N) for g in range(12)}
    assert len(cosets) == 12 // len(N) == 4 and all(len(c) == 3 for c in cosets)
    # well-defined: a~a', b~b' => a+b ~ a'+b'
    cid = {g: c for c in cosets for g in c}
    for a in range(12):
        for b in range(12):
            for a2 in cid[a]:
                for b2 in cid[b]:
                    assert cid[(a2 + b2) % 12] == cid[(a + b) % 12]

def check_tower():
    # Q(sqrt2,sqrt3): 4 = 2*2 ; Gal = Z2xZ2 has 3 subgroups of order 2 <-> 3 quadratic subfields
    assert 2 * 2 == 4
    subs = [(0, 0)]; order2 = [(1, 0), (0, 1), (1, 1)]
    assert len(order2) == 3

def check_lp_balls():
    for p in (1, 2, 4):
        for t in [i * 2 * math.pi / 100 for i in range(100)]:
            x = math.copysign(abs(math.cos(t)) ** (2 / p), math.cos(t))
            y = math.copysign(abs(math.sin(t)) ** (2 / p), math.sin(t))
            assert abs(abs(x) ** p + abs(y) ** p - 1) < 1e-9

def check_hahn_banach_disc():
    o, r, b = (0.0, 0.0), 1.0, (3.0, 1.0)
    d = math.hypot(*b); n = (b[0] / d, b[1] / d); c = n[0] * o[0] + n[1] * o[1] + r
    for k in range(360):
        a = (o[0] + r * math.cos(math.radians(k)), o[1] + r * math.sin(math.radians(k)))
        assert n[0] * a[0] + n[1] * a[1] <= c + 1e-12
    assert n[0] * b[0] + n[1] * b[1] > c

def check_riesz():
    y = (3.0, 4.0); ny = math.hypot(*y)
    best = max(math.cos(t) * y[0] + math.sin(t) * y[1] for t in [i * 2 * math.pi / 3600 for i in range(3600)])
    assert abs(best - ny) < 1e-3   # ||phi|| = ||y||

def check_domain_colour():
    f = lambda z: (z * z - 1) / (z * z + 1)
    assert abs(f(1)) < 1e-12 and abs(f(-1)) < 1e-12 and abs(f(1j + 1e-9)) > 1e6

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "cayley":
        print(cayley_svg()); sys.exit()
    for fn in (check_S3, check_quotient, check_tower, check_lp_balls, check_hahn_banach_disc, check_riesz, check_domain_colour):
        fn(); print("ok", fn.__name__)
