#!/usr/bin/env python

import socket, select, string, sys, readline, argparse, ssl

def prompt(msg = ""):
    sys.stdout.write('<You> ' + msg)
    sys.stdout.flush()

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--host', required=True)
    parser.add_argument('--port', required=True)
    parser.add_argument('--cert', required=True)
    args = parser.parse_args()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)

    ssl_sock = ssl.wrap_socket(sock, ca_certs=args.cert, cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_SSLv3)

    print "Attempting to connect to %s:%s" % (args.host, args.port)

    try:
        ssl_sock.connect((args.host, int(args.port)))
    except:
        print "Unable to connect"
        sys.exit()

    print "Connect to remote host. Start sending messages"
    prompt()

    while True:
        socket_list = [sys.stdin, ssl_sock]

        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        current_msg = ""

        for sock in read_sockets:
            if sock == ssl_sock:
                data = sock.recv(4096)
                if not data:
                    print "\nDisconnected from chat server"
                    sys.exit(1)
                else:
                    sys.stdout.write(data)
                    prompt()
            else:
                current_msg += sys.stdin.readline()
                ssl_sock.send(current_msg)
                current_msg = ""
                prompt()

