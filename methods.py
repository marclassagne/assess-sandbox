def PE_old(p, c):
    # p -> proba
    # c -> choix  0= choix sur 1= choix lotterie

    if c == 0:
        return p + (1 - p) / 4
    else:
        return p / 4

##############Programme PE################################################


def PE(min_interval, max_interval, p, choix, mode):
    #min_interval=0; p=0.75; max_interval=1

    if mode == 'reversed':
        choix = (choix + 1) % 2
    liste = [min_interval, max_interval]
    if choix == 1:
        max_interval = p  # la borne max est remplacee par la nouvelle valeur
        p = round(p / 4, 2)  # au premier abord, on divise p par 4
        if p < min_interval:
            p = round(min_interval + (max_interval - min_interval) / 4, 2)
        # pas la peine de renvoyer la valeur de p car max_interval=p
        liste = [min_interval, max_interval]
        return({"interval": liste, "proba": p})
    else:
        min_interval = p
        p = round(max_interval - (max_interval - min_interval) / 4, 2)
        liste = [min_interval, max_interval]
        return({"interval": liste, "proba": p})

###################Programme LE###########################################


# sachant que p1 va etre egale soit a 0.38 soit a 0.13
def LE(min_interval, max_interval, p, choix, mode):
    #min_interval= 0; p = 0.47; max_interval = 0.5;
    if mode == 'Reversed':
        choix = (choix + 1) % 2
    liste = [min_interval, max_interval]  # p = probabilite qui s affiche
    # choix = 0 correspond a la lotterie de gauche (celle dont la probabilite
    # change)
    if choix == 0:
        max_interval = p
        p = round(p / 4, 2)
        if min_interval > p:
            p = round(min_interval + (max_interval - min_interval) / 4, 2)
        liste = [min_interval, max_interval]
        return({"interval": liste, "proba": p})
    # choix = 1 correspond a la lotterie de droite (celle qui ne change pas)
    else:
        min_interval = p
        p = round(max_interval - (max_interval - p) / 4, 2)
        liste = [min_interval, max_interval]
        return({"interval": liste, "proba": p})

# pour ensuite les deux autres questionnaires il suffit de modifier la
# valeur max de la lotterie de droite (celle qui ne change pas) si au
# debut les bornes sont de [0,50], elles sont ensuite de [0,25] puis de
# [0,75]

#################Programme CE probabilite constante#######################

# from random import *
# L = [0.75*(valeurmax-valeurmin)+valeurmin, 0.25*(valeurmax-valeurmin)+valeurmin]
# gain = choice(L)


def CE(valeurmin, valeurmax, gain, choix, mode):
    if mode == 'Reversed':
        choix = (choix + 1) % 2
    liste = [valeurmin, valeurmax]
    # choix = 1 correspond a l equivalent certain (comme pour la PE)
    if choix == 1:
        valeurmax = gain
        gain = round(valeurmin + ((valeurmax - valeurmin) / 4), 0)
        liste = [valeurmin, valeurmax]
        return ({"interval": liste, "gain": gain})

    else:
        valeurmin = gain
        gain = round(valeurmax - ((valeurmax - valeurmin) / 4), 0)
        liste = [valeurmin, valeurmax]
        return ({"interval": liste, "gain": gain})

# pour les deux autres questionnaires, il suffit de recuperer la valeur du
# gain (que je note gain1) en fin de questionnaire 1 et le nouvel
# intervalle est alors: [valeurmin,gain1]. Pour le 3eme questionnaire l
# intervalle est [gain1,valeurmin]

###################Programme CE probabilite variable######################


def CEPV(valeurmin, valeurmax, gain, p, choix, mode):
    if mode == 'reversed':
        choix = (choix + 1) % 2
    Liste = [valeurmin, valeurmax]
    # choix = 1 correspond a l equivalent certain (comme pour la PE)
    if choix == 1:
        valeurmax = gain
        gain = round(valeurmin + ((valeurmax - valeurmin) / 4), 0)
        liste = [valeurmin, valeurmax]
        return ({"interval": liste, "gain": gain})

    else:
        valeurmin = gain
        gain = round(valeurmax - ((valeurmax - valeurmin) / 4), 0)
        liste = [valeurmin, valeurmax]
        return ({"interval": liste, "gain": gain})

# pour les differents questionnaires seule la probabilite de la lotterie va changer: elle passe de 0.5 a 0.25 puis 0.75
# le code est exactement le meme
