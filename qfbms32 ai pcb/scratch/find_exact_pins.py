import pcbnew
import re

board = pcbnew.LoadBoard(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb")

for ref in ["J_CHG1", "J_BAT1"]:
    fp = board.FindFootprintByReference(ref)
    print(f"\n================ Footprint {ref} ================")
    print(f"FP Position: ({pcbnew.ToMM(fp.GetPosition().x):.3f}, {pcbnew.ToMM(fp.GetPosition().y):.3f}), Orient: {fp.GetOrientationDegrees()} deg")
    for pad in fp.Pads():
        pos = pad.GetPosition()
        print(f"  Pad {pad.GetNumber()}: at ({pcbnew.ToMM(pos.x):.3f}, {pcbnew.ToMM(pos.y):.3f}), drill={pcbnew.ToMM(pad.GetDrillSize().x):.2f}x{pcbnew.ToMM(pad.GetDrillSize().y):.2f}, size={pcbnew.ToMM(pad.GetSize().x):.2f}x{pcbnew.ToMM(pad.GetSize().y):.2f}")

    # Check 3D model
    for m in fp.Models():
        print(f"  3D model file: {m.m_Filename}")
        print(f"  Offset: ({m.m_Offset.x}, {m.m_Offset.y}, {m.m_Offset.z})")
        print(f"  Rotate: ({m.m_Rotation.x}, {m.m_Rotation.y}, {m.m_Rotation.z})")
