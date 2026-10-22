from PIL import Image

try:
    img = Image.open('_reference/vfbms32_real_top_hd.png')
    w, h = img.size
    print(f"real top hd: {w}x{h}")
    crop = img.crop((int(w * 0.65), 0, w, h))
    crop.save('scratch/crop_esp_usb.png')
    print("Saved scratch/crop_esp_usb.png")
except Exception as e:
    print(e)

try:
    img2 = Image.open('_reference/vfbms32_v1_2_master_reference.png')
    w, h = img2.size
    print(f"master: {w}x{h}")
    crop2 = img2.crop((int(w * 0.65), 0, w, h))
    crop2.save('scratch/crop_master_esp_usb.png')
    print("Saved scratch/crop_master_esp_usb.png")
except Exception as e:
    print(e)

try:
    img3 = Image.open('_reference/user_photos/IMG_0916.jpg')
    w, h = img3.size
    print(f"IMG_0916: {w}x{h}")
    crop3 = img3.crop((int(w * 0.5), int(h * 0.2), w, int(h * 0.8)))
    crop3.save('scratch/crop_img0916.png')
    print("Saved scratch/crop_img0916.png")
except Exception as e:
    print(e)
