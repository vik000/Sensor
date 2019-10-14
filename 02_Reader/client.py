import socket
import logging
from Piper import Pipeline

logging.basicConfig(
    filename='logs.log',
    filemode='w',
    level=logging.INFO,
    format='%(asctime)s : %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S'
)

HEADER = 10
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))
p = Pipeline()
p.start_reader() # this starts reader thread

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
            job = full_msg[HEADER:]
            p.add_worker(job) # each worker is a thread
            new_msg = True
            full_msg = ''
