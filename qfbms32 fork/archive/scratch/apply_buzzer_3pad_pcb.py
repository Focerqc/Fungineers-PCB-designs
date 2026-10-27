import re
import uuid

pcb_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
with open(pcb_path, "r", encoding="utf-8") as f:
    pcb = f.read()

# Load the updated footprint from vfbms.pretty
mod_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\vfbms.pretty\Buzzer_5.0x5.0mm_SMD.kicad_mod"
with open(mod_path, "r", encoding="utf-8") as f:
    mod = f.read().strip()

# Find BZ1 in pcb
m = re.search(r'\(property "Reference" "BZ1"', pcb)
if not m:
    print("BZ1 not found!")
    exit(1)

def block_end(text, start):
    depth = 0
    for i in range(start, len(text)):
        c = text[i]
        if c == '(': depth += 1
        elif c == ')':
            depth -= 1
            if depth == 0: return i + 1
    return -1

s = pcb.rfind('\t(footprint ', 0, m.start()) + 1
e = block_end(pcb, s)

# Prepare new footprint block
mod = re.sub(r'\(property "Reference" "REF\*\*"', '(property "Reference" "BZ1"', mod)
mod = re.sub(r'\(property "Value" "[^"]*"', '(property "Value" "FUET-5030"', mod)

# Center at (88.30, 2.80)
mod = mod.replace('(footprint "Buzzer_5.0x5.0mm_SMD"', '(footprint "vfbms:Buzzer_5.0x5.0mm_SMD"')
mod = re.sub(r'(\n\t\(layer "F\.Cu"\))', r'\1\n\t(uuid "' + str(uuid.uuid4()) + r'")\n\t(at 88.3 2.8)', mod, count=1)

# Assign nets: Pad 1 = +3V3, Pad 2 = BUZZ_LOW
mod = re.sub(r'(\(pad "1" smd rect\s+\(at [^\)]+\)\s+\(size [^\)]+\)\s+\(layers [^\)]+\))', r'\1\n\t\t(net "+3V3")', mod)
mod = re.sub(r'(\(pad "2" smd rect\s+\(at [^\)]+\)\s+\(size [^\)]+\)\s+\(layers [^\)]+\))', r'\1\n\t\t(net "BUZZ_LOW")', mod)

# Indent
nl = "\r\n" if "\r\n" in pcb else "\n"
mod = "\n".join("\t" + line for line in mod.splitlines()).replace("\n", nl)

pcb = pcb[:s] + mod + pcb[e:]
with open(pcb_path, "w", encoding="utf-8") as f:
    f.write(pcb)
print("Updated BZ1 in VFBMS32.kicad_pcb successfully!")
