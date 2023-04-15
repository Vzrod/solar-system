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

file = open('data2.csv')
reader = csv.DictReader(file, delimiter=',')

class Astre:
    def __init__(self, data:dict):
        self.nom = data.get('nom')                              # Nom astre
        self.vitesse = data.get('vitesse')                      # Vitesse moyenne en m/s
        self.masse = data.get('masse')                          # Masse en kg
        self.distance = data.get('distance')                    # Distance demi-grand axe
        self.x, self.y, self.z = self.distance, 0.0, 0.0        # Position sur le plan
        self.vx, self.vy, self.vz = 0.0, self.vitesse, 0.0      # Vitesse sur les axes
        self.listpos = [[],[],[]]                               # Liste des positions succésives de l'astre pour afficher l'orbite
        
data = [dict(row) for row in reader]

astres = {}     # Dictionnaire des instances de chaque astre

for ligne in data:
    astre_instance = Astre(ligne)   # Génération Instance avec caractéristique
    astres[ligne.get('nom')] = astre_instance   # Ajout instance dans le dictionnaire

del(data)   # Supprime les données d'initialisation car stockées dans les 

liste_astres = list(astres.keys())

file.close()




# chaque liste est indexé dans l'ordre : [astre]{x/y/z}:valeur


while t<10*365*sec_jour:
    for astre1 in range(len(liste_astres)-1):
        for astre2 in range(astre1+1, len(liste_astres)):
            # Calcul du vecteur unitaire (u) entre l'astre 1 et l'astre 2
            # Calcul distance séparant les 2 astres sur chaque axe, vecteur astre1 --> astre2
            ux, uy, uz = astres[liste_astres[astre1]].x - astres[liste_astres[astre2]].x, astres[liste_astres[astre1]].y - astres[liste_astres[astre2]].y, astres[liste_astres[astre1]].z - astres[liste_astres[astre2]].z
            # Calcul de la norme de u au cube car dans la formule on divise par norme u**2 mais avec projection on multiplie par 1/norme u ==> diviser par norme u**3
            normeu = (ux**2+uy**2+uz**2)**1.5 # Correspond à la racine pour calcule norme plus cube : ((d**2)**1/2)**3 ==> **1.5
            # Projection sur les axes de l'interraction gravitationnelle avec le vecteur u ==> G*(m1*m2)/d**2 *u ==> *cos(angle) ==> *u_axe/normeu (équivaut au vecteur unitaire normalisé)
            #Calcul de la force sur l'astre 1
            fx_1 = -G*(astres[liste_astres[astre1]].masse * astres[liste_astres[astre2]].masse)*ux/normeu
            fy_1 = -G*(astres[liste_astres[astre1]].masse * astres[liste_astres[astre2]].masse)*uy/normeu
            fz_1 = -G*(astres[liste_astres[astre1]].masse * astres[liste_astres[astre2]].masse)*uz/normeu
            
            # Calcul de l'accélération avec projection de la seconde loi de newton : F = ma --> a = F/m
            astres[liste_astres[astre1]].vx += fx







for i in range(5-1):
    for y in range(i+1, 5):
        print(f'({i}, {y})')
        
