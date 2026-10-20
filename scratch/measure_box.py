from PIL import Image

# Reference rotated image is 812 x 200 pixels? Let's check size
img = Image.open('Q VFBMS32 AI PCB/_reference/vfbms32_cad_top_reference_rotated.png')
print('Reference image size:', img.size)

# Board size in mm is 130.0 x 32.0 mm
# Scale is 130 / img.size[0] mm/px
scale_x = 130.0 / img.size[0]
scale_y = 32.0 / img.size[1]
print(f'Scale: X={scale_x:.4f} mm/px, Y={scale_y:.4f} mm/px')

# In VFBMS32.boxes.json:
# box: x=4.1, y=15.75, w=8.9, h=6.7
# In px:
px_x1 = int((4.1 - 8.9/2) / scale_x)
px_x2 = int((4.1 + 8.9/2) / scale_x)
px_y1 = int((15.75 - 6.7/2) / scale_y)
px_y2 = int((15.75 + 6.7/2) / scale_y)
print(f'Box in pixels: x=[{px_x1}, {px_x2}], y=[{px_y1}, {px_y2}]')

crop = img.crop((max(0, px_x1 - 10), max(0, px_y1 - 10), px_x2 + 20, px_y2 + 10))
crop.save('Q VFBMS32 AI PCB/scratch/cad_box_crop.png')
