import os
import pcbnew  # type: ignore
import subprocess
from PIL import Image

def build_layout():
    project_dir = os.path.dirname(os.path.abspath(__file__))
    pcb_path = os.path.join(project_dir, "VFBMS32.kicad_pcb")
    kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints"
    custom_fp_dir = os.path.join(project_dir, "vfbms.pretty")

    if os.path.exists(pcb_path):
        board = pcbnew.LoadBoard(pcb_path)
    else:
        board = pcbnew.BOARD()

    # Clear old footprints
    footprints = list(board.GetFootprints())
    for fp in footprints:
        board.Remove(fp)

    # Design Settings
    ds = board.GetDesignSettings()
    ds.m_TrackMinWidth = pcbnew.FromMM(0.2)
    ds.m_ViasMinSize = pcbnew.FromMM(0.6)
    ds.m_ViasMinDrill = pcbnew.FromMM(0.3)
    ds.m_CopperEdgeClearance = pcbnew.FromMM(0.35)

    def add_line(x1, y1, x2, y2, layer=pcbnew.Edge_Cuts, width=0.15):
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_SEGMENT)
        s.SetFilled(False)
        s.SetLayer(layer)
        s.SetWidth(pcbnew.FromMM(width))
        s.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
        s.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
        board.Add(s)
        return s

    def add_arc_3pts(x_start, y_start, x_mid, y_mid, x_end, y_end, layer=pcbnew.Edge_Cuts, width=0.15):
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_ARC)
        s.SetFilled(False)
        s.SetLayer(layer)
        s.SetWidth(pcbnew.FromMM(width))
        s.SetArcGeometry(
            pcbnew.VECTOR2I(pcbnew.FromMM(x_start), pcbnew.FromMM(y_start)),
            pcbnew.VECTOR2I(pcbnew.FromMM(x_mid),   pcbnew.FromMM(y_mid)),
            pcbnew.VECTOR2I(pcbnew.FromMM(x_end),   pcbnew.FromMM(y_end))
        )
        board.Add(s)
        return s

    def add_rect(x1, y1, x2, y2, layer=pcbnew.F_SilkS, width=0.15):
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_RECTANGLE)
        s.SetFilled(False)
        s.SetLayer(layer)
        s.SetWidth(pcbnew.FromMM(width))
        s.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
        s.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
        board.Add(s)
        return s

    def add_text(layer, text, x, y, size=1.0, thickness=0.18, angle_deg=0.0, mirrored=False):
        t = pcbnew.PCB_TEXT(board)
        t.SetLayer(layer)
        t.SetText(text)
        t.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        t.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size), pcbnew.FromMM(size)))
        t.SetTextThickness(pcbnew.FromMM(thickness))
        t.SetTextAngle(pcbnew.EDA_ANGLE(angle_deg, pcbnew.DEGREES_T))
        t.SetMirrored(mirrored)
        t.SetHorizJustify(pcbnew.GR_TEXT_H_ALIGN_CENTER)
        t.SetVertJustify(pcbnew.GR_TEXT_V_ALIGN_CENTER)
        board.Add(t)
        return t

    # Clean existing drawings
    drawings = list(board.GetDrawings())
    for d in drawings:
        board.Remove(d)

    # 130mm x 32mm rounded rectangle board outline (1mm corner radius)
    r = 1.0
    w = 130.0
    h = 32.0
    add_line(r, 0, w - r, 0)
    add_arc_3pts(w - r, 0, w - r * (1 - 0.7071), r * (1 - 0.7071), w, r)
    add_line(w, r, w, h - r)
    add_arc_3pts(w, h - r, w - r * (1 - 0.7071), h - r * (1 - 0.7071), w - r, h)
    add_line(w - r, h, r, h)
    add_arc_3pts(r, h, r * (1 - 0.7071), h - r * (1 - 0.7071), 0, h - r)
    add_line(0, h - r, 0, r)
    add_arc_3pts(0, r, r * (1 - 0.7071), r * (1 - 0.7071), r, 0)

    # Footprints placement definition
    components = [
        # === 1. LEFT CORNER POWER CONNECTORS (XT30) ===
        # Top-Left: XT30 Female (CHG+ closer to top corner)
        # Solder lugs extend to X ~ 9.8mm
        {
            "dir": custom_fp_dir,
            "lib": "",
            "fp": "XT30PW-F_Lugs",
            "ref": "J_CHG1",
            "val": "XT30PW-F (CHG)",
            "x": 5.2,
            "y": 7.45,
            "rot": 0.0
        },
        # Bottom-Left: XT30 Male (BAT+ closer to bottom corner)
        # Male plug sits forward / lugs recessed to X ~ 7.8mm (shifted left by 1.5mm)
        {
            "dir": custom_fp_dir,
            "lib": "",
            "fp": "XT30PW-M_Lugs",
            "ref": "J_BAT1",
            "val": "XT30PW-M (BAT)",
            "x": 4.0,
            "y": 24.55,
            "rot": 0.0
        },

        # === 2. CURRENT SHUNTS & DISCONNECT MOSFETS ===
        # Shunt Resistor between XT30s (vertical)
        {
            "dir": kicad_fp_dir,
            "lib": "Resistor_SMD.pretty",
            "fp": "R_2512_6332Metric",
            "ref": "R_SH1",
            "val": "R001",
            "x": 10.6,
            "y": 16.0,
            "rot": 90.0
        },
        # 3 diodes/caps vertically next to R_SH1
        {
            "dir": kicad_fp_dir,
            "lib": "Resistor_SMD.pretty",
            "fp": "R_0603_1608Metric",
            "ref": "D_V1",
            "val": "0603",
            "x": 12.0,
            "y": 14.2,
            "rot": 90.0
        },
        {
            "dir": kicad_fp_dir,
            "lib": "Resistor_SMD.pretty",
            "fp": "R_0603_1608Metric",
            "ref": "D_V2",
            "val": "0603",
            "x": 12.0,
            "y": 16.0,
            "rot": 90.0
        },
        {
            "dir": kicad_fp_dir,
            "lib": "Resistor_SMD.pretty",
            "fp": "R_0603_1608Metric",
            "ref": "D_V3",
            "val": "0603",
            "x": 12.0,
            "y": 17.8,
            "rot": 90.0
        },
        # Ceramic Filter Capacitor 1206 (vertical)
        {
            "dir": kicad_fp_dir,
            "lib": "Capacitor_SMD.pretty",
            "fp": "C_1206_3216Metric",
            "ref": "C_FLT1",
            "val": "10uF_100V",
            "x": 13.8,
            "y": 16.0,
            "rot": 90.0
        },
        # TVS Diode / Component 1206 (vertical)
        {
            "dir": kicad_fp_dir,
            "lib": "Diode_SMD.pretty",
            "fp": "D_1206_3216Metric",
            "ref": "D_TVS1",
            "val": "TVS",
            "x": 15.6,
            "y": 16.0,
            "rot": 90.0
        },
        # Q1 Charge Disconnect MOSFET (AGM15T03LL / TOLL-8)
        # Drain tab facing TOP edge (close to top edge at Y = 6.4mm)
        # Shifted right to X = 22.0mm to clear XT30PW-F connector pins with >4.5mm clearance!
        {
            "dir": custom_fp_dir,
            "lib": "",
            "fp": "TOLL-8_AGM15T03LL",
            "ref": "Q1",
            "val": "AGM15T03LL",
            "x": 22.0,
            "y": 6.4,
            "rot": 0.0
        },
        # Shunt Resistor R001 between Q1 and Q2 (horizontal)
        # Centered horizontally right between Q1 and Q2 at X = 22.0mm
        {
            "dir": kicad_fp_dir,
            "lib": "Resistor_SMD.pretty",
            "fp": "R_2512_6332Metric",
            "ref": "R_SH2",
            "val": "R001",
            "x": 22.0,
            "y": 16.0,
            "rot": 0.0
        },
        # Capacitor C_DISC between Q1 and Q2 to the right of R001
        {
            "dir": kicad_fp_dir,
            "lib": "Capacitor_SMD.pretty",
            "fp": "C_1206_3216Metric",
            "ref": "C_DISC",
            "val": "10uF",
            "x": 26.8,
            "y": 16.0,
            "rot": 0.0
        },
        # Q2 Second Disconnect MOSFET (AGM15T03LL / TOLL-8)
        # 8 pins facing UP toward R001, Drain tab facing BOTTOM edge (close to bottom at Y = 25.6mm)
        # Vertically aligned with Q1 at X = 22.0mm!
        {
            "dir": custom_fp_dir,
            "lib": "",
            "fp": "TOLL-8_AGM15T03LL",
            "ref": "Q2",
            "val": "AGM15T03LL",
            "x": 22.0,
            "y": 25.6,
            "rot": 180.0
        },
        # Solid State Relay / Driver H2440
        # Positioned neatly to the right of Q1 with clean 3mm spacing
        {
            "dir": kicad_fp_dir,
            "lib": "Package_SO.pretty",
            "fp": "SOIC-8_3.9x4.9mm_P1.27mm",
            "ref": "U_SSR1",
            "val": "H2440_SSR",
            "x": 32.5,
            "y": 6.0,
            "rot": 0.0
        },

        # === 3. IC2: UPPER BQ7695202 (Cells 17-32) ===
        # Moved more toward center of board (X=48.5, Y=12.0)
        {
            "dir": kicad_fp_dir,
            "lib": "Package_QFP.pretty",
            "fp": "TQFP-48-1EP_7x7mm_P0.5mm_EP5x5mm_ThermalVias",
            "ref": "U_BQ2",
            "val": "BQ7695202 (IC2)",
            "x": 48.5,
            "y": 12.0,
            "rot": 0.0
        },

        # === 4. POWER SUPPLY STAGE (Buck + Boost) ===
        # Boost Converter SPV1040
        {
            "dir": kicad_fp_dir,
            "lib": "Package_SO.pretty",
            "fp": "TSSOP-8_4.4x3mm_P0.65mm",
            "ref": "U_BOOST1",
            "val": "SPV1040",
            "x": 58.5,
            "y": 5.5,
            "rot": 0.0
        },
        # Buck Converter TPS62130
        {
            "dir": kicad_fp_dir,
            "lib": "Package_DFN_QFN.pretty",
            "fp": "Texas_RTE_WQFN-16-1EP_3x3mm_P0.5mm_EP1.2x0.8mm_ThermalVias",
            "ref": "U_BUCK1",
            "val": "TPS62130",
            "x": 58.5,
            "y": 12.5,
            "rot": 0.0
        },
        # Main Inductor 181 (7.3x7.3mm shielded)
        {
            "dir": kicad_fp_dir,
            "lib": "Inductor_SMD.pretty",
            "fp": "L_7.3x7.3_H4.5",
            "ref": "L1",
            "val": "180uH_181",
            "x": 65.5,
            "y": 10.0,
            "rot": 0.0
        },
        # Tantalum Capacitor (100uF 16V, Case C 6032)
        {
            "dir": kicad_fp_dir,
            "lib": "Capacitor_Tantalum_SMD.pretty",
            "fp": "CP_EIA-6032-28_Kemet-C",
            "ref": "C_TAN1",
            "val": "100uF_16V",
            "x": 73.0,
            "y": 10.0,
            "rot": 90.0
        },

        # === 5. IC1: LOWER BQ7695202 (Cells 1-16) ===
        # Moved more toward center of board (X=83.5, Y=12.0)
        {
            "dir": kicad_fp_dir,
            "lib": "Package_QFP.pretty",
            "fp": "TQFP-48-1EP_7x7mm_P0.5mm_EP5x5mm_ThermalVias",
            "ref": "U_BQ1",
            "val": "BQ7695202 (IC1)",
            "x": 83.5,
            "y": 12.0,
            "rot": 0.0
        },

        # === 6. ESP32-C3-MINI-1 (Top-Right Area) ===
        {
            "dir": custom_fp_dir,
            "lib": "",
            "fp": "ESP32-C3-MINI-1",
            "ref": "U_ESP1",
            "val": "ESP32-C3-MINI-1",
            "x": 106.5,
            "y": 8.0,
            "rot": 0.0
        },

        # === 7. USB-C RECEPTACLE (Top Edge, Facing Outward/Upward) ===
        {
            "dir": custom_fp_dir,
            "lib": "",
            "fp": "USB_C_Receptacle_16P",
            "ref": "J_USB1",
            "val": "USB-C",
            "x": 125.0,
            "y": 3.2,
            "rot": 180.0
        },

        # === 8. USB-TO-UART BRIDGE (U7: CH340N, Right Edge Below USB-C) ===
        {
            "dir": kicad_fp_dir,
            "lib": "Package_SO.pretty",
            "fp": "SOIC-8_3.9x4.9mm_P1.27mm",
            "ref": "U7",
            "val": "CH340N",
            "x": 124.8,
            "y": 10.5,
            "rot": 0.0
        },

        # === 9. JST GH CONNECTORS ROW (Closer to bottom edge at Y = 22.5mm) ===
        # Connector 1: CAN & 5V (4-pin JST GH: CANH, CANL, ISO_G, 5V_ESC)
        {
            "dir": kicad_fp_dir,
            "lib": "Connector_JST.pretty",
            "fp": "JST_GH_BM04B-GHS-TBT_1x04-1MP_P1.25mm_Vertical",
            "ref": "J_COMM1",
            "val": "CAN/5V",
            "x": 33.0,
            "y": 22.5,
            "rot": 0.0
        },
        # Connector 2: CELLS 25-32 (6-pin JST GH)
        {
            "dir": kicad_fp_dir,
            "lib": "Connector_JST.pretty",
            "fp": "JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Vertical",
            "ref": "J_CELL4",
            "val": "25-32",
            "x": 43.5,
            "y": 22.5,
            "rot": 0.0
        },
        # Connector 3: CELLS 17-24 (8-pin JST GH)
        {
            "dir": kicad_fp_dir,
            "lib": "Connector_JST.pretty",
            "fp": "JST_GH_BM08B-GHS-TBT_1x08-1MP_P1.25mm_Vertical",
            "ref": "J_CELL3",
            "val": "17-24",
            "x": 56.5,
            "y": 22.5,
            "rot": 0.0
        },
        # Connector 4: CELLS 9-16 (9-pin JST GH)
        {
            "dir": kicad_fp_dir,
            "lib": "Connector_JST.pretty",
            "fp": "JST_GH_BM09B-GHS-TBT_1x09-1MP_P1.25mm_Vertical",
            "ref": "J_CELL2",
            "val": "9-16",
            "x": 71.5,
            "y": 22.5,
            "rot": 0.0
        },
        # Connector 5: CELLS 0-8 (10-pin JST GH)
        {
            "dir": kicad_fp_dir,
            "lib": "Connector_JST.pretty",
            "fp": "JST_GH_BM10B-GHS-TBT_1x10-1MP_P1.25mm_Vertical",
            "ref": "J_CELL1",
            "val": "0-8",
            "x": 88.0,
            "y": 22.5,
            "rot": 0.0
        },
        # Temperature Connectors T4, T3, T2, T1 (2-pin JST GH)
        {
            "dir": kicad_fp_dir,
            "lib": "Connector_JST.pretty",
            "fp": "JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical",
            "ref": "J_T4",
            "val": "T4",
            "x": 99.5,
            "y": 22.5,
            "rot": 0.0
        },
        {
            "dir": kicad_fp_dir,
            "lib": "Connector_JST.pretty",
            "fp": "JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical",
            "ref": "J_T3",
            "val": "T3",
            "x": 106.0,
            "y": 22.5,
            "rot": 0.0
        },
        {
            "dir": kicad_fp_dir,
            "lib": "Connector_JST.pretty",
            "fp": "JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical",
            "ref": "J_T2",
            "val": "T2",
            "x": 112.5,
            "y": 22.5,
            "rot": 0.0
        },
        {
            "dir": kicad_fp_dir,
            "lib": "Connector_JST.pretty",
            "fp": "JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical",
            "ref": "J_T1",
            "val": "T1",
            "x": 119.0,
            "y": 22.5,
            "rot": 0.0
        },
    ]

    # === 10. RESISTOR ROW: UPPER ROW BLEED RESISTORS (VERTICAL 90°) & BOTTOM ROW FILTER CAPS (HORIZONTAL 0°) ===
    res_x_start = 40.0
    res_pitch = 2.45
    for i in range(32):
        rx = res_x_start + i * res_pitch
        components.append({
            "dir": kicad_fp_dir,
            "lib": "Resistor_SMD.pretty",
            "fp": "R_0805_2012Metric",
            "ref": f"R_B{i+1}",
            "val": "27R0",
            "x": rx,
            "y": 26.8,
            "rot": 90.0
        })
        components.append({
            "dir": kicad_fp_dir,
            "lib": "Resistor_SMD.pretty",
            "fp": "R_0402_1005Metric",
            "ref": f"R_F{i+1}",
            "val": "100R",
            "x": rx,
            "y": 29.5,
            "rot": 0.0
        })

    # Load and place all footprints
    for item in components:
        if item["lib"]:
            lib_path = os.path.join(item["dir"], item["lib"])
        else:
            lib_path = item["dir"]
        fp = pcbnew.FootprintLoad(lib_path, item["fp"])
        if not fp:
            print(f"FAILED to load {item['lib']}/{item['fp']}")
            continue
        board.Add(fp)
        fp.SetReference(item["ref"])
        fp.SetValue(item["val"])
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(item["x"]), pcbnew.FromMM(item["y"])))
        fp.SetOrientation(pcbnew.EDA_ANGLE(item["rot"], pcbnew.DEGREES_T))
        
        # Hide reference labels for dense passives and JSTs to keep clean
        is_passive = item["ref"].startswith("R_B") or item["ref"].startswith("R_F") or item["ref"].startswith("C_B") or item["ref"].startswith("J_")
        fp.Reference().SetVisible(not is_passive)
        if not is_passive:
            fp.Reference().SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(0.65), pcbnew.FromMM(0.65)))
            fp.Reference().SetTextThickness(pcbnew.FromMM(0.12))
        fp.Value().SetVisible(False)

    # === DRAW SILKSCREEN XT30 CONNECTOR BODIES FOR CRISP 2D/3D VISUALIZATION ===
    # Top-Left XT30 (Female): Extends further right (X: 0.0 to 9.2mm, Y: 2.25 to 12.65mm)
    add_rect(0.0, 2.25, 9.2, 12.65, layer=pcbnew.F_SilkS, width=0.18)
    # Bottom-Left XT30 (Male): Recessed to the left (X: 0.0 to 7.5mm, Y: 19.35 to 29.75mm)
    add_rect(0.0, 19.35, 7.5, 29.75, layer=pcbnew.F_SilkS, width=0.18)

    # Draw ESP32-C3-MINI-1 Metal Shield outline & Antenna area
    # Module is 13.2mm (X) x 16.6mm (Y), center (106.5, 8.0)
    # Antenna: top 5.5mm (Y: -0.3 to 5.2), Shield: (Y: 5.2 to 16.3)
    add_rect(99.9, 0.2, 113.1, 4.5, layer=pcbnew.F_SilkS, width=0.18)
    add_rect(99.9, 4.5, 113.1, 15.5, layer=pcbnew.F_SilkS, width=0.2)
    add_text(pcbnew.F_SilkS, "ESPRESSIF", 106.5, 8.5, size=0.8, thickness=0.15)
    add_text(pcbnew.F_SilkS, "ESP32-C3-MINI-1", 106.5, 11.0, size=0.65, thickness=0.12)

    # === TOP SILKSCREEN LABELS ===
    # XT30 Corner markings matching real PCB
    add_text(pcbnew.F_SilkS, "CHG +", 10.0, 3.4, size=0.85, thickness=0.15)
    add_text(pcbnew.F_SilkS, "CHG -", 10.0, 11.5, size=0.85, thickness=0.15)
    add_text(pcbnew.F_SilkS, "BOT", 8.2, 20.3, size=0.85, thickness=0.15)
    add_text(pcbnew.F_SilkS, "TOP CELL", 8.2, 28.8, size=0.85, thickness=0.15)

    # U7 (CH340N USB-to-UART Bridge) label
    add_text(pcbnew.F_SilkS, "U7", 121.2, 10.5, size=0.75, thickness=0.13)

    # Right side markings matching physical board
    add_text(pcbnew.F_SilkS, "VBMS", 125.0, 26.5, size=0.8, thickness=0.14)
    add_text(pcbnew.F_SilkS, "Mini32", 125.0, 28.0, size=0.75, thickness=0.13)
    add_text(pcbnew.F_SilkS, "V1.0", 125.0, 29.5, size=0.7, thickness=0.12)
    add_text(pcbnew.F_SilkS, "EN", 128.5, 27.5, size=0.6, thickness=0.10, angle_deg=90.0)

    # === BOTTOM SILKSCREEN (VESC-X LOGO & INSTRUCTIONS) ===
    # Mirrored text for bottom layer
    add_text(pcbnew.B_SilkS, "VESC X", 65.0, 10.0, size=2.8, thickness=0.5, mirrored=True)
    add_text(pcbnew.B_SilkS, "Connect Top cell and bottom cell via power conn first", 65.0, 17.5, size=0.7, thickness=0.12, mirrored=True)
    add_text(pcbnew.B_SilkS, "Cell0- first. Work from lowest V to highest V.", 65.0, 19.3, size=0.7, thickness=0.12, mirrored=True)
    add_text(pcbnew.B_SilkS, "Connecting lower V cells to higher V pin likely to cause irreversible failure.", 65.0, 21.1, size=0.7, thickness=0.12, mirrored=True)

    add_text(pcbnew.B_SilkS, "CHG +", 15.0, 4.0, size=0.8, thickness=0.14, mirrored=True)
    add_text(pcbnew.B_SilkS, "CHG -", 15.0, 10.0, size=0.8, thickness=0.14, mirrored=True)
    add_text(pcbnew.B_SilkS, "BOT CELL", 15.0, 23.0, size=0.8, thickness=0.14, mirrored=True)
    add_text(pcbnew.B_SilkS, "TOP CELL", 15.0, 28.5, size=0.8, thickness=0.14, mirrored=True)

    add_text(pcbnew.B_SilkS, "5VExt GND CANL CANH", 33.0, 27.5, size=0.60, thickness=0.11, angle_deg=90.0, mirrored=True)
    add_text(pcbnew.B_SilkS, "25+ CELLS 32+", 44.5, 29.0, size=0.65, thickness=0.12, mirrored=True)
    add_text(pcbnew.B_SilkS, "17+ CELLS 24+", 59.0, 29.0, size=0.65, thickness=0.12, mirrored=True)
    add_text(pcbnew.B_SilkS, "9+ CELLS 16+", 74.5, 29.0, size=0.65, thickness=0.12, mirrored=True)
    add_text(pcbnew.B_SilkS, "0- CELLS 8+", 90.0, 29.0, size=0.65, thickness=0.12, mirrored=True)
    add_text(pcbnew.B_SilkS, "T4 GND", 101.0, 27.5, size=0.60, thickness=0.11, angle_deg=90.0, mirrored=True)
    add_text(pcbnew.B_SilkS, "T3 GND", 107.5, 27.5, size=0.60, thickness=0.11, angle_deg=90.0, mirrored=True)
    add_text(pcbnew.B_SilkS, "T2 GND", 114.0, 27.5, size=0.60, thickness=0.11, angle_deg=90.0, mirrored=True)
    add_text(pcbnew.B_SilkS, "T1 GND", 120.5, 27.5, size=0.60, thickness=0.11, angle_deg=90.0, mirrored=True)

    # Save board
    pcbnew.SaveBoard(pcb_path, board)
    print("Successfully built and saved board to:", pcb_path)

    # Render board with kicad-cli
    kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
    raw_top_png = os.path.join(project_dir, "VFBMS32_layout_top_hi_raw.png")

    print("Rendering raw top view...")
    subprocess.run([
        kicad_cli, "pcb", "render",
        "--side", "top",
        "--width", "3600", "--height", "1200",
        "--background", "transparent",
        "-o", raw_top_png, pcb_path
    ], check=False)

    # Autocrop transparent margins
    if os.path.exists(raw_top_png):
        im = Image.open(raw_top_png)
        bbox = im.getbbox()
        if bbox:
            pad = 30
            box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(im.width, bbox[2]+pad), min(im.height, bbox[3]+pad))
            im.crop(box).save(raw_top_png)
            print(f"Cropped {os.path.basename(raw_top_png)} to {im.size}")

if __name__ == "__main__":
    build_layout()
