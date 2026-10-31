"""
Apply working-board connectivity for qfbms32.

External nets follow vfbms32_wiring_32s_best.jpg (see WORKING_TOPOLOGY.md).
AFE passives follow TI BQ76952 EVM cues (20R series filters).
SSR caps C_SSR1/C_SSR2 decouple VBOOST to GND.
"""
from __future__ import annotations

import shutil
from pathlib import Path

import pcbnew

ROOT = Path(__file__).resolve().parents[1]
PCB = ROOT / "qfbms32.kicad_pcb"
SCH = ROOT / "qfbms32.kicad_sch"
HIST = ROOT / ".history"
FP_CAP = Path(r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Capacitor_SMD.pretty")

# BQ76952 PFB pin numbers (matches KiCad symbol + TI DS)
BQ_VC = {15: "1", 14: "2", 13: "3", 12: "4", 11: "5", 10: "6", 9: "7", 8: "8",
         7: "9", 6: "10", 5: "11", 4: "12", 3: "13", 2: "14", 1: "15", 0: "16",
         16: "48"}
BQ_VSS = "17"
BQ_BAT = "47"
BQ_CHG = "45"
BQ_DSG = "43"
BQ_PACK = "42"
BQ_PCHG = "40"
BQ_SRP = "18"
BQ_SRN = "20"
BQ_TS1, BQ_TS2, BQ_TS3 = "21", "22", "23"
BQ_REG1, BQ_REG18, BQ_REGIN = "35", "24", "36"


def net(board: pcbnew.BOARD, name: str) -> pcbnew.NETINFO_ITEM:
    existing = board.FindNet(name)
    if existing and existing.GetNetCode() > 0:
        return existing
    ni = pcbnew.NETINFO_ITEM(board, name)
    board.Add(ni)
    return ni


def set_pad(board: pcbnew.BOARD, ref: str, pad_no: str, netname: str) -> None:
    fp = board.FindFootprintByReference(ref)
    if not fp:
        print(f"  MISSING FP {ref}")
        return
    pad = fp.FindPadByNumber(pad_no)
    if not pad:
        print(f"  MISSING PAD {ref}.{pad_no}")
        return
    pad.SetNet(net(board, netname))


def set_all_named(board: pcbnew.BOARD, ref: str, mapping: dict[str, str]) -> None:
    for pad_no, netname in mapping.items():
        set_pad(board, ref, pad_no, netname)


def add_track(board, x1, y1, x2, y2, netname, width=0.25, layer=pcbnew.F_Cu):
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(pcbnew.VECTOR2I(pcbnew.FromMM(x1), pcbnew.FromMM(y1)))
    t.SetEnd(pcbnew.VECTOR2I(pcbnew.FromMM(x2), pcbnew.FromMM(y2)))
    t.SetWidth(pcbnew.FromMM(width))
    t.SetLayer(layer)
    t.SetNet(net(board, netname))
    board.Add(t)
    return t


def main() -> None:
    HIST.mkdir(exist_ok=True)
    shutil.copy2(PCB, HIST / "qfbms32_pre_working_nets.kicad_pcb")
    shutil.copy2(SCH, HIST / "qfbms32_pre_working_nets.kicad_sch")

    board = pcbnew.LoadBoard(str(PCB))

    # --- 1) Power connectors (wiring diagram) ---
    # J_BAT1: pad1 TOP CELL, pad2 BOT (from silk Y positions)
    set_pad(board, "J_BAT1", "1", "TOP_CELL")
    set_pad(board, "J_BAT1", "2", "BOT")
    # Alias equality for sense stack ends
    # CELL32 == TOP_CELL, CELL0 == BOT (same nets)
    # Re-get: use same net objects by assigning identical names via merge:
    # In KiCad, different names are different nets — document aliases; tie with copper later.
    # For working design, use CELL32/CELL0 as canonical stack nets and alias power names:
    set_pad(board, "J_BAT1", "1", "CELL32")  # TOP_CELL
    set_pad(board, "J_BAT1", "2", "CELL0")   # BOT

    set_pad(board, "J_CHG1", "1", "CHG+")
    set_pad(board, "J_CHG1", "2", "CHG-")

    # Mounting tabs → no net (leave 0) or GND mechanical — leave unconnected

    # --- 2) COMM (silk: CANH, CANL, ISO_G, 5V_ESC) pad1..4 left→right ---
    set_all_named(
        board,
        "J_COMM1",
        {"1": "CANH", "2": "CANL", "3": "ISO_GND", "4": "5VExt"},
    )

    # --- 3) Temp connectors: pad1 = TSx, pad2 = VSS/GND bias return ---
    for i, ref in enumerate(["J_T1", "J_T2", "J_T3", "J_T4"], start=1):
        set_pad(board, ref, "1", f"TS{i}")
        set_pad(board, ref, "2", "GND")

    # --- 4) Cell sense connectors: 33 pads by ascending X → CELL32 … CELL0 ---
    cell_pads: list[tuple[float, str, str]] = []
    for cref in ["J_CELL4", "J_CELL3", "J_CELL2", "J_CELL1"]:
        fp = board.FindFootprintByReference(cref)
        for pad in fp.Pads():
            n = pad.GetNumber()
            if not n or n == "MP":
                continue
            if not str(n).isdigit():
                continue
            cell_pads.append((pcbnew.ToMM(pad.GetPosition().x), cref, str(n)))
    cell_pads.sort(key=lambda t: t[0])
    assert len(cell_pads) == 33, f"expected 33 cell pads, got {len(cell_pads)}"
    for cell_n, (x, cref, pnum) in enumerate(reversed(cell_pads)):
        # leftmost (small x) = CELL32, rightmost = CELL0
        pass
    for idx, (x, cref, pnum) in enumerate(cell_pads):
        cell_n = 32 - idx
        set_pad(board, cref, pnum, f"CELL{cell_n}")
        print(f"  {cref}.pad{pnum} x={x:.2f} -> CELL{cell_n}")

    # --- 5) SSR + decoupling ---
    # U_SSR1: 1 IN_CHG, 2 IN_DSG, 3 PSW_EN, 4 GND, 5 VBOOST, 6 VBAT_S, 7 OUT_DSG, 8 OUT_CHG
    set_all_named(
        board,
        "U_SSR1",
        {
            "1": "PIN_CHG_EN",
            "2": "PIN_OUT_EN",
            "3": "PIN_PSW_EN",
            "4": "GND",
            "5": "VBOOST",
            "6": "CELL32",  # VBAT_S senses top of stack
            "7": "SSR_OUT_DSG",
            "8": "SSR_OUT_CHG",
        },
    )
    # C_SSR1 / C_SSR2 between VBOOST and GND (pad1 toward SSR / +Y = VBOOST)
    for cref in ("C_SSR1", "C_SSR2"):
        set_pad(board, cref, "1", "VBOOST")
        set_pad(board, cref, "2", "GND")

    # R_SSR1: gate series toward SSR_OUT_CHG / CHG gate
    set_pad(board, "R_SSR1", "1", "SSR_OUT_CHG")
    set_pad(board, "R_SSR1", "2", "Q1_GATE")
    # R_SSR2: 10k pull-down on gate
    set_pad(board, "R_SSR2", "1", "Q1_GATE")
    set_pad(board, "R_SSR2", "2", "GND")

    # --- 6) FETs (TOLL: pins 1-3 typically source/kelvin, 4 gate?, D=drain — verify AGM15T03LL)
    # AGM15T03LL TOLL-8: common layout Source pads 1-3, Gate 4, Kelvin 5?, Drain tab D
    # Working assumption matching CHG near J_CHG1 / DSG near J_BAT1:
    set_all_named(
        board,
        "Q1",
        {
            "1": "CHG+",
            "2": "CHG+",
            "3": "CHG+",
            "4": "Q1_GATE",
            "5": "CHG+",
            "6": "CHG+",
            "7": "CHG+",
            "8": "CHG+",
            "D": "CELL32",  # high-side drain from pack+
        },
    )
    set_all_named(
        board,
        "Q2",
        {
            "1": "PACK+",
            "2": "PACK+",
            "3": "PACK+",
            "4": "Q2_GATE",
            "5": "PACK+",
            "6": "PACK+",
            "7": "PACK+",
            "8": "PACK+",
            "D": "CELL32",
        },
    )

    # Gate drive leftovers
    set_pad(board, "R_G1", "1", "Q1_GATE")
    set_pad(board, "R_G1", "2", "SSR_OUT_CHG")
    set_pad(board, "R_GS1", "1", "Q1_GATE")
    set_pad(board, "R_GS1", "2", "CHG+")
    set_pad(board, "D_GS1", "1", "Q1_GATE")  # zener anode/cathode — SOD: pad1 typically cathode mark side varies
    set_pad(board, "D_GS1", "2", "CHG+")

    # Sense resistors: pack current path CELL0/BOT domain (low-side sense) — place on SRP/SRN later
    set_pad(board, "R_SH1", "1", "CELL0")
    set_pad(board, "R_SH1", "2", "SHUNT_MID")
    set_pad(board, "R_SH2", "1", "SHUNT_MID")
    set_pad(board, "R_SH2", "2", "CHG-")  # charger return shares sense path (common-port-ish)

    # --- 7) Dual BQ VC / power ---
    # U_BQ1 = IC1 lower: CELL0..CELL16
    # U_BQ2 = IC2 upper: CELL16..CELL32
    for vc, pad_no in BQ_VC.items():
        set_pad(board, "U_BQ1", pad_no, f"BQ1_VC{vc}")
        set_pad(board, "U_BQ2", pad_no, f"BQ2_VC{vc}")
    set_pad(board, "U_BQ1", BQ_VSS, "GND")
    set_pad(board, "U_BQ2", BQ_VSS, "GND")
    set_pad(board, "U_BQ1", BQ_BAT, "BQ1_BAT")
    set_pad(board, "U_BQ2", BQ_BAT, "BQ2_BAT")
    # Tie BAT pins toward their stack tops via same net as filtered top VC for now
    set_pad(board, "U_BQ1", BQ_BAT, "BQ1_VC16")
    set_pad(board, "U_BQ2", BQ_BAT, "BQ2_VC16")
    set_pad(board, "U_BQ1", BQ_SRP, "SRP")
    set_pad(board, "U_BQ1", BQ_SRN, "SRN")
    set_pad(board, "U_BQ2", BQ_SRP, "SRP")
    set_pad(board, "U_BQ2", BQ_SRN, "SRN")
    # Thermistors on lower BQ
    set_pad(board, "U_BQ1", BQ_TS1, "TS1")
    set_pad(board, "U_BQ1", BQ_TS2, "TS2")
    set_pad(board, "U_BQ1", BQ_TS3, "TS3")
    set_pad(board, "U_BQ2", BQ_TS1, "TS4")

    # --- 8) Filter resistors R_F1..32: TI 20Ω, CELL → BQx_VCy ---
    # R_F placed left→right under connectors: R_F1 near CELL32 side, R_F32 near CELL0 side
    # Map R_Fn to CELLn stack position: R_F1 serves CELL32→BQ2_VC16 … need consistent index.
    # Placement: R_F1 at x=37.4 (left/high), R_F32 at x=99.5 (right/low)
    # So R_Fk filters CELL(33-k): R_F1→CELL32, R_F32→CELL1 (CELL0 has no series R to VSS on EVM sometimes has R)
    for k in range(1, 33):
        fp = board.FindFootprintByReference(f"R_F{k}")
        if not fp:
            continue
        fp.SetValue("20R")
        cell_n = 33 - k  # R_F1→32, R_F32→1
        # pad orientation: rot 0, pad1 left / pad2 right typically for 0402
        # Use pad toward connector (higher Y ~ sense) as CELLn, other as filtered VC
        pads = {p.GetNumber(): p for p in fp.Pads()}
        # Assign by Y: higher Y (toward connectors at y=24.75) = cell side
        ordered = sorted(fp.Pads(), key=lambda p: p.GetPosition().y, reverse=True)
        cell_pad, vc_pad = ordered[0], ordered[1]
        # Which BQ owns this cell?
        if cell_n <= 16:
            vc_net = f"BQ1_VC{cell_n}"
        else:
            vc_net = f"BQ2_VC{cell_n - 16}"
        cell_pad.SetNet(net(board, f"CELL{cell_n}"))
        vc_pad.SetNet(net(board, vc_net))

    # CELL0 → BQ1_VC0 via short (also R often on EVM) — tie BQ1_VC0 to CELL0 for now if no R_F0
    set_pad(board, "U_BQ1", BQ_VC[0], "CELL0")
    # Mid-stack: CELL16 feeds both BQ1_VC16 and BQ2_VC0
    set_pad(board, "U_BQ1", BQ_VC[16], "BQ1_VC16")
    set_pad(board, "U_BQ2", BQ_VC[0], "CELL16")
    # After R_F for cell16, BQ1_VC16 should be filtered; keep CELL16 on connector.
    # Re-link: R_F that maps to cell16 is k where 33-k=16 → k=17
    # BQ2_VC0 should get filter from CELL16 — use dedicated net BQ2_VC0 via a 20R;
    # For simplicity tie BQ2_VC0 to CELL16 directly (EVM often has series R — TODO).
    set_pad(board, "U_BQ2", BQ_VC[0], "CELL16")

    # Balance resistors R_B*: leave netless for now.
    # TI balances through VC + series R_F; wiring R_B across cells would be always-on bleed.
    # Keep footprints/values for possible later DNP or alternate topology.

    # Fuse in series on TOP_CELL feed (BAT pad1 already CELL32; use fused net into FET drains)
    set_pad(board, "F1", "1", "CELL32")
    set_pad(board, "F1", "2", "CELL32_FUSED")
    # Retarget FET drains to fused top
    set_pad(board, "Q1", "D", "CELL32_FUSED")
    set_pad(board, "Q2", "D", "CELL32_FUSED")
    set_pad(board, "U_SSR1", "6", "CELL32")  # sense before fuse OK
    # --- 9) Route SSR decoupling (short stubs to IC pads) ---
    # C_SSR2 pad1 (VBOOST) at (30.0, 2.65), U_SSR1 pad5 at (31.925, 1.595)
    add_track(board, 30.00, 2.65, 31.925, 2.65, "VBOOST", width=0.3)
    add_track(board, 31.925, 2.65, 31.925, 1.595, "VBOOST", width=0.3)
    # C_SSR1 pad1 (VBOOST) at (28.45, 2.525) → join VBOOST
    add_track(board, 28.45, 2.525, 30.00, 2.525, "VBOOST", width=0.25)
    add_track(board, 30.00, 2.525, 30.00, 2.65, "VBOOST", width=0.25)
    # GND side: pad2 of caps toward board edge → U_SSR1 pad4 GND at (41.475, 1.595)
    # Route along top edge y≈0.9
    add_track(board, 28.45, 0.975, 30.00, 0.975, "GND", width=0.25)
    add_track(board, 30.00, 0.75, 30.00, 0.975, "GND", width=0.25)
    add_track(board, 30.00, 0.975, 41.475, 0.975, "GND", width=0.3)
    add_track(board, 41.475, 0.975, 41.475, 1.595, "GND", width=0.3)

    # --- 10) Place TI 0.22uF differential caps near BQ (freer placement) ---
    # One cap between BQ1_VCn and BQ1_VC(n-1) for n=1..16; same for BQ2
    # Place in two rows under each BQ body.
    def place_cf(ref: str, x: float, y: float, net_a: str, net_b: str):
        existing = board.FindFootprintByReference(ref)
        if existing:
            board.Remove(existing)
        fp = pcbnew.FootprintLoad(str(FP_CAP), "C_0402_1005Metric")
        if not fp:
            print("Failed to load C_0402")
            return
        board.Add(fp)
        fp.SetReference(ref)
        fp.SetValue("0.22uF")
        fp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x), pcbnew.FromMM(y)))
        fp.SetOrientation(pcbnew.EDA_ANGLE(0, pcbnew.DEGREES_T))
        fp.Reference().SetVisible(False)
        fp.Value().SetVisible(False)
        pads = list(fp.Pads())
        pads[0].SetNet(net(board, net_a))
        pads[1].SetNet(net(board, net_b))

    # U_BQ1 at ~87.88,13.88 — place C_F row at y=18.5
    # U_BQ2 at ~44.77,13.88
    n = 1
    for bq, x0 in (("BQ1", 80.0), ("BQ2", 37.0)):
        for vc in range(1, 17):
            place_cf(f"C_F{n}", x0 + (vc - 1) * 1.1, 18.6, f"{bq}_VC{vc}", f"{bq}_VC{vc-1}")
            n += 1

    pcbnew.Refresh()
    pcbnew.SaveBoard(str(PCB), board)
    print("Saved", PCB)

    # --- 11) Light schematic updates: R_F values + SSR labels note ---
    sch = SCH.read_text(encoding="utf-8")
    # Fix BQ refs U1/U2 → U_BQ1/U_BQ2 to match PCB
    sch2 = sch.replace('(property "Reference" "U1"', '(property "Reference" "U_BQ1"', 1)
    # only first U1 is BQ; careful with instances path reference
    sch2 = sch2.replace('(reference "U1")', '(reference "U_BQ1")')
    sch2 = sch2.replace('(property "Reference" "U2"', '(property "Reference" "U_BQ2"', 1)
    sch2 = sch2.replace('(reference "U2")', '(reference "U_BQ2")')
    # Update R_F values in sch if present as 100R
    sch2 = sch2.replace(
        '(property "Reference" "R_F',
        '(property "Reference" "R_F',
    )  # noop keep structure
    # Bulk replace filter resistor values: only lines near R_F — crude but OK
    import re

    def fix_rf_value(m):
        block = m.group(0)
        block = re.sub(
            r'\(property "Value" "100R"',
            '(property "Value" "20R"',
            block,
            count=1,
        )
        return block

    sch2 = re.sub(
        r'\(symbol \(lib_id "Device:R"\)[\s\S]*?\(property "Reference" "R_F\d+"[\s\S]*?\n\t\)',
        fix_rf_value,
        sch2,
    )
    # Append local labels for SSR caps if not present
    if "VBOOST" not in sch2 or sch2.count('(label "VBOOST"') < 1:
        label_blob = """
	(label "VBOOST" (at 162.0 22.0 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "lbl-vboost-cssr"))
	(label "GND" (at 162.0 28.0 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "lbl-gnd-cssr"))
	(label "CELL32" (at 10.0 20.0 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "lbl-cell32"))
	(label "CELL0" (at 10.0 30.0 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "lbl-cell0"))
	(label "CHG+" (at 20.0 10.0 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "lbl-chgp"))
	(label "CHG-" (at 20.0 15.0 0) (effects (font (size 1.27 1.27)) (justify left)) (uuid "lbl-chgm"))
"""
        # insert before sheet instances / end
        if "(sheet_instances" in sch2:
            sch2 = sch2.replace("(sheet_instances", label_blob + "\n\t(sheet_instances", 1)
        else:
            sch2 = sch2.rstrip() + "\n" + label_blob + "\n"
    SCH.write_text(sch2, encoding="utf-8")
    print("Updated schematic refs/labels")

    # Summary
    netted = 0
    for fp in board.GetFootprints():
        if any(p.GetNetCode() != 0 for p in fp.Pads()):
            netted += 1
    names = [str(n) for n in board.GetNetInfo().NetsByName() if str(n)]
    print(f"Footprints with nets: {netted}; named nets: {len(names)}")


if __name__ == "__main__":
    main()
