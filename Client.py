import numpy as np
from PIL import Image
pic_id = 0
pic_size = 100


def load_pic():
    """
    loads the correct color pixels to the array by its id.
    uses the global pic_id, pic_size.
    :param
    :return:picture
    """
    global pic_id, pic_size
    if pic_id == '1':
        img = Image.open("color1.jpg")
        picture = np.asarray(img)
    elif pic_id == '2':
        img = Image.open("color2.jpg")
        picture = np.asarray(img)
    elif pic_id == '3':
        img = Image.open("color3.jpg")
        picture = np.asarray(img)
    else:
        img = Image.open("color4.jpg")
        picture = np.asarray(img)
    return picture

def part_of_pic(y, x, length, width, picture):
    """
    return the needed part of the pic.
    :param y:
    :param x:
    :param length:
    :param width:
    :param picture:
    :return: part of pic
    """
    part = picture[y:length+1, x:width+1]
    return part


def main():
    global pic_id
    pic_id = 1
    pixels = part_of_pic(2, 2, 50, 50, load_pic())


if __name__ == '__main__':
    main()



