from lib.matrix import diagonal, pentadiagonal_toeplitz, kahan, diagonal_jordan
import numpy as np

startup = {
    "matrix": "diagonal jordan",
    "algorithm": "prediction_correction",
}

matrix_associated = {
    "random diagonal": {
        "func": lambda n: diagonal(1*np.random.default_rng(4242).random(n) + 1j*np.random.default_rng(2424).random(n)),
        "eps": [0.5],
        "step": 0.025,
        "n": 9,
    },
    "diagonal": {
        "func": lambda _, arr: diagonal(arr),
        "eps": [0.5],
        "step": 0.025,
        "n": 0,
    },
    "pentadiagonal toeplitz": {
        "func": pentadiagonal_toeplitz,
        "eps": [10**(-3)],
        "step": 0.03,
        "n": 64,
    },
    "kahan": {
        # "func": lambda n: kahan(n, 1.5+1.1j, 1.2+.3j),
        "func": kahan,
        # lambda s: [0.08*i for i in range(1, 8)],
        "eps": [0.08],
        "step": 0.1,
        "n": 9,
    },
    "diagonal jordan": {
        "func": diagonal_jordan,
        "eps": [0.3],
        "step": 0.1,
        "n": 9,
    },
}

matrix_additional = {
    "random diagonal": {},
    "diagonal": {
        "arr": {
            "default": [-1+1j, 0.5+0.7j, 0.1+0.3j],
            "serialize": lambda val: ", ".join([str(v) for v in val]),
            "parse": lambda st: [complex(v) for v in st.split(", ")]
        },
    },
    "pentadiagonal toeplitz": {},
    "kahan": {
        "c": {
            "default": 1.5+1.1j,
            "serialize": str,
            "parse": complex,
        },
        "s": {
            "default": 1.2+.3j,
            "serialize": str,
            "parse": complex,
        },
    },
    "diagonal jordan": {},
}

algorithm_additional = {
    "componentwise_grid":{},
    "criss_cross_pabscissa":{},
    "cris_cros_pradius":{},
    "grid":{},
    "grid3D":{
        "rstride": {
            "default": None,
            "serialize": lambda x: str(x) if x else "_",
            "parse": lambda x: int(x) if x != "_" else None,
        },
        "cstride": {
            "default": None,
            "serialize": lambda x: str(x) if x else "_",
            "parse": lambda x: int(x) if x != "_" else None,
        },
    },
    "prediction_correction":{},
}