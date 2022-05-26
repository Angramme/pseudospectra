import numpy as np
from collections import Counter
from lib.math import ssvd_min
from lib.utils import flat_map

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

    meps = np.max(eps)
    P = plot

    def solve_ver_bound_intersect(c, meps, A=matrix):
        if not np.isclose(c, np.real(c)): return None
        As = A.conj().T
        mat42 = np.vstack((
            np.hstack(( c * np.eye(n) - As, -meps * np.eye(n)   )),
            np.hstack(( meps * np.eye(n),     A - c * np.eye(n) ))
        ))
        # TODO: replace with hamiltonian eigenvalue solver
        EVs42 = np.linalg.eigvals(mat42)
        intersections = []
        for (ev, mul) in Counter(EVs42).most_common():
            if not np.isclose(np.real(ev), 0, rtol=1e-9): continue
            p = c + ev
            sm = ssvd_min(p*np.eye(n) - A) # find min svd
            if not np.isclose(sm, meps, rtol=1e-9): continue 
            intersections.append((p, mul))
        return intersections

    def solve_max_hor_bound_intersect(c, meps, A=matrix):
        if not np.isclose(c, 1j*np.imag(c)): return None
        As = A.conj().T
        mat42 = np.vstack((
            np.hstack(( c * np.eye(n) + As, meps * np.eye(n)   )),
            np.hstack(( meps * np.eye(n),     A - c * np.eye(n) ))
        ))
        # TODO: replace with hamiltonian eigenvalue solver
        EVs42 = np.linalg.eigvals(mat42)
        mx = (float('-inf'), None, float('-inf'))
        for (ev, mul) in Counter(EVs42).most_common():
            if not np.isclose(np.imag(ev), 0): continue
            if np.real(ev) > mx[2]:
                p = c + ev
                mx = (p, mul, np.real(ev))
        return (mx[0], mx[1])

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

    pcmain(plot, matrix, [meps], step, update, progresstick)

    EVs = np.linalg.eigvals(matrix)
    lam = max(EVs, key=np.real) # rightmost eigenvalue
    P.scatter(lam.real, lam.imag, c="green")

    z1 = solve_max_hor_bound_intersect(1j*np.imag(lam), meps)[0]

    P.scatter(np.real(z1), np.imag(z1), color="cyan")

    zk = z1
    for k in range(10000):
        P.scatter(zk.real, zk.imag, c="red", s=5**2)
        ps = solve_ver_bound_intersect(np.real(zk), meps)
        psts = [x[0] for x in ps]
        P.scatter(np.real(psts), np.imag(psts), color="black", s=3**2)
        segs = intersections_to_segments(ps, np.imag)
        for (a, b) in segs:
            P.plot([a.real, b.real], [a.imag, b.imag], c="black")
        mids = [np.real(a) + 1j*np.imag(a+b)/2 for (a, b) in segs]
        P.scatter(np.real(mids), np.imag(mids), c="black", s=4**2)
        potential = list(map(
            lambda y: solve_max_hor_bound_intersect(1j*np.imag(y), meps)[0],
            mids))
        if len(potential) == 0: break
        zk1 = max(potential, key=np.real)
        if np.isclose(zk1, zk, rtol=1e-9):
            zk = zk1
            break
        zk = zk1

    P.scatter(zk.real, zk.imag, c="violet", marker=".", s=15**2)
