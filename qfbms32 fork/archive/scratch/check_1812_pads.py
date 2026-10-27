import pcbnew
import os

kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints"
lib_path = os.path.join(kicad_fp_dir, "Capacitor_SMD.pretty")
new_fp = pcbnew.FootprintLoad(lib_path, "C_1812_4532Metric")
new_fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(10.18), pcbnew.FromMM(16.63)))
new_fp.SetOrientation(pcbnew.EDA_ANGLE(90.0, pcbnew.DEGREES_T))

for pad in new_fp.Pads():
    pos = pad.GetPosition()
    size = pad.GetSize()
    print(f"Pad {pad.GetName()}: pos=({pcbnew.ToMM(pos.x):.2f}, {pcbnew.ToMM(pos.y):.2f}) size=({pcbnew.ToMM(size.x):.2f}, {pcbnew.ToMM(size.y):.2f})")
