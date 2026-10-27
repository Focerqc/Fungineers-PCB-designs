import pcbnew

board = pcbnew.LoadBoard("qfbms32 ai pcb/qfbms32.kicad_pcb")

for fp in board.GetFootprints():
    ref = str(fp.GetReference())
    if any(k in ref for k in ["S1", "S2", "_S", "SH", "RS"]):
        pos = fp.GetPosition()
        val = str(fp.GetValue())
        fp_id = str(fp.GetFPID().GetLibItemName())
        print(f"Ref: {ref:10} Val: {val:15} FP: {fp_id:25} Pos: ({pcbnew.ToMM(pos.x):6.2f}, {pcbnew.ToMM(pos.y):6.2f})")
