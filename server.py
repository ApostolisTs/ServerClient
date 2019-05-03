from flight import Flight
import os
import pickle
import re
import socket
import sys
from threading import Thread, Lock
from time import sleep


class Server(object):
    """ Implements a Server class which is handling a timetable (list of flights).
    Clients can execute reads/writes on that list concurrently. """

    def __init__(self):
        self.port = 8888
        self.lock = Lock()
        self.timetable = []
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

            client_process = Thread(
                target=self.handle_connection, args=(client_sock, client_address))
            client_process.start()

        socket.close()

    def handle_connection(self, client_sock, client_address):
        """ Handles a client connection based on the command the client typed."""

        while True:
            command = client_sock.recv(1024).decode('utf-8')

            if command[0] == 'r':
                _, flight_code = command.split()
                response = self.read_flight(flight_code)
                client_sock.send(response.encode())

            elif command[0] == 'w':
                _, flight_code, status, time = command.split()
                response = self.write_flight(flight_code, status, time)
                client_sock.send(response.encode())

            elif command[0] == 'm':
                _, flight_code, status, time = command.split()
                response = self.modify_flight(flight_code, status, time)
                client_sock.send(response.encode())

            elif command[0] == 't':
                client_sock.send(pickle.dumps(self.timetable))

            elif command == 'exit':
                print(f'Client: {client_address} disconnected.')
                break

        client_sock.close()

    def get_flight_index(self, flight_code):
        """ Finds the flight with the same flight_code passed in the parameters.
        If there is no flight with such flight_code return None.

        return: flight | None
        """

        for i, flight in enumerate(self.timetable):
            if flight.code == flight_code:
                return i

        return None

    def write_flight(self, flight_code, status, time):
        """ Creates an Flight object and appends it to the timetable.

        return: 'WERR' | 'WOK'
        """
        with self.lock:
            index = self.get_flight_index(flight_code)

            if index is not None:
                return 'WERR'
            else:
                print('Writing to timetable...')
                sleep(3)
                new_flight = Flight(flight_code, status, time)
                self.timetable.append(new_flight)
                return 'WOK'

    def read_flight(self, flight_code):
        """ Search for the flight with the given flight_code in the timetable.

        return: 'RERR-EL' | 'RERR-NF' | 'ROK: repr(flight)'
        """
        with self.lock:
            if len(self.timetable) == 0:
                return 'RERR-EL'
            else:
                print('Reading from timetable...')
                sleep(1)
                index = self.get_flight_index(flight_code)

                return f'ROK: {repr(self.timetable[index])}' if index is not None else 'RERR-NF'

    def modify_flight(self, flight_code, status, time):
        with self.lock:
            index = self.get_flight_index(flight_code)

            if index is None:
                return 'MERR'
            else:
                print(f'Modifing flight:{flight_code} ...')
                sleep(2)
                flight = self.timetable.pop(index)
                if flight.status is not status:
                    flight.status = status

                if flight.time is not time:
                    flight.time = time

                self.timetable.append(flight)
                return 'MOK'

# end of Server class


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    server = Server()
    server.start()
