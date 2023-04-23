# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 09:41:37 2023

@author: aclot
"""

import random as rnd
import socket
from demineur import plateau

class server():
    
    def __init__(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.bind((socket.gethostname(), 2500))
        print(socket.gethostname())
        self.serversocket.listen(5)
        self.lobby()
            
    def lobby(self):
        self.cons_socket = []
        self.players = {}
        while len(self.cons_socket) != 2:
            print('Att co')
            clientsocket, addr = self.serversocket.accept()
            data = clientsocket.recv(1024).decode('utf-8')
            print('receive', data)
            if data[:8] == '<PSEUDO>':
                self.players[addr] = data[8:]
                self.cons_socket.append(clientsocket)
                print(self.cons_socket)
                if len(self.cons_socket) == 2:
                    for client in self.cons_socket:
                        try : client.send(b'bonsoir')
                        except socket.error: self.cons_socket.remove(client)
                print(len(self.cons_socket))
        print('Debut game')
    