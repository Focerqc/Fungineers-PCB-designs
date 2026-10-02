import re
import fitz

sch_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch"

with open(sch_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Move U_SSR1 to Y=25.0
# Current: (symbol (lib_id "vfbms:H2440_SSR")\n\t\t(at 155.0 60.0 0)
text = text.replace('(at 155.0 60.0 0)', '(at 155.0 25.0 0)')
text = text.replace('(property "Reference" "U_SSR1" (at 155.0 50.0 0)', '(property "Reference" "U_SSR1" (at 155.0 15.0 0)')
text = text.replace('(property "Value" "H2440_SSR" (at 155.0 52.5 0)', '(property "Value" "H2440_SSR" (at 155.0 17.5 0)')
text = text.replace('(property "Footprint" "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" (at 155.0 48.0 0)', '(property "Footprint" "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" (at 155.0 13.0 0)')

# Labels for U_SSR1:
# PIN_CHG_EN: at 140.0 63.81 180 -> at 140.0 28.81 180
text = text.replace('(at 140.0 63.81 180)', '(at 140.0 28.81 180)')
# PIN_OUT_EN: at 140.0 61.27 180 -> at 140.0 26.27 180
text = text.replace('(at 140.0 61.27 180)', '(at 140.0 26.27 180)')
# PIN_PSW_EN: at 140.0 58.73 180 -> at 140.0 23.73 180
text = text.replace('(at 140.0 58.73 180)', '(at 140.0 23.73 180)')

# 2. Adjust ESP32 labels:
# Left labels (X = 36.83)
# PIN_ENABLE: was at (18.0 103.886 180) -> move to (36.83 80.01 180) [Pin 6 is y=100.33 - 20.32 = 80.01]
# Note: In KiCad schematic, Y is downwards!
# Let's check where Pin 6 is: symbol offset y=20.32 means schematic Y = 100.33 - 20.32 = 80.01
text = re.sub(r'\(label "PIN_ENABLE"[\s\S]*?\(at [-\d.]+ [-\d.]+ 180\)', '(label "PIN_ENABLE"\n\t\t(at 36.83 80.01 180)', text)

# PIN_PCHG_EN: Pin 14 is y=15.24 -> 100.33 - 15.24 = 85.09
text = re.sub(r'\(label "PIN_PCHG_EN"[\s\S]*?\(at [-\d.]+ [-\d.]+ 180\)', '(label "PIN_PCHG_EN"\n\t\t(at 36.83 85.09 180)', text)

# PIN_COM_EN: Pin 15 is y=12.70 -> 100.33 - 12.70 = 87.63
text = re.sub(r'\(label "PIN_COM_EN"[\s\S]*?\(at [-\d.]+ [-\d.]+ 180\)', '(label "PIN_COM_EN"\n\t\t(at 36.83 87.63 180)', text)

# PIN_PSW_EN: Pin 16 is y=10.16 -> 100.33 - 10.16 = 90.17
text = re.sub(r'\(label "PIN_PSW_EN"[\s\S]*?\(at [-\d.]+ [-\d.]+ 180\)', '(label "PIN_PSW_EN"\n\t\t(at 36.83 90.17 180)', text)

# Right labels (X = 82.55)
# PIN_CHG_EN at ESP32: was at (66.0 116.586 0) -> Pin 10 (MTDI) is at 100.33 - 7.62 = 92.71
text = re.sub(r'\(label "PIN_CHG_EN"[\s\S]*?\(at [-\d.]+ 116\.586 0\)', '(label "PIN_CHG_EN"\n\t\t(at 82.55 92.71 0)', text)

# PIN_OUT_EN at ESP32: was at (66.0 114.046 0) -> Pin 9 (MTMS) is at 100.33 - 10.16 = 90.17
text = re.sub(r'\(label "PIN_OUT_EN"[\s\S]*?\(at [-\d.]+ 114\.046 0\)', '(label "PIN_OUT_EN"\n\t\t(at 82.55 90.17 0)', text)

# CAN_RX: was at (66.0 119.126 0) -> Pin 12 (MTCK) is at 100.33 - 5.08 = 95.25
text = re.sub(r'\(label "CAN_RX"[\s\S]*?\(at [-\d.]+ 119\.126 0\)', '(label "CAN_RX"\n\t\t(at 82.55 95.25 0)', text)

# CAN_TX: was at (66.0 121.666 0) -> Pin 13 (MTDO) is at 100.33 - 2.54 = 97.79
text = re.sub(r'\(label "CAN_TX"[\s\S]*?\(at [-\d.]+ 121\.666 0\)', '(label "CAN_TX"\n\t\t(at 82.55 97.79 0)', text)

with open(sch_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Updated schematic layout positions successfully!")
