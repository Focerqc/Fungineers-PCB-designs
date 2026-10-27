import os
import shutil

src_dump = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\scratch\firmware_dump"
dst_ref1 = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\_reference\firmware"
dst_ref2 = r"c:\Users\quinn\Desktop\AI PCB CAD\_reference\firmware"

os.makedirs(dst_ref1, exist_ok=True)
os.makedirs(dst_ref2, exist_ok=True)

# Also ensure hw.h and hw.c are properly named
# Note that in vesc_express the files are named hw_vbms32.h and hw_vbms32.c, but we should also provide aliases hw.h and hw.c for clarity
copied_files = []
if os.path.exists(src_dump):
    for fname in os.listdir(src_dump):
        src_path = os.path.join(src_dump, fname)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, os.path.join(dst_ref1, fname))
            shutil.copy2(src_path, os.path.join(dst_ref2, fname))
            copied_files.append(fname)

# Copy hw_vbms32.h as hw.h and hw_vbms32.c as hw.c as well
if os.path.exists(os.path.join(dst_ref1, "hw_vbms32.h")):
    shutil.copy2(os.path.join(dst_ref1, "hw_vbms32.h"), os.path.join(dst_ref1, "hw.h"))
    shutil.copy2(os.path.join(dst_ref1, "hw_vbms32.h"), os.path.join(dst_ref2, "hw.h"))
if os.path.exists(os.path.join(dst_ref1, "hw_vbms32.c")):
    shutil.copy2(os.path.join(dst_ref1, "hw_vbms32.c"), os.path.join(dst_ref1, "hw.c"))
    shutil.copy2(os.path.join(dst_ref1, "hw_vbms32.c"), os.path.join(dst_ref2, "hw.c"))

# Clean up raw scratch dump
shutil.rmtree(src_dump, ignore_errors=True)

print("Saved all firmware files permanently to _reference/firmware/:")
for f in os.listdir(dst_ref1):
    sz = os.path.getsize(os.path.join(dst_ref1, f))
    print(f"  {f:25} ({sz} bytes)")
