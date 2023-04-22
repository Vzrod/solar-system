# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 20:05:12 2023

@author: arthu
"""
import random as rnd

class plateau():
    
    def __init__(self, diff: int):
        print('diff',diff)
        self.dico = {}
        self.listeb = []
        self.diff = diff
        self.difficultes = {0: ((9,9), 10), 1: ((16,16), 40), 2:((30, 16), 99)}
        self.gen_dico()
        self.gen_mines()
        self.aff_nb()
    
    def gen_dico(self):
        for i in range(self.difficultes[self.diff][0][0]):
            for y in range(self.difficultes[self.diff][0][1]):
                self.dico[(i, y)] = [0,0,0,0]
    
    
    def gen_mines(self):
        xmax = max([key[0] for key in self.dico.keys()])+1
        ymax = max([key[1] for key in self.dico.keys()])+1
        nbcases = (xmax)*(ymax)
        liste = [i for i in range(nbcases)]
        rnd.shuffle(liste)
        for _ in range(self.difficultes[self.diff][1]):
            nb = liste.pop()
            self.dico[(nb//(xmax), nb%ymax)][2] = -1
            self.listeb.append((nb//(xmax), nb%ymax))
        
    
    def aff_nb(self):
        for bombe in self.listeb:
            coinX = bombe[0]-1
            coinY = bombe[1]-1
            for i in range(9):
                if (((i//3)+coinX, (i%3)+coinY) in self.dico) and not(i==4):
                    self.dico[((i//3)+coinX, (i%3)+coinY)][3]+=1
    
    def affichage(self):
        xmax = max([key[0] for key in self.dico.keys()])+1
        ymax = max([key[1] for key in self.dico.keys()])+1
        for i in range(xmax):
            for y in range(ymax):
                if self.dico[(i,y)][2]!=-1:
                    print(f' {self.dico[(i,y)][3]} |', end='')
                else :
                    print(' X |', end='')
            print('')

