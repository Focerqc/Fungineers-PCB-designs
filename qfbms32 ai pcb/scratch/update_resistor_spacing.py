import os
import re
import subprocess
import pcbnew  # type: ignore
from PIL import Image

def update_resistors():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    pcb_path = os.path.join(project_dir, "VFBMS32.kicad_pcb")
    kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints"

    board = pcbnew.LoadBoard(pcb_path)
    total_fps_before = len(list(board.GetFootprints()))
    print(f"Loaded board with {total_fps_before} footprints.")

    # Find existing R_B (bleed) and R_F (filter) footprints
    rb_map = {}
    rf_map = {}
    for fp in board.GetFootprints():
        ref = fp.GetReference()
        if re.match(r"^R_B\d+$", ref):
            rb_map[int(ref[3:])] = fp
        elif re.match(r"^R_F\d+$", ref):
            rf_map[int(ref[3:])] = fp

    print(f"Found {len(rb_map)} R_B resistors and {len(rf_map)} R_F components.")

    # Geometric parameters matching physical reference
    res_x_start = 37.15
    res_pitch = 1.89
    y_rb = 26.5
    y_rf = 29.3

    # Reposition 1..32
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

    # If 33rd pair is missing, add them
    if 33 not in rb_map:
        rx_33 = res_x_start + 32 * res_pitch
        lib_path_rb = os.path.join(kicad_fp_dir, "Resistor_SMD.pretty")
        fp33_b = pcbnew.FootprintLoad(lib_path_rb, "R_0805_2012Metric")
        if fp33_b:
            board.Add(fp33_b)
            fp33_b.SetReference("R_B33")
            fp33_b.SetValue("27R0")
            fp33_b.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(rx_33), pcbnew.FromMM(y_rb)))
            fp33_b.SetOrientation(pcbnew.EDA_ANGLE(90.0, pcbnew.DEGREES_T))
            fp33_b.Reference().SetVisible(False)
            fp33_b.Value().SetVisible(False)
            print(f"Added R_B33 at ({rx_33:.2f}, {y_rb:.2f})")

    if 33 not in rf_map:
        rx_33 = res_x_start + 32 * res_pitch
        lib_path_rf = os.path.join(kicad_fp_dir, "Resistor_SMD.pretty")
        fp33_f = pcbnew.FootprintLoad(lib_path_rf, "R_0402_1005Metric")
        if fp33_f:
            board.Add(fp33_f)
            fp33_f.SetReference("R_F33")
            fp33_f.SetValue("100R")
            fp33_f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(rx_33), pcbnew.FromMM(y_rf)))
            fp33_f.SetOrientation(pcbnew.EDA_ANGLE(0.0, pcbnew.DEGREES_T))
            fp33_f.Reference().SetVisible(False)
            fp33_f.Value().SetVisible(False)
            print(f"Added R_F33 at ({rx_33:.2f}, {y_rf:.2f})")

    def add_text_if_missing(layer, text, x, y, size=0.55, thickness=0.09, angle_deg=90.0):
        # Check if text already exists
        for d in board.GetDrawings():
            if isinstance(d, pcbnew.PCB_TEXT) and d.GetLayer() == layer and d.GetText() == text:
                d.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
                return d
        t = pcbnew.PCB_TEXT(board)
        t.SetLayer(layer)
        t.SetText(text)
        t.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        t.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size), pcbnew.FromMM(size)))
        t.SetTextThickness(pcbnew.FromMM(thickness))
        t.SetTextAngle(pcbnew.EDA_ANGLE(angle_deg, pcbnew.DEGREES_T))
        t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
        t.SetVertJustify(pcbnew.GR_TEXT_V_ALIGN_CENTER)
        board.Add(t)
        return t

    add_text_if_missing(pcbnew.F_SilkS, "CANH", 31.2, 27.2)
    add_text_if_missing(pcbnew.F_SilkS, "CANL", 32.4, 27.2)
    add_text_if_missing(pcbnew.F_SilkS, "ISO_G", 33.6, 27.2)
    add_text_if_missing(pcbnew.F_SilkS, "5V_ESC", 34.8, 27.2)

    add_text_if_missing(pcbnew.F_SilkS, "T4", 100.5, 26.5)
    add_text_if_missing(pcbnew.F_SilkS, "T3", 107.0, 26.5)
    add_text_if_missing(pcbnew.F_SilkS, "T2", 113.5, 26.5)
    add_text_if_missing(pcbnew.F_SilkS, "T1", 120.0, 26.5)

    total_fps_after = len(list(board.GetFootprints()))
    print(f"Total footprints after update: {total_fps_after}")

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
    update_resistors()
