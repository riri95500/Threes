import sys
sys.path.append("./game/")
from play import *
sys.path.append("./tiles/")
from tiles_moves import *
from tiles_acces import *
sys.path.append("./life_cycle/")
from cycle_game import *
sys.path.append("./ui/")
from user_entries import *

def threes():
    """Permet d'enchainer les parties du jeu threes, de reprendre une partie sauvegardee et de sauvegarder une partie en cours"""
    os.system('cls')
    partie = None   #Quand on demarre le jeu on initialise la partie a rien car aucune partie est en cours
    while True:
        print(colored(str("~~~~~~~~~~ Menu Principal ~~~~~~~~~~").rjust(67),'grey','on_yellow') + colored(str(".").rjust(30),'yellow', 'on_yellow'))
        print(colored(str(" ").ljust(1),'grey','on_yellow') + "'N' : Commencer une nouvelle partie" + ("").rjust(60) + colored(str("").rjust(1),'grey','on_yellow'))
        print(colored(str(" ").ljust(1),'grey','on_yellow') + "'L' : Charger une partie" + ("").rjust(71) + colored(str("").rjust(1),'grey','on_yellow'))
        print(colored(str(" ").ljust(1),'grey','on_yellow') + "'S' : Sauvegarder la partie en cours (si le parametre partie correspond a une partie en cours)" + ("").rjust(1) + colored(str("").rjust(1),'grey','on_yellow'))
        print(colored(str(" ").ljust(1),'grey','on_yellow') + "'C' : Reprendre la partie en cours (si le parametre partie correspond a une partie en cours)" + ("").rjust(3) + colored(str("").rjust(1),'grey','on_yellow'))
        print(colored(str(" ").ljust(1),'grey','on_yellow') + "'Q' : Terminer le jeu" + ("").rjust(74) + colored(str("").rjust(1),'grey','on_yellow'))
        print(colored(str("~~~~~~~~~~ Que souhaitez-vous faire? ~~~~~~~~~~").rjust(72),'grey', 'on_yellow') + colored(str(".").rjust(25),'yellow', 'on_yellow'))
        #Toutes les print ci-dessus servent a afficher un menu agreable a lire
        action = get_user_menu(partie)  #on recupere donc le prochain mouvement
        if action =="N":    #Puis on effectue le tri en fonction de l'action effectuee
            os.system('cls')
            partie = cycle_play(create_new_play())  #Dans ce cas on cree une nouvelle partie
        elif action == "L":
            os.system('cls')
            partie = cycle_play(restore_game()) #Ici on recharge une partie enregistree
        elif action == "S":
            os.system('cls')
            if partie == None:  #On verifie qu'une partie est bien en cours pour sauvegarder
                get_user_menu(partie)
            save_game(partie)   #Ici on sauvegarde
        elif action == "C":
            os.system('cls')
            partie = cycle_play(partie) #Ici on renvoie la partie en cours, si elle existe bien
        elif action == "Q":
            return  #Et ici on quitte le jeu
        if partie == True:  #Si la fonction cycle_play renvoie True, c'est que la partie est terminee il y a donc game over
            print("Game Over")
            partie = None   #On reinitialise donc la partie

threes()
