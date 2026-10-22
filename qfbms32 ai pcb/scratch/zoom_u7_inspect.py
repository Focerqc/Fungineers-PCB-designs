from PIL import Image

# Open high-res user photo IMG_0916 and master reference
master = Image.open('_reference/vfbms32_v1_2_master_reference.png')
# Crop around px x: 700..880, y: 30..180
crop_u7 = master.crop((700, 30, 884, 180))
# Resize 4x with nearest or bicubic to inspect
crop_u7_large = crop_u7.resize((crop_u7.width * 4, crop_u7.height * 4), Image.Resampling.NEAREST)
crop_u7_large.save('scratch/u7_zoomed_x4.png')
print("Saved scratch/u7_zoomed_x4.png")

# Also do real HD photo if available
hd = Image.open('_reference/vfbms32_real_top_hd.png')
w, h = hd.size
crop_hd = hd.crop((int(w * 0.75), int(h * 0.1), int(w * 0.98), int(h * 0.6)))
crop_hd_large = crop_hd.resize((crop_hd.width * 4, crop_hd.height * 4), Image.Resampling.NEAREST)
crop_hd_large.save('scratch/u7_hd_zoomed_x4.png')
print("Saved scratch/u7_hd_zoomed_x4.png")
