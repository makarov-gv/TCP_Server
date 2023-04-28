import cv2
import socket
import struct
import pickle
import smbus2
import imutils

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.118.113', 8485))  # server ip address

cam = cv2.VideoCapture(0)
img_counter = 0

bus = smbus2.SMBus(1)
address = 0x08

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    ret, frame = cam.read()
    if ret:
        frame = imutils.resize(frame, width=320)
        result, image = cv2.imencode('.jpg', frame, encode_param)
        data = pickle.dumps(image, 0)
        size = len(data)

        client_socket.sendall(struct.pack(">L", size) + data)

    msg = client_socket.recv(1024)
    try:
        if msg is not None:
            bus.write_byte(address, int(msg))
        else:
            bus.write_byte(address, 0)
    except:
        pass
