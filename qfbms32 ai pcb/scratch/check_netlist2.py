import re
from pathlib import Path
import subprocess

out = Path("qfbms32 ai pcb/scratch/netlist_test.net")
subprocess.run(
    [
        r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe",
        "sch",
        "export",
        "netlist",
        "--format",
        "kicadsexpr",
        "-o",
        str(out),
        r"qfbms32 ai pcb\qfbms32.kicad_sch",
    ],
    check=False,
)
t = out.read_text(encoding="utf-8")

def nodes_for(name: str):
    # match (name "/NAME") or (name "NAME")
    pat = rf'\(name "(?:/{re.escape(name)}|{re.escape(name)})"\)([\s\S]*?)(?=\n\t\t\(net|\n\t\))'
    m = re.search(pat, t)
    if not m:
        return None
    return re.findall(r'\(ref "([^"]+)"\)\s*\(pin "([^"]+)"\)', m.group(1))

for n in ["BQ1_VC1", "BQ1_VC2", "CELL0", "CELL32", "VBOOST", "CHG+", "SSR_OUT_CHG", "Q1_GATE"]:
    nodes = nodes_for(n)
    if nodes is None:
        print(n, "MISSING")
    else:
        print(n, f"{len(nodes)} nodes", nodes[:8])

# Count unconnected U_BQ1 VC
unc = re.findall(r'unconnected-\(U_BQ1-VC(\d+)', t)
print("unconnected U_BQ1 VCs", sorted(unc, key=int))
unc2 = re.findall(r'unconnected-\(U_BQ2-VC(\d+)', t)
print("unconnected U_BQ2 VCs", sorted(unc2, key=int))
