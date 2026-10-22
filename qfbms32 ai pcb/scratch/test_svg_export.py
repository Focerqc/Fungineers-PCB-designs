import subprocess, os

KICAD_CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"
SCH_PATH = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\VFBMS32.kicad_sch"
SVG_DIR = r"c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\Q VFBMS32 AI PCB\sch_svg"
os.makedirs(SVG_DIR, exist_ok=True)

# kicad-cli sch export svg takes an output directory (-o)
res = subprocess.run([KICAD_CLI, "sch", "export", "svg", "-o", SVG_DIR, SCH_PATH], capture_output=True, text=True)
print("Return code:", res.returncode)
print("Stdout:", res.stdout)
print("Stderr:", res.stderr)
