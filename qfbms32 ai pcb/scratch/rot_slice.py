from PIL import Image

im = Image.open('scratch/slice_1.jpg')
# rotate 270 or 90 to match user's attached photo
# In slice_1.jpg: AGM15T03LL is at bottom-center, H2440 is above it.
# In user attached photo: AGM15T03LL is on left, H2440 is on right.
# So rotating 90 degrees counter-clockwise (or 270 clockwise) makes it horizontal!
rot = im.rotate(90, expand=True)
rot.save('scratch/slice_1_rot90.jpg')

rot270 = im.rotate(270, expand=True)
rot270.save('scratch/slice_1_rot270.jpg')
print("Rotated")
