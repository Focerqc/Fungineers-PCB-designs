import os
import pcbnew  # type: ignore
import subprocess

def generate_v10():
    v10_dir = os.path.dirname(os.path.abspath(__file__))
    shared_pretty = os.path.abspath(os.path.join(v10_dir, "..", "..", "funwheel_led_shared.pretty"))
    pcb_path = os.path.join(v10_dir, "Status_LED_Thor300_v1.0.kicad_pcb")

    board = pcbnew.BOARD()

    ds = board.GetDesignSettings()
    ds.m_TrackMinWidth = pcbnew.FromMM(0.2)
    ds.m_ViasMinSize = pcbnew.FromMM(0.6)
    ds.m_ViasMinDrill = pcbnew.FromMM(0.3)
    ds.m_CopperEdgeClearance = pcbnew.FromMM(0.35)
    ds.m_TextMinHeight = pcbnew.FromMM(0.5)
    ds.m_TextMinWidth = pcbnew.FromMM(0.5)

    net_names = ["GND", "+12V", "DATA_IN", "DIN_1", "DATA_OUT_RET", "DATA_OUT"]
    for i in range(1, 10):
        net_names.append(f"DOUT_{i}")

    nets = {}
    for name in net_names:
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
        nets[name] = net

    def add_line(x1, y1, x2, y2):
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetFilled(False)
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(pcbnew.FromMM(0.1))
        s.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
        s.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
        board.Add(s)

    def add_arc_3pts(x_start, y_start, x_mid, y_mid, x_end, y_end):
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_ARC)
        s.SetFilled(False)
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(pcbnew.FromMM(0.1))
        s.SetArcGeometry(
            pcbnew.VECTOR2I(pcbnew.FromMM(x_start), pcbnew.FromMM(y_start)),
            pcbnew.VECTOR2I(pcbnew.FromMM(x_mid),   pcbnew.FromMM(y_mid)),
            pcbnew.VECTOR2I(pcbnew.FromMM(x_end),   pcbnew.FromMM(y_end))
        )
        board.Add(s)

    # 16 exact DXF contour segments from fungi status PCB.DXF (total length 83.5 mm)
    add_line(10.3, 2.0, 10.3, 4.666784)
    add_arc_3pts(10.3, 4.666784, 10.232025, 4.761517, 10.120513, 4.727478)
    add_arc_3pts(10.120513, 4.727478, 6.8, 5.85, 10.120513, 6.972522)
    add_arc_3pts(10.120513, 6.972522, 10.232025, 6.938483, 10.3, 7.033216)
    add_line(10.3, 7.033216, 10.3, 77.506784)
    add_arc_3pts(10.3, 77.506784, 10.232025, 77.601517, 10.120513, 77.567462)
    add_arc_3pts(10.120513, 77.567462, 6.8, 78.69, 10.120513, 79.812538)
    add_arc_3pts(10.120513, 79.812538, 10.232025, 79.778483, 10.3, 79.873216)
    add_line(10.3, 79.873216, 10.3, 81.5)
    add_arc_3pts(10.3, 81.5, 9.714214, 82.914214, 8.3, 83.5)
    add_line(8.3, 83.5, 2.0, 83.5)
    add_arc_3pts(2.0, 83.5, 0.585786, 82.914214, 0.0, 81.5)
    add_line(0.0, 81.5, 0.0, 2.0)
    add_arc_3pts(0.0, 2.0, 0.585786, 0.585786, 2.0, 0.0)
    add_line(2.0, 0.0, 8.3, 0.0)
    add_arc_3pts(8.3, 0.0, 9.714214, 0.585786, 10.3, 2.0)

    def add_via(net, x, y, size_mm=0.6, drill_mm=0.3):
        v = pcbnew.PCB_VIA(board)
        v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        v.SetWidth(pcbnew.FromMM(size_mm))
        v.SetDrill(pcbnew.FromMM(drill_mm))
        v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
        if net: v.SetNet(net)
        board.Add(v)
        return v

    def add_silk_text(layer, text, x, y, size_mm=0.8, thickness_mm=0.15, angle_deg=0.0, mirrored=False):
        t = pcbnew.PCB_TEXT(board)
        t.SetLayer(layer)
        t.SetText(text)
        t.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        t.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size_mm), pcbnew.FromMM(size_mm)))
        t.SetTextThickness(pcbnew.FromMM(thickness_mm))
        t.SetTextAngle(pcbnew.EDA_ANGLE(angle_deg, pcbnew.DEGREES_T))
        t.SetMirrored(mirrored)
        t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
        t.SetVertJustify(pcbnew.GR_TEXT_V_ALIGN_CENTER)
        board.Add(t)
        return t

    cx = 4.0
    # Spacing matching physical board photo:
    # 9mm from Thor300 text end to D1 edge (D1 center = 11.5mm)
    # 6.5mm pitch across 10 LEDs
    # D10 center = 70.0mm (bottom edge = 72.5mm, ~11mm margin from JST end)
    y_start = 11.5
    pitch = 6.5
    led_y_positions = [y_start + i * pitch for i in range(10)]

    # 10 LEDs on F.Cu at 0 deg
    for i, y_led in enumerate(led_y_positions):
        ref = f"D{i+1}"
        fp = pcbnew.FootprintLoad(shared_pretty, "LED_WS2812_PLCC6_5.0x5.0mm_P1.6mm")
        board.Add(fp)
        fp.SetReference(ref)
        fp.SetValue("SK6815")
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(cx), pcbnew.FromMM(y_led)))
        fp.SetOrientation(pcbnew.EDA_ANGLE(0, pcbnew.DEGREES_T))
        fp.Reference().SetVisible(False)
        fp.Value().SetVisible(False)

        # Via column on right of LEDs as seen in photo
        add_via(nets["GND"], 6.8, y_led, 0.6, 0.3)

    # 0603 Resistor R1 on F.Cu at top-left of D1 (seen in top photo)
    r1 = pcbnew.FootprintLoad(shared_pretty, "R_0603_1608Metric")
    board.Add(r1)
    r1.SetReference("R1")
    r1.SetValue("33R")
    r1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(3.0), pcbnew.FromMM(7.8)))
    r1.SetOrientation(pcbnew.EDA_ANGLE(0, pcbnew.DEGREES_T))
    r1.Reference().SetVisible(False)
    r1.Value().SetVisible(False)

    # 0603 Resistor R2 on F.Cu at bottom-left of D10 (seen in top photo)
    r2 = pcbnew.FootprintLoad(shared_pretty, "R_0603_1608Metric")
    board.Add(r2)
    r2.SetReference("R2")
    r2.SetValue("33R")
    r2.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(2.5), pcbnew.FromMM(73.5)))
    r2.SetOrientation(pcbnew.EDA_ANGLE(0, pcbnew.DEGREES_T))
    r2.Reference().SetVisible(False)
    r2.Value().SetVisible(False)

    # 10 SMD Passives on B.Cu matching the physical board photo behind each LED
    for i, y_cap in enumerate(led_y_positions):
        ref = f"C{i+1}"
        fp = pcbnew.FootprintLoad(shared_pretty, "C_0603_1608Metric")
        board.Add(fp)
        fp.SetReference(ref)
        fp.SetValue("0.1uF")
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(5.0), pcbnew.FromMM(y_cap)))
        fp.SetLayerAndFlip(pcbnew.B_Cu)
        fp.SetOrientation(pcbnew.EDA_ANGLE(0, pcbnew.DEGREES_T))
        fp.Reference().SetVisible(False)
        fp.Value().SetVisible(False)

        # Via beside each passive as seen in photo
        add_via(nets["GND"], 6.6, y_cap, 0.6, 0.3)

    # Vias along left rail as seen in photo
    for y_v in led_y_positions:
        add_via(nets["+12V"], 2.2, y_v, 0.6, 0.3)

    # J1 JST GH Vertical (BM04B-GHS-TBT) on B.Cu facing UP, moved up to Y = 73.5 mm
    # Bottom of shroud is at Y ~ 75.6 mm, completely clear of the mounting notch at Y = 78.69 mm (notch starts at Y = 77.19 mm)
    j1 = pcbnew.FootprintLoad(shared_pretty, "JST_GH_BM04B-GHS-TBT_1x04-1MP_P1.25mm_Vertical")
    board.Add(j1)
    j1.SetReference("J1")
    j1.SetValue("BM04B-GHS-TBT")
    j1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(4.8), pcbnew.FromMM(73.5)))
    j1.SetLayerAndFlip(pcbnew.B_Cu)
    j1.SetOrientation(pcbnew.EDA_ANGLE(0, pcbnew.DEGREES_T))
    j1.Reference().SetVisible(False)
    j1.Value().SetVisible(False)

    # Silkscreen text on B.SilkS directly above each pin (vertical text matching photo)
    # Left to right in bottom view: DIN, DOUT, GND, 12V at Y = 70.5 mm
    add_silk_text(pcbnew.B_SilkS, "DIN",  2.925, 70.5, 0.65, thickness_mm=0.12, angle_deg=90.0, mirrored=True)
    add_silk_text(pcbnew.B_SilkS, "DOUT", 4.175, 70.5, 0.60, thickness_mm=0.11, angle_deg=90.0, mirrored=True)
    add_silk_text(pcbnew.B_SilkS, "GND",  5.425, 70.5, 0.65, thickness_mm=0.12, angle_deg=90.0, mirrored=True)
    add_silk_text(pcbnew.B_SilkS, "12V",  6.675, 70.5, 0.65, thickness_mm=0.12, angle_deg=90.0, mirrored=True)

    # Thor300 text on F.SilkS at the opposite end (Y = 0 end)
    add_silk_text(pcbnew.F_SilkS, "Status LED",   5.15, 2.2, 0.75, thickness_mm=0.14)
    add_silk_text(pcbnew.F_SilkS, "Thor300 v1.0", 5.15, 3.4, 0.70, thickness_mm=0.13)

    pcbnew.SaveBoard(pcb_path, board)
    print("Saved Status LED Thor300 v1.0 board to", pcb_path)

    # Render 3D Top and Bottom views
    kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
    top_png = os.path.join(v10_dir, "Status_LED_Thor300_v1.0_3d_top.png")
    bottom_png = os.path.join(v10_dir, "Status_LED_Thor300_v1.0_3d_bottom.png")

    subprocess.run([
        kicad_cli, "pcb", "render",
        "--side", "top",
        "--width", "1000", "--height", "2000",
        "--background", "transparent",
        "-o", top_png, pcb_path
    ], check=False)
    print("Rendered 3D top view to", top_png)

    subprocess.run([
        kicad_cli, "pcb", "render",
        "--side", "bottom",
        "--width", "1000", "--height", "2000",
        "--background", "transparent",
        "-o", bottom_png, pcb_path
    ], check=False)
    print("Rendered 3D bottom view to", bottom_png)

if __name__ == "__main__":
    generate_v10()
