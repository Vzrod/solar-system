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
        self.client_lost = [False, b'CLIENT_LOST', self.lose_game]
        self.dic = {self.game_state[1]:self.game_state, self.turn_cond[1]:self.turn_cond, self.listen_update[1]:self.listen_update, self.client_lost[1]:self.client_lost}
        
        # Thread affichage GUI
        tfen = Thread(target = self.affichage_fen, args=(2,))
        tfen.start()

    def conn(self):
        """Démarre la connction avec le serveur et transmet le pseudo"""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.host, self.port))
        self.start_listen()
        self.socket.send(('<PSEUDO>'+self.pseudo).encode('utf-8'))
        
        
    def client_update(self, coord):
        """Fonct appelée par le gui lorsqu'une case est cliquée, envoie au serveur la case cliqué si c'est le tour du client"""
        print("client", coord)
        print(self.game_state[0], self.dic[b'GAME_TURN'][0])
        if self.game_state[0] == True and self.dic[b'GAME_TURN'][0] == True:
            self.socket.send(str((coord)).encode('utf-8'))
            self.dic[b'GAME_TURN'][0] = False # Termine le tour du client
    
    
    
    def listen(self):
        """Fonct lancée en thread pour écouter msg du serv et call fonct correspondante"""
        print('listen')
        try:
            data = self.socket.recv(2048)
            print(data)
            header = data[data.find(b'<')+1 : data.find(b'>')]
            if header in self.dic:
                print('data', data, ' == cond[1]', self.dic[header][1])
                self.dic[header][2](data)
                self.dic[header][0] = True
                print(self.dic[header][0], 'Recu, ligne 57 :', self.dic[header][0])
            else : pass
        except socket.timeout: pass
        finally:
            self.start_listen()
                
        
        
    def gui_update(self, data):
        """Communique au GUI les cases à modifier"""
        undata = data.decode('utf-8').split(',')[1:]
        for coord in undata:
            self.fen.frames['game'].game_update(eval(coord.replace('.',',')))
    
    def start_listen(self):
        """Fonct démarre le thread d'écoute"""
        print("start thread listen")
        t = Thread(target = self.listen)
        t.start()
        
    def start_game(self, data):
        """Fonct appelée par serveur depuis listen lors du démarrage de la game/ synchro clients"""
        print('Game started')
        self.fen.frames['game'].msgbox()
    
    def lose_game(self, data):
        print('game lost')
        pseudo = data[data.find(b'>')+1:]
        print(pseudo)
        self.fen.frames['game'].losemsg(pseudo.decode('utf-8'))

        
    def affichage_fen(self, diff):
        self.fen = gui(diff, self)
        self.fen.mainloop()
        
client = threadedClient('DESKTOP-B717DA8', 2500, 'Vzrod')

