# -*- coding: utf-8 -*-
"""
Created on Fri May 26 10:16:29 2023

@author: arthu
"""

import random as rnd

def gen_dico(taille: tuple):
    """
    Parameters
    ----------
    taille : tuple
        Génère des cases auxquelles on associe un dictionnaire donnant les indications de la case (initialisation donc vide).

    Returns
    -------
    dico : dict
        Dictionnaire retourné

    """
    dico = {}
    for i in range(taille[0]):
        for y in range(taille[1]):
            dico[(i, y)] = [0,0,0,0] #[le flag ?, découverte ?, bombe ?, nb bombes ]
    return dico




def aleat_bomb(plateau: dict):
    """
    

    Parameters
    ----------
    plateau : dict
        Définit aléatoirement l'emplacement des bombes, update le dictionnaire pour chaque case.

    Returns
    -------
    plateau : dict

    """
    places=list(plateau.keys())
    nb_bombs=int(len(places)/4)
    rnd.shuffle(places)
    bombs=places[0:nb_bombs] #emplacement des bombes
    for bomb in bombs:
        plateau[bomb]=[0,0,-1,0]
        for x in range(bomb[0]-1,bomb[0]+2):
            for y in range (bomb[1]-1,bomb[1]+2):
                if (x,y) in places and (x,y)!=bomb: #vérfie si a case existe
                    plateau[x,y][3]+=1                    
    return plateau

def print_dico(plateau):
    """
    

    Parameters
    ----------
    plateau : dict
        Affichage du plateau dans la console.

    Returns
    -------
    None.

    """
    for y in range(taille[1]):
        print("| ",end="")
        for x in  range(taille[0]):
            if plateau[x,y][1]==-1:
                print(plateau[x,y][3],end=" | ")
            else:
                print(".",end=" | ")
        print()
        
"""
def coup(plateau,coord:tuple): #(x,y,bool)
    if plateau[coord][2] == -1:
        print("Perdu")
        game_state = False
    #else :
    return game_state
"""




def destroy_zeros_plat(l) :
    global list_update
    zeros=[]
    for zero in l:
        for y in range(zero[1]-1,zero[1]+2):
            for x in range (zero[0]-1,zero[0]+2):
                if (x,y) in list(plat.keys()) and ((x,y)!=zero and (plat[x,y][1]==0 and (plat[x,y][2]==0 and plat[x,y][0]==0))):
                  plat[x,y][1]=-1
                  list_update.append((x,y,plat[x,y][3]))
                  if plat[x,y][3]==0:
                      zeros.append((x,y))
    if len(zeros)!=0:
        destroy_zeros_plat(zeros)
    else:
        update(list_update)

def discover_case_plat(x0,y0):
    global game_state, list_update
    list_update=[]
    if game_state==0:
        if plat[x0,y0][2]==0 and plat[x0,y0][0]==0:
            plat[x0,y0][1]=-1
            list_update.append((x0,y0,plat[x0,y0][3]))
            zeros=[]
            for y in range(grid_info["column"]-1,grid_info["column"]+2):
                for x in range (grid_info["row"]-1,grid_info["row"]+2):
                    if (x,y) in list(plat.keys()) and ((x,y)!=(x0,y0) and (plat[x,y][3]==0 and plat[x,y][1]==0 and plat[x,y][2]==0)):
                        zeros.append((x,y))
                        plat[x,y][1]=-1
                        list_update.append((x,y,plat[x,y][3]))
            if len(zeros)==0:
                update(list_update)
            else:
                destroy_zeros_plat(zeros)
        elif plat[x0,y0][2]==-1 and not(plat[x0,y0][0]==-2):
            plat[x0,y0][1]=-1
            list_update.append((x0,y0,"X"))
            update(list_update)
            game_state=1
            loose_animation()