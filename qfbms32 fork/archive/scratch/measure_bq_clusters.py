from PIL import Image, ImageDraw

ref_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\_reference\vfbms32_v1_2_master_reference.png"
img = Image.open(ref_path)

# Crop U_BQ2 region (pixel X: 260 to 450, Y: 15 to 220)
crop_bq2 = img.crop((260, 15, 450, 220)).convert("RGB")
draw2 = ImageDraw.Draw(crop_bq2)
for x in range(0, crop_bq2.width, 20):
    draw2.line([(x, 0), (x, crop_bq2.height)], fill=(255, 0, 0, 80), width=1)
    draw2.text((x+1, 2), f"{x}", fill=(255, 255, 0))
for y in range(0, crop_bq2.height, 20):
    draw2.line([(0, y), (crop_bq2.width, y)], fill=(0, 255, 0, 80), width=1)
    draw2.text((2, y+1), f"{y}", fill=(0, 255, 255))
crop_bq2.resize((crop_bq2.width * 2, crop_bq2.height * 2), Image.Resampling.NEAREST).save(
    r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\bq2_cluster_grid.png"
)

# Crop U_BQ1 region (pixel X: 570 to 760, Y: 15 to 220)
crop_bq1 = img.crop((570, 15, 760, 220)).convert("RGB")
draw1 = ImageDraw.Draw(crop_bq1)
for x in range(0, crop_bq1.width, 20):
    draw1.line([(x, 0), (x, crop_bq1.height)], fill=(255, 0, 0, 80), width=1)
    draw1.text((x+1, 2), f"{x}", fill=(255, 255, 0))
for y in range(0, crop_bq1.height, 20):
    draw1.line([(0, y), (crop_bq1.width, y)], fill=(0, 255, 0, 80), width=1)
    draw1.text((2, y+1), f"{y}", fill=(0, 255, 255))
crop_bq1.resize((crop_bq1.width * 2, crop_bq1.height * 2), Image.Resampling.NEAREST).save(
    r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\bq1_cluster_grid.png"
)

print("Saved bq2_cluster_grid.png and bq1_cluster_grid.png")
