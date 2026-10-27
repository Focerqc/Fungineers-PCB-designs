from PIL import Image

ref_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\_reference\vfbms32_v1_2_master_reference.png"
img = Image.open(ref_path)

# Let's crop from the right edge of Q1/Q2 up to JST connector:
# In pixel coordinates from measure_power_grid:
# X: 140 to 240, Y: 10 to 180
crop = img.crop((140, 10, 240, 180))
crop_zoom = crop.resize((crop.width * 4, crop.height * 4), Image.Resampling.LANCZOS)
crop_zoom.save(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\power_inter_stage_zoom.png")
print("Saved power_inter_stage_zoom.png")
