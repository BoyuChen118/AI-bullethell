import socket
from time import sleep

HEADER = 64  # header for how long it is
HOST = "10.0.0.199"  # this should be whatever the host name is
PORT = 37059
FORMAT = "utf-8"
ADDR = (HOST, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
# new message 
msg = "endserve"
msg = msg.encode(FORMAT)
msg_length = len(msg)
if msg_length <= HEADER:
    header_length = len(str(msg_length).encode(FORMAT))
    client.send(str(msg_length).encode(FORMAT)+str(' '*(HEADER - header_length)).encode(FORMAT)+msg)
    #client.send(msg)
    sleep(5)
    msg = "endserver"
    msg = msg.encode(FORMAT)
    msg_length = len(msg)
    header_length = len(str(msg_length).encode(FORMAT))
    client.send(str(msg_length).encode(FORMAT)+str(' '*(HEADER - header_length)).encode(FORMAT))
    client.send(msg)
    
else:
    print("message is too long")
client.close()