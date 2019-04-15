import socket
import os


class Client(object):
    def __init__(self):
        self.port = 8888
        # self.server_add = '10.140.5.104'

    def start(self):
        client.create_socket()
        client.connect_to_server()
        client.send_messages()

    def create_socket(self):
        try:
            self.client_socket = socket.socket()
        except socket.error as e:
            print(f'ERROR CREATING CLIENT SOCKET!\n{str(e)}')

    def connect_to_server(self):
        self.client_socket.connect((socket.gethostname(), self.port))
        msg = self.client_socket.recv(1024)
        print(msg.decode('utf-8'))

    def send_messages(self):
        while True:
            msg = input()
            self.client_socket.send(msg.encode())

            if msg == 'exit':
                self.client_socket.close()
                break
                exit(1)

            reply = self.client_socket.recv(1024)
            print(f'Server reply: {reply.decode("utf-8")}')


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    client = Client()
    client.start()
