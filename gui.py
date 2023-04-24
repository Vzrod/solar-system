# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 10:16:43 2023

@author: arthu
"""

import tkinter as tk

class gui(tk.Tk):
    def __init__(self, diff, client):
        tk.Tk.__init__(self)
        #self.geometry('1000x400')
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.diff = diff
        self.client = client
        
        
        self.frames = {}
        for F in (home, game):
            frame_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[frame_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame('home')
        
    def show_frame(self, frame_name):
        frame = self.frames.get(frame_name)
        frame.tkraise()
    
             
class home(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        label = tk.Label(self, text="Démineur Multijoueur")
        label.pack(side='top', pady=10)
        
        button = tk.Button(self, text="Lancer la partie", command=lambda: self.cmd())
        button.pack()
        
    def cmd(self):
        print('cmd')
        self.controller.show_frame("game")
        self.controller.client.conn()

# --------------------A refaire ----------------------
class game(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.difficultes = {0: ((9,9), 10), 1: ((16,16), 40), 2:((16, 30), 99)}
        self.diff = controller.diff
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        
        self.count_frame = tk.Frame(self, padx=10, pady=30)
        self.count_frame.grid(row=0, column=0, sticky="nsew")
        self.count = tk.Label(self.count_frame, text="Timer : ", font=("Helvetica", "20"), fg="blue")
        self.count.pack()
        
        
        self.grid_frame = tk.Frame(self)
        self.grid_frame.grid(row=1, column=0, sticky="nsew")
        for x in range(self.difficultes[self.diff][0][0]):
            for y in range(self.difficultes[self.diff][0][1]):
                button = tk.Button(self.grid_frame, height=1, width=3, font=("Helvetica", "20"))
                button.grid(row = x, column = y)
                button.bind('<Button-1>', self.left_click_helper(x, y))
                button.bind('<Button-3>', self.right_click_helper(x, y))
    
    def left_click_helper(self, x, y):
        return lambda event: self.left_clicked((x, y))
        
    def right_click_helper(self, x, y):
        return lambda event: self.right_clicked((x, y))
    
    
    def left_clicked(self, coord):
        
        print(coord)
        button = self.grid_frame.grid_slaves(row=coord[0], column=coord[1])[0]
        if button.cget('text') == '':
            self.controller.client.client_update(coord)
            self.count.configure(bg="red")
        
    def right_clicked(self, coord):
        print(coord)
        self.flag_update(coord, 'F')
        
    def flag_update(self, coord: tuple, txt: str):
        button = self.grid_frame.grid_slaves(row=coord[0], column=coord[1])[0]
        
        if button.cget('text') == 'F':
            button.configure(text='', fg='black')
        elif button.cget('text') == '': button.configure(text='F', fg='red')
        
    def countdown(self, temps):
        print('countdown')
        self.count.configure(text="Timer : {}".format(temps), bg="yellow")
        
    def msgbox(self):
        tk.messagebox.showinfo("Démineur",  "Game started!")
        
    def game_update(self, coord):
        button = self.grid_frame.grid_slaves(row=coord[0], column=coord[1])[0]
        if coord[2] == 0:
            button.destroy()
        else:
            button.configure(text = str(coord[2]))
            
    def losemsg(self, pseudo):
        tk.messagebox.showinfo("Démineur", f'Le joueur {pseudo} a perdu')
            


"""
class game(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.difficultes = {0: ((9,9), 10), 1: ((16,16), 40), 2:((16, 30), 99)}
        self.diff = controller.diff
        self.l_but = {}
        for x in range(self.difficultes[self.diff][0][0]):
            for y in range(self.difficultes[self.diff][0][1]):
                self.l_but[(x, y)] = tk.Button(height=1, width=3, font=("Helvetica", "20"), command = lambda r = x, c = y : self.clicked(r,c))
                self.l_but[(x,y)].grid(row = x, column = y)
                
    def clicked(self, x, y):
        print(x, y)
        self.update((x,y), 'X')
        
    def update(self, coord: tuple, txt: str):
        self.l_but[coord].configure(text = txt, fg='red')
        self.l_but[coord].destroy()
"""        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    