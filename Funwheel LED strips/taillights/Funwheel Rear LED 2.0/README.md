# Funwheel Rear LED 2.0 (Funwheel X7 Taillight)

**Status:** Laid out.

High-reliability 12V addressable RGB taillight LED PCB stick engineered for the **Funwheel X7** rear light cavity.

---

## 1. Physical & Mechanical Specifications

| Parameter | Value | Notes |
| :--- | :--- | :--- |
| **PCB Length** | **155.0 mm** | Matches Funwheel X7 rear chassis extrusion cavity |
| **PCB Width** | **6.85 mm** | Ultra-narrow strip profile |
| **PCB Thickness** | **1.5 mm** (or standard 1.6 mm) | Rigid 2-layer FR4 |
| **LED Package** | **5050 SMD 6-Pin (PLCC-6)** ($5.0 \times 5.0\text{ mm}$) | 6 solder points (3 on left side, 3 on right side) |
| **LED Count & Grouping** | **16 LEDs in 4 Groups of 4** | 4 optical segments ($8.0\text{ mm}$ intra-group pitch, $11.5\text{ mm}$ inter-group gap) |
| **Connector** | **JST GH 1.25mm 4-Pin SMT (Horizontal/Side-Entry)** | Part: `SM04B-GHS-TB`, rotated 90° along the board edge |
| **Passives Orientation** | **Vertical (Along Board Length)** | All 0603 caps & resistors turned 90° along length for optimal clearance |

---

## 2. Electrical Specifications & Pinout

### Operating Voltage & LEDs
* **LED Driver Type**: **SK6815 / WS2815 / GS8208 (6-Pin 5050)** (12V DC Addressable RGB LED with dual data / breakpoint resume).
* **Nominal Voltage**: **+12V DC** (from Funwheel X7 / VESC controller).
* **Color Sequence**: **GRB** 24-bit.
* **Signal Level**: 5V TTL logic.

### JST GH 4-Pin Silkscreen & Connector Mapping (SMT Backside, Rotated 90°)

Pins run along the board edge with silkscreen markings directly alongside the solder pads:

| Pin # | Silkscreen Marking | Signal Name | Function & Routing |
| :---: | :---: | :---: | :--- |
| **1** | **`in`** | **DATA_IN** | Data input from controller. Connects through $33\,\Omega$ resistor to `DIN`/`BIN` of LED #1. |
| **2** | **`out`** | **DATA_OUT** | Return data from LED #16 (`DOUT`). Connects through $33\,\Omega$ resistor to allow daisy-chaining directly to next strip via single harness! |
| **3** | **`g`** | **GND** | 0V Ground reference & power return plane. |
| **4** | **`12v`** | **+12V** | +12V DC power bus distributing power to all 16 LEDs. |

---

## 3. LED Array Coordinates (4 Groups of 4)

* **Group 1**:
  * D1: $Y = 6.5\text{ mm}$
  * D2: $Y = 14.5\text{ mm}$
  * D3: $Y = 22.5\text{ mm}$
  * D4: $Y = 30.5\text{ mm}$
* **Group 2** (after $6.5\text{ mm}$ optical gap):
  * D5: $Y = 42.0\text{ mm}$
  * D6: $Y = 50.0\text{ mm}$
  * D7: $Y = 58.0\text{ mm}$
  * D8: $Y = 66.0\text{ mm}$
* **Group 3** (after $6.5\text{ mm}$ optical gap):
  * D9: $Y = 77.5\text{ mm}$
  * D10: $Y = 85.5\text{ mm}$
  * D11: $Y = 93.5\text{ mm}$
  * D12: $Y = 101.5\text{ mm}$
* **Group 4** (after $6.5\text{ mm}$ optical gap):
  * D13: $Y = 113.0\text{ mm}$
  * D14: $Y = 121.0\text{ mm}$
  * D15: $Y = 129.0\text{ mm}$
  * D16: $Y = 137.0\text{ mm}$
* **Connector & Passives Zone**: $Y = 139.5\text{ mm}$ to $155.0\text{ mm}$.

---

## 4. Exported Models & Visualizations

* **STEP 3D Model**: [`Funwheel_Rear_LED_2.0.step`](Funwheel_Rear_LED_2.0.step)
* **3D Top View**: [`Funwheel_Rear_LED_2.0_3d_top.png`](Funwheel_Rear_LED_2.0_3d_top.png)
* **3D Bottom View**: [`Funwheel_Rear_LED_2.0_3d_bottom.png`](Funwheel_Rear_LED_2.0_3d_bottom.png)
* **2D Vector View**: [`Funwheel_Rear_LED_2.0_2d_view.png`](Funwheel_Rear_LED_2.0_2d_view.png)
