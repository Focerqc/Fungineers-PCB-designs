from pathlib import Path
import re

t = Path(r"C:\Program Files\KiCad\10.0\share\kicad\symbols\Connector_Generic.kicad_sym").read_text(
    encoding="utf-8"
)
names = sorted(set(re.findall(r'\(symbol "([^"]*Conn_01x[^"]*)"', t)))
for n in names[:40]:
    print(n)
print("total", len(names))
