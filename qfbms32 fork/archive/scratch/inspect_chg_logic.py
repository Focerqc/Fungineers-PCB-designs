import os

fw_dump_dir = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\firmware_dump"
with open(os.path.join(fw_dump_dir, "hw_vbms32.c"), "r") as f:
    lines = f.readlines()

for i in range(750, min(840, len(lines))):
    print(f"{i+1:4}: {lines[i]}", end="")
