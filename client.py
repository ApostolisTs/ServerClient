import argparse
import os
import pickle
import random
import re
import socket
import sys
import time
from threading import Thread

NUM_0F_REQS = 10


class Client(object):
    """Implements a Clients that reads and writes in a server's timetable
    (list of flights)."""

    # pattern for read and delete commands
    rd_cmd_pattern = r'^(read|delete) \d+$'
    # pattern for write and modify commands
    wm_cmd_pattern = r'^(write|modify) \d+ (arrival|departure) \d{2}:\d{2}$'

    def __init__(self, user, id):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 8888
        self.user = user
        self.id = id
        # self.server_add = ''

    def connect_to_server(self):
        """ Connects to server as a user or an automatic writer/reader."""

        self.socket.connect((socket.gethostname(), self.port))
        server_name = self.socket.recv(1024).decode('utf-8')

        if self.user:
            self.__send_commands(server_name)
        else:
            self.__connect_as_automatic_reader_writer()

    def __connect_as_automatic_reader_writer(self):
        """Execute automatic write requests to the server."""

        reqs = 0
        while reqs < NUM_0F_REQS:
            random_choice = random.randint(0, 2)

            if random_choice == 0:
                print(f'<<Client-{self.id}>> waiting to read.')
                self.__send_random_read_req()
            else:
                print(f'<<Client-{self.id}>> waiting to write.')
                self.__send_random_write_req()

            reqs += 1

        self.socket.send('exit'.encode())
        self.socket.close()

    def __send_random_write_req(self):
        """Send a random read request to the server."""

        flight_code = random.randint(1, 20)
        status = 'arrival' if random.randint(0, 1) == 0 else 'departure'
        hour = random.randint(1, 24)
        minute = random.randint(1, 60)
        flight_time = f'{str(hour).zfill(2)}:{str(minute).zfill(2)}'
        command = f'write {flight_code} {status} {flight_time}'

        self.socket.send(command.encode())
        response = self.socket.recv(1024).decode('utf-8')
        response = self.__process_response(command, response)
        print(f'<<Client-{self.id}>> {response}')

    def __send_random_read_req(self):
        """Send a random write request to the server."""

        flight_code = random.randint(1, 20)
        command = f'read {flight_code}'

        self.socket.send(command.encode())
        response = self.socket.recv(1024).decode('utf-8')
        response = self.__process_response(command, response)
        print(f'<<Client-{self.id}>> {response}')

    def __send_commands(self, server_name):
        """Processes and sends the commands to the server."""

        print(f'{server_name}> {self.__help()}')
        while True:
            command = input(f'{server_name}> ')

            if re.match(self.rd_cmd_pattern, command) or re.match(self.wm_cmd_pattern, command):
                self.socket.send(command.encode())
                response = self.socket.recv(1024).decode('utf-8')
                print(self.__process_response(command, response))

            elif command == 'timetable':
                self.socket.send(command.encode())
                response = self.socket.recv(1024)
                self.__process_response(command, response)

            elif command == 'help':
                print(self.__help())

            elif command == 'exit':
                self.socket.send(command.encode())
                self.socket.close()
                sys.exit()

            else:
                print('<WRONG COMMAND>')

    def __process_response(self, command, response):
        """Processes the response sent from the server and return what
        will the user see."""

        args = command.split()
        if args[0] == 'read':
            if response == 'RERR-EL':
                return f'RERR: Timetable is empty.'
            elif response == 'RERR-NF':
                return f'RERR: Flight {args[1]} was not found.'
            else:
                return response

        elif args[0] == 'write':
            if response == 'WOK':
                return f'WOK: Flight {args[1]} successfully written.'
            else:
                return f'WERR: Invalid flight_code: {args[1]}.'

        elif args[0] == 'modify':
            if response == 'MOK':
                return f'MOK: Flight {args[1]} successfully modified.'
            else:
                return f'MERR: Invalid flight {args[1]}.'

        elif args[0] == 'delete':
            if response == 'DOK':
                return f'DOK: Flight {args[1]} deleted.'
            else:
                return f'DERR: Flight {args[1]} was not found.'

        elif args[0] == 'timetable':
            timetable = pickle.loads(response)
            for flight in timetable:
                print(flight)

    def __help(self):
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


def get_arguments():
    parser = argparse.ArgumentParser(description='Client program.')
    parser.add_argument('-u', '--user', type=bool, default=False,
                        help='If the argument is true runs a terminal for the user ' +
                        'to interact with the server and send commands. If its false ' +
                        'it runs a simulations of reads and writes in the server automatically.' +
                        'Default=False')

    args = parser.parse_args()

    return args.user


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    user = get_arguments()
    if user:
        client = Client(user, 1)
        client.connect_to_server()
    else:
        c1 = Client(user, 1)
        c2 = Client(user, 2)
        c1_thread = Thread(target=c1.connect_to_server).start()
        c2_thread = Thread(target=c2.connect_to_server).start()
