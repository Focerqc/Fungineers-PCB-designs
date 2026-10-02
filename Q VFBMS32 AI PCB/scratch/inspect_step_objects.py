import re

def inspect_step_objects(path):
    print("=== Objects in", path, "===")
    with open(path, "r", errors="ignore") as f:
        text = f.read()
    
    # find ADVANCED_BREP_SHAPE_REPRESENTATION or MANIFOLD_SOLID_BREP
    solids = re.findall(r"MANIFOLD_SOLID_BREP\s*\(\s*'([^']*)'", text)
    print("Solids:", solids)
    
    # find STYLED_ITEM or COLOUR
    colors = re.findall(r"COLOUR_RGB\s*\(\s*'([^']*)'\s*,\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*,\s*([-\d.eE]+)\s*\)", text)
    print("Colors:", set(colors))

inspect_step_objects(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\3dmodels\XT30PW-F.step")
inspect_step_objects(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\3dmodels\XT30PW-M.step")
