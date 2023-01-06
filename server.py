clients_responsability = {1: '0.0.0.0',
                          2: '0.0.0.0',
                          3: '0.0.0.0',
                          4: '0.0.0.0'}
WINDOW_LENGTH = 50
WINDOW_WIDTH = 50

"""
msgs format: | - to split each bit in the 2 dimensional array
             _ - to split each line in the 2 dimensional array
             # - separate fields in the msg
             
"""


def get_pixels_to_clients(y_pos, x_pos, client_ip):
    """
    sends a y position, x position, length, width to each client based on their role
    :param y_pos: the picture's position of the client
    :param x_pos:
    :return:
    """

    current_role = 0
    for role, ip in clients_responsability.items():
        if ip == client_ip:
            current_role = role

    left_y_pos = 0
    left_x_pos = 0
    length = 0
    width = 0
    if current_role == 1:
        left_y_pos, left_x_pos, length, width = get_role1_pos(x_pos, y_pos)
    elif current_role == 2:
        left_y_pos, left_x_pos, length, width = get_role2_pos(x_pos, y_pos)
    elif current_role == 3:
        left_y_pos, left_x_pos, length, width = get_role3_pos(x_pos,y_pos)
    elif current_role ==  4:
        left_y_pos, left_x_pos, length, width = get_role4_pos(x_pos,y_pos)
    return left_y_pos, left_x_pos, length, width

def get_role1_pos(x_pos, y_pos):
    left_y_pos = 0
    left_x_pos = 0
    length = 0
    width = 0

    if 100 > x_pos > 100 - WINDOW_WIDTH:
        left_x_pos = 0
        width = WINDOW_WIDTH - (100 - x_pos)
    elif x_pos >= 100:
        left_x_pos = x_pos
        width = WINDOW_WIDTH
    else:
        left_x_pos = -1

    if left_x_pos == -1 or y_pos >= 100:
        left_y_pos = -1
        left_x_pos = -1
        length = -1
        width = -1

    elif 0 < y_pos < WINDOW_LENGTH:
        left_y_pos = y_pos
        length = WINDOW_LENGTH
    elif 100 > y_pos >= WINDOW_LENGTH:
        left_y_pos = y_pos
        length = 100 - y_pos

    return left_y_pos, left_x_pos, length, width


def get_role2_pos(x_pos, y_pos):
    left_y_pos = 0
    left_x_pos = 0
    length = 0
    width = 0

    if 100 > x_pos >= WINDOW_WIDTH:
        left_x_pos = x_pos
        width = 100 - x_pos
    elif 0 < x_pos < WINDOW_WIDTH:
        left_x_pos = x_pos
        width = WINDOW_WIDTH
    else:
        left_x_pos = -1

    if left_x_pos == -1 or y_pos >= 100:
        left_y_pos = -1
        left_x_pos = -1
        length = -1
        width = -1

    elif 0 < y_pos < WINDOW_LENGTH:
        left_y_pos = y_pos
        length = WINDOW_LENGTH

    elif 100 > y_pos >= WINDOW_LENGTH:
        left_y_pos = y_pos
        length = 100 - y_pos

    return left_y_pos, left_x_pos, length, width


def get_role3_pos(x_pos, y_pos):
    left_y_pos = 0
    left_x_pos = 0
    length = 0
    width = 0
    if 100 > x_pos >= WINDOW_WIDTH:
        left_x_pos = x_pos
        width = 100 - x_pos
    elif 0 < x_pos < WINDOW_WIDTH:
        left_x_pos = x_pos
        width = WINDOW_WIDTH
    else:
        left_x_pos = -1

    if left_x_pos == -1 or y_pos < 100 - WINDOW_LENGTH:
        left_y_pos = -1
        left_x_pos = -1
        length = -1
        width = -1
    elif y_pos >= 100:
        length = WINDOW_LENGTH
        left_y_pos = y_pos - 100
    elif y_pos < 100:
        left_y_pos = 0
        length = WINDOW_LENGTH - (100 - y_pos)

    return left_y_pos, left_x_pos, length, width


def get_role4_pos(x_pos, y_pos):
    left_y_pos = 0
    left_x_pos = 0
    length = 0
    width = 0

    if 100 > x_pos > 100 - WINDOW_WIDTH:
        left_x_pos = 0
        width = WINDOW_WIDTH - (100 - x_pos)
    elif x_pos >= 100:
        left_x_pos = x_pos
        width = WINDOW_WIDTH
    else:
        left_x_pos = -1

    if left_x_pos == -1 or y_pos < 100 - WINDOW_LENGTH:
        left_y_pos = -1
        left_x_pos = -1
        length = -1
        width = -1
    elif y_pos >= 100:
        length = WINDOW_LENGTH
        left_y_pos = y_pos - 100
    elif y_pos < 100:
        left_y_pos = 0
        length = WINDOW_LENGTH - (100 - y_pos)

    return left_y_pos, left_x_pos, length, width
