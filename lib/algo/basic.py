from asyncio.windows_events import NULL
import numpy as np
import math
import matplotlib.pyplot as plt


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
    

def basic(A: np.matrix, eps: np.array, step: float =0.5):
    # 1 find the search grid area
    # 1.1 apply the extended Gershgorins Disc theorem to A to find all discs
    # 1.2 find the boudning rectangle
    lb = +math.inf # left bound
    rb = -math.inf # right bound
    tb = -math.inf # top bound
    bb = +math.inf # bottom bound

    n, _ = A.shape
    nsqrt = np.sqrt(n)
    epsmax = np.max(eps)

    for i in range(n):
        a = A[i, i]
        rA = np.sum(np.abs(A[i])) - np.abs(A[i, i])
        r = nsqrt * epsmax + rA
        lb = min(lb, a.real-r)
        rb = max(rb, a.real+r)
        bb = min(bb, a.imag-r)
        tb = max(tb, a.imag+r)

    lb = -0.3
    rb = 0.3
    bb = -0.3
    tb = 0.3

    # 2 calculate sigmin grid     
    sigmin = np.zeros((
        math.ceil((rb-lb)/step), 
        math.ceil((tb-bb)/step)))
    
    xx = np.linspace(lb, rb, sigmin.shape[0])
    yy = np.linspace(bb, tb, sigmin.shape[1])
    xv, yv = np.meshgrid(xx, yy)

    for i, p in enumerate(xx):
        for j, q in enumerate(yy):
            _, s, _ = np.linalg.svd((p+q*1j) * np.eye(n) -A)
            sigmin[j, i] = np.min(s)

    # if len(eps) > 1:
    plt.contour(xv, yv, sigmin, levels=eps)
    # else:
    #     plt.contour(xv, yv, sigmin)
    Xs = np.linalg.eig(A)[0]
    plt.scatter(Xs.real, Xs.imag)
    R = plt.Rectangle((lb, bb), rb-lb, tb-bb, alpha=1, facecolor='none', edgecolor='red')
    plt.gca().add_patch(R)
    print(xv.shape)
    # plt.grid(color='gray', linestyle='-')
    plt.show()



# C = complex
# A = np.matrix([
#     [1, 2, 3, 4],
#     [5, C(6, 3), 7, 8], 
#     [9, 10, 11, 12],
#     [13, 14, 15, 16]
# ])
# basic(A, 0.5)

# basic(matrice_top(64), [10**-7], step=0.07)
# basic(matrice_top(64), [10**(-i) for i in range(7, 2, -1)], step=0.035)
basic(matrice_top(64), [10**(-7)], step=0.005)