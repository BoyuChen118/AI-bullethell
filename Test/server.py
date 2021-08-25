import socket
import threading

client_lock = threading.Lock()
HEADER = 64  # header for how long it is
HOST = socket.gethostbyname(socket.gethostname())
print(HOST)
PORT = 5001
ADDR = (HOST, PORT)
FORMAT = "utf-8"
endServer = False

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(ADDR)

def handle_client(connection, addr):
    global endServer
    client_lock.acquire()
    print(f"new connection from {addr}")
    conn = True
    while conn:
        try:
            # print("BLOCKING BY RECV....")
            length = connection.recv(HEADER).decode(FORMAT)
            print(length)
            if len(length) > 0:
                length = int(length[:HEADER])
                msg = connection.recv(length).decode(FORMAT)
                if msg == 'disconnect' or msg == 'endserver':
                    if msg == 'endserver':
                        endServer = True
                    conn = False
                    client_lock.release()
                    

                print(msg)
        except Exception:
            print(Exception)
            thread.join()

while not endServer:
    server.listen()
    clientsock, foreign_address = server.accept()
    print('Connected by', foreign_address)
    thread = threading.Thread(target=handle_client, args=(clientsock, foreign_address))
    thread.start()
    

server.close()
