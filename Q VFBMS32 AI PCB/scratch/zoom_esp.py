from PIL import Image

# The real board image
img = Image.open('_reference/vfbms32_real_top_hd.png')
w, h = img.size
# Top right area: x from ~0.7 to 1.0, y from 0 to 0.6
crop1 = img.crop((int(w * 0.70), 0, int(w * 0.98), int(h * 0.65)))
crop1.save('scratch/esp_usb_zoom_hd.png')

master = Image.open('_reference/vfbms32_v1_2_master_reference.png')
w, h = master.size
crop2 = master.crop((int(w * 0.70), 0, int(w * 0.98), int(h * 0.65)))
crop2.save('scratch/esp_usb_zoom_master.png')

# Let's also check IMG_0916 where the right side is visible
img16 = Image.open('_reference/user_photos/IMG_0916.jpg')
w, h = img16.size
# Let's find the ESP/USB area
crop3 = img16.crop((int(w * 0.55), int(h * 0.3), int(w * 0.95), int(h * 0.7)))
crop3.save('scratch/esp_usb_zoom_img0916.png')

print("Cropped zooms saved!")
