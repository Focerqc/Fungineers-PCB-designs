import os

fw_dump_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\firmware_dump"

print("=" * 80)
print("CONTENTS OF hw_vbms32.h:")
print("=" * 80)
with open(os.path.join(fw_dump_dir, "hw_vbms32.h"), "r") as f:
    print(f.read())

print("=" * 80)
print("PIN DEFINITIONS & FET CONTROL IN hw_vbms32.c:")
print("=" * 80)
with open(os.path.join(fw_dump_dir, "hw_vbms32.c"), "r") as f:
    c_lines = f.readlines()

for i, line in enumerate(c_lines[:150]):
    print(f"{i+1:3}: {line}", end="")

print("\n" + "=" * 80)
print("EXTENSIONS / CONTROL FUNCTIONS IN hw_vbms32.c:")
print("=" * 80)
# Look for functions setting PIN_CHG_EN, PIN_PCHG_EN, PIN_PSW_EN, PIN_OUT_EN
for i, line in enumerate(c_lines):
    if any(k in line for k in ["PIN_CHG_EN", "PIN_PCHG_EN", "PIN_PSW_EN", "PIN_OUT_EN", "ext_set_chg", "ext_set_pchg"]):
        start = max(0, i-5)
        end = min(len(c_lines), i+15)
        print(f"\n--- Around line {i+1} ---")
        for j in range(start, end):
            print(f"{j+1:4}: {c_lines[j]}", end="")
        break
