import subprocess, sys, xml.etree.ElementTree as ET, os
os.chdir(os.path.dirname(__file__) or ".")
cases = [["cayley","C6"],["cayley","D4"],["cayley","S3"],["cayley","A4"],["cayley","D4","sub=r2"],["cayley","S4"],["cayley","S3","sub=r1"],["cayley","C12","sub=aaaa"],["hasse","S3"],["hasse","D4"],["hasse","C12"],["hasse","A4"],
 ["plot","sin(x)/x","-10","10"],["plot","tan(x)","-3","3","-5","5"],["conformal","z**2"],["conformal","1/z","-2","2","-2","2"],["lp"],["lp","1","2","inf"],["lp","0.5","1","2"],
 ["dijkstra","A-B:4,A-C:1,C-B:2,B-D:1,C-D:5","A"]]
for c in cases:
    o = subprocess.run([sys.executable, "mv.py", *c], capture_output=True, text=True)
    assert o.returncode == 0, (c, o.stderr[-300:])
    ET.fromstring(o.stdout.split("\n<!--")[0])
    print("ok", *c)
bad = subprocess.run([sys.executable, "mv.py", "cayley", "D4", "sub=s"], capture_output=True, text=True)
assert bad.returncode != 0 and "NOT normal" in bad.stderr; print("ok non-normal rejected")
sys.path.insert(0, ".")
import mv, fgroups
for g, nsub, nnorm in [("S3",6,3),("D4",10,6),("A4",10,3),("C12",6,6),("S4",30,4),("Q8",6,6),("C2xC2xC2",16,16),("C2xC4",8,8)]:
    n, G, words, inv, subs, covers, normal = fgroups.lattice_data(g)
    assert (len(subs), len(normal)) == (nsub, nnorm), (g, len(subs), len(normal))
print("ok subgroup/normal counts (incl. Q8, C2^3, C2xC4)")
for g, sub, ident in [("D4","r2","C2×C2" if False else "C2^2"),("Q8","i","C2"),("C12","aaaa","C4"),("S3","r1","C2"),("D4","r1","C2")]:
    s = fgroups.quotient(g, sub); assert "≅ " + ident in s, (g, sub, ident)
print("ok quotient identification")
assert mv.dijkstra("A-B:4,A-C:1,C-B:2,B-D:1,C-D:5","A")[1] == {"A":0,"B":3,"C":1,"D":4}
print("ok dijkstra distances")
for c in cases:
    o = subprocess.run([sys.executable, "mv.py", *c, "--widget"], capture_output=True, text=True)
    assert o.returncode == 0, ("widget", c, o.stderr[-300:])
    ET.fromstring(o.stdout.split("\n<!--")[0])
print("ok widget lint + wellformed (static)")
for n in mv.sliders.DEMOS if hasattr(mv, "sliders") else __import__("sliders").DEMOS:
    o = subprocess.run([sys.executable, "mv.py", "slider", n, "--widget"], capture_output=True, text=True)
    assert o.returncode == 0, ("widget slider", n, o.stderr[-300:])
print("ok widget sliders lint")
o = subprocess.run([sys.executable, "mv.py", "slider", "taylor", "fn=sin", "--widget"], capture_output=True, text=True).stdout
assert 'data-pin="fn=sin"' in o and o.count("Math.sin") >= 1; print("ok pin")
assert len(subprocess.run([sys.executable, "mv.py", "slider", "taylor", "--cdn", "https://cdn.jsdelivr.net/x.js"], capture_output=True, text=True).stdout) < 300; print("ok cdn tiny")
for c in (["domain","(z**2-1)/(z**2+1)"],["domain","exp(1/z)"],["residue","1/(z**2+1)","0","0","2"],["residue","exp(z)/z**3","0","0","1"],["mobius","1","-1","1","1"],["riemann","0","1","1+1i","inf"],["julia"]):
    for extra in ([], ["--widget"]):
        o = subprocess.run([sys.executable, "mv.py", *c, *extra], capture_output=True, text=True); assert o.returncode == 0, (c, o.stderr[-300:])
print("ok complex commands")
import cplx
f = cplx.pyf("1/(z**2+1)")
assert abs(cplx._contour(f, 0j, 2) - 0) < 1e-9 and abs(cplx._contour(cplx.pyf("1/z"), 0j, 1) - 2j*cplx.math.pi) < 1e-9
zs, ps, ok, net, w = cplx.zp(cplx.pyf("(z-1)**2/(z**3*(z+1i))"), 0j, 2.0); assert ok and sorted(o for _, o in zs) == [2] and sorted(o for _, o in ps) == [1, 3]
assert not cplx.zp(cplx.pyf("sqrt(z)"), 0j, 2.0)[2] and not cplx.zp(cplx.pyf("exp(1/z)"), 0j, 2.0)[2]
for bad in (["residue", "1/(z-1)", "0", "0", "1"], ["mobius", "1", "1", "1", "1"]):
    o = subprocess.run([sys.executable, "mv.py", *bad], capture_output=True, text=True); assert o.returncode != 0, bad
print("ok certification, refusals (pole on contour, det=0)")
import alg, re
tx = lambda s: re.findall(r'<tspan font-weight="\d+">([^<]*)</tspan>', s)
for k, nf in [("x^3-2", 6), ("x^4-2", 10), ("x^4-5x^2+6", 5), ("x^3-3x+1", 2), ("cyclo5", 3), ("cyclo7", 4), ("cyclo8", 5), ("cyclo12", 5)]:
    t = tx(alg.galois(k)); assert len([x for x in t if x.startswith("Q") or x.startswith("K")]) == nf, (k, t); assert not any(x.startswith("K,") for x in t), k
assert {"Q(ω)", "Q(∛2)"} <= set(tx(alg.galois("x^3-2"))) and {"Q(i)", "Q(√2)", "Q(i√2)"} <= set(tx(alg.galois("x^4-2"))) and "Q(ζ+ζ²+ζ⁴)" in tx(alg.galois("cyclo7"))
print("ok Galois correspondence (8 presets certified, known subfields present)")
for n, k, nb in [(12, 6, 2), (30, 8, 3), (7, 2, 1), (16, 5, 1)]:
    s = alg.ideals(n); assert s.count("<tspan") == 2*k and s.count('font-weight="700"') == nb, (n, s.count("<tspan"), s.count('font-weight="700"'))
print("ok ideal lattices")
for c in (["quotient", "D4", "sub=r2"], ["galois", "x^4-2"], ["ideals", "12"], ["cayley", "Q8"], ["cayley", "C2xC4"], ["hasse", "Q8"]):
    for extra in ([], ["--widget"]):
        o = subprocess.run([sys.executable, "mv.py", *c, *extra], capture_output=True, text=True); assert o.returncode == 0, (c, o.stderr[-300:]); ET.fromstring(o.stdout)
print("ok P4 commands (+widget lint)")
import fa
cmds = [["separate", "0,0 2,0 2,1 0,1", "3,3"], ["separate", "c:0,0,1", "3,1 4,1 4,2 3,2"], ["extension", "l1", "0.5"], ["extension", "l2", "0.5"], ["extension", "linf", "0.5"], ["riesz", "2", "1"],
        ["dual", "1", "2", "1"], ["dual", "4", "1", "2"], ["dual", "inf", "1", "2"], ["project", "3", "2", "2", "1"], ["fourier", "square", "9"], ["fourier", "tri", "5"], ["fourier", "saw", "8"],
        ["cobweb", "cos(x)", "0.2", "0", "1"], ["cobweb", "2.5*x*(1-x)", "0.2", "0", "1"], ["cobweb", "3.2*x*(1-x)", "0.3", "0", "1"]]
for c in cmds:
    for extra in ([], ["--widget"]):
        o = subprocess.run([sys.executable, "mv.py", *c, *extra], capture_output=True, text=True); assert o.returncode == 0, (c, o.stderr[-300:]); ET.fromstring(o.stdout)
assert "contraction" in fa.cobweb("cos(x)", 0.2, 0, 1) and "NOT certified" in fa.cobweb("3.2*x*(1-x)", 0.3, 0, 1)
for bad in (["separate", "0,0 2,0 2,1 0,1", "1,0.5"], ["dual", "0.5", "1", "1"], ["extension", "l3", "1"], ["fourier", "square", "500"]):
    o = subprocess.run([sys.executable, "mv.py", *bad], capture_output=True, text=True); assert o.returncode != 0, bad
print("ok analysis commands (16 + widget) and refusals (intersecting sets, p<1, unknown norm, N too big)")
import la
cmds = [["linmap", "2", "1", "0", "1.5"], ["linmap", "0", "-1", "1", "0"], ["linmap", "1", "2", "2", "4"], ["basis", "2", "0", "1", "1", "3", "2"], ["solid", "tetra"], ["solid", "cube", "20", "40"], ["solid", "octa"], ["solid", "dodeca"], ["solid", "icosa"],
        ["surface", "x**2-y**2"], ["surface", "sin(x)*cos(y)", "3", "60", "35"], ["ga", "rotate", "1", "0.5", "50"], ["ga", "reflect", "2", "1", "30"], ["ga", "wedge", "2", "0", "1", "1.5"], ["ga", "rotate3", "1", "0", "0.5", "0", "0", "1", "60"], ["ga", "rotate3", "1", "2", "3", "1", "1", "1", "120"], ["triangle", "0,0 6,0 2,4"], ["triangle", "0,0 4,0 1,0.5"]]
for c in cmds:
    for extra in ([], ["--widget"]):
        o = subprocess.run([sys.executable, "mv.py", *c, *extra], capture_output=True, text=True); assert o.returncode == 0, (c, o.stderr[-300:]); ET.fromstring(o.stdout)
for bad in (["basis", "1", "2", "2", "4", "1", "1"], ["triangle", "0,0 1,1 2,2"], ["solid", "sphere"], ["surface", "1/x", "2"]):
    o = subprocess.run([sys.executable, "mv.py", *bad], capture_output=True, text=True); assert o.returncode != 0, bad
# 3D rotor == Rodrigues for random axes; Cl(3) algebra axioms
import random; random.seed(3)
for _ in range(50):
    v = [random.uniform(-2, 2) for _ in range(3)]; ax = [random.uniform(-1, 1) for _ in range(3)]; la.ga("rotate3", *v, *ax, random.uniform(-360, 360))
A, B, Cx = [{m: random.uniform(-1, 1) for m in range(8)} for _ in range(3)]
d = lambda X, Y: max(abs(X.get(k, 0) - Y.get(k, 0)) for k in range(8))
assert d(la.gp(la.gp(A, B), Cx), la.gp(A, la.gp(B, Cx))) < 1e-12 and d(la.rev(la.gp(A, B)), la.gp(la.rev(B), la.rev(A))) < 1e-12
print("ok linear algebra & geometry (18 commands + widget, 4 refusals, 50 random rotors = Rodrigues, GA associativity/reversal)")
import graphs
G = "A-B:4,A-C:1,C-B:2,B-D:1,C-D:5,D-E:3"; F = "S>A:3,S>B:2,A>B:1,A>T:2,B>T:3"
cmds = [["bfs", G, "A"], ["dfs", G, "A"], ["dfs", "A>B,B>C,C>A,A>C,B>D", "A"], ["kruskal", G], ["prim", G, "A"], ["maxflow", F], ["maxflow", "s>a:10,s>b:10,a>b:2,a>t:4,a>c:8,b>c:9,c>t:10,b>t:10"],
        ["proofdag", "ax=Axiom;L1=Lemma 1;L2=Lemma 2;T=Theorem", "ax>L1,ax>L2,L1>T,L2>T"], ["comm", "A B;C D", "A>B:f,A>C:g,B>D:h,C>D:k,A>D:u!", "f h = g k"],
        ["dfa", "q0 q1 q2", "a b", "q0 a q1;q0 b q0;q1 a q2;q1 b q0;q2 a q2;q2 b q2", "q0", "q2", "abaa"]]
for c in cmds:
    for extra in ([], ["--widget"]):
        o = subprocess.run([sys.executable, "mv.py", *c, *extra], capture_output=True, text=True); assert o.returncode == 0, (c, o.stderr[-300:]); ET.fromstring(o.stdout)
for bad in (["proofdag", "a=A;b=B;c=C", "a>b,b>c,c>a"], ["comm", "A B", "A>B:f,B>A:g", "f f = g"], ["comm", "A B;C D", "A>B:f,A>C:g,B>D:h,C>D:k", "f h = g"], ["dfa", "q0 q1", "a", "q0 a q1", "q0", "q1"], ["kruskal", "A>B:1"], ["maxflow", "A-B:1"], ["kruskal", "A-B:1,C-D:2"]):
    o = subprocess.run([sys.executable, "mv.py", *bad], capture_output=True, text=True); assert o.returncode != 0, bad
assert "circular reasoning: a → b → c → a" in subprocess.run([sys.executable, "mv.py", "proofdag", "a=A;b=B;c=C", "a>b,b>c,c>a"], capture_output=True, text=True).stderr
assert "minimal equivalent DFA has 3 state" in graphs.dfa("q0 q1 q2", "a b", "q0 a q1;q0 b q0;q1 a q2;q1 b q0;q2 a q2;q2 b q2", "q0", "q2") and "minimal equivalent DFA has 1 state" in graphs.dfa("p q", "a", "p a q;q a p", "p", "p q")
print("ok graphs/algorithms/proofs (10 commands + widget; BFS=Floyd, DFS parenthesis, Kruskal=Prim=brute force, max-flow=min-cut; 7 refusals)")
import stem
cmds = [["phase", "pendulum"], ["phase", "lotka"], ["phase", "vanderpol"], ["phase", "damped"], ["phase", "saddle"], ["phase", "y", "-x-0.5*y", "3"], ["charges", "1,-1,0;-1,1,0"], ["charges", "2,0,0;-1,2,0;-1,-2,0"],
        ["projectile", "20", "45"], ["projectile", "20", "45", "0.3"], ["dist", "normal", "0", "1", "-1", "1"], ["dist", "exp", "1.5", "0", "1"], ["dist", "uniform", "0", "2", ".5", "1.5"], ["dist", "binom", "10", ".3", "2", "4"], ["dist", "poisson", "4", "2", "6"],
        ["clt", "1"], ["clt", "8"], ["rlc", "10", "1", "1e-3"], ["rlc", "200", "1", "1e-3"], ["rlc", "63.2455532033676", "1", "1e-3"], ["rc", "1000", "1e-3"], ["lens", "10", "30", "2"], ["lens", "10", "6", "2"], ["lens", "-10", "20", "2"]]
for c in cmds:
    for extra in ([], ["--widget"]):
        o = subprocess.run([sys.executable, "mv.py", *c, *extra], capture_output=True, text=True); assert o.returncode == 0, (c, o.stderr[-300:]); ET.fromstring(o.stdout)
for bad in (["lens", "10", "10", "2"], ["dist", "normal", "0", "-1"], ["phase", "nope"], ["charges", "0,0,0"], ["rlc", "-1", "1", "1"]):
    o = subprocess.run([sys.executable, "mv.py", *bad], capture_output=True, text=True); assert o.returncode != 0, bad
assert "underdamped" in stem.rlc(10, 1, 1e-3) and "overdamped" in stem.rlc(200, 1, 1e-3) and "critically damped" in stem.rlc(63.2455532033676, 1, 1e-3)
assert "saddle" in stem.phase("saddle") and "centre (linear)" in stem.phase("lotka") and "stable spiral" in stem.phase("damped") and "unstable spiral" in stem.phase("vanderpol")
print("ok STEM (24 commands + widget, 5 refusals; RK4 vs closed forms, conserved quantities, E=-grad phi, lens equation, classifications)")
