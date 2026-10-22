import os

search_roots = [
    r"C:\Users\quinn\.gemini",
    r"C:\Users\quinn\AppData\Local\Temp"
]

found = []
for sroot in search_roots:
    for root, dirs, files in os.walk(sroot):
        for f in files:
            if "3023b2" in f:
                found.append(os.path.join(root, f))

print("Found files:", found)
