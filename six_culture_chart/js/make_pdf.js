// Print a LIFE_MAP.html to a shareable A4 PDF (evidence drawers expanded, menu hidden).
// Usage: NODE_PATH=$(npm root -g) node js/make_pdf.js <LIFE_MAP.html> <out.pdf> "<footer title>"
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [src, out, title] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' }).catch(() => chromium.launch());
  const p = await b.newPage({ colorScheme: 'light' });
  await p.goto('file://' + path.resolve(src), { waitUntil: 'networkidle' });
  await p.evaluate(() => {
    document.querySelectorAll('details').forEach(d => (d.open = true));
    const s = document.createElement('style');
    s.textContent = 'nav.toc{display:none!important} figure,.hero,.domain,.chapter,.frame,.timeline{break-inside:avoid}' +
      ' .sec-head{break-after:avoid} section{margin-top:36px}';
    document.head.appendChild(s);
  });
  await p.emulateMedia({ media: 'screen', colorScheme: 'light' });
  await p.pdf({ path: out, format: 'A4', printBackground: true, scale: 0.72,
    margin: { top: '12mm', bottom: '14mm', left: '10mm', right: '10mm' }, displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: `<div style="font-size:8px;width:100%;text-align:center;color:#666">${title} · page <span class="pageNumber"></span> of <span class="totalPages"></span></div>` });
  await b.close();
})();
