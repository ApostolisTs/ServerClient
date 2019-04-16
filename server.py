import socket
import os
import sys
from multiprocessing import Process, Lock
from time import sleep


class Server(object):
    """ Implements a Server class which is handling a flights list.
    Clients can execute reads/writes on that list concurrently. """

    def __init__(self):
        self.port = 8888
        self.lock = Lock()
        self.flights = []
        # self.host = ''

    def start(self):
        """ Gets the server running. """

        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((socket.gethostname(), self.port))
        server_sock.listen()
        print('Server running...')

        self.accept_connections(server_sock)

    def accept_connections(self, server_sock):
        """ Accepts connections from clients and creates a new process for each
        client. """

        while True:
            client_sock, client_address = server_sock.accept()
            print(f'Connection with {client_address} has been established.')
            client_sock.send(socket.gethostname().encode())

            client_process = Process(
                target=self.handle_connection, args=(client_sock,))
            client_process.start()

        socket.close()

    def handle_connection(self, client_sock):
        while True:
            command = client_sock.recv(1024).decode('utf-8')

            if 'exit' in command:
                client_sock.close()
            elif 'read' in command:
                self.read()
                client_sock.send('Read'.encode())
            elif 'write' in command:
                self.write()
                client_sock.send('Write'.encode())
            else:
                client_sock.send('Wrong command!'.encode())

        client_sock.close()

    def write(self):
        print('write')

    def read(self):
        print('read')

    def get_flight(self):
        pass

# end of Server class


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    server = Server()
    server.start()
