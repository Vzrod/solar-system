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

file = open('data.csv')
reader = csv.DictReader(file, delimiter=';')

data = [dict(row) for row in reader]

# chaque liste est indexé dans l'ordre : [astre]{x/y/z}:valeur
distances = [{'x':0.0, 'y':0.0, 'z':0.0} for y in range(len(data))]
vitesses = [{'x':0.0, 'y':0.0, 'z':0.0} for y in range(len(data))]
listpositions = [{'x':[], 'y':[], 'z':[]}for y in range(len(data))]

for i in range(len(data)):
    distances[i]['x'] = float(data[i]['distance'])
    vitesses[i]['y'] = float(data[i]['vitesse'])
    data[i]['masse'] = float(data[i]['masse'])

while t<10*365*sec_jour:
    for astre1 in range(len(data)-1):
        for astre2 in range(astre1+1, len(data)):
            dx, dy, dz = distances[astre1]['x'] - distances[astre2]['x'], distances[astre1]['y'] - distances[astre2]['y'], distances[astre1]['z'] - distances[astre2]['z']
            d = (dx**2+dy**2+dz**2)

