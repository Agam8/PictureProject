import numpy as np
from Colors import color_string_to_rgb
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
        color = color_string_to_rgb("green")
    elif pic_id == '2':
        color = color_string_to_rgb("red")
    elif pic_id == '3':
        color = color_string_to_rgb("teal")
    else:
        color = color_string_to_rgb("purple")
    picture = np.full((pic_size, pic_size), color)
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
    print(part)


def main():
    global pic_id
    pic_id = 1
    part_of_pic(2, 2, 50, 50, load_pic())


if __name__ == '__main__':
    main()



