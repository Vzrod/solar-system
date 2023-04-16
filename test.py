# -*- coding: utf-8 -*-
"""
Created on Sat Apr 15 22:35:06 2023

@author: arthu
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 13:40:19 2023
@author: arthu
"""
import csv

G = 6.67430e-11
sec_jour = 24.0*60**2
t = 0.0
dt = 1*sec_jour
AU = 1.5E11

file = open('data3.csv')
reader = csv.DictReader(file, delimiter=',')

class Astre:
    def __init__(self, data:dict):
        self.nom = data.get('nom')                              # Nom astre
        self.vitesse = float(data.get('vitesse'))               # Vitesse moyenne en m/s
        self.masse = float(data.get('masse'))                   # Masse en kg
        self.distance = float(data.get('distance'))             # Distance demi-grand axe
        self.x, self.y, self.z = self.distance, 0.0, 0.0        # Position sur le plan
        self.vx, self.vy, self.vz = 0.0, self.vitesse, 0.0      # Vitesse sur les axes
        self.listpos = [[],[],[]]                               # Liste des positions succésives de l'astre pour afficher l'orbite
        self.test = []
        
data = [dict(row) for row in reader ]#  if row['nom']=='Terre' or row['nom']=='Soleil']

astres = {}     # Dictionnaire des instances de chaque astre

for ligne in data:
    astre_instance = Astre(ligne)   # Génération Instance avec caractéristique
    astres[ligne.get('nom')] = astre_instance   # Ajout instance dans le dictionnaire

del(data)   # Supprime les données d'initialisation car stockées dans les 

liste_astres = list(astres.keys())

file.close()


norme = []
fox = []

# chaque liste est indexé dans l'ordre : [astre]{x/y/z}:valeur


while t<1*365*sec_jour:
    for astre1 in range(len(liste_astres)-1):
        for astre2 in range(astre1+1, len(liste_astres)):
            #astre1 = 1
            #astre2 = 0
            # Calcul du vecteur unitaire (u) entre l'astre 1 et l'astre 2
            # Calcul distance séparant les 2 astres sur chaque axe, vecteur astre1 --> astre2
            ux, uy, uz = astres[liste_astres[astre1]].x - astres[liste_astres[astre2]].x, astres[liste_astres[astre1]].y - astres[liste_astres[astre2]].y, astres[liste_astres[astre1]].z - astres[liste_astres[astre2]].z
            # Calcul de la norme de u au cube car dans la formule on divise par norme u**2 mais avec projection on multiplie par 1/norme u ==> diviser par norme u**3
            normeu = (ux**2+uy**2+uz**2)**1.5 # Correspond à la racine pour calcule norme plus cube : ((d**2)**1/2)**3 ==> **1.5
            if astres[liste_astres[astre1]].nom=='Terre' or astres[liste_astres[astre2]].nom=='Terre' :norme.append(normeu)

            # Projection sur les axes de l'interraction gravitationnelle avec le vecteur u ==> G*(m1*m2)/d**2 *u ==> *cos(angle) ==> *u_axe/normeu (équivaut au vecteur unitaire normalisé)
            #Calcul de la force sur l'astre 1
            fx = -G*(astres[liste_astres[astre1]].masse * astres[liste_astres[astre2]].masse)*ux/normeu
            fy = -G*(astres[liste_astres[astre1]].masse * astres[liste_astres[astre2]].masse)*uy/normeu
            fz = -G*(astres[liste_astres[astre1]].masse * astres[liste_astres[astre2]].masse)*uz/normeu
            if astres[liste_astres[astre1]].nom=='Terre' or astres[liste_astres[astre2]].nom=='Terre' :fox.append(fx)          

            # Calcul et ajout de la variation de vitesse à la vitesse de l'astre avec projection de la seconde loi de newton : F = ma avec a = d_v/d_t --> d_v = F*d_t/m
            astres[liste_astres[astre1]].vx += fx*dt/astres[liste_astres[astre1]].masse
            astres[liste_astres[astre1]].vy += fy*dt/astres[liste_astres[astre1]].masse
            astres[liste_astres[astre1]].vz += fz*dt/astres[liste_astres[astre1]].masse
            print(astres[liste_astres[astre1]].vx)
            
            # Actualisation de la position avec projection sur les axes : v = d/t -> d = v*t
            astres[liste_astres[astre1]].x += astres[liste_astres[astre1]].vx*dt
            astres[liste_astres[astre1]].y += astres[liste_astres[astre1]].vy*dt
            astres[liste_astres[astre1]].z += astres[liste_astres[astre1]].vz*dt
            print(astres[liste_astres[astre1]].vx*dt)
            
            # Enregistrement position de l'astre
            astres[liste_astres[astre1]].listpos[0].append(astres[liste_astres[astre1]].x)
            astres[liste_astres[astre1]].listpos[1].append(astres[liste_astres[astre1]].y)
            astres[liste_astres[astre1]].listpos[2].append(astres[liste_astres[astre1]].z)
           
            
            ############## Application sur le 2e astre ################
            
            # Calcul et ajout de la variation de vitesse à la vitesse de l'astre avec projection de la seconde loi de newton : F = ma avec a = d_v/d_t --> d_v = F*d_t/m
            astres[liste_astres[astre2]].vx += -fx*dt/astres[liste_astres[astre2]].masse
            astres[liste_astres[astre2]].vy += -fy*dt/astres[liste_astres[astre2]].masse
            astres[liste_astres[astre2]].vz += -fz*dt/astres[liste_astres[astre2]].masse
            print(astres[liste_astres[astre2]].vx)
            
            # Actualisation de la position avec projection sur les axes : v = d/t -> d = v*t
            astres[liste_astres[astre2]].x += astres[liste_astres[astre2]].vx*dt
            astres[liste_astres[astre2]].y += astres[liste_astres[astre2]].vy*dt
            astres[liste_astres[astre2]].z += astres[liste_astres[astre2]].vz*dt
            
            # Enregistrement position de l'astre
            astres[liste_astres[astre2]].listpos[0].append(astres[liste_astres[astre2]].x)
            astres[liste_astres[astre2]].listpos[1].append(astres[liste_astres[astre2]].y)
            astres[liste_astres[astre2]].listpos[2].append(astres[liste_astres[astre2]].z)

    t += dt      

"""            
import matplotlib.pyplot as plt
from matplotlib import animation

fig, ax = plt.subplots(figsize=(10,10))
ax.set_aspect('equal')
ax.grid()

line_e,     = ax.plot([],[],'-g',lw=1,c='blue')
point_e,    = ax.plot([AU], [0], marker="o"
                      , markersize=4
                      , markeredgecolor="blue"
                      , markerfacecolor="blue")
text_e      = ax.text(AU,0,'Earth')

point_s,    = ax.plot([0], [0], marker="o"
                      , markersize=7
                      , markeredgecolor="yellow"
                      , markerfacecolor="yellow")
text_s      = ax.text(0,0,'Sun')

exdata,eydata = [],[]                   # earth track
sxdata,sydata = [],[]                   # sun track

print(len(xelist))

def update(i):
    exdata.append(xelist[i])
    eydata.append(yelist[i])
    
    line_e.set_data(exdata,eydata)
    point_e.set_data(xelist[i],yelist[i])
    text_e.set_position((xelist[i],yelist[i]))

    point_s.set_data(xslist[i],yslist[i])
    text_s.set_position((xslist[i],yslist[i]))
    ax.axis('equal')
    ax.set_xlim(-3*AU,3*AU)
    ax.set_ylim(-3*AU,3*AU)

    return line_e,point_s,point_e,text_e,text_s

anim = animation.FuncAnimation(fig
                                ,func=update
                                ,frames=len(xelist)
                                ,interval=1
                                ,blit=True)
plt.show()            
"""