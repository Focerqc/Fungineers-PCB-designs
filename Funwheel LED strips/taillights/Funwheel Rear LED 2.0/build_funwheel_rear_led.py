"""
build_funwheel_rear_led.py
--------------------------
Production-accurate generator for "Funwheel Rear LED 2.0" (155mm x 6.85mm).
Features:
  - 16x 6-Pin 5050 Addressable LEDs (PLCC-6) ROTATED 90 DEGREES
    Solder pads face between adjacent LEDs along the strip length (Y-axis)
  - 4 Groups of 4 LEDs (8.0mm intra-group pitch, 11.5mm inter-group gap)
  - JST GH 4-Pin VERTICAL / TOP-ENTRY SMT connector (BM04B-GHS-TBT) on B.Cu
    Pins on right side, socket opening facing upward
  - 3 passives near connector (R1, R2, C17) oriented vertically side-by-side:
    Left: R1 (33R Data In, black)
    Middle: R2 (33R Data Out, black)
    Right: C17 (10uF Bulk Cap, brown)
  - Decoupling capacitors (0603) under each LED on B.Cu oriented vertically
  - Silkscreen labels matching physical reference: in, out, g, 12v on B.SilkS
  - Silkscreen title: "Funwheel Rear LED 2.0" vertically along margin on F.SilkS and B.SilkS
"""

import os
import pcbnew

def create_board():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    shared_pretty = os.path.abspath(os.path.join(script_dir, "..", "..", "funwheel_led_shared.pretty"))
    output_pcb = os.path.join(script_dir, "Funwheel_Rear_LED_2.0.kicad_pcb")

    board = pcbnew.BOARD()

    # 1. Setup Design Settings
    ds = board.GetDesignSettings()
    ds.m_TrackMinWidth = pcbnew.FromMM(0.2)
    ds.m_ViasMinSize = pcbnew.FromMM(0.6)
    ds.m_ViasMinDrill = pcbnew.FromMM(0.3)

    # 2. Setup Nets
    net_names = [
        "GND", "+12V", "DATA_IN", "DIN_1",
        "DOUT_1", "DOUT_2", "DOUT_3", "DOUT_4",
        "DOUT_5", "DOUT_6", "DOUT_7", "DOUT_8",
        "DOUT_9", "DOUT_10", "DOUT_11", "DOUT_12",
        "DOUT_13", "DOUT_14", "DOUT_15", "DOUT_16",
        "DATA_OUT_RET", "DATA_OUT"
    ]
    nets = {}
    for name in net_names:
        net = pcbnew.NETINFO_ITEM(board, name)
        board.Add(net)
        nets[name] = net

    # 3. Board Outline (155.0 mm x 6.85 mm)
    w_mm = 6.85
    h_mm = 155.0
    outline = pcbnew.PCB_SHAPE(board)
    outline.SetShape(pcbnew.SHAPE_T_RECT)
    outline.SetFilled(False)
    outline.SetLayer(pcbnew.Edge_Cuts)
    outline.SetWidth(pcbnew.FromMM(0.1))
    outline.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(0.0), pcbnew.FromMM(0.0)))
    outline.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(w_mm), pcbnew.FromMM(h_mm)))
    board.Add(outline)

    # Helper function to place tracks
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

    # Helper function to place vias
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

    # 4. Compute 16 LED Y positions in 4 Groups of 4 LEDs
    cx = 3.425
    p_intra = 8.0   # 3.0 mm gap between 5.0 mm packages within group
    p_inter = 11.5  # 6.5 mm gap between groups
    y_start = 6.5

    led_y_positions = []
    current_y = y_start
    for group in range(4):
        for member in range(4):
            if group == 0 and member == 0:
                current_y = y_start
            elif member == 0:
                current_y += p_inter
            else:
                current_y += p_intra
            led_y_positions.append(current_y)

    # 5. Place 16x 6-Pin 5050 LEDs on F.Cu ROTATED 90 DEGREES
    # At 90 degrees rotation:
    # Package center: (cx, y_led)
    # Bottom pads (Y = y_led + 2.45):
    #   Pad 1 (VDD): X = cx - 1.60 = 1.825 mm
    #   Pad 2 (VDD): X = cx        = 3.425 mm
    #   Pad 3 (DOUT): X = cx + 1.60 = 5.025 mm
    # Top pads (Y = y_led - 2.45):
    #   Pad 6 (BIN): X = cx - 1.60 = 1.825 mm
    #   Pad 5 (GND): X = cx        = 3.425 mm
    #   Pad 4 (DIN): X = cx + 1.60 = 5.025 mm
    for i, y_led in enumerate(led_y_positions):
        ref = f"D{i+1}"
        fp = pcbnew.FootprintLoad(shared_pretty, "LED_WS2812_PLCC6_5.0x5.0mm_P1.6mm")
        fp.SetReference(ref)
        fp.SetValue("SK6815")
        board.Add(fp)
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(cx), pcbnew.FromMM(y_led)))
        fp.SetOrientationDegrees(90) # Solder pads between LEDs along Y axis

        # Hide text for clean production look
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

    # 6. Place 16x 0603 Decoupling Capacitors on B.Cu (VERTICALLY ORIENTED)
    # Turned 90 degrees along the board length directly behind each LED
    for i, y_cap in enumerate(led_y_positions):
        ref = f"C{i+1}"
        fp = pcbnew.FootprintLoad(shared_pretty, "C_0603_1608Metric")
        fp.SetReference(ref)
        fp.SetValue("0.1uF")
        board.Add(fp)
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(cx), pcbnew.FromMM(y_cap)))
        fp.SetLayerAndFlip(pcbnew.B_Cu)
        fp.SetOrientationDegrees(90) # Vertical orientation along board length

        fp.Reference().SetVisible(False)
        fp.Value().SetVisible(False)

        p1 = fp.FindPadByNumber("1") # Pad 1 at Y - 0.8
        p2 = fp.FindPadByNumber("2") # Pad 2 at Y + 0.8
        if p1: p1.SetNet(nets["GND"])
        if p2: p2.SetNet(nets["+12V"])

    # 7. Place JST GH 4-Pin VERTICAL / TOP-ENTRY Connector on B.Cu
    # Receptacle opens upward (away from board surface)
    # With Orientation 90 on B.Cu:
    #   Pads 1..4 are at X = 1.475 mm (rendered on the right side of the connector!)
    #   Pad 4 (top): Y = 143.625 mm -> DATA_IN ('in')
    #   Pad 3:       Y = 144.875 mm -> DATA_OUT ('out')
    #   Pad 2:       Y = 146.125 mm -> GND ('g')
    #   Pad 1 (bot): Y = 147.375 mm -> +12V ('12v')
    #   MP pads:     X = 4.825 mm (rendered on left side)
    y_conn = 145.5
    j1 = pcbnew.FootprintLoad(shared_pretty, "JST_GH_BM04B-GHS-TBT_1x04-1MP_P1.25mm_Vertical")
    j1.SetReference("J1")
    j1.SetValue("BM04B-GHS-TBT")
    board.Add(j1)
    j1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(3.425), pcbnew.FromMM(y_conn)))
    j1.SetLayerAndFlip(pcbnew.B_Cu)
    j1.SetOrientationDegrees(90) # Solder pins on right edge, socket facing upward

    j1.Reference().SetVisible(False)
    j1.Value().SetVisible(False)

    jp4 = j1.FindPadByNumber("4") # top pin (Y = 143.625)
    jp3 = j1.FindPadByNumber("3") # (Y = 144.875)
    jp2 = j1.FindPadByNumber("2") # (Y = 146.125)
    jp1 = j1.FindPadByNumber("1") # bot pin (Y = 147.375)
    if jp4: jp4.SetNet(nets["DATA_IN"])
    if jp3: jp3.SetNet(nets["DATA_OUT"])
    if jp2: jp2.SetNet(nets["GND"])
    if jp1: jp1.SetNet(nets["+12V"])

    # 8. Place 3 Passives near Connector on B.Cu (VERTICALLY ORIENTED side-by-side)
    # Matching media_1790771586565.png:
    # Left: Resistor R1 (33R Data In, black) at X = 4.6 mm
    # Middle: Resistor R2 (33R Data Out, black) at X = 3.3 mm
    # Right: Bulk Capacitor C17 (10uF, brown) at X = 2.0 mm (aligned with 12V and GND pins)
    y_passives = 151.0

    r1 = pcbnew.FootprintLoad(shared_pretty, "R_0603_1608Metric")
    r1.SetReference("R1")
    r1.SetValue("33R")
    board.Add(r1)
    r1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(4.6), pcbnew.FromMM(y_passives)))
    r1.SetLayerAndFlip(pcbnew.B_Cu)
    r1.SetOrientationDegrees(90)
    r1.Reference().SetVisible(False)
    r1.Value().SetVisible(False)
    rp1 = r1.FindPadByNumber("1")
    rp2 = r1.FindPadByNumber("2")
    if rp1: rp1.SetNet(nets["DATA_IN"])
    if rp2: rp2.SetNet(nets["DIN_1"])

    r2 = pcbnew.FootprintLoad(shared_pretty, "R_0603_1608Metric")
    r2.SetReference("R2")
    r2.SetValue("33R")
    board.Add(r2)
    r2.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(3.3), pcbnew.FromMM(y_passives)))
    r2.SetLayerAndFlip(pcbnew.B_Cu)
    r2.SetOrientationDegrees(90)
    r2.Reference().SetVisible(False)
    r2.Value().SetVisible(False)
    r2p1 = r2.FindPadByNumber("1")
    r2p2 = r2.FindPadByNumber("2")
    if r2p1: r2p1.SetNet(nets["DATA_OUT"])
    if r2p2: r2p2.SetNet(nets["DATA_OUT_RET"])

    c17 = pcbnew.FootprintLoad(shared_pretty, "C_0603_1608Metric")
    c17.SetReference("C17")
    c17.SetValue("10uF")
    board.Add(c17)
    c17.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(2.0), pcbnew.FromMM(y_passives)))
    c17.SetLayerAndFlip(pcbnew.B_Cu)
    c17.SetOrientationDegrees(90)
    c17.Reference().SetVisible(False)
    c17.Value().SetVisible(False)
    cp1 = c17.FindPadByNumber("1")
    cp2 = c17.FindPadByNumber("2")
    if cp1: cp1.SetNet(nets["+12V"])
    if cp2: cp2.SetNet(nets["GND"])

    # 9. Copper Routing
    # A. +12V Bus on F.Cu along left edge (X = 0.85 mm):
    first_y = led_y_positions[0] - 2.45
    last_y = led_y_positions[-1] + 2.45
    add_track(pcbnew.F_Cu, nets["+12V"], 0.85, first_y, 0.85, last_y, 0.6)
    # Stubs from +12V bus to Pad 1 of each LED (at X = 1.825, Y = y_led + 2.45)
    for y_led in led_y_positions:
        add_track(pcbnew.F_Cu, nets["+12V"], 0.85, y_led + 2.45, 1.825, y_led + 2.45, 0.35)
        # Pad 1 to Pad 2 (at X = 3.425, Y = y_led + 2.45)
        add_track(pcbnew.F_Cu, nets["+12V"], 1.825, y_led + 2.45, 3.425, y_led + 2.45, 0.35)

    # +12V extension down to connector on B.Cu:
    add_track(pcbnew.F_Cu, nets["+12V"], 0.85, last_y, 0.85, 147.375, 0.5)
    add_via(nets["+12V"], 0.85, 147.375, 0.6, 0.3)
    add_track(pcbnew.B_Cu, nets["+12V"], 0.85, 147.375, 1.475, 147.375, 0.4)
    # Connect to C17 Pad 1 (2.0, 150.2)
    add_track(pcbnew.B_Cu, nets["+12V"], 1.475, 147.375, 2.0, 147.375, 0.4)
    add_track(pcbnew.B_Cu, nets["+12V"], 2.0, 147.375, 2.0, 150.2, 0.4)

    # B. GND Bus on F.Cu along right edge (X = 6.00 mm):
    add_track(pcbnew.F_Cu, nets["GND"], 6.00, first_y, 6.00, last_y, 0.6)
    # Stubs from GND bus to Pad 5 of each LED (at X = 3.425, Y = y_led - 2.45):
    for y_led in led_y_positions:
        add_track(pcbnew.F_Cu, nets["GND"], 6.00, y_led - 2.45, 3.425, y_led - 2.45, 0.35)

    # GND extension down to connector on B.Cu:
    add_track(pcbnew.F_Cu, nets["GND"], 6.00, last_y, 6.00, 146.125, 0.5)
    add_via(nets["GND"], 6.00, 146.125, 0.6, 0.3)
    add_track(pcbnew.B_Cu, nets["GND"], 6.00, 146.125, 1.475, 146.125, 0.4)
    # Connect to C17 Pad 2 (2.0, 151.8)
    add_track(pcbnew.B_Cu, nets["GND"], 1.475, 146.125, 1.475, 151.8, 0.4)
    add_track(pcbnew.B_Cu, nets["GND"], 1.475, 151.8, 2.0, 151.8, 0.4)

    # C. Decoupling Capacitors Connections (C1 to C16 on B.Cu):
    for y_led in led_y_positions:
        # GND via & trace:
        add_via(nets["GND"], 3.425, y_led - 1.6, 0.5, 0.25)
        add_track(pcbnew.F_Cu, nets["GND"], 3.425, y_led - 2.45, 3.425, y_led - 1.6, 0.3)
        add_track(pcbnew.B_Cu, nets["GND"], 3.425, y_led - 1.6, 3.425, y_led - 0.8, 0.3)

        # +12V via & trace:
        add_via(nets["+12V"], 3.425, y_led + 1.6, 0.5, 0.25)
        add_track(pcbnew.F_Cu, nets["+12V"], 3.425, y_led + 2.45, 3.425, y_led + 1.6, 0.3)
        add_track(pcbnew.B_Cu, nets["+12V"], 3.425, y_led + 1.6, 3.425, y_led + 0.8, 0.3)

    # D. DATA Daisy Chain on F.Cu:
    # Direct vertical traces connecting DOUT of LED i to DIN of LED i+1:
    # DOUT is at (5.025, y_i + 2.45)
    # DIN is at (5.025, y_{i+1} - 2.45)
    for i in range(15):
        y_curr = led_y_positions[i]
        y_next = led_y_positions[i+1]
        dout_y = y_curr + 2.45
        din_y = y_next - 2.45
        net = nets[f"DOUT_{i+1}"]
        # Straight vertical connection between LEDs!
        add_track(pcbnew.F_Cu, net, 5.025, dout_y, 5.025, din_y, 0.3)
        # Connect BIN (at 1.825, din_y) to DIN (at 5.025, din_y)
        add_track(pcbnew.F_Cu, net, 1.825, din_y, 3.0, din_y, 0.25)
        add_track(pcbnew.F_Cu, net, 3.0, din_y, 3.425, din_y - 0.5, 0.25)
        add_track(pcbnew.F_Cu, net, 3.425, din_y - 0.5, 4.5, din_y - 0.5, 0.25)
        add_track(pcbnew.F_Cu, net, 4.5, din_y - 0.5, 5.025, din_y, 0.25)

    # E. DATA_IN: From J1 Pin 4 (1.475, 143.625) to R1 (4.6, 150.2) to LED 1 DIN (5.025, 4.05):
    add_track(pcbnew.B_Cu, nets["DATA_IN"], 1.475, 143.625, 4.6, 143.625, 0.25)
    add_track(pcbnew.B_Cu, nets["DATA_IN"], 4.6, 143.625, 4.6, 150.2, 0.25)
    # From R1 Pad 2 (4.6, 151.8) trace running up B.Cu all the way to LED 1:
    add_track(pcbnew.B_Cu, nets["DIN_1"], 4.6, 151.8, 4.6, 153.5, 0.25)
    add_track(pcbnew.B_Cu, nets["DIN_1"], 4.6, 153.5, 5.5, 153.5, 0.25)
    add_track(pcbnew.B_Cu, nets["DIN_1"], 5.5, 153.5, 5.5, 3.0, 0.25)
    add_via(nets["DIN_1"], 5.5, 3.0, 0.6, 0.3)
    # On F.Cu, connect via to LED 1 DIN (5.025, 4.05) and BIN (1.825, 4.05):
    add_track(pcbnew.F_Cu, nets["DIN_1"], 5.5, 3.0, 5.025, 4.05, 0.25)
    add_track(pcbnew.F_Cu, nets["DIN_1"], 5.5, 3.0, 1.825, 4.05, 0.25)

    # F. DATA_OUT_RET: From LED 16 DOUT (5.025, 137.0 + 2.45 = 139.45) to R2 to J1 Pin 3:
    add_track(pcbnew.F_Cu, nets["DATA_OUT_RET"], 5.025, 139.45, 5.025, 141.0, 0.25)
    add_via(nets["DATA_OUT_RET"], 5.025, 141.0, 0.6, 0.3)
    add_track(pcbnew.B_Cu, nets["DATA_OUT_RET"], 5.025, 141.0, 3.3, 142.5, 0.25)
    add_track(pcbnew.B_Cu, nets["DATA_OUT_RET"], 3.3, 142.5, 3.3, 150.2, 0.25)
    # From R2 Pad 2 (3.3, 151.8) to J1 Pin 3 (1.475, 144.875):
    add_track(pcbnew.B_Cu, nets["DATA_OUT"], 3.3, 151.8, 3.3, 152.5, 0.25)
    add_track(pcbnew.B_Cu, nets["DATA_OUT"], 3.3, 152.5, 2.7, 152.5, 0.25)
    add_track(pcbnew.B_Cu, nets["DATA_OUT"], 2.7, 152.5, 2.7, 144.875, 0.25)
    add_track(pcbnew.B_Cu, nets["DATA_OUT"], 2.7, 144.875, 1.475, 144.875, 0.25)

    # 10. Silkscreen Markings
    def add_silk_text(layer, text_str, x, y, size=0.8, angle_deg=0, mirrored=False):
        t = pcbnew.PCB_TEXT(board)
        t.SetText(text_str)
        t.SetLayer(layer)
        t.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        t.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size), pcbnew.FromMM(size)))
        t.SetTextThickness(pcbnew.FromMM(0.12))
        t.SetTextAngleDegrees(angle_deg)
        t.SetMirrored(mirrored)
        t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
        t.SetVertJustify(pcbnew.GR_TEXT_V_ALIGN_CENTER)
        board.Add(t)
        return t

    # Labels right alongside the 4 JST GH pins on B.SilkS (Pad X = 1.475, label at X = 0.65 mm):
    # Pin 4 = in  (Y = 143.625)
    # Pin 3 = out (Y = 144.875)
    # Pin 2 = g   (Y = 146.125)
    # Pin 1 = 12v (Y = 147.375)
    add_silk_text(pcbnew.B_SilkS, "in", 0.65, 143.625, 0.45, mirrored=True)
    add_silk_text(pcbnew.B_SilkS, "out", 0.65, 144.875, 0.40, mirrored=True)
    add_silk_text(pcbnew.B_SilkS, "g", 0.65, 146.125, 0.50, mirrored=True)
    add_silk_text(pcbnew.B_SilkS, "12v", 0.65, 147.375, 0.40, mirrored=True)

    # Title on F.SilkS vertically in margin beside LED 1 (matching crop_top.png):
    add_silk_text(pcbnew.F_SilkS, "Funwheel Rear LED 2.0", 0.50, 16.0, 0.50, angle_deg=90.0, mirrored=False)

    # Title along back side (mirrored vertical text in middle gap)
    add_silk_text(pcbnew.B_SilkS, "Funwheel Rear LED 2.0", 1.25, 71.75, 0.70, angle_deg=90.0, mirrored=True)

    # 11. Save Board
    pcbnew.SaveBoard(output_pcb, board)
    print(f"Board successfully built and saved to: {output_pcb}")
    return True

if __name__ == "__main__":
    create_board()
