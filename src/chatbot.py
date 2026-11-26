# -*- coding: utf-8 -*-
"""Sohbet asistanı bilgi tabanı. build.py bunu çağırır ve assets/kb-tr.json, assets/kb-en.json üretir.
Asistan yalnızca buradaki ve content.py'deki bilgilerle yanıt verir; bilmediği konuda ekibe yönlendirir."""
from content import SITE, P, POSTS, AI_KEYS, SRV_KEYS

# Arama için ek anahtar kelimeler (Türkçe karakterler build sırasında normalize edilir)
KW = {
 "tr": {
  "ai": "yapay zeka ai otomasyon otomatik bot chatbot asistan robot", "whatsapp": "whatsapp wp mesaj mesajlara otomatik cevap yanit asistan business bot botu",
  "sales": "satis temsilcisi lead aday musteri adayi teklif takip huni", "support": "musteri hizmetleri chatbot randevu randevular restoran kafe klinik salon rezervasyon instagram dm messenger destek hatirlatma takvim",
  "voice": "telefon sesli cagri arama santral sesli asistan cagri merkezi", "agents": "ajan ajanlar coklu agent multi gorev",
  "workflow": "is akisi otomasyon n8n make webhook api entegrasyon zapier crm baglama tablo sheets",
  "signage": "tabela kutu harf neon led totem pylon cephe giydirme arac kaplama folyo billboard branda pleksi krom isikli isiksiz vitrin montaj olcu kesif cnc lazer",
  "design": "logo kurumsal kimlik katalog brosur kartvizit ambalaj etiket menu tasarim grafik 3d gorsel",
  "web": "web sitesi site internet sitesi e-ticaret eticaret online magaza landing kurumsal sayfa",
  "software": "yazilim crm erp panel uygulama mobil app saas program rezervasyon sistemi stok",
  "marketing": "reklam google ads meta instagram reklami facebook tiktok youtube linkedin kampanya dijital pazarlama remarketing",
  "seo": "seo google sirala siralama ilk sayfa arama geo aeo llm chatgpt gemini harita maps isletme profili",
  "social": "sosyal medya instagram yonetimi reels video icerik paylasim takipci hesap",
  "print": "matbaa baski bastirmak bastirma basim kartvizit brosur roll-up rollup promosyon kupa kalem canta etiket sticker afis",
  "about": "hakkinizda kimsiniz firma sirket deep reklam nedir", "projects": "proje projeler portfoy referans ornek calisma isleriniz",
  "faqpage": "sss sik sorulan", "contact": "iletisim ulas telefon numara whatsapp adres", "kvkk": "kvkk kisisel veri gizlilik",
 },
 "en": {
  "ai": "artificial intelligence ai automation automatic bot chatbot assistant", "whatsapp": "whatsapp message reply automatic assistant business bot",
  "sales": "sales agent lead leads prospect quote follow up funnel", "support": "customer service support chatbot appointment booking reservation instagram dm messenger reminder calendar",
  "voice": "phone voice call calls receptionist call center", "agents": "agent agents multi multiagent tasks",
  "workflow": "workflow automation n8n make webhook api integration zapier crm connect spreadsheet sheets",
  "signage": "sign signs signage channel letters neon led totem pylon facade vehicle wrap film billboard banner acrylic chrome illuminated storefront installation survey cnc laser",
  "design": "logo brand identity catalogue catalog brochure business card packaging label menu design graphic 3d visual",
  "web": "website web site ecommerce e-commerce online store shop landing page",
  "software": "software crm erp panel app mobile saas program booking system stock",
  "marketing": "ads advertising google ads meta instagram facebook tiktok youtube linkedin campaign digital marketing remarketing",
  "seo": "seo google ranking rank first page search geo aeo llm chatgpt gemini maps business profile",
  "social": "social media instagram management reels video content posts followers account",
  "print": "print printing business cards brochure roll-up rollup promotional mugs pens bags labels stickers poster",
  "about": "about who are you company deep reklam", "projects": "projects portfolio references examples work",
  "faqpage": "faq frequently asked", "contact": "contact reach phone number whatsapp address", "kvkk": "data protection privacy personal data gdpr kvkk",
 }}

def intents(lang):
    ph = SITE["phone"]
    if lang == "tr":
        return [
         ("greet", "merhaba selam selamlar iyi gunler gunaydin iyi aksamlar hey sa", "Merhaba! Ben DEEP Asistan. AI otomasyon, tabela, tasarım, web sitesi, yazılım veya reklam hakkında ne öğrenmek istersiniz?", None),
         ("thanks", "tesekkurler tesekkur ederim sagol sag ol eyvallah", "Rica ederim! Başka bir sorunuz olursa buradayım. Projenizi konuşmak isterseniz WhatsApp'tan da yazabilirsiniz.", None),
         ("price", "fiyat fiyati ucret ucreti kac para ne kadar maliyet butce fiyatlar tutar paket", "Fiyatları projeye özel hazırlıyoruz, çünkü ölçü, kapsam, malzeme ve entegrasyon her işte farklı. İhtiyacınızı kısaca WhatsApp'tan ya da teklif formundan iletirseniz size net bir teklif sunarız.", "contact"),
         ("phone", "telefon numara numaraniz arayabilir miyim gsm cep", f"Bize {ph} numarasından telefonla veya WhatsApp'tan ulaşabilirsiniz.", "contact"),
         ("location", "adres nerede neredesiniz konum yeriniz harita yol tarifi ofis dukkan", "Konumumuzu Google Haritalar'daki işletme profilimizde görebilirsiniz. İletişim sayfasındaki 'Google Haritalar'da aç' bağlantısı sizi doğrudan oraya götürür.", "contact"),
         ("hours", "saat saatleri kacta acik kapali calisma saatleri mesai", "Güncel çalışma saatlerimizi Google işletme profilimizde görebilirsiniz. En hızlı yanıt için WhatsApp'tan yazabilirsiniz.", "contact"),
         ("human", "yetkili insan biriyle gorusmek temsilci canli destek sizi arasin geri donus", f"Elbette. Ekibimize WhatsApp'tan veya {ph} numarasından doğrudan ulaşabilirsiniz. Aşağıdaki butonla sorunuzu WhatsApp'a hazır mesaj olarak aktarabilirsiniz.", "contact"),
         ("bot", "sen kimsin bot musun yapay zeka misin insan misin", "Ben DEEP REKLAM web sitesinin otomatik asistanıyım. Sitedeki bilgilerle yanıt veriyorum. Kesin bilgi ve teklif için ekibimiz size dönüş yapar.", None),
         ("intl", "yurt disi yurtdisi ingilizce yabanci uluslararasi abroad", "Tasarım, yazılım, dijital pazarlama ve AI otomasyon hizmetlerini Türkiye geneline ve yurt dışına uzaktan veriyoruz. Çok dilli web siteleri de kuruyoruz. Tabela ve montaj gibi yerinde yapılan işler için bölgesel planlama yapıyoruz.", "about"),
         ("time", "ne kadar surer sure teslim kac gun zaman", "Süre işin kapsamına göre değişiyor. İhtiyacınızı öğrendiğimizde size teklifle birlikte net bir teslim süresi bildiriyoruz.", "contact"),
        ]
    return [
     ("greet", "hello hi hey good morning good afternoon good evening greetings", "Hi! I'm DEEP Assistant. What would you like to know about AI automation, signage, design, websites, software or advertising?", None),
     ("thanks", "thanks thank you cheers", "You're welcome! I'm here if you have more questions. You can also message us on WhatsApp to discuss your project.", None),
     ("price", "price prices pricing cost costs how much budget fee quote package", "We prepare pricing per project, since size, scope, materials and integrations differ every time. Send us a short description on WhatsApp or through the quote form and we'll send a clear quote.", "contact"),
     ("phone", "phone number call mobile", f"You can reach us by phone or WhatsApp at {ph}.", "contact"),
     ("location", "address where located location map directions office", "You can see our location on our Google Business Profile. The 'Open in Google Maps' link on the contact page takes you straight there.", "contact"),
     ("hours", "hours open opening closed working hours", "Our current opening hours are on our Google Business Profile. For the quickest reply, message us on WhatsApp.", "contact"),
     ("human", "human person representative agent talk live support call me back", f"Of course. You can reach our team directly on WhatsApp or at {ph}. Use the button below to send your question to WhatsApp as a ready message.", "contact"),
     ("bot", "who are you are you a bot are you ai human", "I'm the automated assistant on DEEP REKLAM's website. I answer using the information on this site. For firm details and quotes, our team will get back to you.", None),
     ("intl", "abroad international english foreign worldwide", "We deliver design, software, digital marketing and AI automation across Turkey and remotely abroad, and we build multilingual websites. On-site work such as sign installation is planned regionally.", "about"),
     ("time", "how long duration delivery days timeline", "It depends on the scope. Once we understand your needs, we give you a clear timeline along with the quote.", "contact"),
    ]

UI = {
 "tr": {"title": "DEEP Asistan", "sub_local": "Otomatik asistan · sitedeki bilgilerle yanıtlar", "sub_ai": "Yapay zekâ asistanı",
        "hello": "Merhaba! Ben DEEP Asistan. Size nasıl yardımcı olabilirim? Aşağıdan bir konu seçebilir ya da sorunuzu yazabilirsiniz.",
        "chips": ["AI otomasyon nedir?", "WhatsApp AI asistanı", "Tabela yaptırmak istiyorum", "Web sitesi", "Fiyat bilgisi", "İletişim"],
        "ph": "Sorunuzu yazın…", "send": "Gönder", "open": "Sohbet asistanını aç", "close": "Kapat",
        "go": "Sayfaya git", "wa": "WhatsApp'tan devam et", "form": "Teklif formu", "also": "İlgili:",
        "fallback": "Bu konuda en doğru bilgiyi ekibimiz verebilir. Sorunuzu aşağıdaki butonla WhatsApp'a hazır mesaj olarak gönderebilirsiniz.",
        "phone_note": "Telefon numaranızı bu sohbetten kaydetmiyoruz. Ekibimizin size dönmesi için aşağıdaki butonla mesajınızı WhatsApp'tan gönderin.",
        "note": "Yanıtlar bilgilendirme amaçlıdır. Lütfen kişisel veya hassas bilgi paylaşmayın.", "wa_head": "Merhaba, web sitenizdeki asistandan yazıyorum:"},
 "en": {"title": "DEEP Assistant", "sub_local": "Automated assistant · answers from this site", "sub_ai": "AI assistant",
        "hello": "Hi! I'm DEEP Assistant. How can I help? Pick a topic below or type your question.",
        "chips": ["What is AI automation?", "WhatsApp AI assistant", "I need a sign", "Website", "Pricing", "Contact"],
        "ph": "Type your question…", "send": "Send", "open": "Open chat assistant", "close": "Close",
        "go": "Open page", "wa": "Continue on WhatsApp", "form": "Quote form", "also": "Related:",
        "fallback": "Our team can give you the most accurate answer on this. Use the button below to send your question to WhatsApp as a ready message.",
        "phone_note": "We don't store your phone number from this chat. To have our team get back to you, send your message on WhatsApp with the button below.",
        "note": "Answers are for information only. Please don't share personal or sensitive details.", "wa_head": "Hello, I'm writing from the assistant on your website:"},
}

def kb(lang, path):
    """path(key, lang) -> site-relative path. Returns list of entries."""
    out = []
    def add(id_, title, kw, ans, key=None, w=1.0):
        u = path(key, lang) if key else ""
        if key and (u == "" or u.endswith("/")): u += "index.html"
        out.append({"id": id_, "t": title, "k": kw, "a": ans, "u": u, "w": w})
    for k in ["ai"] + AI_KEYS + SRV_KEYS + ["about", "projects", "faqpage", "contact", "kvkk"]:
        t = P[k][lang]
        title = t.get("nav") or t["h1"]
        ans = t.get("card") or t.get("lede") or t["desc"]
        if k in AI_KEYS + SRV_KEYS:
            ans = t["lede"]
        add("p-" + k, title, f'{title} {KW[lang].get(k, "")} {t.get("desc", "")}', ans, k, 1.0)
        for i, (q, a) in enumerate(t.get("faq", []) + t.get("items", [])):
            add(f"f-{k}-{i}", q, f"{q} {title}", a, k, 0.7)
        if "groups" in t:
            items = " ".join(x for _, g in t["groups"] for x in g)
            add("g-" + k, title, items, ans + (" Sunduklarımız arasında: " if lang == "tr" else " Our work includes: ") + ", ".join(x for _, g in t["groups"] for x in g[:2]) + ".", k, 0.8)
    for p in POSTS:
        t = p[lang]
        add("b-" + p["key"], t["h1"], f'{t["h1"]} {t["desc"]}', t["lede"], p["key"], 0.7)
    for id_, kw, a, key in intents(lang):
        add("i-" + id_, "", kw, a, key, 1.6)
    return out

def knowledge_text():
    """Gerçek yapay zekâ modu için sunucu tarafı sistem bilgisi (worker/knowledge.js)."""
    L = []
    for lang in ("tr", "en"):
        L.append(f"## {lang.upper()}")
        for k in ["ai"] + AI_KEYS + SRV_KEYS + ["about", "faqpage"]:
            t = P[k][lang]
            L.append(f"### {t.get('nav') or t['h1']} — page: {k}")
            L.append(t.get("lede", t.get("desc", "")))
            if "list" in t: L.append("; ".join(t["list"]))
            if "groups" in t: L.append("; ".join(x for _, g in t["groups"] for x in g))
            for q, a in t.get("faq", []) + t.get("items", []): L.append(f"Q: {q} A: {a}")
    return "\n".join(L)
