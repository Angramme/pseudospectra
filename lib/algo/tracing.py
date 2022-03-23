from functools import partial
import numpy as np
from lib.math import svd_min, segment_point_distance as segment_d, SegmentGrid, gershgorin
from matplotlib.figure import Figure


def contours(
    figure: Figure, 
    matrix: np.matrix, 
    eps: np.array, 
    step: float, 
    update = lambda: True, 
    progresstick = .01):

    P = figure.add_subplot()
    P.set_aspect(1)

    EVs = np.linalg.eig(matrix)[0]
    P.scatter(EVs.real, EVs.imag, c="green")

    # tau = step*min(eps)
    tau = step if step else 0.5*min(eps) 

    lb, rb, bb, tb = gershgorin(matrix, np.max(eps))

    for i, E in enumerate(eps):
        # bounds = []
        # def is_bound(z):
        #     for B in bounds:
        #         # iterate over bound segments
        #         for i, a in enumerate(B):
        #             b = B[(i+1)%len(B)]
        #             if segment_d(a, b, z) < step: return True
        #     return False

        sg = SegmentGrid(lb, rb, bb, tb, (rb-lb)/10, tau*3.)
        def is_bound(z):
            return sg.is_segment(z)

        for j, Lam in  enumerate(EVs):
            def up(t):
                p, *ts = t
                progress = (max(min(p, 0), 1) + len(EVs)*i + j)/(len(eps)*len(EVs))
                return update((progress, *ts))
            
            bound = trace_one(
                plot=P,
                matrix=matrix, 
                eps=E, 
                tol=1e-2,
                # tau=0.01,
                tau=tau,
                lam0=Lam,
                update=up, 
                is_bound_f=is_bound
                )
            if not isinstance(bound, list): return None
            # if len(bound) > 0: bounds.append(bound)
            if len(bound) > 0: sg.insert_segment(bound)
    
    return figure

def trace_one(
    plot, 
    matrix: np.matrix, 
    eps: float, 
    tol: float,
    tau: float,
    lam0: complex,
    update = lambda: True, 
    is_bound_f = None,
    ):
    """
    :param tol: float : relative accuracy of the first point
    """

    An = matrix.shape[0]
    A = matrix
    def pg(x):
        return x * np.eye(An) - A
    def g(x):
        return svd_min(pg(x))
    
    def find_z1_d(d0=1j):
        theta1n = eps
        z1n = lam0 + theta1n*d0
        uz1n, gz1n, vhz1n = g(z1n)
        it = 0
        while abs(gz1n - eps)/eps > tol:
            if not update((.15*(abs(abs(gz1n - eps)/eps-tol)/tol),)): return "exit"
            z1o = z1n
            uz1o, gz1o, vhz1o = uz1n, gz1n, vhz1n

            theta1n = -(gz1o-eps)/np.real(
                np.conj(d0)*np.vdot(vhz1o.conj(), uz1o)
                )
            z1n = z1o + theta1n*d0

            uz1n, gz1n, vhz1n = g(z1n)

            it += 1
            if it > 100:
                return None
        
        return z1n, uz1n, gz1n, vhz1n

    def find_z1(N):
        ## if we weren't able to find the staring point,
        ## we retry with a sligthly different rotation
        for i in range(N):
            d0 = np.exp(np.pi*2*(i/N))
            val = find_z1_d(d0)
            if val == "exit": return None
            if val: return val
        print("couldn't find a suitable direction")
        return None

    _find_z1 = find_z1(8)
    if not _find_z1: return None
    z_o, u_min_o, s_o, vh_min_o = _find_z1
    z_og = z_o
    if is_bound_f and is_bound_f(z_og): return []
    if not update((0.15,)): return None
    plot.scatter(z_o.real, z_o.imag, s=4.5**2, marker="x", c="red")

    boundary = [z_og]

    stop_armed = False

    while True:
        ## Prediction
        r = 1j * np.vdot(vh_min_o.conj(), u_min_o) / np.abs(np.vdot(vh_min_o.conj(), u_min_o))
        apx_z_n = z_o + tau*r

        ## Correction
        u_min_n, s_n, vh_min_n = g(apx_z_n)
        z_n = apx_z_n - (s_n-eps)/(np.vdot(u_min_n, vh_min_n.conj()))

        z_o, u_min_o, s_o, vh_min_o = z_n, u_min_n, s_n, vh_min_n

        boundary.append(z_n)

        ## Stopping
        if min([np.abs(z-z_n) for z in boundary[0:4]]) < tau*.5:
            if stop_armed: break
        else:
            stop_armed = True

        ## Progress
        v = z_n-lam0
        a = np.arctan2(v.real, v.imag)
        p = -.5*a/np.pi if a < 0 else .5+.5*(np.pi-a)/np.pi
        if not update((.15 + .85*p,)): return None

    plot.plot(np.real(boundary), np.imag(boundary), linestyle='-', color='blue')
    return boundary
