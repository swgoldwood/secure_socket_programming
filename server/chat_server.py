#!/usr/bin/python

import optparse
import socket
import sys
import time

from thread import *

p = optparse.OptionParser()
p.add_option('--port', '-p')

options, arguments = p.parse_args()

host = ''   # Symbolic name meaning all available interfaces
port = int(options.port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((host, port))
except:
    print 'Bind failed, Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

s.listen(10)

clients = {}

def get_name_from_client(conn, addr):

    while True:
        conn.sendall("Give me your name\n")

        data = conn.recv(1024)

        print "Got user_name " + data + " from client"

        if not data:
            next

        user_name = data.rstrip()

        clients[user_name]['port'] = addr[1]
        clients[user_name]['ip'] = addr[1]

        conn.sendall("Thanks %s" % user_name)
        break


while True:
    conn, addr = s.accept()

    start_new_thread(get_name_from_client, (conn, addr))

    conn.close()

s.close()

