# New-chat handover — single `master` (fork retired)

**Date:** 2026-10-27  
**Repo:** `c:\Users\quinn\Documents\GitHub\Fungineers PCB designs`  
**Branch strategy:** **one branch only — `master`** (synced with `origin/master`)  
**Active board:** `qfbms32 ai pcb/`  
**Archived experiment:** entire `qfbms32 fork/` tree (do not edit)

Also read root `CURSOR_HANDOVER.md` for tooling, capacitor notes, and board overview.

## What changed

The separate lookalike/working folder-fork workflow is abandoned. All prior fork iterations stay on disk under `qfbms32 fork/` as backups. Day-to-day work happens only in `qfbms32 ai pcb/` on `master`.

## Active mandate

Continue the BMS board in `qfbms32 ai pcb/`:

- Schematic / PCB / footprints / dashboard annotations live there
- Recent fix already in tree: `C_SSR2` → `C_0805_2012Metric` (see `CURSOR_HANDOVER.md`)
- Prefer TI BQ76952 / EVM / TIDA refs under `_reference/` when reshaping passives

## Next tasks

1. DRC after footprint changes; assign nets / route `C_SSR1` / `C_SSR2` if still netless
2. Schematic ↔ PCB sync + ERC
3. Continue placement / routing toward a manufacturable board
4. 3D render when layout moves

## Tools (Windows / PowerShell)

- KiCad 10: `C:\Program Files\KiCad\10.0\`
- pcbnew: `& "C:\Program Files\KiCad\10.0\bin\python.exe" script.py`
- Dashboard: `python _tools/pcb_dashboard/server.py` → http://localhost:5180/  
  Board path: `qfbms32 ai pcb/qfbms32.kicad_pcb`
- Open: `qfbms32 ai pcb/qfbms32.kicad_pro`

## Do not

- Treat `qfbms32 fork/` as active work
- Create parallel feature branches / folder forks for this board unless the user asks
- Commit `node_modules/`

## Pasteable first prompt

```
Continue qfbms32 on the single master branch in qfbms32 ai pcb/.
Read CURSOR_HANDOVER.md (and optionally qfbms32 fork/NEW_CHAT_HANDOVER.md).
qfbms32 fork/ is archived backup only — do not edit.
Next: DRC / net assign / route SSR caps if needed, schematic↔PCB sync, then keep placing and routing the working BMS.
```
