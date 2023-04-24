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
import time

                     
            
class threadedClient(Thread):
    def __init__(self, host, port, pseudo):
        Thread.__init__(self)
        self.pseudo = pseudo
        self.host = host
        self.port = port
        self.game_state = [False, b'GAME_INIT', self.start_game]
        self.turn_cond = [False, b'GAME_TURN', lambda data:0]
        self.listen_update = [False, b'CLIENT_UPDATE', self.gui_update]
        self.dic = {self.game_state[1]:self.game_state, self.turn_cond[1]:self.turn_cond, self.listen_update[1]:self.listen_update}
        
        
        tfen = Thread(target = self.affichage_fen, args=(2,))
        tfen.start()

    def conn(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.start_listen(self.game_state)
        self.socket.send(('<PSEUDO>'+self.pseudo).encode('utf-8'))
        
        
    def client_update(self, coord):
        print("client",coord)
        print(self.game_state[0], self.dic[b'GAME_TURN'][0])
        if self.game_state[0] == True and self.dic[b'GAME_TURN'][0] == True:
            self.socket.send(str((coord)).encode('utf-8'))
            self.dic[b'GAME_TURN'][0] = False
            u = Thread(target = self.listen, args=(self.dic[b'GAME_TURN'],))
            u.start()
    
    
    def listen(self, cond: list):
        print('listen', cond[0])
        while cond[0] == False:
            try:
                print('Att serv :', cond[1])
                data = self.socket.recv(1024)
                if data[data.find(b'<')+1 : data.find(b'>')] == cond[1]:
                    print('data', data, ' == cond[1]', cond[1])
                    cond[2](data)
                    self.dic[cond[1]][0] = True
                    print(cond[1], 'Recu, ligne 57 :', self.dic[cond[1]][0])
            except socket.timeout: pass
                
    def gui_update(self, data):
        undata = data.decode('utf-8').split(',')[1:]
        for coord in undata:
            self.fen.frames['game'].game_update(eval(coord.replace('.',',')))
        v = Thread(target = self.listen, args=(self.dic[b'CLIENT_UPDATE'],))
        v.start()
            
        
        
        
        self.dic[b'CLIENT_UPDATE'][0] = False
        v = Thread(target = self.listen, args=(self.dic[b'CLIENT_UPDATE'],))
        v.start()
    
    def start_listen(self, cond):
        t = Thread(target = self.listen, args=(cond,))
        t.start()
        
    def start_game(self, data):
         print('Game started')
         self.fen.frames['game'].msgbox()
         u = Thread(target = self.listen, args=(self.dic[b'GAME_TURN'],))
         u.start()
         v = Thread(target = self.listen, args=(self.dic[b'CLIENT_UPDATE'],))
         v.start()
         
        
    def affichage_fen(self, diff):
        self.fen = gui(diff, self)
        self.fen.mainloop()
        
client = threadedClient('DESKTOP-B717DA8', 2500, 'Vzrod')

