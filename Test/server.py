import socket
import threading

HEADER = 64  # header for how long it is
HOST = socket.gethostbyname(socket.gethostname())
print(HOST)
PORT = 5001
ADDR = (HOST, PORT)
FORMAT = "utf-8"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)
server.listen()

def handle_client(connection, addr):
    print(f"new connection from {addr}")
    conn = True
    while conn:
        length = connection.recv(HEADER).decode(FORMAT)
        if len(length) > 0:
            length = int(length[:HEADER])
            msg = connection.recv(length).decode(FORMAT)
            if msg == 'disconnect':
                conn = False
            print(msg)

while True:
    clientsock, foreign_address = server.accept()
    print('Connected by', foreign_address)
    thread = threading.Thread(target=handle_client, args=(clientsock, foreign_address))
    thread.start()
