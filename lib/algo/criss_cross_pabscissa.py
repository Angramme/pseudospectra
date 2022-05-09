import numpy as np
from collections import Counter
from lib.math import ssvd_min
from lib.utils import flat_map

def main(
    figure, 
    matrix: np.matrix, 
    eps: float,
    step: float,
    update = lambda: True, 
    progresstick =.01
    ):
    n, _ = matrix.shape

    eps = np.max(eps)
    P = figure.add_subplot()
    P.set_aspect(1)

    def solve_ver_bound_intersect(c, eps, A=matrix):
        if not np.isclose(c, np.real(c)): return None
        As = A.conj().T
        mat42 = np.vstack((
            np.hstack(( c * np.eye(n) - As, -eps * np.eye(n)   )),
            np.hstack(( eps * np.eye(n),     A - c * np.eye(n) ))
        ))
        # TODO: replace with hamiltonian eigenvalue solver
        EVs42 = np.linalg.eigvals(mat42)
        intersections = []
        for (ev, mul) in Counter(EVs42).most_common():
            if not np.isclose(np.real(ev), 0, rtol=1e-9): continue
            p = c + ev
            sm = ssvd_min(p*np.eye(n) - A) # find min svd
            if not np.isclose(sm, eps, rtol=1e-9): continue 
            intersections.append((p, mul))
        return intersections

    def solve_max_hor_bound_intersect(c, eps, A=matrix):
        if not np.isclose(c, 1j*np.imag(c)): return None
        As = A.conj().T
        mat42 = np.vstack((
            np.hstack(( c * np.eye(n) + As, eps * np.eye(n)   )),
            np.hstack(( eps * np.eye(n),     A - c * np.eye(n) ))
        ))
        # TODO: replace with hamiltonian eigenvalue solver
        EVs42 = np.linalg.eigvals(mat42)
        mx = (float('-inf'), None)
        for (ev, mul) in Counter(EVs42).most_common():
            if not np.isclose(np.imag(ev), 0): continue
            p = c + ev
            if p > mx[0]:
                mx = (p, mul)
        return mx

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
    
    EVs = np.linalg.eigvals(matrix)
    lam = max(EVs, key=np.real) # rightmost eigenvalue
    P.scatter(lam.real, lam.imag, c="green")

    z1 = solve_max_hor_bound_intersect(1j*np.imag(lam), eps)[0]

    P.scatter(np.real(z1), np.imag(z1), color="cyan")

    zk = z1
    for k in range(10000):
        P.scatter(zk.real, zk.imag, c="red")
        ps = solve_ver_bound_intersect(np.real(zk), eps)
        psts = [x[0] for x in ps]
        P.scatter(np.real(psts), np.imag(psts), color="violet")
        segs = intersections_to_segments(ps, np.imag)
        mids = [np.real(a) + 1j*np.imag(a+b)/2 for (a, b) in segs]
        P.scatter(np.real(mids), np.imag(mids), c="yellow")
        potential = list(map(
            lambda y: solve_max_hor_bound_intersect(1j*np.imag(y), eps)[0],
            mids))
        if len(potential) == 0: break
        zk1 = max(potential, key=np.real)
        if np.isclose(zk1, zk, rtol=1e-9):
            zk = zk1
            break
        zk = zk1

    P.scatter(zk.real, zk.imag, c="blue")

