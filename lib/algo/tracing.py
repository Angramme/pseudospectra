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
    P.scatter(EVs.real, EVs.imag)

    for i, E in enumerate(eps):
        def up(t):
            p, *ts = t
            return update(((p + i)/len(eps), *ts))
        trace_one(
            plot=P,
            matrix=matrix, 
            eps=E, 
            tol=0.1,
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
        v = svd_min(pg(x))
        if v[1].real < 0 or v[1].imag != 0:
            print("WARNING: v < 0 or v.imag != 0] failed!")
        return v

    # find z_1
    EVs = np.linalg.eig(A)[0]
    # lam0 = np.random.choice(EVs)
    # lam_mid = np.average(EVs)

    d0 = 1j
    # d0 = lam0-lam_mid
    # d0 /= np.abs(d0)
    
    lam0 = EVs[0]
    
    theta1n = eps
    z1n = lam0 + theta1n*d0
    uz1n, gz1n, vhz1n = g(z1n)

    point, = plot.plot(z1n.real, z1n.imag, marker="x", c="red")
    
    while abs(gz1n - eps)/eps > tol:
        if not update((.1,)): return None
        z1o = z1n
        uz1o, gz1o, vhz1o = uz1n, gz1n, vhz1n

        theta1n = -(gz1o-eps)/np.real(np.conj(d0)*np.dot(vhz1o, uz1o))
        # theta1n = np.random.random()
        print("theta1n : {} | eps : {}".format(theta1n, eps))
        z1n = lam0 + theta1n*d0
        point.set_data(z1n.real, z1n.imag)

        uz1n, gz1n, vhz1n = g(z1n)

    z_1 = z1n
    # plot.scatter(z_1.real, z_1.imag, s=7**2, marker="x", c="red")

    update((.3,))

