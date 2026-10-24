import os
from PIL import Image

# Let's inspect where Q1/SSR appears in these images by creating a thumbnail or finding the region
for fname in ['IMG_0912.jpg', 'IMG_0913.jpg', 'IMG_0916.jpg', 'IMG_0923.jpg']:
    path = os.path.join('_reference/user_photos', fname)
    im = Image.open(path)
    # create thumbnail
    thumb = im.copy()
    thumb.thumbnail((800, 800))
    thumb.save(f'scratch/thumb_{fname}.jpg')

print("Thumbnails generated")
