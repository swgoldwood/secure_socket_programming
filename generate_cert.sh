#/bin/sh

# generates cert public/private ssl keys, sufficient for scripts

# this is suggested generation - http://docs.python.org/2/library/ssl.html
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout cert.pem
