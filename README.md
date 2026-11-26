# DEEP REKLAM — Web Sitesi

AI otomasyon odaklı, Türkçe (varsayılan) ve İngilizce, statik ve hızlı kurumsal web sitesi.

**Yayın adresi:** https://abdullahyilmz1722-pixel.github.io/Deep-Reklam-web-sitesi/

## Yapı

```
src/
  content.py   ← TÜM metinler (TR + EN). Metin değiştirmek için yalnızca bunu düzenleyin.
  build.py     ← Sayfaları, sitemap.xml, robots.txt, llms.txt ve 404 sayfasını üretir.
  check.py     ← Kırık bağlantı, H1, title/description/canonical kontrolü.
  assets/      ← style.css, app.js (demolar + formlar), logo ve görseller.
.github/workflows/deploy.yml ← main dalına her gönderimde derler, kontrol eder, gh-pages dalına yayınlar.
```

## Yerelde çalıştırma

```bash
python3 src/build.py          # _site/ klasörüne derler (ek paket gerekmez, Python 3.9+)
python3 src/check.py          # kontrol
python3 -m http.server 8000 -d _site   # http://localhost:8000
```

## Yayınlama

`main` dalına yapılan her `git push` sonrasında GitHub Actions siteyi derler ve `gh-pages` dalına yayınlar.
GitHub ayarı: **Settings → Pages → Build and deployment → Source: Deploy from a branch → `gh-pages` / `(root)`**.

### Kendi alan adınıza geçiş

1. **Settings → Secrets and variables → Actions → Variables** bölümüne ekleyin:
   - `SITE_URL` = `https://www.alanadiniz.com` (kanonik adresler, sitemap ve hreflang bunu kullanır)
   - `CUSTOM_DOMAIN` = `www.alanadiniz.com`
2. Alan adı sağlayıcınızda `www` için `CNAME → abdullahyilmz1722-pixel.github.io` kaydı açın.
3. **Settings → Pages → Custom domain** alanına alan adını yazıp **Enforce HTTPS** kutusunu işaretleyin.

### Formlar

Varsayılan olarak formlar sunucu gerektirmez: doğrulanan talep, düzenli bir WhatsApp mesajı olarak hazırlanır ve
ziyaretçi **WhatsApp'ta gönder**'e bastığında ulaşır. Site, gönderilmemiş bir mesaj için asla "gönderildi" demez.
Sunucu tarafı form kullanmak isterseniz (Formspree, Wix Velo HTTP fonksiyonu, n8n webhook vb.) Actions değişkeni
olarak `FORM_ENDPOINT` ekleyin; bu durumda yalnızca 2xx yanıtında başarı mesajı gösterilir. Gizli anahtarları asla bu
repoya yazmayın; GitHub Secrets veya Wix Secrets Manager kullanın.

## Dürüstlük kuralları

- Tüm AI demoları **Demo / Simülasyon** etiketlidir; gerçek API çağrısı yapmaz.
- Fiyat, sahte yorum, istatistik, referans veya sertifika yoktur. Portföy yalnızca gerçek ve onaylı işlerle doldurulmalıdır.
- KVKK, gizlilik ve çerez metinleri genel taslaktır; hukuki danışmanla gözden geçirilmelidir.

## Wix Studio sürümü

Wix Studio, dışarıdan HTML aktarmayı ve sayfa tasarımını API ile kurmayı desteklemez; sayfalar Wix editöründe kurulur.
Bu repodaki `content.py` metinleri, sayfa yapısı, renkler (`#0e0e0f`, `#a47a1e`, `#d4aa4f`) ve yazı tipleri (Sora, Inter)
Wix sürümü için kaynak olarak kullanılabilir. Wix'e özgü özellikler (Wix Forms, Wix CMS, Wix Multilingual) GitHub
sürümünde yoktur; buradaki karşılıkları statik sayfalar ve WhatsApp tabanlı formlardır.

## DEEP Asistan (sohbet botu)

Sağ alttaki asistan iki modda çalışır:

1. **Yerel mod (varsayılan, ücretsiz):** Tarayıcıda çalışır, `src/chatbot.py` ve `src/content.py`'den üretilen
   bilgi tabanıyla sohbet eder: ziyaretçi konu açana kadar yalnızca nasıl yardımcı olabileceğini sorar; konu açılınca
   adı bir kez sorar (ısrar etmez), 2-3 kısa soruyla bilgi toplar, sorulara cevap verir
   ve sonunda her şeyi içeren hazır bir WhatsApp mesajı sunar. Hiçbir veri sunucuya gönderilmez.
   Soru akışları: `src/chatbot.py` içindeki `FLOW`.
   Yeni soru-cevap eklemek için `src/chatbot.py` içindeki `intents` listesine satır ekleyin.
2. **Yapay zekâ modu:** `worker/` klasöründeki Cloudflare Worker, soruları Claude modeline gönderir.
   ```bash
   cd worker
   npx wrangler login
   npx wrangler secret put ANTHROPIC_API_KEY   # anahtar yalnızca Cloudflare'de saklanır
   npx wrangler deploy                          # çıktıdaki https://deep-asistan....workers.dev adresini kopyalayın
   ```
   Ardından GitHub'da **Settings → Secrets and variables → Actions → Variables** bölümüne
   `CHAT_ENDPOINT` = worker adresi ekleyin ve Actions'ı yeniden çalıştırın. Gizlilik politikası metni
   bu moda göre otomatik güncellenir. Yapay zekâ servisine ulaşılamazsa asistan yerel moda döner.
