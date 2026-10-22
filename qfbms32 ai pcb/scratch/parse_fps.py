with open('VFBMS32.kicad_pcb', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def parse_footprints(lines):
    footprints = {}
    current_fp = None
    depth = 0
    fp_lines = []
    for line in lines:
        if '(footprint ' in line:
            depth = 1
            fp_lines = [line]
        elif depth > 0:
            fp_lines.append(line)
            depth += line.count('(') - line.count(')')
            if depth == 0:
                # parsed one footprint
                fp_text = "".join(fp_lines)
                import re
                ref_m = re.search(r'\(property "Reference" "([^"]+)"', fp_text)
                val_m = re.search(r'\(property "Value" "([^"]+)"', fp_text)
                fp_name_m = re.search(r'\(footprint "([^"]+)"', fp_lines[0])
                at_m = re.search(r'\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)(?:\s+([0-9\.\-]+))?\)', fp_text)
                models = re.findall(r'\(model\s+"([^"]+)"', fp_text)
                if ref_m:
                    ref = ref_m.group(1)
                    footprints[ref] = {
                        'val': val_m.group(1) if val_m else '',
                        'fp': fp_name_m.group(1) if fp_name_m else '',
                        'at': at_m.groups() if at_m else (),
                        'models': models
                    }
    return footprints

fps = parse_footprints(lines)
for ref in ['L1', 'L2', 'U7', 'U_ESP1', 'J_USB1', 'U_SSR1', 'U_BQ1', 'U_BQ2']:
    if ref in fps:
        print(f"Ref: {ref:<10} | Val: {fps[ref]['val']:<15} | Pos: {fps[ref]['at']} | FP: {fps[ref]['fp']}")
        print(f"     3D Models: {fps[ref]['models']}")
    else:
        print(f"Ref: {ref:<10} | NOT FOUND")
