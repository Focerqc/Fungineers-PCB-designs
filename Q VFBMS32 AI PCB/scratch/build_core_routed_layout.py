import os
import subprocess
from PIL import Image
import pcbnew

def build_core_routed_layout():
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

    def add_track(x1, y1, x2, y2, width_mm=0.25, layer=pcbnew.F_Cu):
        t = pcbnew.PCB_TRACK(board)
        t.SetLayer(layer)
        t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
        t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
        t.SetWidth(pcbnew.FromMM(width_mm))
        board.Add(t)
        return t

    def add_via(x, y, size_mm=0.6, drill_mm=0.3):
        v = pcbnew.PCB_VIA(board)
        v.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        v.SetWidth(pcbnew.FromMM(size_mm))
        v.SetDrill(pcbnew.FromMM(drill_mm))
        board.Add(v)
        return v

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

    components = [
        # === 1. PRESERVED LOCKED XT30 CONNECTORS ===
        {
            "dir": custom_fp_dir, "lib": "", "fp": "XT30PW-F_Lugs",
            "ref": "J_CHG1", "val": "XT30PW-F (CHG)",
            "x": 5.2, "y": 7.45, "rot": 0.0
        },
        {
            "dir": custom_fp_dir, "lib": "", "fp": "XT30PW-M_Lugs",
            "ref": "J_BAT1", "val": "XT30PW-M (BAT)",
            "x": 4.0, "y": 24.55, "rot": 0.0
        },

        # === 2. POWER STAGE & DISCONNECT (ZERO GATE DRIVER COLLISION) ===
        # Vertical R001 Current Shunt
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_2512_6332Metric",
            "ref": "R_SH1", "val": "R001",
            "x": 10.6, "y": 16.0, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_1206_3216Metric",
            "ref": "C_FLT1", "val": "10uF_100V",
            "x": 8.2, "y": 16.0, "rot": 90.0
        },
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

        # Top MOSFET Q1 (Charge Disconnect) - Drain facing top
        {
            "dir": custom_fp_dir, "lib": "", "fp": "TOLL-8_AGM15T03LL",
            "ref": "Q1", "val": "AGM15T03LL",
            "x": 18.5, "y": 6.4, "rot": 0.0
        },
        # Horizontal R001 Current Shunt (sits cleanly between Q1 and Q2)
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_2512_6332Metric",
            "ref": "R_SH2", "val": "R001",
            "x": 18.5, "y": 13.8, "rot": 0.0
        },
        # Fuse F1 ("JT 18A")
        {
            "dir": kicad_fp_dir, "lib": "Fuse.pretty", "fp": "Fuse_2512_6332Metric",
            "ref": "F1", "val": "JT 18A",
            "x": 12.8, "y": 24.5, "rot": 90.0
        },
        # Bottom MOSFET Q2 (Discharge Disconnect) - Drain facing bottom edge
        {
            "dir": custom_fp_dir, "lib": "", "fp": "TOLL-8_AGM15T03LL",
            "ref": "Q2", "val": "AGM15T03LL",
            "x": 19.8, "y": 25.6, "rot": 180.0
        },

        # Solid State Relay / Driver U_SSR1 (SOIC-8 right of Q1, exactly as in master photo)
        {
            "dir": kicad_fp_dir, "lib": "Package_SO.pretty", "fp": "SOIC-8_3.9x4.9mm_P1.27mm",
            "ref": "U_SSR1", "val": "H2440_SSR",
            "x": 27.2, "y": 5.8, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_DRV1", "val": "10k", "x": 23.6, "y": 4.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_DRV1", "val": "100nF", "x": 23.6, "y": 6.8, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_DRV2", "val": "10k", "x": 30.5, "y": 3.8, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_DRV2", "val": "100nF", "x": 30.5, "y": 5.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_1206_3216Metric",
            "ref": "C_DISC", "val": "10uF", "x": 25.2, "y": 12.0, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Diode_SMD.pretty", "fp": "D_SOD-123",
            "ref": "D_TVS1", "val": "TVS", "x": 28.0, "y": 10.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_DRV3", "val": "1k", "x": 28.0, "y": 12.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Diode_SMD.pretty", "fp": "D_SOD-123",
            "ref": "D_SEC1", "val": "D_Schottky", "x": 25.8, "y": 17.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Diode_SMD.pretty", "fp": "D_SOD-123",
            "ref": "D_SEC2", "val": "D_Schottky", "x": 28.2, "y": 17.5, "rot": 90.0
        },

        # === 3. IC2 CLUSTER: UPPER BQ7695202 (Cells 17-32) ===
        {
            "dir": kicad_fp_dir, "lib": "Package_QFP.pretty", "fp": "TQFP-48-1EP_7x7mm_P0.5mm_EP5x5mm_ThermalVias",
            "ref": "U_BQ2", "val": "BQ7695202 (IC2)",
            "x": 48.0, "y": 13.5, "rot": 0.0
        },
        # Left: Vertical filter caps stack
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_FLT1", "val": "100nF", "x": 41.5, "y": 9.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_FLT2", "val": "100nF", "x": 41.5, "y": 11.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_FLT3", "val": "100nF", "x": 41.5, "y": 13.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_FLT4", "val": "100nF", "x": 41.5, "y": 15.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_FLT5", "val": "100nF", "x": 41.5, "y": 17.5, "rot": 90.0
        },
        # Top: Pull-up resistors and decoupling
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_BQ2_PU1", "val": "4k7", "x": 44.5, "y": 7.2, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_BQ2_PU2", "val": "4k7", "x": 46.8, "y": 7.2, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_BQ2_PU3", "val": "10k", "x": 49.1, "y": 7.2, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_BAT", "val": "100nF", "x": 51.4, "y": 7.2, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_CP1", "val": "100nF", "x": 44.5, "y": 5.2, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_BQ2_PU4", "val": "10k", "x": 46.8, "y": 5.2, "rot": 0.0
        },
        # Right: Bypass capacitors for LDOs (REG1, REG2, REG18, VDD)
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_REG1", "val": "2.2uF", "x": 54.5, "y": 9.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_REG2", "val": "2.2uF", "x": 54.5, "y": 11.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_REG18", "val": "2.2uF", "x": 54.5, "y": 13.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ2_VDD", "val": "100nF", "x": 54.5, "y": 15.5, "rot": 90.0
        },

        # === 4. POWER DELIVERY STAGE (Top Middle: Boost, Buck, L1 Inductor, C_TAN1) ===
        # Resistor and input ceramic cap left of Boost
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_1206_3216Metric",
            "ref": "R_PWR1", "val": "10R0", "x": 57.2, "y": 5.2, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_1206_3216Metric",
            "ref": "C_PWR1", "val": "10uF", "x": 59.8, "y": 5.2, "rot": 90.0
        },
        # SPV1040 Boost Converter
        {
            "dir": kicad_fp_dir, "lib": "Package_SO.pretty", "fp": "TSSOP-8_4.4x3mm_P0.65mm",
            "ref": "U_BOOST1", "val": "SPV1040", "x": 63.5, "y": 5.2, "rot": 0.0
        },
        # Boost Diode
        {
            "dir": kicad_fp_dir, "lib": "Diode_SMD.pretty", "fp": "D_SOD-123",
            "ref": "D_BST1", "val": "Schottky", "x": 66.8, "y": 5.2, "rot": 90.0
        },
        # HEAVY SHIELDED POWER INDUCTOR L1 (7.3x7.3 mm, marked "181")
        {
            "dir": kicad_fp_dir, "lib": "Inductor_SMD.pretty", "fp": "L_7.3x7.3_H4.5",
            "ref": "L1", "val": "180uH_181", "x": 72.0, "y": 6.8, "rot": 0.0
        },
        # YELLOW TANTALUM CAPACITOR C_TAN1 (Case C 6032, marked "107 C")
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_Tantalum_SMD.pretty", "fp": "CP_EIA-6032-28_Kemet-C",
            "ref": "C_TAN1", "val": "100uF_16V", "x": 78.5, "y": 6.8, "rot": 90.0
        },
        # TPS62130 Buck Converter (WQFN-16)
        {
            "dir": kicad_fp_dir, "lib": "Package_DFN_QFN.pretty", "fp": "Texas_RTE_WQFN-16-1EP_3x3mm_P0.5mm_EP1.2x0.8mm_ThermalVias",
            "ref": "U_BUCK1", "val": "TPS62130", "x": 68.0, "y": 14.5, "rot": 0.0
        },
        # Buck Passives (Inputs, Outputs, Diode, Feedback)
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0805_2012Metric",
            "ref": "C_PWR2", "val": "22uF", "x": 63.5, "y": 14.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0805_2012Metric",
            "ref": "C_PWR3", "val": "22uF", "x": 72.5, "y": 14.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Diode_SMD.pretty", "fp": "D_SOD-123",
            "ref": "D_PWR1", "val": "Schottky", "x": 75.0, "y": 14.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_BK_FB1", "val": "100k", "x": 64.5, "y": 11.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_BK_FB2", "val": "22k", "x": 71.5, "y": 11.5, "rot": 0.0
        },
        # Miniature Round Power Choke L2 directly above U_BQ1
        {
            "dir": kicad_fp_dir, "lib": "Inductor_SMD.pretty", "fp": "L_6.3x6.3_H3",
            "ref": "L2", "val": "4.7uH", "x": 86.5, "y": 4.5, "rot": 0.0
        },

        # === 5. IC1 CLUSTER: LOWER BQ7695202 (Cells 1-16) ===
        {
            "dir": kicad_fp_dir, "lib": "Package_QFP.pretty", "fp": "TQFP-48-1EP_7x7mm_P0.5mm_EP5x5mm_ThermalVias",
            "ref": "U_BQ1", "val": "BQ7695202 (IC1)",
            "x": 89.5, "y": 13.5, "rot": 0.0
        },
        # Left: Vertical filter caps stack
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ1_FLT1", "val": "100nF", "x": 83.0, "y": 9.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ1_FLT2", "val": "100nF", "x": 83.0, "y": 11.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ1_FLT3", "val": "100nF", "x": 83.0, "y": 13.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ1_FLT4", "val": "100nF", "x": 83.0, "y": 15.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ1_FLT5", "val": "100nF", "x": 83.0, "y": 17.5, "rot": 90.0
        },
        # Top: Pull-up resistors and decoupling
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_BQ1_PU1", "val": "4k7", "x": 87.0, "y": 8.0, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_BQ1_PU2", "val": "4k7", "x": 89.2, "y": 8.0, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0603_1608Metric",
            "ref": "R_BQ1_PU3", "val": "10k", "x": 91.4, "y": 8.0, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ1_BAT", "val": "100nF", "x": 93.6, "y": 8.0, "rot": 0.0
        },
        # Right: Bypass capacitors for LDOs (REG1, REG2, REG18, VDD)
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ1_REG1", "val": "2.2uF", "x": 96.0, "y": 9.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ1_REG2", "val": "2.2uF", "x": 96.0, "y": 11.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ1_REG18", "val": "2.2uF", "x": 96.0, "y": 13.5, "rot": 90.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Capacitor_SMD.pretty", "fp": "C_0603_1608Metric",
            "ref": "C_BQ1_VDD", "val": "100nF", "x": 96.0, "y": 15.5, "rot": 90.0
        },

        # === 6. PRESERVED ESP32-C3-MINI-1 ===
        {
            "dir": custom_fp_dir, "lib": "", "fp": "ESP32-C3-MINI-1",
            "ref": "U_ESP1", "val": "ESP32-C3-MINI-1",
            "x": 106.5, "y": 8.5, "rot": 0.0
        },

        # === 7. PRESERVED USB-C RECEPTACLE ===
        {
            "dir": custom_fp_dir, "lib": "", "fp": "USB_C_Receptacle_16P",
            "ref": "J_USB1", "val": "USB-C",
            "x": 125.0, "y": 3.2, "rot": 180.0
        },

        # === 8. PRESERVED USB-TO-UART BRIDGE U7 (CH340N) ===
        {
            "dir": kicad_fp_dir, "lib": "Package_SO.pretty", "fp": "SOIC-8_3.9x4.9mm_P1.27mm",
            "ref": "U7", "val": "CH340N",
            "x": 124.8, "y": 12.0, "rot": 0.0
        },

        # === 9. FULLY LOCKED ORIGINAL JST GH CONNECTORS (Y = 22.5mm) ===
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM04B-GHS-TBT_1x04-1MP_P1.25mm_Vertical",
            "ref": "J_COMM1", "val": "CAN/5V", "x": 33.0, "y": 22.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Vertical",
            "ref": "J_CELL4", "val": "25-32", "x": 43.5, "y": 22.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM08B-GHS-TBT_1x08-1MP_P1.25mm_Vertical",
            "ref": "J_CELL3", "val": "17-24", "x": 56.5, "y": 22.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM09B-GHS-TBT_1x09-1MP_P1.25mm_Vertical",
            "ref": "J_CELL2", "val": "9-16", "x": 71.5, "y": 22.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM10B-GHS-TBT_1x10-1MP_P1.25mm_Vertical",
            "ref": "J_CELL1", "val": "0-8", "x": 88.0, "y": 22.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical",
            "ref": "J_T4", "val": "T4", "x": 99.5, "y": 22.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical",
            "ref": "J_T3", "val": "T3", "x": 106.0, "y": 22.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical",
            "ref": "J_T2", "val": "T2", "x": 112.5, "y": 22.5, "rot": 0.0
        },
        {
            "dir": kicad_fp_dir, "lib": "Connector_JST.pretty", "fp": "JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical",
            "ref": "J_T1", "val": "T1", "x": 119.0, "y": 22.5, "rot": 0.0
        },
    ]

    # === 10. FULLY LOCKED ORIGINAL PASSIVE ROWS (BENEATH JSTs) ===
    res_x_start = 40.0
    res_pitch = 2.45
    for i in range(32):
        rx = res_x_start + i * res_pitch
        components.append({
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0805_2012Metric",
            "ref": f"R_B{i+1}", "val": "27R0",
            "x": rx, "y": 26.8, "rot": 90.0
        })
        components.append({
            "dir": kicad_fp_dir, "lib": "Resistor_SMD.pretty", "fp": "R_0402_1005Metric",
            "ref": f"R_F{i+1}", "val": "100R",
            "x": rx, "y": 29.5, "rot": 0.0
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
        
        # Silkscreen visibility
        show_ref = item["ref"] in ["U7", "U_SSR1", "Q1", "Q2", "L1", "C_TAN1", "L2", "U_BOOST1", "U_BUCK1", "U_BQ1", "U_BQ2"]
        fp.Reference().SetVisible(show_ref)
        if show_ref:
            fp.Reference().SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(0.65), pcbnew.FromMM(0.65)))
            fp.Reference().SetTextThickness(pcbnew.FromMM(0.12))
        fp.Value().SetVisible(False)

    # === 11. POWER COPPER POURS ===
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

    add_track(6.0, 5.0, 18.5, 5.0, width_mm=3.5, layer=pcbnew.F_Cu)
    add_track(6.0, 5.0, 18.5, 5.0, width_mm=3.5, layer=pcbnew.B_Cu)

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

    add_track(5.0, 27.0, 11.5, 27.0, width_mm=3.5, layer=pcbnew.F_Cu)
    add_track(14.5, 27.0, 24.0, 27.0, width_mm=3.5, layer=pcbnew.F_Cu)
    add_track(5.0, 27.0, 24.0, 27.0, width_mm=3.5, layer=pcbnew.B_Cu)

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

    add_track(18.5, 9.5, 18.5, 13.0, width_mm=4.0, layer=pcbnew.F_Cu)
    add_track(18.5, 14.5, 18.5, 23.0, width_mm=4.0, layer=pcbnew.F_Cu)

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

    add_track(6.0, 10.0, 10.6, 13.0, width_mm=2.5, layer=pcbnew.F_Cu)
    add_track(5.0, 22.0, 10.6, 19.0, width_mm=2.5, layer=pcbnew.F_Cu)

    # === 12. CORE ROUTING EXECUTION: BQ CLUSTERS & POWER STAGE ===
    # A. U_BQ2 Cluster Routing (Upper 16S)
    flt_y_coords = [9.5, 11.5, 13.5, 15.5, 17.5]
    for fy in flt_y_coords:
        add_track(42.5, fy, 43.5, fy, width_mm=0.25)
        add_track(40.5, fy, 40.5, fy + 1.0, width_mm=0.25)
    add_track(40.5, 9.5, 40.5, 18.5, width_mm=0.3)
    add_via(40.5, 18.5)

    add_track(44.5, 8.0, 44.5, 9.0, width_mm=0.25)
    add_track(46.8, 8.0, 46.8, 9.0, width_mm=0.25)
    add_track(49.1, 8.0, 49.1, 9.0, width_mm=0.25)
    add_track(51.4, 8.0, 51.4, 9.0, width_mm=0.25)
    add_track(43.5, 6.4, 50.0, 6.4, width_mm=0.3)

    reg_y_coords = [9.5, 11.5, 13.5, 15.5]
    for ry in reg_y_coords:
        add_track(52.5, ry, 53.5, ry, width_mm=0.25)
        add_track(55.5, ry, 56.5, ry, width_mm=0.3)
        add_via(56.5, ry)

    # B. U_BQ1 Cluster Routing (Lower 16S)
    for fy in flt_y_coords:
        add_track(84.0, fy, 85.0, fy, width_mm=0.25)
        add_track(82.0, fy, 82.0, fy + 1.0, width_mm=0.25)
    add_track(82.0, 9.5, 82.0, 18.5, width_mm=0.3)
    add_via(82.0, 18.5)

    add_track(87.0, 8.8, 87.0, 9.0, width_mm=0.25)
    add_track(89.2, 8.8, 89.2, 9.0, width_mm=0.25)
    add_track(91.4, 8.8, 91.4, 9.0, width_mm=0.25)
    add_track(93.6, 8.8, 93.6, 9.0, width_mm=0.25)
    add_track(86.0, 7.2, 92.5, 7.2, width_mm=0.3)

    for ry in reg_y_coords:
        add_track(94.0, ry, 95.0, ry, width_mm=0.25)
        add_track(97.0, ry, 98.0, ry, width_mm=0.3)
        add_via(98.0, ry)

    # C. Power Delivery Routing (Top Middle: U_BOOST1, L1, C_TAN1, U_BUCK1)
    # 1. Boost converter input from R_PWR1 -> C_PWR1 -> U_BOOST1
    add_track(57.2, 3.8, 59.8, 3.8, width_mm=0.6)
    add_track(59.8, 3.8, 62.0, 3.8, width_mm=0.6)
    # 2. Boost switch node to L1 inductor
    add_track(63.5, 6.4, 66.8, 6.4, width_mm=0.8)
    add_track(66.8, 6.4, 68.5, 6.4, width_mm=0.8)
    # 3. L1 inductor output to C_TAN1 yellow tantalum capacitor
    add_track(75.5, 6.8, 77.0, 6.8, width_mm=1.0)
    # 4. Heavy rail from C_TAN1 to U_BUCK1 (TPS62130) VIN
    add_track(78.5, 8.5, 78.5, 12.5, width_mm=0.8)
    add_track(78.5, 12.5, 69.5, 12.5, width_mm=0.8)
    add_track(69.5, 12.5, 69.5, 13.5, width_mm=0.8)
    # 5. Buck input capacitor C_PWR2 to U_BUCK1
    add_track(63.5, 13.2, 66.5, 13.2, width_mm=0.6)
    # 6. Buck switch node to output capacitor C_PWR3
    add_track(69.5, 15.5, 72.5, 15.5, width_mm=0.8)
    # 7. Buck feedback traces
    add_track(64.5, 12.2, 66.5, 13.5, width_mm=0.25)
    add_track(71.5, 12.2, 69.5, 13.5, width_mm=0.25)
    # 8. L2 round choke connections
    add_track(83.5, 4.5, 86.5, 4.5, width_mm=0.6)
    add_track(86.5, 4.5, 89.5, 4.5, width_mm=0.6)

    # D. Locked Balance Ladder Interconnects (Beneath JSTs)
    for i in range(32):
        rx = res_x_start + i * res_pitch
        add_track(rx, 27.8, rx, 28.8, width_mm=0.25)

    # === 13. SILKSCREEN LABELS & XT30 BODIES ===
    add_rect(0.0, 2.25, 9.2, 12.65, layer=pcbnew.F_SilkS, width=0.18)
    add_rect(0.0, 19.35, 7.5, 29.75, layer=pcbnew.F_SilkS, width=0.18)

    add_text(pcbnew.F_SilkS, "+ HG", 7.5, 1.8, size=0.8, thickness=0.14)
    add_text(pcbnew.F_SilkS, "CHG -", 9.8, 12.5, size=0.75, thickness=0.13)
    add_text(pcbnew.F_SilkS, "BOT", 8.2, 20.3, size=0.8, thickness=0.14)
    add_text(pcbnew.F_SilkS, "TOP CELL", 8.2, 28.8, size=0.8, thickness=0.14)

    add_text(pcbnew.F_SilkS, "U7", 121.2, 12.0, size=0.75, thickness=0.13)
    add_text(pcbnew.F_SilkS, "VBMS", 99.5, 6.5, size=0.85, thickness=0.15, angle_deg=90.0)
    add_text(pcbnew.F_SilkS, "Mini32 V1.2", 101.0, 8.5, size=0.80, thickness=0.14, angle_deg=90.0)

    add_text(pcbnew.F_SilkS, "EN", 128.5, 27.5, size=0.6, thickness=0.10, angle_deg=90.0)
    add_rect(127.2, 25.5, 129.5, 29.5, layer=pcbnew.F_SilkS, width=0.15)

    # Bottom silkscreen
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
    add_text(pcbnew.B_SilkS, "T4 GND", 100.0, 27.5, size=0.60, thickness=0.11, angle_deg=90.0, mirrored=True)
    add_text(pcbnew.B_SilkS, "T3 GND", 106.5, 27.5, size=0.60, thickness=0.11, angle_deg=90.0, mirrored=True)
    add_text(pcbnew.B_SilkS, "T2 GND", 113.0, 27.5, size=0.60, thickness=0.11, angle_deg=90.0, mirrored=True)
    add_text(pcbnew.B_SilkS, "T1 GND", 119.5, 27.5, size=0.60, thickness=0.11, angle_deg=90.0, mirrored=True)

    # Save board
    pcbnew.SaveBoard(pcb_path, board)
    print("Successfully built and saved core routed board to:", pcb_path)

    # Render full 2D top view
    kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
    full_top_png = os.path.join(project_dir, "scratch", "vfbms32_full_top.png")
    brain_dir = r"C:\Users\quinn\.gemini\antigravity-ide\brain\da94429c-ba52-43c3-a118-fc16f71395ae"
    os.makedirs(brain_dir, exist_ok=True)
    brain_full_top = os.path.join(brain_dir, "vfbms32_full_top.png")

    print("Rendering high-res 2D top view with kicad-cli...")
    subprocess.run([
        kicad_cli, "pcb", "render",
        "--side", "top",
        "--width", "3600", "--height", "1200",
        "--background", "transparent",
        "-o", full_top_png, pcb_path
    ], check=True)

    if os.path.exists(full_top_png):
        im = Image.open(full_top_png)
        bbox = im.getbbox()
        if bbox:
            pad = 20
            box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(im.width, bbox[2]+pad), min(im.height, bbox[3]+pad))
            cropped_full = im.crop(box)
            cropped_full.save(full_top_png)
            import shutil
            shutil.copyfile(full_top_png, brain_full_top)
            print(f"Saved full top render: {full_top_png} -> {brain_full_top}")

            # Also create zoomed render of the Power Delivery + BQ Clusters
            cb_w = cropped_full.width
            cb_h = cropped_full.height
            core_zoom_box = (
                int(cb_w * 0.12),
                0,
                int(cb_w * 0.80),
                int(cb_h * 0.85)
            )
            core_zoom = cropped_full.crop(core_zoom_box)
            core_zoom_path = os.path.join(project_dir, "scratch", "vfbms32_core_routed_zoom.png")
            brain_core_zoom = os.path.join(brain_dir, "vfbms32_core_routed_zoom.png")
            core_zoom.save(core_zoom_path)
            shutil.copyfile(core_zoom_path, brain_core_zoom)
            print(f"Saved core zoom render: {core_zoom_path}")

            # Also create power stage zoom to verify ZERO collision
            power_zoom_box = (
                0,
                0,
                int(cb_w * 0.35),
                cb_h
            )
            pwr_zoom = cropped_full.crop(power_zoom_box)
            pwr_zoom_path = os.path.join(project_dir, "scratch", "vfbms32_power_stage_verified.png")
            brain_pwr_zoom = os.path.join(brain_dir, "vfbms32_power_stage_verified.png")
            pwr_zoom.save(pwr_zoom_path)
            shutil.copyfile(pwr_zoom_path, brain_pwr_zoom)
            print(f"Saved power stage verification render: {pwr_zoom_path}")

if __name__ == "__main__":
    build_core_routed_layout()
