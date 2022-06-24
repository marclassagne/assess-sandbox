# -*- coding: utf-8 -*-

import numpy as np
import json
import sys
import fit
import random
import math
from functions import *

import xlsxwriter
from xlsxwriter.utility import xl_rowcol_to_cell

compteur=0


def formatGenerate(decimal):
#Function qui rend une chaîne de caractère de 0.00 avec le nombre de décimal
#correspondant à l'argument decimal (entier)
    s = '0.'
    for i in range(int(decimal)):
        s += '0'
    return s

def generate_fichier(data):
    global compteur
    print()
    print()
    print()
    print()
    compteur+=1
    
    print("00000000000000000000000")
    print("data",data)
    print("dataend")
    print("00000000000000000000000")

    # On crée un "classeur"

    #r = random.randint(1, 1000)
    classeur = xlsxwriter.Workbook('fichier'+str(compteur)+'.xlsx')
    # On ajoute une feuille au classeur

    decimal = data['settings']['decimals_equations']
    formatZero = formatGenerate(decimal)

    for monAttribut in data['attributes']:

        feuille = classeur.add_worksheet(monAttribut['name'])

        format01 = classeur.add_format()
        format01.set_num_format('0.00')

        formatCoeff = classeur.add_format()
        formatCoeff.set_num_format(formatZero)

        formatTitre = classeur.add_format()
        formatTitre.set_bg_color('#C0C0C0')
        formatTitre.set_bold()

        formatNom = classeur.add_format()
        formatNom.set_font_color('#D95152')
        formatNom.set_align('center')
        formatNom.set_bold()
        # ici on va mettre toutes les infos sur l'attribut

        feuille.write(0, 0, 'Attribute', formatTitre)
        feuille.write(0, 1, '', formatTitre)
        feuille.write(0, 3, '', formatTitre)
        feuille.write(0, 4,"Modality",formatTitre)
        feuille.write(0, 5,"Utility value",formatTitre)
        
    
        
        feuille.write(1, 0, 'Name', formatNom)
        feuille.write(2, 0, 'Type', formatNom)
        feuille.write(3, 0, 'Unit', formatNom)
        feuille.write(4, 0, 'Method', formatNom)
        feuille.write(5, 0, 'Mode', formatNom)
        feuille.write(6, 0, 'Active', formatNom)
        feuille.write(7, 0, 'Completed', formatNom)

        feuille.write(1, 1, monAttribut['name'])
        feuille.write(2, 1, monAttribut['type'])
        feuille.write(3, 1, monAttribut['unit'])
        feuille.write(4, 1, monAttribut['method'])
        feuille.write(5, 1, monAttribut['mode'])
        feuille.write(6, 1, monAttribut['checked'])
        feuille.write(7, 1, monAttribut['completed'])
        
        nb_intermediary = len(monAttribut['val_med'])
        
        
        dic_points = monAttribut['questionnaire']['points']
        dic_points[monAttribut['val_min']] = int(monAttribut['mode']!='Normal')
        dic_points[monAttribut['val_max']] = int(monAttribut['mode']=='Normal')

        feuille.write(1, 3, 'Val_min', formatNom)
        feuille.write(1,4, monAttribut['val_min'])
        feuille.write(1,5, dic_points[monAttribut['val_min']])

        
        for i in range(nb_intermediary):
            feuille.write(i+2,3,'Intermediary value ' + str(i+1), formatNom)
            print("monAttribut['val_med'][i]",monAttribut['val_med'][i])
            feuille.write(i+2,4,monAttribut['val_med'][i])
            print("dic_points",dic_points)
          
                
            #print("dic_points[monAttribut['val_med'][i]]",dic_points[monAttribut['val_med'][i]])
            #feuille.write(i+2,5,dic_points[monAttribut['val_med'][i]])
            
        
        feuille.write(nb_intermediary+2,3,'Val_max', formatNom)
        feuille.write(nb_intermediary+2, 4, monAttribut['val_max'])
        feuille.write(nb_intermediary+2, 5, dic_points[monAttribut['val_max']])

        
        # Ensuite on s'occupe de la fonction d'utilité
        # on fait une regression à l'aide des points que l'on a dans le
        # questionnaire et on envoit tout ça dans la fonction regressions du
        # fichier fit.py
        utilities = {}
        
        if monAttribut['type'] == 'Quantitative' :
        
            pointsY = monAttribut['questionnaire']['points'].values()
            pointsX = monAttribut['questionnaire']['points'].keys()
            pointsX = map(float,pointsX)
            print([np.stack((pointsX,pointsY), axis = 0)])
            points = np.stack((pointsX,pointsY), axis = 0).tolist()

            if len(points) > 0:
                if monAttribut['mode'] == "Normal":
                    points.append([monAttribut['val_max'], 1])
                    points.append([monAttribut['val_min'], 0])
                else:
                    points.append([monAttribut['val_max'], 0])
                    points.append([monAttribut['val_min'], 1])

                # go for fit regression using our points
            
                utilities = fit.regressions(points)
                      
        
        

            
        ligne = 0

        for utility in utilities.keys():

            feuille.write(ligne, 8, '', formatTitre)
            
            #Affichage des noms de ligne de chaque régression
            liste_des_noms_de_ligne=['Utility Function',"type","a","b","c","d","r2","DPL"]
            Liste_des_formats=[formatTitre]+7*[formatNom]
            
            for k in range(len(liste_des_noms_de_ligne)):
                feuille.write(ligne + k, 7, liste_des_noms_de_ligne[k], Liste_des_formats[k])
                
                
            # feuille.write(ligne, 7, 'Utility Function', formatTitre)
            # feuille.write(ligne + 1, 7, "type", formatNom)
            # feuille.write(ligne + 2, 7, "a", formatNom)
            # feuille.write(ligne + 3, 7, "b", formatNom)
            # feuille.write(ligne + 4, 7, "c", formatNom)
            # feuille.write(ligne + 5, 7, "d", formatNom)
            # feuille.write(ligne + 6, 7, "r2", formatNom)
            # feuille.write(ligne + 7, 7, "DPL", formatNom)

            if utility == 'exp':
                feuille.write(ligne + 1, 8, "exponential")
            elif utility == 'quad':
                feuille.write(ligne + 1, 8, "quadratic")
            elif utility == 'pow':
                feuille.write(ligne + 1, 8, "power")
            elif utility == 'log':
                feuille.write(ligne + 1, 8, "logarithm")
            elif utility == 'lin':
                feuille.write(ligne + 1, 8, "linear")
            elif utility == 'expo-power':
                feuille.write(ligne + 1, 8, "expo-power")

            parameters=utilities[utility]

            # On rempli les coefficients
            try:
                # On remplit d'abord le dernier car pour les coefficients d ça
                # s'arretera
                
                feuille.write(ligne + 6, 8, parameters['r2'], formatCoeff)
                
                feuille.write(ligne + 7, 8, convert_to_text(utility, parameters, monAttribut['name'], int(data['settings']['decimals_equations'])), formatCoeff)
                
                feuille.write(ligne + 2, 8, parameters['a'], formatCoeff)
                feuille.write(ligne + 3, 8, parameters['b'], formatCoeff)
                feuille.write(ligne + 4, 8, parameters['c'], formatCoeff)
                print("parameters['c']",parameters['c'])
                print("----------------------------")
                feuille.write(ligne + 5, 8, parameters['d'], formatCoeff)

            except:
                print(sys.exc_info())
                pass

            feuille.set_column(5, 5, 20)

            feuille.write(ligne + 0, 9, 'Calculated points', formatTitre)
            feuille.write(ligne + 0, 10, '', formatTitre)
            # On va maintenant generer plusieurs points
            amplitude = (monAttribut['val_max'] -
                        monAttribut['val_min']) / 10.0
            for i in range(0, 11):
                feuille.write(ligne + 1 + i, 9, monAttribut['val_min'] + i * amplitude)
                if utility == 'exp':
                    feuille.write_formula(ligne + 1 + i, 10, funcexp_excel("J" + str(
                        ligne + 2 + i), "$I$" + str(ligne + 3), "$I$" + str(ligne + 4), "$I$" + str(ligne + 5)))
                elif utility == 'quad':
                    feuille.write_formula(ligne + 1 + i, 10, funcquad_excel("J" + str(
                        ligne + 2 + i), "$I$" + str(ligne + 3), "$I$" + str(ligne + 4), "$I$" + str(ligne + 5)))
                elif utility == 'pow':
                    feuille.write_formula(ligne + 1 + i, 10, funcpuis_excel("J" + str(
                        ligne + 2 + i), "$I$" + str(ligne + 3), "$I$" + str(ligne + 4), "$I$" + str(ligne + 5)))
                elif utility == 'log':
                    feuille.write_formula(ligne + 1 + i, 10, funclog_excel("J" + str(ligne + 2 + i), "$I$" + str(
                        ligne + 3), "$I$" + str(ligne + 4), "$I$" + str(ligne + 5), "$I$" + str(ligne + 6)))
                elif utility == 'lin':
                    feuille.write_formula(ligne + 1 + i, 10, funclin_excel(
                        "J" + str(ligne + 2 + i), "$I$" + str(ligne + 3), "$I$" + str(ligne + 4)))
                elif utility == 'expo-power':
                    feuille.write_formula(ligne + 1 + i, 10, funcexpopower_excel("J" + str(
                        ligne + 2 + i), "$I$" + str(ligne + 3), "$I$" + str(ligne + 4), "$I$" + str(ligne + 5)))

            # Ensuite on fait le Chart ! (le diagramme)
            chart5 = classeur.add_chart({'type': 'scatter',
                                        'subtype': 'smooth'})

            # Configure the first series.
            chart5.add_series({
                            'name':       utility,
                            'categories': '=\'' + monAttribut['name'] + '\'' + '!$J$' + str(ligne + 2) + ':$J$' + str(ligne + 12),
                            'values':     '=\'' + monAttribut['name'] + '\'' + '!$K$' + str(ligne + 2) + ':$K$' + str(ligne + 12),

                            })

            # Add a chart title and some axis labels.
            chart5.set_title({'name': 'Utility Function'})

            # Set an Excel chart style.
            chart5.set_style(4)
            chart5.set_x_axis({
                'min': monAttribut['val_min'],
                'max': monAttribut['val_max']
            })

            # Insert the chart into the worksheet (with an offset).
            feuille.insert_chart('L' + str(1 + ligne),
                                chart5, {'x_offset': 35, 'y_offset': 10})

            ligne += 15

    for mesK in data['k_calculus']:
        feuille = classeur.add_worksheet("Multi attribute " + mesK['method'])

        formatTitre = classeur.add_format()
        formatTitre.set_bg_color('#C0C0C0')
        formatTitre.set_align('center')
        formatTitre.set_bold()

        formatNom = classeur.add_format()
        formatNom.set_font_color('#D95152')
        formatNom.set_align('center')
        formatNom.set_font_size(12)
        formatNom.set_bold()
        # ici on va mettre toutes les infos sur l'attribut

        feuille.write(0, 0, 'K', formatTitre)
        feuille.set_column(0, 0, 10)
        feuille.write(0, 1, 'Value', formatTitre)
        feuille.write(0, 2, 'Attribute', formatTitre)
        feuille.set_column(2, 2, 30)
        feuille.write(0, 3, 'IDAttribute', formatTitre)
        feuille.set_column(3, 3, 10)
        feuille.write(0, 4, 'utility type', formatTitre)
        feuille.set_column(4, 4, 15)

        ligne = 1
        for monK in mesK['k']:
            feuille.write(ligne, 0, monK['ID'], formatNom)
            feuille.write(ligne, 1, monK['value'])
            feuille.write(ligne, 2, json.dumps(monK['attribute']))
            feuille.write(ligne, 3, json.dumps(monK['ID_attribute']))
            ligne = ligne + 1

        if mesK['method'] == "multiplicative":
            feuille.write(ligne, 0, "K", formatNom)
            feuille.write(ligne, 1, mesK['GK'])
        else:
            feuille.write(ligne, 0, " ", formatNom)
            feuille.write(ligne, 1, mesK['GK'])

        ligne = ligne + 3
        if mesK['GU'] != None:
            feuille.write(ligne, 0, 'DPL', formatNom)
            feuille.write(ligne, 1, mesK['GU']['U'])

            ligne = 0

            utilities = mesK['GU']['utilities']
            numberUtilities = len(utilities)
            k = mesK['GU']['k']

            numero = 1
            for myUtility in utilities:

                feuille.write(numero, 4, myUtility['type'])

                feuille.write(ligne, 4 + numero, "x" +
                              str(numero), formatTitre)
                feuille.write(ligne + 1, 4 + numero, 1)

                feuille.write(ligne, 4 + numero + numberUtilities, "u" +
                              str(numero) + "(x" + str(numero) + ")", formatTitre)
                if myUtility['type'] == 'exp':
                    feuille.write_formula(ligne + 1, 4 + numero + numberUtilities, funcexp_excel(xl_rowcol_to_cell(
                        ligne + 1, 4 + numero), str(myUtility['a']), str(myUtility['b']), str(myUtility['c'])))
                elif myUtility['type'] == 'quad':
                    feuille.write_formula(ligne + 1, 4 + numero + numberUtilities, funcquad_excel(xl_rowcol_to_cell(
                        ligne + 1, 4 + numero), str(myUtility['a']), str(myUtility['b']), str(myUtility['c'])))
                elif myUtility['type'] == 'pow':
                    feuille.write_formula(ligne + 1, 4 + numero + numberUtilities, funcpuis_excel(xl_rowcol_to_cell(
                        ligne + 1, 4 + numero), str(myUtility['a']), str(myUtility['b']), str(myUtility['c'])))
                elif myUtility['type'] == 'log':
                    feuille.write_formula(ligne + 1, 4 + numero + numberUtilities, funclog_excel(xl_rowcol_to_cell(
                        ligne + 1, 4 + numero), str(myUtility['a']), str(myUtility['b']), str(myUtility['c']), str(myUtility['d'])))
                elif myUtility['type'] == 'lin':
                    feuille.write_formula(ligne + 1, 4 + numero + numberUtilities, funclin_excel(
                        xl_rowcol_to_cell(ligne + 1, 4 + numero), str(myUtility['a']), str(myUtility['b'])))
                elif myUtility['type'] == 'expo-power':
                    feuille.write_formula(ligne + 1, 4 + numero + numberUtilities, funcexpopower_excel(xl_rowcol_to_cell(
                        ligne + 1, 4 + numero), str(myUtility['a']), str(myUtility['b']), str(myUtility['c'])))

                numero = numero + 1

            feuille.write(ligne, 4 + numero +
                          numberUtilities, "U", formatTitre)

            def K(i):
                return xl_rowcol_to_cell(i, 1, row_abs=True, col_abs=True)

            def U(i):
                return xl_rowcol_to_cell(ligne + 1, 4 + i + numberUtilities)

            if mesK['method'] == "multiplicative":
                if numberUtilities == 2:
                    GU = utilite2_excel(K(1), K(2), K(3), U(1), U(2))
                    feuille.write_formula(
                        ligne + 1, 4 + numero + numberUtilities, GU)
                if numberUtilities == 3:
                    # in reality K(4) is K
                    GU = utilite3_excel(K(1), K(2), K(
                        3), K(4), U(1), U(2), U(3))
                    feuille.write_formula(
                        ligne + 1, 4 + numero + numberUtilities, GU)
                if numberUtilities == 4:
                    GU = utilite4_excel(K(1), K(2), K(3), K(
                        4), K(5), U(1), U(2), U(3), U(4))
                    feuille.write_formula(
                        ligne + 1, 4 + numero + numberUtilities, GU)
                if numberUtilities == 5:
                    GU = utilite5_excel(K(1), K(2), K(3), K(4), K(
                        5), K(6), U(1), U(2), U(3), U(4), U(5))
                    feuille.write_formula(
                        ligne + 1, 4 + numero + numberUtilities, GU)
                if numberUtilities == 6:
                    GU = utilite6_excel(K(1), K(2), K(3), K(4), K(5), K(
                        6), K(7), U(1), U(2), U(3), U(4), U(5), U(6))
                    feuille.write_formula(
                        ligne + 1, 4 + numero + numberUtilities, GU)

            else:
                nombre = 1
                GU = ""
                for monK in k:
                    GU += K(nombre)
                    for dk in monK['ID'].split(','):
                        GU += "*" + U(int(dk))
                    GU += "+"
                    nombre = nombre + 1

                GU = GU[:-1]
                feuille.write_formula(
                    ligne + 1, 4 + numero + numberUtilities, GU)

    # Ecriture du classeur sur le disque
    classeur.close()

    # On retourne le nom du fichier
    return 'fichier'+str(compteur)

# generate juste the file with utility function we checked


def generate_fichier_with_specification(data):
    global compteur
    compteur+=1
    #r = random.randint(1, 1000)
    classeur = xlsxwriter.Workbook('fichier'+str(compteur)+'.xlsx')
    # On ajoute une feuille au classeur

    for monAttribut in data['attributes']:
        # we first check if the attribute have a list o defined utility
        # function

        feuille = classeur.add_worksheet(monAttribut['name'])

        format01 = classeur.add_format()
        format01.set_num_format('0.00')

        formatCoeff = classeur.add_format()
        formatCoeff.set_num_format('0.000000')

        formatTitre = classeur.add_format()
        formatTitre.set_bg_color('#C0C0C0')
        formatTitre.set_bold()

        formatNom = classeur.add_format()
        formatNom.set_font_color('#D95152')
        formatNom.set_align('center')
        formatNom.set_bold()
        # ici on va mettre toutes les infos sur l'attribut

        # feuille.merge_range('A1:B1','Attribut')
        feuille.write(0, 0, 'Attribute', formatTitre)
        feuille.write(0, 1, '', formatTitre)
        feuille.write(0, 3, '', formatTitre)
        feuille.write(0, 4,"Modality",formatTitre)
        feuille.write(0, 5,"Utility value",formatTitre)
        
    
        
        feuille.write(1, 0, 'Name', formatNom)
        feuille.write(2, 0, 'Type', formatNom)
        feuille.write(3, 0, 'Unit', formatNom)
        feuille.write(4, 0, 'Method', formatNom)
        feuille.write(5, 0, 'Mode', formatNom)
        feuille.write(6, 0, 'Active', formatNom)
        feuille.write(7, 0, 'Completed', formatNom)

        feuille.write(1, 1, monAttribut['name'])
        feuille.write(2, 1, monAttribut['type'])
        feuille.write(3, 1, monAttribut['unit'])
        feuille.write(4, 1, monAttribut['method'])
        feuille.write(5, 1, monAttribut['mode'])
        feuille.write(6, 1, monAttribut['checked'])
        feuille.write(7, 1, monAttribut['completed'])
        
        nb_intermediary = len(monAttribut['val_med'])
        
        
        dic_points = monAttribut['questionnaire']['points']
        dic_points[monAttribut['val_min']] = int(monAttribut['mode']!='Normal')
        dic_points[monAttribut['val_max']] = int(monAttribut['mode']=='Normal')

        feuille.write(1, 3, 'Val_min', formatNom)
        feuille.write(1,4, monAttribut['val_min'])
        feuille.write(1,5, dic_points[monAttribut['val_min']])

        
        for i in range(nb_intermediary):
            feuille.write(i+2,3,'Intermediary value ' + str(i+1), formatNom)
            feuille.write(i+2,4,monAttribut['val_med'][i])
            feuille.write(i+2,5,dic_points[monAttribut['val_med'][i]])
        
        feuille.write(nb_intermediary+2,3,'Val_max', formatNom)
        feuille.write(nb_intermediary+2, 4, monAttribut['val_max'])
        feuille.write(nb_intermediary+2, 5, dic_points[monAttribut['val_max']])
        # Ensuite on s'occupe de la fonction d'utilité
        #feuille.merge_range('E1:F1','Utility Function')
        # on fait une regression à l'aide des points que l'on a dans le
        # questionnaire et on envoit tout ça dans la fonction regressions du
        # fichier fit.py
        utilities = monAttribut['utilities']

        ligne = 0

        for utility in utilities:

            feuille.write(ligne, 7, 'Utility Function', formatTitre)
            feuille.write(ligne, 5, '', formatTitre)
            feuille.write(ligne + 1, 7, "type", formatNom)
            feuille.write(ligne + 2, 7, "a", formatNom)
            feuille.write(ligne + 3, 7, "b", formatNom)
            feuille.write(ligne + 4, 7, "c", formatNom)
            feuille.write(ligne + 5, 7, "d", formatNom)
            feuille.write(ligne + 6, 7, "r2", formatNom)
            feuille.write(ligne + 7, 7, "DPL", formatNom)

            # Dans le cas ou la fonciton d'utilité est de type exp
            # on cherche quel est notre type de fonction d'utilite

            if utility['type'] == 'exp':
                feuille.write(ligne + 1, 8, "exponential")
            if utility['type'] == 'quad':
                feuille.write(ligne + 1, 8, "quadratic")
            if utility['type'] == 'pow':
                feuille.write(ligne + 1, 8, "power")
            if utility['type'] == 'log':
                feuille.write(ligne + 1, 8, "logarithm")
            if utility['type'] == 'lin':
                feuille.write(ligne + 1, 8, "linear")
            if utility['type'] == 'expo-power':
                feuille.write(ligne + 1, 8, "expo-power")


            # On rempli les coefficients
            try:
                # On remplit d'abord le dernier car pour les coefficients d ça
                # s'arretera
                feuille.write(ligne + 6, 8, utility['r2'], formatCoeff)
                feuille.write(
                    ligne + 7, 8, convert_to_text(utility['type'], utility, "x"), formatCoeff)
                feuille.write(ligne + 2, 8, utility['a'], formatCoeff)
                feuille.write(ligne + 3, 8, utility['b'], formatCoeff)
                feuille.write(ligne + 4, 8, utility['c'], formatCoeff)
                feuille.write(ligne + 5, 8, utility['d'], formatCoeff)
            except:
                pass

            feuille.set_column(5, 5, 20)

            feuille.write(ligne + 0, 9, 'Calculated points', formatTitre)
            feuille.write(ligne + 0, 10, '', formatTitre)
            # On va maintenant generer plusieurs points
            amplitude = (monAttribut['val_max'] -
                         monAttribut['val_min']) / 10.0
            for i in range(0, 11):
                feuille.write(ligne + 1 + i, 9, i * amplitude)
                if utility['type'] == 'exp':
                    feuille.write_formula(ligne + 1 + i, 10, funcexp_excel("J" + str(
                        ligne + 2 + i), "$I$" + str(ligne + 3), "$I$" + str(ligne + 4), "$I$" + str(ligne + 5)))
                elif utility['type'] == 'quad':
                    feuille.write_formula(ligne + 1 + i, 10, funcquad_excel("J" + str(
                        ligne + 2 + i), "$I$" + str(ligne + 3), "$I$" + str(ligne + 4), "$I$" + str(ligne + 5)))
                elif utility['type'] == 'pow':
                    feuille.write_formula(ligne + 1 + i, 10, funcpuis_excel("J" + str(
                        ligne + 2 + i), "$I$" + str(ligne + 3), "$I$" + str(ligne + 4), "$I$" + str(ligne + 5)))
                elif utility['type'] == 'log':
                    feuille.write_formula(ligne + 1 + i, 10, funclog_excel("J" + str(ligne + 2 + i), "$I$" + str(
                        ligne + 3), "$I$" + str(ligne + 4), "$I$" + str(ligne + 5), "$I$" + str(ligne + 6)))
                elif utility['type'] == 'lin':
                    feuille.write_formula(ligne + 1 + i, 10, funclin_excel(
                        "J" + str(ligne + 2 + i), "$I$" + str(ligne + 3), "$I$" + str(ligne + 4)))
                elif utility['type'] == 'expo-power':
                    feuille.write_formula(ligne + 1 + i, 10, funcexpopower_excel("J" + str(
                        ligne + 2 + i), "$I$" + str(ligne + 3), "$I$" + str(ligne + 4), "$I$" + str(ligne + 5)))

            # Ensuite on fait le Chart ! (le diagramme)
            chart5 = classeur.add_chart({'type': 'scatter',
                                         'subtype': 'smooth'})

            # Configure the first series.
            chart5.add_series({
                              'name':       utility['type'],
                              'categories': '=' + monAttribut['name'] + '!$J$' + str(ligne + 2) + ':$J$' + str(ligne + 12),
                              'values':     '=' + monAttribut['name'] + '!$K$' + str(ligne + 2) + ':$K$' + str(ligne + 12),

                              })

            # Add a chart title and some axis labels.
            chart5.set_title({'name': 'Utility Function'})

            # Set an Excel chart style.
            chart5.set_style(4)
            chart5.set_x_axis({
                'min': monAttribut['val_min'],
                'max': monAttribut['val_max']
            })

            # Insert the chart into the worksheet (with an offset).
            feuille.insert_chart('L' + str(1 + ligne),
                                 chart5, {'x_offset': 35, 'y_offset': 10})

            ligne += 15

    for mesK in data['k_calculus']:
        feuille = classeur.add_worksheet("Multi attribute " + mesK['method'])

        formatTitre = classeur.add_format()
        formatTitre.set_bg_color('#C0C0C0')
        formatTitre.set_bold()

        formatNom = classeur.add_format()
        formatNom.set_font_color('#D95152')
        formatNom.set_align('center')
        formatNom.set_font_size(12)
        formatNom.set_bold()
        # ici on va mettre toutes les infos sur l'attribut

        feuille.write(0, 0, 'K', formatTitre)
        feuille.set_column(0, 0, 15)
        feuille.write(0, 1, 'Value', formatTitre)
        feuille.write(0, 2, 'Attribute', formatTitre)
        feuille.set_column(2, 2, 50)
        feuille.write(0, 3, 'IDAttribute', formatTitre)
        feuille.set_column(3, 3, 15)
        feuille.write(0, 4, 'utility type', formatTitre)
        feuille.set_column(4, 4, 15)

        ligne = 1
        for monK in mesK['k']:
            feuille.write(ligne, 0, monK['ID'], formatNom)
            feuille.write(ligne, 1, monK['value'])
            feuille.write(ligne, 2, json.dumps(monK['attribute']))
            feuille.write(ligne, 3, json.dumps(monK['ID_attribute']))
            ligne = ligne + 1

        if mesK['method'] == "multiplicative":
            feuille.write(ligne, 0, "K", formatNom)
            feuille.write(ligne, 1, mesK['GK'])
        else:
            feuille.write(ligne, 0, " ", formatNom)
            feuille.write(ligne, 1, mesK['GK'])

        ligne = ligne + 3
        if mesK['GU'] != None:
            feuille.write(ligne, 0, 'DPL', formatNom)
            feuille.write(ligne, 1, mesK['GU']['U'])

            ligne = 0

            utilities = mesK['GU']['utilities']
            numberUtilities = len(utilities)
            k = mesK['GU']['k']

            numero = 1
            for myUtility in utilities:

                feuille.write(numero, 4, myUtility['type'])

                feuille.write(ligne, 4 + numero, "x" +
                              str(numero), formatTitre)
                feuille.write(ligne + 1, 4 + numero, 1)

                feuille.write(ligne, 4 + numero + numberUtilities, "u" +
                              str(numero) + "(x" + str(numero) + ")", formatTitre)
                if myUtility['type'] == 'exp':
                    feuille.write_formula(ligne + 1, 4 + numero + numberUtilities, funcexp_excel(xl_rowcol_to_cell(
                        ligne + 1, 4 + numero), str(myUtility['a']), str(myUtility['b']), str(myUtility['c'])))
                elif myUtility['type'] == 'quad':
                    feuille.write_formula(ligne + 1, 4 + numero + numberUtilities, funcquad_excel(xl_rowcol_to_cell(
                        ligne + 1, 4 + numero), str(myUtility['a']), str(myUtility['b']), str(myUtility['c'])))
                elif myUtility['type'] == 'pow':
                    feuille.write_formula(ligne + 1, 4 + numero + numberUtilities, funcpuis_excel(xl_rowcol_to_cell(
                        ligne + 1, 4 + numero), str(myUtility['a']), str(myUtility['b']), str(myUtility['c'])))
                elif myUtility['type'] == 'log':
                    feuille.write_formula(ligne + 1, 4 + numero + numberUtilities, funclog_excel(xl_rowcol_to_cell(
                        ligne + 1, 4 + numero), str(myUtility['a']), str(myUtility['b']), str(myUtility['c']), str(myUtility['d'])))
                elif myUtility['type'] == 'lin':
                    feuille.write_formula(ligne + 1, 4 + numero + numberUtilities, funclin_excel(
                        xl_rowcol_to_cell(ligne + 1, 4 + numero), str(myUtility['a']), str(myUtility['b'])))
                elif myUtility['type'] == 'expo-power':
                    feuille.write_formula(ligne + 1, 4 + numero + numberUtilities, funcexpopower_excel(xl_rowcol_to_cell(
                        ligne + 1, 4 + numero), str(myUtility['a']), str(myUtility['b']), str(myUtility['c'])))

                numero = numero + 1

            feuille.write(ligne, 4 + numero +
                          numberUtilities, "U", formatTitre)

            def K(i):
                return xl_rowcol_to_cell(i, 1, row_abs=True, col_abs=True)

            def U(i):
                return xl_rowcol_to_cell(ligne + 1, 4 + i + numberUtilities)

            if mesK['method'] == "multiplicative":
                if numberUtilities == 2:
                    GU = utilite2_excel(K(1), K(2), K(3), U(1), U(2))
                    feuille.write_formula(
                        ligne + 1, 4 + numero + numberUtilities, GU)
                if numberUtilities == 3:
                    # in reality K(4) is K
                    GU = utilite3_excel(K(1), K(2), K(
                        3), K(4), U(1), U(2), U(3))
                    feuille.write_formula(
                        ligne + 1, 4 + numero + numberUtilities, GU)
                if numberUtilities == 4:
                    GU = utilite4_excel(K(1), K(2), K(3), K(
                        4), K(5), U(1), U(2), U(3), U(4))
                    feuille.write_formula(
                        ligne + 1, 4 + numero + numberUtilities, GU)
                if numberUtilities == 5:
                    GU = utilite5_excel(K(1), K(2), K(3), K(4), K(
                        5), K(6), U(1), U(2), U(3), U(4), U(5))
                    feuille.write_formula(
                        ligne + 1, 4 + numero + numberUtilities, GU)
                if numberUtilities == 6:
                    GU = utilite6_excel(K(1), K(2), K(3), K(4), K(5), K(
                        6), K(7), U(1), U(2), U(3), U(4), U(5), U(6))
                    feuille.write_formula(
                        ligne + 1, 4 + numero + numberUtilities, GU)

            else:
                nombre = 1
                GU = ""
                for monK in k:
                    GU += K(nombre)
                    for dk in monK['ID'].split(','):
                        GU += "*" + U(int(dk))
                    GU += "+"
                    nombre = nombre + 1

                GU = GU[:-1]
                feuille.write_formula(
                    ligne + 1, 4 + numero + numberUtilities, GU)

    # Ecriture du classeur sur le disque
    classeur.close()

    # On retourne le nom du fichier
    return 'fichier'+str(compteur)


def reduce(nombre):
    return math.floor(nombre * 100000000.0) / 100000000.0


def signe(nombre):
    if nombre >= 0:
        return "+" + str(nombre)
    else:
        return str(nombre)


def convert_to_text(function_type, data, x, arrondi):
    if function_type == "exp":
        return "(" + str(round(data['a'], arrondi)) + "*exp(" + signe(-round(data['b'], arrondi)) + "*" + x + ")" + signe(round(data['c'], arrondi)) + ")"
    elif function_type == "log":
        return "(" + str(round(data['a'], arrondi)) + "*log(" + str(round(data['b'], arrondi)) + "*" + x + signe(round(data['c'], arrondi)) + ")" + signe(round(data['d'], arrondi)) + ")"
    elif function_type == "pow":
        return "(" + str(round(data['a'], arrondi)) + "*(pow(" + x + "," + str(round(1 - data['b'], arrondi)) + ")-1)/(" + str(round(1 - data['b'], arrondi)) + ")" + signe(round(data['c'], arrondi)) + ")"
    elif function_type == "quad":
        return "(" + str(round(data['c'], arrondi)) + "*" + x + signe(round(-data['b'], arrondi)) + "*pow(" + x + ",2)" + signe(round(data['a'], arrondi)) + ")"
    elif function_type == "lin":
        return "(" + str(round(data['a'], arrondi)) + "*" + x + "+" + signe(round(data['b'], arrondi)) + ")"
    elif function_type == "expo-power":
        return "(" + str(round(data['a'], arrondi)) + "+exp(" + str(round(-data['b'], arrondi)) + "*pow(" + x + "," + str(round(data['c'], arrondi)) + "))"


# utilite pour le excel
def utilite2_excel(k1, k2, k, u1, u2):
    U = "=k*k1*k2*u1*u2 + k1*u1 + k2*u2"
    U = U.replace("k1", k1)
    U = U.replace("k2", k2)
    U = U.replace("k", k)
    U = U.replace("u1", u1)
    U = U.replace("u2", u2)
    return (U)


def utilite3_excel(k1, k2, k3, k, u1, u2, u3):
    U = "=k1*u1 + k2*u2 + k3*u3 + k*k1*k3*u1*u3 + k*k1*k2*u1*u2 + k*k2*k3*u2*u3 + k^2*k1*k2*k3*u1*u2*u3"
    U = U.replace("k1", k1)
    U = U.replace("k2", k2)
    U = U.replace("k3", k3)
    U = U.replace("k", k)
    U = U.replace("u1", u1)
    U = U.replace("u2", u2)
    U = U.replace("u3", u3)
    return (U)


def utilite4_excel(k1, k2, k3, k4, k, u1, u2, u3, u4):
    U = "=k^3*k1*k2*k3*k4*u1*u2*u3*u4 + k^2*(k1*k2*k3*u1*u2*u3+k1*k2*k4*u1*u2*u4+k2*k3*k4*u2*u3*u4+k1*k3*k4*u1*u3*u4) + k*(k1*k2*u1*u2+k2*k3*u2*u3+k1*k3*u1*u3+k1*k4*u1*u4+k2*k4*u2*u4+k3*k4*u3*u4) + k1*u1+k2*u2+k3*u3+k4*u4"
    U = U.replace("k1", k1)
    U = U.replace("k2", k2)
    U = U.replace("k3", k3)
    U = U.replace("k4", k4)
    U = U.replace("k", k)
    U = U.replace("u1", u1)
    U = U.replace("u2", u2)
    U = U.replace("u3", u3)
    U = U.replace("u4", u4)
    return (U)


def utilite5_excel(k1, k2, k3, k4, k5, k, u1, u2, u3, u4, u5):
    U = "=k^4*k1*k2*k3*k4*k5*u1*u2*u3*u4*u5 + k^3*(k1*k2*k3*k5*u1*u2*u3*u5 + k1*k2*k4*k5*u1*u2*u4*u5 + k2*k3*k4*k5*u2*u3*u5*u4 + k1*k3*k4*k5*u1*u5*u3*u4 + k1*k2*k3*k4*u1*u2*u3*u4) + k^2*(k1*k2*k3*u1*u2*u3 + k1*k2*k4*u1*u2*u4 + k1*k2*k5*u1*u2*u5 + k1*k3*k4*u1*u3*u4 +k1*k3*k5*u1*u3*u5 + k1*k4*k5*u1*u4*u5 + k2*k3*k4*u2*u3*u4 + k2*k3*k5*u2*u3*u5 + k2*k4*k5*u2*u4*u5 + k3*k4*k5*u3*u4*u5) + k*(k2*k3*u2*u3 + k1*k3*u1*u3 + k1*k4*u4*u4 + k2*k4*u2*u4 + k3*k4*u3*u4 + k1*k2*u1*u2 + k1*k5*u1*u5 + k2*k5*u2*u5 + k3*k5*u3*u5 + k4*k5*u4*u5) + k1*u1 + k2*u2 + k3*u3 + k4*u4 + k5*u5"
    U = U.replace("k1", k1)
    U = U.replace("k2", k2)
    U = U.replace("k3", k3)
    U = U.replace("k4", k4)
    U = U.replace("k5", k5)
    U = U.replace("k", k)
    U = U.replace("u1", u1)
    U = U.replace("u2", u2)
    U = U.replace("u3", u3)
    U = U.replace("u4", u4)
    U = U.replace("u5", u5)
    return (U)


def utilite6_excel(k1, k2, k3, k4, k5, k6, k, u1, u2, u3, u4, u5, u6):
    U = "=k^5*k1*k2*k3*k4*k5*k6 + k^4*(k1*k2*k3*k5*k6*u1*u2*u3*u5*u6 + k1*k2*k3*k4*k5*u1*u2*u3*u4*u5 + k1*k2*k4*k5*k6*u1*u2*u4*u5*u6 + k2*k3*k4*k5*k6*u2*u3*u4*u5*u6 + k1*k3*k4*k5*k6*u1*u3*u4*u5*u6 + k1*k2*k3*k4*k6*u1*u2*u3*u4*u6) +  k^3*(k1*k2*k3*k5*u1*u2*u3*u5 + k1*k2*k4*k5*u1*u2*u4*u5 + k2*k3*k4*k5*u2*u3*u4*u5 + k1*k3*k4*k5*u1*u3*u4*u5 + k1*k2*k3*k4*u1*u2*u3*u4 + k1*k2*k3*k6*u1*u2*u3*u6 + k1*k2*k4*k6*u1*u2*u4*u6 + k1*k2*k5*k6*u1*u2*u5*u6 + k1*k3*k4*k6*u1*u3*u4*u6 + k1*k3*k5*k6*u1*u3*u5*u6 + k1*k4*k5*k6*u1*u4*u5*u6 + k2*k3*k4*k6*u2*u3*u4*u6 + k2*k3*k5*k6*u2*u3*u5*u6  + k2*k4*k5*k6*u2*u4*u5*u6 + k3*k4*k5*k6*u3*u4*u5*u6) + k^2*(k1*k2*k3*u1*u2*u3 + k1*k2*k4*u1*u2*u4 + k1*k2*k5*u1*u2*u5 + k1*k3*k4*u1*u3*u4 +k1*k3*k5*u1*u3*u5 + k1*k4*k5*u1*u4*u5 + k2*k3*k4*u2*u3*u4 + k2*k3*k5*u2*u3*u5 + k2*k4*k5*u2*u4*u5 + k3*k4*k5*u3*u4*u5 + k3*k4*k6*u3*u4*u6 + k1*k2*k6*u1*u2*u6 + k1*k3*k6*u1*u3*u6 + k1*k4*k6*u1*u4*u6 + k1*k5*k6*u1*u5*u6 + k3*k4*k6*u3*u4*u6 + k3*k5*k6*u3*u5*u6 + k2*k4*k6*u2*u4*u6 + k2*k5*k6*u2*u5*u6 + k4*k5*k6*u4*u5*u6) + k*(k2*k3*u2*u3 + k1*k3*u1*u3 + k1*k4*u1*u4 + k1*k6*u1*u6 + k1*k5*u1*u5 + k1*k2*u1*u2 + k2*k4*u2*u4 + k3*k4*u3*u4 + k2*k5*u2*u5 + k3*k5*u3*u5 + k4*k5*u4*u5 + k2*k6*u2*u6 + k3*k6*u3*u6 + k4*k6*u4*u6 + k5*k6*u5*u6) + k1*u1 +k2*u2 +k3*u3 +k4*u4 +k5*u5 +k6*u6"
    U = U.replace("k1", k1)
    U = U.replace("k2", k2)
    U = U.replace("k3", k3)
    U = U.replace("k4", k4)
    U = U.replace("k5", k5)
    U = U.replace("k6", k6)
    U = U.replace("k", k)
    U = U.replace("u1", u1)
    U = U.replace("u2", u2)
    U = U.replace("u3", u3)
    U = U.replace("u4", u4)
    U = U.replace("u5", u5)
    U = U.replace("u6", u6)
    return (U)
