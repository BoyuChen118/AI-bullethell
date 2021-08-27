import socket
import threading


class GameServer:
    def __init__(self,port):
        self.client_lock = threading.Lock()
        self.HEADER = 64  # header for how long it is
        self.HOST = socket.gethostbyname(socket.gethostname())
        print(self.HOST)
        print(socket.gethostname())
        self.PORT = port     # 37059
        self.ADDR = (self.HOST, self.PORT)
        self.FORMAT = "utf-8"
        self.endServer = False
        self.clientsock = None
        self.foreign_address = None
        self.isWaiting = True
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
          
    def handle_client(self,connection, addr):
        self.client_lock.acquire()
        print(f"new connection from {addr}")
        conn = True
        while conn:
            try:
                # print("BLOCKING BY RECV....")
                length = connection.recv(self.HEADER).decode(self.FORMAT)
                if len(length) > 0:
                    length = int(length[:self.HEADER])
                    msg = connection.recv(length).decode(self.FORMAT)
                    if msg == 'disconnect' or msg == 'endserver':
                        if msg == 'endserver':
                            self.endServer = True
                        conn = False
                        self.client_lock.release()
                    print(msg)
            except Exception:
                print(Exception)
                break
    def WaitForClient(self):
        self.server.bind(self.ADDR)
        self.server.listen()
        self.clientsock, self.foreign_address = self.server.accept()
        self.isWaiting = False
        print("client connected")
    def wait_client(self):
        waitingThread = threading.Thread(target=self.WaitForClient)
        waitingThread.start()
    def connect_client(self,func):
        if not self.endServer:
            print('Connected by', self.foreign_address)
            thread = threading.Thread(target=func, args=(self.clientsock, self.foreign_address))
            thread.start()
        # while not self.endServer:
        #     pass
        self.server.close()
        
if __name__ == '__main__':
    gameserver = GameServer(port=37059)
    gameserver.wait_client()
    while gameserver.isWaiting:
        print("I'm WAITING!!")
    gameserver.connect_client(gameserver.handle_client)


   

    
