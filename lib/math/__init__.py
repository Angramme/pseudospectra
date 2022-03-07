import numpy as np

def ssvd_min(A):
    # TODO: find a faster implementation
    _, s, _ = np.linalg.svd(A)
    return np.min(s)

def svd_min(A):
    # TODO: find a faster implementation
    u, s, v = np.linalg.svd(A)
    i = np.argmin(s)
    return u[i], s[i], v[i]