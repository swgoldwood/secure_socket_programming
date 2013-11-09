#!/usr/bin/env python

#Client for connecting to server and chatting using simple socket connections
# use with server/simple_chat_server.py

import socket, select, string, sys, readline

def prompt(msg = ""):
    sys.stdout.write('<You> ' + msg)
    sys.stdout.flush()

#writes data to screen and returns current stdin string
def write_to_prompt(data):
    print readline.get_line_buffer()

if __name__ == "__main__":

    if(len(sys.argv) < 3):
        print "Usage: python simple_chat_client.py hostname port"
        sys.exit()

    host = sys.argv[1]
    port = int(sys.argv[2])

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    try:
        s.connect((host, port))
    except:
        print "Unable to connect"
        sys.exit()

    print "Connect to remote host. Start sending messages"
    prompt()

    while True:
        socket_list = [sys.stdin, s]

        read_sockets, write_sockets, error_sockets = select.select(socket_list, [], [])

        current_msg = ""

        for sock in read_sockets:
            if sock == s:
                data = sock.recv(4096)
                if not data:
                    print "\nDisconnected from chat server"
                    sys.exit(1)
                else:
                    sys.stdout.write(data)
                    prompt()
                    write_to_prompt(data)
            else:
                current_msg += sys.stdin.readline()
                s.send(current_msg)
                current_msg = ""
                prompt()

