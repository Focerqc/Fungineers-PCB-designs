import re, os

step_path = r'C:\Program Files\KiCad\10.0\share\kicad\3dmodels\Package_DIP.3dshapes\SMDIP-8_W9.53mm.step'
print("STEP exists:", os.path.exists(step_path))

# Check Package_DIP.pretty SMDIP-8_W9.53mm.kicad_mod model definition
mod_path = r'C:\Program Files\KiCad\10.0\share\kicad\footprints\Package_DIP.pretty\SMDIP-8_W9.53mm.kicad_mod'
with open(mod_path, 'r') as f:
    txt = f.read()
    model_m = re.search(r'\(model\s+"[^"]+"[\s\S]*?\)', txt)
    if model_m:
        print("Default model in kicad_mod:")
        print(model_m.group(0))
