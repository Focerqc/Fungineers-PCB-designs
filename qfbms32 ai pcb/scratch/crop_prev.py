from PIL import Image

im = Image.open(r'C:\Users\quinn\.gemini\antigravity-ide\brain\805bb937-8903-4245-8343-56aa9959b3c4\VFBMS32_layout_labeled.png')
print("VFBMS32_layout_labeled size:", im.size)

# Crop left connector region
# In generate_annotated_preview:
# pad_left = 160, pad_top = 85
# board left is at 30 + pad_left = 190
crop = im.crop((140, 85, 450, 480))
crop.save(r'c:\Users\quinn\Desktop\AI PCB CAD\prev_labeled_crop.png')
print("Saved prev_labeled_crop.png")
