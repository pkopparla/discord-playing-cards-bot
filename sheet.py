import math
from PIL import Image
from glob import glob

"""
Generates collection sheets for each suit of cards for easy
visualization. Just type python sheet.py
"""
for species in ["zombie", "cyber", "original", "hoodie"]:
    cards = glob(f"cards/{species}_*")
    cards.sort()
    count = len(cards)
    rows, columns = 2, math.ceil(count / 2)
    image_w, image_h = Image.open(cards[0]).size
    grid_image = Image.new("RGB", (columns * image_w, rows * image_h))
    grid_image.paste((200, 200, 200), [0, 0, grid_image.size[0], grid_image.size[1]])

    icount = 0
    for i in range(0, columns * image_w, image_w):
        for j in range(0, rows * image_h, image_h):
            # paste the image at location i,j:
            if icount == count:
                break
            im = Image.open(cards[icount])
            grid_image.paste(im, (i, j))
            # print(i, j, cards[icount])
            icount += 1

    grid_image.save(f"cards/asheet_{species}.png")
print("done!")
