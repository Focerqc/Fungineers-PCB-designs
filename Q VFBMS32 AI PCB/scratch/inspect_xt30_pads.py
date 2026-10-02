import pcbnew

board = pcbnew.LoadBoard(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb")

for ref in ["J_CHG1", "J_BAT1", "Q1", "Q2"]:
    fp = board.FindFootprintByReference(ref)
    if not fp:
        print(f"{ref} NOT FOUND")
        continue
    pos = fp.GetPosition()
    rot = fp.GetOrientationDegrees()
    print(f"\nFootprint: {ref} at ({pcbnew.ToMM(pos.x):.3f}, {pcbnew.ToMM(pos.y):.3f}), rot={rot:.1f} deg, FP Name: {fp.GetFPID().GetLibItemName()}")
    
    # 3D models
    for m in fp.Models():
        print(f"  3D Model: path={m.m_Filename}")
        print(f"    offset=({m.m_Offset.x}, {m.m_Offset.y}, {m.m_Offset.z})")
        print(f"    scale=({m.m_Scale.x}, {m.m_Scale.y}, {m.m_Scale.z})")
        print(f"    rotate=({m.m_Rotation.x}, {m.m_Rotation.y}, {m.m_Rotation.z})")
        
    for pad in fp.Pads():
        pad_pos = pad.GetPosition()
        drill = pad.GetDrillSize()
        size = pad.GetSize()
        shape = pad.GetShape()
        attr = pad.GetAttribute()
        print(f"  Pad {pad.GetNumber()}: at ({pcbnew.ToMM(pad_pos.x):.3f}, {pcbnew.ToMM(pad_pos.y):.3f}), size=({pcbnew.ToMM(size.x):.2f}, {pcbnew.ToMM(size.y):.2f}), drill=({pcbnew.ToMM(drill.x):.2f}, {pcbnew.ToMM(drill.y):.2f}), attr={attr}, shape={shape}, layers={pad.GetLayerSet().FmtHex()}")
