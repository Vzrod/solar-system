# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:07:31 2023

@author: arthu
"""

import socket
from demineur import plateau
from threading import Thread

            
class threadedClient(Thread):
    def __init__(self, host, port, pseudo):
        Thread.__init__(self)
        self.pseudo = pseudo
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print('Connecté au serveur')
        self.socket.send(('<PSEUDO>'+self.pseudo).encode('utf-8'))
    
    def listen(self):
        try:
            print('att serv')
            data = self.socket.recv(1024)
            print(data)
            return data
        except socket.timeout: pass
    
    def start_listen(self):
        t = Thread(target = self.listen)
        t.start()
        
        