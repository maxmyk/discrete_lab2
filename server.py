import socket
import threading
from rsa_module import RSA

class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)
        self.server = RSA()

        while True:
            c, addr = self.s.accept()
            rec = c.recv(1024).decode()
            username = rec.split()[0]
            other_key_e = rec.split()[1]
            other_key_n = rec.split()[2]
            print(f"{username} tries to connect")
            self.broadcast(f'new person has joined: {username}')
            self.username_lookup[c] = (username, (int(other_key_e), int(other_key_n)))
            self.clients.append(c)
            # send public key to the client
            key = str(self.server.e) + ' ' + str(self.server.n)
            c.send(key.encode())

            threading.Thread(target=self.handle_client, args=(c, addr,)).start()

    def broadcast(self, msg: str):
        for client in self.clients:

            client.send(msg.encode())

    def handle_client(self, c: socket, addr): 
        while True:
            msg = c.recv(1024).decode()
            msg_hash, msg = msg.split('/')[0], msg.split('/')[1]
            msg = self.server.decrypt(msg)
            for client in self.clients:
                if client != c:
                    msg = self.server.encrypt(msg, (self.username_lookup[client][1]))
                    brunch = msg + '/' + msg_hash
                    client.send(brunch.encode())


if __name__ == "__main__":
    s = Server(9001)
    s.start()
