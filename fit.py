# libraries import
# from pylab import *
import numpy as np
from scipy.optimize import curve_fit
import traceback
from functions import *
from functools import partial
# from scipy import numpy
# import matplotlib.pyplot as plt
# import sys


def regressions(liste_cord, dictionnaire={}):

    # creation des fonctions utilisees pour les differentes
    # creation d'un dictionnaire pour stocker les donnees essentielles
    myList = []
    # creation des listes des abscisses et ordonnees
    lx = []
    ly = []

    for coord in liste_cord:
        lx.append(coord[0])
        ly.append(coord[1])

    # creation des valeurs en abscisses et en ordonnee avec les listes lx et ly
    x = np.array(lx)
    y = np.array(ly)
    x=map(float,x)
    y=map(float,y)
    x_test = np.linspace(x[-1], x[-2])

    if y[-1] == 1:
        min = float(x[-2])
        max = float(x[-1])
    else:
        min = float(x[-1])
        max = float(x[-2])

    # creation of the fitted curves
    
    try:
       # exponential function
        funcexpParam = lambda x, b: funcexp2(x, b, min, max)
        # fonction regression utilisant la funcexp du fichier functions.py
        popt1, pcov1 = curve_fit(funcexpParam, x, y, [0.1])
        # popt1 = matrice ligne contenant les coefficients de la regression exponentielle optimisee apres calcul / popcov1 = matrice de covariances pour cette regression exp
        # ajout des coeeficients a, b et c dans le dictionnaire pour la regression
        # exponentielle
        b1 = popt1[0]
        a1 = (1. / (np.exp(-b1 * max) - np.exp(-b1 * min)))
        c1 = (1. / (1 - np.exp(b1 * (min - max))))
        # test de la fonction d'utilite qui doit etre comprise entre 0 et 1
        test = True
        for i in x_test:
            if funcexp(i, a1, b1, c1) < -0.02 or funcexp(i, a1, b1, c1) > 1.02:
                test = False
        if np.isnan(a1) or np.isnan(b1) or np.isnan(c1):
            test = False
			
        if test:
            dictionnaire['exp'] = {}
            dictionnaire['exp']['a'] = a1
            dictionnaire['exp']['b'] = b1
            dictionnaire['exp']['c'] = c1
            # calcul et affichage du mean squared error et du r2
            # print "Mean Squared Error exp : ", np.mean((y-funcexp(x,
            # *popt1))**2)
	    h=0
	    for k in range(len(y)-1):
		h+= (y[k] - funcexp(x[k], a1, b1, c1))**2
            ss_res = h
            ymean = np.mean(y)
            ss_tot = np.dot((y - ymean), (y - ymean))
            # ajout du r2 dans le dictionnaire pour la regression exponentielle
            dictionnaire['exp']['r2'] = 1 - ss_res / ss_tot
    except:
        pass

    try:
        # Meme principe pour la quadratic function
        funcquadParam = lambda x, b: funcquad2(x, b, min, max)
        popt2, pcov2 = curve_fit(funcquadParam, x, y, [0.1])
        b2 = popt2[0]
        a2 = b2 * min**2 - min * ((1 + b2 * (max**2 - min**2)) / (max - min))
        c2 = (1 + b2 * (max**2 - min**2)) / (max - min)
        test = True
        for i in x_test:
            if funcquad(i, a2, b2, c2) < -0.02 or funcquad(i, a2, b2, c2) > 1.02:
                test = False
        if np.isnan(a2) or np.isnan(b2) or np.isnan(c2):
            test = False
			
        if test:
            dictionnaire['quad'] = {}
            dictionnaire['quad']['a'] = a2
            dictionnaire['quad']['b'] = b2
            dictionnaire['quad']['c'] = c2
            # print "Mean Squared Error quad : ", np.mean((y-funcquad(x,
            # *popt2))**2)
            h=0
	    for k in range(len(y)-1):
		h+= (y[k] - funcquad(x[k], a2, b2, c2))**2
            ss_res = h
            ymean = np.mean(y)
            ss_tot = np.dot((y - ymean), (y - ymean))
            ymean = np.mean(y)
            ss_tot = np.dot((y - ymean), (y - ymean))
            dictionnaire['quad']['r2'] = 1 - ss_res / ss_tot
    except:
        pass

    try:
        # Meme principe pour la puissance function
        funcpuisParam = lambda x, b: funcpuis2(x, b, min, max)
        popt3, pcov3 = curve_fit(funcpuisParam, x, y, [0.1])
        b3 = popt3[0]
        a3 = (1 - b3) / (max**(1 - b3) - min**(1 - b3))
        c3 = -(min**(1 - b3) - 1) / (max**(1 - b3) - min**(1 - b3))
        test = True
        for i in x_test:
            if funcpuis(i, a3, b3, c3) < -0.02 or funcpuis(i, a3, b3, c3) > 1.02:
                test = False
        if np.isnan(a3) or np.isnan(b3) or np.isnan(c3):
            test = False
			
        if test:
            dictionnaire['pow'] = {}
            dictionnaire['pow']['a'] = a3
            dictionnaire['pow']['b'] = b3
            dictionnaire['pow']['c'] = c3
            # print "Mean Squared Error puis : ", np.mean((y-funcpuis(x,
            # *popt3))**2)
            h=0
	    for k in range(len(y)-1):
		h+= (y[k] - funcpuis(x[k], a3, b3, c3))**2
            ss_res = h
            ymean = np.mean(y)
            ss_tot = np.dot((y - ymean), (y - ymean))
            
            dictionnaire['pow']['r2'] = 1 - ss_res / ss_tot
    except:
        pass

    try:
        # Meme principe pour la logarithmic function
        funclogParam = lambda x, b, c: funclog2(x, b, c, min, max)
        popt4, pcov4 = curve_fit(funclogParam, x, y, [0.1, 0.1])
        b4 = popt4[0]
        c4 = popt4[1]
        a4 = 1. / (np.log(b4 * max + c4) - np.log(b4 * min + c4))
        d4 = 1. / (1 - np.log(b4 * max + c4) / np.log(b4 * min + c4))
        test = True
        for i in x_test:
            if funclog(i, a4, b4, c4, d4) < -0.02 or funclog(i, a4, b4, c4, d4) > 1.02:
                test = False
        if np.isnan(a4) or np.isnan(b4) or np.isnan(c4) or np.isnan(d4):
            test = False
		
        if test:
            dictionnaire['log'] = {}
            dictionnaire['log']['a'] = a4
            dictionnaire['log']['b'] = b4
            dictionnaire['log']['c'] = c4
            dictionnaire['log']['d'] = d4
            # print "Mean Squared Error log : ", np.mean((y-funclog(x,
            # *popt4))**2)
            h=0
	    for k in range(len(y)-1):
		h+= (y[k] - funclog(x[k], a4, b4, c4, d4))**2
            ss_res = h
            ymean = np.mean(y)
            ss_tot = np.dot((y - ymean), (y - ymean))
            dictionnaire['log']['r2'] = 1 - ss_res / ss_tot
    except:
        pass

    try:
        # Meme principe pour la linear function
        a5 = 1. / (max - min)
        b5 = -min / (max - min)
        dictionnaire['lin'] = {}
        dictionnaire['lin']['a'] = a5
        dictionnaire['lin']['b'] = b5
        # print "Mean Squared Error lin: ", np.mean((y-funclin(x, *popt5))**2)
        h=0
	for k in range(len(y)-1):
		h+= (y[k] - funclin(x[k], a5, b5))**2
        ss_res = h
        ymean = np.mean(y)
        ss_tot = np.dot((y - ymean), (y - ymean))
        dictionnaire['lin']['r2'] = 1 - ss_res / ss_tot
    except:
        pass

    try:
        # Meme principe pour la expo-power function
        funcexpopowerParam = lambda x, a: funcexpopower2(x, a, min, max)
        popt6, pcov6 = curve_fit(
            funcexpopowerParam, x, y, [-30])
        a6 = popt6[0]
        c6 = (np.log(np.log(1 - a6) / np.log(-a6))) / (np.log(max / min))
        b6 = -np.log(-a6) / (min**c6)
        test = True
        for i in x_test:
            if funcexpopower(i, a6, b6, c6) < -0.02 or funcexpopower(i, a6, b6, c6) > 1.02:
                test = False
        if np.isnan(a6) or np.isnan(b6) or np.isnan(c6):
            test = False
			
        if test:
            dictionnaire['expo-power'] = {}
            dictionnaire['expo-power']['a'] = a6
            dictionnaire['expo-power']['b'] = b6
            dictionnaire['expo-power']['c'] = c6
            h=0
	    for k in range(len(y)-1):
		h+= (y[k] - funcexpopower(x[k], a6, b6, c6))**2
            ss_res = h
            ymean = np.mean(y)
            ss_tot = np.dot((y - ymean), (y - ymean))
            dictionnaire['expo-power']['r2'] = 1 - ss_res / ss_tot
    except:
        pass
    return dictionnaire


def multipoints(liste_cord):
    if len(liste_cord) == 3:
        liste_dictionnaires = [{}]
        liste_dictionnaires[0]['points'] = [1]
        liste_dictionnaires[0]['coord'] = liste_cord
        liste_dictionnaires[0] = regressions(
            liste_dictionnaires[0]['coord'], dictionnaire=liste_dictionnaires[0])
    elif len(liste_cord) == 4:
        liste_dictionnaires = [{}, {}, {}]
        liste_dictionnaires[0]['points'] = [1, 2]
        liste_dictionnaires[0]['coord'] = liste_cord
        liste_dictionnaires[0] = regressions(
            liste_dictionnaires[0]['coord'], dictionnaire=liste_dictionnaires[0])
        liste_dictionnaires[1]['points'] = [1]
        liste_dictionnaires[1]['coord'] = [liste_cord[0]] + liste_cord[2:]
        liste_dictionnaires[1] = regressions(
            liste_dictionnaires[1]['coord'], dictionnaire=liste_dictionnaires[1])
        liste_dictionnaires[2]['points'] = [2]
        liste_dictionnaires[2]['coord'] = liste_cord[1:]
        liste_dictionnaires[2] = regressions(
            liste_dictionnaires[2]['coord'], dictionnaire=liste_dictionnaires[2])
    elif len(liste_cord) == 5:
        liste_dictionnaires = [{}, {}, {}, {}, {}, {}, {}]
        liste_dictionnaires[0]['points'] = [1, 2, 3]
        liste_dictionnaires[0]['coord'] = liste_cord
        liste_dictionnaires[0] = regressions(
            liste_dictionnaires[0]['coord'], dictionnaire=liste_dictionnaires[0])
        liste_dictionnaires[1]['points'] = [1, 2]
        liste_dictionnaires[1]['coord'] = liste_cord[:2] + liste_cord[3:]
        liste_dictionnaires[1] = regressions(
            liste_dictionnaires[1]['coord'], dictionnaire=liste_dictionnaires[1])
        liste_dictionnaires[2]['points'] = [1, 3]
        liste_dictionnaires[2]['coord'] = [liste_cord[0]] + liste_cord[2:]
        liste_dictionnaires[2] = regressions(
            liste_dictionnaires[2]['coord'], dictionnaire=liste_dictionnaires[2])
        liste_dictionnaires[3]['points'] = [2, 3]
        liste_dictionnaires[3]['coord'] = liste_cord[1:]
        liste_dictionnaires[3] = regressions(
            liste_dictionnaires[3]['coord'], dictionnaire=liste_dictionnaires[3])
        liste_dictionnaires[4]['points'] = [1]
        liste_dictionnaires[4]['coord'] = [liste_cord[0]] + liste_cord[3:]
        liste_dictionnaires[4] = regressions(
            liste_dictionnaires[4]['coord'], dictionnaire=liste_dictionnaires[4])
        liste_dictionnaires[5]['points'] = [2]
        liste_dictionnaires[5]['coord'] = [liste_cord[1]] + liste_cord[3:]
        liste_dictionnaires[5] = regressions(
            liste_dictionnaires[5]['coord'], dictionnaire=liste_dictionnaires[5])
        liste_dictionnaires[6]['points'] = [3]
        liste_dictionnaires[6]['coord'] = liste_cord[2:]
        liste_dictionnaires[6] = regressions(
            liste_dictionnaires[6]['coord'], dictionnaire=liste_dictionnaires[6])
    return {"data": liste_dictionnaires}


print regressions([[70,0.7],[80,0.8],[90,0.9],[50,0.0],[100,1.0]],False)
