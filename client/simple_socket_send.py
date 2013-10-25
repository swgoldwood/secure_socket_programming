#!/usr/bin/python

import optparse
import socket
import sys

p = optparse.OptionParser()
p.add_option('--port', '-p')
p.add_option('--host', '-H')

options, arguments = p.parse_args()
host, port = options.host, int(options.port)

#create an INET, STREAMing socket
try:
    #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error, msg:
    print 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();

try:
    remote_ip = socket.gethostbyname( host )
except socket.gaierror:
    #could not resolve
    print 'Hostname could not be resolved. Exiting'
    sys.exit()

print 'Attempting socket connection to %s:%i' % (remote_ip, port)

#now connect to the web server on port 80
# - the normal http port
try:
    s.connect((remote_ip, port))
except socket.error, msg:
    print 'Failed to connect with socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();

print "Successful connection"

#Send some data to remote server
message = "GET / HTTP/1.1\r\n\r\n"

try:
    s.sendall(message)
except socket.error:
    #Send failed
    print 'Send failed'
    sys.exit()

print "Message sent"

reply = s.recv(4096)

print reply

s.close()
