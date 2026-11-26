// DEEP Asistan — yapay zekâ modu için Cloudflare Worker.
// API anahtarı yalnızca Cloudflare'de gizli değişken olarak tutulur:  npx wrangler secret put ANTHROPIC_API_KEY
// Siteye bağlamak için GitHub > Settings > Secrets and variables > Actions > Variables:  CHAT_ENDPOINT = https://<worker-adresi>
import { KNOWLEDGE } from "./knowledge.js";

const ALLOWED = [
  "https://abdullahyilmz1722-pixel.github.io",
  // alan adınızı aldığınızda ekleyin, örn. "https://www.deepreklam.com"
];
const MAX_MSG = 500, MAX_TURNS = 10, RATE = 20; // RATE: IP başına dakikada en fazla istek (sunucu örneği başına, en iyi çaba)
const hits = new Map();

const SYSTEM = (lang) => `You are "DEEP Asistan", the website assistant of DEEP REKLAM, a Turkey-based advertising and technology company whose main focus is AI automation (WhatsApp AI assistants, AI sales agents, AI customer service and booking, AI voice assistants, multi-agent systems, n8n/Make workflow automation), plus signage and outdoor advertising, graphic design, web design, custom software, digital marketing, SEO/GEO, social media, and print/promotional products.

Reply in ${lang === "en" ? "English" : "Turkish"} unless the visitor writes in another language, then use theirs. Be warm, short (2–5 sentences) and helpful. Guide visitors to the right service and invite them to continue on WhatsApp or phone: +90 533 316 32 70.

Strict rules:
- Use ONLY the company information below. If something is not covered (opening hours, address details, delivery times, specific past clients), say the team will confirm and suggest WhatsApp.
- Never give prices, price ranges or discounts: pricing is prepared per project.
- Never invent clients, statistics, reviews, certificates, guarantees or results. Never promise search rankings.
- Never claim you booked, saved, sent or recorded anything. You cannot take actions; the visitor contacts the team via WhatsApp or the quote form.
- Do not ask for or store personal data. If the visitor shares sensitive data, tell them not to share it here.
- For general questions loosely related to the visitor's business (e.g. "how can AI help my restaurant?"), answer briefly and relate it to DEEP REKLAM's services. Politely decline unrelated or harmful requests.
- You are an AI assistant; say so if asked.

COMPANY INFORMATION:
${KNOWLEDGE}`;

function cors(origin) {
  const ok = ALLOWED.includes(origin);
  return { "Access-Control-Allow-Origin": ok ? origin : ALLOWED[0], "Access-Control-Allow-Methods": "POST, OPTIONS",
           "Access-Control-Allow-Headers": "Content-Type", "Vary": "Origin" };
}
const json = (obj, status, origin) => new Response(JSON.stringify(obj), { status, headers: { "Content-Type": "application/json", ...cors(origin) } });

export default {
  async fetch(req, env) {
    const origin = req.headers.get("Origin") || "";
    if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors(origin) });
    if (req.method !== "POST") return json({ error: "method" }, 405, origin);
    if (!ALLOWED.includes(origin)) return json({ error: "origin" }, 403, origin);
    if (!env.ANTHROPIC_API_KEY) return json({ error: "not_configured" }, 503, origin);

    const ip = req.headers.get("CF-Connecting-IP") || "?", now = Date.now();
    const h = (hits.get(ip) || []).filter(t => now - t < 60000); h.push(now); hits.set(ip, h);
    if (h.length > RATE) return json({ error: "rate" }, 429, origin);

    let body; try { body = await req.json(); } catch { return json({ error: "bad_json" }, 400, origin); }
    const lang = body.lang === "en" ? "en" : "tr";
    const msgs = (Array.isArray(body.messages) ? body.messages : []).slice(-MAX_TURNS)
      .filter(m => m && (m.role === "user" || m.role === "assistant") && typeof m.content === "string")
      .map(m => ({ role: m.role, content: m.content.slice(0, MAX_MSG) }));
    while (msgs.length && msgs[0].role !== "user") msgs.shift();
    if (!msgs.length || msgs[msgs.length - 1].role !== "user") return json({ error: "no_message" }, 400, origin);

    const r = await fetch("https://api.anthropic.com/v1/messages", {
      method: "POST",
      headers: { "content-type": "application/json", "x-api-key": env.ANTHROPIC_API_KEY, "anthropic-version": "2023-06-01" },
      body: JSON.stringify({ model: env.MODEL || "claude-haiku-5-5", max_tokens: 400, system: SYSTEM(lang), messages: msgs }),
    });
    if (!r.ok) return json({ error: "upstream", status: r.status }, 502, origin);
    const data = await r.json();
    const reply = (data.content || []).filter(c => c.type === "text").map(c => c.text).join("\n").trim();
    return json({ reply }, 200, origin);
  },
};
