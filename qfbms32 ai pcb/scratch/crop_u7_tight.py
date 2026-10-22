from PIL import Image

# Let's inspect the U7 image from the master ref and real HD
im = Image.open('scratch/esp_usb_detail_master.png')
print("Detail master size:", im.size)
# In detail master, let's find the bounding box of U7
# On the board, the right edge has USB on top, ESP32 on left, U7 is situated next to ESP32 / below USB
# Let's crop right around U7
# In detail_master (width 250, height 189):
# U7 is around x: 120..200, y: 50..120
crop_u7 = im.crop((120, 50, 210, 130))
crop_u7.save('scratch/u7_tight.png')
print("Saved scratch/u7_tight.png")
