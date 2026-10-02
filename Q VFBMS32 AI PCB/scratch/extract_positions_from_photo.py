from PIL import Image

im = Image.open(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\_reference\user_photos\image_3023b2.png")

origin_x = 22.0
origin_y = 39.0
scale_x = (957.0 - 22.0) / 130.0  # 7.1923 px/mm
scale_y = (275.0 - 39.0) / 32.0   # 7.375 px/mm

def mm_to_px(x_mm, y_mm):
    return origin_x + x_mm * scale_x, origin_y + y_mm * scale_y

def px_to_mm(px, py):
    return (px - origin_x) / scale_x, (py - origin_y) / scale_y

# Let's inspect features by coordinates
features = [
    ("XT30_CHG", 5.2, 7.45),
    ("XT30_BAT", 4.0, 24.55),
    ("R_SH1_vert", 10.6, 16.0),
    ("Q1_MOSFET", 18.5, 6.4),
    ("R_SH2_horiz", 18.5, 15.0),
    ("U_DRIVER", 18.5, 18.5),
    ("Q2_MOSFET", 20.0, 25.6),
    ("FUSE_18A", 12.8, 24.5),
    ("U_BQ2", 48.0, 13.5),
    ("L1_181", 66.0, 7.5),
    ("C_TAN", 74.0, 7.5),
    ("U_BUCK", 66.0, 14.5),
    ("U_BQ1", 87.5, 13.5),
    ("U_ESP1", 106.5, 8.5),
    ("J_USB1", 125.0, 3.2),
    ("U7", 124.8, 12.0)
]

for name, x, y in features:
    px, py = mm_to_px(x, y)
    print(f"{name:15s}: mm=({x:5.1f}, {y:5.1f}) -> px=({px:5.0f}, {py:5.0f})")
