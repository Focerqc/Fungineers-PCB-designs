import os
import re

candidates = [
    r'C:\Program Files\KiCad\10.0\share\kicad\footprints\Package_DIP.pretty\SMDIP-8_W7.62mm.kicad_mod',
    r'C:\Program Files\KiCad\10.0\share\kicad\footprints\Package_DIP.pretty\SMDIP-8_W9.53mm.kicad_mod',
    r'C:\Program Files\KiCad\10.0\share\kicad\footprints\Package_SO.pretty\SOP-8_6.62x9.15mm_P2.54mm.kicad_mod',
    r'C:\Program Files\KiCad\10.0\share\kicad\footprints\Package_SO.pretty\SOP-8_6.605x9.655mm_P2.54mm.kicad_mod',
]

for fn in candidates:
    if os.path.exists(fn):
        with open(fn, 'r') as f:
            txt = f.read()
            pads1 = re.findall(r'\(pad "1" smd \w+ \(at ([0-9\.\-]+) ([0-9\.\-]+)', txt)
            pads5 = re.findall(r'\(pad "5" smd \w+ \(at ([0-9\.\-]+) ([0-9\.\-]+)', txt)
            pad_size = re.findall(r'\(pad "1" smd \w+ \(at [^\)]+\) \(size ([0-9\.\-]+) ([0-9\.\-]+)', txt)
            if pads1 and pads5:
                span = abs(float(pads5[0][0]) - float(pads1[0][0]))
                size_str = f"pad size: {pad_size[0]}" if pad_size else ""
                print(f"{os.path.basename(fn):<35}: Pad1={pads1[0]}, Pad5={pads5[0]}, Span={span:.2f}mm, {size_str}")
