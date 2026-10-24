import os
from PIL import Image, ImageDraw, ImageFont

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\7bc5fde5-e6cf-413a-9764-f83c0e8df3ae"

cad = Image.open(os.path.join(pcb_dir, "_reference", "vfbms32_cad_top_reference_rotated.png"))
real = Image.open(os.path.join(pcb_dir, "_reference", "vfbms32_real_top_hd.png"))

# Board dimensions: 130 x 32
# Column is at X: 27..32mm, Y: 1..20mm
cw, ch = cad.size
cad_col = cad.crop((int(27.0/130*cw), int(1.0/32*ch), int(32.5/130*cw), int(20.0/32*ch)))

rw, rh = real.size
# Let's find real alignment
real_col = real.crop((int(27.0/130*rw), int(1.0/32*rh), int(32.5/130*rw), int(20.0/32*rh)))

# Scale both to same height
target_h = 800
cad_col_scaled = cad_col.resize((int(cad_col.width * target_h / cad_col.height), target_h), Image.Resampling.LANCZOS)
real_col_scaled = real_col.resize((int(real_col.width * target_h / real_col.height), target_h), Image.Resampling.LANCZOS)

# Create side by side
comb = Image.new("RGB", (cad_col_scaled.width + real_col_scaled.width + 30, target_h + 40), (20, 25, 30))
comb.paste(cad_col_scaled, (10, 30))
comb.paste(real_col_scaled, (cad_col_scaled.width + 20, 30))

draw = ImageDraw.Draw(comb)
font = ImageFont.load_default()
draw.text((10, 10), "CAD REFERENCE (130x32)", fill=(100, 200, 255), font=font)
draw.text((cad_col_scaled.width + 20, 10), "REAL TOP HD", fill=(100, 255, 100), font=font)

out_p = os.path.join(brain_dir, "cad_vs_real_col.png")
comb.save(out_p)
print(f"Saved side-by-side to {out_p}")
