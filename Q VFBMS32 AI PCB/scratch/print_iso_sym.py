import re

sym_file = r'C:\Program Files\KiCad\10.0\share\kicad\symbols\Interface_CAN_LIN.kicad_sym'
with open(sym_file, 'r', encoding='utf-8') as f:
    text = f.read()

# Find (symbol "ISO1050DUB" ... )
pos = text.find('(symbol "ISO1050DUB"')
if pos != -1:
    # balance parentheses
    depth = 0
    end_pos = pos
    for i in range(pos, len(text)):
        if text[i] == '(':
            depth += 1
        elif text[i] == ')':
            depth -= 1
            if depth == 0:
                end_pos = i + 1
                break
    sym_def = text[pos:end_pos]
    print(sym_def)
