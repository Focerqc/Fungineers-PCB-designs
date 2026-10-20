with open('Q VFBMS32 AI PCB/VFBMS32.kicad_sch', 'r', encoding='utf-8') as f:
    sch = f.read()

# Let's find where symbol instances start
pos = sch.rfind('(symbol (lib_id "')
print(sch[pos:pos+600])
