#!/usr/bin/env python

import socket, argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', required=True)
    parser.add_argument('--port', required=True)
    parser.add_argument('--host', required=True)
    args = parser.parse_args()

    FILE = args.filename
    HOST = args.host
    PORT = int(args.port)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)

    print "Connecting to server %s:%i" % (HOST, PORT)

    sock.connect((HOST, PORT))

    f = open(FILE, 'wb')

    print "Writing to file %s" % FILE

    l = sock.recv(1024)

    while (l):
        f.write(l)
        l = sock.recv(1024)

    f.close()
    sock.close()

