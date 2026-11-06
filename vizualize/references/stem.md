# STEM beyond pure maths

Contents: phase portraits · electrostatics · kinematics · probability · circuits · optics

Rule: every number on the picture is recomputed by an independent method; a command fails (non-zero exit) instead of drawing an unverified claim.

- **`phase`**: RK4 trajectories (forward+backward from seeds), nullclines by marching squares, equilibria by Newton from a 7×7 grid. Each equilibrium is classified from the Jacobian (det<0 saddle; tr²−4det<0 spiral or linear centre; else node) and **stable/unstable claims are confirmed by simulating a nearby start**. RK4 step-halving must agree; presets with a conserved quantity (pendulum H, Lotka–Volterra V) must conserve it (drift < 2e-3). A "linear centre" is only a linear statement: say so unless a conserved quantity is checked (as for pendulum and Lotka–Volterra).
- **`charges "q,x,y;..."`**: 3D Coulomb field drawn in the plane through the charges; line count ∝ |q|; E = −∇φ checked by finite differences; far field must match the monopole of the total charge (within 2%).
- **`projectile v0 angle [k]`**: linear drag k gives a closed form (exponential decay); RK4 landing point must match it. Without drag also R = v²sin2θ/g, H = (v sinθ)²/2g, T = 2v sinθ/g and optimal angle 45°. With drag the optimal angle is below 45°.
- **`dist`/`clt`**: normalisation, mean and variance recomputed from the pmf/density (Simpson) and compared with formulas; P(a≤X≤b) compared with the closed-form CDF. `clt n` convolves n dice exactly and reports the sup-norm gap to the normal approximation.
- **`rlc R L C [V]`, `rc R C [V]`**: α = R/2L, ω₀ = 1/√(LC) decide underdamped/critical/overdamped; RK4 equals the closed form at 7 times; poles are drawn in the s-plane.
- **`lens f do h`**: the image is found only by intersecting two principal rays, then checked against 1/f = 1/dₒ + 1/dᵢ and m = −dᵢ/dₒ (virtual images and diverging lenses included; an object at the focal point is refused).
