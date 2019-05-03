import argparse
import os
import pickle
import re
import socket
import sys


class Client(object):
    # pattern for read and delete commands
    rd_cmd_pattern = r'^(read|delete) \d+$'
    # pattern for write and modify commands
    wm_cmd_pattern = r'^(write|modify) \d+ (arrival|departure) \d{2}:\d{2}$'

    def __init__(self):  # add client types (writers/readers)
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 8888
        # self.server_add = ''

    def connect_to_server(self):
        """ Connects to server and prints a help prompt to the console. """

        self.socket.connect((socket.gethostname(), self.port))
        server_name = self.socket.recv(1024).decode('utf-8')

        print(f'{server_name}> {self.help()}')

        self.send_commands(server_name)

    def send_commands(self, server_name):
        """Processes and sends the commands to the server."""

        while True:
            command = input(f'{server_name}> ')

            if re.match(self.rd_cmd_pattern, command) or re.match(self.wm_cmd_pattern, command):
                self.socket.send(command.encode())
                response = self.socket.recv(1024).decode('utf-8')
                self.process_response(command, response)

            # elif re.match(self.wm_cmd_pattern, command):
            #     self.socket.send(command.encode())
            #     response = self.socket.recv(1024).decode('utf-8')
            #     self.process_response(command, response)

            elif command == 'timetable':
                self.socket.send(command.encode())
                response = self.socket.recv(1024)
                self.process_response(command, response)

            elif command == 'help':
                print(self.help())

            elif command == 'exit':
                self.socket.send(command.encode())
                self.socket.close()
                sys.exit()

            else:
                print('<WRONG COMMAND>')

    def process_response(self, command, response):
        """Processes the response sent from the server."""

        args = command.split()
        if args[0] == 'read':
            if response == 'RERR-EL':
                print('RERR: Timetable is empty.')
            elif response == 'RERR-NF':
                print(f'RERR: Flight {args[1]} was not found.')
            else:
                print(response)

        elif args[0] == 'write':
            if response == 'WOK':
                print(f'WOK: Flight {args[1]} successfully written.')
            else:
                print(f'WERR: Invalid flight_code: {args[1]}.')

        elif args[0] == 'modify':
            if response == 'MOK':
                print(f'MOK: Flight {args[1]} successfully modified.')
            else:
                print(f'MERR: Invalid flight {args[1]}.')

        elif args[0] == 'delete':
            if response == 'DOK':
                print(f'DOK: Flight {args[1]} deleted.')
            else:
                print(f'DERR: Flight {args[1]} was not found.')

        elif args[0] == 'timetable':
            timetable = pickle.loads(response)
            for flight in timetable:
                print(flight)

    def help(self):
        """ Returns a string explaining the possible commands a client
        can use in the server. """

        return """\nCommands:
        1) read <flight_code>
        2) write <flight_code> <status> <time>
        3) modify <flight_code> <status> <time>
        4) delete <flight_code>
        5) timetable
        6) help
        7) exit"""

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
