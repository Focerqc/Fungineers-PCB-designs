import os
from PIL import Image, ImageDraw, ImageFont

brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\7bc5fde5-e6cf-413a-9764-f83c0e8df3ae"

img_3d_zoom = Image.open(os.path.join(brain_dir, "zoom_new_0603_hi.png")).convert("RGBA")
# Also load cad_raw_crop or cad_boxes_crop
cad_crop = Image.open(os.path.join(brain_dir, "cad_boxes_crop.png")).convert("RGBA")

# Let's create an annotated card
target_h = 600
scale_3d = target_h / img_3d_zoom.height
im_3d_scaled = img_3d_zoom.resize((int(img_3d_zoom.width * scale_3d), target_h), Image.Resampling.LANCZOS)

scale_cad = target_h / cad_crop.height
im_cad_scaled = cad_crop.resize((int(cad_crop.width * scale_cad), target_h), Image.Resampling.LANCZOS)

card_w = im_cad_scaled.width + im_3d_scaled.width + 420
card_h = target_h + 60

card = Image.new("RGBA", (card_w, card_h), (20, 24, 32, 255))
draw = ImageDraw.Draw(card)

font_h = ImageFont.load_default()

# Paste CAD
x = 20
y = 40
card.paste(im_cad_scaled, (x, y))
draw.text((x + 10, 15), "BOX ANNOTATION (CAD REF)", fill=(78, 161, 255), font=font_h)

# Paste 3D
x += im_cad_scaled.width + 20
card.paste(im_3d_scaled, (x, y))
draw.text((x + 10, 15), "PLACED 0603 FOOTPRINTS (3D)", fill=(80, 250, 120), font=font_h)

# Details text column
x += im_3d_scaled.width + 25
draw.text((x, 15), "PLACED COMPONENT SPECIFICATIONS", fill=(255, 215, 0), font=font_h)

specs = [
    ("1. R_SSR1 (Color 1 Box 3)", [
        "Position: (29.20 mm, 4.05 mm)",
        "Footprint: R_0603_1608Metric (0.0°)",
        "Marking: 'X10' -> EIA-96 '01X' (10 Ω, 1%)",
        "Role: SSRelay / Precharge gate drive resistor"
    ], (78, 161, 255)),
    ("2. R_G1 (Color 1 Box 2)", [
        "Position: (29.50 mm, 7.60 mm)",
        "Footprint: R_0603_1608Metric (0.0°)",
        "Marking: 'X10' -> EIA-96 '01X' (10 Ω, 1%)",
        "Role: Q1 (CHG FET) Gate drive resistor"
    ], (78, 161, 255)),
    ("3. R_GS1 (Color 2 Box 1)", [
        "Position: (29.50 mm, 8.95 mm)",
        "Footprint: R_0603_1608Metric (0.0°)",
        "Marking: '474' (underlined) = 470 kΩ, 1%",
        "Role: Q1 Gate-Source pull-down / bleeder"
    ], (255, 107, 107)),
    ("4. R_SEC1 (Color 1 Box 1)", [
        "Position: (29.75 mm, 17.20 mm)",
        "Footprint: R_0603_1608Metric (0.0°)",
        "Marking: 'X10' -> EIA-96 '01X' (10 Ω, 1%)",
        "Role: Secondary / discharge snubber resistor"
    ], (78, 161, 255))
]

cur_y = 50
for title, lines, color in specs:
    draw.text((x, cur_y), title, fill=color, font=font_h)
    cur_y += 18
    for line in lines:
        draw.text((x + 12, cur_y), line, fill=(210, 220, 230), font=font_h)
        cur_y += 16
    cur_y += 10

out_card = os.path.join(brain_dir, "col1_col2_detail_card.png")
card.save(out_card)
print(f"Saved detail card to {out_card}")
