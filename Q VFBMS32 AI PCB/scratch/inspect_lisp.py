import os

fw_dump_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\firmware_dump"

print("=" * 80)
print("EXTENSIONS IN hw_vbms32.c:")
print("=" * 80)
with open(os.path.join(fw_dump_dir, "hw_vbms32.c"), "r") as f:
    c_lines = f.readlines()

for i, line in enumerate(c_lines):
    if "ext_set_chg" in line or "ext_set_pchg" in line or "ext_set_out" in line:
        start = max(0, i-2)
        end = min(len(c_lines), i+25)
        print(f"\n--- Function at line {i+1} ---")
        for j in range(start, end):
            print(f"{j+1:4}: {c_lines[j]}", end="")

print("\n" + "=" * 80)
print("CONTENTS OF vbms32_micro.lisp:")
print("=" * 80)
lisp_path = os.path.join(fw_dump_dir, "vbms32_micro.lisp")
if os.path.exists(lisp_path):
    with open(lisp_path, "r") as f:
        print(f.read())
