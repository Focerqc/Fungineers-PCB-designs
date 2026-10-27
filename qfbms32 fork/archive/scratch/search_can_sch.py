import re

with open('qfbms32.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's search for symbols near J_COMM1 or CAN transceiver U7 or isolated CAN
symbols = re.findall(r'\(symbol\s+\(lib_id \"[^\"]+\"\)[\s\S]*?\)\s*\)', text)
print(f"Total symbols found: {len(symbols)}")
for s in symbols:
    if any(k in s for k in ["J_COMM", "ISO1050", "CANH", "CANL", "5V", "COMM"]):
        ref = re.search(r'\(property \"Reference\" \"([^\"]+)\"', s)
        val = re.search(r'\(property \"Value\" \"([^\"]+)\"', s)
        fp = re.search(r'\(property \"Footprint\" \"([^\"]+)\"', s)
        print(f"Symbol: {ref.group(1) if ref else ''} val={val.group(1) if val else ''} fp={fp.group(1) if fp else ''}")
