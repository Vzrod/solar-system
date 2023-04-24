# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 09:41:37 2023

@author: aclot
"""

import random as rnd
import socket
from demineur import plateau
from threading import Thread
import time

class threadedServer(Thread):
    
    def __init__(self):
        Thread.__init__(self)
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
                self.players[clientsocket] = data[8:]
                self.cons_socket.append(clientsocket)
                if len(self.cons_socket) == 2:
                    for client in self.cons_socket:
                        try : client.send(b'bonsoir')
                        except socket.error: self.cons_socket.remove(client)
                print(len(self.cons_socket))
        print('Debut game')
        self.start_game()
        
        
        
    def start_game(self):
        self.playerstime = {client:420 for client in self.cons_socket}
        time.sleep(5)
        for client in self.cons_socket:
            try : client.send(b'<GAME_INIT>')
            except socket.error: 
                client.send(b'<SERVER_ERROR>')
                self.lobby()
                break
        while True:
            for client in self.cons_socket:
                self.reponse = False
                client.send(b'<GAME_TURN>')
                t_start = time.time()
                data = client.recv(1024)
                print(eval((data).decode('utf-8')))
                self.playerstime[client] = self.playerstime[client] - round(time.time() - t_start, 2)
                
                """
                    for c in self.cons_socket:
                        c.send(('<END_GAME>'+self.players[client]).encode('utf-8')) #Nom Perdant
                """
s = threadedServer()                    
                    
                
        
        
    