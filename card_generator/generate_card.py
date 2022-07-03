import math
from PIL import Image, ImageDraw, ImageFont
from matplotlib import colors
import numpy as np
import sys
import yaml


def point_grid(x, y):
    """Given two arrays of points x & y, generates (x,y)
    coordinate array. x & y do not have to be the same
    size. used for positioning icons on number cards.

    Args:
        x (array): Array of floats
        y (array): Array of floats

    Returns:
        array: 2D array of coordinates, first row is x
        second row is y
    """
    xv, yv = np.meshgrid(x, y)
    return np.stack((np.ravel(xv), np.ravel(yv)))


def symmetric_points(width, height, n):
    """Find points to place suit icons given
    size of card and number of icons

    Args:
        width (int)
        height (int)
        n (string): number of icons to be placed

    Returns:
        array: 2D array of coordinates, first row is x
        second row is y
    """
    margin = max(width // 6, height // 6)
    match n:
        case "1":
            x = width / 2
            y = height / 2
            return np.array([[x], [y]])
        case "2":
            x = np.array(width / 2)
            y = np.array([2 * margin, height - 2 * margin])
            return point_grid(x, y)
        case "3":
            x = np.array(width / 2)
            y = np.ceil(np.linspace(margin, height - margin, num=int(n)))
            return point_grid(x, y)
        case "4" | "6":
            x = np.array([margin, width - margin])
            y = np.ceil(np.linspace(margin, height - margin, num=int(n) // 2))
            return point_grid(x, y)
        case "5":
            four_card = symmetric_points(width, height, "4")
            one_card = symmetric_points(width, height, "1")
            return np.concatenate((one_card, four_card), axis=1)
        case "7":
            six_card = symmetric_points(width, height, "6")
            two_card = symmetric_points(width, height, "2")
            return np.concatenate((two_card[0, :].reshape(2, 1), six_card), axis=1)
        case "8":
            six_card = symmetric_points(width, height, "6")
            two_card = symmetric_points(width, height, "2")
            return np.concatenate((two_card, six_card), axis=1)
        case "9":
            x = np.array([margin, width - margin])
            y = np.ceil(np.linspace(margin, height - margin, num=4))
            eight_card = point_grid(x, y)
            one_card = symmetric_points(width, height, "1")
            return np.concatenate((eight_card, one_card), axis=1)
        case "10":
            x = np.array([margin, width - margin])
            y = np.ceil(np.linspace(margin, height - margin, num=4))
            eight_card = point_grid(x, y)
            two_card = symmetric_points(width, height, "2")
            return np.concatenate((two_card, eight_card), axis=1)

        case _:
            return None


def get_suit_image(suit_name, width, height, color) -> Image:
    """Preprocess suit images to match the color and card size

    Args:
        suit_name (string): 
        width (int): 
        height (int): 
        color (string): 

    Returns:
        Image: sized and colored PIL.Image of the suit icon
    """
    im1 = Image.open("base_images/" + suit_name + ".png")
    data = np.array(im1)  # "data" is a height x width x 4 numpy array
    red, green, blue, alpha = data.T  # Temporarily unpack the bands for readability
    # Replace white with red... (leaves alpha values alone...)
    black_areas = (red < 10) & (blue < 10) & (green < 10)
    float_colors = np.array(colors.to_rgb(color))
    suit_colors = (float_colors * 255).astype(np.byte)
    data[~black_areas.T, :3] = tuple(suit_colors)
    im2 = Image.fromarray(data)
    return im2.resize((width, height))


def generate_card(card_type="5", suit="heart", species="cyber", color="Violet"):
    """Generates a playing card given the characteristics

    Args:
        card_type (str, optional): Card number or face card letter, use 1 for Aces. Defaults to "5".
        suit (str, optional): heart, diamond, spade or club. Defaults to "heart".
        species (str, optional): zombie, original, cyber or hoodie. Defaults to "cyber".
        color (str, optional): colors for each suit, usually loaded from presets.yaml. Defaults to "Violet".

    Returns:
        None: If it worked, a card of the given description is saved under cards/
    """
    width = 1280
    height = 1800
    canvas_size = (width, height)
    bg_color = (0, 0, 0)
    image = Image.new("RGB", size=canvas_size, color=bg_color)
    font = ImageFont.truetype("junegull.ttf", height // 10)
    points = symmetric_points(width, height, card_type)
    if card_type.isdigit():
        suit_width = width // 6
        suit_height = height // 7
        suit_image = get_suit_image(suit, suit_width, suit_height, color)
        for i in range(int(card_type)):
            image.paste(
                suit_image,
                (
                    math.ceil(points[0, i] - suit_width / 2),
                    math.ceil(points[1, i] - suit_height / 2),
                ),
            )
    elif card_type == "K" or "Q" or "J":
        base_image = presets[species][card_type]
        im = Image.open("base_images/" + base_image)
        newsize = (math.ceil(height / 3), math.ceil(height / 3))
        im_w, im_h = im.size
        im1 = im.crop((0, 0, im_w, im_h - 60))
        im1 = im1.resize(newsize)
        paste_loc = (width // 4, height // 6)
        Image.Image.paste(image, im1, paste_loc)
        image = image.rotate(180)
        Image.Image.paste(image, im1, paste_loc)

    else:
        draw = ImageDraw.Draw(image)
        draw.text((width // 2, height // 2), text=f"?", font=font, fill=color)

    text_pos = (width // 60, height // 60)
    card_text = "A" if card_type == "1" else card_type
    draw = ImageDraw.Draw(image)
    draw.text(text_pos, text=f"{card_text}", font=font, fill=color)
    image = image.rotate(angle=180, expand=False)
    draw = ImageDraw.Draw(image)
    draw.text(text_pos, text=f"{card_text}", font=font, fill=color)
    image = image.rotate(angle=180, expand=False)
    image.save(f"cards/{species}_{card_text}.png")
    return None


if __name__ == "__main__":
    if len(sys.argv) > 1:
        inp = sys.argv[1]
        if inp == "all":
            nums = [str(a) for a in range(1, 11)] + ["J", "Q", "K"]
            with open("card_generator/presets.yaml", "r") as stream:
                presets = yaml.safe_load(stream)
            for species in ["zombie", "cyber", "original", "hoodie"]:
                color = presets[species]["color"]
                suit = presets[species]["suit"]
                for num in nums:
                    generate_card(
                        card_type=num, suit=suit, species=species, color=color
                    )
        else:
            generate_card(inp)

    else:
        inp = "10"
        generate_card(card_type=inp)
