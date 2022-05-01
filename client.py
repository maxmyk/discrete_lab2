import socket
import threading
from rsa_module import RSA

class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_ip = server_ip
        self.port = port
        self.my_client = RSA()
        self.username = username

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return
        usern = self.username + ' ' + str(self.my_client.e) + ' ' + str(self.my_client.n)
        self.s.send(usern.encode())

        key = self.s.recv(1024).decode()
        self.server_key_e = key.split()[0]
        self.server_key_n = key.split()[1]

        message_handler = threading.Thread(target=self.read_handler, args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler, args=())
        input_handler.start()

    def read_handler(self): 
        while True:
            message = self.s.recv(1024).decode()
            if message[:3] != "new":
                message, message_hash = message.split('/')[0], message.split('/')[1]
                message = self.my_client.decrypt(message)
                if message_hash == str(self.my_client.hash(message)):
                    print(message)
                else:
                    pass
            else:
                pass

    def write_handler(self):
        while True:
            message = input()
            message_hash = self.my_client.hash(message)
            brunch = str(message_hash) + '/' + self.my_client.encrypt(message, (self.server_key_e, self.server_key_n))
            self.s.send(brunch.encode())

if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001, "b_g")
    cl.init_connection()
