# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 09:41:37 2023

@author: aclot

(b'<GAME_TURN>,350,(1.2.4),(2.3.6)').decode('utf-8').split(',')

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
        host = ''
        port = 2500
        domain = 'demineur.ddns.net'
        self.serversocket.bind((host, port))
        ip_address = socket.gethostbyname(domain)
        print(ip_address)
        print(socket.gethostname())
        self.serversocket.listen(5)
        self.lobby()
            
    def lobby(self):
        self.game_state = True
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
        self.game = plateau()
        self.game.init_plat(2)
        self.game.log_affichage()
        print()
        time.sleep(5)
        for client in self.cons_socket:
            try : 
                client.send(b'<GAME_INIT>')
                print('Send GAME INIT')
            except socket.error: 
                client.send(b'<SERVER_ERROR>')
                self.lobby()
                break
        while self.game_state:
            for client in self.cons_socket:
                cur_player = self.players[client]
                self.reponse = False
                client.send(b'<GAME_TURN>')
                t_start = time.time()
                data = client.recv(1024)
                d = (data).decode('utf-8')
                plate_update = self.game.coup(eval(d))
                if plate_update == 'Lost':
                    for client in self.cons_socket:
                        client.send(b'<CLIENT_LOST>'+cur_player.encode('utf-8'))
                    self.game_state = False
                    break
                self.game.affichage()
                print()
                self.playerstime[client] = self.playerstime[client] - round(time.time() - t_start, 2)
                com = b'<CLIENT_UPDATE>'
                for up in plate_update:
                    com+=b','+up.encode('utf-8')
                for client in self.cons_socket:
                    client.send(com)
                    
                
                
                
                """
                    for c in self.cons_socket:
                        c.send(('<END_GAME>'+self.players[client]).encode('utf-8')) #Nom Perdant
                """
s = threadedServer()                    
                    
                
        
        
    