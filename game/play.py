from termcolor import colored
import sys
sys.path.append("../tiles/")

############################## Partie 1 ##############################

def init_play():
    """Retourne un plateau correspondant a une nouvelle partie"""
    plateau = {
        'n' : 4, #Le nombre de colonnes et de lignes
        'nb_cases_libres' : 16,
        'tiles' : [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    }
    return plateau

def is_game_over(plateau):
    from tiles_moves import play_move
    """Retourne 'True' si la partie est terminee, 'False' sinon """
    i = 0
    plateau2 = list(plateau['tiles'])   #Cree une copie des tuiles du plateau
    a = 0   #a est une variable qui permet de compter le nombre de deplacements ou le mouvement effectue ne change pas le plateau
    sens = ['h','d','b','g']
    for i in sens:  #On verifie donc pour chaque mouvement effectue, si le plateau reste le meme
        play_move(plateau, i)
        if plateau2 == plateau['tiles']:    #A chaque fois que le mouvement est le meme on incremente a
            a += 1
        plateau['tiles'] = list(plateau2)   #Apres chaque mouvement on retabli le plateau a l'origine
    return a == 4

def get_score(plateau):
    """Retourne le score du plateau"""
    i = 0
    score = 0

    while i < len(plateau['tiles']):    #Incremente 'i' pour toutes les cases du plateau jusqu'a la derniere case
        score += plateau['tiles'][i]    #Incremente le score avec donc, toutes les cases du plateau
        i += 1
    return score

def simple_display(plateau):
    """Affichage du plateau de la facon simplifiee"""
    i = 0
    ligne = ''
    while i < len(plateau['tiles']):
        while i < len(plateau['tiles']) and i%plateau['n'] != 0:    #On creer une ligne de l'affichage jusqu'a ce que 'i' soit un multiple de 'plateau['n']', etant donne que le nombre de 'col' est egal au nombre de 'lig'
            ligne += str(plateau['tiles'][i]).center(5)  #On concatene la valeur d'une case du plateau avec le reste de la ligne et on ajuste pour 5 caracteres la case
            i += 1
        if i != 0:
            print(ligne)    #On affiche la ligne
        if i < len(plateau['tiles']):   #Creer une nouvelle ligne si nous ne sommes pas a la fin de la ligne
            ligne = str(plateau['tiles'][i]).center(5)
        i += 1

def medium_display(plateau):
    """Affichage du plateau avec delimitations textuelles des cases"""
    ligne_etoiles = ''
    i=0
    while i < plateau['n']: #Initialise le nombre d'etoiles par colonnes en fonction du nombre de colonnes 'n'
        ligne_etoiles += '*******'
        i += 1
    i = 0
    print(ligne_etoiles)
    ligne = '*'  #Creer une nouvelle ligne vide
    while i < len(plateau['tiles']):    #Boucle qui cree l'ensemble de toutes les lignes de l'affichage
        if i%plateau['n'] == 0 and i != 0: #Si 'i' est un multiple de 'plateau['n']' on affiche la ligne et on en cree une autre, etant donne que le nombre de 'col' est egal au nombre de 'lig'
            print(ligne)
            print(ligne_etoiles)
            ligne = '*'
        ligne += str(plateau['tiles'][i]).center(5) #Ajoute le case plateau['tiles'][i] a la ligne
        ligne += '*'.center(2)  #Ajoute une etoile a la ligne pour fermer la case
        i += 1
    print(ligne)    #Affiche la derniere ligne du plateau
    print(ligne_etoiles)    #Affiche la ligne d'etoiles pour cloturer l'affichage

def full_display(plateau):
    """Affichage en couleurs"""
    ligne = ''  #Represente une ligne de cases
    ligne_haut = '' #'ligne_haut' est l'equivalent de 'ligne' mais sans les caracteres elle n'a qu'un objectif qui est esthetique
    i=0
    while i < len(plateau['tiles']):    #Cette boucle cree l'ensemble des lignes
        if i%plateau['n'] == 0 and i != 0: #Si 'i' est un multiple de 'plateau['n']' on affiche la ligne et on en cree une autre, etant donne que le nombre de 'col' est egal au nombre de 'lig'
            print(ligne_haut)   #On affiche d'abord cette ligne pour avoir une 'jolie' case
            print(ligne)    #Ensuite on affiche la ligne
            print(ligne_haut)   #Puis de nouveau cette ligne qui vient recentrer la 'ligne'
            ligne_haut = '' #On vide maintenant les lignes pour les reremplir
            ligne = ''
            print(ligne)    #On affiche cette ligne vide pour delimiter les cases
        if plateau['tiles'][i] == 1:    #Les conditions des if, elif, et else suivants n'ont pour but que de changer la couleur de la case en fonction de ce qu'elle contien
            ligne_haut += colored(str(" ").center(5),'white','on_blue') + " "   #Du blanc sur du cyan pour la valeur 1
            ligne += colored(str(plateau['tiles'][i]).center(5),'white','on_blue') + " "
        elif plateau['tiles'][i] == 2:  #Du blanc sur du rouge pour la valeur 2
            ligne_haut += colored(str(" ").center(5),'white','on_red') + " "
            ligne += colored(str(plateau['tiles'][i]).center(5), 'white','on_red') + " "
        elif plateau['tiles'][i] == 0:  #Une case vide de couleur bleu pour la valeur 0
            ligne_haut += colored(str("").center(5),'grey','on_yellow') + " "
            ligne += colored(str(" ").center(5), 'grey','on_yellow') + " "
        else:   #Et du gris sur du blanc pour les valeurs supperieures a 2
            ligne_haut += colored(str(" ").center(5),'grey','on_white') + " "
            ligne += colored(str(plateau['tiles'][i]).center(5), 'grey','on_white') + " "
        i += 1
    print(ligne_haut)   #On affiche enfin la derniere ligne de cases
    print(ligne)
    print(ligne_haut)

############################## Partie 3 ##############################

def create_new_play():
    """Creer et retourne une nouvelle partie"""
    from tiles_moves import get_next_alea_tiles_coordonnees, get_next_alea_tiles_valeurs, put_next_tiles
    plateau = init_play()   #Initialise le plateau vide
    tiles = get_next_alea_tiles_valeurs('init', plateau)    #Recupere les 2 premieres tuiles
    tiles = get_next_alea_tiles_coordonnees(plateau, tiles) #Ainsi que leurs coordonnees
    put_next_tiles(plateau, tiles)  #Et les place dans le plateau
    tiles = get_next_alea_tiles_valeurs('encours', plateau) #Obtient la prochaine tuile a afficher
    partie ={   #Creation du dictionnaire partie avec les elements necessaires au bon fonctionnement de la partie
        'plateau' : plateau,
        'next_tile' : tiles,
        'score' : get_score(plateau)
    }
    return partie
