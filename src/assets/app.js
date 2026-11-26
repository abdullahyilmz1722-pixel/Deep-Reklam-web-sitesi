/* DEEP REKLAM — arayüz ve demo simülasyonları. Tüm demolar senaryoludur; gerçek API çağrısı yapmaz. */
{
const D = window.DR || {lang:'tr', ui:{}}, TR = D.lang === 'tr', $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const sleep = ms => new Promise(r => setTimeout(r, RM ? Math.min(ms, 120) : ms));
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

/* ---------- navigasyon */
const hd = $('.hd'), bg = $('.burger');
bg && bg.addEventListener('click', () => { document.documentElement.style.setProperty('--hh', hd.offsetHeight + 'px'); const o = hd.classList.toggle('open'); bg.setAttribute('aria-expanded', o); document.body.style.overflow = o ? 'hidden' : ''; });
$$('.dd-t').forEach(b => b.addEventListener('click', () => { const li = b.parentElement, o = li.classList.toggle('on'); b.setAttribute('aria-expanded', o); }));
document.addEventListener('keydown', ev => { if (ev.key === 'Escape' && hd && hd.classList.contains('open')) bg.click(); });
$$('#nav a').forEach(a => a.addEventListener('click', () => { if (hd.classList.contains('open')) bg.click(); }));

/* ---------- demo çerçevesi: görünür olunca başlar, "tekrar oynat" ile yeniden başlar */
const RUN = {};
function boot(fig) {
  const kind = fig.dataset.demo, body = $('.demo-body', fig); let token = 0;
  const start = () => { token++; const my = token; body.innerHTML = ''; RUN[kind] && RUN[kind](body, () => my !== token, fig); };
  $('.replay', fig) && $('.replay', fig).addEventListener('click', start);
  const io = new IntersectionObserver(es => { if (es[0].isIntersecting) { io.disconnect(); start(); } }, {threshold: .25});
  io.observe(fig);
}

/* ---------- WhatsApp AI sohbet simülasyonu */
const CHAT = TR ? {
  head: ['DEEP REKLAM Asistan', 'AI asistan · çevrimiçi'],
  intro: [['u', 'Merhaba, dükkânım için ışıklı tabela yaptırmak istiyorum.'], ['a', 'Merhaba, hoş geldiniz! Size yardımcı olayım. Tabela cephede mi olacak, iç mekânda mı?'], ['u', 'Cephede, yaklaşık 4 metre.'], ['a', 'Teşekkürler. Kutu harf mi, ışıklı kasa mı düşünüyorsunuz? Kararsızsanız farkını anlatabilirim.']],
  q: ['Farkını anlat', 'Kutu harf', 'Keşif istiyorum'],
  b: [
    [['a', 'Kutu harfte harfler tek tek üretilir; daha prestijli ve derinlikli görünür. Işıklı kasa tek panel olduğu için daha hızlı üretilir. Fiyat; ölçü ve malzemeye göre ekibimizce hazırlanır.'], ['a', 'Keşif ve ölçü için uygun olduğunuz bir gün var mı?'], ['u', 'Perşembe öğleden sonra olur.'], ['a', 'Not aldım. Ekibimiz sizi arayıp keşif saatini kesinleştirecek.']],
    [['a', 'Güzel seçim. Logonuzu buradan gönderirseniz tasarım ekibimiz cephe görselini hazırlasın.'], ['u', '[logo.png gönderildi]'], ['a', 'Logonuz alındı. Ölçü ve malzeme önerisiyle birlikte ekibimiz size dönüş yapacak.']],
    [['a', 'Elbette. Adınızı ve uygun gününüzü yazar mısınız?'], ['u', 'Mehmet, perşembe öğleden sonra.'], ['a', 'Teşekkürler Mehmet Bey. Keşif talebiniz oluşturuldu, ekibimiz saat için sizi arayacak.']]],
  end: 'Talep özeti ekibe iletildi · CRM’e kaydedildi'
} : {
  head: ['DEEP REKLAM Assistant', 'AI assistant · online'],
  intro: [['u', 'Hi, I need an illuminated sign for my shop.'], ['a', 'Hello and welcome! Happy to help. Will the sign go on the facade or indoors?'], ['u', 'On the facade, about 4 metres.'], ['a', 'Thanks. Are you thinking of channel letters or a lightbox? I can explain the difference if you like.']],
  q: ['Explain the difference', 'Channel letters', 'Book a site visit'],
  b: [
    [['a', 'Channel letters are made one by one and look more premium, with depth. A lightbox is a single panel, so it’s quicker to produce. Pricing is prepared by our team based on size and materials.'], ['a', 'Is there a day that suits you for a site survey?'], ['u', 'Thursday afternoon works.'], ['a', 'Noted. Our team will call you to confirm the survey time.']],
    [['a', 'Great choice. Send your logo here and our design team will prepare a facade visual.'], ['u', '[logo.png sent]'], ['a', 'Logo received. Our team will get back to you with size and material suggestions.']],
    [['a', 'Of course. Could you share your name and a day that suits you?'], ['u', 'Michael, Thursday afternoon.'], ['a', 'Thanks, Michael. Your survey request is created and our team will call to set a time.']]],
  end: 'Summary sent to the team · saved to CRM'
};
RUN.chat = async (body, dead) => {
  body.innerHTML = `<div class="chat-h"><span class="av">AI</span><span><b>${esc(CHAT.head[0])}</b><small>${esc(CHAT.head[1])}</small></span></div><div class="msgs"></div><div class="qr"></div>`;
  const box = $('.msgs', body), qr = $('.qr', body);
  const add = (who, t) => { const d = document.createElement('div'); d.className = 'm ' + who; d.textContent = t; box.appendChild(d); box.scrollTop = box.scrollHeight; return d; };
  const say = async ([who, t]) => { if (dead()) return; if (who === 'a') { const ty = add('t', ''); ty.innerHTML = '<i></i><i></i><i></i>'; await sleep(900 + t.length * 12); ty.remove(); } else await sleep(700); if (!dead()) add(who, t); };
  for (const m of CHAT.intro) { await say(m); await sleep(500); }
  if (dead()) return;
  const pick = await new Promise(res => {
    CHAT.q.forEach((q, i) => { const b = document.createElement('button'); b.type = 'button'; b.textContent = q; b.onclick = () => res(i); qr.appendChild(b); });
    setTimeout(() => res(-1), RM ? 400 : 7000);
  });
  if (dead()) return;
  const i = pick < 0 ? 0 : pick; qr.innerHTML = ''; add('u', CHAT.q[i]);
  for (const m of CHAT.b[i]) { await say(m); await sleep(450); }
  if (!dead()) { await sleep(500); add('s', CHAT.end); }
};

/* ---------- AI satış temsilcisi: lead nitelendirme */
const SALES = TR ? {rows: [['Kaynak', 'Instagram reklamı'], ['İhtiyaç', 'Araç giydirme · 3 araç'], ['Zaman', '2 hafta içinde'], ['Karar verici', 'Firma sahibi'], ['Bütçe', 'Belirlendi']], score: 'Satışa yakınlık', hot: 'Sıcak talep', out: 'Satış ekibine öncelikli iletildi · teklif taslağı hazırlandı · 2 gün sonra hatırlatma planlandı'}
 : {rows: [['Source', 'Instagram ad'], ['Need', 'Vehicle wrap · 3 vehicles'], ['Timing', 'Within 2 weeks'], ['Decision maker', 'Business owner'], ['Budget', 'Confirmed']], score: 'Sales readiness', hot: 'Hot lead', out: 'Routed to sales as priority · quote draft prepared · reminder scheduled in 2 days'};
RUN.sales = async (body, dead) => {
  body.innerHTML = `<div class="sl">${SALES.rows.map(r => `<div class="sl-row"><span>${esc(r[0])}</span><b>${esc(r[1])}</b></div>`).join('')}<div class="sl-row"><span>${esc(SALES.score)}</span><b class="sc">—</b></div><div class="score"><i></i></div><div class="sl-out">${esc(SALES.out)}</div></div>`;
  const rows = $$('.sl-row', body), bar = $('.score i', body), sc = $('.sc', body);
  for (let i = 0; i < rows.length - 1; i++) { await sleep(900); if (dead()) return; rows[i].classList.add('on'); bar.style.width = ((i + 1) / (rows.length - 1) * 84) + '%'; }
  await sleep(700); if (dead()) return; rows[rows.length - 1].classList.add('on'); sc.textContent = SALES.hot;
  await sleep(600); if (!dead()) $('.sl-out', body).classList.add('on');
};

/* ---------- randevu ve rezervasyon */
RUN.booking = async (body, dead) => {
  const loc = TR ? 'tr-TR' : 'en-GB', days = [], d = new Date();
  while (days.length < 5) { d.setDate(d.getDate() + 1); if (d.getDay() % 6) days.push(new Date(d)); }
  const slots = ['10:00', '11:30', '13:00', '14:30', '16:00'], taken = [1, 3];
  const L = TR ? {d: '1. Gün seçin', s: '2. Saat seçin', ok: ['Randevu talebi alındı', 'Takvime işlendi (ekip onayı bekleniyor)', 'Hatırlatma planlandı: 1 gün önce WhatsApp mesajı']} : {d: '1. Choose a day', s: '2. Choose a time', ok: ['Booking request received', 'Added to calendar (awaiting team confirmation)', 'Reminder scheduled: WhatsApp message 1 day before']};
  body.innerHTML = `<div class="bk"><h4>${L.d}</h4><div class="days">${days.map((x, i) => `<button type="button" aria-pressed="false" data-i="${i}">${esc(x.toLocaleDateString(loc, {weekday: 'short', day: 'numeric', month: 'short'}))}</button>`).join('')}</div><h4>${L.s}</h4><div class="slots">${slots.map((s, i) => `<button type="button" aria-pressed="false" ${taken.includes(i) ? 'disabled' : ''} data-i="${i}">${s}</button>`).join('')}</div><div class="bk-out msgs" style="height:auto;background:none;padding:0"></div></div>`;
  let day = null, slot = null, auto = true;
  const out = $('.bk-out', body);
  const done = async () => { out.innerHTML = ''; const lbl = `${$$('.days button', body)[day].textContent} · ${slots[slot]}`; const m = document.createElement('div'); m.className = 'm u'; m.textContent = lbl; out.appendChild(m);
    for (const t of L.ok) { await sleep(650); if (dead()) return; const x = document.createElement('div'); x.className = 'm s'; x.textContent = t; out.appendChild(x); } };
  const press = (grp, i) => { $$(grp + ' button', body).forEach(b => b.setAttribute('aria-pressed', b.dataset.i == i)); };
  $$('.days button', body).forEach(b => b.onclick = () => { auto = false; day = +b.dataset.i; press('.days', day); if (slot != null) done(); });
  $$('.slots button', body).forEach(b => b.onclick = () => { auto = false; slot = +b.dataset.i; press('.slots', slot); if (day == null) { day = 0; press('.days', 0); } done(); });
  await sleep(3500); if (dead() || !auto) return; day = 1; press('.days', 1); await sleep(900); if (dead() || !auto) return; slot = 2; press('.slots', 2); done();
};

/* ---------- sesli asistan */
const VOICE = TR ? [['c', 'Arayan', 'Merhaba, yarın için araç kaplama randevusu almak istiyorum.'], ['a', 'AI asistan', 'Merhaba, ben DEEP REKLAM’ın yapay zekâ asistanıyım. Kaç araç için düşünüyorsunuz?'], ['c', 'Arayan', 'İki ticari araç.'], ['a', 'AI asistan', 'Not aldım. Yarın saat 11:00 ve 15:00 uygun görünüyor, hangisi size uyar?'], ['c', 'Arayan', '15:00 olsun.'], ['a', 'AI asistan', 'Talebinizi oluşturdum. Ekibimiz onay için size WhatsApp’tan yazacak. İyi günler!'], ['s', 'Sistem', 'Görüşme özeti WhatsApp’a ve CRM’e gönderildi.']]
 : [['c', 'Caller', 'Hi, I’d like to book a vehicle wrap appointment for tomorrow.'], ['a', 'AI assistant', 'Hello, I’m DEEP REKLAM’s AI assistant. How many vehicles is it for?'], ['c', 'Caller', 'Two vans.'], ['a', 'AI assistant', 'Noted. Tomorrow at 11:00 or 15:00 looks available — which suits you?'], ['c', 'Caller', '15:00, please.'], ['a', 'AI assistant', 'Your request is created. Our team will message you on WhatsApp to confirm. Have a good day!'], ['s', 'System', 'Call summary sent to WhatsApp and the CRM.']];
RUN.voice = async (body, dead) => {
  body.innerHTML = `<div class="vc idle"><div class="wave">${'<i></i>'.repeat(24)}</div><div class="tr"></div></div>`;
  $$('.wave i', body).forEach((w, i) => w.style.animationDelay = (i * 0.07 % 1.1) + 's');
  const vc = $('.vc', body), tr = $('.tr', body);
  for (const [w, who, t] of VOICE) { vc.classList.remove('idle'); await sleep(600 + t.length * 18); if (dead()) return; const p = document.createElement('p'); if (w === 'c') p.className = 'c'; p.innerHTML = `<b>${esc(who)}</b>${esc(t)}`; tr.appendChild(p); if (tr.children.length > 4) tr.firstChild.remove(); vc.classList.add('idle'); await sleep(350); }
};

/* ---------- çoklu ajanlar */
const AG = TR ? {st: ['Bekliyor', 'Çalışıyor…', 'Tamamlandı'], a: [['Karşılama ajanı', 'Müşteri iletişimi', 'Instagram’dan gelen fuar standı talebini aldı, ihtiyacı netleştirdi.'], ['Araştırma ajanı', 'Analiz', 'Fuarın tarihini, alan ölçülerini ve benzer stand örneklerini derledi.'], ['Teklif ajanı', 'Operasyon', 'Kapsam ve malzeme listesiyle teklif taslağını hazırladı.'], ['Rapor ajanı', 'Raporlama', 'Özeti ekibe iletti. Teklif, gönderim öncesi insan onayı bekliyor.']]}
 : {st: ['Waiting', 'Working…', 'Done'], a: [['Intake agent', 'Customer communication', 'Received a trade show stand request from Instagram and clarified the need.'], ['Research agent', 'Analysis', 'Gathered the show dates, booth size and similar stand examples.'], ['Quote agent', 'Operations', 'Prepared a quote draft with scope and materials.'], ['Report agent', 'Reporting', 'Sent the summary to the team. The quote awaits human approval before sending.']]};
RUN.agents = async (body, dead) => {
  body.innerHTML = `<div class="ag">${AG.a.map(a => `<div class="agc"><h4>${esc(a[0])}</h4><small>${esc(a[1])}</small><p></p><span class="st">${AG.st[0]}</span></div>`).join('')}</div>`;
  const cs = $$('.agc', body);
  for (let i = 0; i < cs.length; i++) { if (dead()) return; cs[i].classList.add('on'); $('.st', cs[i]).textContent = AG.st[1]; await sleep(1500); if (dead()) return; $('p', cs[i]).textContent = AG.a[i][2]; cs[i].classList.replace('on', 'done'); $('.st', cs[i]).textContent = AG.st[2]; await sleep(400); }
};

$$('[data-demo]').forEach(boot);

/* ---------- harita: tıklayınca yüklenir */
$$('.map').forEach(m => { const b = $('button', m); b && b.addEventListener('click', () => { m.innerHTML = `<iframe src="${esc(m.dataset.src)}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Google Maps"></iframe>`; }); });

/* ---------- formlar */
$$('form.lead').forEach(f => {
  const err = $('.ferr', f), ready = $('.fready', f), ok = $('.fok', f), sub = $('button[type=submit]', f);
  const tabTxt = () => { const r = $('input[name=ftype]:checked', f); return r ? r.nextElementSibling.textContent : ''; };
  $$('input[name=ftype]', f).forEach(r => r.addEventListener('change', () => { if (r.value === '1') f.topic.selectedIndex = 0; }));
  f.addEventListener('input', ev => ev.target.classList.remove('bad'));
  f.addEventListener('submit', async ev => {
    ev.preventDefault(); err.hidden = true; ok.hidden = true;
    if (f.website.value) return;                       // bot tuzağı
    const clean = s => s.replace(/[\u0000-\u001f\u007f<>]/g, ' ').replace(/\s+/g, ' ').trim();
    const v = {type: tabTxt(), name: clean(f.name.value), company: clean(f.company.value), phone: clean(f.phone.value), email: clean(f.email.value), topic: f.topic.value, msg: f.msg.value.replace(/[<>]/g, '').trim()};
    const bad = [];
    if (v.name.length < 2) bad.push(f.name);
    if (!/^[0-9 +()\-]{7,20}$/.test(v.phone)) bad.push(f.phone);
    if (v.email && !/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.email)) bad.push(f.email);
    if (v.msg.length < 5) bad.push(f.msg);
    if (!f.kvkk.checked) bad.push(f.kvkk);
    if (bad.length) { bad.forEach(x => x.classList.add('bad')); err.textContent = D.ui.f_err; err.hidden = false; bad[0].focus(); return; }
    sub.disabled = true; setTimeout(() => sub.disabled = false, 8000);   // tekrar gönderim sınırı
    const L = TR ? ['Talep türü', 'Ad soyad', 'Firma', 'Telefon', 'E-posta', 'Konu', 'Mesaj'] : ['Request type', 'Name', 'Company', 'Phone', 'Email', 'Topic', 'Message'];
    const vals = [v.type, v.name, v.company, v.phone, v.email, v.topic, v.msg];
    const text = D.ui.f_wa_head + '\n\n' + L.map((l, i) => vals[i] ? `${l}: ${vals[i]}` : '').filter(Boolean).join('\n');
    if (D.endpoint) {                                   // isteğe bağlı sunucu tarafı gönderim: yalnızca 2xx yanıtında başarı gösterilir
      try { const r = await fetch(D.endpoint, {method: 'POST', headers: {'Content-Type': 'application/json', 'Accept': 'application/json'}, body: JSON.stringify(v)}); if (r.ok) { ok.textContent = D.ui.f_ok; ok.hidden = false; f.reset(); return; } } catch (_) {}
      ok.textContent = D.ui.f_fail; ok.hidden = false;
    }
    $('.fprev', f).textContent = text;
    $('.fwa', f).href = `https://wa.me/${D.wa}?text=${encodeURIComponent(text)}`;
    ready.hidden = false; ready.scrollIntoView({behavior: RM ? 'auto' : 'smooth', block: 'center'});
  });
  const cp = $('.fcopy', f);
  cp && cp.addEventListener('click', async () => { try { await navigator.clipboard.writeText($('.fprev', f).textContent); cp.textContent = D.ui.f_copied; } catch (_) {} });
});
}

/* ---------- DEEP Asistan: sohbet eden asistan
   Yerel mod: tarayıcıda çalışır; tanışır, ihtiyacı sorar, kısa sorularla bilgi toplar, sorulara cevap verir,
   sonunda özeti WhatsApp'a hazır mesaj olarak sunar. Hiçbir veri sunucuya gönderilmez (sohbet sadece bu sekmede tutulur).
   CHAT_ENDPOINT tanımlıysa: sohbet sunucu tarafı yapay zekâyla yürür; hata olursa yerel moda döner. */
{
const D = window.DR || {}, C = D.chat, fab = document.querySelector('.cb-fab');
if (C && fab) {
const $ = (s, r = document) => r.querySelector(s), ROOT = D.root || '', TR = D.lang === 'tr', F_ = C.flow, G = F_.groups;
const RM = matchMedia('(prefers-reduced-motion: reduce)').matches;
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const MAP = {'ç':'c','ğ':'g','ı':'i','ö':'o','ş':'s','ü':'u','â':'a','î':'i','û':'u'};
const norm = s => String(s).toLocaleLowerCase('tr').replace(/[çğıöşüâîû]/g, c => MAP[c]).replace(/[^a-z0-9\s]/g, ' ');
const STOP = new Set(('ve ile bir bu su o da de mi mu mi midir ben biz siz sen icin gibi ama veya ya ne nasil hangi var yok mu ki cok daha en her olarak olan istiyorum isterim lazim bana bize size hakkinda bilgi almak yapiyor musunuz yapar misiniz musunuz misiniz neler nedir yapmak yaptirmak veriyor veriyorsunuz verir yapiyorsunuz sistem sistemi deep firma evet hayir tamam ' +
  'the a an and or of to for in on with is are do does doing make you your we our i me my can could would what how which about please want need have has it this that system offer provide yes no ok').split(' '));
const NOTNAME = new Set('merhaba selam selamlar sa hey hi hello tesekkurler sagol tamam evet hayir ok peki iyi yok var bilmiyorum'.split(' '));
const toks = s => norm(s).replace(/deep\s+reklam/g, ' ').split(/\s+/).filter(t => t.length > 1 && !STOP.has(t));
const hit = (q, e) => { if (q === e) return true; let i = 0; const n = Math.min(q.length, e.length); while (i < n && q[i] === e[i]) i++; return (i === n && n >= 4) || i >= 5; };
let lastPick = '';
const pick = a => { let x, k = 0; do { x = a[Math.floor(Math.random() * a.length)]; } while (x === lastPick && k++ < 5); lastPick = x; return x; };
const short = (s, n = 2) => (s.match(/[^.!?]+[.!?]+/g) || [s]).slice(0, n).join(' ').trim();
let KB = null;
const loadKB = () => KB ? Promise.resolve(KB) : fetch(ROOT + 'assets/kb-' + D.lang + '.json?v=' + (D.ver || '')).then(r => r.json()).then(j => KB = j.map(x => ({...x, tt: toks(x.t), kt: toks(x.k)}))).catch(() => KB = []);
function rank(q) {
  const qt = toks(q); if (!qt.length || !KB) return [];
  return KB.map(x => { let s = 0; for (const t of qt) s += x.tt.some(e => hit(t, e)) ? 1.5 : x.kt.some(e => hit(t, e)) ? 1 : 0; return {x, s: s * x.w + (s > 0 && x.id.startsWith('p-') ? 0.6 : 0)}; })
    .filter(r => r.s >= 1).sort((a, b) => b.s - a.s);
}
const isQ = t => /\?\s*$/.test(t) || /^(ne|neden|nasil|kac|hangi|nerede|nereden|kim|niye|what|how|why|where|when|which|who|do|does|can|could|is|are|will)\b/.test(norm(t).trim()) || /\b(mi|mu|misiniz|musunuz|miyim|muyum|miyiz|mudur|midir)\b/.test(norm(t));
const VEH = /\b(arac|araclar|araci|aracimi|araclarimi)\b.*\b(kapla|giydir|folyo)|\b(kapla\w*|giydir\w*)\b.*\barac|\bfilo\b|\b(wrap|wraps|wrapping|branding)\b.*\b(vans?|cars?|trucks?|vehicles?|fleet)\b|\b(vans?|cars?|trucks?|vehicles?)\b.*\bwrap|\bfleet\b/;
let lastT = '';
const groupOf0 = r => { for (const o of r) { const m = o.x.id.match(/^[pg]-(.+)$/); if (m && C.group_of[m[1]]) return {g: C.group_of[m[1]], s: o.s, key: m[1]}; } return null; };
const groupOf = r => { if (VEH.test(norm(lastT))) return {g: 'vehicle', s: 3, key: 'signage'}; return groupOf0(r); };
const intentOf = (r, ids) => r.find(o => ids.includes(o.x.id) && o.s >= 1.6);
const cap = w => w.charAt(0).toLocaleUpperCase('tr') + w.slice(1).toLocaleLowerCase('tr');
function nameFrom(t) {
  const m = t.match(/(?:ad[ıi]m|ismim|ben(?:im ad[ıi]m)?|my name is|i am|i'm|this is|call me)\s+([A-Za-zÇĞİÖŞÜçğıöşü]{2,20})/i);
  if (m) return cap(m[1]);
  const w = t.trim().replace(/[.!,]+$/, '').split(/\s+/);
  if (w.length <= 3 && w.every(x => /^[A-Za-zÇĞİÖŞÜçğıöşü]{2,20}$/.test(x)) && !STOP.has(norm(w[0]).trim()) && !NOTNAME.has(norm(w[0]).trim())) return cap(w[0]);
  return null;
}

/* durum: sekme açık kaldıkça korunur, sunucuya gitmez */
let S = {step: 'start', name: '', g: '', qi: 0, ans: [], unclear: 0, tip: false, log: [], hist: [], done: false, asked: [], first: ''};
try { const s = sessionStorage.getItem('dr-chat2-' + D.lang); if (s) S = {...S, ...JSON.parse(s)}; } catch (_) {}
const save = () => { try { sessionStorage.setItem('dr-chat2-' + D.lang, JSON.stringify({...S, log: S.log.slice(-60), hist: S.hist.slice(-20)})); } catch (_) {} };
const fill = s => s.replace(/\{n\}/g, S.name || '').replace(/\s+([.!?,])/g, '$1').replace(/\s{2,}/g, ' ').trim();

const box = document.createElement('div');
box.className = 'cb'; box.hidden = true; box.setAttribute('role', 'dialog'); box.setAttribute('aria-label', C.title);
box.innerHTML = `<div class="cb-h"><span class="cb-av">AI</span><span class="cb-ht"><b>${esc(C.title)}</b><small>${esc(C.endpoint ? C.sub_ai : C.sub_local)}</small></span><button type="button" class="cb-x" aria-label="${esc(C.close)}">×</button></div>
<div class="cb-m" aria-live="polite"></div><div class="cb-c"></div>
<form class="cb-f"><label class="sr" for="cb-in">${esc(C.ph)}</label><input id="cb-in" autocomplete="off" maxlength="500" placeholder="${esc(C.ph)}"><button type="submit" aria-label="${esc(C.send)}"><svg viewBox="0 0 24 24" class="ic" aria-hidden="true"><path d="M4 12l16-8-6 16-2-7z"/></svg></button></form>
<p class="cb-n">${esc(C.note)}</p>`;
document.body.appendChild(box);
const M = $('.cb-m', box), CH = $('.cb-c', box), FM = $('.cb-f', box), IN = $('#cb-in', box);

function draw(item) {
  if (item.k === 'b') { const d = document.createElement('div'); d.className = 'cb-b ' + item.w; d.textContent = item.t; M.appendChild(d); }
  else { const d = document.createElement('div'); d.className = 'cb-a'; d.innerHTML = item.l.map(l => `<a ${l.wa ? 'class="wa" target="_blank" rel="noopener"' : ''} href="${esc(l.wa ? l.u : ROOT + l.u)}">${esc(l.t)}</a>`).join(''); M.appendChild(d); }
  M.scrollTop = M.scrollHeight;
}
const push = item => { S.log.push(item); draw(item); save(); };
const sleep = ms => new Promise(r => setTimeout(r, RM ? 80 : ms));
async function say(t, typing = true) {
  t = fill(t); if (!t) return;
  if (typing) { const d = document.createElement('div'); d.className = 'cb-b a t'; d.innerHTML = '<i></i><i></i><i></i>'; M.appendChild(d); M.scrollTop = M.scrollHeight; await sleep(Math.min(1700, 450 + t.length * 14)); d.remove(); }
  push({k: 'b', w: 'a', t}); S.hist.push({role: 'assistant', content: t});
}
const links = l => push({k: 'l', l});
const chips = arr => { CH.innerHTML = (arr || []).map(c => `<button type="button">${esc(c)}</button>`).join(''); CH.querySelectorAll('button').forEach(b => b.onclick = () => send(b.textContent)); };
const waUrl = text => `https://wa.me/${D.wa}?text=${encodeURIComponent(text)}`;
const curQ = () => G[S.g].qs[S.qi][1];

function waMessage() {  // WhatsApp'ta gönderilecek eksiksiz hazır mesaj
  const L = [S.name ? fill(F_.wa_intro) : F_.wa_intro_anon, ''];
  if (G[S.g]) L.push(`${F_.sum_need}: ${G[S.g].label}`);
  if (S.first) L.push(`${F_.wa_first} ${S.first}`);
  S.ans.filter(a => a[1] !== '-').forEach(a => L.push(`• ${a[0]}: ${a[1]}`));
  if (S.asked.length) { L.push('', F_.wa_qs); S.asked.slice(-5).forEach(q => L.push('• ' + q)); }
  L.push('', `${F_.wa_page} ${document.title.split('|')[0].trim()}`, '', F_.wa_end);
  return L.join('\n');
}
function summaryText() {
  const L = [...(S.name ? [`${F_.sum_name}: ${S.name}`] : []), `${F_.sum_need}: ${G[S.g] ? G[S.g].label : '-'}`];
  S.ans.filter(a => a[1] !== '-').forEach(a => L.push(`${a[0]}: ${a[1]}`));
  return L;
}
async function startGroup(g) {
  S.g = g; S.qi = 0; S.ans = []; S.tip = false; S.step = 'q'; save();
  await say(G[g].intro); await say(curQ());
}
async function finish() {
  S.step = 'done'; S.done = true; save();
  const lines = summaryText();
  await say(F_.summary + '\n• ' + lines.join('\n• '));
  await say(F_.handoff);
  links([{wa: 1, u: waUrl(waMessage()), t: F_.wa_btn}]);
}
async function answerQuestion(t, r) {  // sitedeki bilgiyle kısa cevap; true dönerse cevaplandı
  const top = r[0]; if (!top || top.s < 1.6) return false;
  await say(short(top.x.a, 3));
  if (S.step === 'done' && top.x.u && top.x.id.startsWith('p-')) links([{u: top.x.u, t: (top.x.t || C.go) + ' →'}]);
  return true;
}

async function local(t) {
  await loadKB();
  lastT = t; const r = rank(t);
  if (isQ(t)) { S.asked.push(t.slice(0, 160)); save(); }
  if (/(\+?\d[\d\s()-]{8,}\d)/.test(t)) { await say(C.phone_note); links([{wa: 1, u: waUrl(C.wa_head + '\n' + t), t: C.wa}]); if (S.step === 'q') await say(fill(F_.resume.replace('{q}', curQ().charAt(0).toLocaleLowerCase('tr') + curQ().slice(1)))); return; }
  const human = intentOf(r, ['i-human', 'i-phone']), gg = groupOf(r);
  if (human && (!gg || human.s > gg.s)) { await say(human.x.a); links([{wa: 1, u: waUrl(waMessage()), t: C.wa}]); return; }
  if (S.done && intentOf(r, ['i-thanks'])) { await say(F_.bye); return; }
  if (S.step !== 'idle' && intentOf(r, ['i-how']) && toks(t).length <= 3) { await say(F_.how.split(/[.!] /)[0] + '!'); return; }

  if (/\b(ne is yap|neler yap|ne yapiyorsunuz|hizmetleriniz|hizmetleriniz neler|neler sunuyorsunuz|what do you do|your services|what services|what can you do)/.test(norm(t))) {
    await say(F_.services); if (S.step === 'q' && !S.resumed) { S.resumed = true; save(); const q = curQ(); await say(F_.resume.replace('{q}', q.charAt(0).toLocaleLowerCase('tr') + q.slice(1))); } return;
  }
  const g0 = groupOf(r), topic = g0 && g0.s >= 1.6 && !(intentOf(r, ['i-price', 'i-location', 'i-hours']) && intentOf(r, ['i-price', 'i-location', 'i-hours']).s > g0.s);
  if (S.step === 'idle') {  // müşteri konu açana kadar yönlendirme yok
    const n = nameFrom(t);
    if (topic) {
      S.g = g0.g; S.first = t.slice(0, 200); save();
      if (isQ(t)) { if (G[S.g].yes) await say(G[S.g].yes); else await answerQuestion(t, r); }
      if (!S.name) { const nm = n && !(g0.s >= 2.2) ? n : null; if (nm) { S.name = nm; save(); } else { S.step = 'name'; save(); await say(F_.name_first); return; } }
      await say(pick(F_.ack)); return startGroup(S.g);
    }
    if (intentOf(r, ['i-how'])) { await say(F_.how); return; }
    if (isQ(t) && await answerQuestion(t, r)) return;
    if (n && !isQ(t) && !intentOf(r, ['i-greet', 'i-thanks'])) { S.name = n; save(); await say(pick(F_.nice) + ' ' + F_.idle[0]); return; }
    if (intentOf(r, ['i-greet'])) { await say(F_.greet_again); return; }
    if (intentOf(r, ['i-thanks'])) { await say(F_.thanks_idle); return; }
    if (isQ(t)) { await say(C.fallback); links([{wa: 1, u: waUrl(C.wa_head + '\n' + t), t: C.wa}]); return; }
    await say(pick(F_.idle)); return;
  }
  if (S.step === 'name') {  // adı bir kez sorar, ısrar etmez
    const n = nameFrom(t);
    if (n && !isQ(t)) { S.name = n; save(); await say(pick(F_.nice)); return startGroup(S.g); }
    if (isQ(t) && !(await answerQuestion(t, r))) await say(F_.q_unknown);
    return startGroup(S.g);
  }
  if (S.step === 'need') { S.step = 'idle'; save(); return local(t); }
  if (S.step === 'need_old') {
    const g = groupOf(r);
    const it = intentOf(r, ['i-price', 'i-location', 'i-hours']);
    if (g && g.s >= 1.6 && !(it && it.s > g.s)) { CH.innerHTML = ''; S.first = t.slice(0, 200); save(); await say(pick(F_.ack)); return startGroup(g.g); }
    if (isQ(t) && await answerQuestion(t, r)) { await say(F_.need); chips(F_.need_chips); return; }
    if (S.unclear++ < 1) { save(); await say(F_.need_unclear); chips(F_.need_chips); return; }
    S.ans = []; S.g = 'other'; S.step = 'q'; S.qi = 0; S.ans.push([G.other.qs[0][0], t.slice(0, 200)]); save(); return finish();
  }
  if (S.step === 'q') {
    const resume = async () => { if (S.resumed) return; S.resumed = true; save(); const q = curQ(); await say(F_.resume.replace('{q}', q.charAt(0).toLocaleLowerCase('tr') + q.slice(1))); };
    if (isQ(t)) { if (!(await answerQuestion(t, r))) await say(F_.q_unknown); return resume(); }
    if (intentOf(r, ['i-thanks', 'i-greet']) && toks(t).length <= 3) { await say(F_.thanks_mid); return resume(); }
    const ln = !S.name && S.qi === 0 && /^[A-ZÇĞİÖŞÜ][a-zçğıöşü]{1,19}[.!]?$/.test(t.trim()) && !groupOf(r) ? nameFrom(t) : null;
    if (ln) { S.name = ln; save(); await say(pick(F_.nice)); return say(curQ()); }
    S.resumed = false;
    const skip = /^(bilmiyorum|emin degilim|gec|farketmez|fark etmez|sonra|bilmem|idk|not sure|skip|don ?t know|no idea|whatever)/.test(norm(t).trim());
    S.ans.push([G[S.g].qs[S.qi][0], skip ? '-' : t.slice(0, 200)]); S.qi++; save();
    await say(skip ? F_.skip_ack : pick(F_.ack) + (!S.tip && G[S.g].tip ? ' ' + G[S.g].tip : ''));
    S.tip = true; save();
    if (S.qi < G[S.g].qs.length) return say(curQ());
    return finish();
  }
  // sohbet tamamlandıktan sonra: soruları cevapla, yeni konu açılırsa onu da konuş
  const g = groupOf(r);
  if (g && g.s >= 2.2 && g.g !== S.g) { if (isQ(t)) { if (G[g.g].yes) await say(G[g.g].yes); else await answerQuestion(t, r); } S.first = t.slice(0, 200); S.asked = []; await say(F_.new_topic); return startGroup(g.g); }
  if (await answerQuestion(t, r)) return;
  if (isQ(t)) { await say(C.fallback); links([{wa: 1, u: waUrl(C.wa_head + '\n' + t), t: C.wa}]); return; }
  await say(pick(F_.smalltalk));
}

async function remote(t) {  // yapay zekâ modu
  const ctl = new AbortController(), tm = setTimeout(() => ctl.abort(), 25000);
  const r = await fetch(C.endpoint, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({lang: D.lang, page: location.pathname, messages: S.hist.slice(-16)}), signal: ctl.signal});
  clearTimeout(tm); if (!r.ok) throw 0;
  const j = await r.json(); let reply = (j && j.reply || '').trim(); if (!reply) throw 0;
  let sum = null; const k = reply.indexOf('[[WHATSAPP]]');
  if (k >= 0) { sum = reply.slice(k + 12).trim(); reply = reply.slice(0, k).trim(); }
  if (reply) await say(reply.slice(0, 2000), false);
  if (sum) links([{wa: 1, u: waUrl(C.wa_head + '\n\n' + sum.slice(0, 1200)), t: F_.wa_btn}]);
}

let busy = false;
async function send(t) {
  t = String(t).trim().slice(0, 500); if (!t || busy) return;
  busy = true; CH.innerHTML = ''; push({k: 'b', w: 'u', t}); S.hist.push({role: 'user', content: t}); save();
  try {
    if (C.endpoint) { try { const d = document.createElement('div'); d.className = 'cb-b a t'; d.innerHTML = '<i></i><i></i><i></i>'; M.appendChild(d); M.scrollTop = M.scrollHeight; try { await remote(t); } finally { d.remove(); } }
                      catch (_) { await local(t); } }
    else await local(t);
  } finally { busy = false; }
}
async function toggle(v) {
  const open = v ?? box.hidden; box.hidden = !open; fab.setAttribute('aria-expanded', open); fab.classList.toggle('on', open);
  if (!open) return fab.focus();
  setTimeout(() => IN.focus(), 50); loadKB();
  if (!M.children.length) S.log.forEach(draw);
  if (S.step === 'start') { S.step = 'idle'; save(); await say(F_.greet); }
}
fab.addEventListener('click', () => toggle());
$('.cb-x', box).addEventListener('click', () => toggle(false));
document.addEventListener('keydown', e => { if (e.key === 'Escape' && !box.hidden) toggle(false); });
FM.addEventListener('submit', e => { e.preventDefault(); const v = IN.value; IN.value = ''; send(v); });
}
}
