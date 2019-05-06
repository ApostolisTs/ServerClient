from flight import Flight
import os
import pickle
import re
import socket
import sys
from threading import Thread, Lock
from time import sleep

# Default timetable
TIMETABLE = [
    Flight(1, 'arrival', '10:00'),
    Flight(2, 'departure', '10:30'),
    Flight(3, 'arrival', '11:00'),
    Flight(4, 'departure', '18:45'),
    Flight(5, 'arrival', '20:20'),
    Flight(6, 'departure', '8:30'),
    Flight(7, 'arrival', '23:40'),
]

WRITE_DELAY = 6
READ_DELAY = 3
DELETE_DELAY = 4
MODIFY_DELAY = 5


class Server(object):
    """ Implements a Server class which is handling a timetable (list of flights).
    Clients can execute reads/writes on that list concurrently. """

    def __init__(self):
        self.port = 8888
        self.lock = Lock()
        self.timetable = TIMETABLE

    def start(self):
        """ Gets the server running. """

        server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_sock.bind((socket.gethostname(), self.port))
        server_sock.listen()
        print('Server running...')

        self.__accept_connections(server_sock)

    def __accept_connections(self, server_sock):
        """ Accepts connections from clients and creates a new process for each
        client. """

        while True:
            client_sock, client_address = server_sock.accept()
            print(f'Connection with {client_address} has been established.')
            client_sock.send(socket.gethostname().encode())

            client_process = Thread(
                target=self.__handle_connection, args=(client_sock, client_address))
            client_process.start()

        socket.close()

    def __handle_connection(self, client_sock, client_address):
        """ Handles a client connection based on the command the client typed."""

        while True:
            command = client_sock.recv(1024).decode('utf-8')

            if command[0] == 'r':
                _, flight_code = command.split()
                response = self.__read_flight(int(flight_code))
                client_sock.send(response.encode())

            elif command[0] == 'w':
                _, flight_code, status, time = command.split()
                response = self.__write_flight(int(flight_code), status, time)
                client_sock.send(response.encode())

            elif command[0] == 'm':
                _, flight_code, status, time = command.split()
                response = self.__modify_flight(int(flight_code), status, time)
                client_sock.send(response.encode())

            elif command[0] == 'd':
                _, flight_code = command.split()
                response = self.__delete_flight(int(flight_code))
                client_sock.send(response.encode())

            elif command[0] == 't':
                client_sock.send(pickle.dumps(self.timetable))

            elif command == 'exit':
                print(f'Client: {client_address} disconnected.')
                break

        client_sock.close()

    def __get_flight_index(self, flight_code):
        """ Finds the flight with the same flight_code passed in the parameters.
        If there is no flight with such flight_code return None.

        return: flight | None
        """
        for i, flight in enumerate(self.timetable):
            if flight.code == flight_code:
                return i
        return None

    def __write_flight(self, flight_code, status, time,):
        """ Creates an Flight object and appends it to the timetable.

        return: 'WERR' | 'WOK'
        """
        with self.lock:
            index = self.__get_flight_index(flight_code)

            if index is not None:
                return 'WERR'
            else:
                print('Writing to timetable...')
                sleep(WRITE_DELAY)
                new_flight = Flight(flight_code, status, time)
                self.timetable.append(new_flight)
                return 'WOK'

    def __read_flight(self, flight_code,):
        """ Search for the flight with the given flight_code in the timetable.

        return: 'RERR-EL' | 'RERR-NF' | 'ROK: repr(flight)'
        """
        with self.lock:
            index = self.__get_flight_index(flight_code)

            if len(self.timetable) == 0:
                return 'RERR-EL'
            elif index is None:
                return 'RERR-NF'
            else:
                print('Reading from timetable...')
                sleep(READ_DELAY)

                return f'ROK: {repr(self.timetable[index])}'

    def __modify_flight(self, flight_code, status, time):
        """Modify a flight from the timetable based on the given flight_code.

        return: 'MERR' | 'MOK'
        """
        with self.lock:
            index = self.__get_flight_index(flight_code)

            if index is None:
                return 'MERR'
            else:
                print(f'Modifing flight:{flight_code} ...')
                sleep(MODIFY_DELAY)
                flight = self.timetable.pop(index)
                if flight.status is not status:
                    flight.status = status

                if flight.time is not time:
                    flight.time = time

                self.timetable.append(flight)
                return 'MOK'

    def __delete_flight(self, flight_code):
        """Delete a flight from the timetable based on the given flight_code.

        return: 'DERR' | 'DOK'
        """
        with self.lock:
            index = self.__get_flight_index(flight_code)

            if index is None:
                return 'DERR'
            else:
                print(f'Deleting flight: {flight_code}')
                sleep(DELETE_DELAY)
                flight = self.timetable.pop(index)
                return 'DOK'

# end of Server class


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    server = Server()
    server.start()
