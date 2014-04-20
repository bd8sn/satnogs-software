# -*- coding: utf-8 -*-
import socket


class trackersocket:

    TCP_IP = '127.0.0.1'
    TCP_PORT = 5005
    BUFFER_SIZE = 2048

    connected = False

    def __init__(self, ip=None, port=None):
        if ip is not None:
            self.TCP_IP = ip
        if port is not None:
            self.TCP_PORT = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, ip=None, port=None):
        if not ip:
            ip = self.TCP_IP
        if not port:
            port = self.TCP_PORT
        try:
            self.s.connect((ip, port))
            self.connected = True
        except:
            return False
        return True

    def send(self, message):
        if not self.connected:
            self.connect()
        self.s.send(message)
        data = self.s.recv(self.BUFFER_SIZE)
        print(data)

    def disconnect(self):
        self.s.close()
        self.connected = False
