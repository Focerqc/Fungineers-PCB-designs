import os
from PIL import Image, ImageDraw, ImageFont

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\7bc5fde5-e6cf-413a-9764-f83c0e8df3ae"

im12 = Image.open(os.path.join(pcb_dir, "_reference", "user_photos", "IMG_0912.jpg"))
w, h = im12.size

base_x = int(w * 0.2)
base_y = int(h * 0.1)

crop = im12.crop((base_x + 300, base_y + 300, base_x + 800, base_y + 1600))
draw = ImageDraw.Draw(crop)
font = ImageFont.load_default()

# draw vertical and horizontal ruler lines every 50 pixels
for y in range(0, crop.height, 50):
    draw.line([(0, y), (crop.width, y)], fill=(128, 128, 128, 64))
    draw.text((5, y+2), f"y={y}", fill=(255, 255, 0), font=font)

crop.save(os.path.join(brain_dir, "crop12_ruler.jpg"))
print("Saved crop12_ruler.jpg")
