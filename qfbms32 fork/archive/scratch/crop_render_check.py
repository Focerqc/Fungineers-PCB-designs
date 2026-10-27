from PIL import Image
import os

img_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\test_render_esp_usb.png"
img = Image.open(img_path)
w, h = img.size
print(f"Render dimensions: {w}x{h}")

# The board is angled: left is bottom-left, right is top-right in this perspective (-25, 0, 25).
# Right area is around x: 60% to 100%, y: 0% to 70%
crop_right = img.crop((int(w * 0.60), int(h * 0.05), int(w * 0.98), int(h * 0.70)))
crop_right.save(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\crop_right_render.png")
print("Saved crop_right_render.png")
