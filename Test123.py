def CE(valeurmin, valeurmax, gain, choix, mode):
    if mode == 'Reversed':
        print("On est bien reverse")
        choix = (choix + 1) % 2
    liste = [valeurmin, valeurmax]
    # choix = 1 correspond a l equivalent certain (comme pour la PE)
    if choix == 1:
        print("On a choisi 1 finalement")
        valeurmax = gain
        gain = round(valeurmin + ((valeurmax - valeurmin) / 4), 0)
        liste = [valeurmin, valeurmax]
        return ({"interval": liste, "gain": gain})

    else:
        print("On a choisi 0 finalement")
        valeurmin = gain
        gain = round(valeurmax - ((valeurmax - valeurmin) / 4), 0)
        liste = [valeurmin, valeurmax]
        return ({"interval": liste, "gain": gain})

vmin = 3
vmax = 10
gain = 8
c=0
mode = "Reversed"

print(CE(vmin,vmax,gain,c,mode))
