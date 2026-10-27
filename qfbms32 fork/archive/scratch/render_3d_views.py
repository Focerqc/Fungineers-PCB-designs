import subprocess, os, shutil
from PIL import Image

project_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB"
pcb_path = os.path.join(project_dir, "VFBMS32.kicad_pcb")
kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
out_3d = os.path.join(project_dir, "VFBMS32_render_3d.png")
brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\805bb937-8903-4245-8343-56aa9959b3c4"
brain_3d = os.path.join(brain_dir, "VFBMS32_render_3d.png")

print("Rendering 3D perspective view...")
subprocess.run([
    kicad_cli, "pcb", "render",
    "--perspective",
    "--rotate", "-25,0,25",
    "--floor",
    "--width", "3600", "--height", "1600",
    "--background", "transparent",
    "-o", out_3d, pcb_path
], check=True)

# Autocrop transparent margins with 40px padding
if os.path.exists(out_3d):
    im = Image.open(out_3d)
    bbox = im.getbbox()
    if bbox:
        pad = 40
        box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(im.width, bbox[2]+pad), min(im.height, bbox[3]+pad))
        im.crop(box).save(out_3d)
        print(f"Saved {out_3d}, cropped size: {im.size}")

# Copy to brain dir
os.makedirs(brain_dir, exist_ok=True)
shutil.copyfile(out_3d, brain_3d)
print(f"Copied to {brain_3d}")

# Also render a zoom-in on the connectors to clearly show the flush mating face and edge clearance
out_zoom = os.path.join(project_dir, "VFBMS32_xt30_zoom.png")
brain_zoom = os.path.join(brain_dir, "VFBMS32_xt30_zoom.png")

subprocess.run([
    kicad_cli, "pcb", "render",
    "--perspective",
    "--rotate", "-35,0,15",
    "--floor",
    "--width", "2800", "--height", "1600",
    "--background", "transparent",
    "-o", out_zoom, pcb_path
], check=True)

if os.path.exists(out_zoom):
    im_z = Image.open(out_zoom)
    bbox = im_z.getbbox()
    if bbox:
        # Crop specifically the left half where the connectors sit
        crop_w = int((bbox[2] - bbox[0]) * 0.45)
        crop_box = (max(0, bbox[0] - 20), max(0, bbox[1] - 20), bbox[0] + crop_w, min(im_z.height, bbox[3] + 20))
        im_z.crop(crop_box).save(out_zoom)
        shutil.copyfile(out_zoom, brain_zoom)
        print(f"Saved connector zoom render to {brain_zoom}")
