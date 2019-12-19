import numpy as np
from sympy import *
from scipy.optimize import fsolve



def calculk6(k1,k2,k3,k4,k5,k6):
    k = symbols('k')
    a=k1*k2*k3*k4*k5*k6
    b=(k1*k2*k3*k5*k6 + k1*k2*k3*k4*k5 + k1*k2*k4*k5*k6 + k2*k3*k4*k5*k6 + k1*k3*k4*k5*k6 + k1*k2*k3*k4*k6)
    c=(k1*k2*k3*k5 + k1*k2*k4*k5 + k2*k3*k4*k5 + k1*k3*k4*k5 + k1*k2*k3*k4 + k1*k2*k3*k6 + k1*k2*k4*k6 + k1*k2*k5*k6 + k1*k3*k4*k6 + k1*k3*k5*k6 + k1*k4*k5*k6 + k2*k3*k4*k6 + k2*k3*k5*k6  + k2*k4*k5*k6 + k3*k4*k5*k6)
    d=(k1*k2*k3 + k1*k2*k4 + k1*k2*k5 + k1*k3*k4 +k1*k3*k5 + k1*k4*k5 + k2*k3*k4 + k2*k3*k5 + k2*k4*k5 + k3*k4*k5 + k3*k4*k6 + k1*k2*k6 + k1*k3*k6 + k1*k4*k6 + k1*k5*k6 + k3*k4*k6 + k3*k5*k6 + k2*k4*k6 + k2*k5*k6 + k4*k5*k6)
    e=(k2*k3 + k1*k3 + k1*k4 + k1*k6 + k1*k5 + k1*k2 + k2*k4 + k3*k4 + k2*k5 + k3*k5 + k4*k5 + k2*k6 + k3*k6 + k4*k6 + k5*k6)
    f= k1+k2+k3+k4+k5+k6-1
    p_k=lambda k: a*k**5+b*k**4+c*k**3+d*k**2+e*k+f
    
    solutions=fsolve(p_k, 0, xtol=1.49012e-08, maxfev=100000000)
    return (solutions[0])
    

##def utilite(k1,k2,k3,k4,k):
##    	u1=u1.get()
##    	u2=u2.get()
##    	u3=u3.get()    
##	u4=u4.get()
##	u5=u5.get()
##	u6=u6.get()
##   	U= k**5*k1*k2*k3*k4*k5*k6 + k**4(k1*k2*k3*k5*k6*u1*u2*u3*u5*u6 + k1*k2*k3*k4*k5*u1*u2*u3*u4*u5 + k1*k2*k4*k5*k6*u1*u2*u4*u5*u6 + k2*k3*k4*k5*k6*u2*u3*u4*u5*u6 + k1*k3*k4*k5*k6*u1*u3*u4*u5*u6 + k1*k2*k3*k4*k6*u1*u2*u3*u4*u6) +  k^3(k1*k2*k3*k5*u1*u2*u3*u5 + k1*k2*k4*k5*u1*u2*u4*u5 + k2*k3*k4*k5*u2*u3*u4*u5 + k1*k3*k4*k5*u1*u3*u4*u5 + k1*k2*k3*k4*u1*u2*u3*u4 + k1*k2*k3*k6*u1*u2*u3*u6 + k1*k2*k4*k6*u1*u2*u4*u6 + k1*k2*k5*k6*u1*u2*u5*u6 + k1*k3*k4*k6*u1*u3*u4*u6 + k1*k3*k5*k6*u1*u3*u5*u6 + k1*k4*k5*k6*u1*u4*u5*u6 + k2*k3*k4*k6*u2*u3*u4*u6 + k2*k3*k5*k6*u2*u3*u5*u6  + k2*k4*k5*k6*u2*u4*u5*u6 + k3*k4*k5*k6*u3*u4*u5*u6) + k**(k1*k2*k3*u1*u2*u3 + k1*k2*k4*u1*u2*u4 + k1*k2*k5*u1*u2*u5 + k1*k3*k4*u1*u3*u4 +k1*k3*k5*u1*u3*u5 + k1*k4*k5*u1*u4*u5 + k2*k3*k4*u2*u3*u4 + k2*k3*k5*u2*u3*u5 + k2*k4*k5*u2*u4*u5 + k3*k4*k5*u3*u4*u5 + k3*k4*k6*u3*u4*u6 + k1*k2*k6*u1*u2*u6 + k1*k3*k6*u1*u3*u6 + k1*k4*k6*u1*u4*u6 + k1*k5*k6*u1*u5*u6 + k3*k4*k6*u3*u4*u6 + k3*k5*k6*u3*u5*u6 + k2*k4*k6*u2*u4*u6 + k2*k5*k6*u2*u5*u6 + k4*k5*k6*u4*u5*u6) + k*(k2*k3*u2*u3 + k1*k3*u1*u3 + k1*k4*u1*u4 + k1*k6*u1*u6 + k1*k5*u1*u5 + k1*k2*u1*u2 + k2*k4*u2*u4 + k3*k4*u3*u4 + k2*k5*u2*u5 + k3*k5*u3*u5 + k4*k5*u4*u5 + k2*k6*u2*u6 + k3*k6*u3*u6 + k4*k6*u4*u6 + k5*k6*u5*u6) + k1*u1 +k2*u2 +k3*u3 +k4*u4 +k5*u5 +k6*u6
##
##	return (U)





