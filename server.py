import socket, threading, pygame, tcp_by_size
clients_roles_sockets = {1: None,
                         2: None,
                         3: None,
                         4: None}
WINDOW_LENGTH = 50
WINDOW_WIDTH = 50
IP = '0.0.0.0'
PORT = 7171
LOCK = threading.Lock()
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,)


"""
msgs format: | - to split each bit in the 2 dimensional array
             _ - to split each line in the 2 dimensional array
             # - separate fields in the msg
             msg_code#data
             
for the code: part_of_pic(2, 2, 4, 4, pic)
returns the 2 - 4 pixels in lines 2 - 4
format: [[[RGB][RGB][RGB]]
         [[RGB][RGB][RGB]]
         [[RGB][RGB][RGB]]]

y, x, length, width: separate by,

msgs format: separate by  #

protocol: ROLE - server to client, sends the client role (1-4)
          RCVROL - client to server, approval for received role
          CRDNTS - server to client, sends the y, x, length, width (by mentioned format)
          PART - client to server, sends the part of the picture the server asked for (by mentioned format)

"""


def find_role(cli_sock):
    for role, sock in clients_roles_sockets.items():
        if sock == cli_sock:
            return role
    return 0


def get_pixels_to_clients(y_pos, x_pos, current_role):
    """
    sends a y position, x position, length, width to each client based on their role
    :param y_pos: the picture's position of the client
    :param x_pos:
    :return:
    """

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


def get_role1_pos(y_pos,x_pos):
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


def get_role2_pos(y_pos, x_pos):
    left_y_pos = 0
    left_x_pos = 0
    length = 0
    width = 0

    if 100 > x_pos >= WINDOW_WIDTH:
        left_x_pos = x_pos
        width = 100 - x_pos
    elif 0 <= x_pos < WINDOW_WIDTH:
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


def get_role3_pos(y_pos, x_pos):
    left_y_pos = 0
    left_x_pos = 0
    length = 0
    width = 0
    if 100 > x_pos >= WINDOW_WIDTH:
        left_x_pos = x_pos
        width = 100 - x_pos
    elif 0 <= x_pos < WINDOW_WIDTH:
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


def get_role4_pos(y_pos,x_pos):
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


def get_open_role(cli_sock):
    global clients_roles_sockets
    open_role = 0
    for role,sock in clients_roles_sockets.items():
        if sock != None:
            LOCK.acquire()
            open_role = role
            clients_roles_sockets[role] = cli_sock
            LOCK.release()
    return open_role


def handle_client(cli_sock):
    role = get_open_role(cli_sock)
    tcp_by_size.send_with_size(cli_sock, b'role')

    y_pos, x_pos = get_cursor_pos()

    while True:
        if role == 1:
            tcp_by_size.send_with_size(cli_sock, get_role1_pos())
        elif role == 2:
            pass
        elif role == 3:
            pass
        else:
            pass


def get_cursor_pos():
    """
    gets cursor position and returns ypos, xpos
    :return:
    """
    return 0, 0


def handle_screen():
    pygame.init()


def main():
    threads = []
    srv_sock = socket.socket()

    srv_sock.bind((IP, PORT))
    srv_sock.listen(20)

    i = 1
    while True:
        print('\nMain thread: before accepting ...')
        cli_sock, addr = srv_sock.accept()
        t = threading.Thread(target=handle_client, args=(cli_sock,srv_sock))
        t.start()
        i += 1
        threads.append(t)
        if i > 100000000:  # for tests change it to 4
            print('\nMain thread: going down for maintenance')
            break

    all_to_die = True
    print('Main thread: waiting to all clints to die')
    for t in threads:
        t.join()
    srv_sock.close()
    print('Bye ..')


if __name__=="__main__":
    main()