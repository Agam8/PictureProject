import numpy as np
from PIL import Image
import socket, sys, tcp_by_size, traceback

role = '1'
PORT = 7171
picture = b''


def load_pic():
    """
    loads the correct color pixels to the array by its id.
    uses the global pic_id, picture.
    :param
    :return:
    """
    global picture
    if role == '1':
        img = Image.open('color1.jpg')
        picture = np.asarray(img)
    elif role == '2':
        img = Image.open('color2.jpg')
        picture = np.asarray(img)
    elif role == '3':
        img = Image.open('color3.jpg')
        picture = np.asarray(img)
    else:
        img = Image.open('color4.jpg')
        picture = np.asarray(img)


# for the code: part_of_pic(2, 2, 4, 4, pic)
# returns the 2-4 pixels in lines 2-4
# format: [ [[RGB][RGB][RGB]]
#           [[RGB][RGB][RGB]]
#           [[RGB][RGB][RGB]] ]


def part_of_pic(y, x, length, width):
    """
    return the needed part of the pic.
    :param y:
    :param x:
    :param length:
    :param width:
    :return: part of pic
    """
    part = picture[y:length + 1, x:width + 1]
    return part


def handle_data(data):
    global role

    data = data.split('#')
    msg_code = data[0]

    if msg_code == 'GETRL':
        role = data[1]
        load_pic()
        return b'RCVRL#'

    elif msg_code == 'GETPS':
        coordinates = [data[1], data[2], data[3], data[4]]  # y_pos, x_pos, length, width
        data_to_send = part_of_pic(coordinates[0], coordinates[1], coordinates[2], coordinates[3])
        return b'RCVPS#' + str(data_to_send).encode()

    elif msg_code == 'QUITS':
        return 'exit'


def main(ip):
    global PORT
    connected = False
    threads = []
    sock = socket.socket()
    connected = False
    try:
        sock.connect((ip, PORT))
        print(f'Connect succeeded {ip}:{PORT}')
        connected = True
    except:
        print(f'Error while trying to connect.  Check ip or port -- {ip}:{PORT}')

    while connected:
        try:
            while True:
                data = tcp_by_size.recv_by_size(sock).decode()
                to_send = handle_data(data)
                if to_send != 'exit':
                    tcp_by_size.send_with_size(sock, to_send)
                else:
                    connected = False

        except socket.error as err:
            print(f'Got socket error: {err}')
            break
        except Exception as err:
            print(f'General error: {err}')
            print(traceback.format_exc())
            break
    sock.close()


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        main('127.0.0.1')
