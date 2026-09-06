import { offers, type Offer } from './site';

export type ServiceDetail = Offer & {
  metaTitle: string;
  metaDescription: string;
  lede: string;
  /** Long-form body, as ordered blocks. */
  sections: { heading: string; body?: string; list?: string[] }[];
  /** Commercial structure — how the money actually works. */
  commercial: { k: string; v: string }[];
  /** What we need from the client before we can start. */
  inputs: string[];
  faq: { q: string; a: string }[];
};

const detail: Record<string, Omit<ServiceDetail, keyof Offer>> = {
  'sovereign-inference': {
    metaTitle: 'Sovereign AI inference in Australia',
    metaDescription:
      'Dedicated on-shore AI inference on hardware we own in Victoria. Reserved GPU capacity, an OpenAI-compatible endpoint, and written data-handling terms.',
    lede:
      'Dedicated, on-shore inference for open-weight models — yours or ours — served from hardware we own and operate in Victoria. No shared tenancy, no foreign control plane, no quiet reroute to a cheaper region.',
    sections: [
      {
        heading: 'The problem this solves',
        body:
          'Most “Australian” AI is an Australian invoice in front of someone else’s infrastructure. The model weights, the control plane and often the inference itself sit offshore, under a jurisdiction you did not choose and cannot see into. For a defence supplier, a health provider, a law firm or a government contractor, that is not a procurement detail — it is the whole question.',
      },
      {
        heading: 'What we actually run',
        body:
          'Open-weight models on dedicated GPUs at our own facility. We quantise and tune each deployment to your latency and cost targets rather than handing you a generic endpoint, and we publish the evaluation results so you can see what the tuning cost you in quality.',
        list: [
          'Reserved GPU capacity on hardware nobody else shares',
          'An OpenAI-compatible endpoint, so most existing code changes one base URL',
          'Models quantised and tuned to your latency, throughput and cost targets',
          'Request logging and evaluation dashboards you can audit, or switch off entirely',
          'Controlled egress — the node can be configured so nothing leaves except your responses',
        ],
      },
      {
        heading: 'What you get in writing',
        body:
          'Before capacity is allocated you receive a data-handling schedule that names the physical site, the retention period, who at Carbon Project can access the node, and what happens to your data when the agreement ends. If a clause in it is a problem for your risk team, tell us at scoping and we will fix the clause or tell you we cannot.',
      },
    ],
    commercial: [
      { k: 'Entry step', v: 'A fixed-fee scoping engagement: workload profiling, a model recommendation and a capacity sizing. Credited in full against the first month if you proceed.' },
      { k: 'How it is bought', v: 'Monthly reserved capacity, or a fixed price per project for a bounded workload.' },
      { k: 'What is fixed', v: 'The capacity, the model, the endpoint terms and the price — all before you sign.' },
      { k: 'Term', v: 'Month to month once live. No auto-escalating tiers, no overage surprises.' },
      { k: 'Exit', v: 'Weights and configuration hand back on request. Data destruction certified in writing.' },
    ],
    inputs: [
      'A representative sample of the prompts or documents the workload will see',
      'Your latency and throughput targets, and what happens commercially if they are missed',
      'Any jurisdiction, clearance or accreditation constraints your buyer imposes on you',
      'The name of whoever has to sign off the risk assessment, so we write for them',
    ],
    faq: [
      {
        q: 'Which models can you run?',
        a: 'Open-weight models we can license and host lawfully, plus any model you hold rights to. We will tell you plainly if a model you have named cannot be self-hosted, rather than quietly substituting another.',
      },
      {
        q: 'Is my data used for training?',
        a: 'No. Your prompts and responses are not used to train anything, ours or anyone else’s, and the agreement says so in those words.',
      },
      {
        q: 'What happens if you run out of capacity?',
        a: 'Reserved means reserved — your capacity is not resold when demand spikes. If we cannot serve a new client without touching an existing reservation, we do not take the new client.',
      },
      {
        q: 'Can we run it in our own building instead?',
        a: 'Yes. That is a facility engagement rather than an inference one — see facility upgrading and future-proofing.',
      },
    ],
  },

  'fine-tuning': {
    metaTitle: 'AI model fine-tuning and testing',
    metaDescription:
      'Fixed-scope LoRA and full fine-tunes, quantisation, red-teaming and evaluation suites — with a written test report and a go / no-go recommendation.',
    lede:
      'We adapt models to your domain and prove they work before they go anywhere near production — including telling you when the honest answer is that they do not.',
    sections: [
      {
        heading: 'The problem this solves',
        body:
          'A demo that impresses a board is not evidence. Most model projects fail at the point where someone asks how the thing behaves on the ugly ten percent of real inputs, and nobody has measured it. We build the measurement first, then the model, so the decision to ship is made against numbers.',
      },
      {
        heading: 'What the work involves',
        list: [
          'LoRA and full fine-tunes on training data we have checked for licence and provenance',
          'Quantisation and architecture changes so the result fits your target hardware, including edge',
          'A held-out evaluation suite built from your real inputs, not a public benchmark',
          'Red-teaming against the failure modes that would actually cost you money or a licence',
          'Regression tests you keep, so the next version can be compared to this one',
        ],
      },
      {
        heading: 'What you receive',
        body:
          'Weights, training configuration, a data-lineage record, the evaluation suite, and a written test report with a go / no-go recommendation. The report is written to be readable by the person who has to carry the risk, not only by an ML engineer.',
      },
    ],
    commercial: [
      { k: 'Entry step', v: 'A fixed-fee scoping engagement: feasibility, data review and an evaluation plan. Credited against delivery if you proceed.' },
      { k: 'How it is bought', v: 'A fixed-scope, fixed-price project with named deliverables and a fixed end date.' },
      { k: 'What is fixed', v: 'Scope, price, deliverables and the acceptance criteria — agreed in writing before we start.' },
      { k: 'Typical duration', v: 'Four to twelve weeks, set at scoping.' },
      { k: 'Ownership', v: 'You own the resulting weights and the evaluation suite. We keep no exclusive rights over your domain data.' },
    ],
    inputs: [
      'The data you want the model to learn from, and the right to use it for that purpose',
      'Examples of the outputs you would accept and the outputs you would not',
      'The hardware the result must run on, if it is not ours',
      'An internal owner who can answer domain questions inside a day',
    ],
    faq: [
      {
        q: 'What if fine-tuning is not the right answer?',
        a: 'We say so at scoping and refund or re-point the engagement. Retrieval, a better prompt, or a different base model is often cheaper and more robust, and we would rather tell you that than bill you for a fine-tune you did not need.',
      },
      {
        q: 'Do you need our data to leave our premises?',
        a: 'Not necessarily. Training can run on our node with a controlled ingest, or on hardware inside your building. The choice is part of scoping and is priced accordingly.',
      },
      {
        q: 'Who owns the trained model?',
        a: 'You do, subject to the licence of whatever base model was used. The base-model licence is checked at scoping and named in the report.',
      },
    ],
  },

  'ai-robotics-consulting': {
    metaTitle: 'AI and robotics consulting',
    metaDescription:
      'Agent architecture, privilege separation and physical automation — from a threat review through to a commissioned robot cell, in Australia.',
    lede:
      'Agent architecture, privilege separation and physical automation — from a design review through to a working cell. We have built and wired both.',
    sections: [
      {
        heading: 'The problem this solves',
        body:
          'Agentic systems fail in two ways: they are given more privilege than the task needs, or they are given a tool with no audit trail. Robot cells fail the same way in metal. The fix in both cases is architectural, and it is much cheaper before the thing is built.',
      },
      {
        heading: 'Software side',
        list: [
          'Architecture and threat review of an agent, automation or tool-use system',
          'Privilege separation, tool sandboxing, and human-in-the-loop design that people will actually use',
          'Audit and evaluation design — what gets logged, who reads it, and what triggers a stop',
          'Cost and latency modelling before you commit to an architecture',
        ],
      },
      {
        heading: 'Hardware side',
        list: [
          'Robot cell design, integration and commissioning',
          'Machine-vision, pick-and-place and material-handling development',
          'Safety and guarding review against the relevant Australian standards, with the gaps written down',
          'A build plan detailed enough that your own engineers can execute it without us',
        ],
      },
    ],
    commercial: [
      { k: 'Entry step', v: 'A fixed-fee review: two to three weeks, ending in a written findings document and a prioritised remediation plan.' },
      { k: 'How it is bought', v: 'A monthly retainer for ongoing advisory, or a scoped delivery project with named outcomes.' },
      { k: 'What is fixed', v: 'For delivery work: scope, price and acceptance. For retainers: the monthly fee and the notice period.' },
      { k: 'Term', v: 'Retainers are monthly and cancellable. We do not lock in an annual minimum.' },
      { k: 'What we will not do', v: 'Bill a seat. We take responsibility for an outcome or we decline the work.' },
    ],
    inputs: [
      'Access to the system, the cell, or the drawings — whichever exists',
      'The failure you are worried about, described in your own words',
      'Whoever currently operates or maintains the thing, for an hour',
      'Any incident history, including the ones nobody wrote up',
    ],
    faq: [
      {
        q: 'Will you work alongside our existing integrator?',
        a: 'Yes, and we will put our findings in writing so there is no ambiguity about who said what. We will not quietly rebid work an incumbent is already delivering.',
      },
      {
        q: 'Can you just review, without building anything?',
        a: 'Yes — the fixed-fee review stands on its own, and plenty of them end there. That is the correct outcome when the answer is that the design is sound.',
      },
    ],
  },

  'facility-upgrade': {
    metaTitle: 'Facility upgrades and future-proofing',
    metaDescription:
      'Site audits and staged works for Australian manufacturing and process sites: on-site compute, automation, hardened networks and energy independence.',
    lede:
      'We audit manufacturing and process sites and stage the works: on-site compute, automation, network and energy independence. We did our own site first.',
    sections: [
      {
        heading: 'The problem this solves',
        body:
          'Sites that want to adopt automation or on-premises AI usually discover the constraint is not the software. It is a switchboard at capacity, a network that cannot be segmented, a roof that cannot take the plant, or a supply that drops out twice a summer. An audit finds those before a vendor sells you something that cannot be installed.',
      },
      {
        heading: 'What the audit covers',
        list: [
          'Electrical capacity, distribution and the realistic ceiling on new load',
          'Network topology, segmentation and what would happen in a compromise',
          'Automation readiness — what can be automated now, what needs to change first',
          'Compute siting: thermal, physical security, and where the racks can actually go',
          'Energy independence: generation, storage and zero-emission backup options',
        ],
      },
      {
        heading: 'Then the works',
        body:
          'The audit produces a staged programme with costs and sequencing, so the works can be funded in tranches rather than as one unfinanceable number. We can deliver the stages, or hand the programme to your existing contractors — the document is written to be tendered.',
      },
    ],
    commercial: [
      { k: 'Entry step', v: 'A fixed-fee site audit. Two to four weeks from site access, ending in a staged works programme with costs.' },
      { k: 'How it is bought', v: 'Audit first, then works by stage. Each stage is separately priced and separately approved.' },
      { k: 'What is fixed', v: 'The audit fee and scope. Each works stage is fixed before it starts.' },
      { k: 'Independence', v: 'The audit is useful even if you never engage us for the works, and it is written to be tendered to anyone.' },
      { k: 'Documentation', v: 'Written to a standard an auditor, an insurer or a grant assessor will accept.' },
    ],
    inputs: [
      'Site access and a walk-through with whoever maintains the plant',
      'Existing single-line diagrams and network documentation, however out of date',
      'Your load growth expectation over the next three to five years',
      'Any grant, insurance or compliance deadline the works have to meet',
    ],
    faq: [
      {
        q: 'Do we have to use you for the works?',
        a: 'No. The audit is a standalone deliverable and is deliberately written so it can be tendered to any contractor. We would rather be judged on the works we win on merit.',
      },
      {
        q: 'Can the audit support a grant application?',
        a: 'Yes. The output is structured as evidence — costed, staged and referenced — which is the form most Australian funding programmes ask for.',
      },
      {
        q: 'How far will you travel?',
        a: 'Anywhere in Australia. Travel is quoted separately and shown as a line item, not buried in the fee.',
      },
    ],
  },
};

export const services: ServiceDetail[] = offers.map((o) => ({
  ...o,
  ...detail[o.slug]!,
}));

export const serviceBySlug = (slug: string) => services.find((s) => s.slug === slug);
