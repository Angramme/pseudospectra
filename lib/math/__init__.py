import numpy as np
import math

def ssvd_min(A):
    # TODO: find a faster implementation
    _, s, _ = np.linalg.svd(A)
    return np.min(s)

def svd_min(A):
    # TODO: find a faster implementation
    u, s, v = np.linalg.svd(A)
    i = np.argmin(s)
    # return u[i, :], s[i], v[:, i]
    return u[:, i], s[i], v[i, :]

def segment_point_distance(a, b, z):
    l2 = (a.real-b.real)**2 + (a.imag-b.imag)**2
    if l2 == 0.0: return np.abs(z, a)
    t = max(0, min(1, np.dot(z - a, b - a) / l2))
    projection = a + t * (b - a); 
    return np.abs(z - projection)

def gershgorin(A, eps):
    lb = +math.inf # left bound
    rb = -math.inf # right bound
    tb = -math.inf # top bound
    bb = +math.inf # bottom bound

    n, _ = A.shape
    sqrtn = np.sqrt(n)

    for i in range(n):
        a = A[i, i]
        rA = np.sum(np.abs(A[i])) - np.abs(A[i, i])
        # r = nsqrt * eps + rA
        r = sqrtn * eps + rA
        lb = min(lb, a.real-r)
        rb = max(rb, a.real+r)
        bb = min(bb, a.imag-r)
        tb = max(tb, a.imag+r)

    return lb, rb, bb, tb