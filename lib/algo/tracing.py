import numpy as np
from lib.math import ssvd_min, svd_min
from matplotlib.figure import Figure

def contours(
    figure: Figure, 
    matrix: np.matrix, 
    eps: np.array, 
    step: float = 0.5, 
    update = lambda: True, 
    progresstick = .01):

    P = figure.add_subplot()
    P.set_aspect(1)

    EVs = np.linalg.eig(matrix)[0]
    P.scatter(EVs.real, EVs.imag, c="green")

    for i, E in enumerate(eps):
        def up(t):
            p, *ts = t
            return update(((p + i)/len(eps), *ts))
        trace_one(
            plot=P,
            matrix=matrix, 
            eps=E, 
            tol=10e-5,
            update=up, 
            )
    
    return figure

def trace_one(
    plot, 
    matrix: np.matrix, 
    eps: float, 
    tol: float,
    update = lambda: True, 
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

    # find z_1
    EVs = np.linalg.eig(A)[0]
    plot.scatter(EVs[0].real, EVs[0].imag, c="yellow")
    
    def find_z1():
        lam0 = EVs[0]
        d0 = 1j

        theta1n = eps
        z1n = lam0 + theta1n*d0
        uz1n, gz1n, vhz1n = g(z1n)
        while abs(gz1n - eps)/eps > tol:
            if not update((.3*(abs(abs(gz1n - eps)/eps-tol)/tol),)): return None
            z1o = z1n
            uz1o, gz1o, vhz1o = uz1n, gz1n, vhz1n

            theta1n = -(gz1o-eps)/np.real(
                np.conj(d0)*np.vdot(vhz1o, uz1o)
                )
            # print("theta1n : {} | eps : {}".format(theta1n, eps))
            z1n = z1o + theta1n*d0
            # plot.scatter(z1n.real, z1n.imag, marker="+", c="green")

            uz1n, gz1n, vhz1n = g(z1n)
        return z1n, uz1n, gz1n, vhz1n

    z_o, u_min_o, s_o, vh_min_o = find_z1()
    z_og = z_o
    if not update((.3,)): return None

    plot.scatter(z_o.real, z_o.imag, s=7**2, marker="x", c="red")

    boundary_x = []
    boundary_y = []

    prev_side = 0
    switch_cnt = 0

    for _ in range(65*3):
        ## Prediction
        r = 1j * np.vdot(vh_min_o, u_min_o) / np.abs(np.vdot(vh_min_o, u_min_o))
        tau = eps*.03 # TODO: ?? find better tau lol
        apx_z_n = z_o + tau*r

        ## Correction
        u_min_n, s_n, v_min_n = g(apx_z_n)
        z_n = apx_z_n - (s_n-eps)/(np.vdot(u_min_n.conj(), v_min_n.conj()))

        z_o, u_min_o, s_o, vh_min_o = z_n, u_min_n, s_n, v_min_n

        # TODO: find a better stopping criterion
        # if np.abs(z_og-z_o) < tau*.5: break
        side = 1 if z_o-z_og > 0 else -1
        if side != prev_side: switch_cnt += 1
        prev_side = side 
        if switch_cnt >= 3: break

        boundary_x.append(z_n.real)
        boundary_y.append(z_n.imag)
        # plot.scatter(z_n.real, z_n.imag, s=7**2, marker="o", c="blue")

    plot.plot(boundary_x, boundary_y, linestyle='-', color='blue')
