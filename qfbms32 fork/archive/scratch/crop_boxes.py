from PIL import Image

cad = Image.open(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\_reference\vfbms32_cad_top_reference_rotated.png")
sx = cad.width / 130.0
sy = cad.height / 32.0

# User boxes:
# 1: X=90.05, Y=1.10, W=1.00, H=1.60
# 2: X=90.08, Y=4.53, W=0.85, H=1.55
# 3: X=86.55, Y=4.47, W=0.80, H=1.45

# Let's crop tight around each box and save
for i, (bx, by, bw, bh) in enumerate([
    (90.05, 1.10, 1.00, 1.60),
    (90.08, 4.53, 0.85, 1.55),
    (86.55, 4.47, 0.80, 1.45),
    (88.40, 2.70, 5.50, 5.50) # Buzzer area
], 1):
    x1 = int((bx - bw) * sx)
    y1 = int((by - bh) * sy)
    x2 = int((bx + bw) * sx)
    y2 = int((by + bh) * sy)
    c_cad = cad.crop((x1, y1, x2, y2))
    c_cad.save(rf"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\scratch\box_{i}_cad.png")
    print(f"Box {i} saved")
