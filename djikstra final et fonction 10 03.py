# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 14:26:31 2023

@author: arthu

Test implémentation djikstra final

id_gare_py est construit sur l'ordre croissant de id_gare_con

Pour pallier aux branches sur ligne metro, ex metro 7 : id_ligne = 7 ligne principale (ligne + connection haute) et 7.1 (connection basse)

Mairie d'aubervillier

"""


import sys
import pandas as pd

df = pd.read_excel(r'C:\Users\arthu\Documents\projetdextraTest.xlsx')

Blanc = 0
Noir = 1

dist_station_metro = 2

pre_aretes = [[] for i in range(df['id_gares_py'].max()+1)]

lignes = [str(a) for a in range(1, 15)] + ['A1', 'A2', 'A3', 'A4', 'B1', 'B2', 'B3', 'C', 'D', 'E', 'L', 'U']
lignes.insert(3, '3bis')
lignes.insert(8, '7.1')
lignes.insert(9, '7b')
lignes.insert(13, '10.1')


def sort_stations(df = df, i=0):
    """Récupere les lignes stations par ligne de metro et les ordonnes selont leurs positions. Retourne un tableau en 2 dimmensions contenant uniquement les infos sur la ligne"""
    data = df.loc[df['indice_lig']==str(lignes[i])]
    data.sort_values(by=['ord'], inplace=True)
    return data.reset_index(drop=True)
    
def voisins(index_station):
    """Génere la liste de dictionnaire des stations de métros et leur distances"""
    if ligne['mode'][index_station] == 'METRO':
        if index_station == 0:
            list_voisins = {ligne.loc[index_station + 1, 'id_gares_py']: dist_station_metro}
        elif index_station == (len(ligne)-1):
            list_voisins = {ligne.loc[index_station - 1, 'id_gares_py']: dist_station_metro}
        else:
            list_voisins = {ligne.loc[index_station - 1, 'id_gares_py']: dist_station_metro, ligne.loc[index_station + 1, 'id_gares_py']:dist_station_metro}
    return [list_voisins]
    
    
for i in range(5):
    ligne = sort_stations(df, i)
    for y in range(len(ligne)):
        n_sta = ligne.loc[y, 'id_gares_py']
        if pre_aretes[n_sta] == []:
            pre_aretes[n_sta] += voisins(y)
        else:
            pre_aretes[n_sta] = [{**pre_aretes[n_sta][0], **voisins(y)[0]}] #Concatène dictionnaire si connection sur autres lignes


def name_of_id_gare(id_gare, df = df):
    return df.loc[df['id_gares_py']==id_gare, 'nom'].array[0]




class Graphe:
    def __init__(self, aretes):
        self.aretes = aretes
        self.nodes = [i for i in range(0, len(aretes))]
        self.init_data()
        self.id_path = []
        
    def __len__(self):
        return len(self.aretes)
    
    def init_data(self):
        n = len(self.aretes)
        self.peres = n * [-1]
        self.dist = n * [-1]
        self.couleurs = n * [Blanc]
    def get_nodes(self):
        return self.nodes
    def get_outgoing_edges(self, node):
        connections = []
        for nodes in self.aretes[node][0].keys():
            connections.append(nodes)
        return connections
    def value(self, node1, node2):
        return self.aretes[node1][0][node2]
    
    
        

def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())
    shortest_path = {}
    previous_nodes = {}
    max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = max_value
    #Node départ dist = 0 
    shortest_path[start_node] = 0
    
    while unvisited_nodes:
        # Node avec plus petite val
        current_min_node = None
        for node in unvisited_nodes: # Iterate over the nodes
            if current_min_node == None:
                current_min_node = node
            elif shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
                
        # Recupere voisin node actuel et change distance
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # Conserve historique node utilisé pour meilleur chemin
                previous_nodes[neighbor] = current_min_node
 
        # Mettre node comme "marqué"
        unvisited_nodes.remove(current_min_node)
    
    return previous_nodes, shortest_path


# Résultat détaillé
def print_result(previous_nodes, shortest_path, start_node, target_node):
    gmetro.id_path = []
    path = []
    node = target_node
    
    while node != start_node:
        gmetro.id_path.append(node)
        node = previous_nodes[node]
 
    # Add the start node manually
    gmetro.id_path.append(start_node)
    for id_station in gmetro.id_path:
        path.append(name_of_id_gare(id_station))
    
    print("Itinéraire d'une distance de {}.".format(shortest_path[target_node]))
    print(" -> ".join(reversed(path)))
    

def ligne_connections():
    """Retourne tuple nom ligne et gare changement / arrivée"""
    compteur_lignes = {}
    save_id_path = list(gmetro.id_path)
    for ligne in df.loc[df['id_gares_py']==gmetro.id_path[-1], 'ligne'].array: #Pour chaques lignes de la station de départ
        gmetro.id_path = list(save_id_path)
        compteur_nb_gares_it = 0 # Compteur nombre de gare pour chaque ligne jusqu'a prochain changement
        while True:
            compteur_nb_gares_it += 1
            if compteur_nb_gares_it >= len(gmetro.id_path) or not(ligne in df.loc[df['id_gares_py']==gmetro.id_path[-(compteur_nb_gares_it)-1], 'ligne'].array) : break
        compteur_lignes[ligne] = (compteur_nb_gares_it, gmetro.id_path[-(compteur_nb_gares_it)])
    liste = [(compteur, nom, id_sta) for nom, (compteur, id_sta) in compteur_lignes.items()]
    liste.sort()
    del gmetro.id_path[-(liste[-1][0]-1):]
    return liste[-1][1], liste[-1][2]



def print_itinerary(previous_nodes, shortest_path, start_node, target_node):
    gmetro.id_path = []
    node = target_node
    
    while node != start_node:
        gmetro.id_path.append(node)
        node = previous_nodes[node]
 
    # Add the start node manually
    gmetro.id_path.append(start_node)
    
    itinerary = []
    
    itinerary.append(gmetro.id_path[-1])
    while len(gmetro.id_path) != 1:
        ligne, id_sta = ligne_connections()
        itinerary.append(ligne)
        itinerary.append(id_sta)
    for i in range(0, len(itinerary), 2):
        itinerary[i] = name_of_id_gare(itinerary[i])
    print(" -> ".join(itinerary))
        
    
"""
def print_itinerary(previous_nodes, shortest_path, start_node, target_node):
    id_path = []
    itinerary = []
    node = target_node
    
    while node != start_node:
        id_path.append(node)
        node = previous_nodes[node]
 
    # Add the start node manually
    id_path.append(start_node)
    
    itinerary.append(id_path[-1])
    
    compteur_lignes = {}
    
    print(id_path)
    
    for ligne in df.loc[df['id_gares_py']==id_path[-1], 'ligne'].array: #Pour chaques lignes de la station de départ
        compteur_nb_gares_it = 0 # Compteur nombre de gare pour chaque ligne jusqu'a prochain changement
        while True:
            compteur_nb_gares_it += 1
            print(ligne, compteur_nb_gares_it, id_path[-(compteur_nb_gares_it)])
            if compteur_nb_gares_it >= len(id_path) or not(ligne in df.loc[df['id_gares_py']==id_path[-(compteur_nb_gares_it)-1], 'ligne'].array) : break
        compteur_lignes[ligne] = (compteur_nb_gares_it, id_path[-(compteur_nb_gares_it)])
        print(compteur_lignes)
"""        
    
    
gmetro = Graphe(pre_aretes)

previous_nodes, shortest_path = dijkstra_algorithm(graph=gmetro, start_node=31)

#print_result(previous_nodes, shortest_path, start_node=3, target_node=69)
print_itinerary(previous_nodes, shortest_path, start_node=31, target_node=38)
