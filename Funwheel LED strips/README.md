# Funwheel X7 LED Strip PCB Ecosystem

**Status:** Laid out. Headlight, taillight, and both Thor300 status bars are in the folders below.

Custom, high-reliability LED PCB assemblies designed specifically for the **Funwheel X7** platform (VESC-based personal electric vehicle). 

---

## Directory Architecture

```text
Funwheel LED strips/
├── funwheel_led_shared.pretty/     # Shared KiCad Footprint Library (5050 LEDs, JST-GH, WirePad, passives)
├── front led shape.DXF             # Mechanical CAD outline for front headlight strip
├── fungi status PCB.DXF            # Mechanical CAD outline for status indicator PCB
├── headlights/
│   └── Funwheel Front LED 2.0/     # 155mm × 16.5mm/8.7mm 20-LED Headlight Bar (90° LED rotation, JST GH 4-Pin)
│       ├── Funwheel_Front_LED_2.0.kicad_pcb
│       ├── Funwheel_Front_LED_2.0.step
│       ├── build_funwheel_front_led.py
│       └── README.md
├── taillights/
│   └── Funwheel Rear LED 2.0/      # 155mm × 6.85mm 16-LED Taillight Bar (SK6815 12V 5050, JST GH 4-Pin)
│       ├── Funwheel_Rear_LED_2.0.kicad_pcb
│       ├── Funwheel_Rear_LED_2.0.step
│       ├── build_funwheel_rear_led.py
│       └── README.md
├── status led/
│   ├── Status LED Thor300 v1.0/    # 10.3mm × 83.5mm 10-LED Status Bar (JST GH on wider side, backside passives)
│   │   ├── Status_LED_Thor300_v1.0.kicad_pcb
│   │   ├── Status_LED_Thor300_v1.0.step
│   │   ├── build_status_led_v10.py
│   │   └── README.md
│   └── Status LED Thor300 v1.1/    # 10.3mm × 83.5mm 10-LED Status Bar (2x2 Wire Solder on skinny side, flat back)
│       ├── Status_LED_Thor300_v1.1.kicad_pcb
│       ├── Status_LED_Thor300_v1.1.step
│       ├── build_status_led_v11.py
│       └── README.md
└── README.md                       # Top-Level System Overview & KiCad MCP Workflow
```

---

## Hardware Comparison Matrix

| Assembly | Board Dimensions | LED Count & Package | LED Orientation | Connectivity | Backside Components |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Front LED 2.0** | 155.0 mm × 16.5 mm (flared) / 8.7 mm | 20x 5050 PLCC-6 (SK6815 12V) | **Pads Between LEDs** (Matching Taillight) | JST GH 4-Pin Vertical SMT (Long tab) | **100% Flat Backside Along Body** (Passives on tab) |
| **Rear LED 2.0** | 155.0 mm × 6.85 mm (straight) | 16x 5050 PLCC-6 (SK6815 12V) | **90°** (Pads between adjacent LEDs) | JST GH 4-Pin Vertical SMT (Top edge) | 0603 Decoupling Caps + Passives |
| **Status Thor300 v1.0** | 10.3 mm × 83.5 mm (2x M3 notches) | 10x 5050 PLCC-6 (SK6815 12V) | **0°** (Pads along left/right) | JST GH 4-Pin Vertical SMT (Wider bottom side) | 10x 0603 Decoupling Caps |
| **Status Thor300 v1.1** | 10.3 mm × 83.5 mm (2x M3 notches) | 10x 5050 PLCC-6 (SK6815 12V) | **0°** (Pads along left/right) | 4x Wire Solder Pads in 2x2 Grid (Skinny top side) | **None (100% Flat Backside)** |
