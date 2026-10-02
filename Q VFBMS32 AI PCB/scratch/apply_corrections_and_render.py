import os
import re
import subprocess
from PIL import Image
import pcbnew

project_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB"
custom_lib = os.path.join(project_dir, "vfbms.pretty")
pcb_path = os.path.join(project_dir, "VFBMS32.kicad_pcb")
sch_path = os.path.join(project_dir, "VFBMS32.kicad_sch")
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"

brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\3983d48b-3039-4490-8203-875b5320f863"
os.makedirs(brain_dir, exist_ok=True)

print("=== STEP 1: SCHEMATIC CORRECTIONS ===")
with open(sch_path, "r", encoding="utf-8") as f:
    sch_txt = f.read()

# Remove U4 (TPS62130) symbol instance from schematic
# Find symbol block with Reference U4
sch_new = re.sub(
    r'\t\(symbol\s*\n\t\t\(lib_id "Regulator_Switching:TPS62130"\)[\s\S]*?\(property "Reference" "U4"[\s\S]*?\n\t\)\n',
    '',
    sch_txt
)

# Remove TPS62130 from lib_symbols if present
sch_new = re.sub(
    r'\t\t\(symbol "Regulator_Switching:TPS62130"[\s\S]*?\n\t\t\)\n',
    '',
    sch_new
)

with open(sch_path, "w", encoding="utf-8") as f:
    f.write(sch_new)
print("Removed U4 (TPS62130) from schematic.")

print("\n=== STEP 2: LOAD BOARD WITH PCBNEW ===")
board = pcbnew.LoadBoard(pcb_path)

# Delete Ghost ICs: U_BOOST1 and U_BUCK1
for ghost_ref in ["U_BOOST1", "U_BUCK1"]:
    fp = board.FindFootprintByReference(ghost_ref)
    if fp:
        board.Delete(fp)
        print(f"Deleted ghost IC {ghost_ref} from board.")

# Replace XT30 connectors with updated footprints containing PTH drill pads and mounting tabs
connectors = [
    ("J_CHG1", "XT30PW-F_Lugs"),
    ("J_BAT1", "XT30PW-M_Lugs")
]
for ref, lib_item in connectors:
    old_fp = board.FindFootprintByReference(ref)
    if old_fp:
        pos = pcbnew.VECTOR2I(old_fp.GetPosition().x, old_fp.GetPosition().y)
        rot = old_fp.GetOrientation()
        val = old_fp.GetValue()
        board.Delete(old_fp)
        
        new_fp = pcbnew.FootprintLoad(custom_lib, lib_item)
        new_fp.SetPosition(pos)
        new_fp.SetOrientation(rot)
        new_fp.SetReference(ref)
        new_fp.SetValue(val)
        new_fp.Reference().SetVisible(False)
        new_fp.Value().SetVisible(False)
        board.Add(new_fp)
        print(f"Replaced {ref} with updated {lib_item} (PTH pins + mounting tabs).")

# Update Power Stage Placements:
# Shift Q1 and Q2 to X = 21.50 mm (providing safe >2.5mm clearance to XT30 pins)
# Align R_SH2 between them at X = 21.50 mm
# Shift F1 to X = 14.80 mm (between J_BAT1 pins and Q2)
# Shift gate drive passives and U_SSR1 right to clear Q1
relocations = {
    "Q1":     (21.50,  6.40,   0.0),
    "Q2":     (21.50, 25.60, 180.0),
    "R_SH2":  (21.50, 13.80,   0.0),
    "F1":     (14.80, 27.05,  90.0),
    "C_DISC": (27.50, 13.80,  90.0),
    "C_DRV1": (27.50,  6.80,   0.0),
    "R_DRV1": (27.50,  4.50,   0.0),
    "U_SSR1": (31.50,  5.80,   0.0),
    "R_DRV2": (35.00,  4.00,   0.0),
    "C_DRV2": (35.00,  6.00,   0.0),
    "R_DRV3": (31.50, 11.50,   0.0),
    "D_TVS1": (31.50,  9.50,   0.0),
    "D_SEC1": (27.50, 17.50,  90.0),
    "D_SEC2": (29.80, 17.50,  90.0),
}

for ref, (nx, ny, nrot) in relocations.items():
    fp = board.FindFootprintByReference(ref)
    if fp:
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(nx), pcbnew.FromMM(ny)))
        fp.SetOrientation(pcbnew.EDA_ANGLE(nrot, pcbnew.DEGREES_T))
        print(f"Shifted {ref:8s} to ({nx:6.2f}, {ny:6.2f}), rot={nrot:5.1f} deg")

# Remove existing power stage copper shapes (PCB_SHAPE on F.Cu/B.Cu with X < 35) and heavy tracks
drawings_to_remove = []
for d in board.GetDrawings():
    if isinstance(d, pcbnew.PCB_SHAPE) and d.GetLayer() in [pcbnew.F_Cu, pcbnew.B_Cu]:
        bb = d.GetBoundingBox()
        if pcbnew.ToMM(bb.GetX()) < 35.0:
            drawings_to_remove.append(d)

for d in drawings_to_remove:
    board.Delete(d)
print(f"Removed {len(drawings_to_remove)} old power stage copper shapes.")

tracks_to_remove = []
for t in board.GetTracks():
    if not isinstance(t, pcbnew.PCB_VIA) and t.GetWidth() >= pcbnew.FromMM(2.0):
        sp = t.GetStart()
        if pcbnew.ToMM(sp.x) < 35.0:
            tracks_to_remove.append(t)

for t in tracks_to_remove:
    board.Delete(t)
print(f"Removed {len(tracks_to_remove)} old heavy copper tracks.")

# Helpers for adding heavy copper fills and tracks
def add_copper_fill(pts_mm, layer=pcbnew.F_Cu):
    s = pcbnew.PCB_SHAPE(board)
    s.SetShape(pcbnew.SHAPE_T_POLY)
    s.SetLayer(layer)
    s.SetFilled(True)
    poly = pcbnew.SHAPE_LINE_CHAIN()
    for x, y in pts_mm:
        poly.Append(pcbnew.FromMM(x), pcbnew.FromMM(y))
    poly.SetClosed(True)
    s.SetPolyShape(pcbnew.SHAPE_POLY_SET(poly))
    board.Add(s)
    return s

def add_heavy_track(x1, y1, x2, y2, width_mm=3.5, layer=pcbnew.F_Cu):
    t = pcbnew.PCB_TRACK(board)
    t.SetLayer(layer)
    t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
    t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
    t.SetWidth(pcbnew.FromMM(width_mm))
    board.Add(t)
    return t

# 1. CHG+ Heavy Copper Pour: From J_CHG1 pin 1 (13.94, 4.95) to shifted Q1 Drain tab (21.50, 4.80)
# F.Cu pour
add_copper_fill([
    (12.0, 1.0),
    (26.5, 1.0),
    (26.5, 8.5),
    (15.5, 8.5),
    (15.5, 6.5),
    (12.0, 6.5)
], layer=pcbnew.F_Cu)

# B.Cu pour (mirroring CHG+ plane for massive current capacity)
add_copper_fill([
    (12.0, 1.0),
    (26.5, 1.0),
    (26.5, 8.5),
    (12.0, 8.5)
], layer=pcbnew.B_Cu)

add_heavy_track(13.94, 4.95, 21.50, 4.80, width_mm=3.5, layer=pcbnew.F_Cu)
add_heavy_track(13.94, 4.95, 21.50, 4.80, width_mm=3.5, layer=pcbnew.B_Cu)

# 2. BAT+ / FUSE / Q2 Drain Heavy Copper Pour: From J_BAT1 pin 1 (12.10, 27.05) through F1 (14.80, 27.05) to Q2 Drain tab (21.50, 27.20)
# F.Cu pour: J_BAT1 pin 1 to F1
add_copper_fill([
    (10.5, 25.0),
    (14.0, 25.0),
    (14.0, 29.5),
    (10.5, 29.5)
], layer=pcbnew.F_Cu)

# F.Cu pour: F1 to Q2 Drain tab
add_copper_fill([
    (15.5, 23.5),
    (26.5, 23.5),
    (26.5, 31.0),
    (15.5, 31.0)
], layer=pcbnew.F_Cu)

# B.Cu pour: heavy continuous BAT+ plane across bottom
add_copper_fill([
    (10.5, 24.0),
    (26.5, 24.0),
    (26.5, 31.0),
    (10.5, 31.0)
], layer=pcbnew.B_Cu)

add_heavy_track(12.10, 27.05, 14.80, 27.05, width_mm=3.5, layer=pcbnew.F_Cu)
add_heavy_track(15.80, 27.05, 21.50, 27.20, width_mm=3.5, layer=pcbnew.F_Cu)
add_heavy_track(12.10, 27.05, 21.50, 27.20, width_mm=3.5, layer=pcbnew.B_Cu)

# 3. PACK Rail: Q1 Source (Y=11.05) through horizontal R_SH2 (21.50, 13.80) to Q2 Source (Y=20.95)
add_copper_fill([
    (18.0,  9.5),
    (25.0,  9.5),
    (25.0, 13.0),
    (18.0, 13.0)
], layer=pcbnew.F_Cu)

add_copper_fill([
    (18.0, 14.6),
    (25.0, 14.6),
    (25.0, 22.5),
    (18.0, 22.5)
], layer=pcbnew.F_Cu)

add_heavy_track(21.50, 10.0, 21.50, 13.0, width_mm=4.0, layer=pcbnew.F_Cu)
add_heavy_track(21.50, 14.6, 21.50, 22.0, width_mm=4.0, layer=pcbnew.F_Cu)

# 4. Central GND Plane between XT30s around vertical R_SH1 (10.60, 16.00)
add_copper_fill([
    (3.5,  8.5),
    (15.5,  8.5),
    (15.5, 23.5),
    (3.5, 23.5)
], layer=pcbnew.F_Cu)

add_copper_fill([
    (3.5,  8.5),
    (15.5,  8.5),
    (15.5, 23.5),
    (3.5, 23.5)
], layer=pcbnew.B_Cu)

add_heavy_track(13.94,  9.95, 10.60, 13.00, width_mm=2.5, layer=pcbnew.F_Cu)
add_heavy_track(12.10, 22.05, 10.60, 19.00, width_mm=2.5, layer=pcbnew.F_Cu)

# Save updated board
pcbnew.SaveBoard(pcb_path, board)
print("\nSuccessfully updated and saved VFBMS32.kicad_pcb!")

print("\n=== STEP 3: GENERATE VERIFICATION RENDERS ===")

# 1. Side Profile 3D Render
side_render_path = os.path.join(project_dir, "VFBMS32_render_side_profile.png")
brain_side_path = os.path.join(brain_dir, "VFBMS32_render_side_profile.png")

print("Rendering side profile...")
subprocess.run([
    kicad_cli, "pcb", "render",
    "--side", "left",
    "--width", "2400", "--height", "1200",
    "--background", "transparent",
    "-o", side_render_path,
    pcb_path
], check=True)

im_s = Image.open(side_render_path)
bbox_s = im_s.getbbox()
if bbox_s:
    pad = 40
    crop_s = im_s.crop((max(0, bbox_s[0]-pad), max(0, bbox_s[1]-pad), min(im_s.width, bbox_s[2]+pad), min(im_s.height, bbox_s[3]+pad)))
    crop_s.save(side_render_path)
    crop_s.save(brain_side_path)
    print("Saved cropped side profile render:", side_render_path)

# Also render an angled 3D side profile view so pins underneath and flush housing are visible in perspective!
angle_render_path = os.path.join(project_dir, "VFBMS32_render_side_angle.png")
brain_angle_path = os.path.join(brain_dir, "VFBMS32_render_side_angle.png")

subprocess.run([
    kicad_cli, "pcb", "render",
    "--perspective",
    "--rotate", "-20,-65,15",
    "--floor",
    "--width", "2800", "--height", "1400",
    "--background", "transparent",
    "-o", angle_render_path,
    pcb_path
], check=True)

im_a = Image.open(angle_render_path)
bbox_a = im_a.getbbox()
if bbox_a:
    pad = 40
    crop_a = im_a.crop((max(0, bbox_a[0]-pad), max(0, bbox_a[1]-pad), min(im_a.width, bbox_a[2]+pad), min(im_a.height, bbox_a[3]+pad)))
    crop_a.save(angle_render_path)
    crop_a.save(brain_angle_path)
    print("Saved cropped angled 3D side profile render:", angle_render_path)

# 2. Top-Down 2D Render
top_render_path = os.path.join(project_dir, "VFBMS32_layout_top_hi_raw.png")
brain_top_path = os.path.join(brain_dir, "VFBMS32_layout_top_hi_raw.png")

print("Rendering top-down view...")
subprocess.run([
    kicad_cli, "pcb", "render",
    "--side", "top",
    "--width", "3600", "--height", "1200",
    "--background", "transparent",
    "-o", top_render_path,
    pcb_path
], check=True)

im_t = Image.open(top_render_path)
bbox_t = im_t.getbbox()
if bbox_t:
    pad = 40
    crop_t = im_t.crop((max(0, bbox_t[0]-pad), max(0, bbox_t[1]-pad), min(im_t.width, bbox_t[2]+pad), min(im_t.height, bbox_t[3]+pad)))
    crop_t.save(top_render_path)
    crop_t.save(brain_top_path)
    print("Saved cropped top-down render:", top_render_path)

# 3. Main 3D isometric render
iso_render_path = os.path.join(project_dir, "VFBMS32_render_3d.png")
brain_iso_path = os.path.join(brain_dir, "VFBMS32_render_3d.png")

print("Rendering full isometric 3D view...")
subprocess.run([
    kicad_cli, "pcb", "render",
    "--perspective",
    "--rotate", "-25,0,25",
    "--floor",
    "--width", "3600", "--height", "1600",
    "--background", "transparent",
    "-o", iso_render_path,
    pcb_path
], check=True)

im_i = Image.open(iso_render_path)
bbox_i = im_i.getbbox()
if bbox_i:
    pad = 40
    crop_i = im_i.crop((max(0, bbox_i[0]-pad), max(0, bbox_i[1]-pad), min(im_i.width, bbox_i[2]+pad), min(im_i.height, bbox_i[3]+pad)))
    crop_i.save(iso_render_path)
    crop_i.save(brain_iso_path)
    print("Saved cropped full 3D isometric render:", iso_render_path)

# Also generate a power stage zoom crop of top view
power_zoom_path = os.path.join(project_dir, "VFBMS32_power_stage_verified.png")
brain_power_path = os.path.join(brain_dir, "VFBMS32_power_stage_verified.png")
w, h = crop_t.size
crop_power = crop_t.crop((0, 0, int(w * 0.35), h))
crop_power.save(power_zoom_path)
crop_power.save(brain_power_path)
print("Saved power stage zoom crop:", power_zoom_path)

print("\nALL TASKS COMPLETED SUCCESSFULLY!")
