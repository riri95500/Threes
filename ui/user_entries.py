from termcolor import colored
import os

############################## Partie 3 ##############################

def get_user_move():
    """Saisi et retourne le coup joue par le joueur (en minuscule) parmis les choix:
    - 'h' pour haut,
    - 'b' pour bas,
    - 'g' pour gauche,
    - 'd' pour droite,
    - 'm' pour menu principal."""
    action = 'action'   #On initialise la variable action avec une valeur quelquonque qui verifie la boucle suivante pour rentrer dedans
    while action != 'h' and action != 'b' and action != 'g' and action != 'd' and action != 'm' :   #Cette boucle veriffie que le mouvement saisi est valide
        action = input('Que souhaitez-vous faire ? ')   #On recupere l'action
        action = action.lower() #Que l'on met en minuscule
    return action   #Et que l'on renvoie

def get_user_menu(partie):
    """Saisi et retourne le choix du joueur dans le menu principal
    :param partie: Partie de jeu ou None sinon
    :return choix de l'utilisateur (en majuscule)
    -'N' : Commencer une nouvelle partie,
    -'L' : Charger une partie,
    -'S' : Sauvegarder la partie en cours 'si le parametre partie correspond a une partie en cours
    -'C' : Reprendre la partie en cours (si le parametre partie correspond a une partie en cours)
    -'Q' : Terminer le jeu"""
    action = input()
    action = action.upper()
    while (action != 'N') and (action != 'L') and (action != 'S') and (action != 'C') and (action != 'Q') or (action == 'S' and partie == None) or (action == 'C' and partie == None):
        if (action == 'S' and partie == None) or (action == 'C' and partie == None):  #Si aucune partie existe, et qu'une action necessitant une partie est saisie on renvoit un message comme quoi il faute ffectuer une autre saisie
            print(colored(str("Action impossible, aucune partie en cours"),'white','on_red'))
            action = input(colored(str("Veuillez effectuer une autre saisie"),'white','on_red') + "\n") #On demande donc une nouvelle saisie
        else:   #Si seul le mouvement est incorect, on demande d'effectuer une saisie correcte
            action = input(colored(str("Veuillez effectuer une saisie correcte"),'white','on_red') + "\n")
        action = action.upper() #On met la nouvelle saisie en majuscule avant de renvoyer l'action
    return action
