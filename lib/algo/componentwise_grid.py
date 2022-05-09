import numpy as np
import math
import matplotlib.pyplot as plt
from lib.math import gershgorin_componentwise, ssvd_min


def main(
    figure, 
    matrix: np.matrix, 
    eps: np.array, 
    E: np.matrix = None,
    step: float =0.5, 
    update = lambda: True, 
    progresstick =.01):

    A = matrix
    n, _ = A.shape
    if not E: E = 1/n * np.ones((n, n))
    assert(A.shape == E.shape)
    
    # 1 find the search grid area
    # 1.1 apply the extended gershgorins Disc theorem to A to find all discs
    # lb, rb, bb, tb = gershgorin_componentwise(A, E, np.max(eps)/((3+np.sqrt(2))*n))
    lb, rb, bb, tb = gershgorin_componentwise(A, E, np.max(eps))
    # lb, rb, bb, tb = gershgorin_componentwise(A, E, np.max(eps))
    if not update((0.01,)): return None

    print(lb, rb, bb, tb)
    print(math.ceil((rb-lb)/step), math.ceil((tb-bb)/step))
        
    # 2 calculate grid 
    grid = None
    try:
        grid = np.zeros((
            math.ceil((rb-lb)/step), 
            math.ceil((tb-bb)/step)))
    except:
        print("Warning couldn't allocate the grid! ")
        return None


    xx = np.linspace(lb, rb, grid.shape[1])
    yy = np.linspace(bb, tb, grid.shape[0])
    xv, yv = np.meshgrid(xx, yy)

    P_total = grid.shape[0]*grid.shape[1]
    P_step  = math.ceil(P_total*progresstick)
    P_stotal = P_total/P_step
    P_count = 0
    P_scount = 0
    P_pprog = 0

    for i, p in enumerate(xx):
        for j, q in enumerate(yy):
            Al = A - (p+q*1j)*np.eye(n)
            Ali = np.linalg.inv(Al)
            X = np.abs(Ali)
            Y = np.matmul(X, E)
            P = np.max(np.abs(np.linalg.eigvals(Y)))

            grid[j, i] = 1/P

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

    # P.imshow(grid.T, extent=(lb, rb, bb, tb), cmap='hot', interpolation='nearest')
    
    EVs = np.linalg.eig(A)[0]
    P.scatter(EVs.real, EVs.imag)
    
    Re = plt.Rectangle((lb, bb), rb-lb, tb-bb, alpha=1, facecolor='none', edgecolor='red')
    P.add_patch(Re)

    return F