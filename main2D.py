# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 13:40:19 2023
@author: arthu
"""
import csv
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.colors as mcolors

G = 6.67430e-11
sec_jour = 24.0*60**2
t = 0.0
dt = 1*sec_jour
AU = 1.5E11
 feUR
file = open('data4.csv')
reader = csv.DictReader(file, delimiter=',')

fig, ax = plt.subplots(figsize=(10,10))
ax.set_aspect('equal')
ax.grid()
ax.axis('equal')
ax.set_xlim(-15*AU,15*AU)
ax.set_ylim(-15*AU,15*AU)

class Astre:
    def __init__(self, data:dict):
        self.nom = data.get('nom')                              # Nom astre
        self.vitesse = float(data.get('vitesse'))               # Vitesse moyenne en m/s
        self.masse = float(data.get('masse'))                   # Masse en kg
        self.distance = float(data.get('distance'))             # Distance demi-grand axe
        self.x, self.y, self.z = self.distance, 0.0, 0.0        # Position sur le plan
        self.vx, self.vy, self.vz = 0.0, self.vitesse, 0.0      # Vitesse sur les axes
        self.listpos = [[],[],[]]                               # Liste des positions succésives de l'astre pour afficher l'orbite
        self.color = data.get('couleur')
        self.fx, self.fy, self.fz = 0.0, 0.0, 0.0
        self.xdata, self.ydata = [], []
        self.line, = ax.plot([],[],'-g', lw=1,c=mcolors.CSS4_COLORS[self.color])
        self.point, = ax.plot([self.distance], [0], marker="o", markersize=4, markeredgecolor=mcolors.CSS4_COLORS[self.color], markerfacecolor=mcolors.CSS4_COLORS[self.color]) 
        self.text = ax.text(self.distance, 0, self.nom)

        
data = [dict(row) for row in reader]

astres = {}     # Dictionnaire des instances de chaque astre

for ligne in data:
    astre_instance = Astre(ligne)   # Génération Instance avec caractéristique
    astres[ligne.get('nom')] = astre_instance   # Ajout instance dans le dictionnaire

del(data)   # Supprime les données d'initialisation car stockées dans les 

liste_astres = list(astres.keys())

file.close()

while t<100*365*sec_jour:
    for astre1 in range(len(liste_astres)-1):
        for astre2 in range(astre1+1, len(liste_astres)):
            # Calcul du vecteur unitaire (u) entre l'astre 1 et l'astre 2
            # Calcul distance séparant les 2 astres sur chaque axe, vecteur astre1 --> astre2
            ux, uy, uz = astres[liste_astres[astre1]].x - astres[liste_astres[astre2]].x, astres[liste_astres[astre1]].y - astres[liste_astres[astre2]].y, astres[liste_astres[astre1]].z - astres[liste_astres[astre2]].z
            # Calcul de la norme de u au cube car dans la formule on divise par norme u**2 mais avec projection on multiplie par 1/norme u ==> diviser par norme u**3
            normeu = (ux**2+uy**2+uz**2)**1.5 # Correspond à la racine pour calcule norme plus cube : ((d**2)**1/2)**3 ==> **1.5
            # Projection sur les axes de l'interraction gravitationnelle avec le vecteur u ==> G*(m1*m2)/d**2 *u ==> *cos(angle) ==> *u_axe/normeu (équivaut au vecteur unitaire normalisé)
            #Calcul de la force sur l'astre 1
            astres[liste_astres[astre1]].fx += -G*(astres[liste_astres[astre1]].masse * astres[liste_astres[astre2]].masse)*ux/normeu
            astres[liste_astres[astre1]].fy += -G*(astres[liste_astres[astre1]].masse * astres[liste_astres[astre2]].masse)*uy/normeu
            astres[liste_astres[astre1]].fz += -G*(astres[liste_astres[astre1]].masse * astres[liste_astres[astre2]].masse)*uz/normeu
            
            #Calcul de la force sur l'astre 2
            astres[liste_astres[astre2]].fx += -astres[liste_astres[astre1]].fx
            astres[liste_astres[astre2]].fy += -astres[liste_astres[astre1]].fy
            astres[liste_astres[astre2]].fz += -astres[liste_astres[astre1]].fz
                  
    # application forces :
    for astre in range(len(liste_astres)):
        #test
        # Calcul et ajout de la variation de vitesse à la vitesse de l'astre avec projection de la seconde loi de newton : F = ma avec a = d_v/d_t --> d_v = F*d_t/m
        astres[liste_astres[astre]].vx += astres[liste_astres[astre]].fx*dt/astres[liste_astres[astre]].masse
        astres[liste_astres[astre]].vy += astres[liste_astres[astre]].fy*dt/astres[liste_astres[astre]].masse
        astres[liste_astres[astre]].vz += astres[liste_astres[astre]].fz*dt/astres[liste_astres[astre]].masse
        
        # Actualisation de la position avec projection sur les axes : v = d/t -> d = v*t
        astres[liste_astres[astre]].x += astres[liste_astres[astre]].vx*dt
        astres[liste_astres[astre]].y += astres[liste_astres[astre]].vy*dt
        astres[liste_astres[astre]].z += astres[liste_astres[astre]].vz*dt
        
        # Enregistrement position de l'astre
        astres[liste_astres[astre]].listpos[0].append(astres[liste_astres[astre]].x)
        astres[liste_astres[astre]].listpos[1].append(astres[liste_astres[astre]].y)
        astres[liste_astres[astre]].listpos[2].append(astres[liste_astres[astre]].z)

        astres[liste_astres[astre]].fx = 0.0
        astres[liste_astres[astre]].fy = 0.0
        astres[liste_astres[astre]].fz = 0.0
    
    t += dt
            
def update(i):
    tup_update = ()
    for astre in range(len(liste_astres)):
        astres[liste_astres[astre]].xdata.append(astres[liste_astres[astre]].listpos[0][i])
        astres[liste_astres[astre]].ydata.append(astres[liste_astres[astre]].listpos[1][i])
    
    for astre in range(len(liste_astres)):
        astres[liste_astres[astre]].line.set_data(astres[liste_astres[astre]].xdata, astres[liste_astres[astre]].ydata)
        
        astres[liste_astres[astre]].point.set_data(astres[liste_astres[astre]].listpos[0][i], astres[liste_astres[astre]].listpos[1][i])
        
        astres[liste_astres[astre]].text.set_position((astres[liste_astres[astre]].listpos[0][i],astres[liste_astres[astre]].listpos[1][i]))
        
        tup_update += astres[liste_astres[astre]].line,
        tup_update += astres[liste_astres[astre]].point,
        tup_update += astres[liste_astres[astre]].text,
        
    return tup_update

anim = animation.FuncAnimation(fig,func=update,frames=len(astres['Terre'].listpos[0]),interval=1,blit=True)
plt.show()
