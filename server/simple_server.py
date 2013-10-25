#!/usr/bin/python

import optparse
import socket
import sys
import time

from thread import *

#Function for handling connections. This will be used to create threads
def clientthread(conn, addr):
    #Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter\n') #send only takes string
    
    #infinite loop so that function do not terminate and thread do not end.
    while True:

        #Receiving from client
        data = conn.recv(1024)
        reply = 'OK...' + data
        if not data: 
            break

        conn.sendall(reply)
        time.sleep(2)
        conn.sendall("done %s:%s\n" % addr)

    #came out of loop
    conn.close()

if __name__ == "__main__":
    
    p = optparse.OptionParser()
    p.add_option('--port', '-p')
    
    options, arguments = p.parse_args()

    if not options.port:
        print "--port, -p not specified"
        sys.exit(1)
    
    host = ''   # Symbolic name meaning all available interfaces
    port = int(options.port)
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    print 'Socket created'
    
    try:
        s.bind((host, port))
    except socket.error , msg:
        print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
    
    print 'Socket bind complete'
    
    s.listen(10)
    
    print "Socket is listening"
    
    while True:
        conn, addr = s.accept()
         
        #display client information
        print 'Connected with ' + addr[0] + ':' + str(addr[1])
        
        #now keep talking with the client
        start_new_thread(clientthread, (conn, addr))
     
    s.close()
