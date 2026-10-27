import re
import uuid

sch_path = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch"
with open(sch_path, "r", encoding="utf-8") as f:
    sch_text = f.read()

# Verify if U_GATE_DRV is present in schematic text:
if "U_GATE_DRV" in sch_text:
    print("Found U_GATE_DRV in schematic, deleting...")
    sch_text = re.sub(r'\(symbol\s+[^)]*?U_GATE_DRV[\s\S]*?\n\t\)', '', sch_text)
else:
    print("U_GATE_DRV is not in schematic.")

# Let's check lib_symbols in sch_text
# We will define AGM15T03LL in lib_symbols with Gate (pin 1), Drain (pin D), Source (pin S / 2)
toll_sym_def = '''
		(symbol "vfbms:AGM15T03LL"
			(pin_names
				(offset 1.016)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(in_pos_files yes)
			(property "Reference" "Q"
				(at 5.08 1.27 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Value" "AGM15T03LL"
				(at 5.08 -1.27 0)
				(effects
					(font
						(size 1.27 1.27)
					)
					(justify left)
				)
			)
			(property "Footprint" "vfbms:TOLL-8_AGM15T03LL"
				(at 5.08 2.54 0)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Datasheet" ""
				(at 0 0 0)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Description" "TOLL-8 N-Channel Power MOSFET 150V 300A"
				(at 0 0 0)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(symbol "AGM15T03LL_1_1"
				(rectangle
					(start -5.08 6.35)
					(end 5.08 -6.35)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type background)
					)
				)
				(pin input line
					(at -7.62 0 0)
					(length 2.54)
					(name "G"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "1"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 0 8.89 270)
					(length 2.54)
					(name "D"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "D"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
				(pin passive line
					(at 0 -8.89 90)
					(length 2.54)
					(name "S"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
					(number "2"
						(effects
							(font
								(size 1.27 1.27)
							)
						)
					)
				)
			)
		)'''

ssr_sym_def = '''
		(symbol "vfbms:H2440_SSR"
			(pin_names
				(offset 1.016)
			)
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(in_pos_files yes)
			(property "Reference" "U"
				(at 0 10.16 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Value" "H2440_SSR"
				(at 0 7.62 0)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(property "Footprint" "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm"
				(at 0 5.08 0)
				(hide yes)
				(effects
					(font
						(size 1.27 1.27)
					)
				)
			)
			(symbol "H2440_SSR_1_1"
				(rectangle
					(start -7.62 6.35)
					(end 7.62 -6.35)
					(stroke
						(width 0.254)
						(type default)
					)
					(fill
						(type background)
					)
				)
				(pin input line
					(at -10.16 3.81 0)
					(length 2.54)
					(name "IN_CHG"
						(effects (font (size 1.27 1.27)))
					)
					(number "1"
						(effects (font (size 1.27 1.27)))
					)
				)
				(pin input line
					(at -10.16 1.27 0)
					(length 2.54)
					(name "IN_DSG"
						(effects (font (size 1.27 1.27)))
					)
					(number "2"
						(effects (font (size 1.27 1.27)))
					)
				)
				(pin input line
					(at -10.16 -1.27 0)
					(length 2.54)
					(name "PSW_EN"
						(effects (font (size 1.27 1.27)))
					)
					(number "3"
						(effects (font (size 1.27 1.27)))
					)
				)
				(pin power_in line
					(at -10.16 -3.81 0)
					(length 2.54)
					(name "GND"
						(effects (font (size 1.27 1.27)))
					)
					(number "4"
						(effects (font (size 1.27 1.27)))
					)
				)
				(pin output line
					(at 10.16 3.81 180)
					(length 2.54)
					(name "OUT_CHG"
						(effects (font (size 1.27 1.27)))
					)
					(number "8"
						(effects (font (size 1.27 1.27)))
					)
				)
				(pin output line
					(at 10.16 1.27 180)
					(length 2.54)
					(name "OUT_DSG"
						(effects (font (size 1.27 1.27)))
					)
					(number "7"
						(effects (font (size 1.27 1.27)))
					)
				)
				(pin passive line
					(at 10.16 -1.27 180)
					(length 2.54)
					(name "VBAT_S"
						(effects (font (size 1.27 1.27)))
					)
					(number "6"
						(effects (font (size 1.27 1.27)))
					)
				)
				(pin power_in line
					(at 10.16 -3.81 180)
					(length 2.54)
					(name "VBOOST"
						(effects (font (size 1.27 1.27)))
					)
					(number "5"
						(effects (font (size 1.27 1.27)))
					)
				)
			)
		)'''

res_sym_def = '''
		(symbol "Device:R"
			(pin_numbers (hide yes))
			(pin_names (offset 0) (hide yes))
			(exclude_from_sim no)
			(in_bom yes)
			(on_board yes)
			(in_pos_files yes)
			(property "Reference" "R"
				(at 2.032 0 90)
				(effects (font (size 1.27 1.27)))
			)
			(property "Value" "R"
				(at -2.032 0 90)
				(effects (font (size 1.27 1.27)))
			)
			(property "Footprint" "Resistor_SMD:R_0603_1608Metric"
				(at 0 0 90)
				(hide yes)
				(effects (font (size 1.27 1.27)))
			)
			(symbol "R_1_1"
				(rectangle
					(start -1.016 2.54)
					(end 1.016 -2.54)
					(stroke (width 0.254) (type default))
					(fill (type none))
				)
				(pin passive line
					(at 0 3.81 270)
					(length 1.27)
					(name "~" (effects (font (size 1.27 1.27))))
					(number "1" (effects (font (size 1.27 1.27))))
				)
				(pin passive line
					(at 0 -3.81 90)
					(length 1.27)
					(name "~" (effects (font (size 1.27 1.27))))
					(number "2" (effects (font (size 1.27 1.27))))
				)
			)
		)'''

# Insert symbols into lib_symbols if not already present
lib_sym_end = sch_text.find("\n\t(symbol (lib_id \"Battery_Management:BQ7695202PFB\"")
if "vfbms:AGM15T03LL" not in sch_text:
    sch_text = sch_text[:lib_sym_end] + toll_sym_def + ssr_sym_def + res_sym_def + sch_text[lib_sym_end:]

# Now instantiate Q1, Q2, U_SSR1, R_G1, R_G2, R_PD1, R_PD2 and labels in schematic
# Place at X ~ 150-200, Y ~ 40-90
instantiations = f'''
	(symbol (lib_id "vfbms:AGM15T03LL")
		(at 195.0 45.0 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{uuid.uuid4()}")
		(property "Reference" "Q1" (at 195.0 35.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "AGM15T03LL (CHG FET)" (at 195.0 37.5 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "vfbms:TOLL-8_AGM15T03LL" (at 195.0 33.0 0) (hide yes) (effects (font (size 1.27 1.27))))
		(pin "1" (uuid "{uuid.uuid4()}"))
		(pin "D" (uuid "{uuid.uuid4()}"))
		(pin "2" (uuid "{uuid.uuid4()}"))
		(instances
			(project "VFBMS32"
				(path "/a2322edc-ff52-449c-92df-24faffac0236" (reference "Q1") (unit 1))
			)
		)
	)

	(symbol (lib_id "vfbms:AGM15T03LL")
		(at 195.0 80.0 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{uuid.uuid4()}")
		(property "Reference" "Q2" (at 195.0 70.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "AGM15T03LL (DSG FET)" (at 195.0 72.5 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "vfbms:TOLL-8_AGM15T03LL" (at 195.0 68.0 0) (hide yes) (effects (font (size 1.27 1.27))))
		(pin "1" (uuid "{uuid.uuid4()}"))
		(pin "D" (uuid "{uuid.uuid4()}"))
		(pin "2" (uuid "{uuid.uuid4()}"))
		(instances
			(project "VFBMS32"
				(path "/a2322edc-ff52-449c-92df-24faffac0236" (reference "Q2") (unit 1))
			)
		)
	)

	(symbol (lib_id "vfbms:H2440_SSR")
		(at 155.0 60.0 0)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{uuid.uuid4()}")
		(property "Reference" "U_SSR1" (at 155.0 50.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "H2440_SSR" (at 155.0 52.5 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Package_SO:SOIC-8_3.9x4.9mm_P1.27mm" (at 155.0 48.0 0) (hide yes) (effects (font (size 1.27 1.27))))
		(pin "1" (uuid "{uuid.uuid4()}"))
		(pin "2" (uuid "{uuid.uuid4()}"))
		(pin "3" (uuid "{uuid.uuid4()}"))
		(pin "4" (uuid "{uuid.uuid4()}"))
		(pin "5" (uuid "{uuid.uuid4()}"))
		(pin "6" (uuid "{uuid.uuid4()}"))
		(pin "7" (uuid "{uuid.uuid4()}"))
		(pin "8" (uuid "{uuid.uuid4()}"))
		(instances
			(project "VFBMS32"
				(path "/a2322edc-ff52-449c-92df-24faffac0236" (reference "U_SSR1") (unit 1))
			)
		)
	)

	(symbol (lib_id "Device:R")
		(at 175.0 45.0 90)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{uuid.uuid4()}")
		(property "Reference" "R_G1" (at 175.0 41.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "100R" (at 175.0 48.0 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Resistor_SMD:R_0603_1608Metric" (at 175.0 45.0 0) (hide yes) (effects (font (size 1.27 1.27))))
		(pin "1" (uuid "{uuid.uuid4()}"))
		(pin "2" (uuid "{uuid.uuid4()}"))
		(instances
			(project "VFBMS32"
				(path "/a2322edc-ff52-449c-92df-24faffac0236" (reference "R_G1") (unit 1))
			)
		)
	)

	(symbol (lib_id "Device:R")
		(at 175.0 80.0 90)
		(unit 1)
		(exclude_from_sim no)
		(in_bom yes)
		(on_board yes)
		(dnp no)
		(uuid "{uuid.uuid4()}")
		(property "Reference" "R_G2" (at 175.0 76.0 0) (effects (font (size 1.27 1.27))))
		(property "Value" "100R" (at 175.0 83.0 0) (effects (font (size 1.27 1.27))))
		(property "Footprint" "Resistor_SMD:R_0603_1608Metric" (at 175.0 80.0 0) (hide yes) (effects (font (size 1.27 1.27))))
		(pin "1" (uuid "{uuid.uuid4()}"))
		(pin "2" (uuid "{uuid.uuid4()}"))
		(instances
			(project "VFBMS32"
				(path "/a2322edc-ff52-449c-92df-24faffac0236" (reference "R_G2") (unit 1))
			)
		)
	)

	;; Net Labels connecting ESP32 GPIOs directly to the Gate Drivers / FETs
	(label "PIN_CHG_EN"
		(at 140.0 63.81 180)
		(effects (font (size 1.27 1.27)) (justify right bottom))
		(uuid "{uuid.uuid4()}")
	)
	(label "PIN_OUT_EN"
		(at 140.0 61.27 180)
		(effects (font (size 1.27 1.27)) (justify right bottom))
		(uuid "{uuid.uuid4()}")
	)
	(label "PIN_PSW_EN"
		(at 140.0 58.73 180)
		(effects (font (size 1.27 1.27)) (justify right bottom))
		(uuid "{uuid.uuid4()}")
	)

	;; Gate drive nets
	(label "Q1_GATE"
		(at 187.38 45.0 0)
		(effects (font (size 1.27 1.27)) (justify left bottom))
		(uuid "{uuid.uuid4()}")
	)
	(label "Q2_GATE"
		(at 187.38 80.0 0)
		(effects (font (size 1.27 1.27)) (justify left bottom))
		(uuid "{uuid.uuid4()}")
	)

	;; Power Rails
	(label "CHG+"
		(at 195.0 36.11 90)
		(effects (font (size 1.27 1.27)) (justify left bottom))
		(uuid "{uuid.uuid4()}")
	)
	(label "BAT+"
		(at 195.0 71.11 90)
		(effects (font (size 1.27 1.27)) (justify left bottom))
		(uuid "{uuid.uuid4()}")
	)
	(label "PACK_RAIL"
		(at 195.0 53.89 270)
		(effects (font (size 1.27 1.27)) (justify right bottom))
		(uuid "{uuid.uuid4()}")
	)

	;; ESP32 Microcontroller GPIO Labels (Connecting directly to firmware pins)
	;; ESP32 (U3) at (42.418, 124.206)
	;; Pin 10 (GPIO5, PIN_CHG_EN) is at (42.418 + 22.86 = 65.278, 124.206 - 7.62 = 116.586)
	(label "PIN_CHG_EN"
		(at 66.0 116.586 0)
		(effects (font (size 1.27 1.27)) (justify left bottom))
		(uuid "{uuid.uuid4()}")
	)
	;; Pin 9 (GPIO4, PIN_OUT_EN) is at (42.418 + 22.86 = 65.278, 124.206 - 10.16 = 114.046)
	(label "PIN_OUT_EN"
		(at 66.0 114.046 0)
		(effects (font (size 1.27 1.27)) (justify left bottom))
		(uuid "{uuid.uuid4()}")
	)
	;; Pin 16 (GPIO10, PIN_PSW_EN) is at (42.418 - 22.86 = 19.558, 124.206 + 10.16 = 134.366)
	(label "PIN_PSW_EN"
		(at 18.0 134.366 180)
		(effects (font (size 1.27 1.27)) (justify right bottom))
		(uuid "{uuid.uuid4()}")
	)
	;; Pin 14 (GPIO8, PIN_PCHG_EN) is at (42.418 - 22.86 = 19.558, 124.206 + 15.24 = 139.446)
	(label "PIN_PCHG_EN"
		(at 18.0 139.446 180)
		(effects (font (size 1.27 1.27)) (justify right bottom))
		(uuid "{uuid.uuid4()}")
	)
	;; Pin 15 (GPIO9, PIN_COM_EN) is at (42.418 - 22.86 = 19.558, 124.206 + 12.7 = 136.906)
	(label "PIN_COM_EN"
		(at 18.0 136.906 180)
		(effects (font (size 1.27 1.27)) (justify right bottom))
		(uuid "{uuid.uuid4()}")
	)
	;; Pin 6 (GPIO2, PIN_ENABLE) is at (42.418 - 22.86 = 19.558, 124.206 - 20.32 = 103.886)
	(label "PIN_ENABLE"
		(at 18.0 103.886 180)
		(effects (font (size 1.27 1.27)) (justify right bottom))
		(uuid "{uuid.uuid4()}")
	)
	;; Pin 12 (GPIO6, CAN_RX) is at (42.418 + 22.86 = 65.278, 124.206 - 5.08 = 119.126)
	(label "CAN_RX"
		(at 66.0 119.126 0)
		(effects (font (size 1.27 1.27)) (justify left bottom))
		(uuid "{uuid.uuid4()}")
	)
	;; Pin 13 (GPIO7, CAN_TX) is at (42.418 + 22.86 = 65.278, 124.206 - 2.54 = 121.666)
	(label "CAN_TX"
		(at 66.0 121.666 0)
		(effects (font (size 1.27 1.27)) (justify left bottom))
		(uuid "{uuid.uuid4()}")
	)
'''

# Insert instantiations right before sheet_instances
insert_idx = sch_text.rfind("(sheet_instances")
updated_sch = sch_text[:insert_idx] + instantiations + "\n\t" + sch_text[insert_idx:]

with open(sch_path, "w", encoding="utf-8") as f:
    f.write(updated_sch)

print("Updated VFBMS32.kicad_sch successfully!")
