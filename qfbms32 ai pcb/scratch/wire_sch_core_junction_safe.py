"""
Junction-safe schematic wiring for BQ / SSR / FET core.

1) Move power-stage + CHG clutter clear of BQ pin fields
2) Stub-wire BQ VC/sense/temp/I2C + SSR/FET/gate nets with short stubs
3) no_connect unused BQ FET-driver / REG pins (PCB leaves them unnetted)

Does not touch R_F/C_F/connector banks (x>=440 or y>=280).

IMPORTANT: KiCad symbol files use +Y up; the schematic sheet uses +Y down.
For a symbol instance at (sx,sy) with rotation 0:
  world = (sx + local_x, sy - local_y)
Pin angles 0/180 stay left/right; 90/270 stub directions still match outward.
"""
from __future__ import annotations

import re
import shutil
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCH = ROOT / "qfbms32.kicad_sch"
HIST = ROOT / ".history"
G = 1.27
STUB = 2.54  # one pin-pitch — cannot reach neighbor pin tips


def uid() -> str:
    return str(uuid.uuid4())


def snap(v: float) -> float:
    return round(v / G) * G


def pin_world(sx: float, sy: float, dx: float, dy: float, srot: float = 0) -> tuple[float, float]:
    """Map symbol-local pin (dx,dy) (+Y up) to schematic sheet coords (+Y down)."""
    srot = int(srot) % 360
    # local (+Y up) → sheet (+Y down) then apply instance rotation about origin
    lx, ly = dx, -dy
    if srot == 0:
        return sx + lx, sy + ly
    if srot == 90:
        # CW: (x,y) -> (y, -x) in sheet space
        return sx + ly, sy - lx
    if srot == 180:
        return sx - lx, sy - ly
    # 270 CW
    return sx - ly, sy + lx


# Relative pin tips from symbol origin (from embedded lib symbols) — local +Y up
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
    "24": (20.32, -7.62, 180),
    "26": (20.32, -20.32, 180),
    "27": (20.32, -17.78, 180),
    "33": (-20.32, -22.86, 0),
    "34": (20.32, -5.08, 180),
    "35": (20.32, -2.54, 180),
    "36": (20.32, 0.0, 180),
    "37": (20.32, 5.08, 180),
    "39": (20.32, 12.7, 180),
    "40": (20.32, 10.16, 180),
    "41": (20.32, 17.78, 180),
    "42": (20.32, 22.86, 180),
    "43": (20.32, 27.94, 180),
    "45": (20.32, 30.48, 180),
    "46": (20.32, 40.64, 180),
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
RC = {1: (0.0, 3.81), 2: (0.0, -3.81)}  # Device:R / Device:C at rot 0


def rc_pin(sx: float, sy: float, srot: float, pin: int) -> tuple[float, float, float]:
    """Device:R/C/D pin tip. Local coords +Y up; pin1 at +3.81 faces 'up' in symbol."""
    px, py = RC[pin]
    ax, ay = pin_world(sx, sy, px, py, srot)
    # Outward stub angle on the sheet after Y-flip + instance rot
    srot = int(srot) % 360
    # local pin1 faces 270° in symbol editor? Stock Device:R pin1 (at 0 3.81 270) faces up (+local Y).
    # After Y-flip to sheet: faces up on screen = 270 in sch (toward -Y).
    local_facing = 270.0 if pin == 1 else 90.0
    # Rotate facing by instance orientation (CW)
    facing = (local_facing + srot) % 360
    return ax, ay, facing


def diode_pins(sx: float, sy: float, srot: float = 0) -> dict[str, tuple[float, float, float]]:
    # Device:D / D_Zener / D_Schottky: same geometry as R/C for pin tips
    a = rc_pin(sx, sy, srot, 1)
    c = rc_pin(sx, sy, srot, 2)
    return {"1": a, "2": c}


def stub_end(x0: float, y0: float, pin_rot: float, length: float = STUB) -> tuple[float, float, float, str]:
    pr = int(pin_rot) % 360
    if pr == 0:
        return x0 - length, y0, 180.0, "right bottom"
    if pr == 180:
        return x0 + length, y0, 0.0, "left bottom"
    if pr == 90:
        return x0, y0 + length, 90.0, "left bottom"
    return x0, y0 - length, 270.0, "left bottom"


def wire_label(net: str, x0: float, y0: float, pin_rot: float, length: float = STUB) -> str:
    x1, y1, lrot, just = stub_end(x0, y0, pin_rot, length)
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


def find_symbol_span(sch: str, ref: str) -> tuple[int, int] | None:
    """Return [start, end) of the instance symbol block containing Reference ref."""
    # KiCad 10 uses both "(symbol\\n\\t\\t(lib_id" and "(symbol (lib_id"
    for m in re.finditer(r"\n\t\(symbol[\s\n]+\(lib_id ", sch):
        start = m.start() + 1  # at '(symbol'
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
        if end is None:
            continue
        block = sch[start:end]
        if re.search(rf'\(property "Reference" "{re.escape(ref)}"', block):
            return start, end
    return None


def set_symbol_at(sch: str, ref: str, x: float, y: float, rot: float = 0) -> str:
    span = find_symbol_span(sch, ref)
    if not span:
        raise SystemExit(f"missing symbol {ref}")
    start, end = span
    block = sch[start:end]
    block2, n = re.subn(
        r"\(at [0-9.-]+ [0-9.-]+ [0-9.-]+\)",
        f"(at {x:.2f} {y:.2f} {rot:g})",
        block,
        count=1,
    )
    if n != 1:
        raise SystemExit(f"failed to rewrite at for {ref}")
    # Nudge Reference/Value property positions roughly with the symbol
    # (optional — leave property ats; KiCad will still show them)
    return sch[:start] + block2 + sch[end:]


def get_symbol_at(sch: str, ref: str) -> tuple[float, float, float]:
    span = find_symbol_span(sch, ref)
    if not span:
        raise SystemExit(f"missing symbol {ref}")
    block = sch[span[0] : span[1]]
    m = re.search(r"\(at ([0-9.-]+) ([0-9.-]+) ([0-9.-]+)\)", block)
    if not m:
        raise SystemExit(f"no at for {ref}")
    return float(m.group(1)), float(m.group(2)), float(m.group(3))


def bq_netmap(prefix: str, vc0: str, ts: dict[str, str]) -> dict[str, str]:
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
    m = {
        pin_for_vc[0]: vc0,
        "17": "GND",
        "18": "SRP",
        "20": "SRN",
        "47": f"{prefix}_VC16",
        "26": "I2C_SCL",
        "27": "I2C_SDA",
        "33": "GND",  # RST_SHUT pulldown when unused (FW TODO)
    }
    for vc in range(1, 17):
        m[pin_for_vc[vc]] = f"{prefix}_VC{vc}"
    m.update(ts)
    return m


# BQ right-side / unused driver pins → no_connect (match PCB: unnetted)
BQ_NC_PINS = ["24", "34", "35", "36", "37", "39", "40", "41", "42", "43", "45", "46"]


def main() -> None:
    HIST.mkdir(exist_ok=True)
    shutil.copy2(SCH, HIST / "qfbms32_pre_core_wire.kicad_sch")
    sch = SCH.read_text(encoding="utf-8")

    # --- 1) Relocate power / CHG clutter clear of BQ bodies ---
    # BQ1 ~(130-170, 55-146), BQ2 ~(230-270, 55-146)
    # Park power stage at x~330+, y~25..120
    moves = {
        "U_SSR1": (snap(330.2), snap(38.1), 0),
        "C_SSR1": (snap(355.6), snap(38.1), 0),
        "C_SSR2": (snap(368.3), snap(38.1), 0),
        # Keep D_GS1 / R_SSR2 stubs from overlapping on the same vertical (was shorting Q1_GATE↔CHG+)
        "D_GS1": (snap(381.0), snap(38.1), 0),
        "R_SSR2": (snap(406.4), snap(38.1), 0),
        "Q1": (snap(330.2), snap(76.2), 0),
        "R_G1": (snap(355.6), snap(76.2), 90),
        "Q2": (snap(330.2), snap(114.3), 0),
        "R_G2": (snap(355.6), snap(114.3), 90),
        # Charge helper clutter that sat on BQ pin fields
        "R_CHG1": (snap(330.2), snap(152.4), 0),
        "D_CHG1": (snap(355.6), snap(152.4), 0),
        "D_CHG2": (snap(368.3), snap(152.4), 0),
        "D_CHG3": (snap(381.0), snap(152.4), 0),
        "C_FLT1": (snap(393.7), snap(152.4), 0),
        "R_B33": (snap(406.4), snap(152.4), 0),
    }
    for ref, (x, y, rot) in moves.items():
        if find_symbol_span(sch, ref):
            sch = set_symbol_at(sch, ref, x, y, rot)
            print(f"move {ref} -> ({x:.2f},{y:.2f}) rot={rot}")
        else:
            print(f"skip missing {ref}")

    # --- 2) Strip any leftover wire+label in core that we may re-emit ---
    # Keep banks (y>=280 or x>=440) and keep ESP/CAN region (x<100) labels already there.
    def drop_core_pair(m: re.Match) -> str:
        x0, y0 = float(m.group(1)), float(m.group(2))
        if y0 >= 280 or x0 >= 440 or x0 < 100:
            return m.group(0)
        # Also keep anything already far right in new power zone? We'll re-wire power zone.
        return ""

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
        drop_core_pair,
        sch,
    )
    # Strip prior no_connects in BQ pin fields (we'll re-add)
    sch = re.sub(
        r'\n\t\(no_connect \(at ([0-9.-]+) ([0-9.-]+)\) \(uuid "[^"]+"\)\)',
        lambda m: ""
        if (120 <= float(m.group(1)) <= 280 and 50 <= float(m.group(2)) <= 160)
        else m.group(0),
        sch,
    )

    # --- 3) Build pin occupancy set for collision checks ---
    occupied: list[tuple[float, float, str]] = []

    def add_occ(x: float, y: float, tag: str) -> None:
        occupied.append((x, y, tag))

    # Known fixed symbols we don't move
    for ref, pins in (
        ("U_BQ1", BQ),
        ("U_BQ2", BQ),
    ):
        sx, sy, srot = get_symbol_at(sch, ref)
        for p, (dx, dy, _) in pins.items():
            x, y = pin_world(sx, sy, dx, dy, srot)
            add_occ(x, y, f"{ref}.{p}")

    for ref, dxmap in (("U_SSR1", SSR), ("Q1", FET), ("Q2", FET)):
        sx, sy, srot = get_symbol_at(sch, ref)
        for p, (dx, dy, _) in dxmap.items():
            x, y = pin_world(sx, sy, dx, dy, srot)
            add_occ(x, y, f"{ref}.{p}")

    for ref in ("C_SSR1", "C_SSR2", "R_SSR2", "R_G1", "R_G2", "R_CHG1", "C_FLT1", "R_B33"):
        if not find_symbol_span(sch, ref):
            continue
        sx, sy, srot = get_symbol_at(sch, ref)
        for pin in (1, 2):
            x, y, _ = rc_pin(sx, sy, srot, pin)
            add_occ(x, y, f"{ref}.{pin}")

    for ref in ("D_GS1", "D_CHG1", "D_CHG2", "D_CHG3"):
        if not find_symbol_span(sch, ref):
            continue
        sx, sy, srot = get_symbol_at(sch, ref)
        for p, (x, y, _) in diode_pins(sx, sy, srot).items():
            add_occ(x, y, f"{ref}.{p}")

    def clear_stub(x0: float, y0: float, pin_rot: float, tag: str) -> float:
        """Return stub length that doesn't land on another pin (try 2.54 then 3.81 then 5.08)."""
        for length in (2.54, 3.81, 5.08, 7.62):
            x1, y1, _, _ = stub_end(x0, y0, pin_rot, length)
            ok = True
            for ox, oy, ot in occupied:
                if ot == tag:
                    continue
                if (ox - x1) ** 2 + (oy - y1) ** 2 < (0.6**2):
                    ok = False
                    break
                # also avoid landing on foreign pin tip mid-segment? short stubs OK
            if ok:
                return length
        return 2.54  # last resort

    out: list[str] = []
    collisions = 0

    def emit(net: str, x0: float, y0: float, pin_rot: float, tag: str) -> None:
        nonlocal collisions
        length = clear_stub(x0, y0, pin_rot, tag)
        x1, y1, _, _ = stub_end(x0, y0, pin_rot, length)
        for ox, oy, ot in occupied:
            if ot == tag:
                continue
            if (ox - x1) ** 2 + (oy - y1) ** 2 < (0.6**2):
                collisions += 1
                print(f"  WARN stub {tag} {net} collides with {ot}")
        out.append(wire_label(net, x0, y0, pin_rot, length))
        add_occ(x1, y1, f"lbl:{net}@{tag}")

    # --- 4) Wire BQs ---
    for ref, prefix, vc0, ts in (
        ("U_BQ1", "BQ1", "CELL0", {"21": "TS1", "22": "TS2", "23": "TS3"}),
        ("U_BQ2", "BQ2", "CELL16", {"21": "TS4"}),
    ):
        sx, sy, srot = get_symbol_at(sch, ref)
        mp = bq_netmap(prefix, vc0, ts)
        for p, net in mp.items():
            dx, dy, rot = BQ[p]
            x, y = pin_world(sx, sy, dx, dy, srot)
            emit(net, x, y, rot, f"{ref}.{p}")
        for p in BQ_NC_PINS:
            dx, dy, _ = BQ[p]
            x, y = pin_world(sx, sy, dx, dy, srot)
            out.append(no_connect(x, y))

    # --- 5) Wire SSR + caps + FETs + gate network ---
    sx, sy, srot = get_symbol_at(sch, "U_SSR1")
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
        x, y = pin_world(sx, sy, dx, dy, srot)
        emit(net, x, y, rot, f"U_SSR1.{p}")

    for ref in ("C_SSR1", "C_SSR2"):
        sx, sy, srot = get_symbol_at(sch, ref)
        x, y, r = rc_pin(sx, sy, srot, 1)
        emit("VBOOST", x, y, r, f"{ref}.1")
        x, y, r = rc_pin(sx, sy, srot, 2)
        emit("GND", x, y, r, f"{ref}.2")

    # Q1 CHG FET
    sx, sy, srot = get_symbol_at(sch, "Q1")
    for p, net in (("1", "Q1_GATE"), ("D", "CELL32_FUSED"), ("2", "CHG+")):
        dx, dy, rot = FET[p]
        x, y = pin_world(sx, sy, dx, dy, srot)
        emit(net, x, y, rot, f"Q1.{p}")

    # Q2 DSG / pack-path FET
    sx, sy, srot = get_symbol_at(sch, "Q2")
    for p, net in (("1", "Q2_GATE"), ("D", "CELL32_FUSED"), ("2", "PACK+")):
        dx, dy, rot = FET[p]
        x, y = pin_world(sx, sy, dx, dy, srot)
        emit(net, x, y, rot, f"Q2.{p}")

    # R_G1: SSR_OUT_CHG — Q1_GATE
    sx, sy, srot = get_symbol_at(sch, "R_G1")
    x, y, r = rc_pin(sx, sy, srot, 1)
    emit("SSR_OUT_CHG", x, y, r, "R_G1.1")
    x, y, r = rc_pin(sx, sy, srot, 2)
    emit("Q1_GATE", x, y, r, "R_G1.2")

    # R_G2: SSR_OUT_DSG — Q2_GATE
    sx, sy, srot = get_symbol_at(sch, "R_G2")
    x, y, r = rc_pin(sx, sy, srot, 1)
    emit("SSR_OUT_DSG", x, y, r, "R_G2.1")
    x, y, r = rc_pin(sx, sy, srot, 2)
    emit("Q2_GATE", x, y, r, "R_G2.2")

    # R_SSR2: Q1_GATE — GND
    sx, sy, srot = get_symbol_at(sch, "R_SSR2")
    x, y, r = rc_pin(sx, sy, srot, 1)
    emit("Q1_GATE", x, y, r, "R_SSR2.1")
    x, y, r = rc_pin(sx, sy, srot, 2)
    emit("GND", x, y, r, "R_SSR2.2")

    # D_GS1 zener: pad1~anode Q1_GATE, pad2~cathode CHG+ (matches PCB apply script)
    sx, sy, srot = get_symbol_at(sch, "D_GS1")
    dp = diode_pins(sx, sy, srot)
    emit("Q1_GATE", *dp["1"][:2], dp["1"][2], "D_GS1.1")
    emit("CHG+", *dp["2"][:2], dp["2"][2], "D_GS1.2")

    # --- 6) ESP: add missing I2C_SCL label if GPIO pin exists; note DIV nets placeholder ---
    # Chip symbol lacks GPIO4/5/6/7/20/21 — only ensure I2C_SDA already present; add SCL
    # on a dedicated free label near ESP for netlist presence (not attached to wrong pin).
    # Skip attaching SCL to a wrong pin; leave as documentation global-ish local label free? 
    # Better: attach to nothing creates dangling — skip until MINI-1 symbol.

    payload = "\n" + "".join(out) + "\n"
    insert_at = sch.rfind("\n\t(sheet_instances")
    if insert_at < 0:
        insert_at = sch.rfind("\n)")
    sch = sch[:insert_at] + payload + sch[insert_at:]
    SCH.write_text(sch, encoding="utf-8")
    n_lbl = len(re.findall(r"\(label ", sch))
    print(f"Wrote {SCH}")
    print(f"emitted chunks={len(out)} collision_warns={collisions}")
    print(f"wires now={sch.count('(wire')} labels={n_lbl}")


if __name__ == "__main__":
    main()
