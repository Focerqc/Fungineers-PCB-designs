from PIL import Image

top = Image.open(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\VFBMS32_3d_top.png")
sx = top.width / 130.0
sy = top.height / 32.0

crop = top.crop((int(84 * sx), int(0 * sy), int(93 * sx), int(8 * sy)))
crop = crop.resize((crop.width * 2, crop.height * 2), Image.Resampling.NEAREST)
crop.save(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\scratch\buzzer_3d_render_crop.png")
print("Saved buzzer_3d_render_crop.png")
