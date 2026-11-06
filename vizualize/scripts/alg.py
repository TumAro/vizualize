"""Galois correspondence and ring-ideal lattices (stdlib only).
Galois: for a preset splitting field L/Q the group G acts on the roots (permutations). A subgroup H gets the field K^H = Q(S), S = named elements fixed by H,
and the name is accepted ONLY if Stab(S) == H (then Q(S) = K^H exactly, by the fundamental theorem). Also asserted: |G| = [L:Q],
every named element's orbit polynomial has rational coefficients, [K^H:Q] = [G:H]."""
import cmath, math
from fractions import Fraction
from itertools import combinations
from base import *
from fgroups import mul, idn, closure, order, subgroups, draw_lattice, identify
Z = lambda n, k: cmath.exp(2j*math.pi*k/n)
def _cyclo(n, gens_units):
    ks = [k for k in range(1, n) if math.gcd(k, n) == 1]; ix = {k: i for i, k in enumerate(ks)}
    sup = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")
    return dict(deg=len(ks), roots=[Z(n, k) for k in ks], names=["ζ" + (str(k).translate(sup) if k > 1 else "") for k in ks],
                gens=[tuple(ix[(u*k) % n] for k in ks) for u in gens_units], extra={"ζ²": lambda r: r[0]*r[0], "ζ³": lambda r: r[0]**3})
PRE = {
 "x^3-2": dict(deg=6, roots=[2**(1/3)*Z(3, k) for k in range(3)], names=["∛2", "ω∛2", "ω²∛2"], gens=[(1, 2, 0), (0, 2, 1)], extra={"ω": lambda r: r[1]/r[0]}),
 "x^4-2": dict(deg=8, roots=[2**.25*Z(4, k) for k in range(4)], names=["⁴√2", "i⁴√2", "−⁴√2", "−i⁴√2"], gens=[(1, 2, 3, 0), (0, 3, 2, 1)],
               extra={"i": lambda r: r[1]/r[0], "√2": lambda r: r[0]*r[0], "i√2": lambda r: r[0]*r[1]}),
 "x^4-5x^2+6": dict(deg=4, roots=[2**.5, -2**.5, 3**.5, -3**.5], names=["√2", "−√2", "√3", "−√3"], gens=[(1, 0, 2, 3), (0, 1, 3, 2)], extra={"√6": lambda r: r[0]*r[2]}),
 "x^3-3x+1": dict(deg=3, roots=[2*math.cos(2*math.pi*k/9) for k in (1, 2, 4)], names=["2cos(2π/9)", "2cos(4π/9)", "2cos(8π/9)"], gens=[(1, 2, 0)], extra={}),
 "cyclo5": _cyclo(5, [2]), "cyclo7": {**_cyclo(7, [3]), "extra": {"ζ²": lambda r: r[0]*r[0], "ζ+ζ²+ζ⁴": lambda r: r[0]+r[1]+r[3]}}, "cyclo8": _cyclo(8, [3, 5]), "cyclo12": _cyclo(12, [5, 7]),
}
def cstr(p):
    seen, out = set(), []
    for i in range(len(p)):
        if i in seen or p[i] == i: continue
        c, j = [], i
        while j not in seen: seen.add(j); c.append(j+1); j = p[j]
        out.append("(" + " ".join(map(str, c)) + ")")
    return "".join(out) or "e"
def galois(key):
    assert key in PRE, "presets: " + " | ".join(PRE)
    P = PRE[key]; r, n = P["roots"], len(P["roots"]); G = closure(P["gens"], n)
    assert len(G) == P["deg"], f"|G|={len(G)} but [L:Q]={P['deg']}"
    act = lambda g: [r[g[i]] for i in range(n)]                       # automorphism g sends root i to root g(i)
    # candidate field elements: (name, function of the root list), simplest first
    S = [(nm, (lambda i: lambda rr: rr[i])(i)) for i, nm in enumerate(P["names"])] + [(k, f) for k, f in P["extra"].items()]
    S += [((f"{P['names'][i]}+{P['names'][j]}").replace("+−", "−"), (lambda i, j: lambda rr: rr[i]+rr[j])(i, j)) for i, j in combinations(range(n), 2)]
    subs = sorted(subgroups(G, n), key=lambda s: (-len(s), sorted(s)))
    for H in subs:                                                   # trace of each root over H: fixed by H by construction
        if 1 < len(H) < len(G):
            for i in range(n): S.append((f"Tr⟨{','.join(sorted({cstr(h) for h in H if h != idn(n)})[:2])}⟩({P['names'][i]})", (lambda H, i: lambda rr: sum(rr[h[i]] for h in H))(H, i)))
    val = lambda f, g: f(act(g))
    fixed_by = lambda f, g: abs(val(f, g) - f(r)) < 1e-8
    for nm, f in S[:len(P["names"]) + len(P["extra"]) + n*(n-1)//2]:     # rationality of orbit polynomials (named base elements)
        orb = []
        for g in G:
            v = val(f, g)
            if all(abs(v - w) > 1e-8 for w in orb): orb.append(v)
        co = [1+0j]
        for v in orb: co = [a - v*b for a, b in zip(co + [0], [0] + co)]
        for c in co: assert abs(c.imag) < 1e-7 and abs(c.real - Fraction(c.real).limit_denominator(2000)) < 1e-7, f"orbit polynomial of {nm} not rational: Galois group wrong"
    stab = lambda els: frozenset(g for g in G if all(fixed_by(f, g) for _, f in els))
    nodes, label = {}, {}
    for H in subs:
        fx = [(nm, f) for nm, f in S if all(fixed_by(f, h) for h in H)]; got = None
        if len(H) == len(G): got = []
        else:
            for k in (1, 2):
                for sub in combinations(fx, k):
                    if stab(sub) == H: got = list(sub); break
                if got is not None: break
        deg = len(G)//len(H)
        if got is not None:
            assert len(G)//len(stab(got)) == deg                       # [K^H:Q] = [G:H]
            name = "Q" if not got else "Q(" + ", ".join(nm for nm, _ in got) + ")"
        else: name = f"K, degree {deg}"
        gs, cur = [], {idn(n)}
        for p in sorted(H, key=lambda p: (order(p), p)):
            if p not in cur: gs.append(p); cur = closure(gs, n)
        hl = "{e}" if len(H) == 1 else ("G" if len(H) == len(G) else "⟨" + ",".join(cstr(p) for p in gs) + "⟩")
        nodes[H] = ([name, hl], all({mul(mul(g, h), tuple(sorted(range(n), key=lambda i: g[i]))) for h in H} == set(H) for g in G))
    covers = [(b, a) for a in subs for b in subs if a < b and not any(a < c < b for c in subs)]       # low = bigger group = smaller field
    edge = {(b, a): f"{len(b)//len(a)}" for b, a in covers}
    names = ", ".join(f"{i+1}={nm}" for i, nm in enumerate(P["names"]))
    note = f"{key}: Gal ≅ {identify(G)}, |G|=[L:Q]={len(G)} ✓ · permutations act on roots {names} · edge label = index · bold = Galois (normal) subfield · top L, bottom Q"
    return draw_lattice({H: (v[0][:1] + [v[0][1]], v[1]) for H, v in nodes.items()}, covers, 470, edge, note)
def ideals(n):
    divs = [d for d in range(1, n+1) if n % d == 0]
    I = {d: frozenset((d*k) % n for k in range(n)) for d in divs}                     # ideal (d) in Z_n, built from the definition
    for d in divs: assert len(I[d]) == n//d and all((a+b) % n in I[d] for a in I[d] for b in I[d]) and all((a*k) % n in I[d] for a in I[d] for k in range(n))
    assert {frozenset((g*k) % n for k in range(n)) for g in range(1, n+1)} == set(I.values())     # every ideal is principal and is one of these
    covers = [(I[a], I[b]) for a in divs for b in divs if I[a] < I[b] and not any(I[a] < I[c] < I[b] for c in divs)]
    prime = lambda d: d > 1 and all(d % q for q in range(2, int(d**.5)+1))
    nodes = {I[d]: ([f"({d})" if d < n else "(0)", f"Z{n}/({d}) ≅ Z{d}" if d > 1 else "0"], prime(d) or (d == n and prime(n))) for d in divs}
    phi = sum(1 for k in range(1, n+1) if math.gcd(k, n) == 1)
    note = f"Z{n}: {len(divs)} ideals (one per divisor) · units φ({n})={phi} · zero divisors {n-phi-1 if n > 1 else 0} · bold = prime = maximal (quotient is a field)"
    return draw_lattice(nodes, covers, 460, None, note)
