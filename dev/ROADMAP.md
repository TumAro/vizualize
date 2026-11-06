# vizualize roadmap

Design edge vs. other tools: ChatGPT's visual modules = ~70 fixed concepts with sliders/draggable points. GPAI markets an "AI visualizer" but users report wrong diagrams. vizualize target = **computed + asserted + inline + fast**, covering advanced topics those tools skip. Every generator ships with asserts and a test; every phase ends with a rendered contact sheet checked by eye (`dev/tools/shot.js`).

## Done
- Phase 0 – skill + router, 6 reference files, invariant protocol.
- Phase 1 – `scripts/mv.py`: cayley (+quotient), hasse, plot, conformal, lp balls, dijkstra. Rendered and fixed (layout, legend, crowding).

- Phase 2 – `scripts/sliders.py` (`mv.py slider`): 7 offline interactive demos, each with an on-page invariant badge; `dev/tools/test_sliders.js` sweeps 500 random slider states per demo in headless Chromium and screenshots.

- Phase 2.5 – inline-widget mode: `--widget` on every command (theme vars, lint rules from the claude.ai inline-visuals guidelines, sendPrompt button); `dev/tools/widget_host.js` simulates the host in light+dark and sweeps invariants (20/20 pass). Caveat: widget rules are reverse-engineered (github.com/Michaelliv/pi-generative-ui); confirm in claude.ai.

- Phase 2.6 – token diet + fixes: SVG compactor (ints, paths, shared classes: 40 KB -> 5.7 KB for conformal), slider framework rewritten (pins `k=v`, no gap, centred max-width), `--cdn` tiny fragment + `slider bundle`.

- Phase 3 – complex analysis: `scripts/cplx.py` (domain colouring with argument-principle-certified zeros/poles, residue/contour checker, Möbius, Riemann sphere, Mandelbrot/Julia). Evaluator parity test `dev/tools/test_cplx.js`.

- Phase 4 – algebra: `fgroups.py` (Q8, products, S5-size groups, complete subgroup lattice, quotient-as-Cayley with homomorphism checks, group identification), `alg.py` (Galois correspondence for 8 certified presets, Z_n ideal lattices). Note: module `grp` clashes with a stdlib module, hence `fgroups`.

- Phase 5 – analysis & functional analysis: `scripts/fa.py` (separation, HB extension wedge, Riesz, ℓp duality, projection, Fourier, cobweb), all certified, 16 commands tested.

- Phase 6 – linear algebra & geometry: `scripts/la.py` (SVD/linmap, basis, Platonic solids via hull, surface wireframe, Cl(3) geometric algebra, triangle centres). 18 commands tested.

- Phase 7 – graphs/discrete/proofs: `scripts/graphs.py` (BFS, DFS, Kruskal, Prim, Edmonds–Karp, proof DAG with cycle refusal, commutative diagrams, DFA). Planarity deferred (needs DMP planarity + Kuratowski witness).

- Phase 8 – STEM: `scripts/stem.py` (phase portraits, charges, projectile, distributions, CLT, RLC/RC, thin lens); `references/stem.md`.

- Phase 9 – quality gate: `dev/check.py` (certificate tests, 139-command golden regression with determinism and size budget, simulated claude.ai host light+dark: 234 page checks, slider sweeps, JS/Python evaluator parity; all pass). Trigger eval: `dev/trigger_eval.json`; 3-iteration optimisation kept the original description (train 10/14, held-out 4/6) - misses not yet analysed.

## Next (each phase = 1 session, independently shippable)
- ~~P2 Interactive slice (ChatGPT parity):~~ DONE (7 demos; add more by appending `demo(...)` in sliders.py): `mv.py slider` -> single-file HTML, vanilla JS + SVG, no CDN (instant, offline): Pythagoras, quadratic/parabola, sin(ax+b), Taylor polynomial vs f, epsilon-delta, eigen-ellipse of 2x2, Riemann sums. Reuse JSXGraph only for geometry constructions.
- ~~P3 Complex analysis:~~ DONE: domain colouring as HTML canvas generator (`mv.py domain "f(z)"`), Riemann sphere / stereographic, Möbius fixed points, contour + residue picture with computed residues (numeric contour integral asserted = 2πi ΣRes), Julia/Mandelbrot.
- ~~P4 Algebra depth:~~ DONE: field towers/Galois generator (subfield lattice from polynomial via sympy if present, hard-coded table fallback), more groups (Q8, S5 lattice, Z_n×Z_m, GL2(F2)), ring/ideal lattices, Z_n unit-group cycle graph, permutation cycle diagrams, quotient *collapsed* view.
- ~~P5 Analysis & functional analysis:~~ DONE: unit-ball duality (ℓp vs ℓq), Hahn–Banach separating-line generator for polygon/disc + point, Riesz level sets, projection onto subspace, spectrum/pseudospectrum of 2x2/3x3, Fourier partial sums, Banach fixed-point cobweb.
- ~~P6 Linear algebra & geometry:~~ DONE: SVD ellipse, linear map grid, change of basis, quadric slices, GA rotor/bivector pictures, 3D via orthographic SVG projection (no WebGL).
- ~~P7 Graphs/discrete/proofs:~~ DONE (planarity still open): BFS/DFS/Kruskal/Prim/max-flow frame strips, planarity check, automata, commutative-diagram SVG generator from text spec, proof-DAG with cycle detection.
- ~~P8 STEM beyond maths:~~ DONE: physics (fields, vector plots, phase portraits, Lagrangian orbits), probability (distributions, CLT), ODE phase planes (RK4 with asserted energy drift), circuits/free-body schematics.
- **P9 Quality gate:** golden-image regression (render all generators, diff), cross-check numerics against independent formula, trigger-description tuning with eval queries, packaging script.

## Rules for every generator
1. Compute, never place by eye. 2. Assert the defining property inside the generator. 3. Refuse (non-zero exit + message) rather than draw something false. 4. stdlib only; <100 ms; output ≤ ~15 KB SVG. 5. Add to `test_mv.py` and the router table in SKILL.md.

## Dev tooling (not shipped in the skill zip)
`dev/tools/shot.js` renders HTML/SVG to PNG with headless Chromium (Playwright installed in the session scratchpad; reinstall: `npm i playwright && npx playwright install chromium`).
