# Functional analysis

Rule: infinite-dimensional objects have no honest picture. Draw the **ℝ² / ℝ³ analogue** and say so in one clause. The picture illustrates the mechanism, the statement is the theorem.

Contents: ℓp unit balls · Hahn–Banach · Riesz · projection · operators

## Unit balls of ℓp in ℝ² (SVG)
{x : |x|^p+|y|^p ≤ 1}. Parametrise: x=sgn(cos t)|cos t|^{2/p}, y=sgn(sin t)|sin t|^{2/p}, t∈[0,2π], emit ~100 points as `<polyline>`. p=1 diamond, p=2 circle, p=∞ square; p<1 non-convex (not a norm!). Draw p=1,2,∞ nested; scale on the axes.
Invariants: all pass through (±1,0),(0,±1) (p<∞); nested ℓ1 ⊂ ℓ2 ⊂ ℓ∞; p<1 star-shaped but not convex, so fails triangle inequality.

## Hahn–Banach (geometric form, ℝ² analogue)
Statement drawn: closed convex A and a point/convex set B disjoint (one open) are separated by a hyperplane: ∃ f, c with f(a) ≤ c ≤ f(b). Picture: shaded convex set A, point b outside, line {f=c} between them, normal vector f drawn.
Construction for point b and a disc A (centre o, radius r): normal n=(b-o)/|b-o|, place line at distance r from o along n: {x : n·x = n·o + r}. Then n·a ≤ n·o + r for all a∈A and n·b > that value.
Analytic form (extension): f defined on subspace M, dominated by sublinear p; draw M as a line, f as its graph, and the extension as a plane through it staying below p (cone). Label "ℝ³ analogue".
Invariants: separating line has A strictly on one side, b on the other; for the extension, f_ext|M=f and f_ext ≤ p everywhere.

## Riesz representation (Hilbert, ℝ² analogue)
Every bounded linear functional φ is φ(x)=⟨x,y⟩ for a unique y with ‖φ‖=‖y‖. Picture: vector y, level lines {x: ⟨x,y⟩=c} are lines **perpendicular to y**, spaced 1/‖y‖ per unit of c; ker φ is the line through 0 perpendicular to y; the unit ball's maximum of φ is attained at y/‖y‖ giving ‖y‖.
Invariants: level lines ⟂ y; ‖φ‖=‖y‖ (the sup over the unit circle appears as touching point); spacing of c=0,1,2 lines = 1/‖y‖. Counterpoint: on ℓ1 the dual is ℓ∞, so the ball geometry (diamond vs square) swaps; this is why Riesz needs an inner product.

## Orthogonal projection
Point x, closed subspace M (a line): P x = foot of the perpendicular; x−Px ⟂ M; ‖x‖²=‖Px‖²+‖x−Px‖² (Pythagoras). Show the right-angle mark.

## Operators
Spectrum / mapping pictures: draw the image of the unit circle under a 2x2 matrix (ellipse, semi-axes = singular values; ‖T‖ = largest). Compute singular values from eigenvalues of TᵀT.

## Generators (preferred over hand-drawing)
All are finite-dimensional analogues (ℝ²) and say so; each carries a numeric certificate and refuses rather than draw something false.
- `separate A B`: closest pair by alternating projections, then **verified with exact support functions**: sup_A f ≤ c ≤ inf_B f with gap = distance. Intersecting sets are refused (strict separation needs a positive gap).
- `extension l1|l2|linf t`: norm-preserving extensions F=(t,s) of f(x)=t·x₁ from the x-axis are exactly the points of the dual-norm sphere of radius |t| on the line {F₁=t}. For ℓ1 the dual is the ℓ∞ square, whose side lies on that line → a wedge s∈[−|t|,|t|]; for ℓ2 (circle) and ℓ∞ (dual ℓ1 diamond, met at a vertex) → a single point. The generator computes s from the ball and asserts agreement with this theory.
- `riesz y1 y2`, `dual p a b`: ‖φ‖ is recomputed as a supremum over the ball and equated with ‖y‖ (Hilbert) or ‖(a,b)‖_q with 1/p+1/q=1 (ℓp).
- `project`: ⟨x−Px,u⟩=0, Pythagoras, and the minimum distance is checked by brute force.
- `fourier`: numeric coefficients must match the closed forms, and Parseval/Bessel (‖f−S_N‖² = ‖f‖² − π(a₀²/2+Σ(aₖ²+bₖ²))) must hold; Gibbs overshoot is measured (→ 1.179).
- `cobweb`: Banach's a-priori bound |xₙ−x*| ≤ Lⁿ/(1−L)|x₁−x₀| is asserted for every plotted step; if f is not shown to be a self-map with L<1 the caption says the theorem does not apply.
