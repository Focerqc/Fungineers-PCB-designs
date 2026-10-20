import pcbnew
import os

kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints"
diode_lib = os.path.join(kicad_fp_dir, "Diode_SMD.pretty")
fp = pcbnew.FootprintLoad(diode_lib, "D_SOD-123F")

print("D_SOD-123F pads (at rotation 0):")
for pad in fp.Pads():
    pos = pad.GetPosition()
    print(f"  Pad {pad.GetName()}: at ({pcbnew.ToMM(pos.x):.2f}, {pcbnew.ToMM(pos.y):.2f})")

fp.SetOrientation(pcbnew.EDA_ANGLE(90.0, pcbnew.DEGREES_T))
print("D_SOD-123F pads (at rotation 90):")
for pad in fp.Pads():
    pos = pad.GetPosition()
    print(f"  Pad {pad.GetName()}: at ({pcbnew.ToMM(pos.x):.2f}, {pcbnew.ToMM(pos.y):.2f})")

fp.SetOrientation(pcbnew.EDA_ANGLE(270.0, pcbnew.DEGREES_T))
print("D_SOD-123F pads (at rotation 270):")
for pad in fp.Pads():
    pos = pad.GetPosition()
    print(f"  Pad {pad.GetName()}: at ({pcbnew.ToMM(pos.x):.2f}, {pcbnew.ToMM(pos.y):.2f})")
