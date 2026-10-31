import re
from pathlib import Path

net_path = Path("qfbms32 ai pcb/scratch/netlist_test.net")
if not net_path.exists():
    print("netlist missing")
else:
    t = net_path.read_text(encoding="utf-8")
    print("size", len(t))
    # split nets
    nets = re.findall(
        r'\(net \(code "?(\d+)"?\) \(name "([^"]+)"\)([\s\S]*?)(?=\n\t\(net |\n\))',
        t,
    )
    print("nets", len(nets))
    wanted = ["BQ1_VC1", "BQ1_VC2", "CELL0", "BQ1_VC16", "GND", "CELL32", "BQ1_VC7", "VBOOST"]
    by_name = {n: body for _, n, body in nets}
    for w in wanted:
        body = by_name.get(w)
        if not body:
            print(w, "MISSING")
            continue
        nodes = re.findall(r'\(node \(ref "([^"]+)"\) \(pin "([^"]+)"\)', body)
        print(w, nodes, "count", len(nodes))
