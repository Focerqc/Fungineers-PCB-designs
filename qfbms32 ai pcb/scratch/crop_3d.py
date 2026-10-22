from PIL import Image

im = Image.open(r'C:\Users\quinn\.gemini\antigravity-ide\brain\805bb937-8903-4245-8343-56aa9959b3c4\VFBMS32_render_3d.png')
print("3D render size:", im.size)
# Save crop of the connectors
crop = im.crop((100, 100, 700, 700))
crop.save(r'c:\Users\quinn\Desktop\AI PCB CAD\prev_3d_crop.png')
print("Saved prev_3d_crop.png")
