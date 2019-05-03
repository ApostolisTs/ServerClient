import argparse
import os
import pickle
import re
import socket
import sys


class Client(object):
    read_cmd_pattern = r'^read \d+$'
    wm_cmd_pattern = r'^(write|modify) \d+ (arrival|departure) \d{2}:\d{2}$'
    # modify_command_pattern = r'^modify \d+ (arrival|departure) \d{2}:\d{2}$'

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

            # or re.match(self.write_command_pattern, command):
            if re.match(self.read_cmd_pattern, command):
                self.socket.send(command.encode())
                response = self.socket.recv(1024).decode('utf-8')
                self.process_response(command, response)

            elif re.match(self.wm_cmd_pattern, command):
                self.socket.send(command.encode())
                response = self.socket.recv(1024).decode('utf-8')
                self.process_response(command, response)

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

        if command[0] == 'r':
            if response == 'RERR-EL':
                print('RERR: Timetable is empty.')
            elif response == 'RERR-NF':
                print(f'RERR: The flight you requested was not found.')
            else:
                print(response)

        elif command[0] == 'w':
            if response == 'WOK':
                print('WOK: Flight successfully written.')
            else:
                print('WERR: Invalid flight_code.')

        elif command[0] == 'm':
            if response == 'MOK':
                print('MOK: Flight successfully modified.')
            else:
                print('MERR: Invalid flight.')

        elif command[0] == 't':
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
