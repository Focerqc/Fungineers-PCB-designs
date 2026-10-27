from PIL import Image
import numpy as np

def find_board_bbox(img_path):
    img = Image.open(img_path).convert("RGB")
    arr = np.array(img)
    # background is dark or light wood
    # let's find lines with significant content or print min/max
    print(img_path, "size:", img.size)

find_board_bbox("_reference/vfbms32_real_top_hd.png")
find_board_bbox("_reference/vfbms32_v1_2_master_reference.png")
