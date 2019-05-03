import socket
import os
import sys
import re
from threading import Thread, Lock
from time import sleep
from flight import Flight


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
            # client_sock.send(self.help().encode())

            client_process = Thread(
                target=self.handle_connection, args=(client_sock, client_address))
            client_process.start()

        socket.close()

    # def disconnect(function):
    #     """Decorator function to handle the disconnection of a client."""
    #
    #     def inner(*args):
    #         try:
    #             function(*args)
    #         except BrokenPipeError:
    #             _, _, client_address = args
    #             print(f'Client: {client_address} disconnected.')
    #     return inner
    #

    def handle_connection(self, client_sock, client_address):
        """ Handles a client connection based on the command the client typed.

        params: client_sock, client_address
        """

        while True:
            command = client_sock.recv(1024).decode('utf-8')

            if command[0] == 'r':
                _, flight_code = command.split()
                client_sock.send(self.read_from_flights(flight_code).encode())
            elif command[0] == 'w':
                _, flight_code, status, time = command.split()
                client_sock.send(self.write_to_flights(
                    flight_code, status, time).encode())
            elif command == 'exit':
                print(f'Client: {client_address} disconnected.')
                break

        client_sock.close()

    def find_flight(self, flight_code):
        """ Finds the flight with the same flight_code passed in the parameters.
        If there is no flight with such flight_code return None.

        params: flight_code
        return: flight | None
        """

        for flight in self.flights:
            if flight.code == flight_code:
                return flight

        return None

    def write_to_flights(self, flight_code, status, time):
        """ Creates an Flight object and appends it to the flights list.

        params: flight_code, status, time
        return: 'WERR' | 'WOK'
        """

        with self.lock:
            flight = self.find_flight(flight_code)

            if flight is not None:
                return 'WERR'
            else:
                print('Writing to flights list...')
                sleep(5)
                new_flight = Flight(flight_code, status, time)
                self.flights.append(new_flight)
                return 'WOK'

    def read_from_flights(self, flight_code):
        """ Search for the flight with the given flight_code in the flights list.

        params: flight_code
        return: 'RERR-EL' | 'RERR-NF' | flight
        """

        with self.lock:
            if len(self.flights) == 0:
                return 'RERR-EL'
            else:
                print('Reading from flights list...')
                sleep(2)
                flight = self.find_flight(flight_code)

                return f'ROK: {repr(flight)}' if flight is not None else 'RERR-NF'

# end of Server class


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    server = Server()
    server.start()
