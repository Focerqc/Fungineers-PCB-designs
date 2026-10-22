import subprocess
import os
import shutil
from PIL import Image

project_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB"
pcb_path = os.path.join(project_dir, "VFBMS32.kicad_pcb")
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"

brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\b988a972-63be-4423-9bf0-ac3c0e64f999"
os.makedirs(brain_dir, exist_ok=True)

# 1. Main 3D render
out_3d = os.path.join(project_dir, "VFBMS32_render_3d.png")
brain_3d = os.path.join(brain_dir, "VFBMS32_render_3d.png")

print("Rendering main 3D view...")
subprocess.run([
    kicad_cli, "pcb", "render",
    "--perspective",
    "--rotate", "-25,0,25",
    "--floor",
    "--width", "3600", "--height", "1600",
    "--background", "transparent",
    "-o", out_3d, pcb_path
], check=True)

if os.path.exists(out_3d):
    im = Image.open(out_3d)
    bbox = im.getbbox()
    if bbox:
        pad = 40
        box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(im.width, bbox[2]+pad), min(im.height, bbox[3]+pad))
        im.crop(box).save(out_3d)
    shutil.copyfile(out_3d, brain_3d)
    print("Saved main 3D render:", out_3d)

# 2. Render right zoom (ESP32-C3 & USB-C close-up)
out_esp_zoom = os.path.join(project_dir, "VFBMS32_esp_usb_zoom.png")
brain_esp_zoom = os.path.join(brain_dir, "VFBMS32_esp_usb_zoom.png")

print("Rendering right zoom...")
subprocess.run([
    kicad_cli, "pcb", "render",
    "--perspective",
    "--rotate", "-28,0,20",
    "--floor",
    "--width", "3600", "--height", "2000",
    "--background", "transparent",
    "-o", out_esp_zoom, pcb_path
], check=True)

if os.path.exists(out_esp_zoom):
    im_z = Image.open(out_esp_zoom)
    bbox = im_z.getbbox()
    if bbox:
        # Crop the right ~45% of the board where ESP32, USB-C, U7, and headers are
        bw = bbox[2] - bbox[0]
        crop_box = (int(bbox[0] + bw * 0.55), max(0, bbox[1] - 20), min(im_z.width, bbox[2] + 20), min(im_z.height, bbox[3] + 20))
        im_z.crop(crop_box).save(out_esp_zoom)
    shutil.copyfile(out_esp_zoom, brain_esp_zoom)
    print("Saved ESP/USB zoom render:", out_esp_zoom)
