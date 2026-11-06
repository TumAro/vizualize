---
name: vizualize
description: Fast, rigorous in-chat visualisations for advanced mathematics - abstract algebra (groups, Cayley graphs, subgroup lattices, quotient groups, field extensions and towers, Galois), complex analysis (complex plane, conformal maps, domain colouring, Cauchy integral theorem, residues, contours), geometry and geometric algebra, functional analysis (Hahn-Banach, Riesz representation, norms and unit balls, projections, operators), graphs and graph algorithms, commutative diagrams and proof-structure diagrams, and STEM beyond pure maths (ODE phase portraits and equilibria, probability distributions and the central limit theorem, electric fields, projectile motion, RLC/RC circuits, thin-lens optics). Use whenever the user asks to visualise, draw, picture, sketch, plot, illustrate or "show me" any such concept, or is learning/revising a theorem or proof and a diagram would help, even if they never say "visualisation". Output is inline SVG / Mermaid in chat (JSXGraph only when dragging teaches), never slow renders.
---

# vizualize

Goal: a correct picture on the first try, fast, that raises understanding. Wrong pictures teach wrong maths, so correctness outranks beauty; speed outranks decoration.

## 0a. Where it renders (claude.ai inline visuals)

claude.ai can render HTML/SVG inline in chat (beta since Mar 2026; sliders, hover and click work; not saved to the Artifacts drawer). Hand the generator's fragment to that inline-visual tool: **always add `--widget`** (`mv.py cayley D4 --widget`, `mv.py slider taylor --widget`). `--widget` output follows the inline-widget rules (as reverse-engineered, unofficial): fragment only (no html/head/body), host theme variables with fallbacks so dark mode works, weights 400/500, text >= 11px, no comments/emoji/gradients, no `position:fixed`, scripts only from cdnjs/esm.sh/jsdelivr/unpkg (the generators use none). Slider fragments carry an "Explain this state ↗" button that calls `sendPrompt(...)`, so the learning loop continues in chat. Keep explanatory prose in the chat reply, not inside the widget. If the environment has no inline-visual tool (e.g. plain Claude Code), omit `--widget` and deliver the standalone SVG/HTML file.

## 0b. Token budget (each fragment is paid for twice: tool result + re-emission)

- Pin what the user asked for: `mv.py slider taylor fn=sin --widget` (pinned controls are hidden). Never show options the user did not ask about.
- Static SVG (`cayley`, `hasse`, ...) is 2-7 KB, sliders ~5 KB. Use a slider only when varying a parameter is the lesson; otherwise a static picture.
- Copy the generator output verbatim; do not restyle or re-derive it.
- If the user has published `dev/mv.js` (`mv.py slider bundle`) on jsDelivr, add `--cdn <url>` and the fragment shrinks to ~200 characters.

## 0. Fast path (inline, ~50 ms, self-checked)

If a shell/code sandbox exists, generate instead of hand-drawing: `python3 scripts/mv.py <cmd>` prints a ready SVG (stdlib only, no installs) with the maths computed and asserted inside (group laws, normality, Lagrange, real Dijkstra distances, |x|^p+|y|^p=1). Paste the SVG inline in the reply.

| Need | Command |
|---|---|
| domain colouring + certified zeros/poles (orders) | `mv.py domain "(z**2-1)/(z**2+1)" --widget` |
| contour integral & residues (numeric ∮ must equal 2πi·ΣRes, else refuses) | `mv.py residue "exp(z)/z**3" 0 0 1 --widget` |
| Möbius map: polar grid, image, fixed points | `mv.py mobius 1 -1 1 1 --widget` |
| Riemann sphere (stereographic, ∞ = north pole) | `mv.py riemann 0 1 1+1i inf --widget` |
| Mandelbrot + Julia (click to pick c) | `mv.py julia -0.8 0.156 --widget` |
| Cayley graph: C<n>, D<n>, Q8, S3..S5, A4, products (`C2xC4`, `D4xC2`), up to order 60 | `mv.py cayley Q8` |
| quotient group G/N drawn as its own Cayley graph, identified (C4, C2², Q8…); refuses non-normal N | `mv.py quotient D4 sub=r2` |
| Galois correspondence: subgroups ↔ fixed fields, certified (x^3-2, x^4-2, x^4-5x^2+6, x^3-3x+1, cyclo5/7/8/12) | `mv.py galois x^4-2 --widget` |
| ideal lattice of Z_n with quotient rings, primes bold, φ(n), zero divisors | `mv.py ideals 12` |
| quotient: colour cosets of a normal subgroup (refuses if not normal) | `mv.py cayley D4 sub=r2` , `mv.py cayley C12 sub=aaaa` |
| subgroup lattice (complete, Lagrange-checked), normal ones bold | `mv.py hasse S4` |
| function plot (breaks at poles) | `mv.py plot "sin(x)/x" -10 10` |
| z-plane grid vs image under f | `mv.py conformal "1/z"` |
| ℓp unit balls (p<1 flagged non-convex) | `mv.py lp 1 2 inf` |
| Hahn–Banach separation (polygon/disc/point; certificate via support functions; refuses intersecting sets) | `mv.py separate "0,0 2,0 2,1 0,1" 3,3 --widget` |
| Hahn–Banach extension: wedge of norm-preserving extensions (ℓ1 wedge, ℓ2/ℓ∞ unique) | `mv.py extension l1 0.5 --widget` |
| Riesz representation: level lines, kernel, ‖φ‖=‖y‖ | `mv.py riesz 2 1 --widget` |
| ℓp–ℓq duality: where ‖φ‖ is attained, ‖φ‖=‖(a,b)‖_q | `mv.py dual 4 1 2 --widget` |
| orthogonal projection + Pythagoras | `mv.py project 3 2 2 1 --widget` |
| Fourier partial sums, Gibbs, Parseval check | `mv.py fourier square 9 --widget` |
| Banach fixed-point cobweb with a-priori bound (says so when not a contraction) | `mv.py cobweb "cos(x)" 0.2 0 1 --widget` |
| 2×2 linear map: grid image, SVD ellipse, eigenlines, det = area (A V = U Σ asserted) | `mv.py linmap 2 1 0 1.5 --widget` |
| change of basis: coordinates of x in basis (b1, b2) | `mv.py basis 2 0 1 1 3 2 --widget` |
| Platonic solids (faces from the hull, Euler V−E+F=2, dihedral angle, hidden edges dashed; tetra cube octa dodeca icosa) | `mv.py solid dodeca 35 25 --widget` |
| surface z=f(x,y) wireframe | `mv.py surface "x**2-y**2" --widget` |
| geometric algebra: rotor rotation (Cl2), reflection, a∧b area, 3D rotor = Rodrigues (Cl3) | `mv.py ga rotate 1 0.5 50 --widget` , `mv.py ga rotate3 1 0 .5 0 0 1 60` |
| triangle: circumcircle, Euler line (HG = 2GO), nine-point circle with 9 verified points | `mv.py triangle "0,0 6,0 2,4" --widget` |
| BFS / DFS (discovery/finish times, tree/back edges) | `mv.py bfs "A-B,A-C,B-D" A --widget` |
| Kruskal / Prim MST, max flow = min cut (Edmonds–Karp), Dijkstra: all frame strips with independent cross-checks | `mv.py kruskal "A-B:4,A-C:1,C-B:2" --widget` , `mv.py maxflow "S>A:3,S>B:2,A>T:2,B>T:3" --widget` |
| proof dependency DAG; **refuses circular reasoning** and names the cycle | `mv.py proofdag "ax=Axiom;L1=Lemma 1;T=Theorem" "ax>L1,L1>T" --widget` |
| commutative diagram (grid text spec), paths type-checked, ⟳ on commuting faces, dashed ∃! arrows | `mv.py comm "A B;C D" "A>B:f,A>C:g,B>D:h,C>D:k" "f h = g k" --widget` |
| DFA: totality, trace of an input, minimal state count | `mv.py dfa "q0 q1" "a b" "q0 a q1;q0 b q0;q1 a q1;q1 b q0" q0 "q1" abab --widget` |
| ODE phase portrait (equilibria classified by trace/det, nullclines, RK4 checked, conserved quantity checked): presets pendulum lotka vanderpol damped saddle or custom `x' y'` | `mv.py phase pendulum --widget` , `mv.py phase "y" "-x-0.5*y" 3 --widget` |
| electric field lines of point charges (E = −∇φ checked) | `mv.py charges "1,-1,0;-1,1,0" --widget` |
| projectile with optional linear drag (RK4 = closed form, optimal angle) | `mv.py projectile 20 45 0.3 --widget` |
| distributions normal/binom/poisson/exp/uniform with P(a≤X≤b); CLT with exact dice convolution | `mv.py dist normal 0 1 -1 1 --widget` , `mv.py clt 8 --widget` |
| series RLC step response + poles + damping class; RC charging | `mv.py rlc 10 1 1e-3 --widget` , `mv.py rc 1000 1e-3 --widget` |
| thin lens ray diagram, image from two rays = lens equation | `mv.py lens 10 6 2 --widget` |
| Dijkstra frame strip | `mv.py dijkstra "A-B:4,A-C:1,C-B:2" A` |

Interactive (sliders, offline single-file HTML, invariant badge on screen): `mv.py slider pythagoras|quadratic|sine|taylor|epsdelta|eigen|riemann` -> deliver the HTML as an artifact. Use it when varying a parameter is the lesson; use static SVG otherwise (faster, truly inline).

No sandbox, or the case is not listed: write the SVG/Mermaid by hand from the reference templates. Same invariants apply. Never run a command twice to "see" it; the asserts already did the checking.

## 1. Route (pick ONE format, then read ONE reference file)

| Topic | Format | Read |
|---|---|---|
| groups, quotients, lattices, field towers, Galois | `mv.py` SVG, or Mermaid | references/abstract-algebra.md |
| complex plane, conformal maps, Cauchy, residues, domain colouring | `mv.py conformal`, SVG; JSXGraph if dragging teaches; canvas shader for colouring | references/complex-analysis.md |
| Euclidean/analytic geometry, geometric algebra | JSXGraph or SVG | references/geometry-ga.md |
| norms, Hahn-Banach, Riesz, projections, operators | `mv.py lp`, SVG schematic labelled "analogue in R^n" | references/functional-analysis.md |
| graphs, BFS/DFS/Dijkstra, trees, flows | Mermaid; `mv.py dijkstra` | references/graphs-algorithms.md |
| proof structure, commutative diagrams | Mermaid; SVG for labelled arrows | references/proofs-diagrams.md |
| physics/engineering/probability: ODE phase planes, charges, projectile, distributions, CLT, RLC, lens | generators | references/stem.md |
| function plots / surfaces | `mv.py plot`; matplotlib only if SVG cannot | (none) |

Ladder (stop at first that works): generator -> Mermaid -> hand SVG -> JSXGraph artifact (pinned `jsxgraph@1.12.2`) -> matplotlib. Never MathBox/Manim. Prefer inline output; an artifact only for real interactivity.

## 2. Correctness protocol (the "never wrong" guarantee)

Before drawing, write a 2-4 line **invariant list** (e.g. `|G/N| = |G|/|N|`, tower degrees multiply, a-arrows form cycles of length ord(a), contour encloses exactly the listed poles). Then:
1. Derive data by computing, never by eye. Generators do this for you; by hand, compute step by step.
2. Tick each invariant against the finished picture. Fix before replying.
3. Abstract objects have no true geometry: draw the faithful structure (graph, lattice, diagram). Anything schematic says "analogue in R^n".
4. No honest picture exists -> say so and draw the closest structural object.
5. Convention stated once (right multiplication g->g·a; counter-clockwise contours; Hasse = maximal inclusions).

## 3. Response shape (keep it short)

1. One-line statement of what is drawn.
2. The visual (SVG/Mermaid in a code block or artifact).
3. "Read it like this": 3-5 bullets mapping picture elements to maths objects.
4. One line: invariants checked, and what is schematic.
Give a full proof or derivation only if asked.

## 4. SVG mechanics (copy these, don't reinvent)

- `viewBox="0 0 400 300"`, `width="100%"`, no fixed pixels, so it fits any chat.
- Colours via `currentColor` and a few CSS-free hex values readable on light AND dark: stroke `#888`, accents `#e45`, `#27c`, `#2a7`. Text `fill="currentColor"`.
- Arrowhead once: `<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0L10,5L0,10z" fill="context-stroke"/></marker></defs>`, use `marker-end="url(#a)"`.
- y axis is flipped in SVG: use `y_svg = cy - k*y_math`.
- Label every node and every arrow colour class. A legend of <= 4 entries.
- Maths in labels: Unicode (ℤ, ℚ, ⟨, ⟩, √, ≅, ⊴, ∮), no LaTeX in SVG.

## 5. Reuse before inventing

Prefer established conventions: Group Explorer (arrow colour per generator, translucent boxes around cosets), the JSXGraph example wiki for constructions, standard HSV domain colouring. Run `python3 scripts/test_mv.py && python3 scripts/checks.py` (dev: `dev/tools/widget_host.js` renders fragments in a simulated host, light+dark) after editing any generator or template.
