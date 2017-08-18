# coding:utf-8
__author__ = 'yong <siyuyon@163.com>'

import sys
import socket
HOST = 'localhost'
PORT = 12345
ADDR = (HOST, PORT)
BUFSIZE = 1024

sock = socket.socket()

try:
    a = sock.connect(ADDR)
except Exception, e:
    print 'error', e
    sock.close()
    sys.exit()

print 'hava connected with server'

while True:
    data = raw_input('> ')
    if len(data) > 0:
        print 'send', data
        sock.sendall(data) #不要使用sand()
        recv_data = sock.recv(BUFSIZE)
        print 'receive::',recv_data
    else:
        sock.close()
        break