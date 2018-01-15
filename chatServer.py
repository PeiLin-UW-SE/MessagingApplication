#!/usr/bin/python3

import socket
import sys
import signal


class Server:

    clients = []
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def sigint_handler(self, signum, frame):
        self.s.close()  # closes the socket
        sys.exit(0)  # exit without error

    def __init__(self, host="127.0.0.1", port=5000):
        online = True
        self.s.bind((host, port))
        signal.signal(signal.SIGINT, self.sigint_handler)
        print("----- SERVER IS ON-----")

        while online:
            encoded_data, client = self.s.recvfrom(1024)
            decoded_data = encoded_data.decode("utf-8")

            if client not in self.clients:
                self.clients.append(client)

            if "SHUTDOWN" in decoded_data:
                print("----- SERVER IS OFF -----")
                online = False
            else:
                print("Received From: " + str(client) + "\n    " + str(decoded_data))
                for client in self.clients:
                    self.s.sendto(encoded_data, client)
        self.s.close()
        sys.exit(0)


if __name__ == '__main__':
    Server()
