from PIL import Image

cad = Image.open(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\_reference\vfbms32_cad_top_reference_rotated.png")
sx = cad.width / 130.0
sy = cad.height / 32.0

# Crop closely around the buzzer footprint
c = cad.crop((int(85.0 * sx), int(0.0 * sy), int(91.5 * sx), int(6.0 * sy)))
c = c.resize((c.width * 8, c.height * 8), Image.Resampling.NEAREST)
c.save(r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\scratch\buzzer_cad_zoom.png")
print("Saved buzzer_cad_zoom.png")
