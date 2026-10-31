# Fungineers PCB designs

Boards for Fungineers hardware: the 32s pack BMS, the Superflux hall board, Funwheel light bars, and the connectors that sit in the controller box.

A reference photo, an OEM drawing, or a chip vendor's eval board tells us the job and the shape. The board in this repo is finished when it does that job with the parts that are already on it. A different FET, a module instead of a bare chip, or a bleed resistor the eval board never had is fine when the circuit still measures, drives, or lights what it has to. A silk screen that matches a photo, with nets that do not complete the job, is not finished.

## Boards

| Folder | Status | Job |
|---|---|---|
| [`qfbms32 ai pcb/`](qfbms32%20ai%20pcb/README.md) | Incomplete | 32s BMS. Dual BQ76952, ESP32-C3, pack and charge connectors, cell taps, thermistors, CAN. Parts are placed. The circuit is not finished. |
| [`sf hall ai pcb/`](sf%20hall%20ai%20pcb/README.md) | Laid out | Hall board for the Superflux stator. Three sensors on the stator pitch, purple mask, ENIG. |
| [`Funwheel LED strips/`](Funwheel%20LED%20strips/README.md) | Laid out | Funwheel X7 headlight, taillight, and Thor300 status bars. Each size has its own readme. |
| [`footpad connector controller box side/`](footpad%20connector%20controller%20box%20side/README.md) | Laid out | Small breakouts for the controller enclosure: 5-pin Amphenol and 6-pin Switchcraft / Molex. |
| [`GTFO/`](GTFO/README.md) | Photos only | Reference photos for the GTFO lights and the GTS-FO BMS adapter. The laid-out LED boards are under `Funwheel LED strips/`. |
| [`FM VFBMS adapter/`](FM%20VFBMS%20adapter/README.md) | Stopped | Adapter between a Fungineers BMS and the GTFO controller. No board was made. |
| `_reference/firmware/` | Notes | Notes for the smaller charge-only VBMS32, not the 32s board. |
| `_tools/` | Local tools | Board boxes on port 5180. BMS progress, read from the PCB file, on port 5181. |

## KiCad

Boards are KiCad 10 projects. Open the `.kicad_pro` in the folder you mean to work on. Scripts that import `pcbnew` have to run with `C:\Program Files\KiCad\10.0\bin\python.exe`.
