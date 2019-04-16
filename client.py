import socket
import os
import sys
import argparse


class Client(object):
    def __init__(self):  # add client types (writers/readers)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 8888
        # self.type = type
        # self.server_add = ''

    def connect_to_server(self):
        self.socket.connect((socket.gethostname(), self.port))
        server_name = self.socket.recv(1024).decode('utf-8')

        # self.write() if self.type == 'writer' else self.read()
        self.send_commands(server_name)

    def send_commands(self, server_name):
        while True:
            command = input(f'{server_name}> ')

            if command == 'exit':
                self.socket.close()
                sys.exit()

            self.socket.send(command.encode())
            reply = self.socket.recv(1024).decode('utf-8')
            print(reply)

# end of Client class


# def get_arguments():
#     parser = argparse.ArgumentParser(description='Client program.')
#     parser.add_argument('-ct', '--client_type', type=str,
#                         help='Client type. (writer or reader)')
#
#     args = parser.parse_args()
#
#     return args.client_type


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    # client_type = get_arguments()
    # client = Client(client_type)
    client = Client()
    client.connect_to_server()
