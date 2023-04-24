# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:07:31 2023

@author: arthu
"""

import socket
from demineur import plateau
from threading import Thread
from gui import *
import tkinter as tk

                     
            
class threadedClient(Thread):
    def __init__(self, host, port, pseudo):
        Thread.__init__(self)
        self.pseudo = pseudo
        self.host = host
        self.port = port
        self.game_state = [False, b'<GAME_INIT>', self.start_game]
        self.turn_cond = [False, b'<GAME_TURN>', lambda:0]
        self.dic = {self.game_state[1]:self.game_state, self.turn_cond[1]:self.turn_cond}
        
        
        tfen = Thread(target = self.affichage_fen, args=(2,))
        tfen.start()

    def conn(self):
        print('conn')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        print('Connecté au serveur')
        self.start_listen(self.game_state)
        self.socket.send(('<PSEUDO>'+self.pseudo).encode('utf-8'))
        
        
    def client_update(self, coord):
        print("client",coord)
        print(self.game_state[0], self.dic[b'<GAME_TURN>'][0])
        if self.game_state[0] == True and self.dic[b'<GAME_TURN>'][0] == True:
            self.socket.send((coord).encode('utf-8'))
            self.dic[b'<GAME_TURN>'][0] = False
    
    
    def listen(self, cond: list):
        print(cond)
        while cond[0] == False:
            try:
                print('att serv')
                data = self.socket.recv(1024)
                if data == cond[1]:
                    print('data == cond[1]')
                    cond[2]()
                    self.dic[cond[1]][0] = True
            except socket.timeout: pass
                
    #def client_update(self):
    
    def start_listen(self, cond):
        t = Thread(target = self.listen, args=(cond,))
        t.start()
        
    def start_game(self):
         print('Game started')
         self.fen.frames['game'].msgbox()
         while True:
             self.listen(self.dic[b'<GAME_TURN>'])
        
    def affichage_fen(self, diff):
        self.fen = gui(diff, self)
        self.fen.mainloop()
        
client = threadedClient('DESKTOP-B717DA8', 2500, 'Vzrod')

