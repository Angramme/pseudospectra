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

def kohan(n, c, s):
    return np.array(
        [[1] + [-c]*(n-1)] +
        [
            [0]*(i) + [s**i] + [-(s**i) * c for _ in range(i+1, n)]
            for i in range(1, n)
        ])

def diagonal(arr):
    n = len(arr)
    return np.array([
        [0]*i + [arr[i]] + [0]*(n-i-1)
        for i in range(n)
    ])