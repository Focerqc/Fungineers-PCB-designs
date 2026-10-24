from PIL import Image

for name, fname in [("real_top", "_reference/vfbms32_real_top_hd.png"), 
                    ("v1_2", "_reference/vfbms32_v1_2_master_reference.png"),
                    ("3d_top", "qfbms32_3d_top.png")]:
    img = Image.open(fname)
    w, h = img.size
    # approximate normalized coords:
    # box 1: x_norm = 13.4 / 130 = 0.103, y_norm = 30.7 / 32 = 0.959
    # box 2: x_norm = 15.1 / 130 = 0.116, y_norm = 1.13 / 32 = 0.035
    
    # We can crop around these normalized coords
    x1, y1 = int(0.103 * w), int(0.959 * h)
    x2, y2 = int(0.116 * w), int(0.035 * h)
    
    # crop box 1
    cw, ch = int(w * 0.1), int(h * 0.25)
    c1 = img.crop((max(0, x1 - cw//2), max(0, y1 - ch//2), min(w, x1 + cw//2), min(h, y1 + ch//2)))
    c1.save(f"scratch/crop_box1_{name}.png")
    
    # crop box 2
    c2 = img.crop((max(0, x2 - cw//2), max(0, y2 - ch//2), min(w, x2 + cw//2), min(h, y2 + ch//2)))
    c2.save(f"scratch/crop_box2_{name}.png")
    print(f"Saved crops for {name}")
