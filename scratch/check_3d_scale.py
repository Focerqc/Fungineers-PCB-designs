from PIL import Image
import json

# Check the cropped 3d render
im_3d = Image.open('Q VFBMS32 AI PCB/scratch/vfbms32_3d_top_render.png')
print("3D render cropped size:", im_3d.size)

# Board is 130mm x 32mm
# If width is 130mm, scale is:
scale_x = 130.0 / im_3d.size[0]
scale_y = 32.0 / im_3d.size[1]
print(f"Scale: {scale_x:.4f} mm/px, {scale_y:.4f} mm/px (Ratio: {scale_x/scale_y:.4f})")
