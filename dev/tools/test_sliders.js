// node test_sliders.js <dir-with-html> <out-dir> : sweeps invariants (500 random slider states each), screenshots default state
const { chromium } = require(process.env.PW_MODULE || 'playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const b = await chromium.launch(); let fail = 0;
  for (const f of fs.readdirSync(process.argv[2]).filter(f => f.endsWith('.html'))) {
    const p = await b.newPage({ viewport: { width: 480, height: 760 } }); const errs = [];
    p.on('pageerror', e => errs.push(String(e)));
    await p.goto('file://' + path.resolve(process.argv[2], f));
    const bad = await p.evaluate(() => document.getElementById('mv').__sweep(500));
    const ok = await p.evaluate(() => document.querySelector('#mv .o').textContent);
    await p.screenshot({ path: path.join(process.argv[3], f.replace('.html', '.png')) });
    console.log(errs.length || bad.length ? 'FAIL' : 'ok  ', f, '| default:', ok.slice(0, 2), '| bad:', bad.slice(0, 2).join(' '), errs.join(';'));
    if (errs.length || bad.length) fail = 1; await p.close();
  } await b.close(); process.exit(fail);
})();
