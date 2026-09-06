# Claims register

Every substantive factual claim on the site, where it came from, and whether it
is safe to publish as written.

Why this file exists: under **Australian Consumer Law s18** a business must not
engage in misleading or deceptive conduct, and the **ACCC's guidance on
environmental and sustainability claims** treats vague or unqualified green
claims as a specific enforcement priority. A capability statement that a
procurement officer relies on is exactly the kind of document that gets tested.

**Rule for this repo:** do not add a number or an absolute claim to
`src/data/site.ts` or `src/data/services.ts` without adding a row here.

---

## Status key

| | |
| --- | --- |
| ✅ | Safe as written |
| ⚠️ | Published in softened form — **substantiation still needed** |
| 🔴 | Removed from the previous site — do not reinstate without evidence |

---

## Company

| Claim | Source | Status |
| --- | --- | --- |
| Established 2019 | Previous site ("2019 FOUNDED") and the reference design ("Established 2019") | ✅ |
| Mornington Peninsula, Victoria; about an hour from Melbourne | Reference design | ✅ |
| R&D performing entity and research conveyor for partner companies | Reference design | ✅ |
| Registered defence contractor | Reference design badge | ⚠️ Confirm current registration status and the exact scheme name before launch. This claim will be checked by defence buyers. |
| Six years in soil-carbon trading and measurement technology | Reference design | ⚠️ Consistent with a 2019 founding. Confirm the wording you want to stand behind. |

## Facility and inference

| Claim | Source | Status |
| --- | --- | --- |
| Hardware owned and operated by Carbon Project Australia; no sub-let racks | Reference design | ⚠️ True only while it stays true. If any capacity is ever sub-let, this wording must change the same day. |
| On-site renewable generation, storage and zero-emission backup | Reference design | ✅ |
| Requests answered on Australian soil, under Australian law | Reference design | ✅ Provided the data-handling schedule in the client agreement says the same thing. |
| "Reserved capacity is not resold" | Written for this site as a commercial commitment | ⚠️ This is a promise, not a description. Confirm you can operate to it. |
| "Your prompts and responses are not used to train anything" | Written for this site | ⚠️ Must match the executed agreement. |

## Hydrogen fuel-cell power

| Claim | Previous wording | Status on this site |
| --- | --- | --- |
| Output | "250kVA" / "250kW fuel cells" — the previous site used kVA and kW interchangeably | ⚠️ Published as **250 kVA per unit**. kVA and kW are not the same thing; confirm which is correct and correct `src/pages/power/index.astro` if needed. |
| Current | "800A per unit" | ⚠️ Published as written. Confirm against the datasheet. |
| Noise | **"0 dB NOISE EMISSIONS"** | 🔴 **Removed.** Nothing is 0 dB. Published as *"No combustion and no engine. Audible output is limited to auxiliary cooling — measured figures available on request."* Supply a measured dB(A) figure at a stated distance and it can be published as a number. |
| Carbon | **"Carbon Neutral — hydrogen fuel cells produce zero carbon emissions"** | 🔴 **Removed as an unqualified claim.** Published as: no carbon emission *at the point of use*; lifecycle carbon depends on the hydrogen source. This is the position the ACCC's environmental-claims guidance expects, and it is a stronger sales argument because it is checkable. |
| Market position | **"the only company in the country"** / **"We are the only company in Australia offering hydrogen fuel cell generators that can output 800A per unit"** | ⚠️ Published as *"To our knowledge, no other Australian supplier hires out hydrogen fuel-cell generation at 800 A per unit."* A bare absolute superiority claim is the classic s18 exposure. Either supply the market scan that supports it, or leave the qualified wording. |
| Cost | "Cheaper at High Demand — lower cost per kWh than diesel at sustained high-power loads" | ✅ Published with the counter-case stated (diesel wins on light intermittent duty), which materially strengthens it. |
| Indoor installation | "No exhaust means these units can be installed indoors" | ⚠️ Published with the qualifier that indoor siting still needs a ventilation, gas-detection and fire-safety assessment. Do not drop that qualifier. |

## Impact statistics — all removed

The previous site displayed four animated counters that rendered as `0`:

| Previous claim | Status |
| --- | --- |
| "0+ Hectares Under Management — across Victoria, NSW and Queensland" | 🔴 Not published. Supply a real figure and a date. |
| "0M Trees Planted" | 🔴 Not published. |
| "0K Tonnes CO₂ Sequestered — verified carbon credits generated" | 🔴 Not published. **"Verified carbon credits" is a regulated term.** Do not publish without naming the scheme and the verifying body. |
| "0 Autonomous Vehicles Deployed — operating across 14 project sites" | 🔴 Not published. |
| "98% seedling survival" | 🔴 Not published. Needs a measurement method and a sample. |
| "10x planting speed" | 🔴 Not published. Ten times *what*, measured how? |
| "14 active sites" | 🔴 Not published. |
| "24/7 autonomous operation", "GPS-RTK centimetre precision" | 🔴 Not published on the new site. Reinstate on a technology page with equipment references if you want them. |

A real, dated, sourced number is worth more than four impressive ones a buyer
cannot check. When you have them, add them with a source column here first.

## Commercial promises made on this site

These are written as commitments. They are good commitments — they are also
enforceable. Confirm each one is how you actually operate before launch.

| Promise | Where |
| --- | --- |
| Scoping fee is fixed and credited in full against delivery | Home, all service pages, `how-we-work` |
| A written brief is produced at scoping and is yours to keep either way | `how-we-work`, `contact` |
| Pilots are fixed price and fixed date | Every service page |
| Monthly agreements are cancellable with no annual minimum and no auto-escalation | `how-we-work`, service pages |
| "We reply within one business day" | Site-wide, in the footer and every form | 
| ~~"Roughly half of scoping engagements end with a cheaper recommendation"~~ — softened to "regularly", no statistic claimed | `how-we-work`, `services/ai-robotics-consulting` |
| Weights, evaluation suite and data lineage handed over; client owns the trained model | `services/fine-tuning` |
| Facility audit is written to be tendered to any contractor | `services/facility-upgrade` |

## Legal pages

`legal/privacy` and `legal/terms` were written for this site and describe
handling that is standard for a marketing site plus an enquiry form. They are
**not legal advice** and have not been reviewed by an Australian lawyer. Have
them reviewed before launch, particularly the privacy notice if any enquiry data
will be processed by an overseas form or mail provider — that triggers APP 8.
