from PIL import Image

cad = Image.open(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\_reference\vfbms32_cad_top_reference_rotated.png")
real = Image.open(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\_reference\vfbms32_real_top_hd.png")

# Board is 130mm x 32mm
# We want region X: 84 to 93 mm, Y: 0 to 7 mm
sx_cad = cad.width / 130.0
sy_cad = cad.height / 32.0

crop_cad = cad.crop((int(84 * sx_cad), int(0 * sy_cad), int(93 * sx_cad), int(7.5 * sy_cad)))
crop_cad.save(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\scratch\crop_buzzer_cad.png")

sx_real = real.width / 130.0
sy_real = real.height / 32.0
crop_real = real.crop((int(84 * sx_real), int(0 * sy_real), int(93 * sx_real), int(7.5 * sy_real)))
crop_real.save(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\scratch\crop_buzzer_real.png")

print("Saved crop_buzzer_cad.png and crop_buzzer_real.png")
