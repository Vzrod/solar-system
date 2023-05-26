# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 17:07:31 2023

@author: arthu

pyinstyalle client.py --onefile --windowed --collect-submodules solar-system


!!!!!!!!!!!!!!!! close file when window close

"""

import socket
from threading import Thread

import tkinter as tk
import tkinter.messagebox
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
        
        print("Init client")
        # Thread affichage GUI
        #tfen = Thread(target = self.affichage_fen, args=(2,))
        #tfen.start()
        #self.conn()
        
        tconn = Thread(target = self.conn) #Démarre la connection de la fonction conn sur un thread afin de ne pas freeze le gui
        tconn.start()
        
        
    def conn(self):
        """Démarre la connction avec le serveur et transmet le pseudo"""
        print("con")
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.settimeout(5) #Timeout de 5s
        print("socket crée")
        try:
            self.socket.connect((self.host, self.port))

            self.start_listen()
            self.socket.send(('<PSEUDO>'+self.pseudo).encode('utf-8'))
        except socket.error as msg:
            print(f'Socket error : {msg}')
        
        
        
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
        