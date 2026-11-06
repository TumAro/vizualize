// cross-check: JS expression evaluator (in the domain-colouring fragment) vs Python cmath on sample points. usage: node test_cplx.js <jslib.js> <samples.json>
const { chromium } = require(process.env.PW_MODULE || 'playwright'); const fs = require('fs');
(async () => {
  const lib = fs.readFileSync(process.argv[2], 'utf8'), S = JSON.parse(fs.readFileSync(process.argv[3], 'utf8'));
  const b = await chromium.launch(); const p = await b.newPage(); await p.setContent('<body></body>');
  const out = await p.evaluate(([lib, S]) => { const f = new Function(lib + ';return parse;')(); return S.map(s => s.pts.map(z => f(s.e)(z))); }, [lib, S]);
  let worst = 0, bad = 0;
  S.forEach((s, i) => s.pts.forEach((z, j) => { const [a, b2] = out[i][j], [c, d] = s.py[j]; const e = Math.hypot(a - c, b2 - d) / (1 + Math.hypot(c, d)); if (!(e < 1e-9)) { bad++; console.log('MISMATCH', s.e, z, [a, b2], [c, d]); } worst = Math.max(worst, e); }));
  console.log(bad ? 'FAIL' : 'ok  ', 'JS vs Python evaluator, worst rel err', worst.toExponential(1)); await b.close(); process.exit(bad ? 1 : 0);
})();
