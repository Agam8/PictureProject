import numpy as np
from PIL import Image
import socket, sys, tcp_by_size, traceback
pic_id = '1'
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
    if pic_id == '1':
        img = Image.open('color1.jpg')
        picture = np.asarray(img)
    elif pic_id == '2':
        img = Image.open('color2.jpg')
        picture = np.asarray(img)
    elif pic_id == '3':
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
    :param picture:
    :return: part of pic
    """
    part = picture[y:length+1, x:width+1]
    return part


def handle_client(data):
    global pic_id
    data = data.split('#')
    msg_code = data[0]
    data = data[1]

    if msg_code == 'ROLE':
        pic_id = data.decode()
        load_pic()
        return b'RCVROLE'

    elif msg_code == 'CRDNTS':
        coordinates = data.split(',')
        data_to_send = part_of_pic(coordinates[0], coordinates[1], coordinates[2], coordinates[3])
        return b'PART#' + str(data_to_send).encode()


def main(ip):
    global PORT
    connected = False

    sock = socket.socket()
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
                to_send = handle_client(data)
                tcp_by_size.send_with_size(sock, to_send)

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



