#!/usr/bin/env python

import socket, ssl, sys, argparse

def do_something(connstream, data):
    print "Data: " + data
    print "Sending crap back"
    connstream.write('hello')
    return False

def deal_with_client(connstream):
    data = connstream.read()
    # null data means the client is finished with us
    while data:
        if not do_something(connstream, data):
            # we'll assume do_something returns False
            # when we're finished with client
            break

if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--port')
    parser.add_argument('--certfile')
    parser.add_argument('--keyfile')
    args = parser.parse_args()

    bindsocket = socket.socket()
    bindsocket.bind(('0.0.0.0', int(args.port)))
    bindsocket.listen(5)

    while True:
        newsocket, fromaddr = bindsocket.accept()

        print "Connected with %s:%i" % fromaddr

        connstream = ssl.wrap_socket(
            newsocket,
            server_side=True,
            certfile=args.certfile,
            keyfile=args.keyfile,
            ssl_version=ssl.PROTOCOL_SSLv3
        )

        try:
            deal_with_client(connstream)
        finally:
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()
