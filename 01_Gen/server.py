import socket
import time
from Sensor import Data

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 1234))
    s.listen(5)

    HEADERSIZE = 10

    while True:
        clientsocket, address = s.accept()
        print(f"Connection from {address} has been established")

        while True:
            time.sleep(1)
            d = Data()
            msg = d.get_object()
            msg = f'{len(msg):<{HEADERSIZE}}' + msg
            clientsocket.send(bytes(msg, "utf-8"))