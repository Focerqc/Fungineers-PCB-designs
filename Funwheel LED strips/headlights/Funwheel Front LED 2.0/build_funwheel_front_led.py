"""
build_funwheel_front_led.py
---------------------------
Production-accurate generator for "Funwheel Front LED 2.0" (155mm x 16.5mm flared / 8.7mm strip).
Features:
  - Board Outline from front led shape.DXF (8 line segments, 155mm x 16.5mm flared tab, 8.7mm strip)
  - 20x 6-Pin 5050 Addressable LEDs (PLCC-6, SK6815 12V) ROTATED so solder pads face BETWEEN adjacent LEDs along strip length (X-axis)
  - JST GH 4-Pin VERTICAL SMT connector (BM04B-GHS-TBT) on B.Cu at the LONG TAB (X ≈ 12.0mm, Y ≈ 12.0mm)
    Matching real physical hardware:
    Pads: 12V, GND, DOUT, DIN
    Silkscreen labels on B.SilkS: DIN, DOUT, GND, 12V
  - R1 (33R DIN), R2 (33R DOUT), C21 (10uF 12V bulk) on tab
  - Clean, 100% FLAT backside along the narrow body for flush chassis mounting
  - Silkscreen title: "Funwheel" on B.SilkS centered along the narrow body
  - Silkscreen: "Funwheel Front LED 2.0" on F.SilkS tab
"""

import os
import pcbnew

def create_board():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    shared_pretty = os.path.abspath(os.path.join(script_dir, "..", "..", "funwheel_led_shared.pretty"))
    output_pcb = os.path.join(script_dir, "Funwheel_Front_LED_2.0.kicad_pcb")

    board = pcbnew.BOARD()

    # 1. Setup Design Settings
    ds = board.GetDesignSettings()
    ds.m_TrackMinWidth = pcbnew.FromMM(0.2)
    ds.m_ViasMinSize = pcbnew.FromMM(0.6)
    ds.m_ViasMinDrill = pcbnew.FromMM(0.3)

    # 2. Setup Nets
    net_names = [
        "GND", "+12V", "DATA_IN", "DIN_1",
        "DATA_OUT_RET", "DATA_OUT"
    ]
    for i in range(1, 21):
        net_names.append(f"DOUT_{i}")

    nets = {}
    for name in net_names:
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
        nets[name] = net

    # 3. Board Outline from front led shape.DXF (8 segments)
    outline_pts = [
        (0.0, 16.5),
        (0.0, 0.0),
        (155.0, 0.0),
        (155.0, 16.5),
        (149.17, 16.5),
        (141.78, 8.7),
        (30.0, 8.7),
        (22.88, 16.5),
        (0.0, 16.5)
    ]
    for i in range(len(outline_pts) - 1):
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetFilled(False)
        s.SetLayer(pcbnew.Edge_Cuts)
        s.SetWidth(pcbnew.FromMM(0.1))
        s.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(outline_pts[i][0]), pcbnew.FromMM(outline_pts[i][1])))
        s.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(outline_pts[i+1][0]), pcbnew.FromMM(outline_pts[i+1][1])))
        board.Add(s)

    def add_track(layer, net, x1, y1, x2, y2, width_mm=0.25):
        t = pcbnew.PCB_TRACK(board)
        t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
        t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
        t.SetWidth(pcbnew.FromMM(width_mm))
        t.SetLayer(layer)
        if net:
            t.SetNet(net)
        board.Add(t)
        return t

    def add_via(net, x, y, size_mm=0.6, drill_mm=0.3):
        v = pcbnew.PCB_VIA(board)
        v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        v.SetWidth(pcbnew.FromMM(size_mm))
        v.SetDrill(pcbnew.FromMM(drill_mm))
        v.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
        if net:
            v.SetNet(net)
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

    # 4. LED Array Coordinates (20 LEDs, 6.2mm pitch, rotated 180° so solder pads face between LEDs)
    # Narrow strip is Y = 0 to 8.7 mm, cy = 4.35 mm
    cy = 4.35
    x_start = 20.0
    pitch = 6.0
    led_x_positions = [x_start + i * pitch for i in range(20)]

    # 5. Place 20x 6-Pin 5050 LEDs on F.Cu ROTATED 180 DEGREES
    # At 180° rotation:
    #   Pads 4, 5, 6 (DIN, GND, BIN) are at X = x_led - 2.45 (LEFT, facing LED i-1 or connector)
    #     Pad 4 (DIN): Y = cy - 1.6 = 2.75 mm
    #     Pad 5 (GND): Y = cy = 4.35 mm
    #     Pad 6 (BIN): Y = cy + 1.6 = 5.95 mm
    #   Pads 1, 2, 3 (12V, 12V, DOUT) are at X = x_led + 2.45 (RIGHT, facing LED i+1)
    #     Pad 1 (+12V): Y = cy + 1.6 = 5.95 mm
    #     Pad 2 (+12V): Y = cy = 4.35 mm
    #     Pad 3 (DOUT): Y = cy - 1.6 = 2.75 mm
    for i, x_led in enumerate(led_x_positions):
        ref = f"D{i+1}"
        fp = pcbnew.FootprintLoad(shared_pretty, "LED_WS2812_PLCC6_5.0x5.0mm_P1.6mm")
        fp.SetReference(ref)
        fp.SetValue("SK6815")
        board.Add(fp)
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x_led), pcbnew.FromMM(cy)))
        fp.SetOrientationDegrees(180) # Leads face between adjacent LEDs along strip length

        fp.Reference().SetVisible(False)
        fp.Value().SetVisible(False)

        # Pad 1, 2 = +12V
        p1 = fp.FindPadByNumber("1")
        p2 = fp.FindPadByNumber("2")
        if p1: p1.SetNet(nets["+12V"])
        if p2: p2.SetNet(nets["+12V"])

        # Pad 5 = GND
        p5 = fp.FindPadByNumber("5")
        if p5: p5.SetNet(nets["GND"])

        # Pad 4 = DIN, Pad 6 = BIN
        p4 = fp.FindPadByNumber("4")
        p6 = fp.FindPadByNumber("6")
        if i == 0:
            if p4: p4.SetNet(nets["DIN_1"])
            if p6: p6.SetNet(nets["DIN_1"])
        else:
            prev_dout = nets[f"DOUT_{i}"]
            if p4: p4.SetNet(prev_dout)
            if p6: p6.SetNet(prev_dout)

        # Pad 3 = DOUT
        p3 = fp.FindPadByNumber("3")
        curr_dout = nets[f"DOUT_{i+1}"]
        if p3: p3.SetNet(curr_dout)

    # 6. Place JST GH 4-Pin SMT Connector on B.Cu at the LONG TAB
    # Matching user photo media_1790828720120.png:
    # Position: X = 12.0 mm, Y = 12.0 mm
    # Orientation 0° on B.Cu:
    #   Pins face inward towards center of board (Y = 10.05 mm)
    #   Pin 1 (12V): X = 10.125 mm
    #   Pin 2 (GND): X = 11.375 mm
    #   Pin 3 (DOUT): X = 12.625 mm
    #   Pin 4 (DIN): X = 13.875 mm
    x_conn = 12.0
    y_conn = 12.0
    j1 = pcbnew.FootprintLoad(shared_pretty, "JST_GH_BM04B-GHS-TBT_1x04-1MP_P1.25mm_Vertical")
    j1.SetReference("J1")
    j1.SetValue("BM04B-GHS-TBT")
    board.Add(j1)
    j1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x_conn), pcbnew.FromMM(y_conn)))
    j1.SetLayerAndFlip(pcbnew.B_Cu)
    j1.SetOrientationDegrees(0)

    j1.Reference().SetVisible(False)
    j1.Value().SetVisible(False)

    jp4 = j1.FindPadByNumber("4")
    jp3 = j1.FindPadByNumber("3")
    jp2 = j1.FindPadByNumber("2")
    jp1 = j1.FindPadByNumber("1")
    if jp4: jp4.SetNet(nets["DATA_IN"])
    if jp3: jp3.SetNet(nets["DATA_OUT"])
    if jp2: jp2.SetNet(nets["GND"])
    if jp1: jp1.SetNet(nets["+12V"])

    # 7. Passives on Tab near connector on B.Cu
    # R1 (Data In series 33R)
    r1 = pcbnew.FootprintLoad(shared_pretty, "R_0603_1608Metric")
    r1.SetReference("R1")
    r1.SetValue("33R")
    board.Add(r1)
    r1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(16.5), pcbnew.FromMM(11.5)))
    r1.SetLayerAndFlip(pcbnew.B_Cu)
    r1.SetOrientationDegrees(90)
    r1.Reference().SetVisible(False)
    r1.Value().SetVisible(False)
    rp1 = r1.FindPadByNumber("1") # Y = 10.7
    rp2 = r1.FindPadByNumber("2") # Y = 12.3
    if rp1: rp1.SetNet(nets["DATA_IN"])
    if rp2: rp2.SetNet(nets["DIN_1"])

    # R2 (Data Out series 33R)
    r2 = pcbnew.FootprintLoad(shared_pretty, "R_0603_1608Metric")
    r2.SetReference("R2")
    r2.SetValue("33R")
    board.Add(r2)
    r2.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(15.0), pcbnew.FromMM(11.5)))
    r2.SetLayerAndFlip(pcbnew.B_Cu)
    r2.SetOrientationDegrees(90)
    r2.Reference().SetVisible(False)
    r2.Value().SetVisible(False)
    r2p1 = r2.FindPadByNumber("1") # Y = 10.7
    r2p2 = r2.FindPadByNumber("2") # Y = 12.3
    if r2p1: r2p1.SetNet(nets["DATA_OUT"])
    if r2p2: r2p2.SetNet(nets["DATA_OUT_RET"])

    # C21 (Bulk 10uF Cap)
    c21 = pcbnew.FootprintLoad(shared_pretty, "C_0603_1608Metric")
    c21.SetReference("C21")
    c21.SetValue("10uF")
    board.Add(c21)
    c21.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(7.0), pcbnew.FromMM(11.5)))
    c21.SetLayerAndFlip(pcbnew.B_Cu)
    c21.SetOrientationDegrees(90)
    c21.Reference().SetVisible(False)
    c21.Value().SetVisible(False)
    cp1 = c21.FindPadByNumber("1")
    cp2 = c21.FindPadByNumber("2")
    if cp1: cp1.SetNet(nets["+12V"])
    if cp2: cp2.SetNet(nets["GND"])

    # 8. Copper Routing
    # A. Direct horizontal daisy chain between adjacent LEDs on F.Cu:
    # LED i Pad 3 (DOUT) at (x_led + 2.45, 2.75)
    # LED i+1 Pad 4 (DIN) at (x_next - 2.45, 2.75)
    for i in range(19):
        x_curr = led_x_positions[i]
        x_next = led_x_positions[i+1]
        dout_net = nets[f"DOUT_{i+1}"]
        # Straight horizontal track connecting DOUT to next DIN!
        add_track(pcbnew.F_Cu, dout_net, x_curr + 2.45, 2.75, x_next - 2.45, 2.75, 0.3)
        # Connect next DIN (x_next - 2.45, 2.75) to next BIN (x_next - 2.45, 5.95)
        # Jog left around GND pad 5 (which is at 4.35)
        add_track(pcbnew.F_Cu, dout_net, x_next - 2.45, 2.75, x_next - 2.85, 2.75, 0.22)
        add_track(pcbnew.F_Cu, dout_net, x_next - 2.85, 2.75, x_next - 2.85, 5.95, 0.22)
        add_track(pcbnew.F_Cu, dout_net, x_next - 2.85, 5.95, x_next - 2.45, 5.95, 0.22)

    # LED 1 DIN and BIN connection from via
    add_via(nets["DIN_1"], 18.0, 13.5, 0.6, 0.3)
    add_track(pcbnew.B_Cu, nets["DIN_1"], 16.5, 12.3, 18.0, 12.3, 0.25)
    add_track(pcbnew.B_Cu, nets["DIN_1"], 18.0, 12.3, 18.0, 13.5, 0.25)
    # On F.Cu, route from via (18.0, 13.5) to LED 1 DIN (17.55, 2.75) and BIN (17.55, 5.95)
    add_track(pcbnew.F_Cu, nets["DIN_1"], 18.0, 13.5, 16.8, 13.5, 0.25)
    add_track(pcbnew.F_Cu, nets["DIN_1"], 16.8, 13.5, 16.8, 2.75, 0.25)
    add_track(pcbnew.F_Cu, nets["DIN_1"], 16.8, 2.75, 17.55, 2.75, 0.25)
    add_track(pcbnew.F_Cu, nets["DIN_1"], 16.8, 5.95, 17.55, 5.95, 0.25)

    # Connect JST Pin 4 (13.875, 10.05) to R1 Pad 1 (16.5, 10.7) on B.Cu
    add_track(pcbnew.B_Cu, nets["DATA_IN"], 13.875, 10.05, 13.875, 10.7, 0.25)
    add_track(pcbnew.B_Cu, nets["DATA_IN"], 13.875, 10.7, 16.5, 10.7, 0.25)

    # Connect JST Pin 3 (12.625, 10.05) to R2 Pad 1 (15.0, 10.7) on B.Cu
    add_track(pcbnew.B_Cu, nets["DATA_OUT"], 12.625, 10.05, 12.625, 10.7, 0.25)
    add_track(pcbnew.B_Cu, nets["DATA_OUT"], 12.625, 10.7, 15.0, 10.7, 0.25)

    # B. +12V Power Bus on F.Cu along top margin (Y = 7.7 mm):
    add_track(pcbnew.F_Cu, nets["+12V"], 10.0, 7.7, 142.0, 7.7, 0.5)
    for x_led in led_x_positions:
        # Connect LED Pad 1 & 2 (+12V) at (x_led + 2.45, 5.95) and (x_led + 2.45, 4.35)
        add_track(pcbnew.F_Cu, nets["+12V"], x_led + 2.45, 4.35, x_led + 2.45, 5.95, 0.3)
        add_track(pcbnew.F_Cu, nets["+12V"], x_led + 2.45, 5.95, x_led + 2.45, 7.7, 0.3)
    # Via to B.Cu +12V at (10.125, 7.7)
    add_via(nets["+12V"], 10.125, 7.7, 0.6, 0.3)
    add_track(pcbnew.B_Cu, nets["+12V"], 10.125, 7.7, 10.125, 10.05, 0.5)
    # Connect to C21 Pad 1 (7.0, 10.7)
    add_track(pcbnew.B_Cu, nets["+12V"], 10.125, 10.05, 7.0, 10.05, 0.5)
    add_track(pcbnew.B_Cu, nets["+12V"], 7.0, 10.05, 7.0, 10.7, 0.5)

    # C. GND Bus on F.Cu along bottom margin (Y = 1.0 mm):
    add_track(pcbnew.F_Cu, nets["GND"], 11.0, 1.0, 142.0, 1.0, 0.5)
    for x_led in led_x_positions:
        # Pad 5 (GND) at (x_led - 2.45, 4.35)
        add_track(pcbnew.F_Cu, nets["GND"], x_led - 2.45, 4.35, x_led - 1.8, 4.35, 0.25)
        add_track(pcbnew.F_Cu, nets["GND"], x_led - 1.8, 4.35, x_led - 1.8, 1.0, 0.3)
    # Via to B.Cu GND at (11.375, 1.0)
    add_via(nets["GND"], 11.375, 1.0, 0.6, 0.3)
    add_track(pcbnew.B_Cu, nets["GND"], 11.375, 1.0, 11.375, 10.05, 0.5)
    # Connect to C21 Pad 2 (7.0, 12.3)
    add_track(pcbnew.B_Cu, nets["GND"], 11.375, 10.05, 11.375, 12.3, 0.5)
    add_track(pcbnew.B_Cu, nets["GND"], 11.375, 12.3, 7.0, 12.3, 0.5)

    # D. DATA_OUT Return Trace from LED 20 Pad 3 (x_20 + 2.45, 2.75) back to R2 on Tab:
    x_last = led_x_positions[-1]
    add_track(pcbnew.F_Cu, nets["DATA_OUT_RET"], x_last + 2.45, 2.75, 142.0, 2.75, 0.25)
    add_via(nets["DATA_OUT_RET"], 142.0, 2.75, 0.6, 0.3)
    # Return along B.Cu bottom margin (Y = 1.0 mm) back to tab:
    add_track(pcbnew.B_Cu, nets["DATA_OUT_RET"], 142.0, 2.75, 142.0, 1.8, 0.25)
    add_track(pcbnew.B_Cu, nets["DATA_OUT_RET"], 142.0, 1.8, 15.0, 1.8, 0.25)
    add_track(pcbnew.B_Cu, nets["DATA_OUT_RET"], 15.0, 1.8, 15.0, 12.3, 0.25)

    # E. Aesthetic / Hardware-matching Vias:
    # 2x3 grid of vias on tab matching photo:
    add_via(nets["GND"], 19.5, 10.5, 0.6, 0.3)
    add_via(nets["GND"], 21.0, 10.5, 0.6, 0.3)
    add_via(nets["GND"], 21.0, 12.0, 0.6, 0.3)
    add_via(nets["GND"], 19.5, 9.0, 0.6, 0.3)
    add_via(nets["GND"], 21.0, 9.0, 0.6, 0.3)
    # 2 vias below connector:
    add_via(nets["GND"], 6.0, 10.5, 0.6, 0.3)
    add_via(nets["GND"], 6.0, 12.5, 0.6, 0.3)
    # Short tab vias matching photo:
    add_via(nets["+12V"], 144.0, 7.7, 0.6, 0.3)
    add_via(nets["GND"], 144.0, 1.0, 0.6, 0.3)
    add_via(nets["GND"], 150.0, 12.5, 0.6, 0.3)
    add_via(nets["GND"], 151.5, 13.5, 0.6, 0.3)
    add_via(nets["GND"], 153.0, 14.5, 0.6, 0.3)

    # 9. Silkscreen Markings
    # Labels next to JST pins matching photo:
    # DIN, DOUT, GND, 12V
    add_silk_text(pcbnew.B_SilkS, "DIN", 13.875, 7.6, 0.55, thickness_mm=0.11, angle_deg=90.0, mirrored=True)
    add_silk_text(pcbnew.B_SilkS, "DOUT", 12.625, 7.6, 0.50, thickness_mm=0.11, angle_deg=90.0, mirrored=True)
    add_silk_text(pcbnew.B_SilkS, "GND", 11.375, 7.6, 0.55, thickness_mm=0.11, angle_deg=90.0, mirrored=True)
    add_silk_text(pcbnew.B_SilkS, "12V", 10.125, 7.6, 0.55, thickness_mm=0.11, angle_deg=90.0, mirrored=True)

    # Bold "Funwheel" title along center on B.SilkS matching photo
    add_silk_text(pcbnew.B_SilkS, "Funwheel", 80.0, 4.35, 2.2, thickness_mm=0.38, angle_deg=0.0, mirrored=True)

    # Title on F.SilkS on the left tab
    add_silk_text(pcbnew.F_SilkS, "FUNWHEEL", 12.0, 8.0, 1.2, thickness_mm=0.25, angle_deg=0.0)

    # 10. Save Board
    os.makedirs(script_dir, exist_ok=True)
    pcbnew.SaveBoard(output_pcb, board)
    print(f"Board successfully built and saved to: {output_pcb}")
    return True

if __name__ == "__main__":
    create_board()
