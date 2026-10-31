# Start here

- [README.md](README.md) — what this repo is, and what "finished" means for a board
- [qfbms32 ai pcb/README.md](qfbms32%20ai%20pcb/README.md) — the 32s BMS: the job, the current nets, and the files

The live board is `qfbms32 ai pcb/`. Footprints already on `qfbms32.kicad_pcb` stay put. The photos in `qfbms32 ai pcb/_reference/user_photos/` are the placement check. TI docs are for values and pin function. If a placed part cannot do the job, stop and name the ref and the pin. Rule file: `.cursor/rules/qfbms32-placement.mdc`.

Progress for that board is computed from the PCB, at <http://localhost:5181> (`python _tools/progress_dashboard/server.py`).
