# -*- coding: utf-8 -*-
"""
Created on Wed Nov 17 16:14:36 2021

@author: Guedj Yossef
"""
import matplotlib.pyplot as plt

from scipy.optimize import curve_fit


x=np.array([50,60,70,80,80,100])
y=np.array([0.5,0.5,0.7,0.9,0.95,1])

def logistique(x, K, a, r, d):
    """ Fonction logistique (Verhulst)
    Paramètres K, a, r.
    Voir : https://fr.wikipedia.org/wiki/Fonction_logistique_(Verhulst)
    """
    logi = K * np.log(a *x + r) + d
    #logi = K * np.exp(a *x + r) + d

    #logi = K*x**3+a*x**2+r*x+d
    return logi

t=np.linspace(0,100,1000)


#plt.plot(x, y, color="yellow", label="y")

""" Ajouter du bruit (Gaussian distribution) 
pour simuler les données expérimentales.
"""
#noise = 1.10 * np.random.normal(size=len(y))
#y_noise = y + noise

plt.scatter(x, y, s=5, c="red", label="point")

""" Curve Fit """
init_vals = [10, 1, 0.1,100]  # for [K, a, r]
best_vals, covar = curve_fit(logistique, x, y, p0=init_vals)
print('best_vals: {}'.format(best_vals))

print(best_vals)
y_fit = logistique(t, best_vals[0], best_vals[1], best_vals[2],best_vals[3])

y_fit_premium= (y_fit-y_fit[0])/(y_fit[-1]-y_fit[0])


print('a',logistique(50, best_vals[0], best_vals[1], best_vals[2],best_vals[3]))
print('a',logistique(100, best_vals[0], best_vals[1], best_vals[2],best_vals[3]))
# print(t)
print(y_fit_premium)
plt.plot(t, y_fit, label="y_fit")

plt.plot(t, y_fit_premium, label="y_fit_premium")

plt.legend()
plt.grid()
#plt.show()