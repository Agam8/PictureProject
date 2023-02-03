import socket, threading, pygame, tcp_by_size

clients_roles_sockets = {1: None,
                         2: None,
                         3: None,
                         4: None}
PIC_LENGTH = 50
PIC_WIDTH = 50
WINDOW_LENGTH = 200
WINDOW_WIDTH = 200
IP = '0.0.0.0'
PORT = 7171
LOCK = threading.Lock()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
X_POS = 0
Y_POS = 0
MOVED = False


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


msgs format: separate by  #

protocol: GETRL - server to client, sends the client role (1-4)
          RCVRL - client to server, approval for received role
          GETPS - server to client, sends the y, x, length, width (by mentioned format)
          RCVPS - client to server, sends the part of the picture the server asked for (by mentioned format)

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
        left_y_pos, left_x_pos, length, width = get_role3_pos(x_pos, y_pos)
    elif current_role == 4:
        left_y_pos, left_x_pos, length, width = get_role4_pos(x_pos, y_pos)
    return str(left_y_pos), str(left_x_pos), str(length), str(width)


def get_role1_pos(y_pos, x_pos):
    left_y_pos = 0
    left_x_pos = 0
    length = 0
    width = 0

    if 100 > x_pos > 100 - PIC_WIDTH:
        left_x_pos = 0
        width = PIC_WIDTH - (100 - x_pos)
    elif x_pos >= 100:
        left_x_pos = x_pos
        width = PIC_WIDTH
    else:
        left_x_pos = -1

    if left_x_pos == -1 or y_pos >= 100:
        left_y_pos = -1
        left_x_pos = -1
        length = -1
        width = -1

    elif 0 < y_pos < PIC_LENGTH:
        left_y_pos = y_pos
        length = PIC_LENGTH
    elif 100 > y_pos >= PIC_LENGTH:
        left_y_pos = y_pos
        length = 100 - y_pos

    return left_y_pos, left_x_pos, length, width


def get_role2_pos(y_pos, x_pos):
    left_y_pos = 0
    left_x_pos = 0
    length = 0
    width = 0

    if 100 > x_pos >= PIC_WIDTH:
        left_x_pos = x_pos
        width = 100 - x_pos
    elif 0 <= x_pos < PIC_WIDTH:
        left_x_pos = x_pos
        width = PIC_WIDTH
    else:
        left_x_pos = -1

    if left_x_pos == -1 or y_pos >= 100:
        left_y_pos = -1
        left_x_pos = -1
        length = -1
        width = -1

    elif 0 < y_pos < PIC_LENGTH:
        left_y_pos = y_pos
        length = PIC_LENGTH

    elif 100 > y_pos >= PIC_LENGTH:
        left_y_pos = y_pos
        length = 100 - y_pos

    return left_y_pos, left_x_pos, length, width


def get_role3_pos(y_pos, x_pos):
    left_y_pos = 0
    left_x_pos = 0
    length = 0
    width = 0
    if 100 > x_pos >= PIC_WIDTH:
        left_x_pos = x_pos
        width = 100 - x_pos
    elif 0 <= x_pos < PIC_WIDTH:
        left_x_pos = x_pos
        width = PIC_WIDTH
    else:
        left_x_pos = -1

    if left_x_pos == -1 or y_pos < 100 - PIC_LENGTH:
        left_y_pos = -1
        left_x_pos = -1
        length = -1
        width = -1
    elif y_pos >= 100:
        length = PIC_LENGTH
        left_y_pos = y_pos - 100
    elif y_pos < 100:
        left_y_pos = 0
        length = PIC_LENGTH - (100 - y_pos)

    return left_y_pos, left_x_pos, length, width


def get_role4_pos(y_pos, x_pos):
    left_y_pos = 0
    left_x_pos = 0
    length = 0
    width = 0

    if 100 > x_pos > 100 - PIC_WIDTH:
        left_x_pos = 0
        width = PIC_WIDTH - (100 - x_pos)
    elif x_pos >= 100:
        left_x_pos = x_pos
        width = PIC_WIDTH
    else:
        left_x_pos = -1

    if left_x_pos == -1 or y_pos < 100 - PIC_LENGTH:
        left_y_pos = -1
        left_x_pos = -1
        length = -1
        width = -1
    elif y_pos >= 100:
        length = PIC_LENGTH
        left_y_pos = y_pos - 100
    elif y_pos < 100:
        left_y_pos = 0
        length = PIC_LENGTH - (100 - y_pos)
    return left_y_pos, left_x_pos, length, width


def get_open_role(cli_sock):
    global clients_roles_sockets
    open_role = 0
    for role, sock in clients_roles_sockets.items():
        if sock != None:
            LOCK.acquire()
            open_role = role
            clients_roles_sockets[role] = cli_sock
            LOCK.release()
    return open_role

def handle_send(cli_sock, req, role, y_pos= 0, x_pos= 0):
    global clients_roles_sockets
    data = ''
    if req == 'GETRL':
        data += req + '#' + role
    elif req == 'GETPS':
        y_pos, x_pos, length, width =  get_pixels_to_clients(y_pos,x_pos,role)
        data += req + '#' +y_pos  + '#' +x_pos + '#' +length + '#' + width
    elif req == 'QUITS':

        data += 'QUITS'
    tcp_by_size.send_with_size(cli_sock,data.encode())
def handle_recv(cli_sock):
    pass
    recv =  tcp_by_size.recv_by_size(cli_sock)
    data = recv.split(b'#')
    code = data[0]
    if code == b'RCVPS':
        pass



def handle_client(cli_sock, screen):
    global MOVED
    role = get_open_role(cli_sock)
    handle_send(cli_sock, 'GETRL', role)

    y_pos, x_pos = get_cursor_pos()
    finish = False
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            if event.type == pygame.KEYDOWN:
                MOVED = False
                if event.key == pygame.K_UP:
                    set_cursor_pos(y_pos - 1, x_pos)
                elif event.key == pygame.K_DOWN:
                    set_cursor_pos(y_pos + 1, x_pos)
                elif event.key == pygame.K_RIGHT:
                    set_cursor_pos(y_pos, x_pos + 1)
                elif event.key == pygame.K_LEFT:
                    set_cursor_pos(y_pos, x_pos -1)
                handle_send(cli_sock, 'GETPS', role,y_pos,x_pos)
                recv_pic = handle_recv(cli_sock)

    if finish:
        handle_send(cli_sock,'QUITS',role)


def get_cursor_pos():
    """
    gets cursor position and returns ypos, xpos
    :return:
    """
    return Y_POS, X_POS

def set_cursor_pos(y_pos, x_pos):
    global X_POS, Y_POS, MOVED
    if not MOVED:
        X_POS = x_pos
        Y_POS = y_pos
        MOVED = True



def init_screen():
    global X_POS, Y_POS
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_LENGTH,WINDOW_WIDTH))
    pygame.display.set_caption("Server's View")
    screen.fill(BLACK)
    pygame.draw.line(screen, WHITE, [0, WINDOW_WIDTH / 2], [WINDOW_LENGTH, WINDOW_WIDTH / 2], 2)
    pygame.draw.line(screen, WHITE, [WINDOW_LENGTH / 2, 0], [WINDOW_LENGTH / 2, WINDOW_WIDTH], 2)
    pygame.display.flip()
    X_POS = WINDOW_WIDTH + PIC_WIDTH
    Y_POS = WINDOW_LENGTH + PIC_LENGTH
    return screen


def main():
    threads = []
    srv_sock = socket.socket()

    srv_sock.bind((IP, PORT))
    srv_sock.listen(20)
    screen = init_screen()
    i = 1
    while True:
        print('\nMain thread: before accepting ...')
        cli_sock, addr = srv_sock.accept()
        print('accepted a client')
        finish = False
        while not finish:
            t = threading.Thread(target=handle_client, args=(cli_sock, screen))
            t.start()
        i += 1
        threads.append(t)
        if i > 100000000:  # for tests change it to 4
            print('\nMain thread: going down for maintenance')
            break

    all_to_die = True
    print('Main thread: waiting to all clients to die')
    for t in threads:
        t.join()
    srv_sock.close()
    print('Bye ..')


if __name__ == "__main__":
    main()
