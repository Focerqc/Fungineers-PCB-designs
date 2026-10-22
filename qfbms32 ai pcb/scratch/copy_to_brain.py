import shutil
import os

brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\a11d5216-ec23-4de0-9ff6-ae2ffbd1fda7"
project_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB"

files_to_copy = [
    "VFBMS32_buzzer_verified.png",
    "VFBMS32_esp_usb_u7_verified.png",
    "VFBMS32_layout_top_hi_raw.png",
    "VFBMS32_render_3d.png"
]

for fname in files_to_copy:
    src = os.path.join(project_dir, fname)
    dst = os.path.join(brain_dir, fname)
    if os.path.exists(src):
        shutil.copyfile(src, dst)
        print(f"Copied {fname} to brain directory: {dst}")
