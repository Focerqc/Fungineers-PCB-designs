import re

with open("VFBMS32.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

sheets = re.findall(r'\(sheet\s+.*?\(property "Sheetname" "([^"]+)".*?\(property "Sheetfile" "([^"]+)"', text, re.DOTALL)
print("Hierarchical sheets:", sheets)

symbols = re.findall(r'\(symbol\s+.*?\(property "Reference" "([^"]+)".*?\(property "Value" "([^"]+)"', text, re.DOTALL)
print(f"Total symbols in root sch: {len(symbols)}")
print("References:", sorted(set([s[0] for s in symbols])))
