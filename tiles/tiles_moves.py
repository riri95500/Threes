############################## Partie 2 ##############################
from random import randint
from tiles_acces import *
import sys
sys.path.append("../game/")


def get_next_alea_tiles_coordonnees(plateau, tiles):    #Il faut savoir que la fonction est inaccessible si tiles['check'] = False
    """Retourne une ou deux tuile(s) dont la position ('lig','col) est tiree aleatoirement et correspond a un emplacement libre du plateau"""
    if tiles['mode'] == 'init':  #Si l'on commence une nouvelle partie, mode = 'init'
        tiles['a']['lig'] = 0   #On initialise toutes les coordonnees a 0 de maniere a rentrer dans la boucle while
        tiles['a']['col'] = 0
        tiles['b']['lig'] = 0
        tiles['b']['col'] = 0
        while ((tiles['a']['lig']) == (tiles['b']['lig']) and (tiles['a']['col'] == tiles['b']['col'])):    #Grace a cette boucle,les deux tuiles ne seront pas placees au meme endroit car elle verifie que les coordonnees sont differentes
            tiles['a']['lig'] = randint(0, plateau['n'] - 1)    #Et on reatribut de nouvelles coordonnees dans le cas ou les coordonnees sont les memes
            tiles['a']['col'] = randint(0, plateau['n'] - 1)
            tiles['b']['lig'] = randint(0, plateau['n'] - 1)
            tiles['b']['col'] = randint(0, plateau['n'] - 1)
    elif tiles['mode'] == 'encours' : #Si l'on cherche a obtenir la case suivante d'une partie en cours, mode = 'encours'
        lig = -1    #On fait donc la meme chose mais pour une seule case
        col = -1

        while is_room_empty(plateau ,lig ,col ) != True  :  #On verifie donc que les coordonnees de la case existent et que la case est libre
            lig = randint(0,plateau['n']-1)
            col = randint(0,plateau['n']-1)
        tiles['mode'] = 'encours'
        tiles['lig'] = lig
        tiles['col'] = col
    return tiles

def get_next_alea_tiles_valeurs(mode, plateau):
    from play import is_game_over
    tiles = {}  #Cree le doctionnaire avec les tuiles (le reinitialise s'il existe deja)
    tiles['check'] = not(is_game_over(plateau)) #Actualise la variable 'check' qui permet de savoir si une partie est terminee ou non, en utilisant une vraie fonction game_over
    if mode == 'init':  #Si l'on commence une nouvelle partie mode = 'init'
        valeur_tile_1 = randint(1,2)    #On initialise une premiere valeur parmis 1 ou 2
        if valeur_tile_1 == 1:
            valeur_tile_2 = 2   #On attribut la valeur qui n'a pas ete attribuee a la premiere valeur, 2 dans ce cas
        else:
            valeur_tile_2 = 1   #On attribut la valeur qui n'a pas ete attribuee a la premiere valeur, 1 dans ce cas
        tiles = {   #On cree le dictionnaire tiles avec toutes les cles necessaires
        'mode' : mode,
        'a' : { #La premiere tuile
            'chiffre' : valeur_tile_1,
            },

        'b' : { #La seconde tuile (dans le cas d'une nouvelle partie)
            'chiffre' : valeur_tile_2,
            },
        'check' : True  #check est initie a True etant donne le debut de la partie
        }
    elif mode == 'encours': #Si l'on est sur une partie en cours
        tiles['chiffre'] = randint(1,3) #On choisi juste un chiffre parmis 1,2 ou 3
        tiles['mode'] = 'encours'
    return tiles    #Et on renvoie le dictionnaire


def put_next_tiles(plateau, tiles):
    """Permet de placer une ou deux tuiles dans le plateau
    :parametre plateau: plateau de jeu
    :parametre tiles: dictionnaire sous la forme de celui renvoye par la fonction get_next_alea_tiles"""
    if tiles['mode'] == 'encours':  #Verifie s'il s'agit d'un partie en cours(La structure du dictionnaire tiles varie selon l'avancement de la partie)
        set_value(plateau, tiles['lig'], tiles['col'], tiles['chiffre'])    #Place une seule tuile en cas de partie en cours
    else:
        set_value(plateau, tiles['a']['lig'], tiles['a']['col'], tiles['a']['chiffre']) #Place 2 tuiles en cas de debut de partie
        set_value(plateau, tiles['b']['lig'], tiles['b']['col'], tiles['b']['chiffre'])
    return plateau

def line_pack(plateau, num_lig, debut, sens):
    """Tasse les tuiles d'une ligne dans le sens donne
    plateau: dictionnaire comprenant le plateau du jeu
    num_lig: indice de la ligne a "tasser"
    debut: indice a partir duquel se fait le "tassement"
    sens: sens du "tassement", 1 vers la gauche, 0 vers la droite"""
    i = 0
    k = num_lig * plateau['n']  #La premiere valeur de k correspond au premier element de la ligne que l'on souhaite tasser
    ligne = []  #initialisation de la ligne
    while i < plateau['n']:
        ligne.append(plateau['tiles'][k])   #Recupere les elements de la ligne que l'on souhaite tasser
        i += 1
        k += 1
    if sens == 0:   #Tassement a droite
        while debut > 0:
            ligne[debut] = ligne[debut-1]
            debut -= 1
        ligne[0] = 0
    elif sens == 1: #Tassement a gauche
        while debut < len(ligne) - 1:
            ligne[debut] = ligne[debut+1]
            debut += 1
        ligne[plateau['n']-1] = 0
    return ligne

def column_pack(plateau, num_col, debut, sens):
    """Tasse les tuiles d'une colonne donnee dans un sens donne
    plateau: dictionnaire contenant le plateau du jeu
    num_col: indice de la colonne a "tasser"
    debut: indice a partir duquel se fait le "tassement"
    sens: sens du "tassement", 1 vers le haut, 0 vers le bas"""
    i = 0
    colonne = []    #initialisation de la colonne
    while i < plateau['n'] and num_col < len(plateau['tiles']):
        colonne.append(plateau['tiles'][num_col])   #Recupere les elements de la colonne que l'on souhaite tasser
        i += 1
        num_col += 4
    if sens == 0:   #Tassement vers le bas
        while debut > 0:
            colonne[debut] = colonne[debut-1]
            debut -= 1
        colonne[0] = 0
    elif sens == 1: #Tassement vers le haut
        while debut < len(colonne) - 1:
            colonne[debut] = colonne[debut+1]
            debut += 1
        colonne[plateau['n']-1] = 0
    return colonne

def line_move(plateau, num_lig, sens):
    """Deplacement des tuiles d'une ligne donnee dans un sens donne en appliquant les regles du jeu Threes
    plateau: dictionnaire contenant le plateau du jeu
    num_lig: indice de la ligne pour laquelle il faut deplacer les tuiles
    sens: sens de deplacement des tuiles, 1 vers la gauche, 0 vers la droite"""
    i = 0
    k = num_lig * plateau['n']
    ligne = []  #initialisation de la ligne
    while i < plateau['n']:
        ligne.append(plateau['tiles'][k])   #Recupere les elements de la ligne que l'on souhaite deplacer
        i += 1
        k += 1
    if sens == 0 :  #Deplacement vers la droite
        i = plateau['n'] - 1
        while i > 0 :
            if ligne[i] == 0:   #si la valeur de la case est egale a 0, dans ce cas, la ligne est deplacee sans autre modification
                ligne = line_pack(plateau,num_lig,i,0)
                i = 0
            elif ligne[i] == ligne[i-1] and ligne[i] != 1 and ligne[i] != 2:    #Si 2 elements sont identiques lors du deplacement et qu'ils sont differents de 1 ou 2,
                ligne = line_pack(plateau,num_lig,i,0)  #On tasse les 2 cases pour en obtenir qu'une
                ligne[i] = ligne[i] * 2 #Puis on double la valeur de la case
                i = 0
            elif ligne[i] == 1 and ligne[i - 1] == 2 or ligne[i] == 2 and ligne[i-1] == 1:  # On fait la meme chose qu'au dessus, mais avec les valeurs 1 et 2 qui forment des 3
                ligne = line_pack(plateau,num_lig,i,0)
                ligne[i] = 3
                i = 0
            i -= 1
    elif sens == 1: #Deplacement vers la gauche
        i = 0
        while i < len(ligne) - 1 :  #On fait la meme chose que le deplacement a droite mais a gauche
            if ligne[i] == 0:
                ligne = line_pack(plateau,num_lig,i,1)
                i = len(ligne)
            elif ligne[i] == ligne[i+1] and ligne[i] != 1 and ligne[i] != 2:
                ligne = line_pack(plateau,num_lig,i,1)
                ligne[i] = ligne[i] * 2
                i = len(ligne)
            elif ligne[i] == 1 and ligne[i + 1] == 2 or ligne[i] == 2 and ligne[i + 1] == 1:
                ligne = line_pack(plateau,num_lig,i,1)
                ligne[i] = 3
                i = len(ligne)
            i += 1
    return ligne

def column_move(plateau, num_col, sens):
    """Deplace les tuiles d'une colonne donnee dans un sens donne en appliquant les regles du jeu Threes
    plateau: dictionnaire contenant le plateau du jeu
    num_col: indice de la colonne pour laquelle il faut deplacer les tuiles
    sens: sens de deplacement des tuiles, 1 vers le heut, 0 vers le bas"""
    i = 0
    k = num_col
    colonne = []
    while i < plateau['n'] and k < len(plateau['tiles']):
        colonne.append(plateau['tiles'][k]) #Recupere les elements de la colonne que l'on souhaite deplacer
        i += 1
        k += 4
    if sens == 0 :  #Deplacement vers le bas
        i = plateau['n'] - 1
        while i > 0:    #La fonction est la meme que la precedente pour la suite
            if colonne[i] == 0:
                colonne = column_pack(plateau,num_col,i,0)
                i = 0
            elif colonne[i] == colonne[i-1] and colonne[i] != 1 and colonne[i] != 2:
                colonne = column_pack(plateau,num_col,i,0)
                colonne[i] = colonne[i] * 2
                i = 0
            elif colonne[i] == 1 and colonne[i - 1] == 2 or colonne[i] == 2 and colonne[i-1] == 1:
                colonne = column_pack(plateau,num_col,i,0)
                colonne[i] = 3
                i = 0
            i -= 1
    elif sens == 1: #Deplacement vers le haut
        i = 0
        while i < len(colonne) - 1 :
            if colonne[i] == 0:
                colonne = column_pack(plateau,num_col,i,1)
                i = len(colonne)
            elif colonne[i] == colonne[i+1] and colonne[i] != 1 and colonne[i] != 2:
                colonne = column_pack(plateau,num_col,i,1)
                colonne[i] = colonne[i] * 2
                i = len(colonne)
            elif colonne[i] == 1 and colonne[i + 1] == 2 or colonne[i] == 2 and colonne[i + 1] == 1:
                colonne = column_pack(plateau,num_col,i,1)
                colonne[i] = 3
                i = len(colonne)
            i += 1
    return colonne

def lines_move(plateau, sens):
    """Deplace les tuiles de toutes les lignes du plateau dans un sens donne en aplliquant les regles du jeu Threes
    plateau: dictionnaire contenant le plateau du jeu
    sens: sens de deplacement des tuiles, 1 vers la gauche, 0 vers la droite"""
    i = 0
    while i < plateau['n']:
        k = 0
        ligne = line_move(plateau, i, sens)
        while k < plateau['n']: #k correspond a l'element de la ligne (varie de 0 a 3 pour le cas ou l'on utilise 4 colonnes et lignes)
            if i == 0:
                 plateau['tiles'][k] = ligne[k] #i est egal a 0 sur la premiere ligne, on ne multiplie donc pas la rangee par i (sinon on a 0 partout), comme on le fait en dessous (pour atteindre les autres rangees)
            else:
                plateau['tiles'][k + plateau['n'] * i] = ligne[k]
            k+=1
        i += 1
    return plateau

def columns_move(plateau, sens):
    """Deplace les tuiles de toutes les colonnes du plateau dans le sens donne en appliquant les regles du jeu Threes
    plateau: dictionnaire contenant le plateau du jeu
    sens: sens de deplacement, 1 vers le haut, 0 vers le bas"""
    i = 0
    while i < plateau['n']:
        k = i
        j = 0
        colonne = column_move(plateau, i, sens)
        while k < len(plateau['tiles']):
            plateau['tiles'][k] = colonne[j]
            j += 1
            k += 4
        i += 1
    return plateau

def play_move(plateau, sens):
    """Deplace les tuiles du plateau dans un sens donne en appliquant les regles du jeu Threes
    plateau: dictionnaire contenant le plateau de jeu
    sens: sens de deplacement des tuiles:   'b': bas
                                            'h': haut
                                            'd': droite
                                            'g': gauche"""
    if sens == 'b':
        columns_move(plateau, 0)    #En fonction du deplacement voulu, on fait appel aux fonctions de deplacement pour modifier le plateau
    elif sens == 'h':
        columns_move(plateau, 1)
    elif sens == 'd':
        lines_move(plateau, 0)
    elif sens == 'g':
        lines_move(plateau, 1)
    return plateau
