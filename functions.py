import numpy as np


def funcexp(x, a, b, c):			# function for the exponential regression
    return a * np.exp(-b * x) + c


def funcquad(x, a, b, c):			# function for the quadratic regression
    return c * x - b * x**2 + a


def funcpuis(x, a, b, c):			# function for the puissance regression
    return a * ((x**(1 - b) - 1) / (1 - b)) + c


def funclog(x, a, b, c, d):			# function for the logarithmic regression
    return a * np.log(b * x + c) + d


def funclin(x, a, b):				# function for the linear regression
    return a * x + b


def funcexpopower(x, a, b, c):             # function for the expo-power regression
    return a + np.exp(-b * x**c)


# Fonctions parametrees pour avoir U(xmin)=0 et U(xmax)=1
def funcexp2(x, b, min, max):
    return (1. / (np.exp(-b * max) - np.exp(-b * min))) * np.exp(-b * x) + (1. / (1 - np.exp(b * (min - max))))


def funcquad2(x, b, min, max):
    return ((1 + b * (max**2 - min**2)) / (max - min)) * x - b * x**2 + b * min**2 - min * ((1 + b * (max**2 - min**2)) / (max - min))


def funcpuis2(x, b, min, max):
    return ((1 - b) / (max**(1 - b) - min**(1 - b))) * ((x**(1 - b) - 1) / (1 - b)) - (min**(1 - b) - 1) / (max**(1 - b) - min**(1 - b))


def funclog2(x, b, c, min, max):
    return (1. / (np.log(np.abs(b * max + c)) - np.log(np.abs(b * min + c)))) * np.log(np.abs(b * x + c)) + 1. / (1 - np.log(np.abs(b * max + c)) / np.log(np.abs(b * min + c)))


def funcexpopower2(x, a, min, max):
    return (a + np.exp(np.log(-a) * (x / min)**(np.log(np.log(1 - a) / np.log(-a)) / np.log(max / min))))


# Fonctions utilisees pour l'export Excel
def funcexp_excel(x, a, b, c):
    return "="+a+"*EXP(-"+b+"*"+x+")+"+c


def funcquad_excel(x, a, b, c):
    return "="+c+"*"+x+"-"+b+"*"+x+"^2+"+a


def funcpuis_excel(x, a, b, c):
    return "="+a+"*("+x+"^(1-"+b+")-1)/(1-"+b+")+"+c


def funclog_excel(x, a, b, c, d):
    return "="+a+"*LOG("+b+"*"+x+"+"+c+")+"+d


def funclin_excel(x, a, b):
    return "="+a+"*"+x+"+"+b


def funcexpopower_excel(x, a, b, c):
    return "="+a+"+EXP(-"+b+"*"+x+"^"+c+")"
