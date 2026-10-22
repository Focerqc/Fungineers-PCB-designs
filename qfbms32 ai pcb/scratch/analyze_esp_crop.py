from PIL import Image

# Let's inspect the cropped zoom images
im_hd = Image.open('scratch/esp_usb_zoom_hd.png')
print("HD crop size:", im_hd.size)

im_master = Image.open('scratch/esp_usb_zoom_master.png')
print("Master crop size:", im_master.size)

# The board dimensions are 140.0mm x 32.0mm
# In master ref (944x291):
# 944 px / 140 mm ~= 6.74 px/mm
# 291 px / 32 mm ~= 9.09 px/mm (with margins)

# Let's crop very tightly around USB, U7, ESP32 on master ref and save as distinct crops
# USB is at ~125mm, ESP32 is at ~106.5mm
# So in master (944px wide), 100mm -> x = ~674px, 140mm -> x = ~944px
crop_detail = im_master.crop((im_master.width - 250, 0, im_master.width, im_master.height))
crop_detail.save('scratch/esp_usb_detail_master.png')
print("Saved scratch/esp_usb_detail_master.png")
