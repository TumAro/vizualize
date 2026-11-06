(()=>{const CSS="#mv{--fg:var(--color-text-primary,#111);--mt:var(--color-text-secondary,#777);--ax:var(--color-border-secondary,#999);--a:#3b82f6;--b:#f43f5e;--g:#22c55e;--o:#f59e0b;font-size:14px;color:var(--fg)}#mv svg{width:100%;max-width:460px;display:block;margin:auto}#mv .k{display:grid;grid-template-columns:60px 1fr 44px;gap:4px 8px;align-items:center;margin:8px 0;font-size:12px;color:var(--mt)}#mv .k select{grid-column:2/4}#mv .i div{margin:2px 0}#mv .o{font-size:12px;color:var(--g)}#mv .o.x{color:var(--b)}#mv .ax{stroke:var(--ax);fill:none}#mv .c1,#mv .c2,#mv .c3,#mv .c4{fill:none;stroke-width:2.2}#mv .c1{stroke:var(--a)}#mv .c2{stroke:var(--b)}#mv .c3{stroke:var(--g)}#mv .c4{stroke:var(--o)}#mv .d{stroke-dasharray:5 4}#mv .f1{fill:#3b82f633;stroke:var(--a)}#mv .f2{fill:#f43f5e33;stroke:var(--b)}#mv .f3{fill:#22c55e33;stroke:var(--g)}#mv .pt{fill:var(--b)}#mv .t{fill:var(--fg);font-size:11px}#mv .tm{fill:var(--mt);font-size:11px}";const fmt=(x,d=3)=>(+x).toFixed(d).replace(/\.?0+$/,'')||'0',
mk=(b,eq)=>{const W=420,H=320,m=26;let sx=(W-2*m)/(b[1]-b[0]),sy=(H-2*m)/(b[3]-b[2]),ox=m,oy=m;if(eq){const s=Math.min(sx,sy);ox=m+((W-2*m)-s*(b[1]-b[0]))/2;oy=m+((H-2*m)-s*(b[3]-b[2]))/2;sx=sy=s}return{X:x=>ox+(x-b[0])*sx,Y:y=>H-oy-(y-b[2])*sy,b}},
pts=(v,a)=>a.map(p=>v.X(p[0]).toFixed(1)+','+v.Y(p[1]).toFixed(1)).join(' '),
pl=(v,a,c,x='')=>`<polyline class="${c} ${x}" points="${pts(v,a)}"/>`,pg=(v,a,c)=>`<polygon class="${c}" points="${pts(v,a)}"/>`,
tx=(v,x,y,s,c='t',a='middle')=>`<text class="${c}" x="${v.X(x).toFixed(1)}" y="${v.Y(y).toFixed(1)}" text-anchor="${a}">${s}</text>`,
dot=(v,x,y,r=4)=>`<circle class="pt" cx="${v.X(x).toFixed(1)}" cy="${v.Y(y).toFixed(1)}" r="${r}"/>`,
ln=(v,x1,y1,x2,y2,c='ax')=>`<line class="${c}" x1="${v.X(x1).toFixed(1)}" y1="${v.Y(y1).toFixed(1)}" x2="${v.X(x2).toFixed(1)}" y2="${v.Y(y2).toFixed(1)}"/>`,
axes=v=>(v.b[0]<=0&&0<=v.b[1]?ln(v,0,v.b[2],0,v.b[3]):'')+(v.b[2]<=0&&0<=v.b[3]?ln(v,v.b[0],0,v.b[1],0):''),
curve=(f,x0,x1,n=300,lim=1e9)=>{const o=[];let c=[];for(let i=0;i<=n;i++){const x=x0+(x1-x0)*i/n,y=f(x);if(Number.isFinite(y)&&Math.abs(y)<lim)c.push([x,y]);else if(c.length){o.push(c);c=[]}}if(c.length)o.push(c);return o},
area=p=>{let s=0;for(let i=0;i<p.length;i++){const q=p[(i+1)%p.length];s+=p[i][0]*q[1]-q[0]*p[i][1]}return Math.abs(s)/2},
clip=(v,id)=>`<clipPath id="${id}"><rect x="26" y="26" width="368" height="268"/></clipPath>`;
const DM={"pythagoras":{title:"Pythagorean theorem",inv:"area(c\u00b2) = area(a\u00b2) + area(b\u00b2)",params:[{k:"a",label:"leg a",min:1,max:10,step:0.5,v:3},{k:"b",label:"leg b",min:1,max:10,step:0.5,v:4}],draw:function(P){
const a=P.a,b=P.b,Sa=[[0,0],[a,0],[a,-a],[0,-a]],Sb=[[0,0],[0,b],[-b,b],[-b,0]],Sc=[[a,0],[0,b],[b,a+b],[a+b,a]];
const T=[[0,0],[a,0],[0,b]],all=[].concat(Sa,Sb,Sc),bb=[Math.min(...all.map(p=>p[0]))-.5,Math.max(...all.map(p=>p[0]))+.5,Math.min(...all.map(p=>p[1]))-.5,Math.max(...all.map(p=>p[1]))+.5];
const v=mk(bb,true),AA=area(Sa),AB=area(Sb),AC=area(Sc),c=Math.hypot(a,b);
const sq=[[...Sa[0]],[...Sa[1]]];const ok=Math.abs(AC-AA-AB)<1e-9&&Math.abs(Math.hypot(Sc[0][0]-Sc[1][0],Sc[0][1]-Sc[1][1])-c)<1e-9;
return{ok,info:[`a² = ${fmt(AA)}  ·  b² = ${fmt(AB)}  ·  c² = ${fmt(AC)}`,`c = √(${fmt(AA)}+${fmt(AB)}) = ${fmt(c)}`],svg:pg(v,Sa,'f1')+pg(v,Sb,'f3')+pg(v,Sc,'f2')+pg(v,T,'f1').replace('f1','ax')+tx(v,a/2,-a/2,'a²')+tx(v,-b/2,b/2,'b²')+tx(v,(a+b)/2+b/2*0.0+ (b)/2*0,(a+b)/2+a/2*0,'c²')+tx(v,a/2,.15*(bb[3]-bb[2])*0-.35,'a','tm')+tx(v,.35,b/2,'b','tm','start')}}},"quadratic":{title:"Quadratic y = ax\u00b2 + bx + c",inv:"f(root)=0 and f(vertex) is the minimum/maximum",params:[{k:"a",label:"a",min:-3,max:3,step:0.1,v:1},{k:"b",label:"b",min:-6,max:6,step:0.1,v:-2},{k:"c",label:"c",min:-8,max:8,step:0.1,v:-3}],draw:function(P){
const a=P.a,b=P.b,c=P.c,f=x=>a*x*x+b*x+c,D=b*b-4*a*c,v=mk([-8,8,-12,12]);let s=axes(v),ok=true,info=[];
s+=clip(v,'k')+'<g clip-path="url(#k)">'+curve(f,-8,8,400,1e4).map(a=>pl(v,a,'c1')).join('')+'</g>';
if(Math.abs(a)<1e-9){info.push('a = 0: the curve is a line.');if(Math.abs(b)>1e-9){const r=-c/b;s+=dot(v,r,0);ok=Math.abs(b*r+c)<1e-9;info.push('root x = '+fmt(r))}}
else{const xv=-b/(2*a),yv=f(xv);s+=ln(v,xv,-12,xv,12,'c3 d')+dot(v,xv,yv)+tx(v,xv,yv+(a>0?-1:1)*1.4,'vertex ('+fmt(xv,2)+', '+fmt(yv,2)+')','t');
ok=[-.3,-.1,.1,.3].every(h=>a>0?f(xv+h)>=yv-1e-12:f(xv+h)<=yv+1e-12);
info.push('D = b² − 4ac = '+fmt(D));
if(D>=-1e-12){const r=[(-b-Math.sqrt(Math.max(D,0)))/(2*a),(-b+Math.sqrt(Math.max(D,0)))/(2*a)];r.forEach(x=>{s+=dot(v,x,0);ok=ok&&Math.abs(f(x))<1e-7*(1+Math.abs(b)+Math.abs(c))});info.push('roots: x = '+r.map(x=>fmt(x,3)).join(', ')+(D<1e-12?' (double)':''))}
else info.push('D < 0: no real roots (complex pair '+fmt(-b/(2*a),2)+' ± '+fmt(Math.sqrt(-D)/(2*Math.abs(a)),2)+'i)')}
return{ok,info,svg:s}}},"sine":{title:"Sinusoid y = A\u00b7sin(B(x \u2212 C)) + D",inv:"over one full period: max = D+|A|, min = D\u2212|A|; f(x+period)=f(x)",params:[{k:"A",label:"A",min:0.2,max:4,step:0.1,v:2},{k:"B",label:"B",min:0.25,max:4,step:0.25,v:1},{k:"C",label:"C",min:-3,max:3,step:0.1,v:0},{k:"D",label:"D",min:-3,max:3,step:0.1,v:0}],draw:function(P){
const A=P.A,B=P.B,C=P.C,D=P.D,f=x=>A*Math.sin(B*(x-C))+D,T=2*Math.PI/B,v=mk([-7,7,-8,8]);
const xs=Array.from({length:4001},(_,i)=>C+T*i/4000),ys=xs.map(f),mx=Math.max(...ys),mn=Math.min(...ys);
const ok=Math.abs(mx-(D+A))<1e-3&&Math.abs(mn-(D-A))<1e-3&&[0,1,2.5,-3].every(x=>Math.abs(f(x+T)-f(x))<1e-9);
let s=axes(v)+ln(v,-7,D,7,D,'c3 d')+curve(f,-7,7,500).map(a=>pl(v,a,'c1')).join('')+dot(v,C,D)+ln(v,C,D,C+T,D,'c2');
return{ok,info:['amplitude = '+fmt(A)+' · period = 2π/'+fmt(B)+' = '+fmt(T),'phase shift C = '+fmt(C)+' · midline y = '+fmt(D),'range = ['+fmt(D-A,2)+', '+fmt(D+A,2)+']'],svg:s}}},"taylor":{title:"Taylor polynomial about 0",inv:"|f(x) \u2212 T\u2099(x)| \u2264 Lagrange bound at 5 sample points",params:[{k:"fn",label:"f",opts:["sin","cos","exp"],v:"sin"},{k:"n",label:"degree n",min:0,max:15,step:1,v:3}],draw:function(P){
const n=P.n,F={sin:Math.sin,cos:Math.cos,exp:Math.exp}[P.fn];
const co=k=>P.fn=='exp'?1:P.fn=='sin'?[0,1,0,-1][k%4]:[1,0,-1,0][k%4];
const fac=k=>{let r=1;for(let i=2;i<=k;i++)r*=i;return r};
const Tn=x=>{let s=0;for(let k=0;k<=n;k++)s+=co(k)*Math.pow(x,k)/fac(k);return s};
const v=mk([-6,6,-4,4]);let ok=true;
[-5,-2,.3,1.7,4].forEach(x=>{const M=P.fn=='exp'?Math.exp(Math.abs(x)):1,B=M*Math.pow(Math.abs(x),n+1)/fac(n+1);ok=ok&&Math.abs(F(x)-Tn(x))<=B+1e-9});
const s=clip(v,'k')+axes(v)+'<g clip-path="url(#k)">'+curve(F,-6,6,400).map(a=>pl(v,a,'c1')).join('')+curve(Tn,-6,6,400,60).map(a=>pl(v,a,'c2')).join('')+'</g>'+tx(v,-5.8,3.6,'— '+P.fn+'(x)','t','start').replace('class="t"','class="t" style="fill:var(--c1)"')+tx(v,-5.8,3.1,'— T'+n+'(x)','t','start').replace('class="t"','class="t" style="fill:var(--c2)"');
return{ok,info:['T'+n+'(x) = '+Array.from({length:n+1},(_,k)=>co(k)?(co(k)<0?'−':'+')+(k==0?'1':k==1?'x':'x^'+k+'/'+k+'!'):'').join(' ').replace(/^\+/,'').trim(),'error at x = 1: '+(Math.abs(F(1)-Tn(1))).toExponential(2)],svg:s}}},"epsdelta":{title:"\u03b5\u2013\u03b4 limit of f(x) = x\u00b2 at a",inv:"sampled verdict = exact verdict (2|a|\u03b4+\u03b4\u00b2 \u2264 \u03b5)",params:[{k:"a",label:"point a",min:-2,max:2,step:0.1,v:1},{k:"e",label:"ε",min:0.05,max:2,step:0.05,v:0.5},{k:"d",label:"δ",min:0.01,max:1,step:0.01,v:0.2}],draw:function(P){
const a=P.a,e=P.e,d=P.d,f=x=>x*x,L=f(a),v=mk([a-2.2,a+2.2,L-2.2,L+2.2],true);
let worst=0;for(let i=0;i<=2000;i++){const x=a-d+2*d*i/2000;worst=Math.max(worst,Math.abs(f(x)-L))}
const works=worst<=e+1e-9,exact=(2*Math.abs(a)*d+d*d)<=e+1e-9,ok=works===exact;
const bx=[[a-d,L-e],[a+d,L-e],[a+d,L+e],[a-d,L+e]];
const s=clip(v,'k')+axes(v)+pg(v,[[a-2.2,L-e],[a+2.2,L-e],[a+2.2,L+e],[a-2.2,L+e]],'f3')+pg(v,[[a-d,L-9],[a+d,L-9],[a+d,L+9],[a-d,L+9]],'f1')+'<g clip-path="url(#k)">'+curve(f,a-2.2,a+2.2,400).map(c=>pl(v,c,works?'c1':'c2')).join('')+'</g>'+dot(v,a,L)+tx(v,a,L-e-.18,'L−ε','tm')+tx(v,a,L+e+.1,'L+ε','tm');
return{ok,info:['L = a² = '+fmt(L)+' · max |f−L| on window = '+fmt(worst),works?'✓ δ works for this ε (graph inside the band)':'✗ δ too big: graph leaves the band — shrink δ','largest valid δ here: '+fmt(Math.sqrt(a*a+e)-Math.abs(a),3)],svg:s}}},"eigen":{title:"2\u00d72 matrix: eigenvectors and singular values",inv:"|det| = \u03c3\u2081\u03c3\u2082, trace = \u03bb\u2081+\u03bb\u2082, max|Au| over the circle = \u03c3\u2081",params:[{k:"a",label:"a",min:-3,max:3,step:0.1,v:2},{k:"b",label:"b",min:-3,max:3,step:0.1,v:1},{k:"c",label:"c",min:-3,max:3,step:0.1,v:0},{k:"d",label:"d",min:-3,max:3,step:0.1,v:1.5}],draw:function(P){
const a=P.a,b=P.b,c=P.c,d=P.d,tr=a+d,det=a*d-b*c,disc=tr*tr/4-det;
const p=a*a+c*c,q=a*b+c*d,r=b*b+d*d;
const m=(p+r)/2,h=Math.sqrt(((p-r)/2)**2+q*q),s1=Math.sqrt(Math.max(m+h,0)),s2=Math.sqrt(Math.max(m-h,0));
let best=0;const circ=[],img=[];for(let i=0;i<=360;i++){const t=i*Math.PI/180,u=[Math.cos(t),Math.sin(t)],w=[a*u[0]+b*u[1],c*u[0]+d*u[1]];circ.push(u);img.push(w);best=Math.max(best,Math.hypot(w[0],w[1]))}
const lam=disc>=0?[tr/2+Math.sqrt(disc),tr/2-Math.sqrt(disc)]:null;
const ok=Math.abs(Math.abs(det)-s1*s2)<1e-6&&Math.abs(best-s1)<1e-3*(1+s1)&&(!lam||Math.abs(lam[0]+lam[1]-tr)<1e-9&&Math.abs(lam[0]*lam[1]-det)<1e-9);
const R=Math.max(s1,1)*1.25+.2,v=mk([-R,R,-R,R],true);
let s=axes(v)+pl(v,circ,'c1','d')+pl(v,img,'c2');
const th=.5*Math.atan2(2*q,p-r),v1=[Math.cos(th),Math.sin(th)],Av=[a*v1[0]+b*v1[1],c*v1[0]+d*v1[1]];
s+=ln(v,0,0,Av[0],Av[1],'c4')+tx(v,Av[0]*1.08,Av[1]*1.08,'σ₁','t');
const info=['σ₁ = '+fmt(s1,3)+' · σ₂ = '+fmt(s2,3)+' · |det| = '+fmt(Math.abs(det),3)];
if(lam){info.push('eigenvalues λ = '+fmt(lam[0],3)+', '+fmt(lam[1],3));lam.forEach((l,i)=>{let ev=Math.abs(b)>1e-9?[b,l-a]:Math.abs(c)>1e-9?[l-d,c]:(i==0?[1,0]:[0,1]);const nn=Math.hypot(ev[0],ev[1]);ev=[ev[0]/nn,ev[1]/nn];s+=ln(v,-R*ev[0],-R*ev[1],R*ev[0],R*ev[1],i?'c3 d':'c3')})}
else info.push('complex eigenvalues '+fmt(tr/2,2)+' ± '+fmt(Math.sqrt(-disc),2)+'i (a rotation component: no real eigenline)');
return{ok,info,svg:s}}},"riemann":{title:"Riemann sums on [0, 2]",inv:"|sum \u2212 exact| \u2264 rigorous error bound",params:[{k:"fn",label:"f",opts:["x²","eˣ","1/(1+x²)"],v:"x²"},{k:"rule",label:"rule",opts:["left","right","midpoint","trapezoid"],v:"left"},{k:"n",label:"n",min:1,max:60,step:1,v:6}],draw:function(P){
const n=P.n,A=0,B=2,w=(B-A)/n,F={'x²':x=>x*x,'eˣ':Math.exp,'1/(1+x²)':x=>1/(1+x*x)}[P.fn],
ex={'x²':8/3,'eˣ':Math.exp(2)-1,'1/(1+x²)':Math.atan(2)}[P.fn],M2={'x²':2,'eˣ':Math.exp(2),'1/(1+x²)':2}[P.fn];
const v=mk([-.2,2.2,-.3,Math.max(F(0),F(2),1)*1.1+.2]);let sum=0,s=axes(v)+curve(F,0,2,300).map(c=>pl(v,c,'c1')).join('');
for(let i=0;i<n;i++){const x0=A+i*w,x1=x0+w;let h,poly;
if(P.rule=='left')h=F(x0);else if(P.rule=='right')h=F(x1);else if(P.rule=='midpoint')h=F((x0+x1)/2);
if(P.rule=='trapezoid'){poly=[[x0,0],[x1,0],[x1,F(x1)],[x0,F(x0)]];sum+=w*(F(x0)+F(x1))/2}else{poly=[[x0,0],[x1,0],[x1,h],[x0,h]];sum+=w*h}
s+=pg(v,poly,'f2')}
const bound=P.rule=='left'||P.rule=='right'?Math.abs(F(B)-F(A))*w:P.rule=='midpoint'?(B-A)**3*M2/(24*n*n):(B-A)**3*M2/(12*n*n);
const ok=Math.abs(sum-ex)<=bound+1e-12;
return{ok,info:['sum = '+fmt(sum,5)+' · exact ∫ = '+fmt(ex,5),'error = '+fmt(Math.abs(sum-ex),5)+' ≤ bound '+fmt(bound,5)],svg:s}}}};
function run(el){const D=DM[el.dataset.mv],pin=Object.fromEntries((el.dataset.pin||'').split(',').filter(Boolean).map(s=>s.split('='))),P={};
el.innerHTML='<style>'+CSS+'</style><svg viewBox="0 0 420 320" role="img" aria-label="'+D.title+'"></svg><div class=k></div><div class=i></div><div class=o></div><button>Explain this state ↗</button>';
const q=s=>el.querySelector(s),K=q('.k'),sv=q('svg'),I=q('.i'),O=q('.o'),B=q('button');
function render(){const r=D.draw(P);sv.innerHTML=r.svg;I.innerHTML=r.info.map(x=>'<div>'+x+'</div>').join('');O.className='o'+(r.ok?'':' x');O.textContent=(r.ok?'✓ checked on the drawn data: ':'✗ FAILED: ')+D.inv;return r.ok}
D.params.forEach(p=>{if(p.k in pin){P[p.k]=p.opts?pin[p.k]:+pin[p.k];return}P[p.k]=p.v;const l=document.createElement('label');l.textContent=p.label;K.append(l);
if(p.opts){const s=document.createElement('select');p.opts.forEach(o=>{const e=document.createElement('option');e.textContent=e.value=o;s.append(e)});s.value=p.v;s.oninput=()=>{P[p.k]=s.value;render()};K.append(s)}
else{const i=document.createElement('input');i.type='range';i.min=p.min;i.max=p.max;i.step=p.step;i.value=p.v;const o=document.createElement('output');o.value=fmt(p.v,2);i.oninput=()=>{P[p.k]=+i.value;o.value=fmt(i.value,2);render()};K.append(i,o)}});
el.__sweep=n=>{const bad=[],S={...P};for(let t=0;t<n;t++){D.params.forEach(p=>{if(!(p.k in pin))P[p.k]=p.opts?p.opts[Math.floor(Math.random()*p.opts.length)]:+p.min+Math.round(Math.random()*(p.max-p.min)/p.step)*p.step});if(!D.draw(P).ok)bad.push(JSON.stringify(P))}Object.assign(P,S);return bad};
B.onclick=()=>typeof sendPrompt=='function'?sendPrompt('In the "'+D.title+'" visual with '+JSON.stringify(P)+', explain why the invariant ('+D.inv+') holds and what changes as I move the sliders.'):0;
if(typeof sendPrompt!='function')B.style.display='none';render()}
document.querySelectorAll('[data-mv]').forEach(run)})()
