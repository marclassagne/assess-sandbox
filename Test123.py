import numpy as np

donnee = {"5":0.03,"2.5":0.93,"7.5":0.17}

X=donnee.values()
Y=donnee.keys()
X=map(float,X)
points = np.stack((X,Y), axis = 1).tolist()
print(X)
print(points)
