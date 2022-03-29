import numpy as np
import math
import matplotlib.pyplot as plt
from lib.math import gershgorin, ssvd_min


def contours(
    figure, 
    matrix: np.matrix, 
    eps: np.array, 
    E: np.matrix = None,
    step: float =0.5, 
    update = lambda: True, 
    progresstick =.01):

    # 1 find the search grid area
    # 1.1 apply the extended Gershgorins Disc theorem to A to find all discs
    # 1.2 find the boudning rectangle
    A = matrix
    n, _ = A.shape

    if not E: E = np.ones((n, n))
    # if not E: E = np.eye(n)

    assert(A.shape == E.shape)
    
    # lb, rb, bb, tb = gershgorin(A, n*(3+np.sqrt(2))*np.max(eps))
    lb, rb, bb, tb = -1, 2, -1, 2
    if not update((0.01,)): return None
        
    # 2 calculate grid 
    grid = np.zeros((
        math.ceil((rb-lb)/step), 
        math.ceil((tb-bb)/step)))
    
    xx = np.linspace(lb, rb, grid.shape[1])
    yy = np.linspace(bb, tb, grid.shape[0])
    xv, yv = np.meshgrid(xx, yy)

    P_total = grid.shape[0]*grid.shape[1]
    P_step  = math.ceil(P_total*progresstick)
    P_stotal = P_total/P_step
    P_count = 0
    P_scount = 0
    P_pprog = 0

    print(grid.shape)
    for i, p in enumerate(xx):
        for j, q in enumerate(yy):
            # grid[j, i] = ssvd_min((p+q*1j) * np.eye(n) -A)
            Al = A - (p+q*1j)*np.eye(n)
            Ali = np.linalg.inv(Al)
            X = np.abs(Ali)
            Y = np.matmul(X, E)
            P = np.max(np.abs(np.linalg.eigvals(Y)))

            grid[j, i] = P

            # progress updates
            P_count += 1
            P_scount = P_count // P_step
            prog = P_scount / P_stotal
            if prog != P_pprog:
                if not update((prog,)): return None
                P_pprog = prog

    F = figure
    P = F.add_subplot()
    P.set_aspect(1)

    P.contour(xv, yv, grid, levels=eps)
    # P.contour(xv, yv, grid)

    # P.imshow(grid.T, extent=(lb, rb, bb, tb), cmap='hot', interpolation='nearest')
    
    EVs = np.linalg.eig(A)[0]
    P.scatter(EVs.real, EVs.imag)
    
    Re = plt.Rectangle((lb, bb), rb-lb, tb-bb, alpha=1, facecolor='none', edgecolor='red')
    P.add_patch(Re)

    return F