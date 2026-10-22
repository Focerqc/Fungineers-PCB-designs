import os
import subprocess
from PIL import Image
import pcbnew

def build_v12_layout():
    project_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB"
    pcb_path = os.path.join(project_dir, "VFBMS32.kicad_pcb")
    kicad_fp_dir = r"C:\Program Files\KiCad\10.0\share\kicad\footprints"
    custom_fp_dir = os.path.join(project_dir, "vfbms.pretty")

    board = pcbnew.BOARD()

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

    def add_copper_fill(pts_mm, layer=pcbnew.F_Cu):
        s = pcbnew.PCB_SHAPE(board)
        s.SetShape(pcbnew.SHAPE_T_POLY)
        s.SetLayer(layer)
        s.SetFilled(True)
        poly = pcbnew.SHAPE_LINE_CHAIN()
        for x, y in pts_mm:
            poly.Append(pcbnew.FromMM(x), pcbnew.FromMM(y))
        poly.SetClosed(True)
        s.SetPolyShape(pcbnew.SHAPE_POLY_SET(poly))
        board.Add(s)
        return s

    def add_heavy_track(x1, y1, x2, y2, width_mm=3.0, layer=pcbnew.F_Cu):
        t = pcbnew.PCB_TRACK(board)
        t.SetLayer(layer)
        t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
        t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
        t.SetWidth(pcbnew.FromMM(width_mm))
        board.Add(t)
        return t

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

    # Footprints placement definition matching image_3023b2.png
    components = [
        # === 1. LOCKED XT30 POWER CONNECTORS ===
        # Top-Left: XT30 Female (CHG)
        {
            "dir": custom_fp_dir, "lib": "", "fp": "XT30PW-F_Lugs",
            "ref": "J_CHG1", "val": "XT30PW-F (CHG)",
            "x": 5.2, "y": 7.45, "rot": 0.0
        },
        # Bottom-Left: XT30 Male (BAT)
        {
            "dir": custom_fp_dir, "lib": "", "fp": "XT30PW-M_Lugs",
            "ref": "J_BAT1", "val": "XT30PW-M (BAT)",
            "x": 4.0, "y": 24.55, "rot": 0.0
        },

        # === 2. CURRENT SHUNTS, DISCONNECT MOSFETS & FUSE ===
        # Vertical R001 Current Shunt between XT30s
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_2512_6332Metric",
            "ref": "R_SH1", "val": "R001",
            "x": 10.6, "y": 16.0, "rot": 90.0
        },
        # Filter Capacitor 1206 next to vertical R001
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_1206_3216Metric",
            "ref": "C_FLT1", "val": "10uF_100V",
            "x": 8.2, "y": 16.0, "rot": 90.0
        },
        # 3 vertical 0603 diodes/caps to the left of C_FLT1
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "D_V1", "val": "0603", "x": 6.8, "y": 14.2, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "D_V2", "val": "0603", "x": 6.8, "y": 16.0, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "D_V3", "val": "0603", "x": 6.8, "y": 17.8, "rot": 90.0
        },
        # Shunt sense filter passives to the right of R_SH1
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_S1", "val": "100nF", "x": 13.2, "y": 14.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_S2", "val": "100nF", "x": 13.2, "y": 16.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Diode_SMD.pretty", "fp": "D_SOD-323",
            "ref": "D_S1", "val": "TVS", "x": 13.2, "y": 18.5, "rot": 0.0
        },

        # Top MOSFET Q1 (Charge Disconnect, Drain tab facing TOP edge)
        {
            "dir": custom_fp_dir, "lib": "", "fp": "TOLL-8_AGM15T03LL",
            "ref": "Q1", "val": "AGM15T03LL",
            "x": 18.5, "y": 6.4, "rot": 0.0
        },
        # Horizontal R001 Current Shunt (directly below Q1 8 pins)
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_2512_6332Metric",
            "ref": "R_SH2", "val": "R001",
            "x": 18.5, "y": 13.8, "rot": 0.0
        },
        # Disconnect Gate Driver / SSR U_GATE_DRV (SOIC-16 directly below horizontal R001)
        {
            "dir": kicad_fp_dir, "lib": "Package_SO.pretty", "fp": "SOIC-16_3.9x9.9mm_P1.27mm",
            "ref": "U_GATE_DRV", "val": "DISC_DRIVER",
            "x": 18.5, "y": 18.2, "rot": 90.0
        },
        # Fuse F1 ("JT 18A", 2512 SMD fuse next to male XT30)
        {
            "dir": kicad_fp_dir, "lib": "Fuse.pretty", "fp": "Fuse_2512_6332Metric",
            "ref": "F1", "val": "JT 18A",
            "x": 12.8, "y": 24.5, "rot": 90.0
        },
        # Bottom MOSFET Q2 (Discharge Disconnect, Drain tab facing BOTTOM edge)
        {
            "dir": custom_fp_dir, "lib": "", "fp": "TOLL-8_AGM15T03LL",
            "ref": "Q2", "val": "AGM15T03LL",
            "x": 19.8, "y": 25.6, "rot": 180.0
        },
        # Solid State Relay / Driver H2440 (SOIC-8 right of Q1)
        {
            "dir": kicad_fp_dir, "lib": "Package_SO.pretty", "fp": "SOIC-8_3.9x4.9mm_P1.27mm",
            "ref": "U_SSR1", "val": "H2440_SSR",
            "x": 30.5, "y": 6.0, "rot": 0.0
        },
        # Passives right of Q1
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_DRV1", "val": "10k", "x": 25.0, "y": 5.0, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_DRV1", "val": "100nF", "x": 25.0, "y": 7.0, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_DRV2", "val": "10k", "x": 27.0, "y": 5.0, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_DRV2", "val": "100nF", "x": 27.0, "y": 7.0, "rot": 90.0
        },
        # Snubber TVS / Capacitors
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_1206_3216Metric",
            "ref": "C_DISC", "val": "10uF", "x": 25.5, "y": 14.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Diode_SMD.pretty", "fp": "D_1206_3216Metric",
            "ref": "D_TVS1", "val": "TVS", "x": 25.5, "y": 17.5, "rot": 0.0
        },

        # === 3. IC2: UPPER BQ7695202 (Cells 17-32) ===
        {
            "dir": kicad_fp_dir, "lib": "Package_QFP.pretty", "fp": "TQFP-48-1EP_7x7mm_P0.5mm_EP5x5mm_ThermalVias",
            "ref": "U_BQ2", "val": "BQ7695202 (IC2)",
            "x": 47.0, "y": 13.5, "rot": 0.0
        },
        # IC2 Surrounding Passives (Left Column)
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_1", "val": "1uF", "x": 41.5, "y": 10.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_2", "val": "100nF", "x": 41.5, "y": 12.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_3", "val": "100nF", "x": 41.5, "y": 14.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_4", "val": "1uF", "x": 41.5, "y": 16.5, "rot": 90.0
        },
        # IC2 Top Passives
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_BQ2_1", "val": "10k", "x": 44.0, "y": 7.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_BQ2_2", "val": "10k", "x": 46.0, "y": 7.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_BQ2_3", "val": "10k", "x": 48.0, "y": 7.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_BQ2_4", "val": "10k", "x": 50.0, "y": 7.5, "rot": 0.0
        },
        # IC2 Right Column
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_5", "val": "100nF", "x": 52.5, "y": 11.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_6", "val": "100nF", "x": 52.5, "y": 13.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_7", "val": "100nF", "x": 52.5, "y": 15.5, "rot": 90.0
        },

        # === 4. POWER SUPPLY STAGE (Buck + Boost, Top Middle) ===
        # 10R0 Resistor 1206
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_1206_3216Metric",
            "ref": "R_PWR1", "val": "10R0", "x": 56.5, "y": 6.0, "rot": 90.0
        },
        # Ceramic Capacitor 1206
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_1206_3216Metric",
            "ref": "C_PWR1", "val": "10uF", "x": 59.0, "y": 6.0, "rot": 90.0
        },
        # Boost Converter SPV1040
        {
            "dir": kicad_fp_dir, "lib": "Package_SO.pretty", "fp": "TSSOP-8_4.4x3mm_P0.65mm",
            "ref": "U_BOOST1", "val": "SPV1040", "x": 62.5, "y": 6.0, "rot": 0.0
        },
        # Main Inductor 181 (7.3x7.3mm shielded marked "181")
        {
            "dir": kicad_fp_dir, "lib": "Inductor_SMD.pretty", "fp": "L_7.3x7.3_H4.5",
            "ref": "L1", "val": "180uH_181", "x": 67.5, "y": 7.5, "rot": 0.0
        },
        # Yellow Tantalum Capacitor (100uF 16V, Case C 6032 marked "▲ 107 C")
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_Tantalum_SMD.pretty", "fp": "CP_EIA-6032-28_Kemet-C",
            "ref": "C_TAN1", "val": "100uF_16V", "x": 74.5, "y": 7.5, "rot": 90.0
        },
        # Buck Converter TPS62130 (WQFN-16)
        {
            "dir": kicad_fp_dir, "lib": "Package_DFN_QFN.pretty", "fp": "Texas_RTE_WQFN-16-1EP_3x3mm_P0.5mm_EP1.2x0.8mm_ThermalVias",
            "ref": "U_BUCK1", "val": "TPS62130", "x": 67.5, "y": 14.5, "rot": 0.0
        },
        # Miniature Round Inductor L2
        {
            "dir": kicad_fp_dir, "lib": "Inductor_SMD.pretty", "fp": "L_6.3x6.3_H3",
            "ref": "L2", "val": "4.7uH", "x": 81.5, "y": 6.0, "rot": 0.0
        },
        # Power passives
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0805_2012Metric",
            "ref": "C_PWR2", "val": "22uF", "x": 62.5, "y": 14.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0805_2012Metric",
            "ref": "C_PWR3", "val": "22uF", "x": 72.5, "y": 14.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Diode_SMD.pretty", "fp": "D_0805_2012Metric",
            "ref": "D_PWR1", "val": "Schottky", "x": 74.5, "y": 14.5, "rot": 90.0
        },

        # === 5. IC1: LOWER BQ7695202 (Cells 1-16) ===
        {
            "dir": kicad_fp_dir, "lib": "Package_QFP.pretty", "fp": "TQFP-48-1EP_7x7mm_P0.5mm_EP5x5mm_ThermalVias",
            "ref": "U_BQ1", "val": "BQ7695202 (IC1)",
            "x": 88.0, "y": 13.5, "rot": 0.0
        },
        # IC1 Surrounding Passives (Left Column)
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ1_1", "val": "1uF", "x": 82.5, "y": 11.0, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ1_2", "val": "100nF", "x": 82.5, "y": 13.0, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ1_3", "val": "100nF", "x": 82.5, "y": 15.0, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ1_4", "val": "1uF", "x": 82.5, "y": 17.0, "rot": 90.0
        },
        # IC1 Top Passives
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_BQ1_1", "val": "10k", "x": 85.0, "y": 7.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_BQ1_2", "val": "10k", "x": 87.0, "y": 7.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_BQ1_3", "val": "10k", "x": 89.0, "y": 7.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_BQ1_4", "val": "10k", "x": 91.0, "y": 7.5, "rot": 0.0
        },
        # IC1 Right Column
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ1_5", "val": "100nF", "x": 93.5, "y": 11.0, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ1_6", "val": "100nF", "x": 93.5, "y": 13.0, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ1_7", "val": "100nF", "x": 93.5, "y": 15.0, "rot": 90.0
        },

        # === 6. ESP32-C3-MINI-1 (Top-Right Area) ===
        {
            "dir": custom_fp_dir, "lib": "", "fp": "ESP32-C3-MINI-1",
            "ref": "U_ESP1", "val": "ESP32-C3-MINI-1",
            "x": 106.5, "y": 8.5, "rot": 0.0
        },

        # === 7. USB-C RECEPTACLE (Top Edge, Facing Outward/Upward) ===
        {
            "dir": custom_fp_dir, "lib": "", "fp": "USB_C_Receptacle_16P",
            "ref": "J_USB1", "val": "USB-C",
            "x": 125.0, "y": 3.2, "rot": 180.0
        },

        # === 8. USB-TO-UART BRIDGE (U7: CH340N, Right Edge Below USB-C) ===
        {
            "dir": kicad_fp_dir, "lib": "Package_SO.pretty", "fp": "SOIC-8_3.9x4.9mm_P1.27mm",
            "ref": "U7", "val": "CH340N",
            "x": 124.8, "y": 12.0, "rot": 0.0
        },

        # === 9. JST GH CONNECTORS ROW (Y = 19.5mm) ===
        # Connector 1: CAN & 5V (4-pin JST GH: CANH, CANL, ISO_G, 5V_ESC)
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM04B-GHS-TBT_1x04-1MP_P1.25mm_Vertical",
            "ref": "J_COMM1", "val": "CAN/5V", "x": 32.5, "y": 19.5, "rot": 0.0
        },
        # Connector 2: CELLS 25-32 (6-pin JST GH)
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Vertical",
            "ref": "J_CELL4", "val": "25-32", "x": 43.5, "y": 19.5, "rot": 0.0
        },
        # Connector 3: CELLS 17-24 (8-pin JST GH)
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM08B-GHS-TBT_1x08-1MP_P1.25mm_Vertical",
            "ref": "J_CELL3", "val": "17-24", "x": 56.5, "y": 19.5, "rot": 0.0
        },
        # Connector 4: CELLS 9-16 (9-pin JST GH)
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM09B-GHS-TBT_1x09-1MP_P1.25mm_Vertical",
            "ref": "J_CELL2", "val": "9-16", "x": 71.5, "y": 19.5, "rot": 0.0
        },
        # Connector 5: CELLS 0-8 (9-pin JST GH)
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM09B-GHS-TBT_1x09-1MP_P1.25mm_Vertical",
            "ref": "J_CELL1", "val": "0-8", "x": 88.0, "y": 19.5, "rot": 0.0
        },
        # Connectors 6-9: Temperature Sensors T4, T3, T2, T1 (2-pin JST GH)
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical",
            "ref": "J_T4", "val": "T4", "x": 99.5, "y": 19.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical",
            "ref": "J_T3", "val": "T3", "x": 106.0, "y": 19.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical",
            "ref": "J_T2", "val": "T2", "x": 112.5, "y": 19.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical",
            "ref": "J_T1", "val": "T1", "x": 119.0, "y": 19.5, "rot": 0.0
        },
    ]

    # === 10. DENSE 32-CHANNEL BALANCE LADDER (HORIZONTAL ROW BELOW JSTs) ===
    # Upper row: R_B1 to R_B32 (0805 Resistors, Y = 25.5mm)
    # Lower row: R_F1 to R_F32 (0402 Capacitors, Y = 28.5mm)
    # Pitch = 2.45mm, running from X = 29.5mm to X ~ 105.5mm
    res_x_start = 29.5
    res_pitch = 2.45
    for i in range(32):
        rx = res_x_start + i * res_pitch
        components.append({
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0805_2012Metric",
            "ref": f"R_B{i+1}", "val": "27R0",
            "x": rx, "y": 25.5, "rot": 0.0
        })
        components.append({
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0402_1005Metric",
            "ref": f"R_F{i+1}", "val": "100nF",
            "x": rx, "y": 28.5, "rot": 0.0
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
        
        # Only show labels for primary ICs / connectors to keep silkscreen clean matching real board photo
        show_ref = item["ref"] in ["U7", "U_SSR1", "Q1", "Q2", "L1", "C_TAN1", "L2", "U_BOOST1", "U_BUCK1", "U_BQ1", "U_BQ2"]
        fp.Reference().SetVisible(show_ref)
        if show_ref:
            fp.Reference().SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(0.65), pcbnew.FromMM(0.65)))
            fp.Reference().SetTextThickness(pcbnew.FromMM(0.12))
        fp.Value().SetVisible(False)

    # === 11. MAP OUT HEAVY COPPER POURS (F.Cu and B.Cu) ===
    # 1. CHG+ Copper Pour: From J_CHG1 pin 1 lug (top) to Q1 Drain tab
    add_copper_fill([
        (4.0, 1.0),
        (24.5, 1.0),
        (24.5, 7.5),
        (13.0, 7.5),
        (13.0, 6.0),
        (4.0, 6.0)
    ], layer=pcbnew.F_Cu)

    add_copper_fill([
        (4.0, 1.0),
        (24.5, 1.0),
        (24.5, 7.5),
        (4.0, 7.5)
    ], layer=pcbnew.B_Cu)

    # Heavy copper tracks reinforcing CHG+ bus
    add_heavy_track(6.0, 5.0, 18.5, 5.0, width_mm=3.5, layer=pcbnew.F_Cu)
    add_heavy_track(6.0, 5.0, 18.5, 5.0, width_mm=3.5, layer=pcbnew.B_Cu)

    # 2. BAT+ / FUSE / Q2 Drain Copper Pour: From J_BAT1 pin 1 through F1 to Q2 Drain tab
    add_copper_fill([
        (3.5, 24.0),
        (11.0, 24.0),
        (11.0, 27.5),
        (3.5, 27.5)
    ], layer=pcbnew.F_Cu)

    add_copper_fill([
        (14.5, 24.5),
        (25.5, 24.5),
        (25.5, 31.0),
        (14.5, 31.0)
    ], layer=pcbnew.F_Cu)

    add_copper_fill([
        (3.5, 24.0),
        (25.5, 24.0),
        (25.5, 31.0),
        (3.5, 31.0)
    ], layer=pcbnew.B_Cu)

    # Heavy copper tracks reinforcing BAT+ bus
    add_heavy_track(5.0, 27.0, 11.5, 27.0, width_mm=3.5, layer=pcbnew.F_Cu)
    add_heavy_track(14.5, 27.0, 24.0, 27.0, width_mm=3.5, layer=pcbnew.F_Cu)
    add_heavy_track(5.0, 27.0, 24.0, 27.0, width_mm=3.5, layer=pcbnew.B_Cu)

    # 3. PACK Rail: Q1 Source through horizontal R_SH2 to Q2 Source
    add_copper_fill([
        (15.0, 8.5),
        (22.0, 8.5),
        (22.0, 13.0),
        (15.0, 13.0)
    ], layer=pcbnew.F_Cu)

    add_copper_fill([
        (15.0, 14.5),
        (22.0, 14.5),
        (22.0, 23.5),
        (15.0, 23.5)
    ], layer=pcbnew.F_Cu)

    add_heavy_track(18.5, 9.5, 18.5, 13.0, width_mm=4.0, layer=pcbnew.F_Cu)
    add_heavy_track(18.5, 14.5, 18.5, 23.0, width_mm=4.0, layer=pcbnew.F_Cu)

    # 4. Central GND Plane between XT30s around vertical R_SH1
    add_copper_fill([
        (3.5, 8.5),
        (13.5, 8.5),
        (13.5, 23.0),
        (3.5, 23.0)
    ], layer=pcbnew.F_Cu)

    add_copper_fill([
        (3.5, 8.5),
        (13.5, 8.5),
        (13.5, 23.0),
        (3.5, 23.0)
    ], layer=pcbnew.B_Cu)

    add_heavy_track(6.0, 10.0, 10.6, 13.0, width_mm=2.5, layer=pcbnew.F_Cu)
    add_heavy_track(5.0, 22.0, 10.6, 19.0, width_mm=2.5, layer=pcbnew.F_Cu)

    # === 12. DRAW SILKSCREEN XT30 BODIES & CRISP BOARD LABELS ===
    # Top-Left XT30 (Female): Extends to X: 9.2mm, Y: 2.25 to 12.65mm
    add_rect(0.0, 2.25, 9.2, 12.65, layer=pcbnew.F_SilkS, width=0.18)
    # Bottom-Left XT30 (Male): Extends to X: 7.5mm, Y: 19.35 to 29.75mm
    add_rect(0.0, 19.35, 7.5, 29.75, layer=pcbnew.F_SilkS, width=0.18)

    # Silkscreen labels matching VBMS Mini32 V1.2 photo
    add_text(pcbnew.F_SilkS, "+ HG", 7.5, 1.8, size=0.8, thickness=0.14)
    add_text(pcbnew.F_SilkS, "CHG -", 9.8, 12.5, size=0.75, thickness=0.13)
    add_text(pcbnew.F_SilkS, "BOT", 8.2, 20.3, size=0.8, thickness=0.14)
    add_text(pcbnew.F_SilkS, "TOP CELL", 8.2, 28.8, size=0.8, thickness=0.14)

    # U7 label
    add_text(pcbnew.F_SilkS, "U7", 121.2, 12.0, size=0.75, thickness=0.13)

    # VBMS Mini32 V1.2 silk label next to ESP32!
    add_text(pcbnew.F_SilkS, "VBMS", 97.0, 6.5, size=0.85, thickness=0.15, angle_deg=90.0)
    add_text(pcbnew.F_SilkS, "Mini32 V1.2", 98.5, 8.5, size=0.80, thickness=0.14, angle_deg=90.0)

    # Enable header label
    add_text(pcbnew.F_SilkS, "EN", 128.5, 27.5, size=0.6, thickness=0.10, angle_deg=90.0)
    add_rect(127.2, 25.5, 129.5, 29.5, layer=pcbnew.F_SilkS, width=0.15)

    # JST Connector Pinouts Silkscreen (CAN, ISO, 5V)
    add_text(pcbnew.F_SilkS, "CANH", 31.0, 23.2, size=0.55, thickness=0.10, angle_deg=90.0)
    add_text(pcbnew.F_SilkS, "CANL", 32.0, 23.2, size=0.55, thickness=0.10, angle_deg=90.0)
    add_text(pcbnew.F_SilkS, "ISO_G", 33.0, 23.2, size=0.55, thickness=0.10, angle_deg=90.0)
    add_text(pcbnew.F_SilkS, "5V_ESC", 34.0, 23.2, size=0.55, thickness=0.10, angle_deg=90.0)

    # === BOTTOM SILKSCREEN (VESC-X LOGO & INSTRUCTIONS) ===
    add_text(pcbnew.B_SilkS, "VESC X", 65.0, 10.0, size=2.8, thickness=0.5, mirrored=True)
    add_text(pcbnew.B_SilkS, "Connect Top cell and bottom cell via power conn first", 65.0, 17.5, size=0.7, thickness=0.12, mirrored=True)
    add_text(pcbnew.B_SilkS, "Cell0- first. Work from lowest V to highest V.", 65.0, 19.3, size=0.7, thickness=0.12, mirrored=True)
    add_text(pcbnew.B_SilkS, "Connecting lower V cells to higher V pin likely to cause irreversible failure.", 65.0, 21.1, size=0.7, thickness=0.12, mirrored=True)

    add_text(pcbnew.B_SilkS, "CHG +", 15.0, 4.0, size=0.8, thickness=0.14, mirrored=True)
    add_text(pcbnew.B_SilkS, "CHG -", 15.0, 10.0, size=0.8, thickness=0.14, mirrored=True)
    add_text(pcbnew.B_SilkS, "BOT CELL", 15.0, 23.0, size=0.8, thickness=0.14, mirrored=True)
    add_text(pcbnew.B_SilkS, "TOP CELL", 15.0, 28.5, size=0.8, thickness=0.14, mirrored=True)

    add_text(pcbnew.B_SilkS, "5VExt GND CANL CANH", 32.5, 27.5, size=0.60, thickness=0.11, angle_deg=90.0, mirrored=True)
    add_text(pcbnew.B_SilkS, "25+ CELLS 32+", 44.5, 29.0, size=0.65, thickness=0.12, mirrored=True)
    add_text(pcbnew.B_SilkS, "17+ CELLS 24+", 59.0, 29.0, size=0.65, thickness=0.12, mirrored=True)
    add_text(pcbnew.B_SilkS, "9+ CELLS 16+", 74.5, 29.0, size=0.65, thickness=0.12, mirrored=True)
    add_text(pcbnew.B_SilkS, "0- CELLS 8+", 90.0, 29.0, size=0.65, thickness=0.12, mirrored=True)
    add_text(pcbnew.B_SilkS, "T4 GND", 100.0, 27.5, size=0.60, thickness=0.11, angle_deg=90.0, mirrored=True)
    add_text(pcbnew.B_SilkS, "T3 GND", 106.5, 27.5, size=0.60, thickness=0.11, angle_deg=90.0, mirrored=True)
    add_text(pcbnew.B_SilkS, "T2 GND", 113.0, 27.5, size=0.60, thickness=0.11, angle_deg=90.0, mirrored=True)
    add_text(pcbnew.B_SilkS, "T1 GND", 119.5, 27.5, size=0.60, thickness=0.11, angle_deg=90.0, mirrored=True)

    # Save board
    pcbnew.SaveBoard(pcb_path, board)
    print("Successfully built and saved board to:", pcb_path)

    # Render fast draft 2D top-down render with kicad-cli
    kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
    draft_top_png = os.path.join(project_dir, "scratch", "vfbms32_draft_2d_top.png")
    brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\b988a972-63be-4423-9bf0-ac3c0e64f999"
    brain_draft_png = os.path.join(brain_dir, "vfbms32_draft_2d_top.png")

    print("Rendering fast draft 2D top-down view...")
    subprocess.run([
        kicad_cli, "pcb", "render",
        "--side", "top",
        "--width", "3200", "--height", "1000",
        "--background", "transparent",
        "-o", draft_top_png, pcb_path
    ], check=True)

    # Autocrop transparent margins
    if os.path.exists(draft_top_png):
        im = Image.open(draft_top_png)
        bbox = im.getbbox()
        if bbox:
            pad = 20
            box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(im.width, bbox[2]+pad), min(im.height, bbox[3]+pad))
            im.crop(box).save(draft_top_png)
            print(f"Saved draft 2D render: {draft_top_png}, size={im.size}")
            import shutil
            shutil.copyfile(draft_top_png, brain_draft_png)
            print(f"Copied to brain: {brain_draft_png}")

if __name__ == "__main__":
    build_v12_layout()
