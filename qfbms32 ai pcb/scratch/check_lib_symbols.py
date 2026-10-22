with open('VFBMS32.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

import re
lib_symbols = re.findall(r'\(symbol\s+"([^"]+)"', text[:text.find('(symbol (lib_id')])
print("lib_symbols in sch:", lib_symbols)
