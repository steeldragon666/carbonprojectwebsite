# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Three buyer groups, in this order of priority (confirmed by the owner, 2026-09-06):

1. **Defence and government buyers** — procurement and risk officers who must prove data sovereignty, jurisdiction and accreditation before an AI workload can be approved. They arrive from a tender, a referral or a search for "sovereign AI Australia", usually with a risk assessment to complete.
2. **Enterprise technical buyers** — CTOs, CISOs and heads of data who need a credible on-shore alternative to hyperscaler AI for regulated or sensitive workloads.
3. **Industrial operations buying power hire** — events, construction, mining and data-centre operators who need silent, zero-emission generation on sites where a diesel set is restricted or not allowed.

The front page is led by sovereign AI for groups 1 and 2. Power hire and R&D have their own pages and are strong second acts, not afterthoughts.

## Product Purpose

Carbon Project Australia Pty Ltd runs and fine-tunes AI models on hardware it owns, at a self-powered research and fabrication facility on the Mornington Peninsula, Victoria. It also hires out hydrogen fuel-cell generation and performs R&D for partner companies across environmental, defence, energy, agriculture and e-commerce domains.

Success for the site: a qualified buyer books a scoping call or sends an enquiry with enough detail to quote. Secondary: a procurement officer can extract what they need for a tender without calling.

## Positioning

**Lead claim (confirmed): "Your data never leaves our site."** Requests arrive over an encrypted link and are answered on infrastructure the company owns, on Australian soil, under Australian law. This is a property of a building, not a policy.

The claim a neighbouring vendor cannot truthfully copy: the compute, the robotics, the fabrication **and the electricity that runs them** are on one site, owned and operated by the same company. Most "Australian AI" is an Australian invoice in front of offshore infrastructure.

## Operating Context

- Buyers evaluate through written scopes, data-handling schedules, risk assessments and tenders. Documentation that can be pasted into a tender is part of the product.
- Every engagement runs Scope → Pilot → Deploy → Operate. Scoping is a fixed fee credited against delivery; pilots are fixed price and fixed date; operating agreements are monthly and cancellable.
- Prices are not published. Every price is quoted in writing at scoping.
- Site visits are by appointment, about an hour from Melbourne.
- Enquiries go to aaron@carbonproject.com.au. Response within one business day.

## Capabilities and Constraints

Confirmed offers (source: `src/data/site.ts`, `src/data/services.ts`):

- Sovereign inference — reserved GPU capacity, OpenAI-compatible endpoint, monthly or per project.
- Fine-tuning, modification and testing — fixed-scope projects with a written test report.
- AI and robotics consulting — retained advisory or scoped delivery, including robot-cell design.
- Facility upgrading and future-proofing — site audit, then staged works.
- Zero-emission power hire — 250 kVA hydrogen fuel-cell units, 800 A per unit, AC/DC, indoor-capable.

Facility (nominal): dedicated GPU compute, on-site renewable generation with storage and zero-emission backup, collaborative robotics and machine vision, additive and conventional fabrication, hardened private network.

R&D domains: environmental, defence (registered defence contractor — scheme name to be confirmed), energy, agriculture, e-commerce.

Constraints:
- Static site (Astro). No client framework. Deployable to any static host; Cloudflare Pages form handler included.
- No third-party analytics, fonts or trackers. This is a sovereignty product and the site must not undercut it.
- Every factual claim is tracked in `docs/CLAIMS-REGISTER.md`. Claims marked ⚠️ or 🔴 there must not be strengthened on the site.
- **Undecided:** 250 kVA vs 250 kW; measured noise figure; substantiation of the "only Australian supplier at 800 A" claim; the defence-contractor scheme name. Do not resolve these on the site.

## Brand Commitments

- Name: Carbon Project Australia (legal: Carbon Project Australia Pty Ltd). Established 2019.
- Voice (from confirmed copy): plain, declarative, engineering-led. Says what a service is *not*. Tells a buyer when not to buy. No superlatives without a qualifier.
- Incumbent logo mark: an amber square carrying a busbar glyph (`public/favicon.svg`). Incumbent, not confirmed as binding — may be redrawn if the new visual world requires it, but the amber-as-energised idea has been used consistently and should be treated as recognisable.

## Evidence on Hand

- Real: the offer structure, commercial terms, facility specification (nominal), R&D domains, the legal entity, the contact address.
- **Absent, must not be fabricated:** customer names, testimonials, case studies, usage statistics, hectares/trees/CO₂ figures, uptime or latency numbers, certifications beyond "registered defence contractor", team photos, real photographs of the facility or hardware.
- **Imagery decision (confirmed):** the site may use AI-generated imagery from Higgsfield as *illustrative* plates. It must be credited as illustrative and must not be presented as photographs of the company's facility, hardware or people.

## Product Principles

1. Sovereignty is a property of a building. Show the building's logic, not a cloud abstraction.
2. Say the number or say nothing. No decorative statistics, no invented proof.
3. Tell the buyer when not to buy. Disqualifying the wrong customer is part of the sale.
4. Everything a procurement officer needs must be extractable without a phone call.
5. The site itself must not contradict the product: no third-party trackers, fonts or scripts.

## Accessibility & Inclusion

WCAG 2.2 AA is the working floor (inferred from prior build decisions, not owner-stated): 4.5:1 text contrast, 3:1 control boundaries, visible focus, reduced-motion respected, every form field labelled.
