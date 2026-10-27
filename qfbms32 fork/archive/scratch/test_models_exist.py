import subprocess, os

kicad_cli = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"

# Let's check which 3D model files exist for L1
models = [
    r"C:\Program Files\KiCad\10.0\share\kicad\3dmodels\Inductor_SMD.3dshapes\L_SXN_SMDRI73.step",
    r"C:\Program Files\KiCad\10.0\share\kicad\3dmodels\Inductor_SMD.3dshapes\L_TDK_SLF7045.step",
    r"C:\Program Files\KiCad\10.0\share\kicad\3dmodels\Inductor_SMD.3dshapes\L_Coilcraft_MSS7348-XXX.step",
    r"C:\Program Files\KiCad\10.0\share\kicad\3dmodels\Package_SO.3dshapes\SOIC-8_7.5x5.85mm_P1.27mm.step",
    r"C:\Program Files\KiCad\10.0\share\kicad\3dmodels\Package_SO.3dshapes\SOP-8_6.605x9.655mm_P2.54mm.step",
]

for m in models:
    print(f"Exists: {os.path.exists(m)} -> {m}")
