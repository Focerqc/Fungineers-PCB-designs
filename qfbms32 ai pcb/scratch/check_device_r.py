with open('VFBMS32.kicad_sch', 'r', encoding='utf-8') as f:
    text = f.read()

pos_r = text.find('(symbol "Device:R"')
if pos_r != -1:
    end_r = text.find('\n\t\t(symbol "', pos_r + 1)
    if end_r == -1:
        end_r = text.find('\n\t)', pos_r + 1)
    print("Device:R in lib_symbols:")
    print(text[pos_r:end_r])
