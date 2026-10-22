import re

sch_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    text = f.read()

# Find all symbol references in schematic (outside lib_symbols)
# In kicad_sch v2024+, instantiated symbols are (symbol ... (property "Reference" "REF") ...)
sym_matches = re.findall(r'\(symbol\s+\(lib_id\s+\"([^\"]+)\"[\s\S]*?\(property\s+\"Reference\"\s+\"([^\"]+)\"[\s\S]*?\(property\s+\"Value\"\s+\"([^\"]+)\"', text)

# Filter out the lib_symbols section
lib_sym_start = text.find("(lib_symbols")
lib_sym_end = -1
if lib_sym_start != -1:
    depth = 0
    for idx in range(lib_sym_start, len(text)):
        if text[idx] == '(':
            depth += 1
        elif text[idx] == ')':
            depth -= 1
            if depth == 0:
                lib_sym_end = idx
                break

instantiated_text = text[lib_sym_end+1:] if lib_sym_end != -1 else text

inst_symbols = re.findall(r'\(symbol\s+\(lib_id\s+\"([^\"]+)\"[\s\S]*?\(property\s+\"Reference\"\s+\"([^\"]+)\"[\s\S]*?\(property\s+\"Value\"\s+\"([^\"]+)\"', instantiated_text)
print(f"Instantiated symbols in schematic: {len(inst_symbols)}")
for lib, ref, val in inst_symbols:
    print(f"  {ref:12}: {val:20} (lib: {lib})")

# Labels in schematic
labels = re.findall(r'\(label\s+\"([^\"]+)\"', text)
global_labels = re.findall(r'\(global_label\s+\"([^\"]+)\"', text)
hier_labels = re.findall(r'\(hierarchical_label\s+\"([^\"]+)\"', text)
print(f"\nLabels found: {len(labels)} local, {len(global_labels)} global, {len(hier_labels)} hier")
print("Local labels:", set(labels))
print("Global labels:", set(global_labels))
