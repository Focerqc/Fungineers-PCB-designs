"""
Replace dangling net labels with pin→stub-wire→label so KiCad ERC connects them.

Operates on labels we added for WORKING_TOPOLOGY (uuid not required — match by name+near known pins).
Simpler approach: delete all labels we can identify from the wire_sch blob region and
re-emit wire+label pairs for core connectivity.
"""
from __future__ import annotations

import re
import shutil
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCH = ROOT / "qfbms32.kicad_sch"
HIST = ROOT / ".history"

BQ_PINS = {
    "48": (-20.32, 40.64, 0),
    "1": (-20.32, 38.1, 0),
    "2": (-20.32, 35.56, 0),
    "3": (-20.32, 33.02, 0),
    "4": (-20.32, 30.48, 0),
    "5": (-20.32, 27.94, 0),
    "6": (-20.32, 25.4, 0),
    "7": (-20.32, 22.86, 0),
    "8": (-20.32, 20.32, 0),
    "9": (-20.32, 17.78, 0),
    "10": (-20.32, 15.24, 0),
    "11": (-20.32, 12.7, 0),
    "12": (-20.32, 10.16, 0),
    "13": (-20.32, 7.62, 0),
    "14": (-20.32, 5.08, 0),
    "15": (-20.32, 2.54, 0),
    "16": (-20.32, 0.0, 0),
    "17": (0.0, -45.72, 90),
    "18": (-20.32, -7.62, 0),
    "20": (-20.32, -5.08, 0),
    "21": (-20.32, -12.7, 0),
    "22": (-20.32, -15.24, 0),
    "23": (-20.32, -17.78, 0),
    "47": (0.0, 45.72, 270),
}

SSR_PINS = {
    "1": (-10.16, 3.81, 0),
    "2": (-10.16, 1.27, 0),
    "3": (-10.16, -1.27, 0),
    "4": (-10.16, -3.81, 0),
    "5": (10.16, -3.81, 180),
    "6": (10.16, -1.27, 180),
    "7": (10.16, 1.27, 180),
    "8": (10.16, 3.81, 180),
}

FET_PINS = {"1": (-7.62, 0.0, 0), "D": (0.0, 8.89, 270), "2": (0.0, -8.89, 90)}
STUB = 5.08  # 4 grid steps


def uid() -> str:
    return str(uuid.uuid4())


def snap(v: float) -> float:
    return round(v / 1.27) * 1.27


def wire_and_label(net: str, x0: float, y0: float, pin_rot: float) -> str:
    """Stub wire from pin tip outward, label at far end."""
    pr = int(pin_rot) % 360
    if pr == 0:  # pin faces west — stub further west
        x1, y1 = x0 - STUB, y0
        lrot, just = 180, "right bottom"
    elif pr == 180:
        x1, y1 = x0 + STUB, y0
        lrot, just = 0, "left bottom"
    elif pr == 90:  # faces south
        x1, y1 = x0, y0 + STUB
        lrot, just = 90, "left bottom"
    elif pr == 270:  # faces north
        x1, y1 = x0, y0 - STUB
        lrot, just = 270, "left bottom"
    else:
        x1, y1 = x0 - STUB, y0
        lrot, just = 180, "right bottom"
    # Keep pin endpoint exact (may be off 1.27 grid for some symbols); stub end can match.
    return (
        f"\t(wire\n"
        f"\t\t(pts (xy {x0:.2f} {y0:.2f}) (xy {x1:.2f} {y1:.2f}))\n"
        f"\t\t(stroke (width 0) (type default))\n"
        f'\t\t(uuid "{uid()}")\n'
        f"\t)\n"
        f'\t(label "{net}"\n'
        f"\t\t(at {x1:.2f} {y1:.2f} {lrot})\n"
        f"\t\t(effects (font (size 1.27 1.27)) (justify {just}))\n"
        f'\t\t(uuid "{uid()}")\n'
        f"\t)\n"
    )


def rc_pin(sx, sy, srot, pin):
    px, py = (0.0, 3.81) if pin == 1 else (0.0, -3.81)
    srot = srot % 360
    if srot == 0:
        return sx + px, sy + py, 270 if pin == 1 else 90
    if srot == 90:
        return sx - py, sy + px, 0 if pin == 1 else 180
    if srot == 180:
        return sx - px, sy - py, 90 if pin == 1 else 270
    if srot == 270:
        return sx + py, sy - px, 180 if pin == 1 else 0
    return sx + px, sy + py, 0


def conn_pin_ys(n: int):
    top = (n - 1) * 1.27
    return [(str(i), top - (i - 1) * 2.54) for i in range(1, n + 1)]


def vc_map(prefix: str, vc0: str) -> dict[str, str]:
    pin_for_vc = {
        16: "48",
        15: "1",
        14: "2",
        13: "3",
        12: "4",
        11: "5",
        10: "6",
        9: "7",
        8: "8",
        7: "9",
        6: "10",
        5: "11",
        4: "12",
        3: "13",
        2: "14",
        1: "15",
        0: "16",
    }
    m = {pin_for_vc[0]: vc0, "17": "GND", "18": "SRP", "20": "SRN", "47": f"{prefix}_VC16"}
    for vc in range(1, 17):
        m[pin_for_vc[vc]] = f"{prefix}_VC{vc}"
    return m


def main() -> None:
    HIST.mkdir(exist_ok=True)
    shutil.copy2(SCH, HIST / "qfbms32_pre_fix_wires.kicad_sch")
    sch = SCH.read_text(encoding="utf-8")

    # Remove labels that wire_sch added for topology nets (keep ESP/CAN/USB ones that were pre-existing)
    # Heuristic: remove labels whose net names match topology set AND are not the old ESP-area ones
    # Safer: remove ALL labels that appear after C_SSR2 / in our added section by net name list,
    # then re-add wired versions. Keep original ESP labels (PIN_*, USB_*, CAN*, I2C, +3V3, BUZZ*).

    keep_prefix = (
        "PIN_",
        "USB_",
        "CAN_RX",
        "CAN_TX",
        "CANH",
        "CANL",
        "ISO_GND",
        "5VExt",
        "+3V3",
        "I2C_",
        "BUZZ",
    )

    def should_keep(name: str) -> bool:
        return any(name.startswith(p) for p in keep_prefix) or name in ("CANH", "CANL", "ISO_GND", "5VExt", "+3V3")

    # Remove multiline label blocks for non-keep names
    def strip_label(m: re.Match) -> str:
        name = m.group(1)
        if should_keep(name):
            return m.group(0)
        return ""

    sch2 = re.sub(
        r'\n\t\(label "([^"]+)"\s*\n\t\t\(at [^\n]+\n\t\t\(effects[\s\S]*?\n\t\t\(uuid "[^"]+"\)\n\t\)',
        lambda m: ("\n" + m.group(0).lstrip("\n")) if should_keep(m.group(1)) else "",
        sch,
    )
    # Also strip compact one-liners
    sch2 = re.sub(
        r'\n\t\(label "([^"]+)" \(at [^)]+\) \(effects \(font \(size 1\.27 1\.27\)\) \(justify [^)]+\)\) \(uuid "[^"]+"\)\)',
        lambda m: m.group(0) if should_keep(m.group(1)) else "",
        sch2,
    )

    # Remove any wires we may have added previously (none yet) — skip

    blobs: list[str] = []

    def add(net, x, y, prot):
        blobs.append(wire_and_label(net, x, y, prot))

    # BQs
    for ref, (sx, sy), prefix, vc0, extra in (
        ("U_BQ1", (149.86, 100.33), "BQ1", "CELL0", {"21": "TS1", "22": "TS2", "23": "TS3"}),
        ("U_BQ2", (250.19, 100.33), "BQ2", "CELL16", {"21": "TS4"}),
    ):
        mapping = vc_map(prefix, vc0)
        mapping.update(extra)
        for pnum, net in mapping.items():
            if pnum not in BQ_PINS:
                continue
            dx, dy, prot = BQ_PINS[pnum]
            add(net, sx + dx, sy + dy, prot)

    # SSR
    ssr = {
        "1": "PIN_CHG_EN",
        "2": "PIN_OUT_EN",
        "3": "PIN_PSW_EN",
        "4": "GND",
        "5": "VBOOST",
        "6": "CELL32",
        "7": "SSR_OUT_DSG",
        "8": "SSR_OUT_CHG",
    }
    for p, net in ssr.items():
        dx, dy, prot = SSR_PINS[p]
        add(net, 155.0 + dx, 25.0 + dy, prot)

    # C_SSR
    for cx in (165.0, 175.0):
        x, y, r = rc_pin(cx, 25.0, 0, 1)
        add("VBOOST", x, y, r)
        x, y, r = rc_pin(cx, 25.0, 0, 2)
        add("GND", x, y, r)

    # FETs
    for qy, gnet, snet in ((45.0, "Q1_GATE", "CHG+"), (80.0, "Q2_GATE", "PACK+")):
        for p, net in (("1", gnet), ("D", "CELL32_FUSED"), ("2", snet)):
            dx, dy, prot = FET_PINS[p]
            add(net, 195.0 + dx, qy + dy, prot)

    # R_G1 rot90
    x, y, r = rc_pin(175.0, 45.0, 90, 1)
    add("SSR_OUT_CHG", x, y, r)
    x, y, r = rc_pin(175.0, 45.0, 90, 2)
    add("Q1_GATE", x, y, r)

    # R_SSR2
    x, y, r = rc_pin(185.0, 35.0, 0, 1)
    add("Q1_GATE", x, y, r)
    x, y, r = rc_pin(185.0, 35.0, 0, 2)
    add("GND", x, y, r)

    # D_GS1
    x, y, r = rc_pin(185.0, 25.0, 0, 1)
    add("Q1_GATE", x, y, r)
    x, y, r = rc_pin(185.0, 25.0, 0, 2)
    add("CHG+", x, y, r)

    # R_F / C_F — parse positions from sch
    for m in re.finditer(
        r'\(symbol \(lib_id "Device:R"\)\s*\(at ([0-9.-]+) ([0-9.-]+) ([0-9.-]+)\)[\s\S]*?'
        r'\(property "Reference" "(R_F\d+)"',
        sch2,
    ):
        x, y, rot, ref = float(m.group(1)), float(m.group(2)), float(m.group(3)), m.group(4)
        k = int(ref[3:])
        cell_n = 33 - k
        vc = f"BQ1_VC{cell_n}" if cell_n <= 16 else f"BQ2_VC{cell_n - 16}"
        ax, ay, ar = rc_pin(x, y, rot, 1)
        bx, by, br = rc_pin(x, y, rot, 2)
        add(f"CELL{cell_n}", ax, ay, ar)
        add(vc, bx, by, br)

    for m in re.finditer(
        r'\(symbol \(lib_id "Device:C"\)\s*\(at ([0-9.-]+) ([0-9.-]+) ([0-9.-]+)\)[\s\S]*?'
        r'\(property "Reference" "(C_F\d+)"',
        sch2,
    ):
        x, y, rot, ref = float(m.group(1)), float(m.group(2)), float(m.group(3)), m.group(4)
        n = int(ref[3:])
        if n <= 16:
            prefix, vc0, vc = "BQ1", "CELL0", n
        else:
            prefix, vc0, vc = "BQ2", "CELL16", n - 16
        net_a = f"{prefix}_VC{vc}"
        net_b = vc0 if vc == 1 else f"{prefix}_VC{vc - 1}"
        ax, ay, ar = rc_pin(x, y, rot, 1)
        bx, by, br = rc_pin(x, y, rot, 2)
        add(net_a, ax, ay, ar)
        add(net_b, bx, by, br)

    # Connectors
    for m in re.finditer(
        r'\(symbol \(lib_id "Connector_Generic:Conn_01x(\d+)"\)\s*\(at ([0-9.-]+) ([0-9.-]+) ([0-9.-]+)\)[\s\S]*?'
        r'\(property "Reference" "(J_[^"]+)"',
        sch2,
    ):
        n = int(m.group(1))
        x, y = float(m.group(2)), float(m.group(3))
        ref = m.group(5)
        # net maps
        if ref == "J_BAT1":
            nets = ["CELL32", "CELL0"]
        elif ref == "J_CHG1":
            nets = ["CHG+", "CHG-"]
        elif ref == "J_COMM1":
            nets = ["CANH", "CANL", "ISO_GND", "5VExt"]
        elif ref.startswith("J_T"):
            i = int(ref[-1])
            nets = [f"TS{i}", "GND"]
        elif ref == "J_CELL4":
            nets = [f"CELL{c}" for c in range(32, 26, -1)]
        elif ref == "J_CELL3":
            nets = [f"CELL{c}" for c in range(26, 18, -1)]
        elif ref == "J_CELL2":
            nets = [f"CELL{c}" for c in range(18, 9, -1)]
        elif ref == "J_CELL1":
            nets = [f"CELL{c}" for c in range(9, -1, -1)]
        else:
            continue
        for (pnum, py), net in zip(conn_pin_ys(n), nets):
            add(net, x - 5.08, y + py, 0)

    # F1 / R_SH / R_SSR1
    for m in re.finditer(
        r'\(symbol \(lib_id "Device:R"\)\s*\(at ([0-9.-]+) ([0-9.-]+) ([0-9.-]+)\)[\s\S]*?'
        r'\(property "Reference" "(F1|R_SH1|R_SH2|R_SSR1)"',
        sch2,
    ):
        x, y, rot, ref = float(m.group(1)), float(m.group(2)), float(m.group(3)), m.group(4)
        nets = {
            "F1": ("CELL32", "CELL32_FUSED"),
            "R_SH1": ("CELL0", "SHUNT_MID"),
            "R_SH2": ("SHUNT_MID", "CHG-"),
            "R_SSR1": ("SSR_OUT_CHG", "Q1_GATE"),
        }[ref]
        ax, ay, ar = rc_pin(x, y, rot, 1)
        bx, by, br = rc_pin(x, y, rot, 2)
        add(nets[0], ax, ay, ar)
        add(nets[1], bx, by, br)

    payload = "\n" + "".join(blobs) + "\n"
    insert_at = sch2.rfind("\n\t(sheet_instances")
    if insert_at < 0:
        insert_at = sch2.rfind("\n)")
    sch2 = sch2[:insert_at] + payload + sch2[insert_at:]
    SCH.write_text(sch2, encoding="utf-8")
    print(f"wrote wires+labels={len(blobs)} -> {SCH}")


if __name__ == "__main__":
    main()
