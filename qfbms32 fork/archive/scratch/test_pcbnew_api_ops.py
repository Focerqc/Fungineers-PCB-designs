import pcbnew

board = pcbnew.LoadBoard(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb")

# Test 1: Finding footprints
u_boost = board.FindFootprintByReference("U_BOOST1")
u_buck = board.FindFootprintByReference("U_BUCK1")
print("Found U_BOOST1:", u_boost is not None)
print("Found U_BUCK1:", u_buck is not None)

# Test 2: Footprint 3D model API
j_bat = board.FindFootprintByReference("J_BAT1")
if j_bat:
    for m in j_bat.Models():
        print("J_BAT1 model:", m.m_Filename)
        print("  Current offset:", m.m_Offset.x, m.m_Offset.y, m.m_Offset.z)
        # Test setting offset
        m.m_Offset = pcbnew.VECTOR3D(4.1, 0.0, 2.5)
        print("  New offset:", m.m_Offset.x, m.m_Offset.y, m.m_Offset.z)

# Test 3: Reload footprint from library
# In pcbnew, can we load footprint from library and replace, or update pads?
custom_lib = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\vfbms.pretty"
new_f_fp = pcbnew.FootprintLoad(custom_lib, "XT30PW-F_Lugs")
print("Loaded new XT30PW-F_Lugs:", new_f_fp is not None)
if new_f_fp:
    print("  New FP pad count:", len(list(new_f_fp.Pads())))
    for pad in new_f_fp.Pads():
        print(f"    Pad {pad.GetNumber()}: at ({pcbnew.ToMM(pad.GetPosition().x):.2f}, {pcbnew.ToMM(pad.GetPosition().y):.2f}), drill={pcbnew.ToMM(pad.GetDrillSize().x):.2f}")

new_m_fp = pcbnew.FootprintLoad(custom_lib, "XT30PW-M_Lugs")
print("Loaded new XT30PW-M_Lugs:", new_m_fp is not None)
if new_m_fp:
    print("  New FP pad count:", len(list(new_m_fp.Pads())))
    for pad in new_m_fp.Pads():
        print(f"    Pad {pad.GetNumber()}: at ({pcbnew.ToMM(pad.GetPosition().x):.2f}, {pcbnew.ToMM(pad.GetPosition().y):.2f}), drill={pcbnew.ToMM(pad.GetDrillSize().x):.2f}")

