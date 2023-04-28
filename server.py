import socket
import cv2
import pickle
import struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

s.bind(('', 8485))
print('Socket bind complete')
s.listen(10)
print('Socket now listening')

conn, addr = s.accept()

data = b""
payload_size = struct.calcsize(">L")
print("payload_size: {}".format(payload_size))
while True:
    while len(data) < payload_size:
        data += conn.recv(4096)
        if not data:
            cv2.destroyAllWindows()
            conn, addr = s.accept()
            continue

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack(">L", packed_msg_size)[0]
    while len(data) < msg_size:
        data += conn.recv(4096)
    frame_data = data[:msg_size]
    data = data[msg_size:]
    frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    key = cv2.waitKey(1)
    message = b"0"
    if key == ord('w'):  # forward
        message = b"1"
    if key == ord('a'):  # turn left
        message = b"2"
    if key == ord('s'):  # turn right
        message = b"9"
    if key == ord('d'):  # turn right
        message = b"3"
    if key == ord('q'):  # lift arm
        message = b"4"
    if key == ord('e'):  # lean arm
        message = b"5"
    if key == ord('1'):  # close arm
        message = b"6"
    if key == ord('2'):  # open arm
        message = b"7"
    if key == ord('r'):  # buzzer
        message = b"8"
    conn.sendall(message)

    frame = cv2.flip(frame, -1)
    frame = cv2.resize(frame, (1920, 1080))
    cv2.imshow('client', frame)
