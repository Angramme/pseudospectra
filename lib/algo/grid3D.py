import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib import cm
from lib.math import gershgorin_norm, ssvd_min

def init_figure(figure):
    plot = figure.add_subplot(111, projection='3d')
    return plot

def main(
    plot, 
    matrix: np.matrix, 
    eps: np.array, 
    step: float =0.5, 
    update = lambda: True, 
    rstride = None,
    cstride = None,
    progresstick =.01):

    
    A = matrix
    n, _ = A.shape
    
    # 1 find the search grid area
    # 1.1 apply the extended gershgorins Disc theorem to A to find all discs
    # 1.2 find the boudning rectangle
    lb, rb, bb, tb = gershgorin_norm(matrix, np.max(eps))
    if not update((0.01,)): return None

    print(lb, rb, bb, tb)
    print(math.ceil((rb-lb)/step), math.ceil((tb-bb)/step))
        
    # 2 calculate sigmin grid
    sigmin = None
    try:
        sigmin = np.zeros((
            math.ceil((rb-lb)/step), 
            math.ceil((tb-bb)/step)))
    except:
        print("Couldn't allocate the grid!")
        return None

    xx = np.linspace(lb, rb, sigmin.shape[1])
    yy = np.linspace(bb, tb, sigmin.shape[0])
    xv, yv = np.meshgrid(xx, yy)

    P_total = sigmin.shape[0]*sigmin.shape[1]
    P_step  = math.ceil(P_total*progresstick)
    P_stotal = P_total/P_step
    P_count = 0
    P_scount = 0
    P_pprog = 0

    for i, p in enumerate(xx):
        for j, q in enumerate(yy):
            sigmin[j, i] = ssvd_min((p+q*1j) * np.eye(n) -A)

            P_count += 1
            P_scount = P_count // P_step
            prog = P_scount / P_stotal
            if prog != P_pprog:
                if not update((prog,)): return None
                P_pprog = prog

    P = plot
    strides = {}
    if rstride: strides["rstride"] = rstride
    if cstride: strides["cstride"] = cstride
    P.plot_surface(xv, yv, 1/sigmin, cmap=cm.coolwarm, linewidth=0, **strides)
    # plt.title('z as 3d height map')    
    # Re = plt.Rectangle((lb, bb), rb-lb, tb-bb, alpha=1, facecolor='none', edgecolor='red')
    # P.add_patch(Re)