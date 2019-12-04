#!/usr/bin/env python3

# Russell Felts
# Assignment 02 Echo Server

import socket
import sys
import traceback


def server(log_buffer=sys.stderr):
    # set an address for our server
    address = ('127.0.0.1', 10000)
    buffer_size = 16

    # Instantiate a TCP socket with IPv4 Addressing, call the socket you make 'sock'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    # Set an option deals with the port is already used error.
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # log that we are building a server
    print("making a server on {0}:{1}".format(*address), file=log_buffer)

    # Bind your new sock 'sock' to the address above and begin to listen for incoming connections
    sock.bind(address)
    sock.listen()

    try:
        # The outer loop controls the creation of new connection sockets. The server will handle
        # each incoming connection one at a time.
        while True:
            print('waiting for a connection', file=log_buffer)

            # Make a new socket when a client connects and get the address of the client and report it below.
            conn, addr = sock.accept()

            try:
                print('connection - {0}:{1}'.format(*addr), file=log_buffer)

                # Receive messages sent by the client in buffers. When a complete message has been received,
                # the loop will exit
                while True:

                    # Receive 16 bytes of data from the client. Store the data you receive as 'data'
                    data = conn.recv(buffer_size)
                    print('received "{0}"'.format(data.decode('utf8')))

                    # Send the data you received back to the client, log
                    # the fact using the print statement here.  It will help in
                    # debugging problems.
                    conn.sendall(data)
                    print('sent "{0}"'.format(data.decode('utf8')))

                    # Check here to see whether you have received the end of the message. If you have,
                    # then break from the `while True` loop.
                    if len(data) < buffer_size:
                        break

            except Exception as e:
                traceback.print_exc()
                sys.exit(1)
            finally:
                # When the inner loop exits, this 'finally' clause will be hit. Use that opportunity to close the
                # socket you created above when a client connected
                conn.close()
                print('echo complete, client connection closed', file=log_buffer)

    except KeyboardInterrupt:
        # Use the python KeyboardInterrupt exception as a signal to close the server socket and
        # exit from the server function
        sock.close()
        print('quitting echo server', file=log_buffer)
        sys.exit(1)


if __name__ == '__main__':
    server()
    sys.exit(0)
