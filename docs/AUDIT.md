# Audit — carbonproject.ai (as it stood 2026-09-06)

Measured against the live site at `https://carbonproject.ai/`, rendered in
Chromium and inspected at the network and DOM level. Findings are ordered by
commercial impact, not by severity label.

**Summary.** The site was a single-page React application hosted on Manus. It
served **369 kB of HTML containing zero content** — the entire page was built in
the browser from a ~596 kB JavaScript bundle plus a ~366 kB inline runtime
script. `robots.txt` and `sitemap.xml` did not exist and returned the HTML shell
with a `200`. Any unknown URL also returned `200`. The contact form had no
`action` and no `method` beyond the default `GET`, so submitted enquiries went
nowhere. The four headline impact statistics rendered as `0`.

---

## 1. The site was invisible to search engines and language models

| Check | Live site | Consequence |
| --- | --- | --- |
| Content in server HTML | `<div id="root"></div>` — nothing else | Crawlers that do not execute JavaScript see an empty page |
| `robots.txt` | Returned 368 kB of HTML with `200` | No crawl directives; no sitemap discovery |
| `sitemap.xml` | Returned the HTML shell with `200` | Nothing submitted to Search Console will validate |
| `llms.txt` | Same HTML shell | Agents and LLM crawlers get markup, not facts |
| Unknown URL | `200` + HTML shell | Soft-404s; every typo'd URL becomes an indexable duplicate |
| Structured data | None | No Organization, Service, FAQ or Breadcrumb markup |
| Pages | One | One URL competing for every query the business cares about |

The last row is the expensive one. "Hydrogen generator hire Melbourne",
"sovereign AI inference Australia" and "robotic tree planting" are different
buyers with different intent, and a single scrolling page cannot rank for all
three. There was no page to send a paid click to either.

## 2. The contact form did not work

```html
<form>                       <!-- no action, no method -->
  <input type="text">        <!-- no label, no name, no autocomplete -->
  <input type="email">
  <textarea></textarea>
  <button>Send Enquiry</button>
</form>
```

Three unlabelled fields, no `name` attributes, no `action`. Screen-reader users
could not tell what any field was for, and nobody's enquiry reached anyone. For
a business whose entire funnel is "get a scoping call", this was the single
most costly defect on the site.

## 3. Payload

| | Live site | This rebuild |
| --- | --- | --- |
| HTML, home page | 369.6 kB | 40.7 kB |
| JavaScript | ~596 kB module + ~366 kB inline runtime | 0 kB on every page except the mailto fallback (~1 kB, only when no form endpoint is set) |
| CSS | 130.7 kB external, plus the same CSS again inside the inline script | Inlined per page, a few kB |
| Fonts | Google Fonts, third-party request | Self-hosted, same origin |
| Third-party requests | Google Fonts, `manus-analytics.com`, `d2xsxph8kpxj0f.cloudfront.net` | None |
| Total HTML, whole site | 369.6 kB for 1 page | 343 kB for **14 pages** |

The third-party analytics call is worth noting separately: a company selling
data sovereignty was sending every visitor's page views to a third-party
analytics host on someone else's infrastructure.

## 4. Accessibility

- Form fields had no labels and no accessible names.
- Impact counters animated from `0` and rendered as `0+`, `0M`, `0K`, `0` on
  first paint and for any user with reduced motion or no JavaScript.
- No skip link.
- No `prefers-reduced-motion` handling on the scroll-driven animations.
- Images relied on remote CloudFront objects with no dimensions set, so layout
  shifted as they arrived.

## 5. Claims that create legal exposure

Several statements would need substantiation under Australian Consumer Law
s18 (misleading or deceptive conduct) and the ACCC's guidance on environmental
claims. They are itemised with recommended wording in
[`CLAIMS-REGISTER.md`](CLAIMS-REGISTER.md). The three that matter most:

1. **"0 dB noise emissions."** Nothing is 0 dB. Rewritten as *no combustion and
   no engine; audible output limited to auxiliary cooling, measured figures on
   request*.
2. **"Carbon neutral."** Fuel cells emit no carbon *at the point of use*;
   lifecycle carbon depends entirely on the hydrogen source. Rewritten to say
   exactly that, which is both defensible and a stronger sales position.
3. **"The only company in Australia…"** An unqualified absolute superiority
   claim. Rewritten as a qualified, falsifiable statement.

## 6. Positioning

The live site sold reforestation robotics. The reference design the business is
moving to sells sovereign AI inference. Both are real, and the second is the
higher-value line — but the generator hire business was buried at section 02 of
a scrolling page with no page of its own, no specification table a procurement
officer could paste into a tender, and no route from a search result to a quote.

---

## What this rebuild changes

| Was | Now |
| --- | --- |
| 1 page | 14 pages, one per buyer intent |
| Empty server HTML | Full content in the first response, no framework JS |
| No `robots.txt` / `sitemap.xml` | Real files, plus `llms.txt` for agents |
| Soft 404s | A real 404 page |
| No structured data | Organization, WebSite, Service, FAQPage, HowTo, BreadcrumbList |
| Form posts nowhere | Configurable endpoint, Cloudflare handler included, mailto fallback so a lead is never lost |
| Unlabelled fields | Labelled, `autocomplete`-annotated, honeypot-protected |
| Generator hire buried | Its own page with a specification table and a quote path |
| Four vague service mentions | Four service pages, each with deliverables, commercial structure, lead time, what it is *not*, and FAQs |
| Third-party analytics and fonts | Neither |
| No regression protection | `npm run verify` fails the build on any of the above |

Nothing here is verified against production until the site is deployed; the
figures above are measured against `dist/` served locally.
