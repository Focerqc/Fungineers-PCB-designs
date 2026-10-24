import re

with open('qfbms32.kicad_pcb', 'r', encoding='utf-8') as f:
    pcb = f.read()

# Let's find net definitions
net_matches = re.findall(r'\(net\s+(\d+)\s+"([^"]+)"\)', pcb)
net_map = {int(n): name for n, name in net_matches}

# Let's inspect traces near (28-31, 0-4)
segment_matches = re.findall(
    r'\(segment\s+\(start\s+([\d\.-]+)\s+([\d\.-]+)\)\s+\(end\s+([\d\.-]+)\s+([\d\.-]+)\)\s+\(width\s+[\d\.-]+\)\s+\(layer\s+"([^"]+)"\)\s+\(net\s+(\d+)\)',
    pcb
)

print(f"Traces near (28-31, 0-4):")
seen_nets = set()
for x1, y1, x2, y2, layer, net in segment_matches:
    x1, y1, x2, y2, net = float(x1), float(y1), float(x2), float(y2), int(net)
    if (26 <= x1 <= 32 and 0 <= y1 <= 5) or (26 <= x2 <= 32 and 0 <= y2 <= 5):
        net_name = net_map.get(net, f"Net {net}")
        seen_nets.add(net_name)
        print(f"  {layer:10} ({x1:5.2f}, {y1:5.2f}) -> ({x2:5.2f}, {y2:5.2f})  Net: {net_name}")

print("\nUnique nets in this region:", seen_nets)
