import shutil
import os

src = r"C:\Users\quinn\.gemini\antigravity-ide\brain\b988a972-63be-4423-9bf0-ac3c0e64f999\.user_uploaded\media_1790929582915.png"
dst = r"c:\Users\quinn\Desktop\AI PCB CAD\Q VFBMS32 AI PCB\_reference\user_photos\image_3023b2.png"
shutil.copyfile(src, dst)
print("Copied to:", dst)
