import os
import pcbnew
from PIL import Image

pcb_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb"
pcb_path = os.path.join(pcb_dir, "qfbms32.kicad_pcb")
board = pcbnew.LoadBoard(pcb_path)

# Let's inspect tracks, pads, vias around each of the 4 box points
boxes = [
    {"name": "Color1_Box1", "color": "Color 1 (X10)", "x": 29.75, "y": 17.20, "w": 1.6, "h": 0.8},
    {"name": "Color1_Box2", "color": "Color 1 (X10)", "x": 29.50, "y": 7.60, "w": 1.6, "h": 0.8},
    {"name": "Color1_Box3", "color": "Color 1 (X10)", "x": 29.20, "y": 4.05, "w": 1.6, "h": 0.8},
    {"name": "Color2_Box1", "color": "Color 2 (474)", "x": 29.50, "y": 8.95, "w": 1.6, "h": 0.8},
]

print("=== PCB FEATURES NEAR BOXES ===")
for b in boxes:
    bx, by = b["x"], b["y"]
    print(f"\n--- {b['name']} ({b['color']}) at ({bx:.2f}, {by:.2f}) ---")
    
    # Pads within 3mm
    for fp in board.GetFootprints():
        for pad in fp.Pads():
            p = pad.GetPosition()
            px, py = pcbnew.ToMM(p.x), pcbnew.ToMM(p.y)
            dist = ((px - bx)**2 + (py - by)**2)**0.5
            if dist < 2.5:
                print(f"  Pad: {str(fp.GetReference())} pin {str(pad.GetName())} net={str(pad.GetNetname())} at ({px:.3f}, {py:.3f}) dist={dist:.2f}mm")

    # Tracks within 1.5mm
    for tr in board.GetTracks():
        p1 = tr.GetStart()
        p2 = tr.GetEnd()
        x1, y1 = pcbnew.ToMM(p1.x), pcbnew.ToMM(p1.y)
        x2, y2 = pcbnew.ToMM(p2.x), pcbnew.ToMM(p2.y)
        # Check midpoint
        mx, my = (x1 + x2)/2, (y1 + y2)/2
        dist = ((mx - bx)**2 + (my - by)**2)**0.5
        if dist < 1.5:
            print(f"  Track/Via: {str(tr.GetClass())} net={str(tr.GetNetname())} from ({x1:.2f},{y1:.2f}) to ({x2:.2f},{y2:.2f})")
