import re

with open(r'c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

esp_def = re.search(r'\(symbol "MCU_Espressif:ESP32-C3"[\s\S]*?\n\t\t\)', text)
if esp_def:
    pins = re.findall(r'\(pin\s+\w+\s+\w+\s+\(at\s+([-\d.]+)\s+([-\d.]+)\s+(\d+)\)[\s\S]*?\(name "([^"]+)"[\s\S]*?\(number "(\d+)"', esp_def.group(0))
    for x, y, rot, name, num in pins:
        print(f'Pin {num:2s} ({name:15s}): offset ({float(x):6.2f}, {float(y):6.2f}) rot={rot}')
