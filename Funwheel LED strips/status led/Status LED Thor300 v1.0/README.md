# Status LED Thor300 v1.0

State-of-charge / system status LED PCB indicator for the Funwheel Thor300 / X7 platform, featuring backside JST GH connectivity, backside SMD passives, and 100% faithful compliance with the official mechanical DXF contour.

---

## 1. Physical & Mechanical Specifications

| Parameter | Value | Notes |
| :--- | :--- | :--- |
| **Board Outline** | **Exact match from `fungi status PCB.DXF`** | 10.3 mm width × 83.5 mm height with 16 continuous perimeter segments |
| **Mounting Notches** | **2x M3 Circular Edge Notches** | Radius 1.85 mm cutting into $X = 6.80\text{ mm}$ at $Y = 5.85\text{ mm}$ and $Y = 78.69\text{ mm}$, with $R = 0.1\text{ mm}$ corner fillets |
| **LED Package** | **5050 SMD 6-Pin (PLCC-6)** ($5.0 \times 5.0\text{ mm}$) | SK6815 / WS2815 12V with dual data redundancy (DIN & BIN) |
| **LED Count & Pitch** | **10 LEDs @ 6.8 mm pitch** | Centered at $X = 3.8\text{ mm}$, spanning $Y = 11.0\text{ mm}$ to $72.2\text{ mm}$ |
| **LED Orientation** | **0° Orientation** | Solder leads face left and right (X-axis) |
| **Connector** | **JST GH 1.25mm 4-Pin SMT (Vertical)** | Part: `BM04B-GHS-TBT`, mounted on B.Cu at top ($X = 3.6\text{ mm}, Y = 4.6\text{ mm}$) |
| **Passives** | **10x 0603 Decoupling Caps on B.Cu** | Positioned directly behind each LED ($X = 3.8\text{ mm}$) |
| **Data Protection** | **2x 33Ω Resistors (0603)** | R1 on F.Cu at top ($2.5, 2.2\text{ mm}$), R2 on B.Cu near LED 10 ($8.5, 74.5\text{ mm}$) |

---

## 2. Electrical Specifications & Connector Pinout

### JST GH 4-Pin Silkscreen Mapping (B.Cu Bottom Side)

| Pin # | Silkscreen Marking | Signal Name | Function & Routing |
| :---: | :---: | :---: | :--- |
| **1** | **`12V`** | **+12V** | +12V DC power bus. Routes along $X = 1.0\text{ mm}$ rail on B.Cu. |
| **2** | **`GND`** | **GND** | 0V Ground reference return. Routes along $X = 6.25\text{ mm}$ rail on B.Cu. |
| **3** | **`DOUT`** | **DATA_OUT** | Serial RGB data return from LED #10 for daisy chaining. |
| **4** | **`DIN`** | **DATA_IN** | Serial RGB data input to LED #1 via 33Ω resistor R1. |

---

## 3. Production & CAD Artifacts

* **KiCad PCB File**: [`Status_LED_Thor300_v1.0.kicad_pcb`](file:///c:/Users/quinn/Desktop/AI%20PCB%20CAD/Funwheel%20LED%20strips/status%20led/Status%20LED%20Thor300%20v1.0/Status_LED_Thor300_v1.0.kicad_pcb)
* **3D STEP CAD Model**: [`Status_LED_Thor300_v1.0.step`](file:///c:/Users/quinn/Desktop/AI%20PCB%20CAD/Funwheel%20LED%20strips/status%20led/Status%20LED%20Thor300%20v1.0/Status_LED_Thor300_v1.0.step)
* **3D Top Render**: [`Status_LED_Thor300_v1.0_3d_top.png`](file:///c:/Users/quinn/Desktop/AI%20PCB%20CAD/Funwheel%20LED%20strips/status%20led/Status%20LED%20Thor300%20v1.0/Status_LED_Thor300_v1.0_3d_top.png)
* **3D Bottom Render**: [`Status_LED_Thor300_v1.0_3d_bottom.png`](file:///c:/Users/quinn/Desktop/AI%20PCB%20CAD/Funwheel%20LED%20strips/status%20led/Status%20LED%20Thor300%20v1.0/Status_LED_Thor300_v1.0_3d_bottom.png)
* **Python Generator**: [`build_status_led_v10.py`](file:///c:/Users/quinn/Desktop/AI%20PCB%20CAD/Funwheel%20LED%20strips/status%20led/Status%20LED%20Thor300%20v1.0/build_status_led_v10.py)
* **DRC Report**: [`drc_v10.json`](file:///c:/Users/quinn/Desktop/AI%20PCB%20CAD/Funwheel%20LED%20strips/status%20led/Status%20LED%20Thor300%20v1.0/drc_v10.json) (0 unconnected items, 0 critical violations)
