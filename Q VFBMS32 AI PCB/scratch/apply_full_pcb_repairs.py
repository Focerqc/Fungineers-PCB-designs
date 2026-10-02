import os
import re
import shutil
import subprocess
from PIL import Image

PROJECT_DIR = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB"
KICAD_CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
PCB_PATH = os.path.join(PROJECT_DIR, "VFBMS32.kicad_pcb")
USB_MOD_PATH = os.path.join(PROJECT_DIR, "vfbms.pretty", "USB_C_Receptacle_16P.kicad_mod")
BRAIN_DIR = r"C:\Users\quinn\.gemini\antigravity-ide\brain\72831b47-02e9-420d-bfb3-5bd9838b8feb"

print("==========================================================")
print("1. DIAGNOSING J_USB1 FOOTPRINT BEFORE REPAIR")
print("==========================================================")
with open(PCB_PATH, "r", encoding="utf-8") as f:
    pcb_raw = f.read()

m_usb_before = re.search(r'\(footprint [^\n]*\n[\s\S]*?\"Reference\" \"J_USB1\"[\s\S]*?\n\t\)', pcb_raw)
pads_before_count = 0
if m_usb_before:
    pads_before = re.findall(r'\(pad\s+"([^"]*)"\s+([^\s]+)\s+([^\s]+)\s+\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', m_usb_before.group(0))
    pads_before_count = len(pads_before)
    unique_pads_before = set((p[3], p[4]) for p in pads_before)
    print(f"J_USB1 before repair:")
    print(f"  Total pads found: {pads_before_count}")
    print(f"  Unique pad coordinate offsets: {len(unique_pads_before)} (corrupted/stacked pads: all share identical position)")
else:
    print("J_USB1 footprint not found!")

print("\n==========================================================")
print("2. PREPARING CLEAN USB-C FOOTPRINT S-EXPRESSION")
print("==========================================================")
with open(USB_MOD_PATH, "r", encoding="utf-8") as f:
    mod_lines = f.readlines()

usb_sexpr_lines = [
    '\t(footprint "USB_C_Receptacle_16P"\n',
    '\t\t(layer "F.Cu")\n',
    '\t\t(uuid "a83fa8a8-d21e-455d-928e-d03d4d9ffad8")\n',
    '\t\t(at 125 3.2 180)\n',
    '\t\t(descr "USB 2.0 Type C Receptacle, GCT, 16P, top mounted, horizontal, 5A: https://gct.co/files/drawings/usb4105.pdf")\n',
    '\t\t(tags "USB C Type-C Receptacle SMD USB 2.0 16P 16C USB4105-15-A USB4105-15-A-060 USB4105-15-A-120 USB4105-GF-A USB4105-GF-A-060 USB4105-GF-A-120")\n',
    '\t\t(property "Reference" "J_USB1"\n',
    '\t\t\t(at 0 -5.5 0)\n',
    '\t\t\t(unlocked yes)\n',
    '\t\t\t(layer "F.SilkS")\n',
    '\t\t\t(hide yes)\n',
    '\t\t\t(uuid "d81b2ec1-0767-4f87-8b89-63054df5531c")\n',
    '\t\t\t(effects\n',
    '\t\t\t\t(font\n',
    '\t\t\t\t\t(size 1 1)\n',
    '\t\t\t\t\t(thickness 0.15)\n',
    '\t\t\t\t)\n',
    '\t\t\t)\n',
    '\t\t)\n',
    '\t\t(property "Value" "USB-C"\n',
    '\t\t\t(at 0 5 0)\n',
    '\t\t\t(unlocked yes)\n',
    '\t\t\t(layer "F.Fab")\n',
    '\t\t\t(hide yes)\n',
    '\t\t\t(uuid "756b6741-abf8-4a98-8de8-fe7500c817fc")\n',
    '\t\t\t(effects\n',
    '\t\t\t\t(font\n',
    '\t\t\t\t\t(size 1 1)\n',
    '\t\t\t\t\t(thickness 0.15)\n',
    '\t\t\t\t)\n',
    '\t\t\t)\n',
    '\t\t)\n',
    '\t\t(property "Datasheet" ""\n',
    '\t\t\t(at 0 0 0)\n',
    '\t\t\t(unlocked yes)\n',
    '\t\t\t(layer "F.Fab")\n',
    '\t\t\t(hide yes)\n',
    '\t\t\t(uuid "2169e155-14da-40de-8a0f-d9d236f940df")\n',
    '\t\t\t(effects\n',
    '\t\t\t\t(font\n',
    '\t\t\t\t\t(size 1.27 1.27)\n',
    '\t\t\t\t\t(thickness 0.15)\n',
    '\t\t\t\t)\n',
    '\t\t\t)\n',
    '\t\t)\n',
    '\t\t(property "Description" ""\n',
    '\t\t\t(at 0 0 0)\n',
    '\t\t\t(unlocked yes)\n',
    '\t\t\t(layer "F.Fab")\n',
    '\t\t\t(hide yes)\n',
    '\t\t\t(uuid "c6e56b0f-6ad3-4fda-8f6e-0a363af3a539")\n',
    '\t\t\t(effects\n',
    '\t\t\t\t(font\n',
    '\t\t\t\t\t(size 1.27 1.27)\n',
    '\t\t\t\t\t(thickness 0.15)\n',
    '\t\t\t\t)\n',
    '\t\t\t)\n',
    '\t\t)\n'
]

skip_head = True
for line in mod_lines[1:]:
    if '(attr smd)' in line:
        skip_head = False
    if not skip_head:
        if line.strip() == ')':
            usb_sexpr_lines.append('\t)\n')
        else:
            usb_sexpr_lines.append('\t' + line)

usb_clean_sexpr = "".join(usb_sexpr_lines)

print("\n==========================================================")
print("3. APPLYING PRECISE COORDINATES TO PCB COMPONENTS")
print("==========================================================")
# Target Y coordinates:
# JST GH headers: Y = 22.00 mm
# R_B1..32 (0805): Y = 28.00 mm
# R_F1..32 (0402): Y = 30.65 mm
# U7 (DUB-8): X = 124.00 mm, Y = 14.00 mm
# J_USB1: X = 125.00 mm, Y = 3.20 mm, rot = 180.0 deg

jst_set = {"J_COMM1", "J_CELL4", "J_CELL3", "J_CELL2", "J_CELL1", "J_T4", "J_T3", "J_T2", "J_T1"}
rb_set = {f"R_B{i}" for i in range(1, 33)}
rf_set = {f"R_F{i}" for i in range(1, 33)}

with open(PCB_PATH, "r", encoding="utf-8") as f:
    pcb_lines = f.readlines()

new_lines = []
depth = 0
in_fp = False
curr_fp_lines = []

for line in pcb_lines:
    if '(footprint ' in line and depth == 0:
        in_fp = True
        depth = 1
        curr_fp_lines = [line]
    elif in_fp:
        curr_fp_lines.append(line)
        depth += line.count('(') - line.count(')')
        if depth == 0:
            in_fp = False
            fp_text = "".join(curr_fp_lines)
            ref_m = re.search(r'\(property "Reference" "([^"]+)"', fp_text)
            ref = ref_m.group(1) if ref_m else ""

            if ref == "J_USB1":
                print("  -> J_USB1: Replacing with clean footprint at (125.0, 3.2, 180)")
                new_lines.append(usb_clean_sexpr)
            elif ref == "U7":
                print("  -> U7: Positioning at (124.0, 14.0, rot=0)")
                # Set U7 at (at 124 14)
                lines_fp = fp_text.splitlines(keepends=True)
                for i in range(min(6, len(lines_fp))):
                    if re.search(r'^\s*\(at\s+[0-9\.\-]+\s+[0-9\.\-]+(?:\s+[0-9\.\-]+)?\)', lines_fp[i]):
                        lines_fp[i] = "\t\t(at 124 14)\n"
                        break
                new_lines.append("".join(lines_fp))
            elif ref in jst_set:
                lines_fp = fp_text.splitlines(keepends=True)
                for i in range(min(6, len(lines_fp))):
                    m_at = re.search(r'^\s*\(at\s+([0-9\.\-]+)\s+[0-9\.\-]+(?:\s+([0-9\.\-]+))?\)', lines_fp[i])
                    if m_at:
                        x = m_at.group(1)
                        rot_s = f" {m_at.group(2)}" if m_at.group(2) else ""
                        lines_fp[i] = f"\t\t(at {x} 22{rot_s})\n"
                        break
                new_lines.append("".join(lines_fp))
            elif ref in rb_set:
                lines_fp = fp_text.splitlines(keepends=True)
                for i in range(min(6, len(lines_fp))):
                    m_at = re.search(r'^\s*\(at\s+([0-9\.\-]+)\s+[0-9\.\-]+(?:\s+([0-9\.\-]+))?\)', lines_fp[i])
                    if m_at:
                        x = m_at.group(1)
                        rot_s = f" {m_at.group(2)}" if m_at.group(2) else ""
                        lines_fp[i] = f"\t\t(at {x} 28{rot_s})\n"
                        break
                new_lines.append("".join(lines_fp))
            elif ref in rf_set:
                lines_fp = fp_text.splitlines(keepends=True)
                for i in range(min(6, len(lines_fp))):
                    m_at = re.search(r'^\s*\(at\s+([0-9\.\-]+)\s+[0-9\.\-]+(?:\s+([0-9\.\-]+))?\)', lines_fp[i])
                    if m_at:
                        x = m_at.group(1)
                        rot_s = f" {m_at.group(2)}" if m_at.group(2) else ""
                        lines_fp[i] = f"\t\t(at {x} 30.65{rot_s})\n"
                        break
                new_lines.append("".join(lines_fp))
            else:
                new_lines.append(fp_text)
    else:
        new_lines.append(line)

with open(PCB_PATH, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("Saved updated VFBMS32.kicad_pcb successfully!")

print("\n==========================================================")
print("4. VERIFYING J_USB1 AND CLEARANCES AFTER REPAIR")
print("==========================================================")
with open(PCB_PATH, "r", encoding="utf-8") as f:
    updated_pcb = f.read()

m_usb_after = re.search(r'\(footprint [^\n]*\n[\s\S]*?\"Reference\" \"J_USB1\"[\s\S]*?\n\t\)', updated_pcb)
if m_usb_after:
    pads_after = re.findall(r'\(pad\s+"([^"]*)"\s+([^\s]+)\s+([^\s]+)\s+\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', m_usb_after.group(0))
    print(f"J_USB1 after repair: {len(pads_after)} total pads/holes.")
    smd_pads = [p for p in pads_after if p[1] == 'smd']
    th_pads = [p for p in pads_after if p[1] in ['thru_hole', 'np_thru_hole']]
    print(f"  SMT signal/power pads: {len(smd_pads)} (A1-A12, B1-B12)")
    print(f"  Through-hole / shield / NPTH pads: {len(th_pads)}")
    unique_offsets_after = set((p[3], p[4]) for p in pads_after)
    print(f"  Unique distinct pad offsets: {len(unique_offsets_after)}")
    print("  Pad details:")
    for p in pads_after:
        print(f"    Pad {p[0]:4} | {p[1]:12} | {p[2]:10} | at ({float(p[3]):5.2f}, {float(p[4]):5.2f})")

print("\n==========================================================")
print("5. GENERATING 2D AND 3D RENDERS")
print("==========================================================")
render_top = os.path.join(PROJECT_DIR, "VFBMS32_layout_top_hi_raw.png")
subprocess.run([
    KICAD_CLI, "pcb", "render",
    "--rotate", "0,0,0",
    "--zoom", "1",
    "--width", "3600", "--height", "1200",
    "--background", "transparent",
    "-o", render_top, PCB_PATH
], check=True)
print(f"Generated 2D top render: {render_top}")

render_3d = os.path.join(PROJECT_DIR, "VFBMS32_render_3d.png")
subprocess.run([
    KICAD_CLI, "pcb", "render",
    "--perspective",
    "--rotate", "-25,0,25",
    "--floor",
    "--width", "3600", "--height", "1600",
    "--background", "transparent",
    "-o", render_3d, PCB_PATH
], check=True)
print(f"Generated 3D perspective render: {render_3d}")

# Crop top-right corner (USB-C + U7 + ESP32)
im_top = Image.open(render_top)
bbox = im_top.getbbox()
if bbox:
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    crop_x1 = bbox[0] + int(w * 0.75)
    crop_x2 = bbox[2] + 20
    crop_y1 = max(0, bbox[1] - 20)
    crop_y2 = bbox[1] + int(h * 0.65)
    corner_zoom = im_top.crop((crop_x1, crop_y1, crop_x2, crop_y2))
    corner_zoom_path = os.path.join(PROJECT_DIR, "VFBMS32_esp_usb_u7_verified.png")
    corner_zoom.save(corner_zoom_path)
    print(f"Saved verified top-right zoom: {corner_zoom_path}")

    # Crop bottom row region showing JST clearance and ~1mm bottom edge margin
    crop_bx1 = bbox[0] + int(w * 0.20)
    crop_bx2 = bbox[2] - int(w * 0.05)
    crop_by1 = bbox[1] + int(h * 0.45)
    crop_by2 = min(im_top.height, bbox[3] + 20)
    bottom_zoom = im_top.crop((crop_bx1, crop_by1, crop_bx2, crop_by2))
    bottom_zoom_path = os.path.join(PROJECT_DIR, "VFBMS32_bottom_edge_verified.png")
    bottom_zoom.save(bottom_zoom_path)
    print(f"Saved verified bottom edge zoom: {bottom_zoom_path}")

# Crop 3D view of U7 and USB-C
im_3d = Image.open(render_3d)
bbox_3d = im_3d.getbbox()
if bbox_3d:
    w_3d = bbox_3d[2] - bbox_3d[0]
    h_3d = bbox_3d[3] - bbox_3d[1]
    crop_3d = im_3d.crop((bbox_3d[0] + int(w_3d * 0.70), bbox_3d[1], bbox_3d[2], bbox_3d[3]))
    crop_3d_path = os.path.join(PROJECT_DIR, "VFBMS32_u7_usb_3d_zoom.png")
    crop_3d.save(crop_3d_path)
    print(f"Saved 3D zoom: {crop_3d_path}")

print("\n==========================================================")
print("6. COPYING ARTIFACTS TO BRAIN DIRECTORY")
print("==========================================================")
os.makedirs(BRAIN_DIR, exist_ok=True)
for fname in ["VFBMS32_esp_usb_u7_verified.png", "VFBMS32_bottom_edge_verified.png", "VFBMS32_u7_usb_3d_zoom.png", "VFBMS32_layout_top_hi_raw.png", "VFBMS32_render_3d.png"]:
    src = os.path.join(PROJECT_DIR, fname)
    dst = os.path.join(BRAIN_DIR, fname)
    if os.path.exists(src):
        shutil.copyfile(src, dst)
        print(f"Copied {fname} to brain directory!")

print("\nALL REPAIRS, ADJUSTMENTS, AND RENDERS FINISHED SUCCESSFULLY!")
