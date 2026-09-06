/**
 * Renders Open Graph cards with the real site typography, using the same
 * Chromium that ships with Playwright. Run before `astro build`.
 */
import { chromium } from 'playwright';
import { readFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const b64 = (p) => readFileSync(root + p).toString('base64');

const display = b64('node_modules/@fontsource-variable/space-grotesk/files/space-grotesk-latin-wght-normal.woff2');
const body = b64('node_modules/@fontsource-variable/inter/files/inter-latin-wght-normal.woff2');
const mono = b64('node_modules/@fontsource-variable/jetbrains-mono/files/jetbrains-mono-latin-wght-normal.woff2');

const cards = [
  { file: 'default', eyebrow: 'Capability statement', title: 'Sovereign AI inference, powered on site.', sub: 'Mornington Peninsula, Victoria · Established 2019' },
  { file: 'services', eyebrow: 'Services', title: 'Four ways to engage.', sub: 'Inference · Fine-tuning · Robotics · Facilities' },
  { file: 'sovereign-inference', eyebrow: '01 — Service', title: 'Sovereign inference', sub: 'Dedicated on-shore capacity on hardware we own' },
  { file: 'fine-tuning', eyebrow: '02 — Service', title: 'Fine-tuning, modification and testing', sub: 'Fixed scope. Measured before it ships.' },
  { file: 'ai-robotics-consulting', eyebrow: '03 — Service', title: 'AI and robotics consulting', sub: 'Agent architecture and physical automation' },
  { file: 'facility-upgrade', eyebrow: '04 — Service', title: 'Facility upgrading and future-proofing', sub: 'Site audit, then staged works' },
  { file: 'power', eyebrow: '05 — Zero-emission power', title: 'Silent power. No exhaust.', sub: '250 kVA hydrogen fuel cells · 800 A per unit' },
  { file: 'facility', eyebrow: 'The facility', title: 'We future-proofed our own site first.', sub: 'Compute · Power · Robotics · Fabrication' },
  { file: 'research', eyebrow: 'Research and development', title: 'Five domains, one workshop.', sub: 'Environmental · Defence · Energy · Agriculture · E-commerce' },
  { file: 'how-we-work', eyebrow: 'How we work', title: 'Short, fixed, and measurable.', sub: 'Scope · Pilot · Deploy · Operate' },
  { file: 'contact', eyebrow: 'Enquiries', title: 'Tell us what you need.', sub: 'aaron@carbonproject.com.au · One business day' },
];

const html = (c) => `<!doctype html><meta charset="utf-8"><style>
@font-face{font-family:SG;src:url(data:font/woff2;base64,${display}) format('woff2');font-weight:100 900}
@font-face{font-family:IN;src:url(data:font/woff2;base64,${body}) format('woff2');font-weight:100 900}
@font-face{font-family:JB;src:url(data:font/woff2;base64,${mono}) format('woff2');font-weight:100 900}
*{margin:0;box-sizing:border-box}
body{width:1200px;height:630px;background:#f4f3ef;color:#14150f;font-family:IN,sans-serif;
  display:flex;flex-direction:column;justify-content:space-between;padding:64px 72px;
  border-bottom:14px solid #edb200}
.top{display:flex;align-items:center;gap:14px}
.mark{width:34px;height:34px;border:2px solid #14150f;border-radius:3px;background:#edb200;position:relative}
.mark i{position:absolute;background:#14150f}
.mark .bus{left:5px;right:5px;height:3px;bottom:9px}
.mark .a{width:3px;height:11px;left:8px;bottom:11px}
.mark .b{width:3px;height:17px;left:15px;bottom:11px}
.mark .c{width:3px;height:8px;left:22px;bottom:11px}
.brand{font-family:SG;font-weight:600;font-size:24px;letter-spacing:-.02em}
.eyebrow{font-family:JB;font-size:16px;letter-spacing:.12em;text-transform:uppercase;color:#74766c;
  padding-bottom:22px;border-bottom:1px solid #d5d3c9;margin-bottom:26px}
h1{font-family:SG;font-weight:600;font-size:${c.title.length > 34 ? 62 : 76}px;line-height:1.03;letter-spacing:-.028em;max-width:16ch}
.sub{font-family:JB;font-size:19px;color:#4a4c43;letter-spacing:.01em;margin-top:26px}
.foot{display:flex;justify-content:space-between;align-items:baseline;font-family:JB;font-size:15px;
  letter-spacing:.09em;text-transform:uppercase;color:#74766c;border-top:1px solid #d5d3c9;padding-top:20px}
</style>
<body>
<div class="top"><span class="mark"><i class="bus"></i><i class="a"></i><i class="b"></i><i class="c"></i></span><span class="brand">Carbon Project Australia</span></div>
<div><div class="eyebrow">${c.eyebrow}</div><h1>${c.title}</h1><div class="sub">${c.sub}</div></div>
<div class="foot"><span>carbonproject.ai</span><span>Scale NTS</span></div>
</body>`;

mkdirSync(root + 'public/og', { recursive: true });
const browser = await chromium.launch({
  executablePath: process.env.CHROMIUM_PATH || undefined,
});
const page = await browser.newPage({ viewport: { width: 1200, height: 630 }, deviceScaleFactor: 1 });
for (const c of cards) {
  await page.setContent(html(c), { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: `${root}public/og/${c.file}.png` });
  console.log('og:', c.file);
}
await browser.close();
