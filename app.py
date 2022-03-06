# from lib.algo.basic import contours
from lib.matrix.matrix import matrice_top
from lib.algo import list_algos, load_mod, rescan_algos

import tkinter as tk
from lib.driver.AlgoWindow import AlgoWindow



root = tk.Tk()
root.title("Pseudospectra")

algos = list_algos()
algo_o = tk.StringVar(root)
algo_o.set(algos[0])
algo_chs = tk.OptionMenu(root, algo_o, *algos)
algo_chs.pack(side=tk.TOP)

win = None
def start_algo():
    global win
    if win: win.close()
    name = algo_o.get()
    module = load_mod(name)
    win = AlgoWindow(name, module.contours, lambda: matrice_top(64))
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