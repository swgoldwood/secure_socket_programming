#/bin/sh

#openssl req -new -x509 -extensions v3_ca -keyout dummykey.pem -out dummycert.pem -days 3650!

# this is suggested generation - http://docs.python.org/2/library/ssl.html
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.pem
