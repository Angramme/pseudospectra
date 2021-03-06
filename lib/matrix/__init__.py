import numpy as np

def pentadiagonal_toeplitz(n: "int", 
    x: "complex" = 0+0j, 
    y: "complex" = 0+0j, 
    z: "complex" = 0.5+(1/8)*1j, 
    v: "complex" = 1+0j, 
    w: "complex" = 0+0j
    ):
    res = np.array([[0+0j for j in range(n)]for i in range(n)])
    for i in range(n) : 
        for j in range(n): 
            if(i==j ):
                res[i][j] = x
            elif(i == j-1):
                res[i][j] = y			
            elif(i == j+1):
                res[i][j] = z
            elif(i == j-2):
                res[i][j] = v
            elif(i==j+2):
                res[i][j] = w
            else:
                res[i][j] = complex(0,0)
    return res

    V = [w, z, x, y, v]
    return np.array([
        [(V[j-i + 2] if 0<= j-i + 2 <5 else 0+0j) for j in range(n)]
        for i in range(n)
    ])

def kahan(n: "int", c: "complex", s: "complex"):
    return np.array(
        [[1] + [-c]*(n-1)] +
        [
            [0]*(i) + [s**i] + [-(s**i) * c for _ in range(i+1, n)]
            for i in range(1, n)
        ])

def diagonal(arr: "list[complex]"):
    n = len(arr)
    return np.array([
        [0]*i + [arr[i]] + [0]*(n-i-1)
        for i in range(n)
    ])

def diagonal_jordan(n: "int"):
    # mutliplicite de Jordan
    return np.array([
        [0]*i + [-0.08*i + i*1j] + [1*np.log(1.7+.6*i)]*min(1, n-i-1) + [0]*max(0, n-i-2)
        for i in range(n)
    ])