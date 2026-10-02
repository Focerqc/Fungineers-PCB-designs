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

print("=== STEP 1: INSPECTING J_USB1 BEFORE REPAIR ===")
with open(PCB_PATH, "r", encoding="utf-8") as f:
    pcb_content = f.read()

# Parse current J_USB1 footprint
m_usb_before = re.search(r'\(footprint [^\n]*\n[\s\S]*?\"Reference\" \"J_USB1\"[\s\S]*?\n\t\)', pcb_content)
if m_usb_before:
    pads_before = re.findall(r'\(pad\s+"([^"]*)"\s+([^\s]+)\s+([^\s]+)\s+\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', m_usb_before.group(0))
    print(f"Before repair: J_USB1 has {len(pads_before)} pads.")
    unique_pad_positions = set((p[3], p[4]) for p in pads_before)
    print(f"Unique pad coordinates count: {len(unique_pad_positions)} (corrupted if 1: all pads collapsed to same offset)")
else:
    print("J_USB1 not found in PCB!")

print("\n=== STEP 2: LOADING CLEAN USB-C FOOTPRINT ===")
with open(USB_MOD_PATH, "r", encoding="utf-8") as f:
    mod_lines = f.readlines()

# Convert kicad_mod to PCB embedded footprint s-expression
# 1st line: (footprint "USB_C_Receptacle_16P"
# inner lines indented by \t
new_usb_lines = ['\t(footprint "USB_C_Receptacle_16P"\n',
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
                 '\t\t)\n']

# Add attributes, shapes, pads, and 3D model from mod_lines
skip_header = True
for line in mod_lines[1:]:
    if '(attr smd)' in line:
        skip_header = False
    if not skip_header:
        if line.strip() == ')':
            new_usb_lines.append('\t)\n')
        else:
            new_usb_lines.append('\t' + line)

usb_fp_reconstructed = "".join(new_usb_lines)

print("=== STEP 3: APPLYING UPDATES TO VFBMS32.kicad_pcb ===")
# Define bottom row component groups to shift down by +1.1 mm (delta Y)
DELTA_Y_BOTTOM = 1.10

jst_refs = {"J_COMM1", "J_CELL4", "J_CELL3", "J_CELL2", "J_CELL1", "J_T4", "J_T3", "J_T2", "J_T1"}
rb_refs = {f"R_B{i}" for i in range(1, 33)}
rf_refs = {f"R_F{i}" for i in range(1, 33)}
shift_refs = jst_refs | rb_refs | rf_refs

with open(PCB_PATH, "r", encoding="utf-8") as f:
    pcb_lines = f.readlines()

new_pcb_lines = []
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
                print("-> Replacing J_USB1 with fully defined USB_C_Receptacle_16P at (125.0, 3.2, rot=180)")
                new_pcb_lines.append(usb_fp_reconstructed)
            elif ref == "U7":
                print("-> Adjusting U7 (DUB-8) position to (124.0, 14.0, rot=0)")
                # Ensure U7 is at (at 124 14)
                fp_text = re.sub(r'\(footprint "Package_DIP:SMDIP-8_W9.53mm"[\s\S]*?\(at\s+[0-9\.\-]+\s+[0-9\.\-]+(?:\s+[0-9\.\-]+)?\)',
                                 '\t(footprint "Package_DIP:SMDIP-8_W9.53mm"\n\t\t(layer "F.Cu")\n\t\t(uuid "28929e53-d3ff-4d4a-8621-05c659c8e34f")\n\t\t(at 124 14)',
                                 fp_text)
                new_pcb_lines.append(fp_text)
            elif ref in shift_refs:
                # Nudge position Y by DELTA_Y_BOTTOM
                def shift_at(m):
                    x = float(m.group(1))
                    y = float(m.group(2))
                    rot_str = f" {m.group(3)}" if m.group(3) is not None else ""
                    return f"(at {x} {round(y + DELTA_Y_BOTTOM, 3)}{rot_str})"

                # Only replace the top-level footprint (at ...) statement
                # The top-level at is within the first 6 lines of footprint
                lines_fp = fp_text.splitlines(keepends=True)
                for i in range(min(6, len(lines_fp))):
                    if re.search(r'^\s*\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)(?:\s+([0-9\.\-]+))?\)', lines_fp[i]):
                        lines_fp[i] = re.sub(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)(?:\s+([0-9\.\-]+))?\)', shift_at, lines_fp[i], count=1)
                        break
                new_pcb_lines.append("".join(lines_fp))
            else:
                new_pcb_lines.append(fp_text)
    else:
        new_pcb_lines.append(line)

with open(PCB_PATH, "w", encoding="utf-8") as f:
    f.writelines(new_pcb_lines)

print("Saved updated VFBMS32.kicad_pcb successfully!")

print("\n=== STEP 4: VERIFYING J_USB1 AFTER REPAIR ===")
with open(PCB_PATH, "r", encoding="utf-8") as f:
    updated_pcb = f.read()

m_usb_after = re.search(r'\(footprint [^\n]*\n[\s\S]*?\"Reference\" \"J_USB1\"[\s\S]*?\n\t\)', updated_pcb)
if m_usb_after:
    pads_after = re.findall(r'\(pad\s+"([^"]*)"\s+([^\s]+)\s+([^\s]+)\s+\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)', m_usb_after.group(0))
    print(f"After repair: J_USB1 has {len(pads_after)} pads.")
    for p in pads_after:
        print(f"  Pad {p[0]:4} | type: {p[1]:15} | shape: {p[2]:10} | offset: ({p[3]}, {p[4]})")
    unique_offsets = set((p[3], p[4]) for p in pads_after)
    print(f"Unique pad offsets count: {len(unique_offsets)}")

print("\n=== STEP 5: RENDERING 2D TOP-DOWN AND 3D PERSPECTIVE VIEWS ===")
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

# Crop top-right corner showing J_USB1 pads, U7 clearance, ESP32
im_top = Image.open(render_top)
bbox = im_top.getbbox()
if bbox:
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    # Crop top-right corner (X: ~75% to 100%, Y: top 65%)
    crop_x1 = bbox[0] + int(w * 0.75)
    crop_x2 = bbox[2] + 20
    crop_y1 = max(0, bbox[1] - 20)
    crop_y2 = bbox[1] + int(h * 0.65)
    corner_zoom = im_top.crop((crop_x1, crop_y1, crop_x2, crop_y2))
    corner_zoom_path = os.path.join(PROJECT_DIR, "VFBMS32_esp_usb_u7_verified.png")
    corner_zoom.save(corner_zoom_path)
    print(f"Saved verified top-right zoom: {corner_zoom_path}")

    # Crop bottom edge to verify 1mm clearance
    crop_bx1 = bbox[0] + int(w * 0.20)
    crop_bx2 = bbox[2] - int(w * 0.05)
    crop_by1 = bbox[1] + int(h * 0.50)
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

print("\n=== STEP 6: COPYING ARTIFACTS TO BRAIN DIRECTORY ===")
os.makedirs(BRAIN_DIR, exist_ok=True)
for fname in ["VFBMS32_esp_usb_u7_verified.png", "VFBMS32_bottom_edge_verified.png", "VFBMS32_u7_usb_3d_zoom.png", "VFBMS32_layout_top_hi_raw.png", "VFBMS32_render_3d.png"]:
    src = os.path.join(PROJECT_DIR, fname)
    dst = os.path.join(BRAIN_DIR, fname)
    if os.path.exists(src):
        shutil.copyfile(src, dst)
        print(f"Copied {fname} to brain directory!")

print("\nALL TASKS COMPLETED SUCCESSFULLY!")
