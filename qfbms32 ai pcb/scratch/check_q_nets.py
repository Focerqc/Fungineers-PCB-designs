import pcbnew

board = pcbnew.LoadBoard('qfbms32.kicad_pcb')
q2 = board.FindFootprintByReference("Q2")
print("Q2 pads and nets:")
for pad in q2.Pads():
    print(f"  Pad {pad.GetName()}: net='{pad.GetNetname()}'")

q1 = board.FindFootprintByReference("Q1")
print("Q1 pads and nets:")
for pad in q1.Pads():
    print(f"  Pad {pad.GetName()}: net='{pad.GetNetname()}'")
