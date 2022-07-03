from glob import glob
from random import choices, randint
from PIL import Image


def get_cards(k):
    """Draw k cards with replacement from all cards

    Args:
        k (int): number of cards to be drawn
    Returns:
        list: list of card filenames
    """
    cards = glob("cards/[!asheet]*")
    return choices(cards, k=k)


def make_sheet(cards):
    """Takes n cards and assembles them into a sheet, 5<=n<=1

    Args:
        cards (list of filenames): locations of card files

    Returns:
        string: Assembled .png image file 
    """
    columns = len(cards)
    image_w, image_h = Image.open(cards[0]).size
    grid_image = Image.new(
        "RGB", (columns * image_w + (columns + 1) * 100, image_h + 200)
    )
    grid_image.paste((255, 215, 0), [0, 0, grid_image.size[0], grid_image.size[1]])

    icount = 0
    for i in range(0, columns * image_w, image_w):
        im = Image.open(cards[icount])
        grid_image.paste(im, (i + (icount + 1) * 100, 100))
        icount += 1
    filename = str(randint(0, 10000)) + ".png"
    grid_image.save(filename)
    return filename


def get_slots(k=3):
    """Get an image of k randomly drawn cards from the set

    Args:
        k (int, optional): Number of cards to be drawn. Defaults to 3.

    Returns:
        string: Location of a png file
    """
    cards = get_cards(k)
    sheet = make_sheet(cards)
    return sheet


if __name__ == "__main__":
    get_slots(3)
