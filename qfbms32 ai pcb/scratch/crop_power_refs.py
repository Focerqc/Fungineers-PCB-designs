from PIL import Image

def crop_power_stage(img_path, out_path, box):
    im = Image.open(img_path)
    crop = im.crop(box)
    crop.save(out_path)
    print(f"Saved {out_path}: {crop.size}")

# For master reference (size ~1500x350)
im_m = Image.open(r"_reference/vfbms32_v1_2_master_reference.png")
print("Master ref size:", im_m.size)
# Power stage is left ~35% of image
crop_power_stage(
    r"_reference/vfbms32_v1_2_master_reference.png",
    r"scratch/ref_power_stage.png",
    (0, 0, int(im_m.width * 0.35), im_m.height)
)

im_c = Image.open(r"_reference/vfbms32_cad_top_reference_rotated.jpg")
print("CAD ref size:", im_c.size)
crop_power_stage(
    r"_reference/vfbms32_cad_top_reference_rotated.jpg",
    r"scratch/cad_power_stage.png",
    (0, 0, int(im_c.width * 0.35), im_c.height)
)
