donnee = {"5":0.03,"2.5":0.93,"7.5":0.17}

def conv(d):
    k=0
    for key in d:
        print(d[key])
        k+=1
        print(k)

  
print(conv(donnee))
