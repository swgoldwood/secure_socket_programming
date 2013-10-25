#!/usr/bin/env python

import socket, ssl, pprint, sys

if(len(sys.argv) < 2):
    print "Usage: python secure_client.py cert_file [host [port]]"
    sys.exit(1)

#need at least ssl ca_cert file location
cert_file = sys.argv[1]

#default values for host and port
host = 'www.verisign.com'
port = 443

if len(sys.argv) >= 3:
    host = sys.argv[2]

if len(sys.argv) >= 4:
    port = int(sys.argv[3])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# require a certificate from the server
ssl_sock = ssl.wrap_socket(s, ca_certs=cert_file, cert_reqs=ssl.CERT_REQUIRED, ssl_version=ssl.PROTOCOL_SSLv3)

print "Attempting ssl_sock.connect(('%s', %i))" % (host, port)

ssl_sock.connect((host, port))

print "ssl_sock.getpeername() " + repr(ssl_sock.getpeername())
print "ssl_sock.cipher() " + str(ssl_sock.cipher())
print "ssl_sock.getpeercert() " + pprint.pformat(ssl_sock.getpeercert())

# Set a simple HTTP request -- use httplib in actual code.
ssl_sock.write("""GET / HTTP/1.0\r
Host: %s\r\n\r\n""" % host)

# Read a chunk of data.  Will not necessarily
# read all the data returned by the server.
data = ssl_sock.read()

print "Recieved data %s" % data

# note that closing the SSLSocket will also close the underlying socket
ssl_sock.close()
