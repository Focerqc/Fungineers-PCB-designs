import os
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\7bc5fde5-e6cf-413a-9764-f83c0e8df3ae"

ref_master = os.path.join(pcb_dir, "_reference", "vfbms32_v1_2_master_reference.png")
if os.path.exists(ref_master):
    im = Image.open(ref_master)
    print("Master ref size:", im.size)
    mw, mh = im.size
    # Crop X: 26..33mm, Y: 2..20mm
    mx0 = int((26.0 / 130.0) * mw)
    mx1 = int((33.0 / 130.0) * mw)
    my0 = int((2.0 / 32.0) * mh)
    my1 = int((20.0 / 32.0) * mh)
    crop = im.crop((mx0, my0, mx1, my1))
    crop.save(os.path.join(brain_dir, "master_ref_crop.png"))
    print("Saved master_ref_crop.png")
