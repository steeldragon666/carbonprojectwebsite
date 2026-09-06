/**
 * Cloudflare Pages Function: receives the enquiry form and emails it on.
 *
 * Deploy target: Cloudflare Pages. Set PUBLIC_FORM_ENDPOINT=/api/enquiry at
 * build time and RESEND_API_KEY / ENQUIRY_TO / ENQUIRY_FROM as environment
 * variables in the Pages project. Other hosts: point PUBLIC_FORM_ENDPOINT at
 * your own handler instead and delete this file.
 */
interface Env {
  RESEND_API_KEY?: string;
  ENQUIRY_TO?: string;
  ENQUIRY_FROM?: string;
}

/** Minimal local shape of the Cloudflare Pages handler context. */
type Ctx = { request: Request; env: Env };

const FIELDS = ['name', 'email', 'organisation', 'topic', 'brief'] as const;
const LIMITS: Record<string, number> = {
  name: 120, email: 200, organisation: 200, topic: 80, brief: 6000,
};

const redirect = (url: string) => new Response(null, { status: 303, headers: { Location: url } });

export const onRequestPost = async ({ request, env }: Ctx): Promise<Response> => {
  const origin = new URL(request.url).origin;

  let form: FormData;
  try {
    form = await request.formData();
  } catch {
    return new Response('Bad request', { status: 400 });
  }

  // Honeypot: silently accept so a bot learns nothing from the response.
  if (String(form.get('_gotcha') ?? '').trim()) return redirect(`${origin}/contact/received/`);

  const values: Record<string, string> = {};
  for (const f of FIELDS) values[f] = String(form.get(f) ?? '').trim().slice(0, LIMITS[f]);

  if (!values.name || !values.brief) return new Response('Name and brief are required', { status: 400 });
  if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(values.email)) {
    return new Response('A valid email address is required', { status: 400 });
  }

  if (!env.RESEND_API_KEY || !env.ENQUIRY_TO || !env.ENQUIRY_FROM) {
    return new Response('Enquiry handling is not configured on this deployment.', { status: 501 });
  }

  const body = FIELDS.map((f) => `${f}: ${values[f] || '—'}`).join('\n');

  const sent = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      from: env.ENQUIRY_FROM,
      to: [env.ENQUIRY_TO],
      reply_to: values.email,
      subject: `Website enquiry${values.topic ? ` — ${values.topic}` : ''}`,
      text: `${body}\n\nReceived ${new Date().toISOString()} via carbonproject.ai`,
    }),
  });

  if (!sent.ok) return new Response('Could not send the enquiry. Please email us directly.', { status: 502 });
  return redirect(`${origin}/contact/received/`);
};
