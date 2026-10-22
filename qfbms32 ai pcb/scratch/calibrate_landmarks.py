from PIL import Image

ref_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\_reference\vfbms32_v1_2_master_reference.png"
img = Image.open(ref_path)
w, h = img.size

# Landmarks to find:
# 1. Left edge of PCB: ~23 px
# 2. Right edge of PCB: ~884 px
# Width = 884 - 23 = 861 px for 130.0 mm -> 6.623 px/mm
# 3. Top edge of PCB: ~34 px
# 4. Bottom edge of PCB: ~254 px
# Height = 254 - 34 = 220 px for 32.0 mm -> 6.875 px/mm

x_origin = 23.0
x_scale = 861.0 / 130.0  # ~6.623 px/mm

y_origin = 34.0
y_scale = 220.0 / 32.0   # ~6.875 px/mm

def px_to_mm(px, py):
    x_mm = (px - x_origin) / x_scale
    y_mm = (py - y_origin) / y_scale
    return round(x_mm, 2), round(y_mm, 2)

# Test key components:
landmarks = {
    "XT30_TOP": (58, 85),
    "XT30_BOT": (50, 203),
    "Q1_TOLL": (158, 80),
    "R_SH2_HORIZ": (165, 137),
    "Q2_TOLL": (168, 208),
    "J_COMM1": (245, 189),
    "U_BQ2": (342, 126),
    "U_BOOST1": (415, 69),
    "L1": (475, 78),
    "C_TAN1": (520, 78),
    "U_BUCK1": (475, 142),
    "L2_ROUND": (605, 52),
    "U_BQ1": (625, 126),
    "ESP32": (735, 92),
    "USB_C": (820, 56),
    "U7_CH340": (840, 118),
}

print("Physical coordinate mapping from master reference photo:")
for name, (px, py) in landmarks.items():
    x_mm, y_mm = px_to_mm(px, py)
    print(f"  {name:15}: px=({px:3}, {py:3}) -> mm=({x_mm:5.2f}, {y_mm:5.2f})")
