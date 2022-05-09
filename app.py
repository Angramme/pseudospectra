from lib.algo import list_algos, load_mod, rescan_algos
import lib.app.multichoice as MC

import importlib
import tkinter as tk
from lib.driver.AlgoWindow import AlgoWindow

root = tk.Tk()
root.title("Pseudospectra")

algos = list_algos()
algo_o = tk.StringVar(root)
algo_o.set("prediction_correction")
algo_chs = tk.OptionMenu(root, algo_o, *algos)
algo_chs.pack(side=tk.TOP)

matnames = MC.name_matrix_eps_step_quadruplets.keys()
matnames_o = tk.StringVar(root)
matnames_o.set("diagonal jordan")
matnames_chs = tk.OptionMenu(root, matnames_o, *matnames)
matnames_chs.pack(side=tk.TOP)

wins = []
def start_algo():
    global wins
    # if win: win.close()
    name = algo_o.get()
    module = load_mod(name)
    matname = matnames_o.get()
    importlib.reload(MC)
    mattrip = MC.name_matrix_eps_step_quadruplets[matname]
    
    size = 9
    matrix = mattrip[0](size)
    eps = mattrip[1](size)
    step = mattrip[2](size)

    
    def onclose():
        wins.remove(win)
    # print(matrix)
    for l in matrix:
        for x in l:
            print("{:+13.2f}, ".format(x), end="")
        print("\n-------")
    win = AlgoWindow(
        name_v=name, 
        main_f=module.main, 
        matrix_v=matrix,
        eps_v=eps,
        step_v=step,
        onclose_f=onclose
        )
    win.start()
    wins.append(win)

start_btn = tk.Button(root, text="Start!", command=start_algo)
start_btn.pack(side=tk.BOTTOM)


def close():
    def __close():
        # if win: win.stop()
        for w in wins:
            w.stop()
        root.destroy()
    root.after(1, __close) # YES this is very needed for some reason!
root.protocol("WM_DELETE_WINDOW", close)
root.mainloop()