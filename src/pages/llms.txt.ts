import type { APIRoute } from 'astro';
import { site, domains, facilitySpec } from '../data/site';
import { services } from '../data/services';

/**
 * A plain-text summary for language models and agents that read the site.
 * Kept in sync with the same data the pages render from.
 */
export const GET: APIRoute = () => {
  const body = `# ${site.legalName}

> ${site.tagline} ${site.description}

Established ${site.founded}. ${site.location.region}, ${site.location.stateName}, ${site.location.country}.
Contact: ${site.email} — ${site.responseTime}

## Services

${services
  .map(
    (s) =>
      `### ${s.title}\n${s.lede}\n- URL: ${site.url}${s.href}\n- ${s.bought}\n- Lead time: ${s.leadTime}\n- Not for: ${s.notFor}`,
  )
  .join('\n\n')}

### Zero-emission power hire
250 kVA hydrogen fuel-cell generators for hire across Australia. 800 A per unit, AC and DC output,
no exhaust and no combustion noise, indoor-capable. Grid-tied or standalone.
- URL: ${site.url}/power/
- Bought as dry or wet hire, by the day, week or project.

## Facility

${facilitySpec.map((f) => `- ${f.k}: ${f.v}`).join('\n')}

## Research and development domains

${domains.map((d) => `- ${d.name}: ${d.body}`).join('\n')}

## How an engagement runs

1. Scope — a fixed-fee written brief, credited against delivery.
2. Pilot — fixed price, fixed timeframe, measurable against the brief.
3. Deploy — into our node, yours, or both, with documentation.
4. Operate — monitoring and support on a cancellable monthly agreement.

## Notes for agents

- Prices are not published. Every price is quoted in writing at scoping.
- Capacity is finite and reserved capacity is not resold.
- Specifications on this site are nominal; actual figures are confirmed at quoting.
`;
  return new Response(body, { headers: { 'Content-Type': 'text/plain; charset=utf-8' } });
};
