# CURSOR_HANDOVER.md — qfbms32 BMS PCB Project

> **Updated:** 2026-10-27  
> **Branch strategy:** single `master` only (no active feature/folder forks)  
> **Active board path:** `qfbms32 ai pcb/`  
> **Archived experiment:** `qfbms32 fork/` (lookalike / working / fork-time snapshot — do not edit)

---

## 0. Git / workflow (read first)

| Item | Value |
|------|--------|
| **Branch** | `master` only — synced with `origin/master` |
| **Active tree** | `qfbms32 ai pcb/` |
| **Archive tree** | `qfbms32 fork/` — frozen backups of the abandoned lookalike/working experiment |
| **Do not** | Create parallel git branches or treat `qfbms32 fork/` as the live design |

Capacitor footprint fix (`C_SSR2` → 0805) and related docs live in the active tree on `master`.

---

## 1. Project Summary

**Board:** `qfbms32` — a 32-series Battery Management System (BMS) PCB for the Fungineers project.  
**KiCad Version:** 10.0 (installed at `C:\Program Files\KiCad\10.0\`)  
**Workspace Root:** `c:\Users\quinn\Documents\GitHub\Fungineers PCB designs\`

### Key Files

| File | Path (relative to workspace root) | Purpose |
|------|-----------------------------------|---------|
| **PCB Layout** | `qfbms32 ai pcb/qfbms32.kicad_pcb` | Main board layout (28,183 lines) |
| **Schematic** | `qfbms32 ai pcb/qfbms32.kicad_sch` | Main schematic (3,773 lines) |
| **KiCad Project** | `qfbms32 ai pcb/qfbms32.kicad_pro` | Project file |
| **Dashboard Box Data** | `qfbms32 ai pcb/qfbms32.boxes.json` | Component placement annotations for web dashboard |
| **Reference Images** | `qfbms32 ai pcb/_reference/` | CAD renders, real board photos, wiring diagrams |
| **3D Top Render** | `qfbms32 ai pcb/qfbms32_3d_top.png` | Latest top-down 3D render (4000×2000, auto-cropped) |
| **3D Iso Render** | `qfbms32 ai pcb/qfbms32_3d_iso.png` | Latest isometric 3D render (4000×2600, auto-cropped) |
| **Custom Footprints** | `qfbms32 ai pcb/qfbms.pretty/` | Project-local footprint library |
| **Custom Symbols** | `qfbms32 ai pcb/qfbms.kicad_sym` | Project-local symbol library |
| **Scratch Scripts** | `qfbms32 ai pcb/scratch/` | One-off Python scripts used during development (safe to ignore) |
| **Backup History** | `qfbms32 ai pcb/.history/` | Manual PCB/schematic backups before major changes |

### Web Dashboard

| File | Path | Purpose |
|------|------|---------|
| **Server** | `_tools/pcb_dashboard/server.py` | Python HTTP server (port 5180) serving board data, renders, and box annotations |
| **Bridge** | `_tools/pcb_dashboard/kicad_bridge.py` | Reads/writes PCB via `pcbnew` API, outputs JSON |
| **Frontend** | `_tools/pcb_dashboard/index.html` | Dashboard HTML |
| **Styles** | `_tools/pcb_dashboard/style.css` | Dashboard CSS |
| **App Logic** | `_tools/pcb_dashboard/app.js` | Dashboard JavaScript |

---

## 2. Recent Changes (Most Recent First)

### C_SSR2 Footprint Upgrade: 0603 → 0805 (2026-10-24)

**Problem:** Both `C_SSR1` (100nF) and `C_SSR2` (1µF) were incorrectly assigned the same `Capacitor_SMD:C_0603_1608Metric` footprint. The real board has `C_SSR2` as a visibly larger 0805 package (darker brown, taller profile).

**Fix Applied:**
- **PCB:** Replaced `C_SSR2` footprint with `Capacitor_SMD:C_0805_2012Metric` at position `(30.00, 1.70)` mm, 90° rotation, F.Cu.
- **Schematic:** Updated `C_SSR2` Footprint property from `Capacitor_SMD:C_0603_1608Metric` to `Capacitor_SMD:C_0805_2012Metric`.
- **boxes.json:** Updated Color 2 (`#ff6b6b`) box dimensions from 1.3×2.9 to 2.0×1.25 mm.
- **3D Renders:** Re-rendered top and isometric views confirming distinct visual sizes.

**Current State of SSR Capacitors:**

| Ref | Value | Footprint | Position (mm) | Rot | STEP Model Dimensions (L×W×H) |
|-----|-------|-----------|---------------|-----|-------------------------------|
| `C_SSR1` | 100nF | `C_0603_1608Metric` | (28.45, 1.75) | 90° | 1.60 × 0.80 × 0.80 mm |
| `C_SSR2` | 1µF | `C_0805_2012Metric` | (30.00, 1.70) | 90° | 2.00 × 1.25 × 1.25 mm |

**Clearances verified:**
- C_SSR1 ↔ C_SSR2 pad gap: 0.35 mm
- C_SSR2 ↔ R_SSR1 pad gap: ~0.42 mm

### Dashboard Info Mode (2026-10-24)

- Added **Info** toggle button (shortcut `X`) next to Select button in sidebar.
- Clicking any footprint in Info mode shows a detail card in the lower sidebar (Ref, Value, Footprint, Coordinates, Rotation, Side, Pads, Nets, LCSC, MPN).
- Canvas highlights inspected component with amber dashed box and floating badge.

### Quick Sizes Bug Fix (2026-10-24)

- Fixed: Clicking Quick Size preset chips was mutating dimensions of previously placed boxes.
- Fixed: Preset clicks were resetting box rotation (`flipped: false` hardcode removed).

---

## 3. Tooling & Environment

### System

- **OS:** Windows 11 Home 64-bit (25H2, Build 26200.8116)
- **Shell:** PowerShell exclusively — **no Unix commands** (`grep`, `ls`, `cat` etc. will fail)
- **Hardware:** AMD Ryzen 5 2400G, GTX 1660 Ti, 16GB RAM

### KiCad 10.0

- **Install Path:** `C:\Program Files\KiCad\10.0\`
- **CLI:** `C:\Program Files\KiCad\10.0\bin\kicad-cli.exe`
- **Python (with pcbnew):** `C:\Program Files\KiCad\10.0\bin\python.exe`
- **Stock 3D Models:** `C:\Program Files\KiCad\10.0\share\kicad\3dmodels\`
- **Stock Footprints:** `C:\Program Files\KiCad\10.0\share\kicad\footprints\`

> **Important:** The system Python (`C:\Python314\python.exe`) does NOT have `pcbnew`. Any script that imports `pcbnew` must run via `& "C:\Program Files\KiCad\10.0\bin\python.exe"`.

### KiCad CLI Render Commands

```powershell
# Top-down 3D render
& "C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" pcb render --side top --width 4000 --height 2000 --background transparent -o "output.png" "board.kicad_pcb"

# Isometric 3D render
& "C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" pcb render --rotate "-45,0,45" --width 4000 --height 2600 --background transparent -o "output.png" "board.kicad_pcb"
```

### Web Dashboard Server

```powershell
# Start the dashboard server (port 5180)
cd "c:\Users\quinn\Documents\GitHub\Fungineers PCB designs"
python _tools/pcb_dashboard/server.py
# Open http://localhost:5180/
```

The dashboard server:
1. Serves the web UI (HTML/CSS/JS)
2. Provides `/api/board?path=...` — reads PCB footprints via `kicad_bridge.py`
3. Provides `/api/boxes?path=...` — reads/writes `.boxes.json` annotation files
4. Provides `/api/render_3d?path=...&kind=top|iso` — triggers kicad-cli 3D renders
5. Provides `/api/apply` — applies component moves via `kicad_bridge.py`

### pcbnew Python API Patterns

```python
# Always use KiCad's bundled Python:
# & "C:\Program Files\KiCad\10.0\bin\python.exe" script.py

import pcbnew

board = pcbnew.LoadBoard(r"path\to\board.kicad_pcb")

# Find a footprint
fp = board.FindFootprintByReference("C_SSR2")

# Load a library footprint
fp_new = pcbnew.FootprintLoad(
    r"C:\Program Files\KiCad\10.0\share\kicad\footprints\Capacitor_SMD.pretty",
    "C_0805_2012Metric"
)

# Place it
board.Add(fp_new)
fp_new.SetReference("C_SSR2")
fp_new.SetValue("1uF")
fp_new.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(30.0), pcbnew.FromMM(1.7)))
fp_new.SetOrientation(pcbnew.EDA_ANGLE(90.0, pcbnew.DEGREES_T))

pcbnew.SaveBoard(r"path\to\board.kicad_pcb", board)
```

---

## 4. Board Overview

- **Dimensions:** 130 × 32 mm (elongated strip)
- **Layers:** 2-layer (F.Cu, B.Cu)
- **Total Footprints:** ~90+
- **Key ICs:**
  - `U_BQ1`, `U_BQ2` — BQ7695202 (TQFP-48) battery monitor ICs
  - `U_ESP1` — ESP32-C3-MINI-1 microcontroller
  - `U_SSR1` — H2440 solid-state relay (SOIC-8 variant)
  - `U4` — LTC7138 DC/DC buck converter (MSOP-12)
  - `U7` — ISO1050 CAN transceiver (SMDIP-8)
- **Passive Arrays:** 32× balance resistors (`R_B1`–`R_B33`), 32× filter resistors (`R_F1`–`R_F32`)
- **Connectors:** XT30 power connectors, JST connectors for cell sense

### Component Naming Convention

| Prefix | Meaning |
|--------|---------|
| `C_SSR*` | Capacitors in SSR / charge power stage |
| `R_B*` | Balance resistors (one per cell, 0805) |
| `R_F*` | Cell voltage filter resistors (0402) |
| `C_B*` | BQ IC bypass/decoupling capacitors |
| `R_SSR*` | Resistors in SSR gate drive circuit |
| `U_BQ*` | BQ769x battery monitor ICs |

---

## 5. Known Issues & Gotchas

1. **Net assignments:** `C_SSR1` and `C_SSR2` pads currently have no net assignments (net code 0). This is expected — they were placed directly on the PCB without being routed from the schematic netlist yet.

2. **Schematic ↔ PCB sync:** After modifying footprints directly in the PCB, run "Update PCB from Schematic" in KiCad to re-sync net assignments. Be careful: this may move unconnected footprints.

3. **3D models use STEP only** (no `.wrl` files for these capacitors). KiCad 10 handles `.step` natively.

4. **PowerShell escaping:** When running Python one-liners from PowerShell, use `& "C:\Program Files\KiCad\10.0\bin\python.exe" -c "..."` syntax. Avoid `$_` or `${}` in double-quoted strings — PowerShell will try to interpolate them.

5. **Dashboard cache:** The web dashboard caches board reads. After modifying the PCB file, reload the dashboard page to pick up changes.

6. **Scratch directory:** `qfbms32 ai pcb/scratch/` contains 300+ one-off scripts from iterative development. These are safe to ignore — they are not part of the build process.

---

## 6. Continuation Checklist

For the next agent picking up this project in Cursor:

- [ ] Confirm `git status` is clean on **`master`** and matches `origin/master`
- [ ] Work only under **`qfbms32 ai pcb/`** (ignore `qfbms32 fork/` unless restoring a backup)
- [ ] **Verify 3D renders** look correct by opening `qfbms32_3d_top.png` and `qfbms32_3d_iso.png`
- [ ] **Run DRC** in KiCad to check for clearance violations after the footprint change
- [ ] **Assign nets** to `C_SSR1` and `C_SSR2` pads (currently unrouted)
- [ ] **Route traces** from `C_SSR1`/`C_SSR2` pads to the appropriate power nets
- [ ] **Continue component placement** for any remaining unplaced parts
- [ ] **Generate Gerbers** when placement and routing are complete

---

## 7. Quick Start for Cursor

```powershell
# 1. Navigate to workspace / confirm branch
cd "c:\Users\quinn\Documents\GitHub\Fungineers PCB designs"
git checkout master
git status -sb

# 2. Start dashboard server
python _tools/pcb_dashboard/server.py
# Dashboard at http://localhost:5180/
# Board: qfbms32 ai pcb/qfbms32.kicad_pcb

# 3. Open KiCad project (active tree)
& "C:\Program Files\KiCad\10.0\bin\kicad.exe" "qfbms32 ai pcb\qfbms32.kicad_pro"

# 4. Run a pcbnew script
& "C:\Program Files\KiCad\10.0\bin\python.exe" your_script.py

# 5. Re-render 3D after changes
& "C:\Program Files\KiCad\10.0\bin\kicad-cli.exe" pcb render --side top --width 4000 --height 2000 --background transparent -o "qfbms32 ai pcb\qfbms32_3d_top.png" "qfbms32 ai pcb\qfbms32.kicad_pcb"
```
