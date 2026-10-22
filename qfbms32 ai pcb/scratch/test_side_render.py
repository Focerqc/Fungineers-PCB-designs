import subprocess
from PIL import Image

kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
pcb_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_pcb"

subprocess.run([
    kicad_cli, "pcb", "render",
    "--side", "left",
    "--width", "1600", "--height", "900",
    "--background", "transparent",
    "-o", "scratch/test_side_left.png",
    pcb_path
], check=True)

# Also test a slight angle to see both connectors and top/bottom of PCB
subprocess.run([
    kicad_cli, "pcb", "render",
    "--perspective",
    "--rotate", "0,-70,0",
    "--zoom", "2.0",
    "--pan", "0,0,0",
    "--width", "1600", "--height", "900",
    "--background", "transparent",
    "-o", "scratch/test_angle_left.png",
    pcb_path
], check=True)

print("Side renders complete!")
