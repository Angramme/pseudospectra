import numpy as np
from collections import Counter
from cmath import phase
from scipy.linalg import eigvals
from matplotlib.patches import Arc

from lib.algo.prediction_correction import main as pcmain

def main(
    plot, 
    matrix: np.matrix, 
    eps: float,
    step: float,
    update = lambda: True, 
    progresstick =.01
    ):
    n, _ = matrix.shape

    eps = np.max(eps)
    P = plot

    def solve_max_mag_bound_intersect(theta, eps, A=matrix):
        As = A.conj().T
        mat42 = np.vstack((
            np.hstack(( 1j*np.exp(1j*theta)*As, -eps * np.eye(n)       )),
            np.hstack(( eps * np.eye(n),        1j*np.exp(-1j*theta)*A ))
        ))
        # TODO: replace with hamiltonian eigenvalue solver
        EVs42 = np.linalg.eigvals(mat42)
        mx = (float('-inf'), None, float('-inf'))
        for (ev, mul) in Counter(EVs42).most_common():
            if not np.isclose(np.real(ev), 0, rtol=1e-9): continue
            if np.imag(ev) > mx[2]:
                p = np.imag(ev)*np.exp(1j*theta)
                mx = (p, mul, np.imag(ev))
        return (mx[0], mx[1])

    def solve_circle_bound_intersect(r, eps, A=matrix):
        As = A.conj().T
        X = np.vstack((
            np.hstack((-eps*np.eye(n), A)),
            np.hstack((r*np.eye(n), np.zeros((n, n))))
        ))
        Y = np.vstack((
            np.hstack((np.zeros((n, n)), r*np.eye(n))),
            np.hstack((As, -eps*np.eye(n)))
        ))
        # evs = np.linalg.eigh((X, Y))
        # evs = [x+1j*y for (x, y) in zip(evs[0], evs[1])]
        evs = eigvals(X, Y)
        intersections = []
        for (ev, mul) in Counter(evs).most_common():
            if not np.isclose(np.abs(ev), 1): continue
            theta = phase(ev)
            intersections.append((theta, mul))
        return intersections


    def intersections_to_segments(xs, comp=np.real):
        xs = sorted(xs, key=lambda p: comp(p[0]))
        segs = []
        a = None
        for (x, m) in xs:
            if(m % 2 == 0): # degenerate point: both beginning and end of a segment!
                if(a):
                    segs.append((a, x))
                    a = x
                else:
                    segs.append((x, x))
            else:
                if(a):
                    segs.append((a, x))
                    a = None
                else:
                    a = x
        return segs

    pcmain(plot, matrix, [eps], step, update, progresstick)
    
    EVs = np.linalg.eigvals(matrix)
    lam = max(EVs, key=np.abs) # eigenvalue with greatest magnitude 
    P.scatter(lam.real, lam.imag, c="green")

    z1 = solve_max_mag_bound_intersect(phase(lam), eps)[0]

    zk = z1
    for k in range(10000):
        P.scatter(zk.real, zk.imag, c="red", s=5**2)
        r = np.abs(zk)
        ps = solve_circle_bound_intersect(r, eps)
        print(ps)
        psts = [r*np.exp(1j*x[0]) for x in ps]
        P.scatter(np.real(psts), np.imag(psts), color="black", s=3**2)
        segs = intersections_to_segments(ps, np.imag)
        for (a, b) in segs:
            if np.isclose(a, b): continue
            arc = Arc((0, 0), 2*r, 2*r, a/3.1415*180, (b-a)/3.1415*180, 0)
            P.add_patch(arc)
        mids = [(a+b)/2 for (a, b) in segs]
        psts = [r*np.exp(1j*x) for x in mids]
        P.scatter(np.real(psts), np.imag(psts), c="black", s=3**2)
        potential = list(map(
            lambda y: solve_max_mag_bound_intersect(y, eps)[0],
            mids))
        if len(potential) == 0: break
        zk1 = max(potential)
        if np.isclose(zk1, zk, rtol=1e-9):
            zk = zk1
            break
        zk = zk1

    P.scatter(zk.real, zk.imag, c="violet", s=5**2)

