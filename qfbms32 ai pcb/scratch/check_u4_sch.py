with open("VFBMS32.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

import re
# check for wires or labels near 59.69, 170.18
wires = re.findall(r'\(wire[\s\S]*?\)', text)
print(f"Total wires: {len(wires)}")
labels = re.findall(r'\(label[\s\S]*?\)', text)
print(f"Total labels: {len(labels)}")
# check if any mention TPS or U4
for w in wires:
    if "U4" in w or "TPS" in w:
        print("Wire with U4/TPS:", w)

# check symbols in lib_symbols
lib_symbols = re.findall(r'\(symbol\s+"([^"]+)"', text)
print("Lib symbols defined:", [s for s in lib_symbols if "TPS" in s or "SPV" in s or "BOOST" in s or "BUCK" in s])
