# Status LED Thor300 v1.1

High-reliability direct-solder version of the Funwheel Thor300 status LED PCB indicator, featuring a **completely flat backside** (zero SMD components on B.Cu), four through-hole wire solder pads contoured safely around the mounting notch, and 100% faithful compliance with the official mechanical DXF contour.

---

## 1. Physical & Mechanical Specifications

| Parameter | Value | Notes |
| :--- | :--- | :--- |
| **Board Outline** | **Exact match from `fungi status PCB.DXF`** | 10.3 mm width × 83.5 mm height with 16 continuous perimeter segments |
| **Mounting Notches** | **2x M3 Circular Edge Notches** | Radius 1.85 mm cutting into $X = 6.80\text{ mm}$ at $Y = 5.85\text{ mm}$ and $Y = 78.69\text{ mm}$, with $R = 0.1\text{ mm}$ corner fillets |
| **Wire Solder Interface** | **4x Plated Through-Hole Solder Pads** | 1.0 mm drill hole, 1.8 mm annular pad diameter |
| **Backside Profile** | **100% Flat Backside (Zero SMD Components)** | No passives or connectors on B.Cu; flush heatsink/chassis direct tape or thermal interface mounting |
| **Front Passives** | **All 10x Decoupling Caps on F.Cu** | 10x 0603 0.1µF MLCC capacitors placed vertically along the right rail ($X = 8.8\text{ mm}$) |
| **Data Resistors** | **2x 33Ω Resistors (0603) on F.Cu** | R1 (DATA_IN) at $(6.0, 82.5\text{ mm})$, R2 (DATA_OUT) at $(2.0, 75.9\text{ mm})$ |
| **LED Package** | **5050 SMD 6-Pin (PLCC-6)** ($5.0 \times 5.0\text{ mm}$) | SK6815 / WS2815 12V with dual data redundancy (DIN & BIN) |
| **LED Count & Pitch** | **10 LEDs @ 6.8 mm pitch** | Centered at $X = 3.8\text{ mm}$, spanning $Y = 11.0\text{ mm}$ to $72.2\text{ mm}$ |
| **LED Orientation** | **0° Orientation** | Solder leads face left and right (X-axis) |

---

## 2. Wire Solder Interface & Pinout (Bottom Tab)

The 4 solder wire pads are located on the bottom tab, strategically positioned and contoured around the bottom mounting notch ($Y = 78.69\text{ mm}$):

```text
               [ LED #10 ]
               [ R2 33R  ]
    (DO)  (2.0, 78.0)     (4.6, 78.5) (GND)       <- Notch at (8.65, 78.69)
    (12V) (2.2, 81.2)     (5.2, 81.2) (DI)
                          [ R1 33R  ]
```

| Signal | Silkscreen | Pad Position (X, Y) | Wire Color | Function |
| :---: | :---: | :---: | :---: | :--- |
| **DATA_OUT** | **`DO`** | $(2.0, 78.0\text{ mm})$ | **White** | Serial RGB data return from LED #10 via R2 for daisy-chaining. |
| **GND** | **`GND`** | $(4.6, 78.5\text{ mm})$ | **Black** | 0V Ground reference return. |
| **+12V** | **`12V`** | $(2.2, 81.2\text{ mm})$ | **Red** | +12V DC power bus. |
| **DATA_IN** | **`DI`** | $(5.2, 81.2\text{ mm})$ | **Green** | Serial RGB data input to LED #1 via R1. |

---

## 3. Production & CAD Artifacts

* **KiCad PCB File**: [`Status_LED_Thor300_v1.1.kicad_pcb`](file:///c:/Users/quinn/Desktop/AI%20PCB%20CAD/Funwheel%20LED%20strips/status%20led/Status%20LED%20Thor300%20v1.1/Status_LED_Thor300_v1.1.kicad_pcb)
* **3D STEP CAD Model**: [`Status_LED_Thor300_v1.1.step`](file:///c:/Users/quinn/Desktop/AI%20PCB%20CAD/Funwheel%20LED%20strips/status%20led/Status%20LED%20Thor300%20v1.1/Status_LED_Thor300_v1.1.step)
* **3D Top Render**: [`Status_LED_Thor300_v1.1_3d_top.png`](file:///c:/Users/quinn/Desktop/AI%20PCB%20CAD/Funwheel%20LED%20strips/status%20led/Status%20LED%20Thor300%20v1.1/Status_LED_Thor300_v1.1_3d_top.png)
* **3D Bottom Render**: [`Status_LED_Thor300_v1.1_3d_bottom.png`](file:///c:/Users/quinn/Desktop/AI%20PCB%20CAD/Funwheel%20LED%20strips/status%20led/Status%20LED%20Thor300%20v1.1/Status_LED_Thor300_v1.1_3d_bottom.png)
* **Python Generator**: [`build_status_led_v11.py`](file:///c:/Users/quinn/Desktop/AI%20PCB%20CAD/Funwheel%20LED%20strips/status%20led/Status%20LED%20Thor300%20v1.1/build_status_led_v11.py)
* **DRC Report**: [`drc_v11.json`](file:///c:/Users/quinn/Desktop/AI%20PCB%20CAD/Funwheel%20LED%20strips/status%20led/Status%20LED%20Thor300%20v1.1/drc_v11.json) (0 unconnected items, 0 critical violations)
