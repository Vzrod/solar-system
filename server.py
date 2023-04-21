# -*- coding: utf-8 -*-
"""
Created on Fri Apr 21 09:41:37 2023

@author: aclot
"""

import socket


serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serversocket.bind((socket.gethostname(), 80))

serversocket.listen(5)


