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

/* ---------- DEEP Asistan: sohbet botu
   Varsayılan: tarayıcıda çalışan, sitedeki bilgi tabanından yanıt veren asistan (veri göndermez).
   CHAT_ENDPOINT tanımlıysa: mesajlar sunucu tarafı yapay zekâya gider; hata olursa yerel asistana döner. */
{
const D = window.DR || {}, C = D.chat; if (!C) throw 0;
const $ = (s, r = document) => r.querySelector(s), ROOT = D.root || '', TR = D.lang === 'tr';
const esc = s => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const MAP = {'ç':'c','ğ':'g','ı':'i','ö':'o','ş':'s','ü':'u','â':'a','î':'i','û':'u'};
const norm = s => String(s).toLocaleLowerCase('tr').replace(/[çğıöşüâîû]/g, c => MAP[c]).replace(/[^a-z0-9\s]/g, ' ');
const STOP = new Set(('ve ile bir bu su o da de mi mu mi midir ben biz siz sen icin gibi ama veya ya ne nasil hangi var yok mu ki cok daha en her olarak olan istiyorum isterim lazim bana bize size hakkinda bilgi almak yapiyor musunuz yapar misiniz musunuz misiniz neler nedir yapmak yaptirmak veriyor veriyorsunuz verir yapiyorsunuz sistem sistemi deep firma ' +
  'the a an and or of to for in on with is are do does doing make you your we our i me my can could would what how which about please want need have has it this that system offer provide').split(' '));
const toks = s => norm(s).replace(/deep\s+reklam/g, ' ').split(/\s+/).filter(t => t.length > 1 && !STOP.has(t));
const hit = (q, e) => { if (q === e) return true; let i = 0; const n = Math.min(q.length, e.length); while (i < n && q[i] === e[i]) i++; return (i === n && n >= 3) || i >= 5; };
let KB = null, hist = [], open = false;
const loadKB = () => KB ? Promise.resolve(KB) : fetch(ROOT + 'assets/kb-' + D.lang + '.json').then(r => r.json()).then(j => KB = j.map(x => ({...x, tt: toks(x.t), kt: toks(x.k)}))).catch(() => KB = []);
function rank(q) {
  const qt = toks(q); if (!qt.length || !KB) return [];
  return KB.map(x => { let s = 0; for (const t of qt) s += x.tt.some(e => hit(t, e)) ? 1.5 : x.kt.some(e => hit(t, e)) ? 1 : 0; return {x, s: s * x.w + (s > 0 && x.id.startsWith('p-') ? 0.6 : 0)}; })
    .filter(r => r.s >= 1).sort((a, b) => b.s - a.s);
}
const waUrl = q => `https://wa.me/${D.wa}?text=${encodeURIComponent(C.wa_head + (q ? '\n' + q : ''))}`;

const fab = $('.cb-fab'); if (!fab) throw 0;
const box = document.createElement('div');
box.className = 'cb'; box.hidden = true; box.setAttribute('role', 'dialog'); box.setAttribute('aria-label', C.title);
box.innerHTML = `<div class="cb-h"><span class="cb-av">AI</span><span class="cb-ht"><b>${esc(C.title)}</b><small>${esc(C.endpoint ? C.sub_ai : C.sub_local)}</small></span><button type="button" class="cb-x" aria-label="${esc(C.close)}">×</button></div>
<div class="cb-m" aria-live="polite"></div><div class="cb-c"></div>
<form class="cb-f"><label class="sr" for="cb-in">${esc(C.ph)}</label><input id="cb-in" autocomplete="off" maxlength="500" placeholder="${esc(C.ph)}"><button type="submit" aria-label="${esc(C.send)}"><svg viewBox="0 0 24 24" class="ic" aria-hidden="true"><path d="M4 12l16-8-6 16-2-7z"/></svg></button></form>
<p class="cb-n">${esc(C.note)}</p>`;
document.body.appendChild(box);
const M = $('.cb-m', box), CH = $('.cb-c', box), F = $('.cb-f', box), IN = $('#cb-in', box);

function bubble(who, text) { const d = document.createElement('div'); d.className = 'cb-b ' + who; d.textContent = text; M.appendChild(d); M.scrollTop = M.scrollHeight; return d; }
function actions(links, q) {
  const d = document.createElement('div'); d.className = 'cb-a';
  d.innerHTML = links.map(l => `<a href="${esc(ROOT + l.u)}">${esc(l.label)}</a>`).join('') +
    `<a class="wa" href="${esc(waUrl(q))}" target="_blank" rel="noopener">${esc(C.wa)}</a>`;
  M.appendChild(d); M.scrollTop = M.scrollHeight;
}
function chips() { CH.innerHTML = C.chips.map(c => `<button type="button">${esc(c)}</button>`).join(''); CH.querySelectorAll('button').forEach(b => b.onclick = () => ask(b.textContent)); }

function localAnswer(q) {
  if (/(\+?\d[\d\s()-]{8,}\d)/.test(q)) return {text: C.phone_note, links: []};
  const r = rank(q);
  if (!r.length) return {text: C.fallback, links: [{u: TR ? 'iletisim.html' : 'en/contact.html', label: C.form}]};
  const best = r[0].x, links = [], ttl = u => (KB.find(x => x.u === u && x.id.startsWith('p-')) || {}).t;
  if (best.u) links.push({u: best.u, label: (ttl(best.u) || C.go) + ' →'});
  const seen = new Set([best.u]);
  for (const o of r.slice(1)) { if (links.length >= 3) break; const t = ttl(o.x.u); if (o.x.u && t && !seen.has(o.x.u) && o.s >= r[0].s * 0.6) { seen.add(o.x.u); links.push({u: o.x.u, label: t}); } }
  return {text: best.a, links};
}
async function ask(q) {
  q = q.trim().slice(0, 500); if (!q) return;
  CH.innerHTML = ''; bubble('u', q); hist.push({role: 'user', content: q});
  const ty = bubble('a t', ''); ty.innerHTML = '<i></i><i></i><i></i>';
  await loadKB();
  let ans = null;
  if (C.endpoint) {
    try {
      const ctl = new AbortController(), tm = setTimeout(() => ctl.abort(), 20000);
      const r = await fetch(C.endpoint, {method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({lang: D.lang, page: location.pathname, messages: hist.slice(-10)}), signal: ctl.signal});
      clearTimeout(tm);
      if (r.ok) { const j = await r.json(); if (j && typeof j.reply === 'string' && j.reply.trim()) { const loc = localAnswer(q); ans = {text: j.reply.trim().slice(0, 2000), links: loc.text === C.fallback ? [] : loc.links.slice(0, 2)}; } }
    } catch (_) {}
  } else await new Promise(r => setTimeout(r, 450));
  if (!ans) ans = localAnswer(q);
  ty.remove(); bubble('a', ans.text); actions(ans.links, q); hist.push({role: 'assistant', content: ans.text});
  if (hist.length > 20) hist = hist.slice(-20);
}
function toggle(v) {
  open = v ?? !open; box.hidden = !open; fab.setAttribute('aria-expanded', open); fab.classList.toggle('on', open);
  if (open) { loadKB(); if (!M.children.length) { bubble('a', C.hello); chips(); } setTimeout(() => IN.focus(), 50); } else fab.focus();
}
fab.addEventListener('click', () => toggle());
$('.cb-x', box).addEventListener('click', () => toggle(false));
document.addEventListener('keydown', e => { if (e.key === 'Escape' && open) toggle(false); });
F.addEventListener('submit', e => { e.preventDefault(); const v = IN.value; IN.value = ''; ask(v); });
}
