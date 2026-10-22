from PIL import Image, ImageDraw

ref_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\_reference\vfbms32_v1_2_master_reference.png"
img = Image.open(ref_path)

# Crop power delivery stage (pixel X: 370 to 590, Y: 10 to 180)
crop_pwr = img.crop((370, 10, 590, 180)).convert("RGB")
draw = ImageDraw.Draw(crop_pwr)
for x in range(0, crop_pwr.width, 20):
    draw.line([(x, 0), (x, crop_pwr.height)], fill=(255, 0, 0, 80), width=1)
    draw.text((x+1, 2), f"{x}", fill=(255, 255, 0))
for y in range(0, crop_pwr.height, 20):
    draw.line([(0, y), (crop_pwr.width, y)], fill=(0, 255, 0, 80), width=1)
    draw.text((2, y+1), f"{y}", fill=(0, 255, 255))
crop_pwr.resize((crop_pwr.width * 2, crop_pwr.height * 2), Image.Resampling.NEAREST).save(
    r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\power_delivery_stage_grid.png"
)

print("Saved power_delivery_stage_grid.png")
