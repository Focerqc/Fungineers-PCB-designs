# Funwheel Front LED 2.0 (Funwheel X7 Headlight)

High-reliability 12V addressable RGB headlight LED PCB assembly engineered for the **Funwheel X7** front light cavity.

---

## 1. Physical & Mechanical Specifications

| Parameter | Value | Notes |
| :--- | :--- | :--- |
| **Board Outline** | **Exact match from `front led shape.DXF`** | 155.0 mm total length, 16.5 mm flared end tabs, 8.7 mm center strip |
| **PCB Thickness** | **1.6 mm** | Standard 2-layer rigid FR4 |
| **LED Package** | **5050 SMD 6-Pin (PLCC-6)** ($5.0 \times 5.0\text{ mm}$) | SK6815 / WS2815 12V with dual data redundancy (DIN & BIN) |
| **LED Count & Pitch** | **20 LEDs @ 6.4 mm pitch** | High-density optical headlight bar spanning $X = 18.0\text{ mm}$ to $139.6\text{ mm}$ |
| **LED Orientation** | **Solder Leads Face Between Adjacent LEDs** | Turned 90° so solder leads face along the strip length (X-axis), matching the Taillight bar |
| **Connector** | **JST GH 1.25mm 4-Pin SMT (Vertical / Top-Entry)** | Part: `BM04B-GHS-TBT`, mounted on B.Cu at the **long flared tab** ($X \approx 12.0\text{ mm}$, $Y \approx 12.0\text{ mm}$) |
| **Backside & Passives** | **100% Flat Backside Along Body** + **Tab Passives** | Zero SMD components along the body for flush chassis mounting; Series $33\,\Omega$ data resistors (R1, R2) and $10\,\mu\text{F}$ bulk cap (C21) positioned on tab |

---

## 2. Electrical Specifications & Pinout

### JST GH 4-Pin Silkscreen Mapping (B.Cu)

| Pin # | Silkscreen Marking | Signal Name | Function & Routing |
| :---: | :---: | :---: | :--- |
| **4** | **`DIN`** | **DATA_IN** | Data input from controller. Routes through R1 ($33\,\Omega$) along B.Cu to left tab vias to feed LED #1. |
| **3** | **`DOUT`** | **DATA_OUT** | Return data from LED #20 (`DOUT`). Routes through R2 ($33\,\Omega$) to allow single-harness chaining. |
| **2** | **`GND`** | **GND** | 0V Ground power return plane. |
| **1** | **`12V`** | **+12V** | +12V DC power bus distributing power to all 20 LEDs. |

---

## 3. Production & CAD Artifacts

* **KiCad PCB File**: [`Funwheel_Front_LED_2.0.kicad_pcb`](file:///c:/Users/quinn/Desktop/AI%20PCB%20CAD/Funwheel%20LED%20strips/headlights/Funwheel%20Front%20LED%202.0/Funwheel_Front_LED_2.0.kicad_pcb)
* **3D STEP CAD Model**: [`Funwheel_Front_LED_2.0.step`](file:///c:/Users/quinn/Desktop/AI%20PCB%20CAD/Funwheel%20LED%20strips/headlights/Funwheel%20Front%20LED%202.0/Funwheel_Front_LED_2.0.step)
* **Python Generator**: [`build_funwheel_front_led.py`](file:///c:/Users/quinn/Desktop/AI%20PCB%20CAD/Funwheel%20LED%20strips/headlights/Funwheel%20Front%20LED%202.0/build_funwheel_front_led.py)
* **DRC Report**: [`drc_report.json`](file:///c:/Users/quinn/Desktop/AI%20PCB%20CAD/Funwheel%20LED%20strips/headlights/Funwheel%20Front%20LED%202.0/drc_report.json)
