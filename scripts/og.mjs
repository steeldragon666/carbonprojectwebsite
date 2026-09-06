/**
 * Renders Open Graph cards with the real site typography, using the same
 * Chromium that ships with Playwright. Run before `astro build`.
 */
import { chromium } from 'playwright';
import { readFileSync, mkdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const b64 = (p) => readFileSync(root + p).toString('base64');

const display = b64('node_modules/@fontsource-variable/big-shoulders-display/files/big-shoulders-display-latin-wght-normal.woff2');
const body = b64('node_modules/@fontsource/barlow/files/barlow-latin-500-normal.woff2');

const cards = [
  { file: 'default', title: 'Your data never leaves this site.', sub: 'Sovereign AI inference, robotics and zero-emission power, on hardware we own in Victoria.' },
  { file: 'services', title: 'Four ways to engage.', sub: 'Sovereign inference. Fine-tuning and testing. AI and robotics consulting. Facility upgrades.' },
  { file: 'sovereign-inference', title: 'Sovereign inference', sub: 'Dedicated on-shore capacity on hardware we own. Reserved, never resold.' },
  { file: 'fine-tuning', title: 'Fine-tuning, modification and testing', sub: 'Fixed scope. Measured before it ships.' },
  { file: 'ai-robotics-consulting', title: 'AI and robotics consulting', sub: 'Agent architecture and physical automation, from review to working cell.' },
  { file: 'facility-upgrade', title: 'Facility upgrading and future-proofing', sub: 'Site audit, then staged works.' },
  { file: 'power', title: 'Silent power. No exhaust.', sub: '250 kVA hydrogen fuel-cell generation for hire. 800 A per unit.' },
  { file: 'facility', title: 'We future-proofed our own site first.', sub: 'Compute, power, robotics and fabrication under one roof.' },
  { file: 'research', title: 'Five domains. One workshop.', sub: 'Environmental, defence, energy, agriculture, e-commerce.' },
  { file: 'how-we-work', title: 'Short, fixed, and measurable.', sub: 'Scope. Pilot. Deploy. Operate.' },
  { file: 'contact', title: 'Tell us what you need.', sub: 'aaron@carbonproject.com.au. We reply within one business day.' },
];

const rivet = (x, y) => `<svg style="position:absolute;left:${x}px;top:${y}px" width="22" height="22" viewBox="0 0 14 14"><circle cx="7" cy="7" r="6" fill="#f5c400" stroke="#000" stroke-width="2"/><path d="M4 7h6" stroke="#000" stroke-width="2" stroke-linecap="square"/></svg>`;

const html = (c) => `<!doctype html><meta charset="utf-8"><style>
@font-face{font-family:BS;src:url(data:font/woff2;base64,${display}) format('woff2');font-weight:100 900}
@font-face{font-family:BA;src:url(data:font/woff2;base64,${body}) format('woff2');font-weight:500}
*{margin:0;box-sizing:border-box}
body{width:1200px;height:630px;background:#000;padding:26px;font-family:BA,sans-serif}
.pl{position:relative;width:100%;height:100%;background:#f5c400;color:#000;padding:64px 72px;display:flex;flex-direction:column;justify-content:space-between}
.pl::before{content:'';position:absolute;inset:18px;border:3px solid #000;pointer-events:none}
.id{display:inline-block;align-self:flex-end;border:3px solid #000;padding:10px 14px;font-family:BS;font-weight:700;font-size:20px;letter-spacing:.06em;text-transform:uppercase;line-height:1.15}
.id span{display:block;font-family:BA;font-weight:500;text-transform:none;letter-spacing:0;font-size:17px;color:#3f3b28}
h1{font-family:BS;font-weight:800;text-transform:uppercase;font-size:${c.title.length > 30 ? 96 : 118}px;line-height:.88;letter-spacing:.005em;max-width:11ch}
.sub{font-size:26px;line-height:1.3;color:#3f3b28;max-width:38ch;margin-top:22px}
.foot{display:flex;justify-content:space-between;font-family:BS;font-weight:700;font-size:20px;letter-spacing:.08em;text-transform:uppercase;border-top:3px solid #000;padding-top:16px}
</style>
<body><div class="pl">
${rivet(7,7)}${rivet(1200-52-7-22,7)}${rivet(7,630-52-7-22)}${rivet(1200-52-7-22,630-52-7-22)}
<div class="id">Carbon Project Australia<span>Established 2019. Mornington Peninsula, VIC</span></div>
<div><h1>${c.title}</h1><div class="sub">${c.sub}</div></div>
<div class="foot"><span>carbonproject.ai</span><span>Sovereign by design</span></div>
</div></body>`;

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
