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
            progresstick=progresstick
            )
    
    return figure

def trace_one(
    plot, 
    matrix: np.matrix, 
    eps: float, 
    tol: float,
    update = lambda: True, 
    progresstick =.01,
    ):
    """
    :param tol: relative accuracy of the first point
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
    # lam0 = np.random.choice(EVs)
    # lam_mid = np.average(EVs)

    d0 = 1j
    # d0 = lam0-lam_mid
    # d0 /= np.abs(d0)
    
    lam0 = EVs[0]
    
    theta1n = eps
    z1n = lam0 + theta1n*d0
    uz1n, gz1n, vhz1n = g(z1n)
    
    print(uz1n, gz1n, vhz1n)
    print(abs(gz1n - eps)/eps, tol)
    while abs(gz1n - eps)/eps > tol:
        if not update((.1,)): return None
        z1o = z1n
        uz1o, gz1o, vhz1o = uz1n, gz1n, vhz1n

        theta1n = -(gz1o-eps)/np.real(
            np.conj(d0)*np.vdot(vhz1o, uz1o)
            )
        print("theta1n : {} | eps : {}".format(theta1n, eps))
        z1n = z1o + theta1n*d0
        plot.scatter(z1n.real, z1n.imag, marker="+", c="green")

        uz1n, gz1n, vhz1n = g(z1n)

    z_1 = z1n
    plot.scatter(z_1.real, z_1.imag, s=7**2, marker="x", c="red")

    update((.3,))

