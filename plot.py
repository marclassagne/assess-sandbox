import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import io
from functions import *


def generate_svg_plot(dictionary, min, max, liste_cord, width):

    # img
    imgdata = io.BytesIO()

    # creation des listes des abscisses et ordonnees
    lx = []
    ly = []

    for coord in liste_cord:
        lx.append(coord[0])
        ly.append(coord[1])

    # creation des valeurs en abscisses et en ordonnee avec les listes lx et ly
    x1 = np.array(lx)
    y1 = np.array(ly)

    plt.figure(figsize=(width, width))
    plt.axis([min, max, 0., 1.])
    plt.plot(x1, y1, 'ko', label="Original Data")
    x = np.linspace(min, max, 100)

    #translation suivant x des courbes a afficher en cas de valeurs negatives
    xneg = np.linspace(0, max-min, 100)

    if min >= 0 :
        for func in dictionary.keys():
            if func == 'exp':
                a = dictionary[func]['a']
                b = dictionary[func]['b']
                c = dictionary[func]['c']
                plt.plot(x, funcexp(x, a, b, c), '#401539',
                         label="Exp Fitted Curve")

            elif func == 'quad':
                a = dictionary[func]['a']
                b = dictionary[func]['b']
                c = dictionary[func]['c']
                plt.plot(x, funcquad(x, a, b, c), '#458C8C',
                         label="Quad Fitted Curve")

            elif func == 'pow':
                a = dictionary[func]['a']
                b = dictionary[func]['b']
                c = dictionary[func]['c']
                plt.plot(x, funcpuis(x, a, b, c), '#6DA63C',
                         label="Pow Fitted Curve")

            elif func == 'log':
                a = dictionary[func]['a']
                b = dictionary[func]['b']
                c = dictionary[func]['c']
                d = dictionary[func]['d']
                plt.plot(x, funclog(x, a, b, c, d),
                         '#D9585A', label="Log Fitted Curve")

            elif func == 'lin':
                a = dictionary[func]['a']
                b = dictionary[func]['b']
                plt.plot(x, funclin(x, a, b), '#D9B504', label="Lin Fitted Curve")

            elif func =='expo-power':
                a = dictionary[func]['a']
                b = dictionary[func]['b']
                c = dictionary[func]['c']
                plt.plot(x, funcexpopower(x, a, b, c),
                         '#26C4EC', label="Expo-Power Fitted Curve")

    else: 
        for func in dictionary.keys():
            if func == 'exp':
                a = dictionary[func]['a']
                b = dictionary[func]['b']
                c = dictionary[func]['c']
                plt.plot(x, funcexp(xneg, a, b, c), '#401539',
                         label="Exp Fitted Curve")

            elif func == 'quad':
                a = dictionary[func]['a']
                b = dictionary[func]['b']
                c = dictionary[func]['c']
                plt.plot(x, funcquad(xneg, a, b, c), '#458C8C',
                         label="Quad Fitted Curve")

            elif func == 'pow':
                a = dictionary[func]['a']
                b = dictionary[func]['b']
                c = dictionary[func]['c']
                plt.plot(x, funcpuis(xneg, a, b, c), '#6DA63C',
                         label="Pow Fitted Curve")

            elif func == 'log':
                a = dictionary[func]['a']
                b = dictionary[func]['b']
                c = dictionary[func]['c']
                d = dictionary[func]['d']
                plt.plot(x, funclog(xneg, a, b, c, d),
                         '#D9585A', label="Log Fitted Curve")

            elif func == 'lin':
                a = dictionary[func]['a']
                b = dictionary[func]['b']
                plt.plot(x, funclin(xneg, a, b), '#D9B504', label="Lin Fitted Curve")

            elif func =='expo-power':
                a = dictionary[func]['a']
                b = dictionary[func]['b']
                c = dictionary[func]['c']
                plt.plot(x, funcexpopower(xneg, a, b, c),
                         '#26C4EC', label="Expo-Power Fitted Curve")


    plt.savefig(imgdata, format='svg')
    plt.close()

    return imgdata.getvalue()

def pie_chart(names, probas):

    imgdata = io.BytesIO()
    colors=['lightcoral', 'lightskyblue']

    if len(names) == 3:
        plt.figure(1)
        plt.subplot(121)
        plt.pie([1], labels=[names[0]], colors=colors, startangle=90, autopct='%1.0f%%', textprops={"weight":"bold"})
        plt.title("A", fontdict={"fontweight":"bold"})
        plt.subplot(122)
        plt.pie(probas, labels=names[1:], colors=colors, startangle=90, autopct='%1.0f%%', textprops={"weight":"bold"})
        plt.title("B", fontdict={"fontweight":"bold"})
        fig = plt.gcf()
        fig.set_size_inches(8, 4)
    else:
        plt.pie(probas, labels=names, colors=colors, startangle=90, autopct='%1.0f%%', textprops={"weight":"bold"})
        fig = plt.gcf()
        fig.set_size_inches(4, 4)

    plt.savefig(imgdata, format='svg')
    plt.close()

    return imgdata.getvalue()

def generate_svg_plot_QUALI(dictionary, list_names, width):

	# img
	imgdata = io.BytesIO()

	# Open a new figure with the right width
	plt.figure(figsize=(width, width))
	
	graph_x = list(range(len(dictionary)))
	graph_y = dictionary
	
	plt.figure(1)
	plt.plot(graph_x, graph_y, 'r')
	plt.plot([0, graph_x[-1]], [0, 1], 'k')
	plt.axis([0, graph_x[-1], 0, 1])
	plt.grid()
	plt.xticks(graph_x, list_names)

	plt.savefig(imgdata, format='svg')
	plt.close()

	return imgdata.getvalue()
