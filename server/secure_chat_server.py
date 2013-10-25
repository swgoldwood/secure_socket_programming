#!/usr/bin/python

# Secure Tcp Chat server
 
import socket, select, argparse, ssl
 
#Function to broadcast chat messages to all connected clients
def broadcast_data (sock, message):
    #Do not send the message to master socket and the client who has send us the message
    for socket in CONNECTION_LIST:
        if socket != server_socket and socket != sock:
            try :
                socket.send(message)
            except :
                # broken socket connection may be, chat client pressed ctrl+c for example
                socket.close()
                CONNECTION_LIST.remove(socket)
 
if __name__ == "__main__":
    # Parse arguments - need credential file and port
    p = argparse.ArgumentParser()
    p.add_argument('--port', required=True)
    p.add_argument('--cert', required=True)
    args = p.parse_args()
     
    # List to keep track of socket descriptors
    CONNECTION_LIST = []
    PORT = int(args.port)
    CERT_FILE = args.cert
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
     
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)
 
    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)
 
    print "Chat server started on port " + str(PORT)
 
    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
 
        for sock in read_sockets:
            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()

                #create server side ssl context to socket and append CONNECTION_LIST
                connstream = ssl.wrap_socket(
                    sockfd,
                    server_side=True,
                    certfile=CERT_FILE,
                    keyfile=CERT_FILE,
                    ssl_version=ssl.PROTOCOL_SSLv3
                )

                CONNECTION_LIST.append(connstream)
                print "Client (%s, %s) connected" % addr
                 
                broadcast_data(connstream, "[%s:%s] entered room\n" % addr)
             
            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                try:
                    #In Windows, sometimes when a TCP program closes abruptly,
                    # a "Connection reset by peer" exception will be thrown
                    data = sock.recv(RECV_BUFFER)
                    if data:
                        broadcast_data(sock, "\r" + '<' + str(sock.getpeername()) + '> ' + data)                
                 
                except:
                    broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                    print "Client (%s, %s) is offline" % addr
                    sock.close()
                    CONNECTION_LIST.remove(sock)
                    continue
     
    server_socket.close()
