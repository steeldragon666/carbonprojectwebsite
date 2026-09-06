/**
 * Post-build verification. Serves dist/ and checks every page for the things
 * that actually broke on the previous site: empty HTML for crawlers, dead
 * links, unlabelled form fields, missing metadata and runaway payloads.
 *
 *   npm run build && npm run verify
 */
import { chromium } from 'playwright';
import { createServer } from 'node:http';
import { readFile, stat, readdir } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import { extname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const DIST = fileURLToPath(new URL('../dist', import.meta.url));
const PORT = 4399;
const MIME = {
  '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript',
  '.svg': 'image/svg+xml', '.png': 'image/png', '.ico': 'image/x-icon',
  '.xml': 'application/xml', '.txt': 'text/plain; charset=utf-8',
  '.json': 'application/json', '.webmanifest': 'application/manifest+json',
  '.woff2': 'font/woff2',
};

const server = createServer(async (req, res) => {
  const url = decodeURIComponent(req.url.split('?')[0]);
  const candidates = [join(DIST, url), join(DIST, url, 'index.html'), join(DIST, `${url}.html`)];
  for (const f of candidates) {
    if (!f.startsWith(DIST) || !existsSync(f)) continue;
    if ((await stat(f)).isDirectory()) continue;
    res.writeHead(200, { 'Content-Type': MIME[extname(f)] ?? 'application/octet-stream' });
    res.end(await readFile(f));
    return;
  }
  res.writeHead(404, { 'Content-Type': 'text/html' });
  res.end(existsSync(join(DIST, '404.html')) ? await readFile(join(DIST, '404.html')) : 'Not found');
});
await new Promise((r) => server.listen(PORT, '127.0.0.1', r));
const base = `http://127.0.0.1:${PORT}`;

/* Every built page, discovered from dist rather than hard-coded. */
const walk = async (dir, out = []) => {
  for (const e of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, e.name);
    if (e.isDirectory()) await walk(p, out);
    else if (e.name === 'index.html') out.push(p.slice(DIST.length, -'index.html'.length) || '/');
  }
  return out;
};
const routes = (await walk(DIST)).sort();

const problems = [];
const fail = (route, msg) => problems.push(`${route.padEnd(34)} ${msg}`);

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM_PATH || undefined });
const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 } });
const page = await ctx.newPage();

const consoleErrors = [];
page.on('pageerror', (e) => consoleErrors.push(String(e)));
page.on('console', (m) => m.type() === 'error' && consoleErrors.push(m.text()));

let totalBytes = 0;
const seenLinks = new Set();
const rows = [];

for (const route of routes) {
  const url = base + route;

  /* 1. The raw HTML a crawler sees must already contain the content. */
  const raw = await (await fetch(url)).text();
  const bytes = Buffer.byteLength(raw);
  totalBytes += bytes;
  if (!/<h1[\s>]/.test(raw)) fail(route, 'no <h1> in server HTML');
  if (bytes > 120_000) fail(route, `server HTML is ${(bytes / 1024).toFixed(0)} kB`);

  const res = await page.goto(url, { waitUntil: 'networkidle' });
  if (res.status() !== 200) fail(route, `status ${res.status()}`);

  const r = await page.evaluate(() => {
    const q = (s) => [...document.querySelectorAll(s)];
    const meta = (n) => document.querySelector(`meta[name="${n}"]`)?.content;
    const prop = (n) => document.querySelector(`meta[property="${n}"]`)?.content;
    const levels = q('h1,h2,h3,h4,h5,h6').map((h) => Number(h.tagName[1]));
    let skips = 0;
    for (let i = 1; i < levels.length; i++) if (levels[i] - levels[i - 1] > 1) skips++;
    return {
      title: document.title,
      titleLen: document.title.length,
      description: meta('description') ?? '',
      canonical: document.querySelector('link[rel=canonical]')?.href,
      ogImage: prop('og:image'),
      noindex: (meta('robots') ?? '').includes('noindex'),
      h1s: q('h1').length,
      headingSkips: skips,
      lang: document.documentElement.lang,
      jsonLd: q('script[type="application/ld+json"]').map((s) => s.textContent),
      imgsNoAlt: q('img').filter((i) => i.getAttribute('alt') === null).length,
      svgNoLabel: q('svg').filter((s) =>
        !s.getAttribute('aria-label') && !s.getAttribute('aria-labelledby') &&
        !s.querySelector('title') && s.getAttribute('aria-hidden') !== 'true').length,
      fieldsNoLabel: q('input,select,textarea').filter((i) => {
        if (i.type === 'hidden') return false;
        const id = i.id;
        const lab = id && document.querySelector(`label[for="${CSS.escape(id)}"]`);
        return !lab && !i.getAttribute('aria-label') && !i.closest('label');
      }).map((i) => i.name || i.type),
      emptyLinks: q('a').filter((a) =>
        !a.textContent.trim() && !a.getAttribute('aria-label') && !a.querySelector('[aria-label],title')).length,
      links: q('a[href]').map((a) => a.getAttribute('href')),
      hDocScroll: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      textLen: document.body.innerText.length,
    };
  });

  if (r.h1s !== 1) fail(route, `${r.h1s} <h1> elements (want exactly 1)`);
  if (r.headingSkips) fail(route, `${r.headingSkips} heading-level skip(s)`);
  if (!r.description) fail(route, 'no meta description');
  else if (r.description.length > 165) fail(route, `meta description ${r.description.length} chars`);
  if (r.titleLen > 65) fail(route, `title ${r.titleLen} chars`);
  if (!r.canonical) fail(route, 'no canonical');
  if (!r.ogImage) fail(route, 'no og:image');
  if (r.lang !== 'en-AU') fail(route, `lang="${r.lang}"`);
  if (r.imgsNoAlt) fail(route, `${r.imgsNoAlt} img without alt`);
  if (r.svgNoLabel) fail(route, `${r.svgNoLabel} svg without accessible name`);
  if (r.fieldsNoLabel.length) fail(route, `unlabelled field(s): ${r.fieldsNoLabel.join(', ')}`);
  if (r.emptyLinks) fail(route, `${r.emptyLinks} link(s) with no accessible name`);
  if (r.hDocScroll) fail(route, 'page scrolls horizontally at 1280px');
  if (r.textLen < 400 && !r.noindex) fail(route, `thin page (${r.textLen} chars)`);
  for (const s of r.jsonLd) {
    try { JSON.parse(s); } catch { fail(route, 'invalid JSON-LD'); }
  }

  r.links.filter((h) => h.startsWith('/')).forEach((h) => seenLinks.add(h.split('#')[0]));
  rows.push({ route, kB: +(bytes / 1024).toFixed(1), text: r.textLen, title: r.title });

  /* Narrow viewport must not scroll sideways either. */
  await page.setViewportSize({ width: 360, height: 780 });
  const overflow = await page.evaluate(() =>
    document.documentElement.scrollWidth > document.documentElement.clientWidth + 1);
  if (overflow) fail(route, 'page scrolls horizontally at 360px');
  await page.setViewportSize({ width: 1280, height: 900 });
}

/* 2. No internal link may 404. */
for (const href of [...seenLinks].sort()) {
  const res = await fetch(base + href, { redirect: 'manual' });
  if (res.status !== 200) fail(href, `internal link returns ${res.status}`);
}

/* 3. Files the previous site served as HTML must be real files. */
for (const f of ['/robots.txt', '/sitemap-index.xml', '/llms.txt', '/site.webmanifest', '/favicon.svg']) {
  const res = await fetch(base + f);
  const ct = res.headers.get('content-type') ?? '';
  if (res.status !== 200) fail(f, `status ${res.status}`);
  else if (ct.includes('text/html')) fail(f, `served as HTML (${ct})`);
}

/* 4. A missing page must not answer 200. */
const soft404 = await fetch(`${base}/definitely-not-a-page-xyz/`);
if (soft404.status === 200) fail('/404', 'unknown URL returns 200 (soft 404)');

if (consoleErrors.length) problems.push(`console errors: ${consoleErrors.slice(0, 5).join(' | ')}`);

console.table(rows);
console.log(`\n${routes.length} routes · ${(totalBytes / 1024).toFixed(0)} kB of HTML total`);

await browser.close();
server.close();

if (problems.length) {
  console.error(`\n✗ ${problems.length} problem(s):\n` + problems.map((p) => '  ' + p).join('\n'));
  process.exit(1);
}
console.log('\n✓ all checks passed');
