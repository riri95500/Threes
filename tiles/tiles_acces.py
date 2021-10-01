############################## Partie 1 ##############################

def check_indice(plateau, indice):
    """Retourne 'True' si 'indice' correspond a un indice valide de case pour le plateau (entre 0 et n-1)"""
    return indice < plateau['n'] and indice >= 0

def check_room(plateau, lig, col):
    """Retourne 'True' si ('lig','col') sont les coordonnees d'une case du plateau ('lig' et 'col' sont des indices valides)"""
    return check_indice(plateau,lig) == True and check_indice(plateau, col) == True

def get_value(plateau, lig, col):
    """Retourne la valeur de la case ('lig','col'), et 'Erreur' si les coordonnees de la case ne sont pas valides"""
    if check_room(plateau, lig, col) == True:   #Verifie si les coordonnees de la case sont valides
        return plateau['tiles'][lig*plateau['n']+col]   #Renvoie la valeur de la case
    return "Erreur" #Renvoie 'Erreur'

def set_value(plateau, lig, col, val):
    """Affecte la valeur 'val' dans la case ('lig','col') du plateau, renvoie 'Erreur' si les coordonnees ne sont pas valides ou si 'val' n'est pas superieur ou egal a 0"""
    if get_value(plateau, lig, col) == 0 and val >= 0:  #Regarde si la case est vide et egalement que la valeur 'val' est supperieure ou egale a 0
        plateau['tiles'][lig*plateau['n']+col] = val    #Affecte la valeur 'val' aux coordonnees ('lig','col')
    elif get_value(plateau, lig, col) != "Erreur" and val >= 0 :    #Regarde si les coordonnees sont valides et egalement que la valeur 'val' est supperieure ou egale a 0
        plateau['tiles'][lig*plateau['n']+col] = val    #Affecte la valeur 'val' aux coordonnees ('lig','col')
    else:   #Ne correspond a aucun des cas de fonctionnement normaux, renvoie une erreur
        return "Erreur"
    plateau['nb_cases_libres'] = get_nb_empty_rooms(plateau) #Une nouvelle case a peut-etre ete afectee, il faut ajuster le nombre de cases libres
    return (plateau['tiles'][lig*plateau['n']+col])

def is_room_empty(plateau, lig, col):
    """Teste si une case du plateau est libre ou pas, renvoie 'True' si la case est libre, 'False' si elle ne l'est pas et enfin 'Erreur' si les coordonnees sont fausses"""
    if check_room(plateau, lig, col) == True:   #Verifie si les coordonnees ('lig','col') correspondent a une case
        return get_value(plateau, lig, col) == 0    #Renvoie True ou False
    return "Erreur" #Les coordonnees ne sont pas valides, le progamme renvoie une erreur

def get_nb_empty_rooms(plateau):
    """Met a jour le dictionnaire plateau avec le nombre de case(s) libre(s) du plateau et renvoie le nombre de case(s) libre(s)"""
    i=0
    nb_cases_libres = 0
    while i< len(plateau['tiles']): #On va verifier pour toutes les cases du plateau
        if plateau['tiles'][i] == 0:    #On verifie que la case est vide
            nb_cases_libres += 1    #Le nombre de cases libres augmente de 1
        i += 1
    plateau['nb_cases_libres'] = nb_cases_libres    #On met a jour le nombre de case(s) libre(s) du plateau
    return nb_cases_libres
