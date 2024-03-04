# ---------- IMPORTS ---------- #
from random import *
import math
import matplotlib.pyplot as plt

# ---------- FONCTIONS ---------- #
def genererVilles(nombreVilles) :
    '''
    DESCRIPTION
    ----------
    Génère une matrice de coordonnées ( abscisses et ordonnées ) 
    comprises entre 0 et 1 pour chacune des n villes
    
    Parameters
    ----------
    nombreVilles : Int

    Returns
    -------
    villes : Matrice de coordonnées des n villes
    '''
    villes = []
    for k in range(nombreVilles) :
        coordonnees = [round(random(),2), round(random(),2)]
        villes.append(coordonnees)
    return villes



def genererDistances(nombreVilles) :
    '''
    DESCRIPTION
    ----------
    Génère une matrice de distance entre toutes les villes
    
    Parameters
    ----------
    nombreVilles : Int

    Returns
    -------
    distances : matrice de distances entre les n villes
    '''
    villes = genererVilles(nombreVilles)
    distances = []
    for i in range(len(villes)) :
        distancesVilleCourante = []
        for j in range(len(villes)) :
            distancesVilleCourante.append(round(math.sqrt((villes[i][0] - villes[j][0])**2 + (villes[i][1] - villes[j][1])**2),2))
        distances.append(distancesVilleCourante)
    placerVilles(villes)
    return distances, villes



def afficherCoordonneesVilles(villes) :
    '''
    DESCRIPTION
    ----------
    Affiche les coordonnées des villes

    Parameters
    ----------
    villes : Liste de coordonnées
    '''
    for k in range(len(villes)) :
        print(villes[k])



def afficherDistances(distances) :
    '''
    DESCRIPTION
    ----------
    Affiche les distances entre les villes
    
    Parameters
    ----------
    distances : Matrice de distances
    '''
    for k in range(len(distances)) :
        print(distances[k])
        
        
        
def placerVilles(villes) :
    '''
    DESCRIPTION
    ----------
    Place les villes sur un graphe
    
    Parameters
    ----------
    villes : Matrice de coordonnées ( [[x,y],[x,y],...])
    '''
    for k in range(len(villes)) :
        plt.scatter(villes[k][0], villes[k][1])
        
        
        
def genererChemin(nombreVilles, distances) :
    '''
    DESCRIPTION
    ----------
    Genere un chemin. Par exemple pour une liste de [0,3,4,1,2],
    On part de la ville 0, on va à la ville 3 puis à la ville 4, etc...
    
    Parameters
    ----------
    nombreVilles : Liste des indices des villes
    '''
    chemin = [k for k in range(nombreVilles)]
    shuffle(chemin)
    distanceChemin = calculerDistancePourUnChemin(chemin, distances)
    chemin.append(distanceChemin)
    return chemin



def genererPopulation(nombreChemins, nombreVilles, distances) :
    '''
    DESCRIPTION
    ----------
    Genere une population de n chemins
    
    Parameters
    ----------
    nombreChemins : Le nombre de chemins voulu pour une population
    nombreVilles : Le nombre de villes 
    '''
    population = []
    for k in range(nombreChemins) :
        population.append(genererChemin(nombreVilles, distances))
    return population



def calculerDistancePourUnChemin(chemin, distances) :
    '''
    DESCRIPTION
    -----------
    Calcule la distance d'un chemin grâce à la matrice distances.
    Par exemple pour une liste de [0,3,4,1,2],
    On regarde distances[0][3], puis on ajoute distances[3][4], etc...
    A la fin, on fait distances[len(villes)][0] 
    ( len(villes) = nombres de villes générés )

    Parameters
    ----------
    chemin : Liste d'indices de villes correspondant à un chemin
    distances : Matrice des distances entre toutes les villes
    '''
    distanceChemin = 0
    for k in range(len(chemin) - 1) :
        distanceChemin += distances[chemin[k]][chemin[k + 1]]
    distanceChemin += distances[chemin[0]][chemin[len(chemin) - 1]]
    return round(distanceChemin,2)



def trierPopulation(population, villes, generation) :
    '''
    DESCRIPTION
    -----------
    Trie par ordre croissant la population 
    en fonction de la distance de chaque chemin

    Parameters
    ----------
    population : Liste des chemins et leurs distances
    villes : Coordonnées des villes
    '''
    populationTriee = sorted(population, key=lambda x: x[-1])
    afficherMeilleurChemin(populationTriee[0], villes, generation)
    return populationTriee     



def afficherMeilleurChemin(chemin, villes, generation) :
    '''
    DESCRIPTION
    -----------
    Affiche sur le graphique le meilleur chemin

    Parameters
    ----------
    chemin : Liste d'indices de villes correspondant à un chemin 
    villes : Coordonnées des villes
    '''
    plt.figure(figsize=(10, 10))
    placerVilles(villes)
    for k in range(len(chemin) - 2) :
        x = [villes[chemin[k]][0] , villes[chemin[k + 1]][0]] 
        y = [villes[chemin[k]][1] , villes[chemin[k + 1]][1]]
        plt.plot(x, y, color='blue')
    xFinal = [villes[chemin[0]][0] , villes[chemin[-2]][0]] 
    yFinal = [villes[chemin[0]][1] , villes[chemin[-2]][1]]
    plt.plot(xFinal,yFinal, color='blue')
    plt.plot([], [], color='blue', label=f'Meilleur chemin génération {generation} de distance {chemin[len(chemin)-1]}')
    plt.legend(loc='lower left')
    plt.show()



def selection(population, nombreVilles, distances) :
    '''
    DESCRIPTION
    ----------
    Selectionne les n // 2 meilleurs chemins de la génération précédente, 
    puis effectue des croisements entre le meilleur et tous les autres
    ( n // 2 étant la moitié de la taille de la population ).
    Puis il a 1/10 chances d'effectuer une mutation

    Parameters
    ----------
    population : Liste des chemins et leurs distances
    nombreVilles : Le nombre de villes générées
    distances : La matrices des distances entre toutes les villes
    '''
    nouvelleGeneration = [population[k] for k in range(len(population) // 2)]
    indice = 1
    while (len(nouvelleGeneration) < len(population)) :
        nouvelleGeneration.append(croisement(population[0], population[indice], distances))
        indice += 1
    for k in range(len(nouvelleGeneration)) :
        mutationProbabilite = randint(0,9)
        if mutationProbabilite == 0 :
            nouvelleGeneration[k]
            nouvelleGeneration[k] = mutation(nouvelleGeneration[k], distances)
    return nouvelleGeneration
        


def croisement(cheminOriginal_1, cheminOriginal_2, distances) :
    '''
    DESCRIPTION
    ----------
    On coupe les deux chemins en 2. On forme un nouveau chemin avec ces 2
    moitiés, si il y a des doublons dans ce nouveau chemin alors,
    selon la moitié dans lequel il y a des doublons, on change le doublon
    avec une autre ville. On recommence pour tous les doublons
    
    Parameters
    ----------
    cheminOriginal_1 : Liste d'indices de villes correspondant à un chemin 
    cheminOriginal_2 : Liste d'indices de villes correspondant à un chemin 
    distances : La matrices des distances entre toutes les villes
    '''
    chemin_1 = cheminOriginal_1[:-1]
    chemin_2 = cheminOriginal_2[:-1]    
    cheminEnfant = []
    for k in range(len(chemin_1)) :
        if (k % 2 == 0) :
            cheminEnfant.append(chemin_1[k])
        else :
            cheminEnfant.append(chemin_2[k])
    doublons = trouverIndiceDoublon(cheminEnfant)
    if doublons :
        for valeur, indice in doublons.items():
            if indice % 2 == 0:
                for item in chemin_1:
                    if item not in cheminEnfant:
                        cheminEnfant[indice] = item
            else:
                for item in chemin_2:
                    if item not in cheminEnfant :
                        cheminEnfant[indice] = item
    cheminEnfant.append(calculerDistancePourUnChemin(cheminEnfant, distances))
    return cheminEnfant



def trouverIndiceDoublon(cheminEnfant) :
    '''
    DESCRIPTION
    -----------
    Trouve les indices des doublons dans un chemin donné.
    
    Parameters
    ----------
    cheminEnfant : Liste d'indices de villes correspondant à un chemin.
    
    Returns
    -------
    indicesDoublons : Un dictionnaire contenant les éléments en 
    doublon en tant que clés et leurs indices respectifs en tant que valeurs.
    '''
    indicesDoublons = {}
    for i, item in enumerate(cheminEnfant) :
        if cheminEnfant.count(item) > 1:
            indicesDoublons[item] = i
    return indicesDoublons



def mutation(chemin, distances) :
    '''
    DESCRIPTION
    ----------
    Echange 2 villes d'un chemin de façon aléatoire
    
    Parameters
    ----------
    chemin : Liste d'indices de villes correspondant à un chemin 
    distances : La matrices des distances entre toutes les villes
    '''
    cheminMute = chemin.copy()
    cheminMute.pop(-1)
    indiceUnAleatoire = randint(0, len(chemin) - 2)
    indiceDeuxAleatoire = randint(0, len(chemin) - 2)
    while indiceDeuxAleatoire == indiceUnAleatoire:
        indiceUnAleatoire = randint(0, len(chemin) - 2)
        indiceDeuxAleatoire = randint(0, len(chemin) - 2)
    cheminMute[indiceUnAleatoire], cheminMute[indiceDeuxAleatoire] = cheminMute[indiceDeuxAleatoire], cheminMute[indiceUnAleatoire]
    cheminMute.append(calculerDistancePourUnChemin(cheminMute, distances))
    return cheminMute



def afficherMeilleurCheminDernierCheminEtPremierChemin(premierChemin, dernierChemin, meilleurChemin, villes) :
    '''
    DESCRIPTION
    -----------
    Affiche sur le graphique le meilleur chemin, le premier chemin et 
    le dernier chemin trouvé par l'algo

    Parameters
    ----------
    chemin : Liste d'indices de villes correspondant à un chemin 
    villes : Coordonnées des villes
    '''
    plt.figure(figsize=(10, 10))
    placerVilles(villes)
    for k in range(len(premierChemin) - 2) :
        x = [villes[premierChemin[k]][0] , villes[premierChemin[k + 1]][0]] 
        y = [villes[premierChemin[k]][1] , villes[premierChemin[k + 1]][1]]
        plt.plot(x, y, color='green')
    xFinal = [villes[premierChemin[0]][0] , villes[premierChemin[-2]][0]] 
    yFinal = [villes[premierChemin[0]][1] , villes[premierChemin[-2]][1]]
    plt.plot(xFinal,yFinal, color='green')
    plt.plot([], [], color='green', label=f'Premier Chemin de distance {premierChemin[-1]}')
    plt.legend(loc='lower left')
    plt.show()
    for k in range(len(dernierChemin) - 2) :
        x = [villes[dernierChemin[k]][0] , villes[dernierChemin[k + 1]][0]] 
        y = [villes[dernierChemin[k]][1] , villes[dernierChemin[k + 1]][1]]
        plt.plot(x, y, color='red')
    xFinal = [villes[dernierChemin[0]][0] , villes[dernierChemin[-2]][0]] 
    yFinal = [villes[dernierChemin[0]][1] , villes[dernierChemin[-2]][1]]
    plt.plot(xFinal,yFinal, color='red')
    plt.plot([], [], color='red', label=f'Dernier Chemin de distance {dernierChemin[-1]}')
    plt.legend(loc='lower left')
    plt.show()
    for k in range(len(meilleurChemin) - 2) :
        x = [villes[meilleurChemin[k]][0] , villes[meilleurChemin[k + 1]][0]] 
        y = [villes[meilleurChemin[k]][1] , villes[meilleurChemin[k + 1]][1]]
        plt.plot(x, y, color='blue')
    xFinal = [villes[meilleurChemin[0]][0] , villes[meilleurChemin[-2]][0]] 
    yFinal = [villes[meilleurChemin[0]][1] , villes[meilleurChemin[-2]][1]]
    plt.plot(xFinal,yFinal, color='blue')
    plt.plot([], [], color='blue', label=f'Meilleur Chemin de distance {meilleurChemin[-1]}')
    plt.legend(loc='lower left')
    plt.show()



def algorithmeGenetique(nombreVilles, nombreChemins, nombreGenerationsMax) :
    generation = 0
    distances, villes = genererDistances(nombreVilles)
    population = genererPopulation(nombreChemins, nombreVilles, distances)
    compteur = 0 # Cas d'arrêt de l'algorithme
    while(compteur < 100 and generation <= nombreGenerationsMax ) :
        if generation == 0 :    
            populationTrie = trierPopulation(population, villes, generation)
            premierChemin = populationTrie[0]
            meilleurChemin = premierChemin
        else :
            populationTrie = trierPopulation(nouvellePopulation, villes, generation)
            dernierChemin = populationTrie[0]
            if meilleurChemin[-1] > dernierChemin[-1] :
                meilleurChemin = dernierChemin
                compteur = 0 # Si le chemin change, on réinitialise le cas d'arrêt
            else :
                compteur += 1
        nouvellePopulation = selection(populationTrie, nombreVilles, distances)
        generation += 1
    afficherMeilleurCheminDernierCheminEtPremierChemin(premierChemin, dernierChemin, meilleurChemin, villes)
    
# ---------- CODE ---------- #
nombreVilles = 20
nombreChemins = 100
nombreGenerationsMax = 1000

algorithmeGenetique(nombreVilles, nombreChemins, nombreGenerationsMax)