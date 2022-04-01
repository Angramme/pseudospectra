from lib.algo import list_algos, load_mod, rescan_algos
import lib.app.multichoice as MC

import importlib
import tkinter as tk
from lib.driver.AlgoWindow import AlgoWindow

root = tk.Tk()
root.title("Pseudospectra")

algos = list_algos()
algo_o = tk.StringVar(root)
algo_o.set("componentwise_grid")
algo_chs = tk.OptionMenu(root, algo_o, *algos)
algo_chs.pack(side=tk.TOP)

matnames = MC.name_matrix_eps_step_quadruplets.keys()
matnames_o = tk.StringVar(root)
matnames_o.set("random diagonal")
matnames_chs = tk.OptionMenu(root, matnames_o, *matnames)
matnames_chs.pack(side=tk.TOP)

win = None
def start_algo():
    global win
    if win: win.close()
    name = algo_o.get()
    module = load_mod(name)
    matname = matnames_o.get()
    importlib.reload(MC)
    mattrip = MC.name_matrix_eps_step_quadruplets[matname]
    
    size = 9
    matrix = mattrip[0](size)
    eps = mattrip[1](size)
    step = mattrip[2](size)

    print(matrix)
    win = AlgoWindow(
        name_v=name, 
        contours_f=module.contours, 
        matrix_v=matrix,
        eps_v=eps,
        step_v=step,
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