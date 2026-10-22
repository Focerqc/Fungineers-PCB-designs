import os
import time

now = time.time()
recent = []
for sroot in [r"C:\Users\quinn\.gemini", os.environ.get("TEMP", r"C:\Users\quinn\AppData\Local\Temp")]:
    for root, dirs, files in os.walk(sroot):
        for f in files:
            if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                p = os.path.join(root, f)
                try:
                    mtime = os.path.getmtime(p)
                    if now - mtime < 900: # 15 min
                        recent.append((mtime, p, os.path.getsize(p)))
                except:
                    pass

recent.sort(reverse=True)
for mtime, p, sz in recent[:15]:
    print(f"{time.ctime(mtime)}: {p} ({sz} bytes)")
