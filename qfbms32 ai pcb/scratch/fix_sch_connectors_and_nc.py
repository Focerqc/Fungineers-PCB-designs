"""
Fix connector stub wiring (wrong pin Y map + missing symbol Y-flip) and
add no_connect on remaining unused BQ digital pins.
Also re-stub D_GS1 with horizontal stubs to avoid vertical self-shorts.
"""
from __future__ import annotations

import re
import shutil
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCH = ROOT / "qfbms32.kicad_sch"
HIST = ROOT / ".history"
STUB = 2.54

# Conn_01xN pin local coords from embedded lib (+Y up)
CONN_PINS: dict[int, list[tuple[str, float, float]]] = {
    2: [("1", -5.08, 0.0), ("2", -5.08, -2.54)],
    4: [("1", -5.08, 2.54), ("2", -5.08, 0.0), ("3", -5.08, -2.54), ("4", -5.08, -5.08)],
    6: [
        ("1", -5.08, 5.08),
        ("2", -5.08, 2.54),
        ("3", -5.08, 0.0),
        ("4", -5.08, -2.54),
        ("5", -5.08, -5.08),
        ("6", -5.08, -7.62),
    ],
    8: [
        ("1", -5.08, 7.62),
        ("2", -5.08, 5.08),
        ("3", -5.08, 2.54),
        ("4", -5.08, 0.0),
        ("5", -5.08, -2.54),
        ("6", -5.08, -5.08),
        ("7", -5.08, -7.62),
        ("8", -5.08, -10.16),
    ],
    9: [
        ("1", -5.08, 10.16),
        ("2", -5.08, 7.62),
        ("3", -5.08, 5.08),
        ("4", -5.08, 2.54),
        ("5", -5.08, 0.0),
        ("6", -5.08, -2.54),
        ("7", -5.08, -5.08),
        ("8", -5.08, -7.62),
        ("9", -5.08, -10.16),
    ],
    10: [
        ("1", -5.08, 10.16),
        ("2", -5.08, 7.62),
        ("3", -5.08, 5.08),
        ("4", -5.08, 2.54),
        ("5", -5.08, 0.0),
        ("6", -5.08, -2.54),
        ("7", -5.08, -5.08),
        ("8", -5.08, -7.62),
        ("9", -5.08, -10.16),
        ("10", -5.08, -12.7),
    ],
}

# BQ right-side leftovers + BQ2 unused TS
BQ_EXTRA_NC = {
    "U_BQ1": ["25", "28", "29", "30", "31", "32", "38"],
    "U_BQ2": ["22", "23", "25", "28", "29", "30", "31", "32", "38"],
}
BQ_PIN = {
    "22": (-20.32, -15.24),
    "23": (-20.32, -17.78),
    "25": (20.32, -25.4),
    "28": (20.32, -15.24),
    "29": (20.32, -12.7),
    "30": (20.32, -35.56),
    "31": (20.32, -33.02),
    "32": (20.32, -30.48),
    "38": (20.32, 35.56),
}


def uid() -> str:
    return str(uuid.uuid4())


def pin_world(sx: float, sy: float, dx: float, dy: float) -> tuple[float, float]:
    return sx + dx, sy - dy


def wire_label(net: str, x0: float, y0: float, facing: float = 0) -> str:
    pr = int(facing) % 360
    if pr == 0:
        x1, y1, lrot, just = x0 - STUB, y0, 180, "right bottom"
    elif pr == 180:
        x1, y1, lrot, just = x0 + STUB, y0, 0, "left bottom"
    elif pr == 90:
        x1, y1, lrot, just = x0, y0 + STUB, 90, "left bottom"
    else:
        x1, y1, lrot, just = x0, y0 - STUB, 270, "left bottom"
    return (
        f"\t(wire\n"
        f"\t\t(pts\n"
        f"\t\t\t(xy {x0:.2f} {y0:.2f}) (xy {x1:.2f} {y1:.2f})\n"
        f"\t\t)\n"
        f"\t\t(stroke (width 0) (type default))\n"
        f'\t\t(uuid "{uid()}")\n'
        f"\t)\n"
        f'\t(label "{net}"\n'
        f"\t\t(at {x1:.2f} {y1:.2f} {lrot:g})\n"
        f"\t\t(effects (font (size 1.27 1.27)) (justify {just}))\n"
        f'\t\t(uuid "{uid()}")\n'
        f"\t)\n"
    )


def no_connect(x: float, y: float) -> str:
    return f'\t(no_connect (at {x:.2f} {y:.2f}) (uuid "{uid()}"))\n'


def find_symbol_at(sch: str, ref: str) -> tuple[float, float, float]:
    for m in re.finditer(r"\n\t\(symbol[\s\n]+\(lib_id ", sch):
        start = m.start() + 1
        depth = 0
        end = None
        for i in range(start, len(sch)):
            if sch[i] == "(":
                depth += 1
            elif sch[i] == ")":
                depth -= 1
                if depth == 0:
                    end = i + 1
                    break
        block = sch[start:end]
        if re.search(rf'\(property "Reference" "{re.escape(ref)}"', block):
            am = re.search(r"\(at ([0-9.-]+) ([0-9.-]+) ([0-9.-]+)\)", block)
            return float(am.group(1)), float(am.group(2)), float(am.group(3))
    raise SystemExit(f"missing {ref}")


def main() -> None:
    HIST.mkdir(exist_ok=True)
    shutil.copy2(SCH, HIST / "qfbms32_pre_fix_connectors.kicad_sch")
    sch = SCH.read_text(encoding="utf-8")

    # Strip wire+label pairs in connector/power-discrete bank (x>=440)
    def drop_bank(m: re.Match) -> str:
        x0 = float(m.group(1))
        if x0 >= 440:
            return ""
        return m.group(0)

    sch = re.sub(
        r"\n\t\(wire\n"
        r"\t\t\(pts\n"
        r"\t\t\t\(xy ([0-9.-]+) ([0-9.-]+)\) \(xy [0-9.-]+ [0-9.-]+\)\n"
        r"\t\t\)\n"
        r"\t\t\(stroke \(width 0\) \(type default\)\)\n"
        r'\t\t\(uuid "[^"]+"\)\n'
        r"\t\)\n"
        r'\t\(label "[^"]+"\n'
        r"\t\t\(at [^\n]+\n"
        r"\t\t\(effects [^\n]+\n"
        r'\t\t\(uuid "[^"]+"\)\n'
        r"\t\)",
        drop_bank,
        sch,
    )

    # Strip D_GS1 stubs near (381, 38) so we can re-emit horizontal
    def drop_dgs(m: re.Match) -> str:
        x0, y0 = float(m.group(1)), float(m.group(2))
        if abs(x0 - 381.0) < 0.2 and 30 <= y0 <= 50:
            return ""
        return m.group(0)

    sch = re.sub(
        r"\n\t\(wire\n"
        r"\t\t\(pts\n"
        r"\t\t\t\(xy ([0-9.-]+) ([0-9.-]+)\) \(xy [0-9.-]+ [0-9.-]+\)\n"
        r"\t\t\)\n"
        r"\t\t\(stroke \(width 0\) \(type default\)\)\n"
        r'\t\t\(uuid "[^"]+"\)\n'
        r"\t\)\n"
        r'\t\(label "[^"]+"\n'
        r"\t\t\(at [^\n]+\n"
        r"\t\t\(effects [^\n]+\n"
        r'\t\t\(uuid "[^"]+"\)\n'
        r"\t\)",
        drop_dgs,
        sch,
    )

    out: list[str] = []

    connectors: list[tuple[str, int, list[str]]] = [
        ("J_BAT1", 2, ["CELL32", "CELL0"]),
        ("J_CHG1", 2, ["CHG+", "CHG-"]),
        ("J_COMM1", 4, ["CANH", "CANL", "ISO_GND", "5VExt"]),
        ("J_T1", 2, ["TS1", "GND"]),
        ("J_T2", 2, ["TS2", "GND"]),
        ("J_T3", 2, ["TS3", "GND"]),
        ("J_T4", 2, ["TS4", "GND"]),
        ("J_CELL4", 6, [f"CELL{c}" for c in range(32, 26, -1)]),
        ("J_CELL3", 8, [f"CELL{c}" for c in range(26, 18, -1)]),
        ("J_CELL2", 9, [f"CELL{c}" for c in range(18, 9, -1)]),
        ("J_CELL1", 10, [f"CELL{c}" for c in range(9, -1, -1)]),
    ]
    for ref, n, nets in connectors:
        sx, sy, _ = find_symbol_at(sch, ref)
        for (pnum, dx, dy), net in zip(CONN_PINS[n], nets):
            x, y = pin_world(sx, sy, dx, dy)
            out.append(wire_label(net, x, y, 0))
            print(f"{ref}.{pnum} -> {net} @({x:.2f},{y:.2f})")

    # Power discretes F1 / R_SH* / R_SSR1 (Device:R, Y-flip)
    for ref, nets in (
        ("F1", ("CELL32", "CELL32_FUSED")),
        ("R_SH1", ("CELL0", "SHUNT_MID")),
        ("R_SH2", ("SHUNT_MID", "CHG-")),
        ("R_SSR1", ("SSR_OUT_CHG", "Q1_GATE")),
    ):
        sx, sy, srot = find_symbol_at(sch, ref)
        # pin1 local (0,+3.81), pin2 (0,-3.81); instance may be rot 90
        for pin, net, local in ((1, nets[0], (0.0, 3.81)), (2, nets[1], (0.0, -3.81))):
            lx, ly = local[0], -local[1]  # to sheet before rot
            srot_i = int(srot) % 360
            if srot_i == 0:
                ax, ay = sx + lx, sy + ly
                facing = 270 if pin == 1 else 90
            elif srot_i == 90:
                ax, ay = sx + ly, sy - lx
                facing = 0 if pin == 1 else 180
            else:
                raise SystemExit(f"unsupported rot {srot} for {ref}")
            # fix facing after Y-flip for rot0: pin1 at top faces 270
            if srot_i == 0:
                facing = 270 if pin == 1 else 90
            out.append(wire_label(net, ax, ay, facing))
            print(f"{ref}.{pin} -> {net} @({ax:.2f},{ay:.2f})")

    # D_GS1: horizontal stubs (left for anode/top→Q1_GATE, right for cathode/bot→CHG+)
    sx, sy, _ = find_symbol_at(sch, "D_GS1")
    # pin1 top (local +3.81) → world sy-3.81; stub LEFT
    x1, y1 = pin_world(sx, sy, 0.0, 3.81)
    x2, y2 = pin_world(sx, sy, 0.0, -3.81)
    out.append(wire_label("Q1_GATE", x1, y1, 0))
    out.append(wire_label("CHG+", x2, y2, 180))
    print(f"D_GS1.1 Q1_GATE @({x1:.2f},{y1:.2f})  D_GS1.2 CHG+ @({x2:.2f},{y2:.2f})")

    # Extra BQ no_connects
    for ref, pins in BQ_EXTRA_NC.items():
        sx, sy, _ = find_symbol_at(sch, ref)
        for p in pins:
            dx, dy = BQ_PIN[p]
            x, y = pin_world(sx, sy, dx, dy)
            out.append(no_connect(x, y))

    payload = "\n" + "".join(out) + "\n"
    insert_at = sch.rfind("\n\t(sheet_instances")
    if insert_at < 0:
        insert_at = sch.rfind("\n)")
    sch = sch[:insert_at] + payload + sch[insert_at:]
    SCH.write_text(sch, encoding="utf-8")
    print("Wrote", SCH, "added", len(out))


if __name__ == "__main__":
    main()
