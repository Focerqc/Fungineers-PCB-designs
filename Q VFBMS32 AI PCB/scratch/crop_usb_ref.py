from PIL import Image

img = Image.open(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\_reference\vfbms32_real_top_hd.png")
w, h = img.size
print("Real top HD size:", w, h)

# USB-C is in top right
# Let's crop the top-right corner
crop_usb = img.crop((int(w * 0.8), 0, w, int(h * 0.6)))
crop_usb.save(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\inspect_usb_real.png")
print("Saved inspect_usb_real.png")
