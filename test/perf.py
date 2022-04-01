from lib.matrix import kahan, diagonal
from lib.algo import list_algos, load_mod
import threading as Th

import tkinter as tk
from lib.driver.AlgoWindow import AlgoWindow
import numpy as np

def multisize_timealg(
    name_v,
    rangee=range(10, 50, 10),
    matrix_f=lambda s:diagonal(np.random.default_rng(4242+s).random(s) + 1j*np.random.default_rng(2424+s).random(s)),
    eps_f=lambda s: [0.1*i for i in range(1, 5)],
    step_f=lambda s: 0.01,
    ):
    module = load_mod(name_v)
    times = []

    for size in rangee:
        tm = timealg(
            name=name_v, 
            module=module, 
            matrix=matrix_f(size),
            eps=eps_f(size),
            step=step_f(size)
            )
        print(name_v, size, tm)
        times.append((size, tm)) 
    return times

def timealg(name, module, matrix, eps, step):
    win = AlgoWindow(
        name_v=name, 
        contours_f=module.contours, 
        matrix_v=matrix,
        eps_v=eps,
        step_v=step,
        )
    win.start()
    win.wait()
    win.close()
    return win.end_time - win.start_time

def multimatrix_multisize_timealg(
    name_v,
    rangee=range(10, 50, 10),
    ):
    mat_triples = [
        (
        "random diagonal",
        lambda s: diagonal(1*np.random.default_rng(4242).random(s) + 1j*np.random.default_rng(2424).random(s)),
        lambda s: [0.1*i for i in range(1, 5)],
        lambda s: 0.01
        ),
        (
        "kahan",
        lambda s: kahan(s, 1.5+1.1j, 1.2+.3j),
        lambda s: [0.08*i for i in range(1, 8)],
        lambda s: 0.1,
        )
    ]

    times = dict()
    for (mat_name, mat_f, eps_f, step_f) in mat_triples:
        tm = multisize_timealg(name_v=name_v, rangee=rangee, matrix_f=mat_f, eps_f=eps_f, step_f=step_f)
        times[mat_name] = tm
    return times

def all_multimatrix_multisize_timealg(
    rangee=range(10, 50, 10)
    ):
    algos = list_algos()
    times = dict()

    for name in algos:
        if name[0] == '_': continue
        tm = multimatrix_multisize_timealg(name, rangee)  
        times[name] = tm
    return times

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Pseudospectra")
    def run():
        res = all_multimatrix_multisize_timealg(range(10, 60, 10))
        print(res)
    th = Th.Thread(target=run)
    th.start()
    root.mainloop()
    th.join()
    root.destroy()