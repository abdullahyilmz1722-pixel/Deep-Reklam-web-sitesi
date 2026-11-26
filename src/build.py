# -*- coding: utf-8 -*-
"""DEEP REKLAM statik site üreticisi.  Kullanım:  python3 src/build.py  ->  _site/
Ortam değişkenleri: SITE_URL (kanonik adres), FORM_ENDPOINT (isteğe bağlı form POST adresi)."""
import os, json, shutil, html, re
from content import SITE, UI, P, POSTS, AI_KEYS, SRV_KEYS
import chatbot

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(ROOT), "_site")
SITE_URL = os.environ.get("SITE_URL", "https://abdullahyilmz1722-pixel.github.io/Deep-Reklam-web-sitesi").rstrip("/")
FORM_ENDPOINT = os.environ.get("FORM_ENDPOINT", "")
CHAT_ENDPOINT = os.environ.get("CHAT_ENDPOINT", "")
import hashlib
def _ver():  # varlık dosyaları ve içerik değişince sürüm otomatik değişir (tarayıcı önbelleğini kırar)
    h = hashlib.sha1()
    for d in ("assets",):
        for f in sorted(os.listdir(os.path.join(ROOT, d))): h.update(open(os.path.join(ROOT, d, f), "rb").read())
    for f in ("content.py", "chatbot.py"): h.update(open(os.path.join(ROOT, f), "rb").read())
    return h.hexdigest()[:8]
VER = _ver()
LANGS = ["tr", "en"]
e = lambda s: html.escape(str(s), quote=True)

for p in POSTS:
    P[p["key"]] = dict(p, kind="post")
_CHAT_PRIV = {
 "tr": ("Sohbet asistanı", ["Sitedeki sohbet asistanı yazdıklarınızı yapay zekâ yanıtı üretmek için sunucumuz üzerinden yapay zekâ hizmet sağlayıcısına (Anthropic) iletir. Sohbetler tarafımızca kaydedilmez. Lütfen asistana kişisel veya hassas bilgi yazmayın."] if CHAT_ENDPOINT else
        ["Sitedeki sohbet asistanı tamamen tarayıcınızda çalışır; yazdıklarınız (adınız dahil) bize veya üçüncü kişilere gönderilmez, yalnızca sekme açık kaldığı sürece tarayıcınızda tutulur. Ekibe ulaşmak için WhatsApp butonunu kullandığınızda mesajınız WhatsApp üzerinden iletilir."]),
 "en": ("Chat assistant", ["The chat assistant on this site sends what you type through our server to an AI service provider (Anthropic) to generate replies. We don't store conversations. Please don't share personal or sensitive details with the assistant."] if CHAT_ENDPOINT else
        ["The chat assistant on this site runs entirely in your browser; what you type (including your name) is not sent to us or any third party and is kept in your browser only while the tab stays open. When you use the WhatsApp button to reach our team, your message is sent via WhatsApp."])}
for _l in ("tr", "en"):
    P["privacy"][_l]["body"].insert(3, _CHAT_PRIV[_l])
NAVDEF = {"ai": ("AI Otomasyon", "AI Automation"), "about": ("Hakkımızda", "About"), "projects": ("Projeler", "Projects"),
          "blog": ("Blog", "Blog"), "faqpage": ("SSS", "FAQ"), "contact": ("İletişim", "Contact"),
          "privacy": ("Gizlilik Politikası", "Privacy Policy"), "kvkk": ("KVKK Aydınlatma Metni", "Data Protection Notice"), "cookies": ("Çerez Politikası", "Cookie Policy")}
for k, (a, b_) in NAVDEF.items():
    P[k]["tr"].setdefault("nav", a); P[k]["en"].setdefault("nav", b_)

# ------------------------------------------------------------ yollar
def path(key, lang):
    s = P[key]["slug"][lang]
    base = "" if lang == "tr" else "en/"
    return base + ("" if s == "index" else s + ".html")

def link(key, lang, cur):
    p = path(key, lang); pre = "../" if cur == "en" else ""
    if p in ("", "en/"): p += "index.html"
    return pre + p

def absu(key, lang):
    p = path(key, lang)
    return SITE_URL + "/" + p

def T(key, lang): return P[key][lang]

# ------------------------------------------------------------ ikonlar
IC = {
 "chat": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
 "target": '<circle cx="12" cy="12" r="8"/><circle cx="12" cy="12" r="4"/><path d="M12 2v4M22 12h-4"/>',
 "calendar": '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4M8 14h3"/>',
 "wave": '<path d="M3 12h2M7 8v8M11 5v14M15 9v6M19 7v10M21 12h0"/>',
 "nodes": '<circle cx="5" cy="6" r="2.5"/><circle cx="19" cy="6" r="2.5"/><circle cx="12" cy="18" r="2.5"/><path d="M7 7l3.5 9M17 7l-3.5 9M7.5 6h9"/>',
 "flow": '<rect x="2" y="9" width="5" height="6" rx="1"/><rect x="17" y="3" width="5" height="6" rx="1"/><rect x="17" y="15" width="5" height="6" rx="1"/><path d="M7 12h5v-6h5M12 12v6h5"/>',
 "sign": '<rect x="3" y="4" width="18" height="9" rx="1"/><path d="M8 13v7M16 13v7M6 8h12"/>',
 "pen": '<path d="M4 20l4-1 11-11-3-3L5 16z"/><path d="M14 7l3 3"/>',
 "browser": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M7 6.5h.01M10 6.5h.01"/>',
 "code": '<path d="M8 8l-4 4 4 4M16 8l4 4-4 4M13.5 6l-3 12"/>',
 "chart": '<path d="M4 20V4M4 20h16"/><path d="M8 16l4-5 3 3 5-6"/>',
 "search": '<circle cx="11" cy="11" r="6"/><path d="M20 20l-4.5-4.5"/>',
 "spark": '<path d="M12 3v5M12 16v5M3 12h5M16 12h5M6 6l3 3M15 15l3 3M18 6l-3 3M9 15l-3 3"/>',
 "print": '<path d="M7 9V3h10v6"/><rect x="3" y="9" width="18" height="8" rx="1"/><path d="M7 14h10v7H7z"/>',
 "phone": '<path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/>',
 "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
 "check": '<path d="M5 12l4 4 10-10"/>',
 "map": '<path d="M12 21s-7-6.2-7-11a7 7 0 0 1 14 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
 "core": '<circle cx="12" cy="12" r="3"/><circle cx="12" cy="12" r="8"/><path d="M12 1v3M12 20v3M1 12h3M20 12h3"/>',
}
WA_SVG = '<svg viewBox="0 0 24 24" aria-hidden="true" class="ic" fill="currentColor" stroke="none"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2c-1.5 0-3-.4-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.3-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5c-.2 0-.4.1-.7.3-.2.3-.9.9-.9 2.2s.9 2.5 1 2.7c.1.2 1.8 2.8 4.4 3.9 1.6.7 2.3.8 3.1.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3z"/></svg>'
def ic(n, cls="ic"): return f'<svg viewBox="0 0 24 24" aria-hidden="true" class="{cls}">{IC[n]}</svg>'

# ------------------------------------------------------------ parçalar
def wa_link(lang, text=None):
    t = text or UI[lang]["f_wa_head"]
    from urllib.parse import quote
    return f"https://wa.me/{SITE['wa']}?text={quote(t)}"

def nav_html(lang, cur_key):
    u = UI[lang]; L = lambda k: link(k, lang, lang)
    ai_items = "".join(f'<li><a href="{L(k)}">{ic(P[k]["icon"])}<span>{e(T(k,lang)["nav"])}</span></a></li>' for k in AI_KEYS)
    srv_items = "".join(f'<li><a href="{L(k)}">{ic(P[k]["icon"])}<span>{e(T(k,lang)["nav"])}</span></a></li>' for k in SRV_KEYS)
    other = "en" if lang == "tr" else "tr"
    alt = link(cur_key, other, lang)
    return f'''<header class="hd" id="top"><div class="hd-in">
<a class="brand" href="{L('home')}" aria-label="DEEP REKLAM — {e(u['home'])}"><img src="{'../' if lang=='en' else ''}assets/logo.png" alt="DEEP REKLAM" width="82" height="62"></a>
<button class="burger" aria-expanded="false" aria-controls="nav"><span></span><span></span><span class="sr">{e(u['menu'])}</span></button>
<nav id="nav" aria-label="{e(u['menu'])}"><ul class="nl">
<li class="has"><a href="{L('ai')}" class="nk">{e(u['nav_ai'])}</a><button class="dd-t" aria-label="{e(u['nav_ai'])}" aria-expanded="false"></button><ul class="dd"><li class="dd-all"><a href="{L('ai')}">{ic('core')}<span>{e(u['all_ai'])}</span></a></li>{ai_items}</ul></li>
<li class="has"><button type="button" class="nk">{e(u["nav_services"])}</button><button class="dd-t" aria-label="{e(u['nav_services'])}" aria-expanded="false"></button><ul class="dd">{srv_items}</ul></li>
<li><a class="nk" href="{L('projects')}">{e(u['nav_projects'])}</a></li>
<li><a class="nk" href="{L('blog')}">{e(u['nav_blog'])}</a></li>
<li><a class="nk" href="{L('about')}">{e(u['nav_about'])}</a></li>
<li><a class="nk" href="{L('contact')}">{e(u['nav_contact'])}</a></li>
</ul>
<div class="nx"><a class="lang" href="{alt}" hreflang="{other}" lang="{other}">{'EN' if lang=='tr' else 'TR'}<span class="sr"> — {e(u['other'])}</span></a>
<a class="btn btn-wa sm" href="{wa_link(lang)}" rel="noopener" target="_blank">{WA_SVG}<span>{e(u['wa_btn'])}</span></a></div>
</nav></div></header>'''

def footer_html(lang):
    u = UI[lang]; L = lambda k: link(k, lang, lang); pre = '../' if lang == 'en' else ''
    col = lambda keys: "".join(f'<li><a href="{L(k)}">{e(T(k,lang).get("nav") or T(k,lang)["h1"])}</a></li>' for k in keys)
    corp = [("about", u["nav_about"]), ("projects", u["nav_projects"]), ("blog", u["nav_blog"]), ("faqpage", u["nav_faq"]), ("contact", u["nav_contact"])]
    legal = ["privacy", "kvkk", "cookies"]
    email = f'<li><a href="mailto:{e(SITE["email"])}">{e(SITE["email"])}</a></li>' if SITE["email"] else ""
    return f'''<footer class="ft"><div class="ft-in">
<div class="ft-brand"><img src="{pre}assets/logo-light.png" alt="DEEP REKLAM" width="120" height="91">
<p class="ft-tag">{e(u['footer_tag'])}</p>
<ul class="ft-c"><li><a href="tel:{SITE['phone_href']}">{ic('phone')}<span>{e(SITE['phone'])}</span></a></li>
<li><a href="{wa_link(lang)}" target="_blank" rel="noopener">{WA_SVG}<span>WhatsApp</span></a></li>{email}
<li><a href="{SITE['maps']}" target="_blank" rel="noopener">{ic('map')}<span>{e(u['maps_link'])}</span></a></li></ul></div>
<div><h2>{e(u['footer_ai'])}</h2><ul>{col(['ai']+AI_KEYS)}</ul></div>
<div><h2>{e(u['footer_srv'])}</h2><ul>{col(SRV_KEYS)}</ul></div>
<div><h2>{e(u['footer_corp'])}</h2><ul>{''.join(f'<li><a href="{L(k)}">{e(t)}</a></li>' for k,t in corp)}</ul>
<h2 class="mt">{e(u['footer_legal'])}</h2><ul>{col(legal)}</ul></div>
</div><div class="ft-b"><span>© 2026 DEEP REKLAM. {e(u['rights'])}</span><span>Design. Advertising. Technology. Intelligent Automation.</span></div></footer>
<div class="mbar"><a href="tel:{SITE['phone_href']}">{ic('phone')}<span>{e(u['call'])}</span></a><a class="wa" href="{wa_link(lang)}" target="_blank" rel="noopener">{WA_SVG}<span>WhatsApp</span></a><a href="{L('contact')}">{ic('chat')}<span>{e(u['cta_quote'])}</span></a></div>'''

def head_html(key, lang, title, desc, ld, noindex=False):
    pre = '../' if lang == 'en' else ''
    alts = ""
    if key:
        alts = (f'<link rel="canonical" href="{absu(key,lang)}">'
                f'<link rel="alternate" hreflang="tr" href="{absu(key,"tr")}">'
                f'<link rel="alternate" hreflang="en" href="{absu(key,"en")}">'
                f'<link rel="alternate" hreflang="x-default" href="{absu(key,"tr")}">'
                f'<meta property="og:url" content="{absu(key,lang)}">')
    ldj = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)
    return f'''<!DOCTYPE html><html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
{'<meta name="robots" content="noindex">' if noindex else ''}{alts}
<meta property="og:type" content="website"><meta property="og:site_name" content="DEEP REKLAM"><meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}"><meta property="og:image" content="{SITE_URL}/assets/og.png"><meta property="og:locale" content="{'tr_TR' if lang=='tr' else 'en_US'}">
<meta name="twitter:card" content="summary_large_image"><meta name="theme-color" content="#0e0e0f">
<link rel="icon" href="{pre}assets/favicon.png"><link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Inter:wght@400;500;600&display=swap">
<link rel="stylesheet" href="{pre}assets/style.css?v={VER}">{ldj}</head>'''

def page(key, lang, title, desc, body, ld=None, noindex=False, cls=""):
    u = UI[lang]; pre = '../' if lang == 'en' else ''
    return (head_html(key, lang, title, desc, ld or [], noindex) +
            f'<body class="{cls}"><a class="skip" href="#main">{e(u["skip"])}</a>{nav_html(lang, key or "home")}<main id="main">{body}</main>{footer_html(lang)}'
            f'<button class="cb-fab" type="button" aria-haspopup="dialog" aria-label="{e(chatbot.UI[lang]["open"])}">{ic("chat","ic lg")}<span>{e(chatbot.UI[lang]["title"])}</span></button>'
            f'<script>window.DR={json.dumps({"lang":lang,"wa":SITE["wa"],"endpoint":FORM_ENDPOINT,"root":pre,"ver":VER,"chat":{"endpoint":CHAT_ENDPOINT,**chatbot.UI[lang]},"ui":{k:u[k] for k in ["f_err","f_copied","f_ok","f_fail","f_wa_head","replay","demo"]}}, ensure_ascii=False)}</script>'
            f'<script src="{pre}assets/app.js?v={VER}" defer></script></body></html>')

# ------------------------------------------------------------ JSON-LD
ORG = lambda lang: {"@context": "https://schema.org", "@type": ["Organization", "LocalBusiness"], "@id": SITE_URL + "/#org",
    "name": "DEEP REKLAM", "url": SITE_URL + "/", "logo": SITE_URL + "/assets/logo.png", "image": SITE_URL + "/assets/og.png",
    "telephone": SITE["phone"], "slogan": "Markanızı Her Alanda Güçlendiriyoruz." if lang == "tr" else "Design. Advertising. Technology. Intelligent Automation.",
    "geo": {"@type": "GeoCoordinates", "latitude": SITE["lat"], "longitude": SITE["lng"]}, "hasMap": SITE["maps"],
    "areaServed": ["TR", "Worldwide"], "founder": {"@type": "Person", "name": SITE["owner"]},
    "contactPoint": {"@type": "ContactPoint", "telephone": SITE["phone"], "contactType": "customer service", "availableLanguage": ["Turkish", "English"]}}

def crumbs(key, lang):
    items = [("home", UI[lang]["home"])]
    if P[key]["kind"] == "ai": items.append(("ai", UI[lang]["nav_ai"]))
    if P[key]["kind"] == "post": items.append(("blog", T("blog", lang)["h1"]))
    items.append((key, T(key, lang).get("nav") or T(key, lang)["h1"]))
    ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": absu(k, lang)} for i, (k, n) in enumerate(items)]}
    h = '<nav class="bc" aria-label="breadcrumb"><ol>' + "".join(
        f'<li>{"<a href=" + chr(34) + link(k, lang, lang) + chr(34) + ">" + e(n) + "</a>" if i < len(items) - 1 else "<span aria-current=" + chr(34) + "page" + chr(34) + ">" + e(n) + "</span>"}</li>'
        for i, (k, n) in enumerate(items)) + '</ol></nav>'
    return h, ld

def faq_ld(items):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in items]}

# ------------------------------------------------------------ bloklar
def faq_block(lang, items, title=True):
    if not items: return ""
    qs = "".join(f'<details class="qa"><summary><span>{e(q)}</span></summary><p>{e(a)}</p></details>' for q, a in items)
    return f'<section class="band"><div class="wrap narrow">{"<h2>" + e(UI[lang]["faq"]) + "</h2>" if title else ""}{qs}</div></section>'

def steps_block(lang, ai=True):
    st = UI[lang]["steps" if ai else "steps_srv"]
    li = "".join(f'<li><span class="sn">{i+1}</span><h3>{e(a)}</h3><p>{e(b)}</p></li>' for i, (a, b) in enumerate(st))
    return f'<section class="band alt"><div class="wrap"><h2>{e(UI[lang]["how"])}</h2><ol class="steps">{li}</ol></div></section>'

def cta_band(lang, ai=False):
    u = UI[lang]; L = lambda k: link(k, lang, lang)
    return f'''<section class="band dark cta"><div class="wrap cta-in"><div><h2>{e(u['cta_band_t'])}</h2><p>{e(u['cta_band_p'])}</p></div>
<div class="cta-b"><a class="btn btn-gold" href="{L('contact')}">{e(u['cta_main'] if ai else u['cta_quote'])}{ic('arrow')}</a>
<a class="btn btn-wa" href="{wa_link(lang)}" target="_blank" rel="noopener">{WA_SVG}<span>{e(u['cta_wa'])}</span></a>
<a class="btn btn-ghost" href="tel:{SITE['phone_href']}">{ic('phone')}<span>{e(SITE['phone'])}</span></a></div></div></section>'''

def demo_shell(lang, kind, extra=""):
    u = UI[lang]
    return f'''<figure class="demo demo-{kind}" data-demo="{kind}" aria-label="{e(u['demo'])}">
<div class="demo-tag"><span class="dot"></span>{e(u['demo'])}</div>{extra}<div class="demo-body" aria-live="polite"></div>
<figcaption>{e(u['demo_note'])} <button class="replay" type="button">{e(u['replay'])}</button></figcaption></figure>'''

def flow_svg(lang, kind="flow"):
    if kind == "flow":
        L = {"tr": (["WhatsApp", "Instagram", "Web sitesi", "Telefon"], "DEEP AI", ["CRM kaydı", "Randevu", "Ekibe bildirim"]),
             "en": (["WhatsApp", "Instagram", "Website", "Phone"], "DEEP AI", ["CRM record", "Booking", "Team alert"])}[lang]
    else:
        L = {"tr": (["Web formu", "Webhook", "Reklam leadi", "E-posta"], "n8n / Make", ["CRM", "Google Sheets", "WhatsApp mesajı"]),
             "en": (["Web form", "Webhook", "Ad lead", "Email"], "n8n / Make", ["CRM", "Google Sheets", "WhatsApp message"])}[lang]
    ins, core, outs = L
    W, H = 760, 340
    s = [f'<svg viewBox="0 0 {W} {H}" class="flow" role="img" aria-label="{e(" → ".join(ins) + " → " + core + " → " + " / ".join(outs))}"><defs><linearGradient id="g{kind}" x1="0" x2="1"><stop offset="0" stop-color="#c99e3e" stop-opacity=".1"/><stop offset=".5" stop-color="#e6c37a"/><stop offset="1" stop-color="#c99e3e" stop-opacity=".1"/></linearGradient></defs>']
    cx, cy = W / 2, H / 2
    for i, t in enumerate(ins):
        y = 40 + i * 86
        d = f"M150 {y+22} C 260 {y+22}, 250 {cy}, {cx-62} {cy}"
        s.append(f'<path d="{d}" class="fl-l"/><path d="{d}" class="fl-p" style="animation-delay:{i*0.7}s"/>')
        s.append(f'<g class="fl-n"><rect x="10" y="{y}" width="140" height="44" rx="10"/><text x="80" y="{y+27}" text-anchor="middle">{e(t)}</text></g>')
    for i, t in enumerate(outs):
        y = 62 + i * 96
        d = f"M{cx+62} {cy} C 500 {cy}, 500 {y+22}, 610 {y+22}"
        s.append(f'<path d="{d}" class="fl-l"/><path d="{d}" class="fl-p o" style="animation-delay:{1.4+i*0.7}s"/>')
        s.append(f'<g class="fl-n o"><rect x="610" y="{y}" width="140" height="44" rx="10"/><text x="680" y="{y+27}" text-anchor="middle">{e(t)}</text></g>')
    s.append(f'<g class="fl-core"><circle cx="{cx}" cy="{cy}" r="74" class="ring"/><circle cx="{cx}" cy="{cy}" r="60"/><text x="{cx}" y="{cy+6}" text-anchor="middle">{e(core)}</text></g></svg>')
    return "".join(s)

def hero_small(lang, t, crumb_h, extra_cls="", tag=None):
    return f'''<section class="ph {extra_cls}"><div class="wrap">{crumb_h}{('<p class="kick">'+e(tag)+'</p>') if tag else ''}<h1>{e(t['h1'])}</h1><p class="lede">{e(t['lede'])}</p></div></section>'''

def cards_ai(lang, keys=AI_KEYS):
    L = lambda k: link(k, lang, lang)
    return '<ul class="cards">' + "".join(
        f'<li><a class="card" href="{L(k)}">{ic(P[k]["icon"], "ic lg")}<h3>{e(T(k,lang)["nav"])}</h3><p>{e(T(k,lang)["card"])}</p><span class="more">{e(UI[lang]["read"])}{ic("arrow")}</span></a></li>'
        for k in keys) + '</ul>'

def cards_srv(lang, keys=SRV_KEYS):
    L = lambda k: link(k, lang, lang)
    return '<ul class="cards srv">' + "".join(
        f'<li><a class="card" href="{L(k)}">{ic(P[k]["icon"], "ic lg")}<h3>{e(T(k,lang)["nav"])}</h3><p>{e(T(k,lang)["card"])}</p><span class="more">{e(UI[lang]["read"])}{ic("arrow")}</span></a></li>'
        for k in keys) + '</ul>'

def form_html(lang, preset=0):
    u = UI[lang]; L = lambda k: link(k, lang, lang)
    tabs = "".join(f'<label class="tab"><input type="radio" name="ftype" value="{i}" {"checked" if i==preset else ""}><span>{e(t)}</span></label>' for i, t in enumerate(u["f_tabs"]))
    opts = "".join(f'<option{" selected" if (preset==1 and i==0) else ""}>{e(t)}</option>' for i, t in enumerate(u["f_topics"]))
    return f'''<form class="lead" novalidate data-endpoint="{e(FORM_ENDPOINT)}">
<fieldset class="tabs"><legend class="sr">{e(u['f_service'])}</legend>{tabs}</fieldset>
<div class="grid2"><label>{e(u['f_name'])} *<input name="name" required autocomplete="name" maxlength="80"></label>
<label>{e(u['f_company'])}<input name="company" autocomplete="organization" maxlength="100"></label>
<label>{e(u['f_phone'])} *<input name="phone" type="tel" required autocomplete="tel" inputmode="tel" maxlength="20" pattern="[0-9 +()-]{{7,20}}"></label>
<label>{e(u['f_email'])}<input name="email" type="email" autocomplete="email" maxlength="120"></label></div>
<label>{e(u['f_service'])}<select name="topic">{opts}</select></label>
<label>{e(u['f_msg'])} *<textarea name="msg" required rows="5" maxlength="1500"></textarea></label>
<label class="hp" aria-hidden="true">Website<input name="website" tabindex="-1" autocomplete="off"></label>
<label class="chk"><input type="checkbox" name="kvkk" required><span>{e(u['f_kvkk'])} <a href="{L('kvkk')}">{e(u['f_kvkk_link'])}</a> {e(u['f_kvkk_end'])} *</span></label>
<p class="ferr" role="alert" hidden></p>
<button class="btn btn-gold" type="submit">{e(u['f_submit'])}{ic('arrow')}</button>
<div class="fready" hidden><h3>{e(u['f_ready_t'])}</h3><p>{e(u['f_ready_p'])}</p><pre class="fprev"></pre>
<div class="cta-b"><a class="btn btn-wa fwa" target="_blank" rel="noopener">{WA_SVG}<span>{e(u['f_send_wa'])}</span></a><button type="button" class="btn btn-ghost-d fcopy">{e(u['f_copy'])}</button></div></div>
<p class="fok" role="status" hidden></p></form>'''

# ------------------------------------------------------------ sayfa türleri
def r_home(lang):
    t = T("home", lang); u = UI[lang]; L = lambda k: link(k, lang, lang)
    why = "".join(f'<li><h3>{e(a)}</h3><p>{e(b)}</p></li>' for a, b in t["why"])
    body = f'''<section class="hero"><div class="wrap hero-in"><div class="hero-t">
<p class="kick">{e('Design. Advertising. Technology. Intelligent Automation.')}</p>
<h1>{e(t['h1'])}</h1><p class="lede">{e(t['lede'])}</p>
<div class="cta-b"><a class="btn btn-gold" href="{L('contact')}">{e(u['cta_main'])}{ic('arrow')}</a><a class="btn btn-wa" href="{wa_link(lang)}" target="_blank" rel="noopener">{WA_SVG}<span>{e(u['cta_wa'])}</span></a></div>
<ul class="chips">{''.join(f'<li><a href="{L(k)}">{e(T(k,lang)["nav"])}</a></li>' for k in AI_KEYS)}</ul></div>
<div class="hero-v"><div class="orb" aria-hidden="true"></div><div class="phone">{demo_shell(lang,'chat')}</div></div></div></section>
<section class="band"><div class="wrap"><div class="sh"><h2>{e(t['ai_t'])}</h2><p>{e(t['ai_p'])}</p></div>{cards_ai(lang)}
<p class="center"><a class="btn btn-ghost-d" href="{L('ai')}">{e(u['all_ai'])}{ic('arrow')}</a></p></div></section>
<section class="band dark"><div class="wrap"><div class="sh"><h2>{e(t['flow_t'])}</h2><p>{e(t['flow_p'])}</p></div>
<div class="flow-wrap"><div class="demo-tag"><span class="dot"></span>{e(u['demo'])}</div>{flow_svg(lang)}</div></div></section>
<section class="band"><div class="wrap"><div class="sh"><h2>{e(t['srv_t'])}</h2><p>{e(t['srv_p'])}</p></div>{cards_srv(lang)}</div></section>
<section class="band alt"><div class="wrap"><h2>{e(t['why_t'])}</h2><ul class="why">{why}</ul></div></section>
{steps_block(lang)}
<section class="band"><div class="wrap gcard"><div>{ic('map','ic lg')}<h2>{e(t['google_t'])}</h2><p>{e(t['google_p'])}</p></div>
<a class="btn btn-ghost-d" href="{SITE['maps']}" target="_blank" rel="noopener">{e(u['reviews_link'])}{ic('arrow')}</a></div></section>
{cta_band(lang, True)}'''
    web = {"@context": "https://schema.org", "@type": "WebSite", "name": "DEEP REKLAM", "url": SITE_URL + "/", "inLanguage": lang}
    return page("home", lang, t["seo"], t["desc"], body, [ORG(lang), web], cls="home")

def r_ai_hub(lang):
    k = "ai"; t = T(k, lang); u = UI[lang]; ch, cld = crumbs(k, lang)
    li = "".join(f'<li>{ic("check")}<span>{e(x)}</span></li>' for x in t["list"])
    body = f'''<section class="ph dark"><div class="wrap ph-split"><div>{ch}<h1>{e(t['h1'])}</h1><p class="lede">{e(t['lede'])}</p>
<div class="cta-b"><a class="btn btn-gold" href="#form">{e(u['cta_main'])}{ic('arrow')}</a><a class="btn btn-wa" href="{wa_link(lang)}" target="_blank" rel="noopener">{WA_SVG}<span>{e(u['cta_wa'])}</span></a></div></div>
<div class="flow-wrap"><div class="demo-tag"><span class="dot"></span>{e(u['demo'])}</div>{flow_svg(lang)}</div></div></section>
<section class="band"><div class="wrap"><div class="sh"><h2>{e(u['what_we_do'])}</h2><p>{e(t['intro'])}</p></div>{cards_ai(lang)}</div></section>
<section class="band alt"><div class="wrap"><h2>{'Kapsam' if lang=='tr' else 'Scope'}</h2><ul class="ticks">{li}</ul></div></section>
<section class="band dark"><div class="wrap"><div class="sh"><h2>{'Çoklu ajanlar nasıl iş bölüşür?' if lang=='tr' else 'How agents share the work'}</h2></div>{demo_shell(lang,'agents')}</div></section>
{steps_block(lang)}
<section class="band" id="form"><div class="wrap narrow"><h2>{e(u['f_tabs'][1])}</h2>{form_html(lang,1)}</div></section>
{faq_block(lang, t['faq'])}'''
    svc = {"@context": "https://schema.org", "@type": "Service", "name": t["h1"], "serviceType": u["nav_ai"], "provider": {"@id": SITE_URL + "/#org"}, "description": t["desc"], "areaServed": "Worldwide"}
    return page(k, lang, t["seo"], t["desc"], body, [cld, svc, faq_ld(t["faq"])])

def r_ai(k, lang):
    t = T(k, lang); u = UI[lang]; ch, cld = crumbs(k, lang); d = P[k]["demo"]
    pts = "".join(f'<li>{ic("check","ic lg")}<h3>{e(a)}</h3><p>{e(b)}</p></li>' for a, b in t["points"])
    li = "".join(f'<li>{ic("check")}<span>{e(x)}</span></li>' for x in t["list"])
    demo = flow_svg(lang, "wf") if d == "workflow" else ""
    demo_html = (f'<div class="flow-wrap"><div class="demo-tag"><span class="dot"></span>{e(u["demo"])}</div>{demo}</div>' if d == "workflow" else demo_shell(lang, d))
    others = [x for x in AI_KEYS if x != k][:3]
    body = f'''<section class="ph dark"><div class="wrap ph-split"><div>{ch}<h1>{e(t['h1'])}</h1><p class="lede">{e(t['lede'])}</p>
<div class="cta-b"><a class="btn btn-gold" href="{link('contact',lang,lang)}">{e(u['cta_main'])}{ic('arrow')}</a><a class="btn btn-wa" href="{wa_link(lang, u['f_wa_head']+' '+t['nav'])}" target="_blank" rel="noopener">{WA_SVG}<span>{e(u['cta_wa'])}</span></a></div></div>
<div class="{'phone' if d=='chat' else 'demo-box'}">{demo_html}</div></div></section>
<section class="band"><div class="wrap"><ul class="points">{pts}</ul></div></section>
<section class="band alt"><div class="wrap"><h2>{e(u['what_we_do'])}</h2><ul class="ticks">{li}</ul></div></section>
{steps_block(lang)}{faq_block(lang, t['faq'])}
<section class="band"><div class="wrap"><h2>{e(u['related'])}</h2>{cards_ai(lang, others)}</div></section>{cta_band(lang, True)}'''
    svc = {"@context": "https://schema.org", "@type": "Service", "name": t["nav"], "serviceType": u["nav_ai"], "provider": {"@id": SITE_URL + "/#org"}, "description": t["desc"], "areaServed": "Worldwide", "url": absu(k, lang)}
    return page(k, lang, t["seo"], t["desc"], body, [cld, svc, faq_ld(t["faq"])])

def r_service(k, lang):
    t = T(k, lang); u = UI[lang]; ch, cld = crumbs(k, lang)
    groups = "".join(f'<div class="grp"><h3>{e(g)}</h3><ul class="ticks one">{"".join(f"<li>{ic(chr(99)+chr(104)+chr(101)+chr(99)+chr(107))}<span>{e(x)}</span></li>" for x in items)}</ul></div>' for g, items in t["groups"])
    ai_hint = {"tr": "Bu hizmeti AI otomasyonla birleştirin: reklamınızdan, tabelanızdaki QR koddan veya web sitenizden gelen talepleri WhatsApp AI asistanı anında karşılasın.",
               "en": "Combine this service with AI automation: let a WhatsApp AI assistant instantly answer leads coming from your ads, the QR code on your sign or your website."}[lang]
    others = [x for x in SRV_KEYS if x != k][:3]
    body = f'''{hero_small(lang, t, ch)}
<section class="band"><div class="wrap"><h2>{e(u['what_we_do'])}</h2><div class="grps">{groups}</div></div></section>
<section class="band dark"><div class="wrap aihint">{ic('core','ic xl')}<div><h2>{'AI ile bir adım öteye' if lang=='tr' else 'One step further with AI'}</h2><p>{e(ai_hint)}</p></div>
<a class="btn btn-gold" href="{link('whatsapp',lang,lang)}">{e(T('whatsapp',lang)['nav'])}{ic('arrow')}</a></div></section>
{steps_block(lang, False)}
<section class="band"><div class="wrap"><h2>{e(u['related'])}</h2>{cards_srv(lang, others)}</div></section>{cta_band(lang)}'''
    svc = {"@context": "https://schema.org", "@type": "Service", "name": t["nav"], "provider": {"@id": SITE_URL + "/#org"}, "description": t["desc"], "areaServed": ["TR", "Worldwide"], "url": absu(k, lang)}
    return page(k, lang, t["seo"], t["desc"], body, [cld, svc])

def text_sections(body):
    return "".join(f'<h2>{e(h)}</h2>' + "".join(f"<p>{e(p)}</p>" for p in ps) for h, ps in body)

def r_text(k, lang, extra=""):
    t = T(k, lang); ch, cld = crumbs(k, lang)
    body = f'''{hero_small(lang, t, ch)}<section class="band"><div class="wrap narrow prose">{text_sections(t['body'])}{extra}</div></section>{cta_band(lang)}'''
    return page(k, lang, t["seo"], t["desc"], body, [cld])

def r_projects(lang):
    u = UI[lang]
    extra = f'<div class="cta-b"><a class="btn btn-wa" href="{wa_link(lang, u["f_wa_head"] + (" Örnek çalışmalarınızı görmek istiyorum." if lang=="tr" else " I would like to see examples of your work."))}" target="_blank" rel="noopener">{WA_SVG}<span>{e(u["cta_wa"])}</span></a><a class="btn btn-ghost-d" href="{SITE["maps"]}" target="_blank" rel="noopener">{e(u["reviews_link"])}{ic("arrow")}</a></div>'
    return r_text("projects", lang, extra)

def r_blog(lang):
    t = T("blog", lang); ch, cld = crumbs("blog", lang)
    items = "".join(f'<li><a class="card post" href="{link(p["key"],lang,lang)}"><time datetime="{p["date"]}">{p["date"][8:]}.{p["date"][5:7]}.{p["date"][:4]}</time><h3>{e(p[lang]["h1"])}</h3><p>{e(p[lang]["desc"])}</p><span class="more">{e(UI[lang]["read"])}{ic("arrow")}</span></a></li>' for p in POSTS)
    body = f'{hero_small(lang, t, ch)}<section class="band"><div class="wrap"><ul class="cards">{items}</ul></div></section>{cta_band(lang)}'
    return page("blog", lang, t["seo"], t["desc"], body, [cld])

def r_post(p, lang):
    k = p["key"]; t = p[lang]; ch, cld = crumbs(k, lang)
    art = {"@context": "https://schema.org", "@type": "Article", "headline": t["h1"], "description": t["desc"], "datePublished": p["date"], "inLanguage": lang,
           "author": {"@type": "Organization", "name": "DEEP REKLAM"}, "publisher": {"@id": SITE_URL + "/#org"}, "mainEntityOfPage": absu(k, lang), "image": SITE_URL + "/assets/og.png"}
    body = f'''{hero_small(lang, t, ch)}<article class="band"><div class="wrap narrow prose"><p class="meta"><time datetime="{p['date']}">{p['date']}</time> · DEEP REKLAM</p>{text_sections(t['body'])}</div></article>{cta_band(lang, True)}'''
    return page(k, lang, t["h1"] + " | DEEP REKLAM", t["desc"], body, [cld, art])

def r_faq(lang):
    t = T("faqpage", lang); ch, cld = crumbs("faqpage", lang)
    body = f'{hero_small(lang, t, ch)}{faq_block(lang, t["items"], False)}{cta_band(lang)}'
    return page("faqpage", lang, t["seo"], t["desc"], body, [cld, faq_ld(t["items"])])

def r_contact(lang):
    t = T("contact", lang); u = UI[lang]; ch, cld = crumbs("contact", lang)
    email = f'<li><a href="mailto:{e(SITE["email"])}">{e(SITE["email"])}</a></li>' if SITE["email"] else ""
    q = f'https://maps.google.com/maps?q={SITE["lat"]},{SITE["lng"]}&z=16&output=embed'
    body = f'''{hero_small(lang, t, ch)}<section class="band"><div class="wrap ct">
<div class="ct-side"><ul class="ct-list">
<li><a class="btn btn-wa wide" href="{wa_link(lang)}" target="_blank" rel="noopener">{WA_SVG}<span>{e(u['cta_wa'])}</span></a></li>
<li><a class="ct-row" href="tel:{SITE['phone_href']}">{ic('phone','ic lg')}<span><small>{e(u['call'])}</small>{e(SITE['phone'])}</span></a></li>{email}
<li><a class="ct-row" href="{SITE['maps']}" target="_blank" rel="noopener">{ic('map','ic lg')}<span><small>Google</small>{e(u['maps_link'])}</span></a></li></ul>
<div class="map" data-src="{e(q)}"><button type="button" class="btn btn-ghost-d">{ic('map')}<span>{e(u['map_load'])}</span></button><p>{e(u['map_note'])}</p></div></div>
<div class="ct-form">{form_html(lang,0)}</div></div></section>'''
    return page("contact", lang, t["seo"], t["desc"], body, [cld, ORG(lang)])

def r_404(lang="tr"):
    u = UI["tr"]; v = UI["en"]
    body = f'''<section class="ph dark nf"><div class="wrap"><p class="kick">404</p><h1>{e(u['404_t'])}</h1><p class="lede">{e(u['404_p'])}</p>
<p class="lede" lang="en">{e(v['404_t'])} {e(v['404_p'])}</p><div class="cta-b"><a class="btn btn-gold" href="./">{e(u['home'])}</a><a class="btn btn-ghost" href="en/">English</a><a class="btn btn-wa" href="{wa_link('tr')}" target="_blank" rel="noopener">{WA_SVG}<span>WhatsApp</span></a></div></div></section>'''
    h = page(None, "tr", "404 | DEEP REKLAM", u["404_p"], body, noindex=True)
    return h.replace("<head><meta charset=\"utf-8\">", f'<head><meta charset="utf-8"><base href="{SITE_URL}/">', 1)

# ------------------------------------------------------------ çıktı
def write(rel, s):
    fp = os.path.join(OUT, rel); os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(s)

def main():
    if os.path.exists(OUT): shutil.rmtree(OUT)
    shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))
    for lang in LANGS:
        pre = "" if lang == "tr" else "en/"
        for k, pg in P.items():
            kind = pg["kind"]
            if kind == "home": h = r_home(lang)
            elif kind == "ai_hub": h = r_ai_hub(lang)
            elif kind == "ai": h = r_ai(k, lang)
            elif kind == "service": h = r_service(k, lang)
            elif kind == "projects": h = r_projects(lang)
            elif kind in ("text", "legal"): h = r_text(k, lang)
            elif kind == "blog": h = r_blog(lang)
            elif kind == "post": h = r_post(pg, lang)
            elif kind == "faq": h = r_faq(lang)
            elif kind == "contact": h = r_contact(lang)
            p = path(k, lang)
            write(p + "index.html" if p in ("", "en/") else p, h)
    for lang in LANGS:
        write(f"assets/kb-{lang}.json", json.dumps(chatbot.kb(lang, path), ensure_ascii=False, separators=(",", ":")))
    wk = os.path.join(os.path.dirname(ROOT), "worker", "knowledge.js")
    os.makedirs(os.path.dirname(wk), exist_ok=True)
    open(wk, "w", encoding="utf-8").write("// build.py tarafından üretilir — elle düzenlemeyin\nexport const KNOWLEDGE = " + json.dumps(chatbot.knowledge_text(), ensure_ascii=False) + ";\n")
    write("404.html", r_404())
    write(".nojekyll", "")
    # sitemap
    urls = []
    for k in P:
        alts = "".join(f'<xhtml:link rel="alternate" hreflang="{l}" href="{absu(k,l)}"/>' for l in LANGS) + f'<xhtml:link rel="alternate" hreflang="x-default" href="{absu(k,"tr")}"/>'
        for l in LANGS: urls.append(f"<url><loc>{absu(k,l)}</loc>{alts}</url>")
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(urls) + "\n</urlset>\n")
    write("robots.txt", f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n")
    # llms.txt
    lines = ["# DEEP REKLAM", "", "> DEEP REKLAM is a Turkey-based advertising and technology brand. Core focus: AI automation (WhatsApp AI assistants, AI sales agents, AI customer service and booking, AI voice assistants, multi-agent systems, n8n/Make workflow automation). Also: signage and outdoor advertising, graphic design, web design, custom software, digital marketing, SEO/GEO, social media, print and promotion. Prices are quoted per project.", "",
             f"Contact: phone and WhatsApp {SITE['phone']}. Google Maps: {SITE['maps']}", "", "## AI automation (EN)"]
    lines += [f"- [{T(k,'en').get('nav', T(k,'en')['h1'])}]({absu(k,'en')}): {T(k,'en')['desc']}" for k in ["ai"] + AI_KEYS]
    lines += ["", "## Services (EN)"] + [f"- [{T(k,'en')['nav']}]({absu(k,'en')}): {T(k,'en')['desc']}" for k in SRV_KEYS]
    lines += ["", "## Türkçe sayfalar"] + [f"- [{T(k,'tr').get('nav') or T(k,'tr')['h1']}]({absu(k,'tr')}): {T(k,'tr')['desc']}" for k in ["home", "ai"] + AI_KEYS + SRV_KEYS + ["about", "faqpage", "contact"]]
    lines += ["", "## Optional", f"- [FAQ]({absu('faqpage','en')})", f"- [About]({absu('about','en')})", f"- [Contact]({absu('contact','en')})"]
    write("llms.txt", "\n".join(lines) + "\n")
    print("built", sum(len(f) for _, _, f in os.walk(OUT)), "files ->", OUT)

if __name__ == "__main__":
    main()
