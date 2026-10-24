import os
from PIL import Image

for fname in os.listdir('_reference/user_photos'):
    if fname.endswith(('.jpg', '.png')):
        path = os.path.join('_reference/user_photos', fname)
        im = Image.open(path)
        print(fname, im.size)
