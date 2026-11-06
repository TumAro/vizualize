"""Complex-analysis generators (stdlib only). Every picture's marks are computed numerically AND certified by the argument principle.
  mv.py domain  "f(z)" [R=2]            domain colouring (canvas) + certified zeros/poles with orders
  mv.py residue "f(z)" cx cy r          contour circle, poles, residues; numeric ∮ must equal 2πi·ΣRes or it refuses
  mv.py mobius  a b c d                 (az+b)/(cz+d): polar grid & image, fixed points checked
  mv.py riemann z1 z2 ...  (inf ok)     points on the Riemann sphere (stereographic), round-trip checked
  mv.py julia   [re im]                 Mandelbrot + Julia set (canvas, click to pick c)
Expressions: z, i, pi, e, + - * / ^ **, exp log sqrt sin cos tan sinh cosh tanh. Principal branches."""
import cmath, math, re, json
BIG = 1e300
def pyf(expr):
    e = re.sub(r"(\d)i\b", r"\1j", re.sub(r"\bi\b", "1j", expr.replace("^", "**")))
    env = {k: getattr(cmath, k) for k in ("exp", "log", "sqrt", "sin", "cos", "tan", "sinh", "cosh", "tanh")}; env.update(pi=math.pi, e=math.e)
    code = compile(e, "f", "eval")
    def f(z):
        try: return complex(eval(code, {"__builtins__": {}}, {**env, "z": z}))
        except (ZeroDivisionError, OverflowError, ValueError): return complex(BIG)
    return f
def roots(g, c, R, N=70):
    """isolated roots of g in the box c±R (grid minima -> Newton), deduplicated."""
    h = 2*R/N; pts = [[c + complex(-R + h*i, -R + h*j) for i in range(N+1)] for j in range(N+1)]
    A = [[abs(g(p)) for p in row] for row in pts]; out = []
    for j in range(N+1):
        for i in range(N+1):
            a = A[j][i]
            if not all(A[jj][ii] >= a for jj in range(max(j-1, 0), min(j+2, N+1)) for ii in range(max(i-1, 0), min(i+2, N+1))): continue
            z = pts[j][i]
            for _ in range(60):
                dz = 1e-7*(1+abs(z)); gz = g(z); d = (g(z+dz)-g(z-dz))/(2*dz)
                if d == 0 or abs(gz) > 1e100: break
                step = gz/d; z -= step
                if abs(step) < 1e-14: break
            if abs(g(z)) < 1e-8 and abs(z-c).real <= R*1.001 and abs(z.real-c.real) <= R and abs(z.imag-c.imag) <= R and all(abs(z-w) > 1e-5 for w in out): out.append(z)
    return out
def winding(f, c, r, N=6000):
    tot = 0.0; prev = f(c + r); winding.jump = 0.0
    for k in range(1, N+1):
        cur = f(c + r*cmath.exp(2j*math.pi*k/N)); tot += cmath.phase(cur/prev)
        winding.jump = max(winding.jump, abs(cur-prev)/(max(abs(cur), abs(prev)) + 1e-12)); prev = cur
    return tot/(2*math.pi)
def zp(f, c, R):
    """-> (zeros, poles, certified) with integer orders; certified = (#zeros-#poles inside circle) == winding of f."""
    inv = lambda z: (1/f(z) if f(z) != 0 and abs(f(z)) < 1e100 else (0j if abs(f(z)) >= 1e100 else complex(BIG)))
    Z, P = roots(f, c, R), roots(inv, c, R)
    cuts = []
    def order(p, sign):
        rr = 0.02
        for q in Z + P:
            if q != p: rr = min(rr, abs(q-p)/3)
        if rr <= 1e-6: return 0
        o = round(winding(f, p, rr, 800)); cuts.append(winding.jump); return o
    zs = [(z, order(z, 1)) for z in Z]; ps = [(p, -order(p, -1)) for p in P]
    zs = [(z, o) for z, o in zs if o > 0]; ps = [(p, o) for p, o in ps if o > 0]
    rho = R*0.97; ins = lambda p: abs(p-c) < rho
    net = sum(o for z, o in zs if ins(z)) - sum(o for p, o in ps if ins(p))
    w = winding(f, c, rho); cuts.append(winding.jump)
    return zs, ps, abs(w-net) < 1e-6 and abs(w-round(w)) < 1e-3 and max(cuts or [0]) < 0.5, net, w
JSLIB = r"""const cx=(a,b)=>[a,b],ad=(a,b)=>[a[0]+b[0],a[1]+b[1]],sb=(a,b)=>[a[0]-b[0],a[1]-b[1]],ml=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]],dv=(a,b)=>{const d=b[0]*b[0]+b[1]*b[1];return[(a[0]*b[0]+a[1]*b[1])/d,(a[1]*b[0]-a[0]*b[1])/d]},
ex=a=>{const r=Math.exp(a[0]);return[r*Math.cos(a[1]),r*Math.sin(a[1])]},lg=a=>[Math.log(Math.hypot(a[0],a[1])),Math.atan2(a[1],a[0])],
sq=a=>{const r=Math.hypot(a[0],a[1]),t=Math.atan2(a[1],a[0])/2,s=Math.sqrt(r);return[s*Math.cos(t),s*Math.sin(t)]},
pw=(a,b)=>{if(b[1]==0&&Number.isInteger(b[0])&&Math.abs(b[0])<=64){let r=[1,0],n=Math.abs(b[0]);for(let i=0;i<n;i++)r=ml(r,a);return b[0]<0?dv([1,0],r):r}return ex(ml(b,lg(a)))},
sn=a=>[Math.sin(a[0])*Math.cosh(a[1]),Math.cos(a[0])*Math.sinh(a[1])],cs=a=>[Math.cos(a[0])*Math.cosh(a[1]),-Math.sin(a[0])*Math.sinh(a[1])],
sh=a=>[Math.sinh(a[0])*Math.cos(a[1]),Math.cosh(a[0])*Math.sin(a[1])],ch=a=>[Math.cosh(a[0])*Math.cos(a[1]),Math.sinh(a[0])*Math.sin(a[1])],
FN={exp:ex,log:lg,sqrt:sq,sin:sn,cos:cs,tan:a=>dv(sn(a),cs(a)),sinh:sh,cosh:ch,tanh:a=>dv(sh(a),ch(a))};
function parse(s){const t=s.match(/\d*\.?\d+(?:e[+-]?\d+)?i?|[a-z]+|\*\*|[-+*\/^()]/g);let p=0;
const E=()=>{let a=T();while(t[p]=='+'||t[p]=='-'){const o=t[p++],b=T(),x=a;a=o=='+'?z=>ad(x(z),b(z)):z=>sb(x(z),b(z))}return a},
T=()=>{let a=U();while(t[p]=='*'||t[p]=='/'){const o=t[p++],b=U(),x=a;a=o=='*'?z=>ml(x(z),b(z)):z=>dv(x(z),b(z))}return a},
U=()=>{if(t[p]=='-'){p++;const a=U();return z=>sb([0,0],a(z))}const a=A();if(t[p]=='^'||t[p]=='**'){p++;const b=U();return z=>pw(a(z),b(z))}return a},
A=()=>{const k=t[p++];if(k=='('){const a=E();p++;return a}if(k=='z')return z=>z;if(k=='i')return()=>[0,1];if(k=='pi')return()=>[Math.PI,0];if(k=='e')return()=>[Math.E,0];
if(FN[k]){p++;const a=E();p++;return z=>FN[k](a(z))}const v=parseFloat(k);return k.endsWith('i')?()=>[0,v]:()=>[v,0]};return E()}"""
def _wrap(body, js):
    return '<div id="mv">%s</div><script>(()=>{%s})()</script>' % (body, js)
def domain(expr, R=2.0):
    f = pyf(expr); zs, ps, ok, net, w = zp(f, 0j, R)
    marks = [[z.real, z.imag, 0, o] for z, o in zs] + [[p.real, p.imag, 1, o] for p, o in ps] if ok else []
    cap = ("zeros ○ %s; poles × %s; zeros − poles inside |z|<%.2f = %d = winding of f (argument principle ✓)" % (
        ", ".join("%s(ord %d)" % (_fmt(z), o) for z, o in zs) or "none", ", ".join("%s(ord %d)" % (_fmt(p), o) for p, o in ps) or "none", R*.97, net)) if ok else "markers not certified (branch cut / essential singularity / non-isolated): picture shows colours only"
    js = JSLIB + r"""
const F=parse(%s),R=%s,M=%s,c=document.querySelector('#mv canvas'),g=c.getContext('2d'),W=c.width,I=g.createImageData(W,W);
const hs=(h,s,v)=>{const k=n=>(n+h*6)%%6;return[255*v*(1-s*Math.max(0,Math.min(k(5),4-k(5),1))),255*v*(1-s*Math.max(0,Math.min(k(3),4-k(3),1))),255*v*(1-s*Math.max(0,Math.min(k(1),4-k(1),1)))]};
for(let j=0;j<W;j++)for(let i=0;i<W;i++){const w=F([(i/W*2-1)*R,(1-j/W*2)*R]),a=(Math.atan2(w[1],w[0])/(2*Math.PI)+1)%%1,m=Math.log2(Math.hypot(w[0],w[1])),b=0.5+0.5*(m-Math.floor(m)),q=hs(a,0.85,Number.isFinite(b)?b:1);I.data.set([q[0],q[1],q[2],255],(j*W+i)*4)}
g.putImageData(I,0,0);g.strokeStyle='rgba(0,0,0,.35)';g.beginPath();g.moveTo(W/2,0);g.lineTo(W/2,W);g.moveTo(0,W/2);g.lineTo(W,W/2);g.stroke();
M.forEach(m=>{const x=(m[0]/R+1)*W/2,y=(1-m[1]/R)*W/2;g.lineWidth=3;g.strokeStyle='#fff';g.fillStyle='#000';g.beginPath();if(m[2]){g.moveTo(x-6,y-6);g.lineTo(x+6,y+6);g.moveTo(x+6,y-6);g.lineTo(x-6,y+6);g.stroke();g.lineWidth=1.5;g.strokeStyle='#000';g.stroke()}else{g.arc(x,y,6,0,7);g.fill();g.stroke()}});""" % (json.dumps(expr), R, json.dumps(marks))
    body = '<canvas width="400" height="400" style="width:100%%;max-width:440px;display:block;margin:auto"></canvas><div style="font-size:12px;margin-top:6px;color:var(--color-text-secondary,#777)">f(z) = %s · hue = arg f, brightness cycles each doubling of |f| · %s</div>' % (expr, cap)
    return _wrap(body, js)
def _fmt(z):
    r, i = round(z.real, 4) + 0.0, round(z.imag, 4) + 0.0
    return "%g" % r if i == 0 else ("%gi" % i if r == 0 else "%g%+gi" % (r, i))

def _contour(f, c, r, N=8000):
    s = 0j
    for k in range(N):
        t = 2*math.pi*k/N; z = c + r*cmath.exp(1j*t); s += f(z) * 1j*r*cmath.exp(1j*t) * (2*math.pi/N)
    return s
def residue(expr, cx, cy, r):
    f = pyf(expr); c = complex(cx, cy); R = r + 1.5
    zs, ps, ok, net, w = zp(f, c, R)
    assert all(abs(abs(p-c) - r) > 1e-3 for p, _ in ps + zs), "a pole/zero lies on the contour: integral undefined"
    inside = [(p, o) for p, o in ps if abs(p-c) < r]
    assert ok or not ps, "poles not certified (branch cut / essential singularity near the contour); refusing to draw false data"
    res = []
    for p, o in inside:
        rr = min([0.1] + [abs(p-q)/3 for q, _ in ps if q != p]); res.append(_contour(f, p, rr) / (2j*math.pi))
    I = _contour(f, c, r); S = 2j*math.pi*sum(res)
    assert abs(I - S) < 1e-6*(1+abs(I)), f"numeric ∮={I} but 2πi·ΣRes={S}: refusing"
    zr = R*1.15; sc = 190/zr; X = lambda x: 210+sc*(x-c.real); Y = lambda y: 160-sc*(y-c.imag)
    o = [f'<circle cx="{X(c.real):.1f}" cy="{Y(c.imag):.1f}" r="{sc*r:.1f}" fill="#3b82f622" stroke="#3b82f6" stroke-width="2"/>',
         f'<path d="M{X(c.real)-6:.0f} {Y(c.imag)-sc*r:.0f}l8 -4v8z" fill="#3b82f6"/>']
    o.append(f'<path d="M20 {Y(0):.0f}H400M{X(0):.0f} 20V290" stroke="#888" stroke-width="1"/>')
    for p, k in ps:
        x, y = X(p.real), Y(p.imag); ins = abs(p-c) < r
        o.append(f'<path d="M{x-5:.0f} {y-5:.0f}l10 10m0 -10l-10 10" stroke="{"#f43f5e" if ins else "#888"}" stroke-width="2.5"/><text x="{x+8:.0f}" y="{y-6:.0f}" text-anchor="start" font-size="11">{_fmt(p)}' + (f" (order {k})" if k > 1 else "") + (f" · Res={_fmt(res[[q for q, _ in inside].index(p)])}" if ins else " · outside") + "</text>")
    o.append(f'<text x="210" y="312" font-size="12">∮ = {_fmt(I)} = 2πi·ΣRes = {_fmt(S)}  (numeric ✓)</text>')
    return '<svg viewBox="0 0 420 320" width="100%%" xmlns="http://www.w3.org/2000/svg" fill="currentColor" text-anchor="middle">%s</svg>' % "".join(o)

def _lin(a, b):
    t = "" if abs(a) < 1e-12 else ("z" if abs(a-1) < 1e-12 else "-z" if abs(a+1) < 1e-12 else _fmt(a) + "z")
    if abs(b) < 1e-12: return t or "0"
    u = _fmt(b); u = u if t == "" or u[0] == "-" else "+" + u
    return t + u
def mobius(a, b, c, d):
    a, b, c, d = map(complex, (a, b, c, d)); det = a*d - b*c
    assert abs(det) > 1e-12, "ad-bc = 0: map is constant, not a Möbius transformation"
    f = lambda z: (a*z+b)/(c*z+d) if abs(c*z+d) > 1e-12 else complex(BIG)
    fixed = []
    if abs(c) > 1e-12:
        D = cmath.sqrt((d-a)**2 + 4*b*c); fixed = list({(a-d+D)/(2*c), (a-d-D)/(2*c)})
    elif abs(a-d) > 1e-12: fixed = [b/(d-a)]
    for z in fixed: assert abs(f(z)-z) < 1e-8*(1+abs(z)), "fixed point check failed"
    lines = [("c", [r*cmath.exp(2j*math.pi*k/40) for k in range(41)]) for r in (.5, 1, 1.5, 2)] + [("r", [t*cmath.exp(1j*math.pi*k/6) for t in [x/5 for x in range(-12, 13)]]) for k in range(6)]
    def runs(ws, R):
        o, cur = [], []
        for w in ws:
            if abs(w) < BIG/10 and abs(w.real) <= R and abs(w.imag) <= R: cur.append(w)
            elif cur: o.append(cur); cur = []
        if cur: o.append(cur)
        return o
    def panel(ox, data, R, title, marks):
        s = [f'<rect x="{ox}" y="12" width="200" height="200" fill="none" stroke="#888"/><text x="{ox+100}" y="228" font-size="12">{title}</text><path d="M{ox} 112h200M{ox+100} 12v200" stroke="#888" stroke-width=".8"/>']
        for k, ws in data:
            for rn in runs(ws, R):
                s.append('<polyline fill="none" stroke="%s" stroke-width="1.4" points="%s"/>' % ("#3b82f6" if k == "c" else "#f43f5e", " ".join(f"{ox+100+100*w.real/R:.0f},{112-100*w.imag/R:.0f}" for w in rn)))
        for z in marks:
            if abs(z.real) <= R and abs(z.imag) <= R: s.append(f'<circle cx="{ox+100+100*z.real/R:.0f}" cy="{112-100*z.imag/R:.0f}" r="4" fill="#22c55e"/>')
        return s
    img = [(k, [f(z) for z in ws]) for k, ws in lines]
    out = panel(5, lines, 2.4, "z-plane", fixed) + panel(215, img, 4, f"w = ({_lin(a, b)})/({_lin(c, d)})", [f(z) for z in fixed])
    cap = ("fixed points (green): " + ", ".join(_fmt(z) for z in fixed)) if fixed else "no finite fixed point (translation-like: only ∞ fixed)"
    out.append(f'<text x="210" y="248" font-size="11">det = {_fmt(det)} ≠ 0 · {cap}</text>')
    return '<svg viewBox="0 0 420 256" width="100%%" xmlns="http://www.w3.org/2000/svg" fill="currentColor" text-anchor="middle">%s</svg>' % "".join(out)

def riemann(pts):
    zs = [complex(p.replace("i", "j")) if p != "inf" else None for p in pts]
    az, el = math.radians(35), math.radians(22)
    def proj(X, Y, Z):
        x1, y1 = X*math.cos(az) - Y*math.sin(az), X*math.sin(az) + Y*math.cos(az)
        return 130 + 105*x1, 130 - 105*(Z*math.cos(el) + y1*math.sin(el)), (y1*math.cos(el) - Z*math.sin(el)) > 0   # visible if depth towards viewer
    def sph(z):
        if z is None: return 0, 0, 1
        n = abs(z)**2 + 1; return 2*z.real/n, 2*z.imag/n, (abs(z)**2 - 1)/n
    o = ['<circle cx="130" cy="130" r="105" fill="none" stroke="#888"/>']
    for lat in (-60, -30, 0, 30, 60):
        z = math.sin(math.radians(lat)); rr = math.cos(math.radians(lat))
        ptsl = [proj(rr*math.cos(t), rr*math.sin(t), z) for t in [k*math.pi/36 for k in range(73)]]
        for vis in (True, False):
            seg = " ".join(f"{x:.0f},{y:.0f}" for x, y, v in ptsl if v == vis)
            dash = "" if vis else ' stroke-dasharray="3 3" opacity=".5"'
            if seg: o.append(f'<polyline fill="none" stroke="#888" stroke-width="{1.2 if lat == 0 else .6}"{dash} points="{seg}"/>')
    for z, lab in zip(zs, pts):
        X, Y, Z = sph(z); assert abs(X*X + Y*Y + Z*Z - 1) < 1e-12
        if z is not None:                                  # inverse stereographic: z = (X+iY)/(1-Z)
            assert abs(complex(X, Y)/(1-Z) - z) < 1e-9*(1+abs(z))
        x, y, vis = proj(X, Y, Z)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="4.5" fill="#f43f5e" opacity="{1 if vis else .35}"/><text x="{x+7:.0f}" y="{y-5:.0f}" font-size="11" text-anchor="start">{"∞ (north pole)" if z is None else lab}</text>')
    o.append('<text x="130" y="262" font-size="11">equator = unit circle · faded = far side</text>')
    return '<svg viewBox="-40 0 340 270" width="100%%" style="max-width:420px;display:block;margin:auto" xmlns="http://www.w3.org/2000/svg" fill="currentColor" text-anchor="middle">%s</svg>' % "".join(o)

def julia(cr=-0.8, ci=0.156):
    js = r"""const q=s=>document.querySelector('#mv '+s),M=q('#m'),J=q('#j'),mg=M.getContext('2d'),jg=J.getContext('2d'),W=220,IT=60;let c=[%s,%s];
function it(x,y,a,b){let i=0;while(i<IT&&x*x+y*y<=4){const t=x*x-y*y+a;y=2*x*y+b;x=t;i++}return i}
const col=i=>i==IT?[0,0,0]:[255*Math.min(1,i/20),255*Math.min(1,i/40),255*(0.4+0.6*i/IT)];
function paint(g,f){const I=g.createImageData(W,W);for(let j=0;j<W;j++)for(let i=0;i<W;i++){const k=col(f((i/W*2-1)*1.8,(1-j/W*2)*1.8)),p=(j*W+i)*4;I.data.set([k[0],k[1],k[2],255],p)}g.putImageData(I,0,0)}
function draw(){paint(mg,(x,y)=>it(0,0,x-0.5,y));paint(jg,(x,y)=>it(x,y,c[0],c[1]));mg.fillStyle='#fff';mg.strokeStyle='#000';mg.beginPath();mg.arc((c[0]+0.5)/1.8*W/2+W/2,(1-c[1]/1.8)*W/2,5,0,7);mg.fill();mg.stroke();q('#o').textContent='c = '+c[0].toFixed(3)+(c[1]<0?' − ':' + ')+Math.abs(c[1]).toFixed(3)+'i'}
M.onclick=e=>{const r=M.getBoundingClientRect();c=[((e.clientX-r.left)/r.width*2-1)*1.8-0.5,(1-(e.clientY-r.top)/r.height*2)*1.8];draw()};draw()""" % (cr, ci)
    return _wrap('<div style="display:flex;gap:8px;flex-wrap:wrap"><canvas id="m" width="220" height="220" style="flex:1;min-width:180px;max-width:100%"></canvas><canvas id="j" width="220" height="220" style="flex:1;min-width:180px;max-width:100%"></canvas></div><div id="o" style="font-size:12px"></div><div style="font-size:12px;color:var(--color-text-secondary,#777)">Left: Mandelbrot set (click to choose c; shown with c as a dot, window centred at −0.5). Right: filled Julia set of z→z²+c. Escape-time colouring, 60 iterations, bailout |z|>2.</div>', js)
