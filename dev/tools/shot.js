// usage: node shot.js in.html out.png   (headless chromium; set PLAYWRIGHT_BROWSERS_PATH)
const { chromium } = require(process.env.PW_MODULE || 'playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1000, height: 900 } });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => m.type()==='error' && errs.push(m.text()));
  await p.goto('file://' + require('path').resolve(process.argv[2])); await p.waitForTimeout(1500);
  await p.screenshot({ path: process.argv[3], fullPage: true }); await b.close();
  if (errs.length) { console.error('PAGE ERRORS:', errs.join('\n')); process.exit(2); }
})();
