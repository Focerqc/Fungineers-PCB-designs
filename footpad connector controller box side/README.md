# Controller-Box-Side PEV Breakout & Adapter PCBs

High-reliability, vibration-resistant breakout and adapter PCBs designed to mount directly inside the controller enclosure of PEV (Personal Electric Vehicle / VESC) builds such as Onewheel XR, Plus, Pint, Pint X, and GT platforms.

---

## 1. Directory Structure

```text
footpad connector controller box side/
├── 5-pin/
│   ├── Footpad_5Pin_Amphenol.kicad_pro       # GT / Pint 5-Pin Project (Amphenol AU-05)
│   ├── Footpad_5Pin_Amphenol.kicad_sch       # Schematic (3.3V excited, ADC1, ADC2)
│   ├── Footpad_5Pin_Amphenol.kicad_pcb       # 16x16mm PCB (0 DRC violations)
│   └── fp-lib-table                          # Project Footprint Library Table
├── 6-pin/
│   ├── Footpad_6Pin_Switchcraft/             # Universal 6-Pin Project (Switchcraft EN3)
│   │   ├── Footpad_6Pin_Switchcraft.kicad_pro
│   │   ├── Footpad_6Pin_Switchcraft.kicad_sch # Dual-Use: Motor Hall & Footpad
│   │   ├── Footpad_6Pin_Switchcraft.kicad_pcb # 20x20mm PCB (JST-GH + Solder Pads, 0 DRC violations)
│   │   └── fp-lib-table
│   └── Molex_MX150L_6Pin_Header/             # 6-Circuit Vertical Header Faceplate
│       ├── Molex_MX150L_6Pin_Header.kicad_pro
│       ├── Molex_MX150L_6Pin_Header.kicad_sch
│       ├── Molex_MX150L_6Pin_Header.kicad_pcb
│       └── fp-lib-table
├── references/                               # Archived Reference Documents & Diagrams
│   ├── GT_Pint_5Pin_Handwritten_Reference.jpg
│   ├── XR_6Pin_Footpad_Handwritten_Reference.jpg
│   ├── XR_Hypercore_Motor_Hall_Switchcraft_6Pin_Reference.png
│   ├── Pint_GT_5Pin_Wiring_Schematic_Reference.png
│   └── KiCad_PCB_Screenshot_Reference.png
├── footpad_shared.pretty/                    # Shared KiCad Footprint Library
└── README.md
```

---

## 2. Hardware Specifications & Connectors

| Connector Type | Manufacturer & Part Number | Application | Board Dimensions | Primary Termination | Backup Termination |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **5-Pin Circular** | Amphenol LTW `AU-05PMMS-LC7001` | GT / Pint Footpad | $16 \times 16\text{ mm}$ (chamfered) | JST-PH 3-Pin (2.00mm pitch) | 3 Plated Oval Wire Solder Pads |
| **6-Pin Circular** | Switchcraft `EN3P6MX` | **Universal**: XR Motor Hall / Footpad | $20 \times 20\text{ mm}$ (chamfered) | **SMD JST-GH 6-Pin (1.25mm pitch)** | **6 Plated Through-Hole Solder Pads (2.0mm pitch)** |
| **Modular Header** | Molex MX150L `19428-0012` | Controller Faceplate Breakout | $88 \times 28\text{ mm}$ (flanged) | Dual-row solder bars & harness | Solder pads |

---

## 3. Pinouts & Electrical Mappings

### A. GT / Pint 5-Pin Connector (Amphenol AU-05)
*Connector Geometry: 4 Outer Pins in Square ($r = 2.0\text{ mm}$) + Pin 5 at Center `(0, 0)`. Notch at 12 o'clock.*

| Pin # | Solder Side Position (Notch at Top) | VESC Signal | Hybrid Pad Destination | Function / Notes |
| :---: | :--- | :---: | :---: | :--- |
| **1** | Top-Right (`X = +1.414, Y = -1.414`) | **`3.3V`** | Pad 3 (`3.3V`) | FSR Common Excitation Rail |
| **2** | Bottom-Right (`X = +1.414, Y = +1.414`)| `NC` | — | Unconnected / Spare |
| **3** | Bottom-Left (`X = -1.414, Y = +1.414`) | **`ADC1`** | Pad 2 (`ADC1`) | Sensor Half 1 (VESC ADC1 Input) |
| **4** | Top-Left (`X = -1.414, Y = -1.414`) | **`ADC2`** | Pad 1 (`ADC2`) | Sensor Half 2 (VESC ADC2 Input) |
| **5** | Center (`X = 0, Y = 0`) | `NC` | — | Ground / Shield / Spare |

> **Note on Excitation Voltage**: VESC ADC inputs utilize internal/external pull-down resistors to Ground. The common footpad excitation must connect to **`3.3V`** so that depressing the FSR creates a positive voltage divider signal into `ADC1` and `ADC2`.

---

### B. Universal 6-Pin Switchcraft EN3 Connector (Motor Hall / Footpad)
*Connector Geometry: 5 Outer Pins ($r = 2.4\text{ mm}$, $72^\circ$ spacing) + Pin 6 at Center `(0, 0)`. Notch at 12 o'clock.*

| Pin # | Solder Side Position (Notch at Top) | Motor Hall Signal | Footpad Signal | Motor Wire Color | JST-GH Pin | Backup Solder Pad |
| :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| **1** | Top-Right (`X = +1.41, Y = -1.94`) | **`HALL 1`** (`H1`) | **`ADC 1`** | **Green** | Pin 1 | Pad 1 (Right) |
| **2** | Bottom-Right (`X = +2.28, Y = +0.74`) | **`HALL 2`** (`H2`) | **`ADC 2`** | **Blue** | Pin 2 | Pad 2 |
| **3** | Bottom (`X = 0.0, Y = +2.40`) | **`GND`** | **`GND`** (Shield) | **Black** | Pin 3 | Pad 3 |
| **4** | Bottom-Left (`X = -2.28, Y = +0.74`) | **`5V`** (Hall Power) | `NC` | **Red** | Pin 4 | Pad 4 |
| **5** | Top-Left (`X = -1.41, Y = -1.94`) | **`TEMP`** (Motor NTC)| `NC` | **White** | Pin 5 | Pad 5 |
| **6** | Center (`X = 0.0, Y = 0.0`) | **`HALL 3`** (`H3`) | **`3.3V`** (Excitation) | **Yellow** | Pin 6 | Pad 6 (Left) |

### Dual Silkscreen Markings on Universal 6-Pin PCB:
- **Front Silkscreen (`F.SilkS`)**:
  - Row 1 (Motor): `MOT:  H3   TMP   5V   GND   H2   H1`
  - Row 2 (Footpad): ` FP: 3.3V  NC    NC   GND  ADC2 ADC1`
- **Back Silkscreen (`B.SilkS`)**: Full quick-reference color-code reference chart:
  - `1: H1/ADC1 (GRN)`
  - `2: H2/ADC2 (BLU)`
  - `3: GND/GND (BLK)`
  - `4: 5V/NC   (RED)`
  - `5: TMP/NC  (WHT)`
  - `6: H3/3.3V (YEL)`

---

## 4. Fabrication & Verification

- **Layers**: 2-Layer (Top: `F.Cu`, Bottom: `B.Cu`)
- **Board Thickness**: 1.6 mm (FR-4)
- **Surface Finish**: Lead-Free HASL or ENIG
- **Copper Weight**: 1 oz (35 µm)
- **Minimum Trace / Space**: 0.35 mm / 0.35 mm (> 13.8 mil, exceeding standard fab limits)
- **KiCad DRC**: **0 DRC Violations, 0 Unconnected Items, 0 Footprint Errors** on both projects.