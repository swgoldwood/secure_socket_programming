#!/usr/bin/python

# Send file over ssl socket
 
import socket, argparse

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument('--filename', required=True)
    p.add_argument('--port', required=True)
    args = p.parse_args()

    FILE = args.filename
    PORT = int(args.port)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)

    print "Started file server on port %i using file %s" % (PORT, FILE)

    while (True):
        client_conn, address = server_socket.accept()

        print "New client %s:%i" % address

        f = open(FILE, 'rb')
        l = f.read(1024)
        while (l):
            client_conn.sendall(l)
            l = f.read(1024)

        f.close()
        client_conn.close()

    server_socket.close()
