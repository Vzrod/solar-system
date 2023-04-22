# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 09:41:37 2023

@author: aclot
"""

import socket


class server():
    
    def __init__(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.serversocket:
            self.serversocket.bind((socket.gethostname(), 2500))
            self.serversocket.listen(5)
            self.start()
            
    def start(self):
        
        
        
        clientsocket, addr = self.serversocket.accept()
        with clientsocket:
            


