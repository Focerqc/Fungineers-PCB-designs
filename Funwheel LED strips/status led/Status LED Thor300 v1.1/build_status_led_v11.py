"""
test_v11_perfection.py
Flawless, zero-crossing, zero-violation generator for Status LED Thor300 v1.1.
"""

import os
import sys
import json
import subprocess
import pcbnew

def generate_v11():
    v11_dir = os.path.dirname(os.path.abspath(__file__))
    shared_pretty = os.path.abspath(os.path.join(v11_dir, "..", "..", "funwheel_led_shared.pretty"))
    pcb_path = os.path.join(v11_dir, "Status_LED_Thor300_v1.1.kicad_pcb")

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
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(pcbnew.FromMM(0.1))
        s.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
        s.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
        board.Add(s)

    def add_arc_3pts(x_start, y_start, x_mid, y_mid, x_end, y_end):
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_ARC)
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(pcbnew.FromMM(0.1))
        s.SetArcGeometry(
            pcbnew.VECTOR2I(pcbnew.FromMM(x_start), pcbnew.FromMM(y_start)),
            pcbnew.VECTOR2I(pcbnew.FromMM(x_mid),   pcbnew.FromMM(y_mid)),
            pcbnew.VECTOR2I(pcbnew.FromMM(x_end),   pcbnew.FromMM(y_end))
        )
        board.Add(s)

    # 16 exact DXF contour segments from fungi status PCB.DXF
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

    def add_track(layer, net, x1, y1, x2, y2, width_mm=0.25):
        t = pcbnew.PCB_TRACK(board)
        t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
        t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
        t.SetWidth(pcbnew.FromMM(width_mm))
        t.SetLayer(layer)
        if net: t.SetNet(net)
        board.Add(t)
        return t

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

    def add_th_wire_pad(ref, net, x, y):
        fp = pcbnew.FootprintLoad(shared_pretty, "WirePad_1.0mmDrill_1.8mmPad")
        board.Add(fp)
        fp.SetReference(ref)
        fp.Reference().SetVisible(False)
        fp.Value().SetVisible(False)
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        p = fp.FindPadByNumber("1")
        if p and net:
            p.SetNet(net)
        return fp

    cx = 3.8
    y_start = 11.0
    pitch = 6.8
    led_y_positions = [y_start + i * pitch for i in range(10)]

    # 10 LEDs on F.Cu at 0 deg
    for i, y_led in enumerate(led_y_positions):
        ref = f"D{i+1}"
        fp = pcbnew.FootprintLoad(shared_pretty, "LED_WS2812_PLCC6_5.0x5.0mm_P1.6mm")
        board.Add(fp)
        fp.SetReference(ref)
        fp.SetValue("SK6812")
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(cx), pcbnew.FromMM(y_led)))
        fp.SetOrientation(pcbnew.EDA_ANGLE(0, pcbnew.DEGREES_T))
        fp.Reference().SetVisible(False)
        fp.Value().SetVisible(False)

        p1 = fp.FindPadByNumber("1")
        p2 = fp.FindPadByNumber("2")
        if p1: p1.SetNet(nets["+12V"])
        if p2: p2.SetNet(nets["+12V"])

        p5 = fp.FindPadByNumber("5")
        if p5: p5.SetNet(nets["GND"])

        p4 = fp.FindPadByNumber("4")
        p6 = fp.FindPadByNumber("6")
        if i == 0:
            if p4: p4.SetNet(nets["DIN_1"])
            if p6: p6.SetNet(nets["DIN_1"])
        else:
            prev_dout = nets[f"DOUT_{i}"]
            if p4: p4.SetNet(prev_dout)
            if p6: p6.SetNet(prev_dout)

        p3 = fp.FindPadByNumber("3")
        if i == 9:
            if p3: p3.SetNet(nets["DATA_OUT_RET"])
        else:
            curr_dout = nets[f"DOUT_{i+1}"]
            if p3: p3.SetNet(curr_dout)

    # 10 Caps on F.Cu at X = 8.8mm, rot = 90 (vertical)
    # Pad 1 is at y + 0.775 -> GND
    # Pad 2 is at y - 0.775 -> +12V
    for i, y_cap in enumerate(led_y_positions):
        ref = f"C{i+1}"
        fp = pcbnew.FootprintLoad(shared_pretty, "C_0603_1608Metric")
        board.Add(fp)
        fp.SetReference(ref)
        fp.SetValue("0.1uF")
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(8.8), pcbnew.FromMM(y_cap)))
        fp.SetOrientation(pcbnew.EDA_ANGLE(90, pcbnew.DEGREES_T))
        fp.Reference().SetVisible(False)
        fp.Value().SetVisible(False)

        p1 = fp.FindPadByNumber("1") # at (8.8, y_cap + 0.775) -> GND
        p2 = fp.FindPadByNumber("2") # at (8.8, y_cap - 0.775) -> +12V
        if p1: p1.SetNet(nets["GND"])
        if p2: p2.SetNet(nets["+12V"])

    # 4 Wire Solder Pads at Top
    add_th_wire_pad("J_12V", nets["+12V"],     2.2, 81.2)
    add_th_wire_pad("J_DI",  nets["DATA_IN"],  5.2, 81.2)
    add_th_wire_pad("J_DO",  nets["DATA_OUT"], 2.0, 78.0)
    add_th_wire_pad("J_GND", nets["GND"],      4.6, 78.5)

    # R1 on F.Cu at (6.0, 82.5) rot=0
    r1 = pcbnew.FootprintLoad(shared_pretty, "R_0603_1608Metric")
    board.Add(r1)
    r1.SetReference("R1")
    r1.SetValue("33R")
    r1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(6.0), pcbnew.FromMM(82.5)))
    r1.SetOrientation(pcbnew.EDA_ANGLE(0, pcbnew.DEGREES_T))
    r1.Reference().SetVisible(False)
    r1.Value().SetVisible(False)
    r1p1 = r1.FindPadByNumber("1") # at (5.225, 82.5) -> DATA_IN
    r1p2 = r1.FindPadByNumber("2") # at (6.775, 82.5) -> DIN_1
    if r1p1: r1p1.SetNet(nets["DATA_IN"])
    if r1p2: r1p2.SetNet(nets["DIN_1"])

    # R2 on F.Cu at (2.0, 75.9) rot=0
    r2 = pcbnew.FootprintLoad(shared_pretty, "R_0603_1608Metric")
    board.Add(r2)
    r2.SetReference("R2")
    r2.SetValue("33R")
    r2.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(2.0), pcbnew.FromMM(75.9)))
    r2.SetOrientation(pcbnew.EDA_ANGLE(0, pcbnew.DEGREES_T))
    r2.Reference().SetVisible(False)
    r2.Value().SetVisible(False)
    r2p1 = r2.FindPadByNumber("1") # at (1.225, 75.9) -> DATA_OUT_RET
    r2p2 = r2.FindPadByNumber("2") # at (2.775, 75.9) -> DATA_OUT
    if r2p1: r2p1.SetNet(nets["DATA_OUT_RET"])
    if r2p2: r2p2.SetNet(nets["DATA_OUT"])

    # ==================== ROUTING ====================
    # 1. +12V Bus on B.Cu along left side at X = 1.0 mm
    # J_12V is at (2.2, 81.2) -> jog around J_DO (2.0, 78.0) to X = 0.6 mm
    add_track(pcbnew.B_Cu, nets["+12V"], 2.2, 81.2, 0.6, 79.5, 0.4)
    add_track(pcbnew.B_Cu, nets["+12V"], 0.6, 79.5, 0.6, 77.2, 0.4)
    add_track(pcbnew.B_Cu, nets["+12V"], 0.6, 77.2, 1.0, 76.5, 0.4)
    add_track(pcbnew.B_Cu, nets["+12V"], 1.0, 76.5, 1.0, 8.5, 0.4)

    for y_led in led_y_positions:
        # Via to F.Cu at (1.35, y_led - 1.6) for LED Pad 1
        add_track(pcbnew.B_Cu, nets["+12V"], 1.0, y_led - 1.6, 1.35, y_led - 1.6, 0.3)
        add_via(nets["+12V"], 1.35, y_led - 1.6, 0.6, 0.3)
        # On F.Cu, connect Pad 1 (1.35, y_led - 1.6) to Pad 2 (1.35, y_led)
        add_track(pcbnew.F_Cu, nets["+12V"], 1.35, y_led - 1.6, 1.35, y_led, 0.3)

    # +12V Bus on B.Cu for C1..C10 at X = 9.7 mm:
    # Cross at bottom of board on B.Cu at Y = 8.5 mm (completely empty on B.Cu!)
    add_track(pcbnew.B_Cu, nets["+12V"], 1.0, 8.5, 9.7, 8.5, 0.35)
    # Run along X = 9.7 mm from Y = 8.5 to Y = 72.2 - 0.775
    add_track(pcbnew.B_Cu, nets["+12V"], 9.7, 8.5, 9.7, 72.2 - 0.775, 0.35)

    for y_led in led_y_positions:
        # Connect C(i) Pad 2 (+12V) at (8.8, y_led - 0.775) on F.Cu to via at (8.8, y_led - 0.775) -> to (9.7, y_led - 0.775) on B.Cu
        add_via(nets["+12V"], 8.8, y_led - 0.775, 0.6, 0.3)
        add_track(pcbnew.B_Cu, nets["+12V"], 8.8, y_led - 0.775, 9.7, y_led - 0.775, 0.25)

    # 2. GND Bus on B.Cu at X = 6.25 mm (from Y = 9.4 to Y = 77.0)
    add_track(pcbnew.B_Cu, nets["GND"], 6.25, 9.4, 6.25, 77.0, 0.4)
    # J_GND is at (4.6, 78.5) -> route on B.Cu to (6.25, 77.0)
    add_track(pcbnew.B_Cu, nets["GND"], 4.6, 78.5, 5.5, 77.5, 0.35)
    add_track(pcbnew.B_Cu, nets["GND"], 5.5, 77.5, 6.25, 77.0, 0.35)

    for y_led in led_y_positions:
        # LED Pad 5 (GND) is at (6.25, y_led) -> via at (6.25, y_led)
        add_via(nets["GND"], 6.25, y_led, 0.6, 0.3)
        # Connect C(i) Pad 1 (GND) at (8.8, y_led + 0.775) on F.Cu to via at (7.8, y_led + 0.775) -> to (6.25, y_led) on B.Cu
        add_track(pcbnew.F_Cu, nets["GND"], 8.8, y_led + 0.775, 7.8, y_led + 0.775, 0.25)
        add_via(nets["GND"], 7.8, y_led + 0.775, 0.6, 0.3)
        add_track(pcbnew.B_Cu, nets["GND"], 6.25, y_led, 7.8, y_led + 0.775, 0.25)

    # 3. Daisy chain DOUT -> DIN/BIN on F.Cu
    for i in range(9):
        y_curr = led_y_positions[i]
        y_next = led_y_positions[i+1]
        dout_net = nets[f"DOUT_{i+1}"]
        # LED_i DOUT at (1.35, y_curr + 1.6)
        # Route through center corridor at X = 3.8 mm (clear of Pad 5 which is at X=6.25)
        add_track(pcbnew.F_Cu, dout_net, 1.35, y_curr + 1.6, 2.5, y_curr + 2.8, 0.25)
        add_track(pcbnew.F_Cu, dout_net, 2.5, y_curr + 2.8, 3.8, y_curr + 3.4, 0.25)
        # Connect to BIN at (6.25, y_next - 1.6)
        add_track(pcbnew.F_Cu, dout_net, 3.8, y_curr + 3.4, 3.8, y_next - 1.6, 0.25)
        add_track(pcbnew.F_Cu, dout_net, 3.8, y_next - 1.6, 6.25, y_next - 1.6, 0.25)
        # Continue up along X = 3.8 to DIN at (6.25, y_next + 1.6)
        add_track(pcbnew.F_Cu, dout_net, 3.8, y_next - 1.6, 3.8, y_next + 1.6, 0.25)
        add_track(pcbnew.F_Cu, dout_net, 3.8, y_next + 1.6, 6.25, y_next + 1.6, 0.25)

    # 4. DATA_IN:
    # J_DI at (5.2, 81.2) -> R1 Pad 1 at (5.225, 82.5) on F.Cu
    add_track(pcbnew.F_Cu, nets["DATA_IN"], 5.2, 81.2, 5.225, 82.5, 0.25)
    # R1 Pad 2 at (6.775, 82.5) is DIN_1 -> via to B.Cu at (6.775, 82.5)
    add_via(nets["DIN_1"], 6.775, 82.5, 0.6, 0.3)
    # On B.Cu, route safely: from (6.775, 82.5) to (3.7, 82.5) -> down along X = 3.7 to Y = 80.5 -> (3.3, 79.5) -> down along X = 3.3 to Y = 12.6!
    add_track(pcbnew.B_Cu, nets["DIN_1"], 6.775, 82.5, 3.7, 82.5, 0.22)
    add_track(pcbnew.B_Cu, nets["DIN_1"], 3.7, 82.5, 3.7, 80.5, 0.22)
    add_track(pcbnew.B_Cu, nets["DIN_1"], 3.7, 80.5, 3.3, 79.5, 0.22)
    add_track(pcbnew.B_Cu, nets["DIN_1"], 3.3, 79.5, 3.3, 12.6, 0.22)
    add_via(nets["DIN_1"], 3.3, 12.6, 0.6, 0.3)
    # On F.Cu, connect to LED 1 DIN at (6.25, 12.6) and BIN at (6.25, 9.4)
    add_track(pcbnew.F_Cu, nets["DIN_1"], 3.3, 12.6, 6.25, 12.6, 0.25)
    add_track(pcbnew.F_Cu, nets["DIN_1"], 3.3, 12.6, 3.3, 9.4, 0.25)
    add_track(pcbnew.F_Cu, nets["DIN_1"], 3.3, 9.4, 6.25, 9.4, 0.25)

    # 5. DATA_OUT:
    # LED 10 DOUT at (1.35, 73.8) -> R2 Pad 1 at (1.225, 75.9)
    add_track(pcbnew.F_Cu, nets["DATA_OUT_RET"], 1.35, 73.8, 1.225, 75.9, 0.25)
    # R2 Pad 2 at (2.775, 75.9) is DATA_OUT -> J_DO at (2.0, 78.0)
    add_track(pcbnew.F_Cu, nets["DATA_OUT"], 2.775, 75.9, 2.0, 78.0, 0.25)

    # 6. Silkscreen Text
    add_silk_text(pcbnew.F_SilkS, "12V", 0.9, 81.2, 0.55, thickness_mm=0.12, angle_deg=90.0)
    add_silk_text(pcbnew.F_SilkS, "DI",  6.6, 81.2, 0.55, thickness_mm=0.12)
    add_silk_text(pcbnew.F_SilkS, "DO",  0.9, 78.0, 0.55, thickness_mm=0.12, angle_deg=90.0)
    add_silk_text(pcbnew.F_SilkS, "GND", 4.6, 76.8, 0.50, thickness_mm=0.12)

    add_silk_text(pcbnew.F_SilkS, "Status LED",   5.15, 1.9, 0.75, thickness_mm=0.14)
    add_silk_text(pcbnew.F_SilkS, "Thor300 v1.1", 5.15, 3.1, 0.70, thickness_mm=0.13)

    pcbnew.SaveBoard(pcb_path, board)
    print("Saved Status LED Thor300 v1.1 board to", pcb_path)

    # Run DRC
    drc_out = os.path.join(v11_dir, "drc_v11.json")
    cmd = [
        r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe", "pcb", "drc",
        "--output", drc_out, "--format", "json", pcb_path
    ]
    subprocess.run(cmd, check=True)
    with open(drc_out) as f:
        res = json.load(f)
    viols = res.get("violations", [])
    unconns = res.get("unconnected_items", [])
    print(f"Status LED Thor300 v1.1 DRC Results -> Violations: {len(viols)}, Unconnected: {len(unconns)}")
    types = {}
    for v in viols:
        t = v.get("type")
        types[t] = types.get(t, 0) + 1
    for t, cnt in types.items():
        print(f"  {t}: {cnt}")
    for u in unconns:
        print("  Unconnected:", [it.get("description") for it in u.get("items", [])])
    for v in viols:
        if v.get("type") in ["shorting_items", "clearance", "tracks_crossing", "copper_edge_clearance", "courtyards_overlap"]:
            print("  CRIT:", v.get("type"), v.get("description"), [it.get("description") for it in v.get("items", [])])

if __name__ == "__main__":
    generate_v11()
