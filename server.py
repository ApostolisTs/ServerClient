import socket
import os
import sys
import re
from multiprocessing import Process, Lock
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
            client_sock.send(self.help().encode())

            client_process = Process(
                target=self.handle_connection, args=(client_sock, client_address))
            client_process.start()

        socket.close()

    def handle_connection(self, client_sock, client_address):
        """ Handles a client connection based on the command the client typed.

        params: client_sock, client_address
        """

        try:
            while True:
                command = client_sock.recv(1024).decode('utf-8')

                if re.match(r'^read \d+$', command):
                    _, flight_code = command.split()
                    flight = self.read_from_flights(flight_code)

                    if flight == 'EL':
                        client_sock.send('Flights list is empty.'.encode())
                    elif flight == 'NF':
                        client_sock.send(
                            'Flight with code: {flight_code} was not found.'.encode())
                    else:
                        client_sock.send(repr(flight).encode())

                elif re.match(r'^write \d+ (arrival|departure) \d{2}:\d{2}$', command):
                    _, flight_code, status, time = command.split()
                    written = self.write_to_flights(flight_code, status, time)

                    if written == 'OK':
                        client_sock.send(
                            'Flight successfully written.'.encode())
                    else:
                        client_sock.send('Invalid flight_code.'.encode())

                elif command == 'help':
                    client_sock.send(self.help().encode())
                elif command == 'exit':
                    client_sock.close()
                else:
                    client_sock.send('<WRONG COMMAND>'.encode())

            client_sock.close()
        except ConnectionAbortedError:
            print(f'Client: {client_address} disconnected.')

    def help(self):
        """ Returns a string explaining the possible commands a client
        can use in the server. """

        return'Commands syntax:\n1)read <flight_code>\n2)write <flight_code> <status> <time>\n3)help\n4)exit'

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
        return: 'IC' | 'OK'
        """

        with self.lock:
            flight = self.find_flight(flight_code)

            if flight != None:
                return 'IC'
            else:
                print('Writing to flights list...')
                sleep(5)
                new_flight = Flight(flight_code, status, time)
                self.flights.append(new_flight)
                return 'OK'

    def read_from_flights(self, flight_code):
        """ Search for the flight with the given flight_code in the flights list.

        params: flight_code
        return: 'EL' | 'NF' | flight
        """

        with self.lock:
            if len(self.flights) == 0:
                return 'EL'
            else:
                print('Reading from flights list...')
                sleep(2)
                flight = self.find_flight(flight_code)

                return flight if flight != None else 'NF'

# end of Server class


if __name__ == '__main__':
    os.system('cls' if os.name == 'nt' else 'clear')
    server = Server()
    server.start()
