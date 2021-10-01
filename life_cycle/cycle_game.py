from termcolor import colored
import os
import sys
sys.path.append("../game/")
from play import *
sys.path.append("../tiles")
from tiles_moves import *
sys.path.append("./ui/")
from user_entries import *

############################## Partie 3 ##############################

def cycle_play(partie):
    """Permet de jouer a Threes
    partie: partie de jeu en cours, None sinon
    retourne True si la partie est terminee, False si le menu est demande

    Sequencement des actions pour cette fonction:
    1 - afficher le plateau de jeu
    2 - afficher la prochaine tuile pour informer le joueur
    3 - saisir le mouvement propose par le jouer ; deux cas possibles:
        * jouer le coup du joueur courant, mettre le score a jour et revenir au point 1
        * ou retourner False si le menu est demande
    4 - si partie terminee, retourne True"""
    if partie == None:
        partie = create_new_play()  #Si la fonction est appelee avec une partie vide, on fait appel a la fonctione qui en creee une
    while True: #Cette boucle ne s'arrete jamais sauf en cas de game over ou en cas de demande du menu
        plateau2 = list(partie['plateau']['tiles']) #Cree un double des tuiles du plateau en cours
        full_display(partie['plateau']) #On affiche le plateau
        print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~')   #Puis cette ligne purement esthetique
        ligne_haut = "                 "    #On initialise la ligne avec des espaces pour qu'elle soit alignee avec les elements qui suivent
        ligne = "Prochaine tuile: " #Il est demande un affichage textuel uniquement pour la prochaine tuile mais nous preferons l'affichage colore
        if partie['next_tile']['chiffre'] == 1:    #Les conditions des if, elif, et else suivants n'ont pour but que de changer la couleur de la case en fonction de ce qu'elle contien
            ligne_haut += colored(str(" ").center(5),'white','on_blue') + " "    #Du blanc sur du cyan pour la valeur 1
            ligne += colored(str(partie['next_tile']['chiffre']).center(5),'white','on_blue') + " "
        elif partie['next_tile']['chiffre'] == 2:  #Du blanc sur du rouge pour la valeur 2
            ligne_haut += colored(str(" ").center(5),'white','on_red') + " "
            ligne += colored(str(partie['next_tile']['chiffre']).center(5), 'white','on_red') + " "
        else:   #Et du gris sur du blanc pour les valeurs supperieures a 2
            ligne_haut += colored(str(" ").center(5),'grey','on_white') + " "
            ligne += colored(str(partie['next_tile']['chiffre']).center(5), 'grey','on_white') + " "
        print(ligne_haut)   #On affiche cette ligne pour que la case ne soit pas toute petite
        print(ligne)    #La ligne avec la prochaine tuile
        print(ligne_haut)   #Puis de nouveau cette ligne pour la meme raison que la premiere fois
        print('')   #On affiche une ligne vide pour avoir un espace
        print(('Votre score: ') + str(partie['score'] ))    #Puis le score actuel
        i=0 #On initialise i a 0 afin que l'on puisse voir dans la boucle ou si l'on a effectue un mauvais mouvement et afficher un message
        while plateau2 == partie['plateau']['tiles']:
            if i > 0 :  #Si l'on effectue un mouvement qui ne deplace pas le plateau on atteri dans cette boucle
                print(colored(str("Ce mouvement n'est pas valide, veuillez en saisir un autre"),'white','on_red'))
            action = get_user_move()
            if action != "m":
                play_move(partie['plateau'], action)
            else:   #Si on demande le menu on renvoie la partie au menu, pour y revenir en cas de poursuite de la partie; ou pour sauvegarder la partie
                os.system('cls')  #Cette fonction efface tout precedant affichage dans l'invite de commande linux, elle est legerement differente dans powershell
                return partie
            i += 1

        tiles = get_next_alea_tiles_coordonnees(partie['plateau'], partie['next_tile'] )    #On a donc effectue un mouvement valide, il nous faut maintenant les coordonnes de la tuile que l'on veut placer
        put_next_tiles(partie['plateau'], tiles)    #Pour pouvoir la placer
        partie['score'] = get_score(partie['plateau'])  #On actualise le score avec la nouvelle tuile

        partie['next_tile'] = get_next_alea_tiles_valeurs('encours', partie['plateau']) #Puis on actualise la prochaine tuile a venir
        if  partie['next_tile']['check'] == False:  #Cette condition regarde si la partie est en game over ou non
            os.system('cls')
            full_display(partie['plateau'])
            print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
            print(('Votre score: ') + str(partie['score'] ))
            return True #Si c'est le cas, elle retourne True
        os.system('cls')

def save_game(partie):
    import json
    """Sauvegarde une partie dans le fichier saved_game.json"""
    fichier = open("./life_cycle/saved_game.json", "w") #On ouvre ou cree le fichier de sauvegarde s'il n'existe pas
    json.dump(partie, fichier)  #Et on y met le dictionnaire partie
    fichier.close() #On referme le fichier
    print(colored(str("Partie sauvegardee !"),'white','on_green'))  #Puis on annonce que la partie a ete sauvegardee

def restore_game():
    import json
    """Restaure et retourne une partie sauvegardee dans le fichier "saved_game.json", ou retourne une nouvelle partie si aucune partie n'est sauvegardee"""
    if os.path.isfile("./life_cycle/saved_game.json") == False: #Pour restaurer, on regarde tout d'abord si le fichier de sauvegarde existe
        os.system('cls')
        print(colored(str("Aucune sauvegarde!"),'white','on_red'))  #Dans ce cas aucune partie existe, on renvoie donc une nouvelle partie
        print(colored(str("Nouvelle partie !"),'white','on_green') + "\n")
        partie = create_new_play()
    else:
        fichier = open("./life_cycle/saved_game.json", "r")
        partie = json.load(fichier) #Dans ce cas la partie existe, on charge donc les donnees de la partie dans partie
        fichier.close()
    return partie   #Puis l'on retourne la partie
