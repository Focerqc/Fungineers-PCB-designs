from PIL import Image

img = Image.open(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\_reference\vfbms32_cad_top_reference_rotated.jpg")
w, h = img.size
print("CAD top ref size:", w, h)
crop_cad = img.crop((int(w * 0.75), 0, w, int(h * 0.5)))
crop_cad.save(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\inspect_usb_cad.png")
