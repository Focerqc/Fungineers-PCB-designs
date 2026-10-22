import os
import re

fw_dump_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\firmware_dump"

print("=" * 80)
print("INVESTIGATING hw_vbms32.h:")
print("=" * 80)
hw_h_path = os.path.join(fw_dump_dir, "hw_vbms32.h")
if os.path.exists(hw_h_path):
    with open(hw_h_path, "r", encoding="utf-8", errors="ignore") as f:
        hw_h = f.read()
    print(hw_h)

print("\n" + "=" * 80)
print("SEARCHING hw_vbms32.c FOR PINS, FETS, CHG, DSG:")
print("=" * 80)
hw_c_path = os.path.join(fw_dump_dir, "hw_vbms32.c")
if os.path.exists(hw_c_path):
    with open(hw_c_path, "r", encoding="utf-8", errors="ignore") as f:
        hw_c = f.read()
    
    # Search for all GPIO definitions, pinMode, gpio_set_level, etc.
    lines = hw_c.splitlines()
    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in ["gpio", "pin", "fet", "chg", "dsg", "gate", "drv", "bq", "toll"]):
            print(f"L{i+1:4}: {line}")

print("\n" + "=" * 80)
print("SEARCHING vbms32_conf_default.h:")
print("=" * 80)
conf_path = os.path.join(fw_dump_dir, "vbms32_conf_default.h")
if os.path.exists(conf_path):
    with open(conf_path, "r", encoding="utf-8", errors="ignore") as f:
        print(f.read())
