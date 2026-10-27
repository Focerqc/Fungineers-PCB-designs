import os
import glob
import shutil

# 1. Clean up root loose test/crop files
root_dir = r"c:\Users\quinn\Desktop\AI PCB CAD"
root_patterns = [
    "crop_exact_*.png",
    "crop_f_*.png",
    "find_m_rot_*.png",
    "find_m_rot_*.kicad_prl",
    "prev_*.png",
    "raw_left_crop.png",
    "test_align_*.png",
    "test_crop.png",
    "test_current.png",
    "test_exact_*.png",
    "test_f_off_*.png",
]

deleted_root = []
for pat in root_patterns:
    for f in glob.glob(os.path.join(root_dir, pat)):
        try:
            os.remove(f)
            deleted_root.append(os.path.basename(f))
        except Exception as e:
            print(f"Error removing {f}: {e}")

print(f"Removed {len(deleted_root)} loose test/crop files from root.")

# 2. In Q VFBMS32 AI PCB\_reference:
# Organize user uploaded original photos into 'original_photos'
ref_dir = os.path.join(root_dir, "Q VFBMS32 AI PCB", "_reference")
orig_photos_dir = os.path.join(ref_dir, "user_photos")
os.makedirs(orig_photos_dir, exist_ok=True)

# Move user photos: IMG_0912.jpg, etc.
for img_name in ["IMG_0912.jpg", "IMG_0913.jpg", "IMG_0916.jpg", "IMG_0923.jpg", "IMG_0927.jpg"]:
    p = os.path.join(ref_dir, img_name)
    if os.path.exists(p):
        shutil.move(p, os.path.join(orig_photos_dir, img_name))
        print(f"Moved {img_name} to user_photos/")

# Remove intermediate thumbnails and contrast crops from _reference
temp_crops = glob.glob(os.path.join(ref_dir, "thumb_*.jpg")) + \
             glob.glob(os.path.join(ref_dir, "contrast_*.png")) + \
             glob.glob(os.path.join(ref_dir, "chip_rot*.png"))

for tc in temp_crops:
    try:
        os.remove(tc)
    except Exception as e:
        print(f"Error removing {tc}: {e}")

print(f"Cleaned up {len(temp_crops)} temporary thumb/contrast files in _reference.")
