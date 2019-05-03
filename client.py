import argparse
import os
import re
import socket
import sys


class Client(object):
    read_command_pattern = r'^read \d+$'
    write_command_pattern = r'^write \d+ (arrival|departure) \d{2}:\d{2}$'

    def __init__(self):  # add client types (writers/readers)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 8888
        # self.type = type
        # self.server_add = ''

    def connect_to_server(self):
        """ Connects to server and prints a help prompt to the console. """

        self.socket.connect((socket.gethostname(), self.port))
        server_name = self.socket.recv(1024).decode('utf-8')

        print(f'{server_name}> {self.help()}')

        self.send_commands(server_name)

    def send_commands(self, server_name):
        while True:
            command = input(f'{server_name}> ')

            if re.match(self.read_command_pattern, command) or re.match(self.write_command_pattern, command):
                self.socket.send(command.encode())
                reply = self.socket.recv(1024).decode('utf-8')
                self.process_reply(command, reply)
            elif command == 'exit':
                self.socket.send(command.encode())
                self.socket.close()
                sys.exit()
            elif command == 'help':
                print(self.help())
            else:
                print('<WRONG COMMAND>')

    def process_reply(self, command, reply):
        if command[0] == 'r':
            if reply == 'RERR-EL':
                print('RERR: Flights list is empty.')
            elif reply == 'RERR-NF':
                print(f'RERR: The flight you requested was not found.')
            else:
                print(reply)
        elif command[0] == 'w':
            if reply == 'WOK':
                print('WOK: Flight successfully written.')
            else:
                print('WERR: Invalid flight_code.')

    def help(self):
        """ Returns a string explaining the possible commands a client
        can use in the server. """

        return'Commands syntax:\n1)read <flight_code>\n2)write <flight_code> <status> <time>\n3)help\n4)exit'

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
