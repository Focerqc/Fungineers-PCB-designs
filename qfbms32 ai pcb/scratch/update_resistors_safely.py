import os
import re
import subprocess
import pcbnew  # type: ignore
from PIL import Image

def update_resistor_spacing():
    project_dir = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB"
    pcb_path = os.path.join(project_dir, "VFBMS32.kicad_pcb")

    board = pcbnew.LoadBoard(pcb_path)
    if not board:
        raise RuntimeError("Failed to load board from: " + pcb_path)

    total_fps_before = len(list(board.GetFootprints()))
    print(f"Loaded board with {total_fps_before} footprints.")
    if total_fps_before < 100:
        raise RuntimeError(f"Safety check failed: only {total_fps_before} footprints found on board!")

    rb_map = {}
    rf_map = {}
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if re.match(r"^R_B\d+$", ref):
            rb_map[int(ref[3:])] = fp
        elif re.match(r"^R_F\d+$", ref):
            rf_map[int(ref[3:])] = fp

    print(f"Found {len(rb_map)} R_B resistors and {len(rf_map)} R_F passives.")

    # Geometric parameters
    res_x_start = 37.40
    res_pitch = 1.90
    y_rb = 28.0875  # Keep original verified Y or 28.0mm
    y_rf = 30.74    # Keep original verified Y

    for i in range(1, 33):
        rx = res_x_start + (i - 1) * res_pitch
        if i in rb_map:
            fp = rb_map[i]
            fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(rx), pcbnew.FromMM(y_rb)))
            fp.SetOrientation(pcbnew.EDA_ANGLE(90.0, pcbnew.DEGREES_T))
            fp.Reference().SetVisible(False)
            fp.Value().SetVisible(False)
        if i in rf_map:
            fp = rf_map[i]
            fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(rx), pcbnew.FromMM(y_rf)))
            fp.SetOrientation(pcbnew.EDA_ANGLE(0.0, pcbnew.DEGREES_T))
            fp.Reference().SetVisible(False)
            fp.Value().SetVisible(False)

    total_fps_after = len(list(board.GetFootprints()))
    print(f"Total footprints after update: {total_fps_after} (must match {total_fps_before})")
    assert total_fps_before == total_fps_after, "Footprint count changed unexpectedly!"

    pcbnew.SaveBoard(pcb_path, board)
    print("Saved board successfully.")

    # Render board
    kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
    raw_top_png = os.path.join(project_dir, "VFBMS32_layout_top_hi_raw.png")
    subprocess.run([
        kicad_cli, "pcb", "render",
        "--side", "top",
        "--width", "3600", "--height", "1200",
        "--background", "transparent",
        "-o", raw_top_png, pcb_path
    ], check=False)

    if os.path.exists(raw_top_png):
        im = Image.open(raw_top_png)
        bbox = im.getbbox()
        if bbox:
            pad = 30
            box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(im.width, bbox[2]+pad), min(im.height, bbox[3]+pad))
            im.crop(box).save(raw_top_png)
            print(f"Cropped raw to {im.size}")

if __name__ == "__main__":
    update_resistor_spacing()
