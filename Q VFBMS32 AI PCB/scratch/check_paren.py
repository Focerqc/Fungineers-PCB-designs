with open(r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\VFBMS32.kicad_sch", "r", encoding="utf-8") as f:
    text = f.read()

# Let's count parentheses
open_p = text.count('(')
close_p = text.count(')')
print(f"Parentheses: {open_p} open, {close_p} close (diff: {open_p - close_p})")

# Let's check where the mismatch is
depth = 0
for i, ch in enumerate(text):
    if ch == '(':
        depth += 1
    elif ch == ')':
        depth -= 1
        if depth < 0:
            print(f"Negative depth at pos {i}")
            break
print(f"Final depth: {depth}")
