# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 10:16:43 2023

@author: arthu
"""

from tkinter import *

class gui():
    def __init__(self):
        self.fen = Tk()
        self.fen.title("Démineur Python Multiplayer")
        self.fen.resizable(0,0)
        self.gen_grid(2)
        #self.fen.geometry("400x300")
        
        self.fen.mainloop()
             
        
    def gen_grid(self, diff):
        self.difficultes = {0: ((9,9), 10), 1: ((16,16), 40), 2:((16, 30), 99)}
        self.diff = diff
        self.l_but = {}
        for x in range(self.difficultes[self.diff][0][0]):
            for y in range(self.difficultes[self.diff][0][1]):
                self.l_but[(x, y)] = Button(height=1, width=3, font=("Helvetica", "20"), command = lambda r = x, c = y : self.clicked(r,c))
                self.l_but[(x,y)].grid(row = x, column = y)
                
    def clicked(self, x, y):
        print(x, y)
        self.update((x,y), 'X')
        
    def update(self, coord: tuple, txt: str):
        self.l_but[coord].configure(text = txt, fg='red')
        self.l_but[coord].destroy()