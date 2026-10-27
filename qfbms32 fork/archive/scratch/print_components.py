import re

with open('build_qfbms32_layout.py') as f:
    text = f.read()

items = re.findall(r'\{\s*"dir"[^\}]+\}', text, re.DOTALL)
for item in items:
    ref = re.search(r'"ref":\s*"([^"]+)"', item)
    val = re.search(r'"val":\s*"([^"]+)"', item)
    fp = re.search(r'"fp":\s*"([^"]+)"', item)
    x = re.search(r'"x":\s*([\d\.-]+)', item)
    y = re.search(r'"y":\s*([\d\.-]+)', item)
    rot = re.search(r'"rot":\s*([\d\.-]+)', item)
    if ref and x and y:
        print(f"{ref.group(1):10s} {val.group(1) if val else '':15s} {fp.group(1) if fp else '':30s} ({float(x.group(1)):6.2f}, {float(y.group(1)):6.2f}) rot={float(rot.group(1)) if rot else 0.0}")
