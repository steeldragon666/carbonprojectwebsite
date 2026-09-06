# carbonproject.ai

Static site for **Carbon Project Australia** — sovereign AI inference, robotics,
and zero-emission power, run from a self-powered facility on the Mornington
Peninsula, Victoria.

Built with [Astro](https://astro.build). Every page is pre-rendered HTML with no
client-side framework, so a crawler, a screen reader and a slow connection all
get the content on the first response.

---

## Quick start

```bash
npm install
npm run dev        # http://localhost:4321
```

## Scripts

| Script | What it does |
| --- | --- |
| `npm run dev` | Dev server with hot reload |
| `npm run build` | Static build into `dist/` |
| `npm run check` | Astro + TypeScript diagnostics |
| `npm run verify` | Serves `dist/` and audits every page (see below) |
| `npm run build:verify` | Build, then verify |
| `npm run assets` | Regenerate favicons and Open Graph cards |

`npm run verify` is the safety net. It walks every built route and fails the
build on: a page whose server HTML has no `<h1>`, a missing or over-long title
or meta description, a missing canonical or `og:image`, a heading-level skip, an
unlabelled form field, an `img` with no `alt`, an `svg` with no accessible name,
a dead internal link, horizontal overflow at 360 px or 1280 px, a `robots.txt`
or `sitemap` served as HTML, or an unknown URL answering `200`. Every one of
those was a real defect on the previous site.

`npm run assets` needs a local Chromium (Playwright). The generated files in
`public/` are committed, so CI and hosting never need a browser to build.

---

## Editing content

Almost everything a non-developer would want to change lives in two files:

- **`src/data/site.ts`** — company details, contact address, navigation, the
  four service offers, R&D domains, facility specification, engagement steps.
- **`src/data/services.ts`** — the long-form body, commercial structure and FAQ
  for each service page.

Page files in `src/pages/` render that data. Adding a service means adding an
entry to `offers` in `site.ts` and a matching entry in `services.ts` — the page,
the sitemap, the schema markup and the OG card list follow automatically.

> **Before adding a number to `site.ts`, add it to
> [`docs/CLAIMS-REGISTER.md`](docs/CLAIMS-REGISTER.md)** with its source. Several
> claims inherited from the previous site are unverified and are flagged there.

## Enquiry form

The form posts to `PUBLIC_FORM_ENDPOINT`. **If that variable is unset, the form
hands the enquiry to the visitor's mail client instead** — it never posts into a
void, which is what the previous site's form did.

Options, in rough order of effort:

1. **Cloudflare Pages** — `functions/api/enquiry.ts` is included. Set
   `PUBLIC_FORM_ENDPOINT=/api/enquiry` at build time and `RESEND_API_KEY`,
   `ENQUIRY_TO`, `ENQUIRY_FROM` in the Pages project.
2. **A hosted form service** — set `PUBLIC_FORM_ENDPOINT` to a Formspree or
   Web3Forms endpoint. The form already sends `_subject` and `_next` fields.
3. **Nothing** — the mailto fallback works everywhere.

Copy `.env.example` to `.env` to set it locally.

## Deploying

The output is plain static files in `dist/`; any static host works.

- **Cloudflare Pages** — build `npm run build`, output `dist`. `public/_headers`
  and `public/_redirects` are applied automatically.
- **Netlify** — `netlify.toml` is configured. `_headers`/`_redirects` apply.
- **Vercel** — `vercel.json` carries the same headers and redirects.

`public/_headers` sets HSTS, `nosniff`, `X-Frame-Options`, a referrer policy, a
content security policy, and immutable caching for hashed assets.

## Structure

```
src/
  components/   Header, Footer, Section, PageHeader, EnquiryForm,
                Faq, CtaBand, SingleLine (the hero schematic), Logo
  data/         site.ts, services.ts  ← content lives here
  layouts/      Base.astro — head, SEO, JSON-LD, page chrome
  pages/        one file per route; services/[slug].astro is generated
  styles/       global.css — design tokens and shared primitives
functions/api/  optional Cloudflare Pages form handler
scripts/        icons.mjs, og.mjs, verify.mjs
docs/           AUDIT.md, CLAIMS-REGISTER.md
```

## Design system

The visual world is **Switchyard Placard**: the page is the site's own safety
signage. Signal-yellow enamel placards carry the surface, black panels
instruct, white exists only as text on black. Rivets at placard corners, 2px
rules, zero radius, no gradients or glass. Display type is Big Shoulders
Display (condensed caps), body is Barlow, both self-hosted through Fontsource.
Tokens live at the top of `src/styles/global.css`; every page uses the
`Placard`, `Plate`, `.plate` (nameplate rows) and `.sw` (switch button)
primitives. The direction contract and product truth are recorded for future
rounds in `PRODUCT.md`, `DESIGN.md` and `.impeccable/surfaces/`.

Imagery is generated (Higgsfield) and illustrative. Every plate carries an
"Illustrative image" label, the footer says so, and each PNG carries its
generation prompt as embedded metadata. None of it depicts the real facility.
