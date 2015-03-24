#!/usr/bin/env python
 
import socket
 
 
TCP_IP = '127.0.0.1'
TCP_PORT = 1234
BUFFER_SIZE = 1024*32


f = open('workfile.rtliq', 'w')
 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
var=1
length=0
while var==1:
	data = s.recv(BUFFER_SIZE)
	length+=len(data)
	f.write(data);
	print length,"(",len(data),")"
print "bye"
s.close()
