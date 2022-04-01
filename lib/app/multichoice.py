from lib.matrix import diagonal, pentadiagonal_toeplitz, kahan
import numpy as np

name_matrix_eps_step_quadruplets = {
    "random diagonal": (
    lambda s: diagonal(1*np.random.default_rng(4242).random(s) + 1j*np.random.default_rng(2424).random(s)),
    lambda s: [0.1*i for i in range(1, 5)],
    lambda s: 0.01
    ),
    "pentadiagonal toeplitz": (
    lambda s: pentadiagonal_toeplitz(64),
    lambda s: [10**(-i) for i in range(7, 3, -1)],
    lambda s: 0.03,
    ),
    "kahan": (
    lambda s: kahan(s, 1.5+1.1j, 1.2+.3j),
    lambda s: [0.08*i for i in range(1, 8)],
    lambda s: 0.1,
    )
}