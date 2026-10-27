from PIL import Image

im = Image.open("scratch/test_render_top.png")
bbox = im.getbbox()
if bbox:
    pad = 10
    box = (max(0, bbox[0]-pad), max(0, bbox[1]-pad), min(im.width, bbox[2]+pad), min(im.height, bbox[3]+pad))
    cropped_board = im.crop(box)
    cropped_board.save("scratch/board_cropped.png")
    w, h = cropped_board.size
    print(f"Board cropped size: {w}x{h}")
    
    # 130mm x 32mm
    # box 1: (13.4, 30.7)
    # box 2: (15.1, 1.13)
    x1 = int(13.4 / 130.0 * w)
    y1 = int(30.7 / 32.0 * h)
    
    x2 = int(15.1 / 130.0 * w)
    y2 = int(1.13 / 32.0 * h)
    
    c1 = cropped_board.crop((max(0, x1 - 100), max(0, y1 - 80), min(w, x1 + 100), min(h, y1 + 80)))
    c1.save("scratch/render_crop_box1.png")
    
    c2 = cropped_board.crop((max(0, x2 - 100), max(0, y2 - 80), min(w, x2 + 100), min(h, y2 + 80)))
    c2.save("scratch/render_crop_box2.png")
    print("Saved crop 1 and crop 2")
