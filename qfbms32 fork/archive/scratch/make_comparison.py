from PIL import Image, ImageDraw, ImageFont
import os

brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\0b8fcda9-1947-42aa-99e4-1151d2cb92f0"
crop_3d_old = Image.open("qfbms32 ai pcb/scratch/crop_3d_s1_s2.png")
crop_3d_new = Image.open("qfbms32 ai pcb/scratch/zoom_new_rs1_rs2.png")
crop_real = Image.open("qfbms32 ai pcb/scratch/zoom_s1_s2_real.png")

# Resize real to match height roughly
target_h = crop_3d_new.height
scale = target_h / crop_real.height
real_resized = crop_real.resize((int(crop_real.width * scale), target_h), Image.Resampling.LANCZOS)

# Create combined canvas
pad = 10
total_w = crop_3d_old.width + crop_3d_new.width + real_resized.width + pad * 4
canvas_h = target_h + 50
canvas = Image.new("RGB", (total_w, canvas_h), (25, 30, 36))
draw = ImageDraw.Draw(canvas)

font = ImageFont.load_default()

# Paste images
x = pad
canvas.paste(crop_3d_old, (x, 35))
draw.text((x + 10, 10), "BEFORE (0603 C_S1, C_S2)", fill=(255, 100, 100), font=font)

x += crop_3d_old.width + pad
canvas.paste(crop_3d_new, (x, 35))
draw.text((x + 10, 10), "AFTER (0805 R_S1, R_S2 '1000')", fill=(100, 255, 100), font=font)

x += crop_3d_new.width + pad
canvas.paste(real_resized, (x, 35))
draw.text((x + 10, 10), "REAL PCB (Physical)", fill=(100, 200, 255), font=font)

out_p = os.path.join(brain_dir, "s1_s2_comparison.png")
canvas.save(out_p)
print(f"Saved side-by-side comparison to {out_p}")
