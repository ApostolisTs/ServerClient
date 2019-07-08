# Multithreaded Server / Client.

A multithreaded Server that handles a flight timetable and a client
that performs some operations on that flight timetable. The Server starts with
a default timetable.
Written in Python 3.7.

### Running the Server.

To run the server simply type the following command in your terminal (it doesn't take any
command line argumets):
```
python server.py
```

### Running the Client.

The Client can be executed in two different ways, as an automatic reader/writer
and as interactive shell connected to the Server that the user can use to type commands
and perform operations on the Server's timetable.

###### Automatic reader/writer.

When the user runs the Client as an automatic reader/writer it creates and connects to the
Server two Client instances. Those instances perform random read and write operations
and output the server response.

To run it simply type the following command in your terminal:
```
python client.py -u True
```

###### Interactive Shell.

When the user runs the Client without specifying the `-u` argument it runs as an Interactive
shell connected to the Server. From that point the user can type commands and perform
read/write operations on the Server's flight timetable.

To run it simply type the following command in your terminal:
```
python client.py
```
Once the Client is running and it's connected to the Server type the `help` command to
the availiable operations on the Server.
