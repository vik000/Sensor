import socket

HEADER = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))

while True:
    full_msg = ''
    new_msg = True
    while True:
        msg = s.recv(128)
        if new_msg:
            msg_len = int(msg[:HEADER])
            new_msg = False

        full_msg += msg.decode("utf-8")
        if len(full_msg) - HEADER == msg_len:
            print(full_msg[HEADER:])
            new_msg = True
            full_msg = ''
