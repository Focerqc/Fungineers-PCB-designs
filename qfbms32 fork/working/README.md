# qfbms32 working

**Mandate:** Ship a working BMS — not a pixel-perfect clone.

## Frozen (do not move)

Keep these where the clone put them (mech / harness fit):

| Refs | Role |
|------|------|
| `J_BAT1`, `J_CHG1` | XT30 power |
| `J_CELL1`–`J_CELL4` | JST GH cell sense |
| `J_T1`–`J_T4` | JST GH thermistors |
| `J_COMM1` | JST GH CAN/5V |
| `J_USB1` | USB-C |

## Prefer keep (reuse clone placement)

- `U_BQ1`, `U_BQ2` — BQ7695202
- `U_ESP1` — ESP32-C3-MINI-1
- `U7` — ISO1050
- `U4` — LTC7138
- `U_SSR1` — H2440 SSR
- `Q1`, `Q2` — AGM15T03LL CHG/DSG FETs
- Board outline / mounting

Nudge only if electrical routing or clearance forces it.

## Free to change

- Balance / filter / bypass passives (values + placement) — align to **TI BQ76952** typical/EVM, not photo match
- Supporting nets, vias, pours, silk that aren’t connector-critical

## Electrical reference

See `_reference/ti_bq76952/` (datasheet + EVM UG + TIDA-010208).  
Clone passives are a starting guess only.

Open `qfbms32.kicad_pro` in this folder.
