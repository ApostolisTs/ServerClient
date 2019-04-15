import socket
import os


class Server(object):
    def __init__(self):
        self.port = 8888
        # self.host = ''

    def start(self):
        self.create_socket()
        self.bind_socket()
        self.accept_connections()

    def create_socket(self):
        try:
            self.server_socket = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as e:
            print(f'ERROR CREATING SERVER SOCKET!\n{str(e)}')

    def bind_socket(self):
        try:
            self.server_socket.bind((socket.gethostname(), self.port))
            self.server_socket.listen()
            print('Server waiting for connections...')
        except socket.error as e:
            print(f'ERROR BINDING SOCKET!\n{str(e)}\nTrying again!')
            self.bind_socket()

    def accept_connections(self):
        client_socket, client_address = self.server_socket.accept()
        print(f'Connection with {client_address} has been established.')
        client_socket.send(f'Welcome to {socket.gethostname()}'.encode())

        while True:
            msg = client_socket.recv(1024)

            if msg.decode('utf-8') == 'exit':
                client_socket.close()
                self.server_socket.close()
                break
                exit(1)
            else:
                print(msg.decode('utf-8'))
                client_socket.send(msg)


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    server = Server()
    server.start()
