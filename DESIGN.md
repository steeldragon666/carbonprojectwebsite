---
name: Carbon Project Australia
description: Switchyard Placard. The site is its own safety signage, enamel placards bolted to a black wall.
colors:
  signal-yellow: "#f5c400"
  pressed-yellow: "#dcaf00"
  wall-black: "#000000"
  enamel-white: "#ffffff"
  galvanised-steel: "#767260"
  steel-on-yellow: "#6b6647"
  ink-on-yellow: "#3f3b28"
  ink-on-black: "#b8b3a3"
  pressed-black: "#26230f"
  fault-red: "#c0392b"
typography:
  placard-headline:
    fontFamily: "Big Shoulders Display Variable, Big Shoulders Display, Barlow Condensed, Arial Narrow, sans-serif"
    fontSize: "clamp(3.4rem, 0.8rem + 12vw, 11.5rem)"
    fontWeight: 800
    lineHeight: 0.9
    letterSpacing: "0.005em"
  display:
    fontFamily: "Big Shoulders Display Variable, Big Shoulders Display, Barlow Condensed, Arial Narrow, sans-serif"
    fontSize: "clamp(3rem, 2.2rem + 4vw, 6rem)"
    fontWeight: 800
    lineHeight: 0.92
    letterSpacing: "0.005em"
  headline:
    fontFamily: "Big Shoulders Display Variable, Big Shoulders Display, Barlow Condensed, Arial Narrow, sans-serif"
    fontSize: "clamp(2.2rem, 1.8rem + 2vw, 3.5rem)"
    fontWeight: 800
    lineHeight: 0.92
    letterSpacing: "0.005em"
  title:
    fontFamily: "Big Shoulders Display Variable, Big Shoulders Display, Barlow Condensed, Arial Narrow, sans-serif"
    fontSize: "clamp(1.6rem, 1.4rem + 1vw, 2.25rem)"
    fontWeight: 800
    lineHeight: 0.95
    letterSpacing: "0.005em"
  stamp:
    fontFamily: "Big Shoulders Display Variable, Big Shoulders Display, Barlow Condensed, Arial Narrow, sans-serif"
    fontSize: "clamp(1.15rem, 1.08rem + 0.35vw, 1.35rem)"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0.02em"
  lede:
    fontFamily: "Barlow, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1.15rem, 1.08rem + 0.35vw, 1.35rem)"
    fontWeight: 400
    lineHeight: 1.45
  body:
    fontFamily: "Barlow, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(1rem, 0.97rem + 0.2vw, 1.125rem)"
    fontWeight: 400
    lineHeight: 1.55
  label:
    fontFamily: "Big Shoulders Display Variable, Big Shoulders Display, Barlow Condensed, Arial Narrow, sans-serif"
    fontSize: "clamp(0.85rem, 0.82rem + 0.15vw, 0.95rem)"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "0.05em"
  small:
    fontFamily: "Barlow, Helvetica Neue, Arial, sans-serif"
    fontSize: "clamp(0.85rem, 0.82rem + 0.15vw, 0.95rem)"
    fontWeight: 500
    lineHeight: 1.4
rounded:
  none: "0"
spacing:
  gutter: "clamp(1rem, 0.6rem + 2vw, 2.5rem)"
  band: "clamp(2.5rem, 1.6rem + 4vw, 5rem)"
  pad: "clamp(1.4rem, 1rem + 2.4vw, 3.25rem)"
  inset: "clamp(0.75rem, 0.5rem + 1vw, 1.1rem)"
  wall-gap: "clamp(0.9rem, 0.5rem + 1.6vw, 1.75rem)"
  split-gap: "clamp(1.5rem, 1rem + 2vw, 3rem)"
  mt: "1.5rem"
  mt-lg: "1.75rem"
  max: "1360px"
components:
  placard-yellow:
    backgroundColor: "{colors.signal-yellow}"
    textColor: "{colors.wall-black}"
    rounded: "{rounded.none}"
    padding: "calc({spacing.inset} + {spacing.pad})"
  placard-black:
    backgroundColor: "{colors.wall-black}"
    textColor: "{colors.enamel-white}"
    rounded: "{rounded.none}"
    padding: "calc({spacing.inset} + {spacing.pad})"
  switch-on-black:
    backgroundColor: "{colors.signal-yellow}"
    textColor: "{colors.wall-black}"
    typography: "{typography.stamp}"
    rounded: "{rounded.none}"
    padding: "0.6em 1.5em 0.6em 2.05em"
    height: "3.1rem"
  switch-on-black-hover:
    backgroundColor: "{colors.pressed-yellow}"
    textColor: "{colors.wall-black}"
    padding: "0.6em 2.05em 0.6em 1.5em"
  switch-on-yellow:
    backgroundColor: "{colors.wall-black}"
    textColor: "{colors.signal-yellow}"
    typography: "{typography.stamp}"
    rounded: "{rounded.none}"
    padding: "0.6em 1.5em 0.6em 2.05em"
    height: "3.1rem"
  switch-on-yellow-hover:
    backgroundColor: "{colors.pressed-black}"
    textColor: "{colors.signal-yellow}"
    padding: "0.6em 2.05em 0.6em 1.5em"
  switch-ghost:
    backgroundColor: "transparent"
    typography: "{typography.stamp}"
    rounded: "{rounded.none}"
    padding: "0.6em 1.5em 0.6em 2.05em"
    height: "3.1rem"
  switch-rail:
    backgroundColor: "{colors.signal-yellow}"
    textColor: "{colors.wall-black}"
    rounded: "{rounded.none}"
    padding: "0.3em 1.5em 0.3em 1.95em"
    height: "2.2rem"
  tag:
    typography: "{typography.label}"
    rounded: "{rounded.none}"
    padding: "0.55rem 0.8rem"
  field:
    rounded: "{rounded.none}"
    padding: "0.7rem 0.8rem"
    typography: "{typography.body}"
  plate-figure:
    backgroundColor: "{colors.wall-black}"
    rounded: "{rounded.none}"
    padding: "0"
  rating-plate-cell:
    backgroundColor: "{colors.wall-black}"
    textColor: "{colors.enamel-white}"
    rounded: "{rounded.none}"
    padding: "0.85rem 1rem"
---

# Design System: Carbon Project Australia

## Overview

**Creative North Star: "Switchyard Placard"**

The site is its own safety signage. Every page is a stack of enamel placards bolted to a black wall: signal-yellow placards carry the message, black placards instruct, and white exists only as text on black. Nothing is rendered as a screen. A rule is a 2px enamel line inset from the edge, a corner is a domed rivet, a button is an isolator switch with a lever that throws. The world was chosen for a product whose whole claim is that sovereignty is a property of a building (see PRODUCT.md, Positioning); the signage is that building's, and the visitor is standing in front of an energised installation they are not allowed to touch.

Density is high but never crowded. Placards sit close to each other with a narrow wall gap between them, and inside each placard the padding is generous and fluid. Type does the work: condensed black caps at very large size on yellow, plain Barlow for everything the caps do not say. The palette is two materials plus the tints they need to keep secondary text legible. There is no chrome, no glow, no glass, and no decorative statistic.

Confirmed visual rejections: the glowing dark AI hero, the paper technical datasheet, gradients used as surfaces, glass and blur, eyebrow and kicker labels above headings, section numbers as decoration, and monospace type.

**Key Characteristics:**
- Two materials, yellow enamel and black wall; every colour role is derived from which one you are standing on.
- Big Shoulders Display 800 uppercase for every heading; Barlow 400 to 700 for everything else.
- Zero radius everywhere. Rules are 2px. Corners carry rivets.
- Placards are the only container. Layout is a wall of placards, not a page of sections.
- One signature interaction: placards land and their rivets snap in once at load; the primary switch throws its lever on hover.
- Every raster image is a bordered plate captioned "Illustrative image".

## Colors

Two materials and the minimum set of tints needed for AA legibility on each; the material you are on decides every role.

### Primary
- **Signal Yellow** (`signal-yellow`): the enamel field of every yellow placard, the header asset tag, the rating plate border, the active nav underline, scrollbar and caret, selection background on black, and the switch field on black placards. It is a surface, not an accent: it covers more than half the home page.
- **Pressed Yellow** (`pressed-yellow`): the switch field while its lever is thrown (hover, focus-visible) on a black placard. Nowhere else.

### Neutral
- **Wall Black** (`wall-black`): the page background, every black placard, the header rail, and all text and rules on yellow. Also the switch field on yellow placards.
- **Enamel White** (`enamel-white`): primary text on black only. Never a surface, never a border on yellow.
- **Galvanised Steel** (`galvanised-steel`): the inset rule and control borders on black placards, the header rail's bottom rule, the footer's top rule. 3:1 against black, which is the control-boundary floor.
- **Steel on Yellow** (`steel-on-yellow`): control borders and nameplate row dividers on yellow. Measured 3.5:1 against Signal Yellow.
- **Ink on Yellow** (`ink-on-yellow`): secondary text (ledes, `.sub`, breadcrumbs, dd values) on yellow. Measured 6.8:1.
- **Ink on Black** (`ink-on-black`): secondary text and nav links at rest on black, and the "Illustrative image" caption. Measured 10:1.
- **Pressed Black** (`pressed-black`): the switch field while thrown on a yellow placard.
- **Fault Red** (`fault-red`): the only colour outside the two materials. Border of a form field in `:user-invalid`. Approximately 3.3:1 on yellow and 3.9:1 on black, which clears the boundary floor and no more.

Primary text measures 12.8:1 (black on yellow) and 21:1 (white on black).

### Named Rules
**The Surface Decides Rule.** Components never pick a colour. They read `--bg --fg --fg2 --rule --field --act-bg --act-fg`, and the placard variant (`.pl-y` or `.pl-k`) sets all seven. On yellow: fg is black, fg2 is Ink on Yellow, rule is black, field is Steel on Yellow, the action pair is black-on-yellow inverted to yellow-on-black. On black: fg is white, fg2 is Ink on Black, rule and field are Galvanised Steel, the action pair is yellow field with black text. A new component that hard-codes a material colour is wrong unless it is a rivet, a rating plate, or the header rail.

**The White Is Text Rule.** White appears only as text and rivets on black. There is no white surface, no white border on yellow, no white placard.

**The Two Materials Rule.** Every surface is Signal Yellow or Wall Black. Tints exist only to make secondary text and borders legible on those two; they are never surfaces.

## Typography

**Display Font:** Big Shoulders Display Variable (with Big Shoulders Display, Barlow Condensed, Arial Narrow, sans-serif), self-hosted via Fontsource.
**Body Font:** Barlow 400 / 400 italic / 500 / 600 / 700 (with Helvetica Neue, Arial, sans-serif), self-hosted via Fontsource.

**Character:** Stencilled signage over engineering copy. Headings are condensed black caps set very tight (line-height 0.9 to 0.95, tracking near zero) so they read as cut letters on enamel. Body is a plain grotesque with tabular numerals where numbers align. Nothing is set in monospace. `font-synthesis-weight: none` is on, so only the loaded weights render.

### Hierarchy
The ramp is seven fluid steps, `--t-1` through `--t5`, every one a `clamp()`.

- **Placard headline** (`--t5`, 800, 0.9): the home page's single hazard headline only. Max width 11ch.
- **Display** (`--t4`, 800, 0.92): the page h1 on every secondary page (max 16ch in the page header) and the engagement-step numerals.
- **Headline** (`--t3`, 800, 0.92): placard h2s and the two large offer h3s.
- **Title** (`--t2`, 800, 0.95): h3s, the compact `.h-mid` h2 used on secondary placards, nameplate keys in the pillars list.
- **Stamp** (`--t1`, 700, 1.0, 0.02em tracking, uppercase): the display face at small size. Nameplate keys (`dt`), FAQ questions, switch labels, h4s, footer column heads.
- **Lede** (`--t1`, Barlow 400, 1.45): the paragraph under a heading, max 46ch, always in fg2.
- **Body** (`--t0`, Barlow 400, 1.55): running text. `.flow` paragraphs and list items are capped at 68ch.
- **Label** (`--t-1`, display 700, 0.05em tracking, uppercase): the `.tag` ID plate, form labels (0.06em), rating plate keys (0.08em), the header asset name (0.06em).
- **Small** (`--t-1`, Barlow 500, 1.4): captions, breadcrumbs, nav links, footer links, form help.

### Named Rules
**The Caps Are the Display Rule.** Every h1 to h4 and every `.disp` is Big Shoulders Display 800, uppercase, line-height 0.92 or tighter. There is no mixed-case heading and no Barlow heading anywhere on the site.

**The No Eyebrow Rule.** Nothing sits above a heading except the ID tag on the home fold and the breadcrumb on page headers. No kicker, no category label, no section number, except the four engagement-step numerals, which are an ordered sequence and not decoration.

## Layout

The page is a wall. The header rail is sticky at the top on black with a 2px steel rule beneath it. Below it, placards stack inside a `.wrap` (max 1360px, fluid gutter `--gutter`) with a wall gap (`wall-gap`, 0.9 to 1.75rem) between them; page-header and hero placards bleed to the viewport edge and drop their shadow. The footer is a rating plate and four link columns on black, separated from the wall by `--band` of vertical space.

Inside a placard, content is padded by `inset + pad` so text clears the inset rule by the full `--pad`. Two-column placards use `.split`, a 5fr/7fr grid (or 1fr/1fr with `.split--even`) with `split-gap`, collapsing to one column below 60rem. The offers grid on the home page is two columns from 60rem. Step and related-item lists are single column, then 2, 3 or 4 columns from 52rem with a 2px top rule.

Vertical rhythm inside placards is small and consistent: 0.75 to 1rem after a heading, 1.5rem between blocks, 1.75rem before a nameplate or button. Two global utilities, `.mt` (1.5rem) and `.mt-lg` (1.75rem), exist because Astro-scoped page styles cannot reach a child component; use them on a `Plate` handed a spacing class and nowhere else.

Responsive rules observed in the build:
- Below 62rem the nav rail drops to its own row under the asset and CTA, scrolls horizontally with no visible scrollbar, and has a 1px steel top rule. From 62rem it sits inline, right-aligned, with the CTA last.
- Below 26rem the header hides the wordmark and shows only the "CP" tag.
- `.split` is one column below 60rem. Rivets are 14px below 60rem and 20px above.
- Nameplate rows are stacked below 40rem and key/value (minmax(7rem,1fr) / 3fr) above.
- The single-line diagram is fixed at 760px minimum width and scrolls inside its own container below that; the placard does not stretch.
- The rating plate is 2 columns, 3 from 48rem, 5 from 72rem. Footer columns are 2, then 4 from 56rem.
- The enquiry form is one column below 40rem and two above, with the brief spanning both.
- The home hero is a 3-row grid; at 60rem and above the ID tag moves to the top-right and the headline spans the first two rows.

## Elevation & Depth

Depth is material, not lit. A placard sits proud of the wall by one soft shadow, `0 10px 28px -10px rgb(0 0 0 / 0.55)`, and that shadow is removed when a placard bleeds to the viewport edge because a bleed placard is the wall. Nothing else casts a shadow: not buttons, not fields, not the rail, not the plates. Rivets and inset rules do the rest of the depth work; a black placard on a black wall is visible only because its steel rule and white rivets are.

### Shadow Vocabulary
- **Placard lift** (`box-shadow: 0 10px 28px -10px rgb(0 0 0 / 0.55)`): every non-bleed placard, at rest, unchanged on hover.

### Named Rules
**The One Shadow Rule.** The placard lift is the only shadow in the system. Interactive elements signal state with colour, border and transform, never with elevation.

## Shapes

Zero radius everywhere; the only `rounded` token is `none`. Every edge is cut square. Rules are 2px (placard inset rule, nameplate top rule, switch border, tag border, plate border, field border, rating plate cells, rail bottom rule). Secondary dividers are 1px (nameplate row bottoms, FAQ item bottoms, the nav row's top rule, the footer base rule). The nav's active underline is 3px.

The placard's inset rule sits `--inset` in from every edge, and the four rivets are centred on its corners. A rivet is an SVG circle in fg with a smaller circle in bg at its centre, so it reads as a domed fixing on either material. The list marker is a short bar (0.6em by 0.28em) in fg, never a disc. The FAQ marker is a plus made of two 3px bars that collapses to a minus. The select chevron is two hard-edged 6px triangles, not a glyph. The single-line diagram is drawn in 3px strokes with 8/6 dashes for data links, squares and circles only.

## Components

### Placard
The only container. A section, article, div, li or aside carrying `.placard`, a tone class, and four rivets.
- **Corner Style:** square, rivet at each corner of the inset rule.
- **Background:** Signal Yellow (`.pl-y`, the default) or Wall Black (`.pl-k`). Alternate tones down a wall so no two adjacent placards match where possible.
- **Border:** the 2px inset rule in `--rule`, drawn as a pseudo-element `--inset` from the edge.
- **Internal Padding:** `inset + pad` on all sides. Bleed placards (`placard--bleed`) drop the shadow and are used for the hero and page headers.
- **Entrance:** `--i` is the stagger index. Only placards with `i` of 0, 1 or 2 receive `.bolt`: they fade and settle from scale 1.02 over 400ms with a 120ms per-index delay, then the four rivets snap in (scale 0 to 1.25 to 1 over 220ms) clockwise from top-left at 40ms intervals starting 400ms after the placard lands. Placards further down the page (`i` of 3 or more) render without animation.

### Buttons
The switch. An isolator lever sits at the left of a condensed-caps label; on hover or focus the field presses to its pressed shade, the whole switch slides 3px right, and the lever travels to the right end of the label over 260ms.
- **Shape:** square (0 radius), 2px border in the field colour, min-height 3.1rem, lever 0.55em wide.
- **Primary (`.sw`):** field `--act-bg`, text `--act-fg`, Stamp type at 0.03em tracking. On black: yellow field, black text, presses to Pressed Yellow. On yellow: black field, yellow text, presses to Pressed Black.
- **Hover / Focus:** transform 3px right, pressed field, padding swaps so the label makes room for the lever on the right; lever `left` animates to the far end. Active: 5px right. Focus-visible additionally shows the global 3px outline (yellow on black, black on yellow) at 3px offset.
- **Ghost (`.sw--ghost`):** transparent field, 2px border in fg, lever in fg, no press colour. Defined in the primitive layer; used once in the build.
- **Rail (`.sw--sm`):** the header CTA at min-height 2.2rem, 0.9rem type, 0.45em lever.
- **Disabled:** 50% opacity, no transform.
- **Text link (`.lk`):** Barlow 600, 2px underline in `--act-bg` (black on yellow), underline goes currentColor on hover. Used for secondary actions beside a switch.

### Nameplate (`.plate`)
Stamped key/value rows for specifications, commercial terms, contact details.
- **Style:** 2px top rule in `--rule`; each row has a 1px bottom rule in `--field`, 0.8rem vertical padding.
- **Key (`dt`):** Stamp type, fg. **Value (`dd`):** body in fg2, tabular numerals; links inside are fg with a `--act-bg` underline.

### ID Tag (`.tag`)
A small stamped label block: 2px border in fg, Label type for the first line, Barlow 500 in fg2 for the sub-lines, inline-grid with 0.15rem row gap. Used for the entity plate on the home fold, the "bought as" plate on service pages, and the 404 code.

### Plate (illustrative image)
- **Style:** `figure` with a 2px border in fg and a black background; the image fills it at the given aspect ratio (default 16/9, also 4/3, 16/10, 21/9), WebP at quality 72 in four widths.
- **Caption:** every plate carries a bottom-right "Illustrative image" chip in Ink on Black on black at 0.72rem Barlow 500. It is not optional; the product commits that no image is presented as a photograph of the facility (PRODUCT.md, Evidence on Hand). The source PNGs carry their generation prompt as tEXt metadata.

### Inputs / Fields
- **Style:** background `--bg`, text `--fg`, 2px border in `--field`, 0.7rem by 0.8rem padding, body size, no radius. Labels are Label type at 0.06em in fg; required marks in fg2.
- **Hover / Focus:** border goes to fg; focus-visible adds the global outline at 2px offset.
- **Error:** border Fault Red on `:user-invalid`. No error text colour; the field's own label stays in fg.
- **Select:** native appearance removed, chevron drawn as two hard triangles in fg.

### Navigation
- **Rail:** sticky, black, 2px steel bottom rule, min-height 3.5rem. Asset mark is a yellow "CP" tag (display 800, 0.04em) joined to a yellow-outlined wordmark (display 700, 0.06em, uppercase).
- **Links:** Small type, Barlow 500, Ink on Black at rest, white on hover, white with a 3px yellow bottom border when current. Below 62rem the list becomes a horizontally scrolling row under the asset and CTA.
- **CTA:** the rail switch, yellow on black, always visible in the top row.
- **Breadcrumb (page headers):** Small type in fg2, slash separators, above the h1.

### Rating Plate (footer)
Entity details as a grid of cells bordered 2px in Signal Yellow on black; keys are Label type at 0.08em in yellow, values Small type in white. Below it, four link columns with yellow Stamp headings and Ink on Black links, then a 1px steel base rule.

### FAQ
Native `details`: 2px top rule on the group, 1px `--field` rule under each item, Stamp-type question with a plus/minus bar marker, answer in fg2 capped at 66ch.

### List (`.list`)
Unstyled list with a short fg bar marker at 0.58em, 1.35em indent, 0.5em between items. The `.list--lg` variant sets items at Lede size for deliverables.

## Do's and Don'ts

### Do:
- **Do** put every piece of content inside a placard, and alternate yellow and black down the wall.
- **Do** read colour from the surface roles (`--bg --fg --fg2 --rule --field --act-bg --act-fg`) so a component works unchanged on either material.
- **Do** set every heading in Big Shoulders Display 800 uppercase, line-height 0.92 or tighter, and every paragraph in Barlow.
- **Do** use the switch for the primary action and a `.lk` text link for the secondary one, never two switches side by side.
- **Do** caption every raster image "Illustrative image" inside a bordered plate.
- **Do** use `.mt` / `.mt-lg` when a child component needs spacing from a scoped page style.
- **Do** keep control borders at 3:1 or better against their surface: Steel on Yellow on yellow, Galvanised Steel on black.
- **Do** respect the reduced-motion policy: under `prefers-reduced-motion: reduce` every animation and transition runs at 0.01ms with zero delay and a single iteration, so placards and rivets appear already bolted and the switch lever is simply at its thrown position on hover.

### Don't:
- **Don't** add radius to anything; the only rounded token is `none`.
- **Don't** use a gradient, blur, glass, glow, or any shadow other than the placard lift.
- **Don't** put an eyebrow, kicker, category label or section number above a heading. The engagement-step numerals are the one ordered sequence that earns numbers.
- **Don't** set anything in monospace, including specifications and code-like values; use Barlow with tabular numerals.
- **Don't** use white as a surface or as a border on yellow; white is text on black.
- **Don't** introduce a third material. Fault Red is a state border on form fields only.
- **Don't** add rivets, inset rules or the placard shadow to anything that is not a placard; rivets are structural, not ornament.
- **Don't** animate placards below the fold; `.bolt` is for `i` of 0 to 2 only, once, at load.
- **Don't** hide the header CTA on small screens or move it into the scrolling nav row.
