import pcbnew

board = pcbnew.LoadBoard(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb")
custom_lib = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\vfbms.pretty"

old_fp = board.FindFootprintByReference("J_CHG1")
pos = pcbnew.VECTOR2I(old_fp.GetPosition().x, old_fp.GetPosition().y)
rot = old_fp.GetOrientation()
ref = old_fp.GetReference()
val = old_fp.GetValue()

board.Delete(old_fp)

new_fp = pcbnew.FootprintLoad(custom_lib, "XT30PW-F_Lugs")
new_fp.SetPosition(pos)
new_fp.SetOrientation(rot)
new_fp.SetReference(ref)
new_fp.SetValue(val)
board.Add(new_fp)

print("Successfully replaced J_CHG1!")
found = board.FindFootprintByReference("J_CHG1")
print("Found new J_CHG1 with pads:", len(list(found.Pads())))
for p in found.Pads():
    print(f"  Pad {p.GetNumber()}: at ({pcbnew.ToMM(p.GetPosition().x):.2f}, {pcbnew.ToMM(p.GetPosition().y):.2f}), drill={pcbnew.ToMM(p.GetDrillSize().x):.2f}")
