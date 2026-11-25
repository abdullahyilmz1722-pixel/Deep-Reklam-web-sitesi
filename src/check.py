"""Derleme sonrası kontrol: kırık iç bağlantı, sayfa başına tek H1, title/description/canonical varlığı."""
import os, re, sys
from html.parser import HTMLParser
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_site")
class P(HTMLParser):
    def __init__(s): super().__init__(); s.links = []; s.h1 = 0; s.meta = set()
    def handle_starttag(s, t, a):
        a = dict(a)
        if t == "h1": s.h1 += 1
        if t == "title": s.meta.add("title")
        if t == "meta" and a.get("name") == "description" and a.get("content"): s.meta.add("desc")
        if t == "link" and a.get("rel") == "canonical": s.meta.add("canonical")
        for k in ("href", "src"):
            v = a.get(k)
            if v and not re.match(r"(https?:|mailto:|tel:|#|data:)", v): s.links.append(v)
bad = []; n = 0
for d, _, fs in os.walk(ROOT):
    for f in fs:
        if not f.endswith(".html"): continue
        n += 1; fp = os.path.join(d, f); p = P(); p.feed(open(fp, encoding="utf-8").read()); rel = os.path.relpath(fp, ROOT)
        if p.h1 != 1: bad.append(f"{rel}: {p.h1} adet h1")
        need = {"title", "desc"} | (set() if f == "404.html" else {"canonical"})
        if need - p.meta: bad.append(f"{rel}: eksik {need - p.meta}")
        if f == "404.html": continue
        for l in p.links:
            t = os.path.normpath(os.path.join(d, l.split("?")[0].split("#")[0]))
            if not os.path.exists(t): bad.append(f"{rel}: kırık bağlantı {l}")
print(f"{n} sayfa kontrol edildi, {len(bad)} sorun")
for b in bad: print(" -", b)
sys.exit(1 if bad else 0)
