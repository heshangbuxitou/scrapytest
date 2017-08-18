# coding:utf-8
__author__ = 'yong <siyuyon@163.com>'

import socket
import threading

BUFSIZE = 1024


def handle(connected_sock):
    while True:
        data = connected_sock.recv(BUFSIZE)
        if len(data) > 0:
            print 'receive', data
            cur_thread = threading.current_thread()
            send_data = '{}:{}'.format(cur_thread.ident, data)
            connected_sock.sendall(send_data) #用sendall，不要用send，send并不一定发送所有send_data，可能发送了部分就返回了
            print 'send', send_data
        else:
            print 'close the connected socket and terminate sub thread'
            connected_sock.close()
            break


HOST = ''
PORT = 12345
ADDR = (HOST, PORT)
sub_threads = []

listen_sock = socket.socket()
listen_sock.settimeout(5.0) #设定超时时间后，socket其实内部变成了非阻塞，但有一个超时时间
listen_sock.bind(ADDR)
listen_sock.listen(2)
print 'build connect when new TCP comes'

while True:
    try:
        connected_sock, cliend_addr = listen_sock.accept()
    except socket.timeout:
        length = len(sub_threads)
        while length:
            sub = sub_threads.pop(0)
            sub_id = sub.ident #进程ID
            sub.join(0.1) #等待线程结束，0.1秒
            if sub.isAlive():
                sub_threads.append(sub)
            else:
                print 'killed sub thread ', sub_id
            length -= 1
    else:
        t = threading.Thread(
            target=handle, name='sub thread', args=(connected_sock,))
        #它继承了listen_socket的阻塞/非阻塞特性，因为listen_socket是非阻塞的，所以它也是非阻塞的
        #要让他变为阻塞，所以要调用setblocking
        connected_sock.setblocking(1)
        t.start()
        sub_threads.append(t)
