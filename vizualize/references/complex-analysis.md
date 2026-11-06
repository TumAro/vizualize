# Complex analysis

Contents: plane & maps · domain colouring · Cauchy / residues · conformal grids

## Complex plane (SVG)
Map z=x+iy -> (cx+k x, cy-k y). Draw axes, unit circle, mark points with Re/Im labels. For arithmetic: multiplication by w = rotate by arg w + scale |w|; show both in one picture (arc for angle, ratio of radii).

## Domain colouring (canvas, ~15 lines, instant)
Hue = arg f(z), brightness from log|f(z)| fractional part. Zeros: all colours meet counter-clockwise; poles: clockwise, order = number of cycles.
```html
<canvas id="c" width="400" height="400" style="width:100%"></canvas>
<script>
const f=(x,y)=>{/* z^2-1 over z^2+1: returns [re,im] */
 const nr=x*x-y*y-1, ni=2*x*y, dr=x*x-y*y+1, di=2*x*y, d=dr*dr+di*di;
 return [(nr*dr+ni*di)/d,(ni*dr-nr*di)/d];};
const c=document.getElementById('c'),g=c.getContext('2d'),W=400,I=g.createImageData(W,W),R=2;
const hsv=(h,s,v)=>{const k=n=>(n+h*6)%6;return [255*v*(1-s*Math.max(0,Math.min(k(5),4-k(5),1))),255*v*(1-s*Math.max(0,Math.min(k(3),4-k(3),1))),255*v*(1-s*Math.max(0,Math.min(k(1),4-k(1),1)))]};
for(let j=0;j<W;j++)for(let i=0;i<W;i++){
 const [u,v]=f((i/W*2-1)*R,(1-j/W*2)*R), a=(Math.atan2(v,u)/(2*Math.PI)+1)%1,
 m=Math.log2(Math.hypot(u,v)), b=0.55+0.45*(m-Math.floor(m)), p=(j*W+i)*4,
 [r,gg,bl]=hsv(a,0.85,b); I.data.set([r,gg,bl,255],p);}
g.putImageData(I,0,0);
</script>
```
Replace f with the function; keep the comment saying what f is. Invariants: zeros/poles of f appear at the right points (here ±1 zeros, ±i poles); winding count of colours = order.

## Cauchy integral theorem / residues
Picture: contour C (closed curve), poles as ×, shaded interior. Statement of what the picture proves: ∮_C f dz = 2πi Σ Res(f, a_k) over poles **inside** C, counted with winding number. For Cauchy's theorem: f analytic inside => no ×, integral 0. Deform-contour picture: two contours homotopic in the domain avoiding poles give equal integrals; contour crossing a pole changes the value by 2πi·Res.
Invariants: poles inside/outside classified by actual geometry; orientation counter-clockwise arrow; keyhole/indent paths drawn avoiding the branch cut.
For dragging: JSXGraph (`jsxgraph@1.12.2`) with a draggable pole point and a circle contour; display "inside? yes/no" computed with `|p-centre|<r`.

## Conformal maps
Draw the image of a rectangular grid under f: sample lines x=const, y=const, compute f at ~60 points per line, emit `<polyline>`. Conformality check: grid images still meet at 90° except where f'=0 (critical points: z² at 0 doubles angles). Examples: z² (parabolas), 1/z (circles <-> circles), e^z (strip -> annulus sector), Möbius.

## Generators (preferred over hand-writing)
- `domain "f(z)" [R=2]`: canvas colouring. Zeros ○ / poles × are found numerically and **certified**: (#zeros − #poles inside |z|<0.97R) must equal the winding number of f (argument principle). With a branch cut or essential singularity (sqrt, log, exp(1/z)) the check fails, the markers are dropped and the caption says so. Never claim marks for an uncertified picture.
- `residue "f(z)" cx cy r`: refuses if a pole sits on the contour or if numeric ∮ ≠ 2πi·ΣRes (1e-6). Residues come from small-circle integrals, not formulas.
- `mobius a b c d`: det ≠ 0 enforced; fixed points solve cz²+(d−a)z−b=0 and are verified f(z)=z.
- `riemann z...`: X²+Y²+Z²=1 and the inverse z=(X+iY)/(1−Z) are asserted.
- Expressions: `z i pi e + - * / ^ **` and exp log sqrt sin cos tan sinh cosh tanh, written `2i` or `2*i`. The in-browser evaluator is cross-checked against Python cmath (rel. error 6e-16 on principal branches).
