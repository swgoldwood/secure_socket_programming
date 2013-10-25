#!/usr/bin/env python

import socket, select

#Function to broadcast chat messages to all connected clients
def broadcast_data(sock, message):
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock:
            try:
                socket.send(message)
            except:
                print "Client is now offline: %s" % str(sock.getpeername())

                socket.close()
                CONNECTION_LIST.remove(socket)

if __name__ == "__main__":
    
    #List to keep track of socket descriptors
    CONNECTION_LIST = []
    RECV_BUFFER = 4096
    PORT = 5000

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(10)

    CONNECTION_LIST.append(server_socket)

    print "Chat server started on port " + str(PORT)

    while True:
        read_sockets, write_sockets, error_sockets = select.select(CONNECTION_LIST, [], [])

        for sock in read_sockets:
            if sock == server_socket:
                sockfd, addr = server_socket.accept()
                print "New Connection: %s:%s" % addr
                CONNECTION_LIST.append(sockfd)
                broadcast_data(sockfd, "[%s:%s] entered room\n" % addr)
            else:
                try:
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)
                except:
                    broadcast_data(sock, "Client (%s:%s) is now offline" % addr)
                    print "Client is now offline: %s:%s" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue

    server_socket.close()

