from lib.matrix import matrice_top, diagonal
from lib.algo import list_algos, load_mod
import threading as Th

import tkinter as tk
from lib.driver.AlgoWindow import AlgoWindow
import numpy as np

root = tk.Tk()
root.title("Pseudospectra")

algos = list_algos()

def run_perf():    
    times = {n:[] for n in algos}

    for name in algos:
        if name[0] == '_': continue

        module = load_mod(name)

        for size in range(10, 50, 10):
            matrix = diagonal(np.random.default_rng(4242+size).random(size) + 1j*np.random.default_rng(2424+size).random(size))
            print(matrix)
            win = AlgoWindow(
                name_v=name, 
                contours_f=module.contours, 
                matrix_v=matrix,
                # eps_v=[10**(-i) for i in range(7, 2, -1)], 
                eps_v=[0.1*i for i in range(1, 5)],
                step_v=0.01,
                )
            win.start()
            win.wait()
            win.close()

            times[name].append((size, win.end_time - win.start_time))

    for k, T in times.items():
        print("{} : ".format(k))
        for (s, t) in T:
            print("size : {} ; time : {}s".format(s, t))

    root.destroy()

th = Th.Thread(target=run_perf)
th.start()
root.mainloop()
th.join()