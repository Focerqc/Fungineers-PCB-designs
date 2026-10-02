"""
render_board_preview.py
-----------------------
Auto-computes true board bounding box & aspect ratio from KiCad PCB files
and generates perfectly proportioned, unstretched 2D and 3D preview PNGs.
"""

import os
import sys
import re
import subprocess
import tempfile
from pathlib import Path

KICAD_CLI = r"C:\Program Files\KiCad\10.0\bin\kicad-cli.exe"

def get_board_extents_mm(pcb_path: Path):
    """
    Exports Edge.Cuts to a temporary SVG with --page-size-mode 2 to extract
    exact physical board width and height in millimeters.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp_svg = Path(tmpdir) / "outline.svg"
        cmd = [
            KICAD_CLI, "pcb", "export", "svg",
            "--mode-single",
            "--layers", "Edge.Cuts",
            "--exclude-drawing-sheet",
            "--page-size-mode", "2",
            "-o", str(tmp_svg),
            str(pcb_path)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0 or not tmp_svg.exists():
            return None, None
        
        content = tmp_svg.read_text(encoding="utf-8", errors="ignore")
        m = re.search(r'width="([0-9.]+)mm"\s+height="([0-9.]+)mm"', content)
        if m:
            return float(m.group(1)), float(m.group(2))
        
        # Fallback: viewBox
        m_vb = re.search(r'viewBox="[0-9.]+\s+[0-9.]+\s+([0-9.]+)\s+([0-9.]+)"', content)
        if m_vb:
            return float(m_vb.group(1)), float(m_vb.group(2))
            
    return None, None

def render_board(pcb_path: Path, max_dim: int = 2000, render_3d: bool = False):
    pcb_path = Path(pcb_path).resolve()
    if not pcb_path.exists():
        print(f"Error: PCB file not found: {pcb_path}")
        return False

    w_mm, h_mm = get_board_extents_mm(pcb_path)
    if not w_mm or not h_mm or w_mm <= 0 or h_mm <= 0:
        print(f"Warning: Could not determine valid extents for {pcb_path.name}. Using default 1:1 scale.")
        px_w, px_h = max_dim, max_dim
    else:
        aspect = w_mm / h_mm
        if aspect >= 1.0:
            px_w = max_dim
            px_h = max(200, int(round(max_dim / aspect)))
        else:
            px_h = max_dim
            px_w = max(200, int(round(max_dim * aspect)))
        print(f"Board {pcb_path.name}: {w_mm:.2f}mm x {h_mm:.2f}mm (Aspect {aspect:.3f}:1) -> {px_w}x{px_h} px")

    # Output paths
    base_name = pcb_path.stem
    output_2d = pcb_path.parent / f"{base_name}_2d_view.png"
    output_top = pcb_path.parent / f"{base_name}_top.png"

    # 1. Export 2D View via kicad-cli SVG -> render using KiCad CLI or MCP
    # We can export high-res SVG and then render
    svg_path = pcb_path.parent / f"{base_name}_2d_view.svg"
    cmd_svg = [
        KICAD_CLI, "pcb", "export", "svg",
        "--mode-single",
        "--layers", "F.Cu,B.Cu,F.SilkS,Edge.Cuts",
        "--exclude-drawing-sheet",
        "--page-size-mode", "2",
        "-o", str(svg_path),
        str(pcb_path)
    ]
    subprocess.run(cmd_svg, capture_output=True)

    # 2. Render realistic 3D top-down view (never stretched)
    cmd_3d = [
        KICAD_CLI, "pcb", "render",
        "--side", "top",
        "--width", str(px_w),
        "--height", str(px_h),
        "--background", "transparent",
        "-o", str(output_top),
        str(pcb_path)
    ]
    res_3d = subprocess.run(cmd_3d, capture_output=True, text=True)
    if res_3d.returncode == 0:
        print(f"  -> Generated realistic top view: {output_top.name} ({px_w}x{px_h})")

    return px_w, px_h

if __name__ == "__main__":
    workspace = Path(r"c:\Users\quinn\Desktop\AI PCB CAD")
    if len(sys.argv) > 1 and sys.argv[1] != "--all":
        target = Path(sys.argv[1])
        render_board(target)
    else:
        # Scan workspace for all main boards
        pcbs = list(workspace.glob("*/*.kicad_pcb")) + list(workspace.glob("*/*/*.kicad_pcb"))
        for pcb in pcbs:
            if "backup" in pcb.name.lower() or "test" in pcb.name.lower():
                continue
            render_board(pcb)
