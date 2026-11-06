# Geometry & geometric algebra

Contents: constructions · loci · transformations · geometric algebra

## Construction (JSXGraph, interactive)
```html
<script src="https://cdn.jsdelivr.net/npm/jsxgraph@1.12.2/distrib/jsxgraphcore.js"></script>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/jsxgraph@1.12.2/distrib/jsxgraph.css">
<div id="b" class="jxgbox" style="width:100%;aspect-ratio:1"></div>
<script>
const B=JXG.JSXGraph.initBoard('b',{boundingbox:[-5,5,5,-5],axis:true});
const A=B.create('point',[-3,0]),C=B.create('point',[3,0]),P=B.create('point',[0,3]);
B.create('polygon',[A,C,P]);
B.create('circumcircle',[A,C,P]);   // uses built-in constructions: exact, no hand maths
</script>
```
Rule: use built-in JSXGraph elements (`circumcircle`, `perpendicular`, `midpoint`, `intersection`, `angle`) so the construction is exact by definition. Static figure: same coordinates into SVG.
Invariants: all derived points defined from the dragged ones (not typed coordinates); label the property that stays true while dragging (e.g. angle sum 180°, Euler line collinear).

## Geometric algebra (Cl(2) / Cl(3))
Picture rotors, not formulas: rotor R=exp(-Bθ/2)=cos(θ/2) − B sin(θ/2); v' = R v R̃ rotates by θ in the plane of bivector B. Draw: vector v, rotated v', shaded oriented parallelogram for B (bivector = oriented area). a∧b area = |a||b| sinθ; a·b = |a||b| cosθ; ab = a·b + a∧b.
Invariants: |v'|=|v|; rotation angle = θ not θ/2; bivector orientation matches the rotation sense; sign convention stated.

## Generators (preferred over hand-drawing)
- `linmap a b c d`: unit circle -> ellipse; A v_i = σ_i u_i, σ₁σ₂ = |det|, ‖A‖ = σ₁ are asserted; real eigenvectors verified A v = λ v; det = signed area of the image of the unit square.
- `solid <name> [az el]`: vertices exact, **faces found by convex hull**; asserts V−E+F=2, every edge borders exactly 2 faces, all edges equal, dihedral angle matches the known value. Visibility by back-face culling (solid vs dashed). Orthographic projection (no WebGL).
- `surface`: wireframe only, no hidden-line removal (said in the caption).
- `ga`: Cl(3) geometric product implemented from blade bitmasks (associativity and reversal tested). rotate: R = cos(θ/2) − e₁₂ sin(θ/2), v' = R v R̃ equals the counter-clockwise rotation by θ. reflect: v' = −n v n. wedge: ab = a·b + a∧b with a∧b = signed area. rotate3: R = cos(θ/2) − B sin(θ/2), B = n₁e₂₃ + n₂e₃₁ + n₃e₁₂, checked equal to Rodrigues' formula (50 random rotors in the tests).
- `triangle`: O, G, H, N computed; asserts AH ⟂ BC, collinearity, HG = 2·GO, and that all 9 points lie on the circle of radius R/2 about N.
