"""Apply boxes.json fixes to VFBMS32.kicad_pcb:
 - C_FLT1 -> C_1812_4532Metric centered at (10.175, 16.625), rot 90
 - R_B1..32 re-pitched to 2.003 mm starting at (36.375, 28.05)
 - R_F1..32 re-pitched to 2.003 mm starting at (37.4, 30.3)
 - R_B33 (27R0, 0805) added at (100.975, 28.025), rot 90
Run with KiCad's python:  & "C:\\Program Files\\KiCad\\10.0\\bin\\python.exe" scratch/apply_bottom_row_fix.py
"""
import os, shutil, sys, datetime
import pcbnew

proj = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB"
pcb_path = os.path.join(proj, "VFBMS32.kicad_pcb")
fp_root = r"C:\Program Files\KiCad\10.0\share\kicad\footprints"

# path UUIDs for symbols added to the schematic (keep in sync with apply_sch_additions.py)
SCH_ROOT = "a2322edc-ff52-449c-92df-24faffac0236"
SYM_UUIDS = {
    "C_FLT1": "6f1c2d4e-8a3b-4c5d-9e0f-1a2b3c4d5e01",
    "R_B33":  "6f1c2d4e-8a3b-4c5d-9e0f-1a2b3c4d5e02",
}

stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
bk_dir = os.path.join(proj, ".mcp-backups")
os.makedirs(bk_dir, exist_ok=True)
shutil.copy2(pcb_path, os.path.join(bk_dir, f"VFBMS32_{stamp}_pre_bottomrow.kicad_pcb"))

PRELOADED = {}
for _lib, _name in (("Capacitor_SMD", "C_1812_4532Metric"), ("Resistor_SMD", "R_0805_2012Metric")):
    _fp = pcbnew.FootprintLoad(os.path.join(fp_root, _lib + ".pretty"), _name)
    if _fp is None:
        sys.exit(f"Failed to load {_lib}:{_name}")
    _fp.SetFPID(pcbnew.LIB_ID(_lib, _name))
    PRELOADED[(_lib, _name)] = _fp

board = pcbnew.LoadBoard(pcb_path)
mm = pcbnew.FromMM

def find(ref):
    for f in board.GetFootprints():
        if hasattr(f, "GetReference") and f.GetReference() == ref:
            return f
    return None

def at(x, y):
    return pcbnew.VECTOR2I(mm(x), mm(y))

def load(lib, name):
    return PRELOADED[(lib, name)]

def set_path(fp, ref):
    if ref in SYM_UUIDS:
        fp.SetPath(pcbnew.KIID_PATH(f"/{SYM_UUIDS[ref]}"))

def replace(ref, lib, name, x, y, rot, value=None):
    old = find(ref)
    val = value or (old.GetValue() if old else "")
    layer_hidden = {}
    if old:
        board.Remove(old)
    new = load(lib, name)
    new.SetReference(ref)
    new.SetValue(val)
    new.SetPosition(at(x, y))
    new.SetOrientation(pcbnew.EDA_ANGLE(rot, pcbnew.DEGREES_T))
    new.Reference().SetVisible(False)
    new.Value().SetVisible(False)
    set_path(new, ref)
    board.Add(new)
    return new

# 2) / 3) re-pitch R_B and R_F rows (before any Add())
PITCH = 2.003
for i in range(32):
    for prefix, x0, y0 in (("R_B", 36.375, 28.05), ("R_F", 37.4, 30.3)):
        ref = f"{prefix}{i+1}"
        fp = find(ref)
        if fp is None:
            print("MISSING", ref); continue
        fp.SetPosition(at(round(x0 + i * PITCH, 4), y0))
print("Re-pitched R_B1..32 and R_F1..32 to 2.003 mm")

# 1) C_FLT1 -> 1812
replace("C_FLT1", "Capacitor_SMD", "C_1812_4532Metric", 10.175, 16.625, 90.0, "10uF_100V")
print("C_FLT1 -> C_1812_4532Metric @ (10.175, 16.625)")

# 4) R_B33
if find("R_B33"):
    print("R_B33 exists, moving")
replace("R_B33", "Resistor_SMD", "R_0805_2012Metric", 100.975, 28.025, 90.0, "27R0")
print("R_B33 27R0 0805 @ (100.975, 28.025)")

pcbnew.SaveBoard(pcb_path, board)
print("Saved", pcb_path)
