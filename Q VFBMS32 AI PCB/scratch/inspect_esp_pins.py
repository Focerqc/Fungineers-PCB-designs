import re

with open(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

# Find ESP32 symbol definition in lib_symbols
esp_sym_m = re.search(r'\(symbol\s+\"MCU_Espressif:ESP32-C3\"[\s\S]*?\n\t\t\)', text)
if esp_sym_m:
    esp_sym_text = esp_sym_m.group(0)
    pins = re.findall(r'\(pin\s+(\w+)\s+(\w+)\s+\(at\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\)\s+\(length\s+[-\d.]+\)\s+\(name\s+\"([^\"]+)\"[\s\S]*?\(number\s+\"([^\"]+)\"', esp_sym_text)
    print("ESP32 pins:")
    for ptype, pshape, x, y, rot, name, num in sorted(pins, key=lambda x: int(x[6]) if x[6].isdigit() else 99):
        print(f"  Pin {num:2}: {name:15} at rel ({x}, {y})")
