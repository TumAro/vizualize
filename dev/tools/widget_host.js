// Simulates the claude.ai inline-widget host: fragment injected via innerHTML, scripts executed once afterwards,
// host CSS vars (light+dark), sendPrompt stub. usage: node widget_host.js <dir-of-fragments> <out-dir>
const { chromium } = require(process.env.PW_MODULE || 'playwright'); const fs = require('fs'), path = require('path');
const HOST = (frag, dark) => `<!doctype html><body style="margin:0;padding:16px;width:680px;background:${dark ? '#1a1a1a' : '#fff'};--color-text-primary:${dark ? '#eee' : '#111'};--color-text-secondary:${dark ? '#aaa' : '#555'};--color-border-secondary:${dark ? '#666' : '#999'};--color-border-tertiary:${dark ? '#444' : '#ccc'};font-family:system-ui;color:${dark ? '#eee' : '#111'}"><div id="host"></div><script>window.__sent=[];window.sendPrompt=t=>window.__sent.push(t);</script></body>`;
(async () => {
  const b = await chromium.launch(); let fail = 0;
  for (const f of fs.readdirSync(process.argv[2]).filter(f => f.endsWith('.frag'))) {
    for (const dark of [false, true]) {
      const p = await b.newPage({ viewport: { width: 720, height: 900 } }); const errs = [];
      p.on('pageerror', e => errs.push(String(e))); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
      await p.setContent(HOST('', dark));
      const frag = fs.readFileSync(path.join(process.argv[2], f), 'utf8');
      await p.evaluate(h => { const d = document.getElementById('host'); d.innerHTML = h; d.querySelectorAll('script').forEach(s => { const n = document.createElement('script'); n.textContent = s.textContent; s.replaceWith(n); }); }, frag);
      let bad = [], sent = 0;
      if (frag.includes('data-mv')) {
        bad = await p.evaluate(() => document.getElementById('mv').__sweep(300)); const btn = await p.$('#mv button');
        if (btn) { await btn.click(); sent = await p.evaluate(() => window.__sent.length); }
      }
      await p.screenshot({ path: path.join(process.argv[3], f.replace('.frag', dark ? '-dark.png' : '-light.png')), fullPage: true });
      const isSlider = f.startsWith('slider');
      const ok = !errs.length && !bad.length && (!isSlider || sent === 1);
      console.log(ok ? 'ok  ' : 'FAIL', f, dark ? 'dark' : 'light', isSlider ? `sendPrompt=${sent}` : '', bad.slice(0, 1).join(''), errs.join(';')); if (!ok) fail = 1; await p.close();
    }
  } await b.close(); process.exit(fail);
})();
