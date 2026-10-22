"""Text-level (S-expression) edit of VFBMS32.kicad_pcb — avoids pcbnew SWIG instability.
 - R_B1..32 -> x = 36.375 + i*2.003, y = 28.05
 - R_F1..32 -> x = 37.4   + i*2.003, y = 30.3
 - C_FLT1   -> Capacitor_SMD:C_1812_4532Metric @ (10.175, 16.625, 90)
 - R_B33    -> clone of R_B32 (0805, 27R0) @ (100.975, 28.025, 90)
"""
import os, re, shutil, uuid, datetime

proj = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB"
pcb_path = os.path.join(proj, "VFBMS32.kicad_pcb")
lib_mod = r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Capacitor_SMD.pretty\C_1812_4532Metric.kicad_mod"
SYM_UUIDS = {"C_FLT1": "6f1c2d4e-8a3b-4c5d-9e0f-1a2b3c4d5e01",
             "R_B33":  "6f1c2d4e-8a3b-4c5d-9e0f-1a2b3c4d5e02"}
PITCH = 2.003

with open(pcb_path, "r", encoding="utf-8", newline="") as f:
    pcb = f.read()
NL = "\r\n" if "\r\n" in pcb else "\n"

stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
os.makedirs(os.path.join(proj, ".mcp-backups"), exist_ok=True)
shutil.copy2(pcb_path, os.path.join(proj, ".mcp-backups", f"VFBMS32_{stamp}_pre_bottomrow.kicad_pcb"))

def block_end(text, start):
    depth = 0
    for i in range(start, len(text)):
        c = text[i]
        if c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return i + 1
    raise ValueError("unbalanced")

def find_fp(text, ref):
    m = re.search(r'\(property "Reference" "%s"' % re.escape(ref), text)
    if not m:
        return None
    s = text.rfind("\t(footprint ", 0, m.start()) + 1
    return s, block_end(text, s)

def fresh_uuids(blk):
    return re.sub(r'\(uuid "[^"]+"\)', lambda _: f'(uuid "{uuid.uuid4()}")', blk)

def set_at(blk, x, y, rot=None):
    m = re.search(r'\n\t\t\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', blk)
    r = rot if rot is not None else (m.group(3) or "0")
    rs = f" {r}" if float(r) != 0 else ""
    return blk[:m.start()] + f"\n\t\t(at {x:g} {y:g}{rs})" + blk[m.end():]

def add_path(blk, ref):
    if ref in SYM_UUIDS and "(path " not in blk:
        blk = blk.replace("\t\t(attr ", f'\t\t(path "/{SYM_UUIDS[ref]}"){NL}\t\t(attr ', 1)
    return blk

# --- re-pitch rows ---
for i in range(32):
    for prefix, x0, y0 in (("R_B", 36.375, 28.05), ("R_F", 37.4, 30.3)):
        ref = f"{prefix}{i+1}"
        s, e = find_fp(pcb, ref)
        pcb = pcb[:s] + set_at(pcb[s:e], round(x0 + i * PITCH, 4), y0) + pcb[e:]
print("Re-pitched R_B1..32 / R_F1..32")

# --- R_B33 ---
if find_fp(pcb, "R_B33") is None:
    s, e = find_fp(pcb, "R_B32")
    blk = pcb[s:e]
    blk = blk.replace('(property "Reference" "R_B32"', '(property "Reference" "R_B33"', 1)
    blk = re.sub(r'\n\t\t\(path "[^"]*"\)', "", blk)
    blk = add_path(fresh_uuids(set_at(blk, 100.975, 28.025, "90")), "R_B33")
    pcb = pcb[:e] + NL + "\t" + blk + pcb[e:]
    print("Added R_B33")

# --- C_FLT1 -> 1812 ---
with open(lib_mod, "r", encoding="utf-8") as f:
    mod = f.read().strip()
mod = re.sub(r'\n\s*\((version|generator|generator_version) [^\n]*\)', "", mod)
ROT = 90.0
def rot_at(m):
    a = float(m.group(3) or 0) + ROT
    return f"(at {m.group(1)} {m.group(2)} {a:g})"
# rotate pads / properties / fp_text anchors (absolute angles in board files)
out_lines = []
ctx = None
for ln in mod.splitlines():
    st = ln.strip()
    if st.startswith(("(pad ", "(property ", "(fp_text ")):
        ctx = "rot"
    elif st.startswith(("(fp_line", "(fp_rect", "(fp_circle", "(fp_arc", "(fp_poly", "(model")):
        ctx = None
    if ctx == "rot":
        ln = re.sub(r'\(at ([-\d.]+) ([-\d.]+)(?: ([-\d.]+))?\)', rot_at, ln, count=1)
    out_lines.append(ln)
mod = "\n".join(out_lines)
mod = mod.replace('(property "Reference" "REF**"', '(property "Reference" "C_FLT1"', 1)
mod = re.sub(r'\(property "Value" "[^"]*"', '(property "Value" "10uF_100V"', mod, count=1)
# hide ref/value like the rest of the board
for prop in ("Reference", "Value"):
    m = re.search(r'\(property "%s" "[^"]*"\n(\s*)\(at [^\n]*\)\n\s*\(layer [^\n]*\)' % prop, mod)
    if m and "(hide yes)" not in mod[m.end():m.end() + 40]:
        mod = mod[:m.end()] + f"\n{m.group(1)}(hide yes)" + mod[m.end():]
mod = mod.replace('(footprint "C_1812_4532Metric"', '(footprint "C_1812_4532Metric"', 1)
mod = re.sub(r'(\n\t\(layer "F\.Cu"\))',
             r'\1' + f'\n\t(uuid "{uuid.uuid4()}")\n\t(at 10.175 16.625 90)', mod, count=1)
mod = fresh_uuids(mod)
mod = "\n".join("\t" + l for l in mod.splitlines()).replace("\n", NL)
mod = add_path(mod.lstrip("\t"), "C_FLT1")
s, e = find_fp(pcb, "C_FLT1")
pcb = pcb[:s] + mod + pcb[e:]
print("Replaced C_FLT1 with C_1812_4532Metric")

with open(pcb_path, "w", encoding="utf-8", newline="") as f:
    f.write(pcb)
print("Saved")
