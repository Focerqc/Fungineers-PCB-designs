import pcbnew

board = pcbnew.LoadBoard("qfbms32 ai pcb/qfbms32.kicad_pcb")

# Find an existing 0805 resistor, e.g. R_CHG2 or R_B1
ref_fp = board.FindFootprintByReference("R_B1")
if not ref_fp:
    ref_fp = board.FindFootprintByReference("R_CHG2")

print("Found ref fp:", ref_fp.GetReference(), ref_fp.GetFPID().GetLibItemName())

# Let's test duplicating or FootprintLoad
try:
    clone = pcbnew.FOOTPRINT(ref_fp)
    print("Cloned successfully via copy constructor!")
except Exception as e:
    print("Copy constructor failed:", e)

try:
    dup = ref_fp.Duplicate()
    print("Duplicate method:", dup)
except Exception as e:
    print("Duplicate failed:", e)
