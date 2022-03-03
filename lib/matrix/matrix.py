import numpy as np

def matrice_top(n):
    # fonction qui n'est pas a moi...
    a = complex(0,0)
    b = complex(0,0)
    c = complex(1/2,1/8)
    d = complex(1,0)
    e = complex(0,0)
    res = np.zeros((n, n), np.complex_)
    # res = [[0 for j in range(n)]for i in range(n)]
    for i in range(n) : 
        for j in range(n) : 
            if(i==j ):
                res[i][j] = a
            elif(i == j-1):
                res[i][j] = b
            elif(i == j+1):
                res[i][j] = c
            elif(i == j-2):
                res[i][j] = d
            elif(i==j+2):
                res[i][j] = e
            else:
                res[i][j] = complex(0,0)
    return res