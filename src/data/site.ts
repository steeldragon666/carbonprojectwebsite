/**
 * Single source of truth for company facts, navigation and commercial offers.
 * Anything a non-developer might need to change should live here.
 *
 * NOTE ON CLAIMS: every substantive factual claim in this file is listed in
 * CLAIMS-REGISTER.md with its provenance. Do not add a new number here without
 * adding it there — see docs/CLAIMS-REGISTER.md.
 */

export const site = {
  name: 'Carbon Project Australia',
  legalName: 'Carbon Project Australia Pty Ltd',
  shortName: 'Carbon Project',
  url: 'https://carbonproject.ai',
  tagline: 'Sovereign AI inference, powered on site.',
  description:
    'Sovereign AI inference, fine-tuning and robotics, run on hardware we own at a self-powered facility in Victoria. Your data stays on Australian soil.',
  founded: '2019',
  email: 'aaron@carbonproject.com.au',
  location: {
    region: 'Mornington Peninsula',
    state: 'VIC',
    stateName: 'Victoria',
    country: 'Australia',
    countryCode: 'AU',
    note: 'Visits by appointment — about an hour from Melbourne.',
  },
  responseTime: 'We reply within one business day.',
  /** Where the enquiry form posts. Set PUBLIC_FORM_ENDPOINT at build time. */
  formEndpoint: import.meta.env.PUBLIC_FORM_ENDPOINT ?? '',
  /** Drawing-sheet revision block shown in the footer. */
  revision: 'C',
} as const;

export const nav = [
  { label: 'Services', href: '/services/' },
  { label: 'Power', href: '/power/' },
  { label: 'Facility', href: '/facility/' },
  { label: 'Research', href: '/research/' },
  { label: 'How we work', href: '/how-we-work/' },
] as const;

export const cta = {
  label: 'Book a scoping call',
  href: '/contact/',
} as const;

export type Offer = {
  slug: string;
  href: string;
  no: string;
  title: string;
  /** One line a buyer can repeat to their own boss. */
  summary: string;
  /** How it is bought. Shown in the commercial strip. */
  bought: string;
  /** What you get, in deliverable terms. */
  deliverables: string[];
  /** What it is not, so nobody buys the wrong thing. */
  notFor: string;
  linkLabel: string;
  leadTime: string;
};

export const offers: Offer[] = [
  {
    slug: 'sovereign-inference',
    href: '/services/sovereign-inference/',
    no: '01',
    title: 'Sovereign inference',
    summary:
      'Dedicated, on-shore inference for open-weight models — yours or ours — served from our node in Victoria.',
    bought: 'Bought as monthly reserved capacity, or per project',
    deliverables: [
      'Reserved GPU capacity on hardware nobody else shares',
      'OpenAI-compatible endpoint over an encrypted link',
      'Models quantised and tuned to your latency and cost targets',
      'Monitoring, logs and evaluations you can audit',
      'Written data-handling terms naming where every byte sits',
    ],
    notFor:
      'Not a reseller of a hyperscaler API. If you want someone else’s cloud with our invoice on it, we are the wrong supplier.',
    linkLabel: 'Ask about capacity',
    leadTime: 'Capacity is finite. Current lead time is quoted at scoping.',
  },
  {
    slug: 'fine-tuning',
    href: '/services/fine-tuning/',
    no: '02',
    title: 'Fine-tuning, modification and testing',
    summary:
      'We adapt models to your domain and prove they work before they go anywhere near production.',
    bought: 'Bought as a fixed-scope project',
    deliverables: [
      'LoRA and full fine-tunes on licence-checked training data',
      'Quantisation and architecture changes for your target hardware',
      'Red-teaming, evaluation suites and regression tests',
      'Hand-over with weights, data lineage and a test report',
      'A go / no-go recommendation in writing, including “do not ship”',
    ],
    notFor:
      'Not a data-labelling shop. If the problem is that you have no data, say so at scoping and we will tell you honestly.',
    linkLabel: 'Scope a fine-tune',
    leadTime: 'Typically four to twelve weeks, fixed at scoping.',
  },
  {
    slug: 'ai-robotics-consulting',
    href: '/services/ai-robotics-consulting/',
    no: '03',
    title: 'AI and robotics consulting',
    summary:
      'Agent architecture, privilege separation and physical automation — from a design review to a working cell.',
    bought: 'Bought as retained advisory or scoped delivery',
    deliverables: [
      'Architecture and threat review of an agent or automation system',
      'Privilege separation, tool sandboxing and audit design',
      'Robot cell design, integration and commissioning',
      'Machine-vision and pick-and-place development',
      'A build plan your own engineers can execute without us',
    ],
    notFor:
      'Not a staff-augmentation contract. We take responsibility for an outcome, not a seat.',
    linkLabel: 'Talk to an engineer',
    leadTime: 'Retainers start monthly. Delivery work is scheduled at scoping.',
  },
  {
    slug: 'facility-upgrade',
    href: '/services/facility-upgrade/',
    no: '04',
    title: 'Facility upgrading and future-proofing',
    summary:
      'We audit manufacturing and process sites and stage the works: on-site compute, automation and energy independence.',
    bought: 'Bought as a site audit, then staged works',
    deliverables: [
      'Site audit covering power, network, automation and compute readiness',
      'Staged works programme with costs and sequencing',
      'On-site compute and network build',
      'Energy independence design — generation, storage and backup',
      'Documentation an auditor or an insurer will accept',
    ],
    notFor:
      'Not a generic ESG report. Every recommendation is something we can build, or tell you who can.',
    linkLabel: 'Request a site audit',
    leadTime: 'Audit typically two to four weeks from site access.',
  },
];

export type Domain = {
  name: string;
  body: string;
  badge?: string;
};

export const domains: Domain[] = [
  {
    name: 'Environmental',
    body: 'Autonomous restoration platforms and soil-carbon measurement, built on six years in soil-carbon trading and measurement technology.',
  },
  {
    name: 'Defence',
    body: 'Hybrid-energy autonomous resupply vehicles and counter-UAS sensing for the Australian environment.',
    badge: 'Registered defence contractor',
  },
  {
    name: 'Energy',
    body: 'Hydrogen fuel-cell power, biofuel feedstocks and advanced carbon materials with our partner companies.',
  },
  {
    name: 'Agriculture',
    body: 'High-yield biomass feedstock systems and robotic cultivation for planting at scale.',
  },
  {
    name: 'E-commerce',
    body: 'Agentic storefront operations, sovereign content generation and margin modelling, tested on brands we run ourselves.',
  },
];

export const facilitySpec = [
  {
    k: 'Compute',
    v: 'Dedicated GPU infrastructure for training and inference, with edge hardware for inference in the field.',
  },
  {
    k: 'Power',
    v: 'On-site renewable generation, energy storage and zero-emission backup for uninterrupted operation.',
  },
  {
    k: 'Robotics',
    v: 'Collaborative robotics and machine vision for machining, shaping and handling.',
  },
  {
    k: 'Fabrication',
    v: 'Additive and conventional fabrication, from prototype through to production.',
  },
  {
    k: 'Network',
    v: 'Private, hardened network with encrypted client links and controlled egress.',
  },
  {
    k: 'Site',
    v: 'A dedicated research and fabrication facility on the Mornington Peninsula, about an hour from Melbourne.',
  },
] as const;

export const engagementSteps = [
  {
    n: '1',
    title: 'Scope',
    body: 'A short call and a written brief that says what we will do and what it costs. Fixed fee, credited against delivery if you proceed.',
  },
  {
    n: '2',
    title: 'Pilot',
    body: 'Fixed price, fixed timeframe, and a result you can measure against the brief. You see a number before you commit to anything ongoing.',
  },
  {
    n: '3',
    title: 'Deploy',
    body: 'Into our node, into yours, or both — with the documentation to run it and the training to run it without us.',
  },
  {
    n: '4',
    title: 'Operate',
    body: 'Monitoring, retraining and support on a monthly agreement. Cancellable. Optional.',
  },
] as const;

export const pillars = [
  {
    title: 'Owned and operated',
    body: 'Every system on this sheet is owned and operated by Carbon Project Australia, on our own site in Victoria. No sub-let racks, no third-party control plane.',
  },
  {
    title: 'Sovereign by design',
    body: 'Requests arrive over an encrypted link and are answered on infrastructure we own, on Australian soil, under Australian law.',
  },
  {
    title: 'Self-powered',
    body: 'On-site renewable generation, storage and zero-emission backup keep our compute running, whatever the grid is doing.',
  },
] as const;

/** Enquiry-form subject options. Keep aligned with offers + power. */
export const enquiryTopics = [
  'Sovereign inference capacity',
  'Fine-tuning or model testing',
  'AI and robotics consulting',
  'Facility audit and upgrade',
  'Zero-emission power hire',
  'Research or partnership',
  'Something else',
] as const;
