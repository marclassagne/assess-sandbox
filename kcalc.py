import numpy as np
import math
import json
from sympy import *
from scipy.optimize import fsolve


def calculUtilityMultiplicative(myK, myU):
    if len(myK) - 1 == 2:
        return {'Ulatex':utilite2(myK[0]['value'], myK[1]['value'], myK[2]['value'], convert_to_text_latex(myU[0], "x1"), convert_to_text_latex(myU[1], "x2")),'Uexcel':utilite2(myK[0]['value'], myK[1]['value'], myK[2]['value'], convert_to_text_excel(myU[0], "x1"), convert_to_text_excel(myU[1], "x2")), 'U': utilite2(myK[0]['value'], myK[1]['value'], myK[2]['value'], convert_to_text(myU[0], "x1"), convert_to_text(myU[1], "x2")), 'k': myK, 'utilities': myU}
    elif len(myK) - 1 == 3:
        return {'Ulatex':utilite3(myK[0]['value'], myK[1]['value'], myK[2]['value'], myK[3]['value'], convert_to_text_latex(myU[0], "x1"), convert_to_text_latex(myU[1], "x2"), convert_to_text_latex(myU[2], "x3")),'Uexcel':utilite3(myK[0]['value'], myK[1]['value'], myK[2]['value'], myK[3]['value'], convert_to_text_excel(myU[0], "x1"), convert_to_text_excel(myU[1], "x2"), convert_to_text_excel(myU[2], "x3")),'U': utilite3(myK[0]['value'], myK[1]['value'], myK[2]['value'], myK[3]['value'], convert_to_text(myU[0], "x1"), convert_to_text(myU[1], "x2"), convert_to_text(myU[2], "x3")), 'k': myK, 'utilities': myU}
    elif len(myK) - 1 == 4:
        return {'Ulatex':utilite4(myK[0]['value'], myK[1]['value'], myK[2]['value'], myK[3]['value'], myK[4]['value'], convert_to_text_latex(myU[0], "x1"), convert_to_text_latex(myU[1], "x2"), convert_to_text_latex(myU[2], "x3"), convert_to_text_latex(myU[3], "x4")),'Uexcel':utilite4(myK[0]['value'], myK[1]['value'], myK[2]['value'], myK[3]['value'], myK[4]['value'], convert_to_text_excel(myU[0], "x1"), convert_to_text_excel(myU[1], "x2"), convert_to_text_excel(myU[2], "x3"), convert_to_text_excel(myU[3], "x4")), 'U': utilite4(myK[0]['value'], myK[1]['value'], myK[2]['value'], myK[3]['value'], myK[4]['value'], convert_to_text(myU[0], "x1"), convert_to_text(myU[1], "x2"), convert_to_text(myU[2], "x3"), convert_to_text(myU[3], "x4")), 'k': myK, 'utilities': myU}
    elif len(myK) - 1 == 5:
        return {'Ulatex':utilite5(myK[0]['value'], myK[1]['value'], myK[2]['value'], myK[3]['value'], myK[4]['value'], myK[5]['value'], convert_to_text_latex(myU[0], "x1"), convert_to_text_latex(myU[1], "x2"), convert_to_text_latex(myU[2], "x3"), convert_to_text_latex(myU[3], "x4"), convert_to_text_latex(myU[4], "x5")),'Uexcel':utilite5(myK[0]['value'], myK[1]['value'], myK[2]['value'], myK[3]['value'], myK[4]['value'], myK[5]['value'], convert_to_text_excel(myU[0], "x1"), convert_to_text_excel(myU[1], "x2"), convert_to_text_excel(myU[2], "x3"), convert_to_text_excel(myU[3], "x4"), convert_to_text_excel(myU[4], "x5")), 'U': utilite5(myK[0]['value'], myK[1]['value'], myK[2]['value'], myK[3]['value'], myK[4]['value'], myK[5]['value'], convert_to_text(myU[0], "x1"), convert_to_text(myU[1], "x2"), convert_to_text(myU[2], "x3"), convert_to_text(myU[3], "x4"), convert_to_text(myU[4], "x5")), 'k': myK, 'utilities': myU}
    elif len(myK) - 1 == 6:
        return {'Ulatex':utilite6(myK[0]['value'], myK[1]['value'], myK[2]['value'], myK[3]['value'], myK[4]['value'], myK[5]['value'], myK[6]['value'], convert_to_text_latex(myU[0], "x1"), convert_to_text_latex(myU[1], "x2"), convert_to_text_latex(myU[2], "x3"), convert_to_text_latex(myU[3], "x4"), convert_to_text_latex(myU[4], "x5"), convert_to_text_latex(myU[5], "x6")),'Uexcel':utilite6(myK[0]['value'], myK[1]['value'], myK[2]['value'], myK[3]['value'], myK[4]['value'], myK[5]['value'], myK[6]['value'], convert_to_text_excel(myU[0], "x1"), convert_to_text_excel(myU[1], "x2"), convert_to_text_excel(myU[2], "x3"), convert_to_text_excel(myU[3], "x4"), convert_to_text_excel(myU[4], "x5"), convert_to_text_excel(myU[5], "x6")), 'U': utilite6(myK[0]['value'], myK[1]['value'], myK[2]['value'], myK[3]['value'], myK[4]['value'], myK[5]['value'], myK[6]['value'], convert_to_text(myU[0], "x1"), convert_to_text(myU[1], "x2"), convert_to_text(myU[2], "x3"), convert_to_text(myU[3], "x4"), convert_to_text(myU[4], "x5"), convert_to_text(myU[5], "x6")), 'k': myK, 'utilities': myU}
    U = 1
    return "Error : nothing was done"


def calculUtilityMultilinear(myK, myU):
    U = ""
    for monK in myK:
        U += str(monK['value'])
        for dk in monK['ID'].split(','):
            U += "*" + convert_to_text(myU[int(dk) - 1], "k" + dk)
        U += "+"
    # In order to delete the last + character
    U = U[:-1]

    Ulatex = ""
    for monK in myK:
        Ulatex += str(monK['value'])
        for dk in monK['ID'].split(','):
            Ulatex += "*" + convert_to_text_latex(myU[int(dk) - 1], "k" + dk)
        Ulatex += "+"
    # In order to delete the last + character
    Ulatex = Ulatex[:-1]

    Uexcel = ""
    for monK in myK:
        Uexcel += str(monK['value'])
        for dk in monK['ID'].split(','):
            Uexcel += "*" + convert_to_text_excel(myU[int(dk) - 1], "k" + dk)
        Uexcel += "+"
    # In order to delete the last + character
    Uexcel = Uexcel[:-1]
	
    return {'U': U, 'Ulatex': Ulatex, 'Uexcel': Uexcel, 'k': myK, 'utilities': myU}


# ---- 2 -----
def calculk2(k1, k2):
    if k1 + k2 == 1:
        return {'success': True, 'k': 0}
    k = symbols('k')
    solution = solve(k1 * k2 * k + k1 + k2 - 1, k)
    return {'success': True, 'k': round(float(solution[0]), 4)}


# def utilite2(k1,k2,k):
# u1=u1.get()
# u2=u2.get()
# U=k*k1*k2*u1*u2+k1*u1+k2*u2
# return (U)

def utilite2(k1, k2, k, u1, u2):
    U = str(k1) + "*" + u1 + str(k2) + "*" + u2 + \
        str(k * k1 * k2) + "*" + u1 + "*" + u2
    return (U)

# ---- 3 -----


def calculk3(k1, k2, k3):
    if k1 + k2 + k3 == 1:
        return {'success': True, 'k': 0}
    coeff = [k1 * k2 * k3, k1 * k2 + k2 * k3 + k1 * k3, k1 + k2 + k3 - 1]
    solution = np.roots(coeff)
    liste = [solution[0], solution[1]]

    if k1 + k2 + k3 > 1:
        k = float(round(liste[0], 1))
        return {'success': True, 'k': k}
    else:
        k = float(round(liste[1], 1))
        return {'success': True, 'k': k}


def utilite3(k1, k2, k3, k, u1, u2, u3):
    U = str(k1) + "*" + u1 + "+"
    U += str(k2) + "*" + u2 + "+"
    U += str(k3) + "*" + u3 + "+"
    U += str(k * k1 * k3) + "*" + u1 + "*" + u3 + "+"
    U += str(k * k1 * k2) + "*" + u1 + "*" + u2 + "+"
    U += str(k * k2 * k3) + "*" + u2 + "*" + u3 + "+"
    U += str(k**2 * k1 * k2 * k3) + "*" + u1 + "*" + u2 + "*" + u3
    return (U)


# ---- 4 -----
def calculk4(k1, k2, k3, k4):
    if k1 + k2 + k3 + k4 == 1:
        return {'success': True, 'k': 0}
    x0 = 0
    p_k = lambda k: k1 * k2 * k3 * k4 * k**3 + (k1 * k2 * k3 + k1 * k2 * k4 + k2 * k3 * k4 + k1 * k3 * k4) * k**2 + (
        k1 * k2 + k2 * k3 + k1 * k3 + k1 * k4 + k2 * k4 + k3 * k4) * k + k1 + k2 + k3 + k4 - 1
    solution = fsolve(p_k, x0, xtol=1.49012e-12, maxfev=1000)

    if solution[0] == x0:
        return {'success': False, 'k': "Unable to calculate K, please change your ki values"}
    else:
        return {'success': True, 'k': float(solution[0])}


# def utilite4(k1,k2,k3,k4,k):
# u1=u1.get()
# u2=u2.get()
# u3=u3.get()
# u4=u4.get()
# U=k**3*k1*k2*k3*k4*u1*u2*u3*u4+k**2*(k1*k2*k3*u1*u2*u3+k1*k2*k4*u1*u2*u4+k2*k3*k4*u2*u3*u4+k1*k3*k4*u1*u3*u4)+k*(k1*k2*u1*u2+k2*k3*u2*u3+k1*k3*u1*u3+k1*k4*u1*u4+k2*k4*u2*u4+k3*k4*u3*u4)+k1*u1+k2*u2+k3*u3+k4*u4
# return (U)

def utilite4(k1, k2, k3, k4, k, u1, u2, u3, u4):
    U = str(k1) + "*" + u1 + "+"
    U += str(k2) + "*" + u2 + "+"
    U += str(k3) + "*" + u3 + "+"
    U += str(k4) + "*" + u4 + "+"
    U += str(k * k1 * k2) + "*" + u1 + "*" + u2 + "+"
    U += str(k * k1 * k3) + "*" + u1 + "*" + u3 + "+"
    U += str(k * k1 * k4) + "*" + u1 + "*" + u4 + "+"
    U += str(k * k2 * k3) + "*" + u2 + "*" + u3 + "+"
    U += str(k * k3 * k4) + "*" + u3 + "*" + u4 + "+"
    U += str(k * k2 * k4) + "*" + u2 + "*" + u4 + "+"
    U += str(k**2 * k1 * k2 * k3) + "*" + u1 + "*" + u2 + "*" + u3 + "+"
    U += str(k**2 * k1 * k2 * k4) + "*" + u1 + "*" + u2 + "*" + u4 + "+"
    U += str(k**2 * k1 * k3 * k4) + "*" + u2 + "*" + u3 + "*" + u4 + "+"
    U += str(k**2 * k2 * k3 * k4) + "*" + u2 + "*" + u3 + "*" + u4 + "+"
    U += str(k**3 * k1 * k2 * k3 * k4) + "*" + \
        u1 + "*" + u2 + "*" + u3 + "*" + u4
    return (U)


# ---- 5 -----
def calculk5(k1, k2, k3, k4, k5):
    if k1 + k2 + k3 + k4 + k5 == 1:
        return {'success': True, 'k': 0}
    x0 = 0
    p_k = lambda k: k1 * k2 * k3 * k4 * k5 * k**4 + (k1 * k2 * k3 * k5 + k1 * k2 * k4 * k5 + k2 * k3 * k4 * k5 + k1 * k3 * k4 * k5 + k1 * k2 * k3 * k4) * k**3 + (k1 * k2 * k3 + k1 * k2 * k4 + k1 * k2 * k5 + k1 * k3 * k4 + k1 *
                                                                                                                                                                  k3 * k5 + k1 * k4 * k5 + k2 * k3 * k4 + k2 * k3 * k5 + k2 * k4 * k5 + k3 * k4 * k5) * k**2 + (k2 * k3 + k1 * k3 + k1 * k4 + k2 * k4 + k3 * k4 + k1 * k2 + k1 * k5 + k2 * k5 + k3 * k5 + k4 * k5) * k + k1 + k2 + k3 + k4 + k5 - 1
    solution = fsolve(p_k, x0, xtol=1.49012e-12, maxfev=1000)

    if solution[0] == x0:
        return {'success': False, 'k': "Unable to calculate K, please change your ki values"}
    else:
        return {'success': True, 'k': float(solution[0])}


# def utilite5(k1,k2,k3,k4,k5,k):
# u1=u1.get()
# u2=u2.get()
# u3=u3.get()
# u4=u4.get()
# u5=u5.get()
##    U= k^4*k1*k2*k3*k4*k5*u1*u2*u3*u4*u5 + k^3(k1*k2*k3*k5*u1*u2*u3*u5 + k1*k2*k4*k5*u1*u2*u4*u5 + k2*k3*k4*k5*u2*u3*u5*u4 + k1*k3*k4*k5*u1*u5*u3*u4 + k1*k2*k3*k4*u1*u2*u3*u4) + k**(k1*k2*k3*u1*u2*u3 + k1*k2*k4*u1*u2*u4 + k1*k2*k5*u1*u2*u5 + k1*k3*k4*u1*u3*u4 +k1*k3*k5*u1*u3*u5 + k1*k4*k5*u1*u4*u5 + k2*k3*k4*u2*u3*u4 + k2*k3*k5*u2*u3*u5 + k2*k4*k5*u2*u4*u5 + k3*k4*k5*u3*u4*u5) + k(k2*k3*u2*u3 + k1*k3*u1*u3 + k1*k4*u4*u4 + k2*k4*u2*u4 + k3*k4*u3*u4 + k1*k2*u1*u2 + k1*k5*u1*u5 + k2*k5*u2*u5 + k3*k5*u3*u5 + k4*k5*u4*u5) + k1*u1 + k2*u2 + k3*u3 + k4*u4 + k5*u5
# return (U)

def utilite5(k1, k2, k3, k4, k5, k, u1, u2, u3, u4, u5):
    U = str(k1) + "*" + u1 + "+"
    U += str(k2) + "*" + u2 + "+"
    U += str(k3) + "*" + u3 + "+"
    U += str(k4) + "*" + u4 + "+"
    U += str(k5) + "*" + u5 + "+"
    U += str(k * k1 * k2) + "*" + u1 + "*" + u2 + "+"
    U += str(k * k1 * k3) + "*" + u1 + "*" + u3 + "+"
    U += str(k * k1 * k4) + "*" + u1 + "*" + u4 + "+"
    U += str(k * k1 * k5) + "*" + u1 + "*" + u5 + "+"
    U += str(k * k2 * k3) + "*" + u2 + "*" + u3 + "+"
    U += str(k * k2 * k4) + "*" + u2 + "*" + u4 + "+"
    U += str(k * k2 * k5) + "*" + u2 + "*" + u5 + "+"
    U += str(k * k3 * k4) + "*" + u3 + "*" + u4 + "+"
    U += str(k * k3 * k5) + "*" + u3 + "*" + u5 + "+"
    U += str(k * k4 * k5) + "*" + u4 + "*" + u5 + "+"
    U += str(k**2 * k1 * k2 * k3) + "*" + u1 + "*" + u2 + "*" + u3 + "+"
    U += str(k**2 * k1 * k2 * k5) + "*" + u1 + "*" + u2 + "*" + u5 + "+"
    U += str(k**2 * k1 * k3 * k4) + "*" + u1 + "*" + u3 + "*" + u4 + "+"
    U += str(k**2 * k1 * k2 * k4) + "*" + u1 + "*" + u2 + "*" + u4 + "+"
    U += str(k**2 * k2 * k3 * k4) + "*" + u2 + "*" + u3 + "*" + u4 + "+"
    U += str(k**2 * k1 * k3 * k5) + "*" + u1 + "*" + u3 + "*" + u5 + "+"
    U += str(k**2 * k1 * k4 * k5) + "*" + u1 + "*" + u4 + "*" + u5 + "+"
    U += str(k**2 * k2 * k3 * k5) + "*" + u2 + "*" + u3 + "*" + u5 + "+"
    U += str(k**2 * k4 * k2 * k5) + "*" + u4 + "*" + u2 + "*" + u5 + "+"
    U += str(k**2 * k3 * k4 * k5) + "*" + u3 + "*" + u4 + "*" + u5 + "+"
    U += str(k**3 * k1 * k2 * k3 * k4) + "*" + u1 + \
        "*" + u2 + "*" + u3 + "*" + u4 + "+"
    U += str(k**3 * k1 * k3 * k4 * k5) + "*" + u1 + \
        "*" + u5 + "*" + u3 + "*" + u4 + "+"
    U += str(k**3 * k1 * k2 * k3 * k5) + "*" + u1 + \
        "*" + u2 + "*" + u3 + "*" + u5 + "+"
    U += str(k**3 * k1 * k2 * k4 * k5) + "*" + u1 + \
        "*" + u2 + "*" + u4 + "*" + u5 + "+"
    U += str(k**3 * k2 * k3 * k4 * k5) + "*" + u2 + \
        "*" + u3 + "*" + u4 + "*" + u5 + "+"
    U += str(k**4 * k1 * k2 * k3 * k4 * k5) + "*" + u1 + \
        "*" + u2 + "*" + u3 + "*" + u4 + "*" + u5
    return (U)


# ---- 6 -----
def calculk6(k1, k2, k3, k4, k5, k6):
    if k1 + k2 + k3 + k4 + k5 + k6 == 1:
        return {'success': True, 'k': 0}
    a = k1 * k2 * k3 * k4 * k5 * k6
    b = (k1 * k2 * k3 * k5 * k6 + k1 * k2 * k3 * k4 * k5 + k1 * k2 * k4 * k5 *
         k6 + k2 * k3 * k4 * k5 * k6 + k1 * k3 * k4 * k5 * k6 + k1 * k2 * k3 * k4 * k6)
    c = (k1 * k2 * k3 * k5 + k1 * k2 * k4 * k5 + k2 * k3 * k4 * k5 + k1 * k3 * k4 * k5 + k1 * k2 * k3 * k4 + k1 * k2 * k3 * k6 + k1 * k2 * k4 * k6 + k1 *
         k2 * k5 * k6 + k1 * k3 * k4 * k6 + k1 * k3 * k5 * k6 + k1 * k4 * k5 * k6 + k2 * k3 * k4 * k6 + k2 * k3 * k5 * k6 + k2 * k4 * k5 * k6 + k3 * k4 * k5 * k6)
    d = (k1 * k2 * k3 + k1 * k2 * k4 + k1 * k2 * k5 + k1 * k3 * k4 + k1 * k3 * k5 + k1 * k4 * k5 + k2 * k3 * k4 + k2 * k3 * k5 + k2 * k4 * k5 + k3 * k4 *
         k5 + k3 * k4 * k6 + k1 * k2 * k6 + k1 * k3 * k6 + k1 * k4 * k6 + k1 * k5 * k6 + k3 * k4 * k6 + k3 * k5 * k6 + k2 * k4 * k6 + k2 * k5 * k6 + k4 * k5 * k6)
    e = (k2 * k3 + k1 * k3 + k1 * k4 + k1 * k6 + k1 * k5 + k1 * k2 + k2 * k4 +
         k3 * k4 + k2 * k5 + k3 * k5 + k4 * k5 + k2 * k6 + k3 * k6 + k4 * k6 + k5 * k6)
    f = k1 + k2 + k3 + k4 + k5 + k6 - 1
    p_k = lambda k: a * k**5 + b * k**4 + c * k**3 + d * k**2 + e * k + f

    solutions = fsolve(p_k, 0, xtol=1.49012e-08, maxfev=1000)
    return {'success': True, 'k': float(solutions[0])}


# def utilite6(k1,k2,k3,k4,k):
# u1=u1.get()
# u2=u2.get()
# u3=u3.get()
# u4=u4.get()
# u5=u5.get()
# u6=u6.get()
##   	U= k**5*k1*k2*k3*k4*k5*k6 + k**4(k1*k2*k3*k5*k6*u1*u2*u3*u5*u6 + k1*k2*k3*k4*k5*u1*u2*u3*u4*u5 + k1*k2*k4*k5*k6*u1*u2*u4*u5*u6 + k2*k3*k4*k5*k6*u2*u3*u4*u5*u6 + k1*k3*k4*k5*k6*u1*u3*u4*u5*u6 + k1*k2*k3*k4*k6*u1*u2*u3*u4*u6) +  k^3(k1*k2*k3*k5*u1*u2*u3*u5 + k1*k2*k4*k5*u1*u2*u4*u5 + k2*k3*k4*k5*u2*u3*u4*u5 + k1*k3*k4*k5*u1*u3*u4*u5 + k1*k2*k3*k4*u1*u2*u3*u4 + k1*k2*k3*k6*u1*u2*u3*u6 + k1*k2*k4*k6*u1*u2*u4*u6 + k1*k2*k5*k6*u1*u2*u5*u6 + k1*k3*k4*k6*u1*u3*u4*u6 + k1*k3*k5*k6*u1*u3*u5*u6 + k1*k4*k5*k6*u1*u4*u5*u6 + k2*k3*k4*k6*u2*u3*u4*u6 + k2*k3*k5*k6*u2*u3*u5*u6  + k2*k4*k5*k6*u2*u4*u5*u6 + k3*k4*k5*k6*u3*u4*u5*u6) + k**(k1*k2*k3*u1*u2*u3 + k1*k2*k4*u1*u2*u4 + k1*k2*k5*u1*u2*u5 + k1*k3*k4*u1*u3*u4 +k1*k3*k5*u1*u3*u5 + k1*k4*k5*u1*u4*u5 + k2*k3*k4*u2*u3*u4 + k2*k3*k5*u2*u3*u5 + k2*k4*k5*u2*u4*u5 + k3*k4*k5*u3*u4*u5 + k3*k4*k6*u3*u4*u6 + k1*k2*k6*u1*u2*u6 + k1*k3*k6*u1*u3*u6 + k1*k4*k6*u1*u4*u6 + k1*k5*k6*u1*u5*u6 + k3*k4*k6*u3*u4*u6 + k3*k5*k6*u3*u5*u6 + k2*k4*k6*u2*u4*u6 + k2*k5*k6*u2*u5*u6 + k4*k5*k6*u4*u5*u6) + k*(k2*k3*u2*u3 + k1*k3*u1*u3 + k1*k4*u1*u4 + k1*k6*u1*u6 + k1*k5*u1*u5 + k1*k2*u1*u2 + k2*k4*u2*u4 + k3*k4*u3*u4 + k2*k5*u2*u5 + k3*k5*u3*u5 + k4*k5*u4*u5 + k2*k6*u2*u6 + k3*k6*u3*u6 + k4*k6*u4*u6 + k5*k6*u5*u6) + k1*u1 +k2*u2 +k3*u3 +k4*u4 +k5*u5 +k6*u6
##
# return (U)
def utilite6(k1, k2, k3, k4, k5, k6, k, u1, u2, u3, u4, u5, u6):

    U = str(k1) + "*" + u1 + "+"
    U += str(k2) + "*" + u2 + "+"
    U += str(k3) + "*" + u3 + "+"
    U += str(k4) + "*" + u4 + "+"
    U += str(k5) + "*" + u5 + "+"
    U += str(k6) + "*" + u6 + "+"
    U += str(k * k1 * k2) + "*" + u1 + "*" + u2 + "+"
    U += str(k * k1 * k3) + "*" + u1 + "*" + u3 + "+"
    U += str(k * k1 * k4) + "*" + u1 + "*" + u4 + "+"
    U += str(k * k1 * k5) + "*" + u1 + "*" + u5 + "+"
    U += str(k * k1 * k6) + "*" + u1 + "*" + u6 + "+"
    U += str(k * k2 * k3) + "*" + u2 + "*" + u3 + "+"
    U += str(k * k2 * k4) + "*" + u2 + "*" + u4 + "+"
    U += str(k * k2 * k5) + "*" + u2 + "*" + u5 + "+"
    U += str(k * k2 * k6) + "*" + u2 + "*" + u6 + "+"
    U += str(k * k3 * k4) + "*" + u3 + "*" + u4 + "+"
    U += str(k * k3 * k5) + "*" + u3 + "*" + u5 + "+"
    U += str(k * k3 * k6) + "*" + u3 + "*" + u6 + "+"
    U += str(k * k4 * k5) + "*" + u4 + "*" + u5 + "+"
    U += str(k * k4 * k6) + "*" + u4 + "*" + u6 + "+"
    U += str(k * k5 * k6) + "*" + u5 + "*" + u6 + "+"
    U += str(k**2 * k1 * k2 * k3) + "*" + u1 + "*" + u2 + "*" + u3 + "+"
    U += str(k**2 * k1 * k2 * k5) + "*" + u1 + "*" + u2 + "*" + u5 + "+"
    U += str(k**2 * k1 * k3 * k4) + "*" + u1 + "*" + u3 + "*" + u4 + "+"
    U += str(k**2 * k1 * k2 * k4) + "*" + u1 + "*" + u2 + "*" + u4 + "+"
    U += str(k**2 * k2 * k3 * k4) + "*" + u2 + "*" + u3 + "*" + u4 + "+"
    U += str(k**2 * k1 * k3 * k5) + "*" + u1 + "*" + u3 + "*" + u5 + "+"
    U += str(k**2 * k1 * k4 * k5) + "*" + u1 + "*" + u4 + "*" + u5 + "+"
    U += str(k**2 * k2 * k3 * k5) + "*" + u2 + "*" + u3 + "*" + u5 + "+"
    U += str(k**2 * k4 * k2 * k5) + "*" + u4 + "*" + u2 + "*" + u5 + "+"
    U += str(k**2 * k3 * k4 * k5) + "*" + u3 + "*" + u4 + "*" + u5 + "+"
    U += str(k**2 * k1 * k2 * k6) + "*" + u1 + "*" + u2 + "*" + u6 + "+"
    U += str(k**2 * k1 * k3 * k6) + "*" + u1 + "*" + u3 + "*" + u6 + "+"
    U += str(k**2 * k1 * k4 * k6) + "*" + u1 + "*" + u4 + "*" + u6 + "+"
    U += str(k**2 * k1 * k5 * k6) + "*" + u1 + "*" + u5 + "*" + u6 + "+"
    U += str(k**2 * k2 * k3 * k6) + "*" + u2 + "*" + u3 + "*" + u6 + "+"
    U += str(k**2 * k2 * k4 * k6) + "*" + u2 + "*" + u4 + "*" + u6 + "+"
    U += str(k**2 * k2 * k5 * k6) + "*" + u2 + "*" + u5 + "*" + u6 + "+"
    U += str(k**2 * k3 * k4 * k6) + "*" + u3 + "*" + u4 + "*" + u6 + "+"
    U += str(k**2 * k3 * k5 * k6) + "*" + u3 + "*" + u5 + "*" + u6 + "+"
    U += str(k**2 * k4 * k5 * k6) + "*" + u4 + "*" + u5 + "*" + u6 + "+"
    U += str(k**3 * k1 * k2 * k3 * k4) + "*" + u1 + \
        "*" + u2 + "*" + u3 + "*" + u4 + "+"
    U += str(k**3 * k1 * k3 * k4 * k5) + "*" + u1 + \
        "*" + u5 + "*" + u3 + "*" + u4 + "+"
    U += str(k**3 * k1 * k2 * k3 * k5) + "*" + u1 + \
        "*" + u2 + "*" + u3 + "*" + u5 + "+"
    U += str(k**3 * k1 * k2 * k4 * k5) + "*" + u1 + \
        "*" + u2 + "*" + u4 + "*" + u5 + "+"
    U += str(k**3 * k2 * k3 * k4 * k5) + "*" + u2 + \
        "*" + u3 + "*" + u4 + "*" + u5 + "+"
    U += str(k**3 * k1 * k2 * k3 * k6) + "*" + u1 + \
        "*" + u2 + "*" + u3 + "*" + u6 + "+"
    U += str(k**3 * k1 * k2 * k4 * k6) + "*" + u1 + \
        "*" + u2 + "*" + u4 + "*" + u6 + "+"
    U += str(k**3 * k1 * k2 * k5 * k6) + "*" + u1 + \
        "*" + u2 + "*" + u5 + "*" + u6 + "+"
    U += str(k**3 * k1 * k3 * k5 * k6) + "*" + u1 + \
        "*" + u3 + "*" + u5 + "*" + u6 + "+"
    U += str(k**3 * k1 * k4 * k5 * k6) + "*" + u1 + \
        "*" + u4 + "*" + u5 + "*" + u6 + "+"
    U += str(k**3 * k2 * k3 * k4 * k6) + "*" + u2 + \
        "*" + u3 + "*" + u4 + "*" + u6 + "+"
    U += str(k**3 * k1 * k3 * k4 * k6) + "*" + u1 + \
        "*" + u3 + "*" + u4 + "*" + u6 + "+"
    U += str(k**3 * k2 * k3 * k5 * k6) + "*" + u2 + \
        "*" + u3 + "*" + u5 + "*" + u6 + "+"
    U += str(k**3 * k2 * k4 * k5 * k6) + "*" + u2 + \
        "*" + u4 + "*" + u5 + "*" + u6 + "+"
    U += str(k**3 * k1 * k2 * k5 * k6) + "*" + u1 + \
        "*" + u2 + "*" + u5 + "*" + u6 + "+"
    U += str(k**4 * k1 * k2 * k3 * k4 * k5) + "*" + u1 + \
        "*" + u2 + "*" + u3 + "*" + u4 + "+" + u5 + "+"
    U += str(k**4 * k1 * k2 * k3 * k4 * k6) + "*" + u1 + \
        "*" + u2 + "*" + u3 + "*" + u4 + "+" + u6 + "+"
    U += str(k**4 * k1 * k2 * k3 * k5 * k6) + "*" + u1 + \
        "*" + u2 + "*" + u3 + "*" + u5 + "+" + u6 + "+"
    U += str(k**4 * k1 * k2 * k4 * k5 * k6) + "*" + u1 + \
        "*" + u2 + "*" + u4 + "*" + u5 + "+" + u6 + "+"
    U += str(k**4 * k1 * k3 * k4 * k5 * k6) + "*" + u1 + \
        "*" + u3 + "*" + u4 + "*" + u5 + "+" + u6 + "+"
    U += str(k**4 * k2 * k3 * k4 * k5 * k6) + "*" + u2 + \
        "*" + u3 + "*" + u4 + "*" + u5 + "+" + u6 + "+"
    U += str(k**5 * k1 * k2 * k3 * k4 * k5 * k6) + "*" + u1 + \
        "*" + u2 + "*" + u3 + "*" + u4 + "*" + u5 + "+" + u6
    return U


# def reduce(nombre):
#     return math.floor(nombre*100000000.0)/100000000.0;

def signe(nombre):
    if nombre >= 0:
        return "+" + str(nombre)
    else:
        return str(nombre)


def convert_to_text(data, x):
    if data['type'] == "exp":
        return "(" + str(round(data['a'], 8)) + "*exp(" + signe(-round(data['b'], 8)) + "*" + x + ")" + signe(round(data['c'], 8)) + ")"
    elif data['type'] == "log":
        return "(" + str(round(data['a'], 8)) + "*log(" + str(round(data['b'], 8)) + "*" + x + signe(round(data['c'], 8)) + ")" + signe(round(data['d'], 8)) + ")"
    elif data['type'] == "pow":
        return "(" + str(round(data['a'], 8)) + "*(pow(" + x + "," + str(round(1 - data['b'], 8)) + ")-1)/(" + str(round(1 - data['b'], 8)) + ")" + signe(round(data['c'], 8)) + ")"
    elif data['type'] == "quad":
        return "(" + str(round(data['c'], 8)) + "*" + x + signe(round(-data['b'], 8)) + "*pow(" + x + ",2)" + signe(round(data['a'], 8)) + ")"
    elif data['type'] == "lin":
        return "(" + str(round(data['a'], 8)) + "*" + x + signe(round(data['b'], 8)) + ")"
    elif data['type'] == "expo-power":
        return "(" + str(round(data['a'], 8)) + "+exp(" + str(round(-data['b'], 8)) + "*pow(" + x + "," + str(round(data['c'], 8)) + "))"

def convert_to_text_excel(data, x):
    if data['type'] == "exp":
        return "(" + str(round(data['a'], 8)) + "*EXP(" + signe(-round(data['b'], 8)) + "*" + x + ")" + signe(round(data['c'], 8)) + ")"
    elif data['type'] == "log":
        return "(" + str(round(data['a'], 8)) + "*LN(" + str(round(data['b'], 8)) + "*" + x + signe(round(data['c'], 8)) + ")" + signe(round(data['d'], 8)) + ")"
    elif data['type'] == "pow":
        return "(" + str(round(data['a'], 8)) + "*(" + x + "^" + str(round(1 - data['b'], 8)) + "-1)/(" + str(round(1 - data['b'], 8)) + ")" + signe(round(data['c'], 8)) + ")"
    elif data['type'] == "quad":
        return "(" + str(round(data['c'], 8)) + "*" + x + signe(round(-data['b'], 8)) + "*" + x + "^2" + signe(round(data['a'], 8)) + ")"
    elif data['type'] == "lin":
        return "(" + str(round(data['a'], 8)) + "*" + x + signe(round(data['b'], 8)) + ")"
    elif data['type'] == "expo-power":
        return "(" + str(round(data['a'], 8)) + "+EXP(" + str(round(-data['b'], 8)) + "*" + x + "^" + str(round(data['c'], 8)) + ")"

def convert_to_text_latex(data, x):
    if data['type'] == "exp":
        return "(" + str(round(data['a'], 2)) + "*e^{" + signe(-round(data['b'], 2)) + x + "}" + signe(round(data['c'], 2)) + ")"
    elif data['type'] == "log":
        return "(" + str(round(data['a'], 2)) + "\\log(" + str(round(data['b'], 2)) + x + signe(round(data['c'], 2)) + ")" + signe(round(data['d'], 2)) + ")"
    elif data['type'] == "pow":
        return "(" + str(round(data['a'], 2)) + "\\frac{" + x + "^{" + str(round(1 - data['b'], 2)) + "}-1}{" + str(round(1 - data['b'], 2)) + "}" + signe(round(data['c'], 2)) + ")"
    elif data['type'] == "quad":
        return "(" + str(round(data['c'], 2)) + x + signe(round(-data['b'], 2)) + x + "^{2}" + signe(round(data['a'], 2)) + ")"
    elif data['type'] == "lin":
        return "(" + str(round(data['a'], 2)) + x + signe(round(data['b'], 2)) + ")"
    elif data['type'] == "expo-power":
        return "(" + str(round(data['a'], 2)) + "+exp(" + str(round(-data['b'], 2)) + "*" + x + "^{" + str(round(data['c'], 2)) + "})"
