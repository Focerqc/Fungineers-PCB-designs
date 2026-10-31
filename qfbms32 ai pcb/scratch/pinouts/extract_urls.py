import re
from pathlib import Path

t = Path(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\scratch\pinouts\agm_pinout.html").read_text(encoding="utf-8", errors="ignore")
urls = set(re.findall(r"https?://[^\"'\s>]+\.(?:png|jpg|jpeg|webp|pdf)", t, re.I))
print("count", len(urls))
for u in sorted(urls):
    print(u[:300])
# also oss-style without extension
oss = set(re.findall(r"https?://[^\"'\s>]+(?:pin|datasheet|pdf|image)[^\"'\s>]*", t, re.I))
print("--- loose", len(oss))
for u in list(oss)[:30]:
    print(u[:300])
