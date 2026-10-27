# New-chat handover — qfbms32 fork

**Date:** 2026-10-27  
**Repo:** `c:\Users\quinn\Documents\GitHub\Fungineers PCB designs`  
**Branch:** `master` (ahead of origin by 1: `6cb3895` pre-fork snapshot)  
**Uncommitted:** entire `qfbms32 fork/` tree + `qfbms32 ai pcb/FORKED.md`

## What happened

Placement-perfect clone of the real VFBMS32 was abandoned as the primary goal. That board was snapshotted and forked:

| Path | Role |
|------|------|
| `qfbms32 ai pcb/` | Old active tree (frozen in practice; see `FORKED.md`) |
| `qfbms32 fork/archive/` | Full copy of that board at fork time — do not edit |
| `qfbms32 fork/lookalike/` | Visual twin; fake values OK |
| `qfbms32 fork/working/` | Real BMS; same plugs/ICs mainly; freer layout |

Both `lookalike/` and `working/` were seeded from the same KiCad project (sch/pcb/pro, `qfbms.pretty`, `3dmodels`, `_reference`). Neither path has been redesigned yet beyond that seed (except any local notes under `working/`).

## Recommended next (do this first)

**1. Commit the fork tree** so the split is durable, then pick **one** active path.

**2. Start on `working/`, not lookalike.**  
Why: a rideable BMS unblocks the product; the lookalike can stay a visual reference / later polish. Same connectors + BQ / ESP / SSR / buck / CAN is enough mechanical/electrical compatibility without chasing pixel placement.

**3. First concrete working-path task:** freeze the mechanical interface, then clean schematic→PCB sync.
- Lock connector locations (XT30, cell-sense JSTs, USB-C, CAN) — see `working/FIXED_CONNECTORS.md` if present
- Keep key ICs: `U_BQ1`/`U_BQ2` (BQ76952), `U_ESP1` (ESP32-C3-MINI-1), `U_SSR1` (H2440), `U4` (LTC7138), `U7` (ISO1050)
- Run ERC; fix missing nets (known: `C_SSR1`/`C_SSR2` had net 0 on the clone)
- Only then rearrange passives for clearance/routing — stop comparing to photo crops unless needed for plug alignment

**4. Lookalike later:** use `_reference/user_photos/IMG_214*.png` + CAD refs; fake silkscreen/values allowed; no ERC obsession.

## Tools (Windows / PowerShell)

- KiCad 10: `C:\Program Files\KiCad\10.0\`
- pcbnew scripts: `& "C:\Program Files\KiCad\10.0\bin\python.exe" script.py` (system Python has no pcbnew)
- Dashboard: `python _tools/pcb_dashboard/server.py` → http://localhost:5180/  
  Point board path at `qfbms32 fork/working/qfbms32.kicad_pcb` (or lookalike)

## Do not

- Edit `qfbms32 fork/archive/` or treat `qfbms32 ai pcb/` as the active design
- Resume photo-pixel placement hunting as the main workflow for `working/`
- Commit `node_modules/`

## Pasteable first prompt for new chat

```
Continue qfbms32 in qfbms32 fork/working/ (functional BMS path).
Read qfbms32 fork/NEW_CHAT_HANDOVER.md and qfbms32 fork/working/README.md.
Do not edit archive/ or the old qfbms32 ai pcb/ tree.
First: commit the uncommitted fork tree if still uncommitted, then lock connector positions and audit schematic↔PCB / ERC for the working board. Freer passive placement is OK; keep main plugs + BQ/ESP/SSR/buck/CAN ICs.
```
