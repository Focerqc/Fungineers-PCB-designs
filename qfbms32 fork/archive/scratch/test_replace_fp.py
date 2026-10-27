import pcbnew
import os

board = pcbnew.LoadBoard(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb")
custom_lib = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\vfbms.pretty"

# Test removing U_BOOST1 and U_BUCK1
for ref in ["U_BOOST1", "U_BUCK1"]:
    fp = board.FindFootprintByReference(ref)
    if fp:
        board.Remove(fp)
        print(f"Removed {ref}")

# Test replacing J_CHG1 and J_BAT1
for ref, lib_item in [("J_CHG1", "XT30PW-F_Lugs"), ("J_BAT1", "XT30PW-M_Lugs")]:
    old_fp = board.FindFootprintByReference(ref)
    if old_fp:
        pos = old_fp.GetPosition()
        rot = old_fp.GetOrientation()
        val = old_fp.GetValue()
        board.Remove(old_fp)
        
        new_fp = pcbnew.FootprintLoad(custom_lib, lib_item)
        new_fp.SetPosition(pos)
        new_fp.SetOrientation(rot)
        new_fp.SetReference(ref)
        new_fp.SetValue(val)
        board.Add(new_fp)
        print(f"Replaced {ref} with {lib_item}")

test_out = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\test_board_replace.kicad_pcb"
pcbnew.SaveBoard(test_out, board)
print("Saved test board!")

# Re-read test board to verify
b2 = pcbnew.LoadBoard(test_out)
print("U_BOOST1 in b2:", b2.FindFootprintByReference("U_BOOST1") is not None)
print("U_BUCK1 in b2:", b2.FindFootprintByReference("U_BUCK1") is not None)
f1 = b2.FindFootprintByReference("J_CHG1")
print("J_CHG1 pads in b2:", len(list(f1.Pads())))
m1 = b2.FindFootprintByReference("J_BAT1")
print("J_BAT1 pads in b2:", len(list(m1.Pads())))
