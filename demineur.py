# -*- coding: utf-8 -*-
"""
Created on Thu Apr 20 20:05:12 2023

@author: arthu
"""
from sys import getsizeof
import random as rnd

def gen_dico(taille: tuple):
    dico = {}
    for i in range(taille[0]):
        for y in range(taille[1]):
            dico[(i, y)] = [0,0,0,0]
    return dico

def gen_mines(dico: dict, nbbombes):
    listeb = []
    xmax = max([key[0] for key in dico.keys()])+1
    ymax = max([key[1] for key in dico.keys()])+1
    nbcases = (xmax)*(ymax)
    liste = [i for i in range(nbcases)]
    rnd.shuffle(liste)
    for _ in range(nbbombes):
        nb = liste.pop()
        dico[(nb//(xmax), nb%ymax)][2] = -1
        listeb.append((nb//(xmax), nb%ymax))
    
    return dico, listeb

def aff_nb(dico: dict, listeb):
    for bombe in listeb:
        coinX = bombe[0]-1
        coinY = bombe[1]-1
        print(coinX)
        print(coinY)
        for i in range(9):
            if (((i//3)+coinX, (i%3)+coinY) in dico) and not(i==4):
                dico[((i//3)+coinX, (i%3)+coinY)][3]+=1
            
    return dico



































"""
def gen_liste(taille: tuple):
    liste = [[[[0], [0], [0], [0]] for _ in range(taille[0])] for _ in range(taille[1])]
    return liste

print('Dico', getsizeof(gen_dico((500,500))))
print('Liste', getsizeof(gen_liste((500,500))))
"""