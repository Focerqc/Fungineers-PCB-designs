import re

with open(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

start = text.find('(symbol "MCU_Espressif:ESP32-C3"')
end = text.find('(symbol "Regulator_Switching:TPS62130"')
sym_text = text[start:end]

pins = re.findall(r'\(pin\s+\w+\s+\w+\s+\(at\s+([-\d.]+)\s+([-\d.]+)\s+([-\d.]+)\)[\s\S]*?\(name\s+\"([^\"]+)\"[\s\S]*?\(number\s+\"([^\"]+)\"', sym_text)
for p in sorted(pins, key=lambda x: int(x[4]) if x[4].isdigit() else 99):
    print(f"Pin {p[4]:2}: {p[3]:15} at ({p[0]}, {p[1]}, rot={p[2]})")
