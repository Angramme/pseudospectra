from lib.algo.basic import contours
from lib.matrix.matrix import matrice_top

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler as mplib_key_press_handler
import tkinter as tk
from tkinter.ttk import Progressbar
from matplotlib.figure import Figure

import threading
import time


root = tk.Tk()
root.title("Pseudospectra")
wsize = int(min(root.winfo_screenmmwidth(), root.winfo_screenheight()))
root.geometry("{}x{}".format(wsize, wsize))

progress_calc = Progressbar(root, orient=tk.HORIZONTAL, mode='determinate')
time_calc = tk.Label(master=progress_calc, background=None)
time_calc.pack(side=tk.BOTTOM)

fig = Figure(dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.

# pack_toolbar=False will make it easier to use a layout manager later on.
toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)

canvas.mpl_connect("key_press_event", mplib_key_press_handler)


# Packing order is important. Widgets are processed sequentially and if there
# is no space left, because the window is too small, they are not displayed.
# The canvas is rather flexible in its size, so we pack it last which makes
# sure the UI controls are displayed as long as possible.
toolbar.pack(side=tk.BOTTOM, fill=tk.X)
progress_calc.pack(side=tk.BOTTOM, fill=tk.X, expand=True)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

keep_running = True
start_time = 0
def upprogressbar(p):
    if not keep_running:
        return False
    now = time.time()
    time_left = (now-start_time)/p*(1-p)
    time_calc['text'] = "{}% - {:.1f}s".format(int(p*100), time_left)
    progress_calc['value'] = p * 100
    return True

def calculate():
    # contours(matrice_top(64), [10**(-7)], step=0.015)
    # contours(matrice_top(64), [10**(-i) for i in range(7, 2, -1)], step=0.035)
    contours(
        figure=fig,
        matrix=matrice_top(64), 
        eps=[10**(-i) for i in range(7, 2, -1)], 
        step=0.003,
        onprogress=upprogressbar,
        progresstick=0.003
        )
    if not keep_running: return
    canvas.draw()
    progress_calc.pack_forget()

calc_th = threading.Thread(target=calculate)

start_time = time.time()
calc_th.start()
root.mainloop()
keep_running = False
calc_th.join()
