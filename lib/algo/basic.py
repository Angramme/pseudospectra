import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.figure as fig

def contours(figure, matrix: np.matrix, eps: np.array, step: float =0.5, onprogress =None, progresstick =.01):
    # 1 find the search grid area
    # 1.1 apply the extended Gershgorins Disc theorem to A to find all discs
    # 1.2 find the boudning rectangle
    lb = +math.inf # left bound
    rb = -math.inf # right bound
    tb = -math.inf # top bound
    bb = +math.inf # bottom bound

    A = matrix
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
        
    # 2 calculate sigmin grid     
    sigmin = np.zeros((
        math.ceil((rb-lb)/step), 
        math.ceil((tb-bb)/step)))
    
    xx = np.linspace(lb, rb, sigmin.shape[0])
    yy = np.linspace(bb, tb, sigmin.shape[1])
    xv, yv = np.meshgrid(xx, yy)

    P_total = sigmin.shape[0]*sigmin.shape[1]
    P_step  = round(P_total*progresstick)
    P_stotal = P_total/P_step
    P_count = 0
    P_scount = 0
    P_pprog = 0

    for i, p in enumerate(xx):
        for j, q in enumerate(yy):
            _, s, _ = np.linalg.svd((p+q*1j) * np.eye(n) -A)
            sigmin[j, i] = np.min(s)
            if onprogress:
                P_count += 1
                P_scount = P_count // P_step
                prog = P_scount / P_stotal
                if prog != P_pprog:
                    if not onprogress(prog):
                        return None
                    P_pprog = prog

    # F = fig.Figure(figsize=sigmin.shape, dpi=100)
    F = figure
    P = F.add_subplot()
    P.set_aspect(1)

    P.contour(xv, yv, sigmin, levels=eps)
    
    EVs = np.linalg.eig(A)[0]
    P.scatter(EVs.real, EVs.imag)
    
    Re = plt.Rectangle((lb, bb), rb-lb, tb-bb, alpha=1, facecolor='none', edgecolor='red')
    P.add_patch(Re)

    return F

if __name__ == "__main__":
    # basic(matrice_top(64), [10**-7], step=0.07)
    # basic(matrice_top(64), [10**(-i) for i in range(7, 2, -1)], step=0.035)
    # contours(matrice_top(64), [10**(-7)], step=0.005)
    pass