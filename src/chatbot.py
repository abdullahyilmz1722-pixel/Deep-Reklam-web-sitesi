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
         ("how", "nasilsin nasilsiniz naber nasil gidiyor iyi misin", "", None),
         ("greet", "merhaba selam selamlar iyi gunler gunaydin iyi aksamlar hey sa", "Merhaba! Ben DEEP Asistan. AI otomasyon, tabela, tasarım, web sitesi, yazılım veya reklam hakkında ne öğrenmek istersiniz?", None),
         ("thanks", "tesekkurler tesekkur ederim sagol sag ol eyvallah", "Rica ederim! Başka bir sorunuz olursa buradayım. Projenizi konuşmak isterseniz WhatsApp'tan da yazabilirsiniz.", None),
         ("price", "fiyat fiyati ucret ucreti kac para ne kadar maliyet butce fiyatlar tutar paket", "Fiyatları projeye özel hazırlıyoruz, çünkü ölçü, kapsam, malzeme ve entegrasyon her işte farklı. İhtiyacınızı kısaca WhatsApp'tan ya da teklif formundan iletirseniz size net bir teklif sunarız.", "contact"),
         ("phone", "telefon telefonunuz numara numaraniz numaranizi gsm", f"Bize {ph} numarasından telefonla veya WhatsApp'tan ulaşabilirsiniz.", "contact"),
         ("location", "adres adresiniz nerede neredesiniz konum konumunuz yeriniz harita yol tarifi ofisiniz", "Konumumuzu Google Haritalar'daki işletme profilimizde görebilirsiniz. İletişim sayfasındaki 'Google Haritalar'da aç' bağlantısı sizi doğrudan oraya götürür.", "contact"),
         ("hours", "saat saatleri kacta acik kapali calisma saatleri mesai", "Güncel çalışma saatlerimizi Google işletme profilimizde görebilirsiniz. En hızlı yanıt için WhatsApp'tan yazabilirsiniz.", "contact"),
         ("human", "yetkili insan biriyle gorusmek temsilci canli destek sizi arasin geri donus", f"Elbette. Ekibimize WhatsApp'tan veya {ph} numarasından doğrudan ulaşabilirsiniz. Aşağıdaki butonla sorunuzu WhatsApp'a hazır mesaj olarak aktarabilirsiniz.", "contact"),
         ("bot", "sen kimsin bot musun yapay zeka misin insan misin", "Ben DEEP REKLAM web sitesinin otomatik asistanıyım. Sitedeki bilgilerle yanıt veriyorum. Kesin bilgi ve teklif için ekibimiz size dönüş yapar.", None),
         ("intl", "yurt disi yurtdisi ingilizce yabanci uluslararasi abroad", "Tasarım, yazılım, dijital pazarlama ve AI otomasyon hizmetlerini Türkiye geneline ve yurt dışına uzaktan veriyoruz. Çok dilli web siteleri de kuruyoruz. Tabela ve montaj gibi yerinde yapılan işler için bölgesel planlama yapıyoruz.", "about"),
         ("time", "ne kadar surer sure teslim kac gun zaman", "Süre işin kapsamına göre değişiyor. İhtiyacınızı öğrendiğimizde size teklifle birlikte net bir teslim süresi bildiriyoruz.", "contact"),
        ]
    return [
     ("how", "how are you how is it going hows going", "", None),
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

# ---------------------------------------------------------------- SOHBET AKIŞI
# Her grup: label, intro (ilk cümle), qs [(özet etiketi, soru)], tip (ilk cevaptan sonra verilen kısa bilgi)
FLOW = {
 "tr": {
  "greet": "Merhaba, hoş geldiniz! Ben DEEP Asistan, DEEP REKLAM'ın dijital asistanıyım. Size nasıl yardımcı olabilirim?",
  "idle": ["Size nasıl yardımcı olabilirim? Aklınızdaki konuyu yazmanız yeterli.", "Anladım. Yardımcı olabileceğim bir konu olursa buradayım."],
  "how": "Teşekkür ederim, iyiyim! Umarım siz de iyisinizdir. Size nasıl yardımcı olabilirim?",
  "greet_again": "Merhaba! Size nasıl yardımcı olabilirim?",
  "name_retry": "Size nasıl hitap edeyim? Adınızı yazmanız yeterli.",
  "name_first": "Memnuniyetle yardımcı olurum. Bu arada size nasıl hitap edeyim?",
  "nice": ["Memnun oldum {n}!", "Tanıştığımıza çok sevindim {n}.", "Hoş geldiniz {n}!"],
  "need": "Bugün size nasıl yardımcı olabilirim? Aklınızdaki projeyi ya da ihtiyacı kısaca anlatır mısınız?",
  "need_chips": ["Yapay zekâ / WhatsApp asistanı", "Tabela", "Web sitesi", "Logo ve tasarım", "Reklam ve sosyal medya", "Matbaa"],
  "need_unclear": "Tam anlayamadım, kusura bakmayın. Biraz daha açar mısınız? Örneğin tabela, web sitesi, reklam ya da WhatsApp'a cevap veren bir yapay zekâ asistanı gibi.",
  "ack": ["Anladım.", "Harika.", "Çok güzel.", "Tamam, not ettim.", "Süper.", "Anladım {n}.", "Teşekkürler {n}.", "Peki, anlaşıldı."],
  "skip_ack": "Hiç sorun değil, bunu ekibimiz sizinle birlikte netleştirir.",
  "q_unknown": "Güzel soru. Bunu ekibimiz size en doğru şekilde anlatır, sorunuzu WhatsApp mesajına da ekleyeceğim.",
  "thanks_mid": "Rica ederim!", "thanks_idle": "Rica ederim! Başka bir konuda yardımcı olabileceğim bir şey olursa buradayım.", "wa_first": "Talebim:",
  "resume": "Hazır olduğunuzda kaldığımız yerden devam edebiliriz: {q}",
  "summary": "Çok teşekkürler {n}, şimdi resmi daha iyi görüyorum. Özetle şöyle anladım:",
  "handoff": "Ekibimiz bu bilgilerle size özel bir öneri ve teklif hazırlayabilir. Aşağıdaki butona basınca bu özet WhatsApp'ta hazır gelir, siz gönderince ekibimiz size oradan döner. Başka merak ettiğiniz bir şey olursa sormaya devam edebilirsiniz, buradayım.",
  "wa_btn": "Özeti WhatsApp'tan gönder",
  "after": "Başka merak ettiğiniz bir şey var mı? Hizmetlerimiz, çalışma şeklimiz ya da aklınıza takılan herhangi bir konu olabilir.",
  "smalltalk": ["Anladım. Bu konuda yardımcı olabileceğim başka bir şey var mı?", "Tamam {n}. Aklınıza takılan başka bir şey olursa sorabilirsiniz."],
  "bye": "Rica ederim {n}, asıl ben teşekkür ederim. Görüşmek üzere, iyi günler!",
  "new_topic": "Tabii, bunu da konuşalım.",
  "sum_need": "İhtiyaç", "sum_name": "Ad",
  "wa_intro": "Merhaba DEEP REKLAM, ben {n}. Web sitenizdeki asistanla görüştüm, bilgilerim aşağıda:",
  "wa_intro_anon": "Merhaba DEEP REKLAM, web sitenizdeki asistanla görüştüm, bilgilerim aşağıda:",
  "services": "DEEP REKLAM olarak en çok yapay zekâ otomasyonu üzerine çalışıyoruz: WhatsApp ve Instagram'a cevap veren asistanlar, AI satış temsilcisi, randevu otomasyonu, sesli asistan ve iş akışı otomasyonu. Bunun yanında tabela ve açık hava reklamı, grafik tasarım, web sitesi, özel yazılım, dijital reklam, SEO, sosyal medya yönetimi ve matbaa hizmetleri de veriyoruz. Merak ettiğiniz bir konu varsa anlatabilirim.",
  "wa_qs": "Sohbette sorduğum konular:", "wa_page": "Görüştüğüm sayfa:",
  "wa_end": "Benim için öneri ve teklif hazırlayabilir misiniz? Teşekkürler.",
  "groups": {
   "ai": {"label": "Yapay zekâ otomasyonu", "intro": "Yapay zekâ otomasyonu tam bizim alanımız. Size en uygun kurguyu anlamak için birkaç kısa soru sorayım.",
          "qs": [("Sektör", "Hangi sektörde çalışıyorsunuz?"), ("Kanallar", "Müşterileriniz size en çok nereden ulaşıyor? WhatsApp, Instagram, telefon, web sitesi…"), ("En çok vakit alan iş", "Günlük işlerde en çok vaktinizi ne alıyor? Aynı soruları yanıtlamak, randevu ayarlamak, teklif takibi gibi…")],
          "tip": "Bu tür işletmelerde genelde ilk adım, gelen mesajları anında karşılayan ve talebi toparlayan bir asistan oluyor. Ekip de yalnızca hazır taleplerle ilgileniyor."},
   "signage": {"label": "Tabela / açık hava reklamı", "intro": "Tabela işini çok seviyoruz, güzel bir proje olacak gibi.",
          "qs": [("Yer", "Tabela dış cephe için mi, iç mekân için mi?"), ("Model", "Aklınızda bir model var mı? Kutu harf, ışıklı kasa, neon, totem… Kararsızsanız da sorun değil."), ("Ölçü ve konum", "Yaklaşık ölçüsü ve hangi şehir ya da ilçede olacağı? Keşif ve montajı planlamak için soruyorum.")],
          "tip": "Dış cephede gece de fark edilmek için ışıklı kutu harf çok tercih ediliyor. Ama en doğru seçimi keşifte, görüş mesafesine bakarak birlikte yapıyoruz."},
   "vehicle": {"label": "Araç kaplama / giydirme", "yes": "Evet, araç kaplama ve filo giydirme yapıyoruz; tasarımdan uygulamaya kadar tüm süreci biz yürütüyoruz.", "intro": "Araç giydirme markanızı her gün yola taşımanın en etkili yollarından biri.",
          "qs": [("Araçlar", "Kaç araç ve ne tür araçlar? Binek, kamyonet, kamyon…"), ("Kaplama türü", "Tam kaplama mı düşünüyorsunuz, yoksa logo ve iletişim bilgisi gibi kısmi bir giydirme mi?"), ("Tasarım ve konum", "Tasarımınız hazır mı, ve araçlar hangi şehirde?")],
          "tip": "Araç giydirmede okunabilirlik çok önemli: trafikte birkaç saniyede anlaşılan sade bir tasarım genelde en iyi sonucu veriyor."},
   "design": {"label": "Grafik tasarım", "intro": "Tasarım tarafında da size yardımcı olabiliriz.",
          "qs": [("Tasarım", "Ne tasarlatmak istiyorsunuz? Logo, kurumsal kimlik, katalog, menü, ambalaj…"), ("Sektör ve tarz", "Markanız hangi sektörde ve nasıl bir his vermesini istersiniz? Modern, lüks, samimi gibi…")],
          "tip": "İyi bir logo tabelada, kartvizitte ve sosyal medyada aynı netlikte okunabilmeli. Biz tasarlarken hepsini birlikte düşünüyoruz."},
   "web": {"label": "Web sitesi", "intro": "Web sitesi işini birlikte çok güzel planlarız.",
          "qs": [("Amaç", "Siteniz ne iş yapacak? Firmanızı tanıtmak mı, online satış mı, randevu almak mı?"), ("Mevcut site", "Şu an bir web siteniz var mı?"), ("Dil", "Site sadece Türkçe mi olsun, yoksa İngilizce gibi başka diller de olsun mu?")],
          "tip": "Ziyaretçilerin çoğu artık telefondan giriyor. Bu yüzden siteleri önce mobil için tasarlıyoruz."},
   "software": {"label": "Özel yazılım", "intro": "Özel yazılım tarafında süreçlerinize göre çözüm geliştiriyoruz.",
          "qs": [("Kolaylaşacak iş", "Yazılımla hangi işinizi kolaylaştırmak istiyorsunuz?"), ("Şu anki yöntem", "Bu işi şu an nasıl yürütüyorsunuz? Excel, kâğıt, başka bir program…")],
          "tip": "Çoğu zaman en verimli çözüm, alışkanlıklarınızı bozmadan işi tek ekrana toplamak oluyor."},
   "marketing": {"label": "Dijital reklam", "intro": "Reklam tarafında doğru kurguyla çok fark yaratılabiliyor.",
          "qs": [("Platform", "Hangi platformlarda reklam düşünüyorsunuz? Google, Instagram, TikTok…"), ("Hedef", "Reklamdan beklentiniz ne? Satış, telefon ya da mesaj almak, bilinirlik…")],
          "tip": "Reklamdan gelen mesajlara hızlı dönmek sonucu çok etkiliyor. Bunu bir AI asistanla birleştirebiliyoruz."},
   "seo": {"label": "SEO / Google görünürlüğü", "intro": "Google'da ve yapay zekâ aramalarında görünür olmak artık çok önemli.",
          "qs": [("Web sitesi", "Bir web siteniz var mı? Varsa adresini yazabilirsiniz."), ("Hedef bölge", "Hangi şehir ya da bölgede, hangi aramalarda görünmek istersiniz?")],
          "tip": "Yerel aramalarda Google İşletme Profili çok önemli. Çoğu zaman ilk iyileştirmeyi oradan yapıyoruz. Tabii kimse sıralama garantisi veremez, biz doğru altyapıyı kuruyoruz."},
   "social": {"label": "Sosyal medya yönetimi", "intro": "Sosyal medyada düzenli ve kaliteli içerik çok şey değiştiriyor.",
          "qs": [("Hesaplar", "Hangi hesaplar için düşünüyorsunuz? Instagram, TikTok, LinkedIn…"), ("İçerik üretimi", "Çekim ve tasarım gibi içerik üretimini de bizden mi istersiniz?")],
          "tip": "Mesajlara hızlı dönüş de sosyal medyanın bir parçası. İsterseniz DM'leri yanıtlayan bir AI asistanla birlikte kurgulayabiliriz."},
   "print": {"label": "Matbaa ve promosyon", "intro": "Baskı işlerinizi de tasarımdan teslimata kadar yönetebiliriz.",
          "qs": [("Ürün ve adet", "Ne bastırmak istiyorsunuz, yaklaşık kaç adet?"), ("Tasarım", "Tasarımınız hazır mı, yoksa tasarımı da biz mi yapalım?")],
          "tip": "Kurumsal kimliğinizle uyumlu baskılar markanızı çok daha profesyonel gösterir."},
   "other": {"label": "Diğer", "intro": "Elbette.",
          "qs": [("Detay", "Biraz daha anlatır mısınız, tam olarak ne yapmak istiyorsunuz?")], "tip": ""},
  },
 },
 "en": {
  "greet": "Hi, welcome! I'm DEEP Assistant, DEEP REKLAM's digital assistant. How can I help you?",
  "idle": ["How can I help you? Just tell me what's on your mind.", "Got it. I'm here if there's anything I can help with."],
  "how": "I'm doing well, thank you! I hope you are too. How can I help you?",
  "greet_again": "Hello! How can I help you?",
  "name_retry": "What should I call you? Just type your name.",
  "name_first": "Happy to help. By the way, what should I call you?",
  "nice": ["Nice to meet you, {n}!", "Great to meet you, {n}.", "Welcome, {n}!"],
  "need": "How can I help you today? Tell me briefly about the project or what you need.",
  "need_chips": ["AI / WhatsApp assistant", "Signage", "Website", "Logo and design", "Ads and social media", "Print"],
  "need_unclear": "Sorry, I didn't quite get that. Could you tell me a bit more? For example a sign, a website, ads, or an AI assistant that answers WhatsApp.",
  "ack": ["Got it.", "Great.", "Lovely.", "Okay, noted.", "Perfect.", "Got it, {n}.", "Thanks, {n}.", "Understood."],
  "skip_ack": "No problem at all, our team will work that out with you.",
  "q_unknown": "Good question. Our team will explain that properly, and I'll add your question to the WhatsApp message.",
  "thanks_mid": "You're welcome!", "thanks_idle": "You're welcome! If there's anything else I can help with, I'm here.", "wa_first": "My request:",
  "resume": "Whenever you're ready, we can pick up where we left off: {q}",
  "summary": "Thanks so much, {n}, I have a much clearer picture now. Here's what I understood:",
  "handoff": "Our team can prepare a tailored proposal and quote from this. Press the button below and this summary will open ready in WhatsApp; once you send it, our team will reply there. If anything else is on your mind, keep asking, I'm here.",
  "wa_btn": "Send summary on WhatsApp",
  "after": "Anything else you'd like to know? Our services, how we work, or anything at all.",
  "smalltalk": ["Got it. Is there anything else I can help with?", "Okay, {n}. Feel free to ask anything else."],
  "bye": "You're welcome, {n}, thank you! Talk soon, have a great day!",
  "new_topic": "Sure, let's talk about that too.",
  "sum_need": "Need", "sum_name": "Name",
  "wa_intro": "Hello DEEP REKLAM, I'm {n}. I chatted with the assistant on your website; my details are below:",
  "wa_intro_anon": "Hello DEEP REKLAM, I chatted with the assistant on your website; my details are below:",
  "services": "At DEEP REKLAM our main focus is AI automation: assistants that answer WhatsApp and Instagram, AI sales agents, booking automation, voice assistants and workflow automation. We also do signage and outdoor advertising, graphic design, websites, custom software, digital ads, SEO, social media management and print. Happy to tell you more about anything you're curious about.",
  "wa_qs": "Topics I asked about:", "wa_page": "Page I was on:",
  "wa_end": "Could you prepare a proposal and quote for me? Thank you.",
  "groups": {
   "ai": {"label": "AI automation", "intro": "AI automation is exactly our thing. Let me ask a few quick questions to understand the best setup for you.",
          "qs": [("Industry", "What industry are you in?"), ("Channels", "Where do customers reach you most? WhatsApp, Instagram, phone, website…"), ("Biggest time sink", "What takes most of your time day to day? Answering the same questions, booking appointments, following up on quotes…")],
          "tip": "For businesses like this, the first step is usually an assistant that greets messages instantly and gathers the request, so the team only handles ready-to-act leads."},
   "signage": {"label": "Signage / outdoor", "intro": "We love sign projects, this sounds like a good one.",
          "qs": [("Placement", "Is the sign for the facade or indoors?"), ("Type", "Do you have a type in mind? Channel letters, lightbox, neon, totem… It's fine if you're unsure."), ("Size and location", "Roughly what size, and which city or district? I'm asking to plan the survey and installation.")],
          "tip": "Illuminated channel letters are a popular choice for facades so you're visible at night. We decide the best option together during the site survey."},
   "vehicle": {"label": "Vehicle wrap", "yes": "Yes, we do vehicle wraps and fleet branding, handling everything from design to application.", "intro": "A vehicle wrap is one of the most effective ways to take your brand on the road every day.",
          "qs": [("Vehicles", "How many vehicles, and what type? Cars, vans, trucks…"), ("Wrap type", "Full wrap, or partial branding like a logo and contact details?"), ("Design and location", "Is your design ready, and which city are the vehicles in?")],
          "tip": "Readability matters most on vehicles: a simple design that's understood in a few seconds in traffic usually works best."},
   "design": {"label": "Graphic design", "intro": "We can help on the design side too.",
          "qs": [("Design", "What would you like designed? Logo, brand identity, catalogue, menu, packaging…"), ("Industry and style", "What industry is your brand in, and what feel do you want? Modern, premium, friendly…")],
          "tip": "A good logo should read just as clearly on a sign, a business card and social media. We design with all of them in mind."},
   "web": {"label": "Website", "intro": "We'll plan a great website together.",
          "qs": [("Purpose", "What should the site do? Introduce your company, sell online, take bookings?"), ("Current site", "Do you have a website right now?"), ("Languages", "Turkish only, or other languages like English too?")],
          "tip": "Most visitors now come from their phones, so we design mobile-first."},
   "software": {"label": "Custom software", "intro": "We build custom software around your processes.",
          "qs": [("Process", "Which part of your work would you like software to make easier?"), ("Current method", "How do you handle it today? Spreadsheets, paper, another program…")],
          "tip": "Often the best solution is bringing the work onto one screen without breaking your habits."},
   "marketing": {"label": "Digital ads", "intro": "The right ad setup can make a big difference.",
          "qs": [("Platforms", "Which platforms are you considering? Google, Instagram, TikTok…"), ("Goal", "What do you want from ads? Sales, calls or messages, awareness…")],
          "tip": "Replying fast to ad leads makes a big difference, and we can combine that with an AI assistant."},
   "seo": {"label": "SEO / Google visibility", "intro": "Being visible on Google and in AI search really matters now.",
          "qs": [("Website", "Do you have a website? If so, feel free to share the address."), ("Target area", "Which city or region, and which searches do you want to show up for?")],
          "tip": "For local searches your Google Business Profile matters a lot, so that's often where we start. No one can guarantee rankings; we build the right foundation."},
   "social": {"label": "Social media management", "intro": "Regular, quality content changes a lot on social media.",
          "qs": [("Accounts", "Which accounts are you thinking of? Instagram, TikTok, LinkedIn…"), ("Content production", "Would you like us to handle content production too, like shoots and design?")],
          "tip": "Fast replies are part of social media too. We can pair it with an AI assistant that answers DMs."},
   "print": {"label": "Print and promotion", "intro": "We can manage your print work from design to delivery.",
          "qs": [("Item and quantity", "What would you like printed, and roughly how many?"), ("Design", "Is your design ready, or should we design it too?")],
          "tip": "Print that matches your brand identity makes your business look much more professional."},
   "other": {"label": "Other", "intro": "Of course.",
          "qs": [("Details", "Could you tell me a bit more about what you'd like to do?")], "tip": ""},
  },
 },
}
GROUP_OF = {"ai": "ai", "whatsapp": "ai", "sales": "ai", "support": "ai", "voice": "ai", "agents": "ai", "workflow": "ai",
            "signage": "signage", "design": "design", "web": "web", "software": "software", "marketing": "marketing", "seo": "seo", "social": "social", "print": "print"}
for _l in ("tr", "en"):
    UI[_l]["flow"] = FLOW[_l]; UI[_l]["group_of"] = GROUP_OF
