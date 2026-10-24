import os
from PIL import Image

# Let's crop full resolution from user photos around this area
for img_name in ['IMG_0912.jpg', 'IMG_0913.jpg', 'IMG_0916.jpg', 'IMG_0923.jpg']:
    path = os.path.join('_reference/user_photos', img_name)
    im = Image.open(path)
    # The image is 3024 x 4032. Let's find where the board is.
    # In earlier scripts, let's see how they cropped
    print(f"{img_name} loaded, size {im.size}")
