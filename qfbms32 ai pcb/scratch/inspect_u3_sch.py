import re

sch_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    text = f.read()

# Let's search for U3 (ESP32) definition in lib_symbols or instances
esp_idx = text.find('(property "Reference" "U3"')
if esp_idx != -1:
    print("Instance U3 found:")
    print(text[esp_idx-100:esp_idx+400])

# Find pins connected to U3
# Check wires or labels near U3 position (42.418, 124.206)
wires = re.findall(r'\(wire\s+\(pts\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\s+\(xy\s+([-\d.]+)\s+([-\d.]+)\)\)', text)
print(f"Total wires in schematic: {len(wires)}")

labels = re.findall(r'\((?:label|global_label|hierarchical_label)\s+\"([^\"]+)\"\s+\(shape\s+\w+\)?\s*\(at\s+([-\d.]+)\s+([-\d.]+)', text)
print(f"Total labels in schematic: {len(labels)}")
for l in labels:
    print(f"  Label: {l[0]} at ({l[1]}, {l[2]})")
