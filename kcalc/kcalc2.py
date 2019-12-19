import numpy as np
from sympy import *

def calculk2(k1,k2):
    k = symbols('k')
    solution=solve(k1*k2*k+k1+k2-1,k)
    return (solution[0])


def utilite(k1,k2,k):
    u1=u1.get()
    u2=u2.get()
    U=k*k1*k2*u1*u2+k1*u1+k2*u2
    return (U)
