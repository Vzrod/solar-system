# -*- coding: utf-8 -*-
"""
Created on Fri Apr 28 21:27:10 2023

@author: kamdoum alex, haas zoe, clot arthur
"""

import tkinter as tk
import time
from NSI_client import threadedClient




class GUI():
    
    #game_state = 0
    
    def __init__(self):
        self.demin=tk.Tk()
        self.demin.geometry("520x570")
        self.demin.title("Partie de démineur")
        
        self.menu=tk.Frame(self.demin)
        self.menu.grid()
        
        self.plage=tk.Frame(self.demin,height=200,width=300)
        self.plage.grid()
        
        self.plat = {}
        self.dico = {}
    
    
    
    def update(uplist):
        global list_update
        for case in uplist:
            if plat[case[0],case[1]][2]==0:
                dico[case[0],case[1]].configure(text=case[2],fg=color(case[0],case[1]))
            else:
                dico[case[0],case[1]].configure(text=case[2],fg=color(case[0],case[1]),bg="red")
        list_update=[]
        
                
    def color(x,y):
        """
        
    
        Parameters
        ----------
        x : int
            absciss value of case.
        y : int
            y value of case.
    
        Returns
        -------
        str
            Retourne la couleur de la case entrée.
    
        """
        l=["white","#56ea62","green","sienna1","red","turquoise4","#ff7700","purple","VioletRed"]
        if plat[x,y][2]==0:
            return l[plat[x,y][3]]
        else:
            return "black"
    
    def restart():
        """
        Appelé pour réinitialiser le plateau et l'interface.
    
        Returns
        -------
        None.
    
        """
        global game_state
        for coords in list(dico.keys()):
            dico[coords].destroy()
        retry_button.destroy()
        lost_label.destroy()
        game_state=0
        start()
        
    def mouse(event):
        """
        Recupère l'event du clic et créer un dictionnaire des infos relatives à l'event
    
        Parameters
        ----------
        event : clic gauche
            DESCRIPTION.
    
        Returns
        -------
        None.
    
        """
        global grid_info
        grid_info = event.widget.grid_info()
        print(grid_info["row"], grid_info["column"])
    
                
    def flag(self, event):
        global grid_sources
        grid_sources=event.widget.grid_info()
        if game_state==0:
            if plat[grid_sources["row"], grid_sources["column"]][0]==0 and not(plat[grid_sources["row"], grid_sources["column"]][2]==-1 and plat[grid_sources["row"], grid_sources["column"]][1]==-1) and not(plat[grid_sources["row"], grid_sources["column"]][1]==-1 and plat[grid_sources["row"], grid_sources["column"]][2]==0):
                plat[grid_sources["row"], grid_sources["column"]][0]=-2
                dico[grid_sources["row"], grid_sources["column"]].configure(text=chr(9872),fg="black")
            elif plat[grid_sources["row"], grid_sources["column"]][0]==-2:
                plat[grid_sources["row"], grid_sources["column"]][1]=0
                plat[grid_sources["row"], grid_sources["column"]][0]=0
                dico[grid_sources["row"], grid_sources["column"]].configure(text="")
    
    def dico_button(self, taille):
        for i in range(taille[0]):
            for j in range(taille[1]):
                self.dico[(i, j)] = tk.Button(self.plage, height=1, width=3, font=("Helvetica", "20"),text=None)
                #dico[i, j]["command"]=lambda button= dico[i, j]: mouse()
                self.dico[i, j].grid(row=i,column=j)
                
    
    
    
    
    def main_menu(self):
        
        ip_label = tk.Label(self.menu, text="Server IP :")
        ip_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
        
        ip_entry = tk.Entry(self.menu)
        ip_entry.insert(-1,'127.0.0.0')
        ip_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)
        
        port_label = tk.Label(self.menu, text="Port :")
        port_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
        
        port_entry = tk.Entry(self.menu)
        port_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)
        
        pseudo_label = tk.Label(self.menu, text="Pseudo :")
        pseudo_label.grid(column=0, row=2, sticky=tk.W, padx=5, pady=5)
        
        pseudo_entry = tk.Entry(self.menu)
        pseudo_entry.grid(column=1, row=2, sticky=tk.E, padx=5, pady=5)
        
        
        join_server_btn = tk.Button(self.menu, text="Join Server", command=lambda: self.connect_server(ip_entry.get(), port_entry.get(), pseudo_entry.get()), height=2,width=10)
        join_server_btn.grid(row=3,column=1)
        
    #!!! CHANGER LA DEF ==> LE BTN DOIT APPELER UNE DEF EN THREAD SUR LE CLIENT
    def connect_server(self, ip, port, pseudo):
        if pseudo != "" and port != "" and ip != "":
            print(ip, port, pseudo)
            client = threadedClient(ip, int(port), pseudo)
    
    def start(self):
        self.menu.destroy()
        self.demin_interface=dico_button()
        
    def loose_animation(self, event=None):
        global game_state, retry_button, lost_label
        for case in list(plat.keys()):
            if plat[case][1]==0 and plat[case][2]==-1 and plat[case][0]==0:
                dico[case].configure(text="X", bg="#d33",fg="black")
            elif plat[case][1]==0 and plat[case][2]==-1 and plat[case][0]==-2:
                dico[case].configure(bg="#d33",fg="black")
        game_state=2
        
        lost_label=tk.Label(self.demin,text="You have lost the game, click on the button 'retry' in order to restart the game.",fg="black")
        lost_label.grid(row=taille[0]+1)
        
        retry_button=tk.Button(self.plage,text="Retry",command=restart,height=2,width=5)
        retry_button.grid(row=taille[0]+5,column=int(taille[1]/2))
    
    
    
    #start()
    #Alex tu ne boucles pas sur les test de condition ==> ce code ne s'exécute qu'une fois au début 
    
    self.main_menu()
    
    
    self.demin.bind("<Button-1>",mouse)
    self.demin.bind("<Button-3>",flag)
    
    self.demin.mainloop()













