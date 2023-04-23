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
        self.game_state = [False, b'<GAME_INIT>', self.start_game]
        
        
        
        
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print('Connecté au serveur')
        self.start_listen()
        self.socket.send(('<PSEUDO>'+self.pseudo).encode('utf-8'))
        
        
    
    def listen(self, cond: tuple):
        print(cond)
        while cond[0] == False:
            try:
                print('att serv')
                data = self.socket.recv(1024)
                if data == cond[1]:
                    cond[2]()
                    cond[0] = True
            except socket.timeout: pass
    
    def start_listen(self):
        t = Thread(target = self.listen, args=(self.game_state,))
        t.start()
        
    def start_game(self):
         print('test')
        
        