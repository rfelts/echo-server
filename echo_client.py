#!/usr/bin/env python3

# Russell Felts
# Assignment 02 Echo Client


import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    server_address = ('localhost', 10000)
    buffer_size = 16

    # Instantiate a TCP socket with IPv4 Addressing
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
    print('connecting to {0} port {1}'.format(*server_address), file=log_buffer)

    # Connect your socket to the server
    sock.connect(server_address)

    # Use this variable to accumulate the entire message received back from the server
    received_message = ''

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)

        # Send your message to the server here.
        sock.sendall(msg.encode('utf-8'))

        # Accumulate the chunks you get to build the entire reply from the server.
        # Make sure that you have received the entire message and then you can break the loop.
        while True:
            chunk = sock.recv(buffer_size)

            # Print each chunk you receive for help with debugging
            print('received "{0}"'.format(chunk.decode('utf8')), file=log_buffer)

            # Append the new chunk to the received message
            received_message += chunk.decode('utf8')

            # Break out of the loop if there are no more chunks
            if len(chunk) < buffer_size:
                break
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    finally:

        # Close your client socket.
        print('closing socket', file=log_buffer)
        sock.close()

        # Return the entire reply
        return received_message


if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
