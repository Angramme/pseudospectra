from lib.matrix.matrix import matrice_top, diagonal
from lib.algo import list_algos, load_mod, rescan_algos

import tkinter as tk
from lib.driver.AlgoWindow import AlgoWindow
import numpy as np
import random


root = tk.Tk()
root.title("Pseudospectra")

algos = list_algos()
algo_o = tk.StringVar(root)
# algo_o.set(algos[0])
algo_o.set("tracing")
algo_chs = tk.OptionMenu(root, algo_o, *algos)
algo_chs.pack(side=tk.TOP)

win = None
def start_algo():
    global win
    if win: win.close()
    name = algo_o.get()
    module = load_mod(name)
    # matrix = matrice_top(64)
    # matrix = diagonal([2+1.31415j, 1+1j, 3+2j])
    matrix = diagonal([random.random()+random.random()*1j for i in range(7)])
    print(matrix)
    win = AlgoWindow(
        name_v=name, 
        contours_f=module.contours, 
        matrix_v=matrix,
        # eps_v=[10**(-i) for i in range(7, 2, -1)], 
        eps_v=[0.1, 0.2, 0.3, 0.4],
        step_v=0.05,
        )
    win.start()

start_btn = tk.Button(root, text="Start!", command=start_algo)
start_btn.pack(side=tk.BOTTOM)

def close():
    def __close():
        if win: win.stop()
        root.destroy()
    root.after(1, __close) # YES this is very needed for some reason!
root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()