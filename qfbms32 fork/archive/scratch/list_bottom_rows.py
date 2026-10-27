import pcbnew, os, re

pcb_path = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"
board = pcbnew.LoadBoard(pcb_path)

rows = []
for fp in board.GetFootprints():
    p = fp.GetPosition()
    x, y = pcbnew.ToMM(p.x), pcbnew.ToMM(p.y)
    if y > 25.5:
        bb = fp.GetFpPadsLocalBbox() if hasattr(fp, "GetFpPadsLocalBbox") else None
        pads = [(pd.GetName(), round(pcbnew.ToMM(pd.GetPosition().x), 2), round(pcbnew.ToMM(pd.GetPosition().y), 2),
                 pd.GetNetname()) for pd in fp.Pads()]
        rows.append((x, y, fp.GetReference(), fp.GetValue(), str(fp.GetFPID().GetLibItemName()),
                     fp.GetOrientation().AsDegrees(), fp.GetLayerName(), pads))

for r in sorted(rows, key=lambda r: (round(r[1]), r[0])):
    print(f"{r[2]:8} {r[3]:10} {r[4]:22} ({r[0]:7.3f},{r[1]:7.3f}) rot={r[5]:6.1f} {r[6]} pads={r[7]}")
print("count", len(rows))
