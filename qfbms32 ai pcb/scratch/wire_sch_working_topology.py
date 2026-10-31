"""
Wire qfbms32 schematic to WORKING_TOPOLOGY / PCB nets (clean rewrite).

Strategy:
- Embed Conn_01xN lib symbols
- Add missing refs (R_F*, C_F*, J_*, F1, R_SH*, R_SSR1) as instances
- Attach connectivity via short stub wires + local labels (KiCad 10 needs wires)
- Rename U3 -> U_ESP1
- All coordinates computed from known symbol origins (no fragile re-parse)
"""
from __future__ import annotations

import re
import shutil
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCH = ROOT / "qfbms32.kicad_sch"
HIST = ROOT / ".history"
CONN_LIB = Path(r"C:\Program Files\KiCad\10.0\share\kicad\symbols\Connector_Generic.kicad_sym")
SHEET = "/a2322edc-ff52-449c-92df-24faffac0236"
STUB = 5.08
G = 1.27


def uid() -> str:
    return str(uuid.uuid4())


def snap(v: float) -> float:
    return round(v / G) * G


def extract_conn(lib_text: str, name: str) -> str:
    key = f'(symbol "{name}"'
    start = lib_text.find(key)
    if start < 0:
        raise SystemExit(f"missing {name}")
    depth = 0
    for i in range(start, len(lib_text)):
        if lib_text[i] == "(":
            depth += 1
        elif lib_text[i] == ")":
            depth -= 1
            if depth == 0:
                block = lib_text[start : i + 1]
                block = block.replace(f'(symbol "{name}"', f'(symbol "Connector_Generic:{name}"', 1)
                return "\t\t" + block.replace("\n", "\n\t\t") + "\n"
    raise SystemExit(f"unclosed {name}")


def wire_label(net: str, x0: float, y0: float, pin_rot: float) -> str:
    pr = int(pin_rot) % 360
    # Short vertical stubs avoid landing on another VC row (2.54 pitch)
    vstub = 2.54
    if pr == 0:
        x1, y1, lrot, just = x0 - STUB, y0, 180, "right bottom"
    elif pr == 180:
        x1, y1, lrot, just = x0 + STUB, y0, 0, "left bottom"
    elif pr == 90:
        x1, y1, lrot, just = x0, y0 + vstub, 90, "left bottom"
    else:  # 270
        x1, y1, lrot, just = x0, y0 - vstub, 270, "left bottom"
    return (
        f"\t(wire\n"
        f"\t\t(pts\n"
        f"\t\t\t(xy {x0:.2f} {y0:.2f}) (xy {x1:.2f} {y1:.2f})\n"
        f"\t\t)\n"
        f"\t\t(stroke (width 0) (type default))\n"
        f'\t\t(uuid "{uid()}")\n'
        f"\t)\n"
        f'\t(label "{net}"\n'
        f"\t\t(at {x1:.2f} {y1:.2f} {lrot})\n"
        f"\t\t(effects (font (size 1.27 1.27)) (justify {just}))\n"
        f'\t\t(uuid "{uid()}")\n'
        f"\t)\n"
    )


def rc_symbol(lib_id: str, ref: str, value: str, fp: str, x: float, y: float, rot: float = 0) -> str:
    return f"""\t(symbol (lib_id "{lib_id}")
\t\t(at {x:.2f} {y:.2f} {rot:g})
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{ref}" (at {x:.2f} {y - 5.08:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "{value}" (at {x:.2f} {y + 5.08:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "{fp}" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
\t\t(pin "1" (uuid "{uid()}"))
\t\t(pin "2" (uuid "{uid()}"))
\t\t(instances (project "qfbms32" (path "{SHEET}" (reference "{ref}") (unit 1))))
\t)
"""


def conn_symbol(n: int, ref: str, value: str, fp: str, x: float, y: float) -> str:
    pins = "\n".join(f'\t\t(pin "{i}" (uuid "{uid()}"))' for i in range(1, n + 1))
    return f"""\t(symbol (lib_id "Connector_Generic:Conn_01x{n:02d}")
\t\t(at {x:.2f} {y:.2f} 0)
\t\t(unit 1)
\t\t(exclude_from_sim no)
\t\t(in_bom yes)
\t\t(on_board yes)
\t\t(dnp no)
\t\t(uuid "{uid()}")
\t\t(property "Reference" "{ref}" (at {x:.2f} {y - n * 1.27 - 2.54:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Value" "{value}" (at {x:.2f} {y + n * 1.27 + 2.54:.2f} 0) (effects (font (size 1.27 1.27))))
\t\t(property "Footprint" "{fp}" (at {x:.2f} {y:.2f} 0) (hide yes) (effects (font (size 1.27 1.27))))
{pins}
\t\t(instances (project "qfbms32" (path "{SHEET}" (reference "{ref}") (unit 1))))
\t)
"""


def rc_pin(sx: float, sy: float, srot: float, pin: int) -> tuple[float, float, float]:
    px, py = (0.0, 3.81) if pin == 1 else (0.0, -3.81)
    srot %= 360
    if srot == 0:
        return sx + px, sy + py, 270.0 if pin == 1 else 90.0
    if srot == 90:
        return sx - py, sy + px, 0.0 if pin == 1 else 180.0
    if srot == 180:
        return sx - px, sy - py, 90.0 if pin == 1 else 270.0
    return sx + py, sy - px, 180.0 if pin == 1 else 0.0


def conn_pins(n: int) -> list[tuple[str, float]]:
    top = (n - 1) * 1.27
    return [(str(i), top - (i - 1) * 2.54) for i in range(1, n + 1)]


# BQ pin number -> (dx, dy, pin_rot)
BQ = {
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
SSR = {
    "1": (-10.16, 3.81, 0),
    "2": (-10.16, 1.27, 0),
    "3": (-10.16, -1.27, 0),
    "4": (-10.16, -3.81, 0),
    "5": (10.16, -3.81, 180),
    "6": (10.16, -1.27, 180),
    "7": (10.16, 1.27, 180),
    "8": (10.16, 3.81, 180),
}
FET = {"1": (-7.62, 0.0, 0), "D": (0.0, 8.89, 270), "2": (0.0, -8.89, 90)}


def bq_netmap(prefix: str, vc0: str) -> dict[str, str]:
    pin_for_vc = {
        16: "48", 15: "1", 14: "2", 13: "3", 12: "4", 11: "5", 10: "6", 9: "7",
        8: "8", 7: "9", 6: "10", 5: "11", 4: "12", 3: "13", 2: "14", 1: "15", 0: "16",
    }
    m = {pin_for_vc[0]: vc0, "17": "GND", "18": "SRP", "20": "SRN", "47": f"{prefix}_VC16"}
    for vc in range(1, 17):
        m[pin_for_vc[vc]] = f"{prefix}_VC{vc}"
    return m


def main() -> None:
    HIST.mkdir(exist_ok=True)
    shutil.copy2(SCH, HIST / "qfbms32_pre_wire_sch.kicad_sch")
    sch = SCH.read_text(encoding="utf-8")

    if '(property "Reference" "R_F1"' in sch:
        print("R_F1 already present — abort to avoid duplex")
        return

    sch = sch.replace('(property "Reference" "U3"', '(property "Reference" "U_ESP1"', 1)
    sch = sch.replace('(reference "U3")', '(reference "U_ESP1")')

    # Strip prior dangling topology one-liners
    sch = re.sub(
        r'\n\t\(label "(?:VBOOST|GND|CELL32|CELL0|CHG\+|CHG-)" \(at [^)]+\) \(effects \(font \(size 1\.27 1\.27\)\) \(justify left\)\) \(uuid "[^"]+"\)\)',
        "",
        sch,
    )

    lib_text = CONN_LIB.read_text(encoding="utf-8")
    inserts = []
    for name in ("Conn_01x02", "Conn_01x04", "Conn_01x06", "Conn_01x08", "Conn_01x09", "Conn_01x10"):
        if f'Connector_Generic:{name}' not in sch:
            inserts.append(extract_conn(lib_text, name))
            print("embed", name)
    if inserts:
        m = re.search(
            r"\n\)\n\t\(symbol\n\t\t\(lib_id \"Battery_Management:BQ7695202PFB\"\)",
            sch,
        )
        if not m:
            raise SystemExit("lib_symbols end not found")
        sch = sch[: m.start()] + "\n" + "".join(inserts) + sch[m.start() :]

    out: list[str] = []

    def wl(net: str, x: float, y: float, rot: float) -> None:
        out.append(wire_label(net, x, y, rot))

    # --- Existing core: BQ / SSR / caps / FETs / gate parts ---
    for sx, sy, prefix, vc0, extra in (
        (149.86, 100.33, "BQ1", "CELL0", {"21": "TS1", "22": "TS2", "23": "TS3"}),
        (250.19, 100.33, "BQ2", "CELL16", {"21": "TS4"}),
    ):
        mp = bq_netmap(prefix, vc0)
        mp.update(extra)
        for p, net in mp.items():
            dx, dy, rot = BQ[p]
            wl(net, sx + dx, sy + dy, rot)

    for p, net in {
        "1": "PIN_CHG_EN",
        "2": "PIN_OUT_EN",
        "3": "PIN_PSW_EN",
        "4": "GND",
        "5": "VBOOST",
        "6": "CELL32",
        "7": "SSR_OUT_DSG",
        "8": "SSR_OUT_CHG",
    }.items():
        dx, dy, rot = SSR[p]
        wl(net, 155.0 + dx, 25.0 + dy, rot)

    for cx in (165.0, 175.0):
        x, y, r = rc_pin(cx, 25.0, 0, 1)
        wl("VBOOST", x, y, r)
        x, y, r = rc_pin(cx, 25.0, 0, 2)
        wl("GND", x, y, r)

    for qy, gnet, snet in ((45.0, "Q1_GATE", "CHG+"), (80.0, "Q2_GATE", "PACK+")):
        for p, net in (("1", gnet), ("D", "CELL32_FUSED"), ("2", snet)):
            dx, dy, rot = FET[p]
            wl(net, 195.0 + dx, qy + dy, rot)

    x, y, r = rc_pin(175.0, 45.0, 90, 1)
    wl("SSR_OUT_CHG", x, y, r)
    x, y, r = rc_pin(175.0, 45.0, 90, 2)
    wl("Q1_GATE", x, y, r)

    x, y, r = rc_pin(185.0, 35.0, 0, 1)
    wl("Q1_GATE", x, y, r)
    x, y, r = rc_pin(185.0, 35.0, 0, 2)
    wl("GND", x, y, r)

    x, y, r = rc_pin(185.0, 25.0, 0, 1)
    wl("Q1_GATE", x, y, r)
    x, y, r = rc_pin(185.0, 25.0, 0, 2)
    wl("CHG+", x, y, r)

    # --- R_F bank (grid-aligned), place then wire from known coords ---
    rf_base_x, rf_base_y = snap(25.4), snap(304.8)
    for k in range(1, 33):
        cell_n = 33 - k
        vc = f"BQ1_VC{cell_n}" if cell_n <= 16 else f"BQ2_VC{cell_n - 16}"
        col, row = (k - 1) % 16, (k - 1) // 16
        x = rf_base_x + col * 12.7
        y = rf_base_y + row * 25.4
        out.append(rc_symbol("Device:R", f"R_F{k}", "20R", "Resistor_SMD:R_0402_1005Metric", x, y, 0))
        ax, ay, ar = rc_pin(x, y, 0, 1)
        bx, by, br = rc_pin(x, y, 0, 2)
        wl(f"CELL{cell_n}", ax, ay, ar)
        wl(vc, bx, by, br)

    # --- C_F bank ---
    cf_base_x, cf_base_y = snap(25.4), snap(381.0)
    n = 1
    for prefix, vc0 in (("BQ1", "CELL0"), ("BQ2", "CELL16")):
        for vc in range(1, 17):
            net_a = f"{prefix}_VC{vc}"
            net_b = vc0 if vc == 1 else f"{prefix}_VC{vc - 1}"
            col, row = (n - 1) % 16, (n - 1) // 16
            x = cf_base_x + col * 12.7
            y = cf_base_y + row * 25.4
            out.append(rc_symbol("Device:C", f"C_F{n}", "0.22uF", "Capacitor_SMD:C_0402_1005Metric", x, y, 0))
            ax, ay, ar = rc_pin(x, y, 0, 1)
            bx, by, br = rc_pin(x, y, 0, 2)
            wl(net_a, ax, ay, ar)
            wl(net_b, bx, by, br)
            n += 1

    # --- Connectors ---
    connectors = [
        ("J_BAT1", 2, "XT30 BAT", "qfbms:XT30PW-M_Lugs", snap(508.0), snap(50.8), ["CELL32", "CELL0"]),
        ("J_CHG1", 2, "XT30 CHG", "qfbms:XT30PW-F_Lugs", snap(533.4), snap(50.8), ["CHG+", "CHG-"]),
        (
            "J_COMM1",
            4,
            "CAN/5V",
            "Connector_JST:JST_GH_BM04B-GHS-TBT_1x04-1MP_P1.25mm_Vertical",
            snap(508.0),
            snap(101.6),
            ["CANH", "CANL", "ISO_GND", "5VExt"],
        ),
    ]
    for i in range(1, 5):
        connectors.append(
            (
                f"J_T{i}",
                2,
                f"T{i}",
                "Connector_JST:JST_GH_BM02B-GHS-TBT_1x02-1MP_P1.25mm_Vertical",
                snap(508.0 + (i - 1) * 25.4),
                snap(152.4),
                [f"TS{i}", "GND"],
            )
        )
    cell_maps = [
        ("J_CELL4", 6, list(range(32, 26, -1)), "Connector_JST:JST_GH_BM06B-GHS-TBT_1x06-1MP_P1.25mm_Vertical"),
        ("J_CELL3", 8, list(range(26, 18, -1)), "Connector_JST:JST_GH_BM08B-GHS-TBT_1x08-1MP_P1.25mm_Vertical"),
        ("J_CELL2", 9, list(range(18, 9, -1)), "Connector_JST:JST_GH_BM09B-GHS-TBT_1x09-1MP_P1.25mm_Vertical"),
        ("J_CELL1", 10, list(range(9, -1, -1)), "Connector_JST:JST_GH_BM10B-GHS-TBT_1x10-1MP_P1.25mm_Vertical"),
    ]
    x0 = snap(508.0)
    for ref, n, cells, fp in cell_maps:
        connectors.append((ref, n, ref, fp, x0, snap(228.6), [f"CELL{c}" for c in cells]))
        x0 = snap(x0 + 38.1)

    for ref, n, value, fp, x, y, nets in connectors:
        out.append(conn_symbol(n, ref, value, fp, x, y))
        for (_, py), net in zip(conn_pins(n), nets):
            wl(net, x - 5.08, y + py, 0)

    # Power stage discretes
    for ref, val, fp, x, y, rot, nets in (
        ("F1", "15A", "Fuse:Fuse_2512_6332Metric", snap(457.2), snap(50.8), 0, ("CELL32", "CELL32_FUSED")),
        ("R_SH1", "R001", "Resistor_SMD:R_2512_6332Metric", snap(457.2), snap(76.2), 0, ("CELL0", "SHUNT_MID")),
        ("R_SH2", "R001", "Resistor_SMD:R_2512_6332Metric", snap(457.2), snap(101.6), 0, ("SHUNT_MID", "CHG-")),
        ("R_SSR1", "01X", "Resistor_SMD:R_0603_1608Metric", snap(457.2), snap(127.0), 90, ("SSR_OUT_CHG", "Q1_GATE")),
    ):
        out.append(rc_symbol("Device:R", ref, val, fp, x, y, rot))
        ax, ay, ar = rc_pin(x, y, rot, 1)
        bx, by, br = rc_pin(x, y, rot, 2)
        wl(nets[0], ax, ay, ar)
        wl(nets[1], bx, by, br)

    payload = "\n" + "".join(out) + "\n"
    insert_at = sch.rfind("\n\t(sheet_instances")
    if insert_at < 0:
        insert_at = sch.rfind("\n)")
    sch = sch[:insert_at] + payload + sch[insert_at:]
    SCH.write_text(sch, encoding="utf-8")
    print(f"Wrote {SCH}; elements≈{len(out)}")


if __name__ == "__main__":
    main()
