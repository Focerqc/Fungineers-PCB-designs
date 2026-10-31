"""Audit pad nets vs wiring diagram and BQ76952 pin functions."""
import pcbnew
from collections import defaultdict

PCB = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\qfbms32 ai pcb\qfbms32.kicad_pcb"
board = pcbnew.LoadBoard(PCB)

# BQ76952 TQFP-48 pin functions (TI DS, PFB/TQFP numbering used on this board)
BQ_PINS = {
    "1": "VC5", "2": "VC4", "3": "VC3", "4": "VC2", "5": "VC1", "6": "VC0",
    "7": "VC6", "8": "VC7", "9": "VC8", "10": "VC9", "11": "VC10", "12": "VC11",
    "13": "VC12", "14": "VC13", "15": "VC14", "16": "VC15",
    "17": "VSS", "18": "SRP", "19": "SRN", "20": "TS1", "21": "TS2", "22": "TS3",
    "23": "ALERT", "24": "SCL", "25": "SDA", "26": "CFETOFF", "27": "DFETOFF",
    "28": "DCHG", "29": "DDSG", "30": "RST_SHUT", "31": "REG1", "32": "REG2",
    "33": "REGIN", "34": "BREG", "35": "LD", "36": "PACK", "37": "PCHG",
    "38": "PDSG", "39": "CHG", "40": "DSG", "41": "FUSE", "42": "BAT",
    "43": "VC16", "44": "VC15B", "45": "RSVD", "46": "RSVD", "47": "CAP1", "48": "CAP2",
}
# The apply script used a DIFFERENT map. Print both so we can see which the board uses.
SCRIPT_MAP = {
    "15": "VC1", "14": "VC2", "13": "VC3", "12": "VC4", "11": "VC5", "10": "VC6",
    "9": "VC7", "8": "VC8", "7": "VC9", "6": "VC10", "5": "VC11", "4": "VC12",
    "3": "VC13", "2": "VC14", "1": "VC15", "16": "VC0", "48": "VC16",
    "17": "VSS", "47": "BAT", "45": "CHG", "43": "DSG", "42": "PACK", "40": "PCHG",
    "18": "SRP", "20": "SRN", "21": "TS1", "22": "TS2", "23": "TS3",
    "35": "REG1", "24": "REG18", "36": "REGIN",
}

fps = {fp.GetReference(): fp for fp in board.GetFootprints()}
print("FOOTPRINTS", len(fps))

def pad_net(ref, num):
    fp = fps.get(ref)
    if not fp:
        return "MISSING_FP"
    pad = fp.FindPadByNumber(str(num))
    if not pad:
        return "MISSING_PAD"
    name = pad.GetNetname()
    return name if name else "(none)"

def dump(ref):
    fp = fps.get(ref)
    if not fp:
        print(f"\n{ref}: MISSING")
        return
    pads = []
    for p in fp.Pads():
        n = p.GetNetname() or "(none)"
        pads.append(f"{p.GetNumber()}={n}")
    print(f"\n{ref}  {fp.GetValue()}  side={'B' if fp.GetLayer()==pcbnew.B_Cu else 'F'}")
    print("  " + ", ".join(pads))

for ref in [
    "J_BAT1", "J_CHG1", "J_COMM1", "J_T1", "J_T2", "J_T3", "J_T4",
    "J_CELL1", "J_CELL2", "J_CELL3", "J_CELL4",
    "U_BQ1", "U_BQ2", "U_SSR1", "U_ESP1", "U4", "U7",
    "Q1", "Q2", "F1", "R_SH1", "R_SH2", "R_SSR1", "R_SSR2",
    "C_SSR1", "C_SSR2", "R_G1", "R_GS1", "D_GS1",
]:
    dump(ref)

print("\n=== R_F sample ===")
for k in (1, 2, 16, 17, 32):
    dump(f"R_F{k}")

print("\n=== C_F sample ===")
for k in (1, 2, 16, 17, 32):
    dump(f"C_F{k}")

print("\n=== R_B sample ===")
for k in (1, 16, 33):
    dump(f"R_B{k}")

# net occupancy
pads_by_net = defaultdict(list)
none_pads = 0
total_pads = 0
for fp in board.GetFootprints():
    for p in fp.Pads():
        total_pads += 1
        name = p.GetNetname()
        if not name:
            none_pads += 1
        else:
            pads_by_net[name].append(f"{fp.GetReference()}.{p.GetNumber()}")

print(f"\nPADS {total_pads}  unnetted {none_pads}  named nets with pads {len(pads_by_net)}")

# copper: tracks/vias per net
trk = defaultdict(int)
for t in board.GetTracks():
    trk[t.GetNetname() or "(none)"] += 1
print(f"TRACK+VIA items {sum(trk.values())}")

print("\n=== nets with >1 pad, and whether any copper exists ===")
multi = []
for name, pads in sorted(pads_by_net.items(), key=lambda kv: -len(kv[1])):
    if len(pads) < 2:
        continue
    multi.append(name)
    copper = trk.get(name, 0)
    flag = "COPPER" if copper else "RATSNEST-ONLY"
    print(f"  {flag:14} pads={len(pads):3} tracks={copper:3}  {name}")

print(f"\nmulti-pad nets {len(multi)}  of which copper {sum(1 for n in multi if trk.get(n,0))}")

# BQ pin coverage vs TI names — report actual net on each pad
print("\n=== U_BQ1 / U_BQ2 every pad ===")
for ref in ("U_BQ1", "U_BQ2"):
    fp = fps[ref]
    print(ref, "pads", fp.GetPadCount())
    for p in sorted(fp.Pads(), key=lambda p: int(p.GetNumber()) if str(p.GetNumber()).isdigit() else 99):
        num = p.GetNumber()
        netn = p.GetNetname() or "(none)"
        ti = BQ_PINS.get(str(num), "?")
        print(f"  pad {num:>3}  TI={ti:8}  net={netn}")
