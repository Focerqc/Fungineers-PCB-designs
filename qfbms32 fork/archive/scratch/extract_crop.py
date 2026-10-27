import re
import base64
import io
from PIL import Image

with open('qfbms32.kicad_pcb', 'r', encoding='utf-8') as f:
    text = f.read()

m = re.search(r'\(image\s+\(at\s+([0-9\.]+)\s+([0-9\.]+)\)\s+\(layer\s+"User\.4"\)\s+\(scale\s+([0-9\.]+)\).*?\(data\s+"([^"]+)"\)', text, re.DOTALL)
if m:
    x_at = float(m.group(1))
    y_at = float(m.group(2))
    scale = float(m.group(3))
    data = base64.b64decode(m.group(4))
    im = Image.open(io.BytesIO(data))
    print(f'Embedded image size: {im.size}, at=({x_at}, {y_at}), scale={scale}')
    im.save('scratch/embedded_user4.png')
    
    x0_mm, y0_mm = -0.027897, -0.059642
    w_mm, h_mm = 130.094195, 32.003492
    
    px_w, px_h = im.size
    def mm_to_px(x, y):
        px = (x - x0_mm) / w_mm * px_w
        py = (y - y0_mm) / h_mm * px_h
        return int(px), int(py)
        
    px0, py0 = mm_to_px(13.0, 0.0)
    px1, py1 = mm_to_px(17.0, 3.0)
    crop = im.crop((px0, py0, px1, py1))
    crop.save('scratch/r_chg2_zoomed.png')
    print(f'Crop saved: size={crop.size}, mm span=4.0 x 3.0 mm')
    print(f'Pixels per mm: x={crop.size[0]/4.0:.2f}, y={crop.size[1]/3.0:.2f}')
else:
    print('Image not matched')
