# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:07:31 2023

@author: arthu
"""

import socket

class client():
    def con_server(self, HOST, PORT, pseudo):
        self.pseudo = pseudo
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.socket:
            self.socket.connect((HOST, PORT))
            print('Connecté au serveur')
            self.socket.send(('<PSEUDO>'+self.pseudo).encode('utf-8'))
            while True:
                data = self.socket.recv(1024)
                print(data)
            
