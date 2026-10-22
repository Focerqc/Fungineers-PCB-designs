with open('VFBMS32.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find MCU_Espressif:ESP32-C3 symbol instance and symbol definition
import re
m = re.search(r'\(symbol\s+\(lib_id "MCU_Espressif:ESP32-C3"\)[\s\S]*?\n\t\)', text)
if m:
    print("ESP32 Instance:")
    print(m.group(0))

# Also find symbol definition in lib_symbols
pos = text.find('(symbol "MCU_Espressif:ESP32-C3"')
if pos != -1:
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
    print("\nESP32 Symbol Definition (pins):")
    sym_def = text[pos:end_pos]
    for p in re.finditer(r'\(pin\s+\w+\s+\w+\s+\(at\s+([0-9\.\-]+)\s+([0-9\.\-]+)[^\)]*\)[\s\S]*?\(name\s+"([^"]+)"[\s\S]*?\(number\s+"([^"]+)"', sym_def):
        print(f"Pin {p.group(4):<4}: {p.group(3):<15} at ({p.group(1)}, {p.group(2)})")
