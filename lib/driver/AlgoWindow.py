import tkinter as tk
from tkinter.ttk import Progressbar
from matplotlib.figure import Figure

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler as mplib_key_press_handler

import time
import threading
from functools import partial

import numpy as np

class AlgoWindow:
    def __init__(self, name_v, contours_f, matrix_v, eps_v, step_v):
        self.contours_f = contours_f
        self.matrix_v = matrix_v
        self.name_v = name_v
        self.eps_v = eps_v
        self.step_v = step_v

        self.root = tk.Toplevel()
        self.root.protocol("WM_DELETE_WINDOW", partial(AlgoWindow.close, self))
        self.root.title("{} - pseudospectra".format(self.name_v))
        wsize = int(min(self.root.winfo_screenmmwidth(), self.root.winfo_screenheight()))
        self.root.geometry("{}x{}".format(wsize, wsize))

        self.progbar = Progressbar(self.root, orient=tk.HORIZONTAL, mode='determinate')
        self.progbar_txt = tk.Label(master=self.progbar, background=None)
        self.progbar_txt.pack(side=tk.BOTTOM)

        self.figure = Figure(dpi=100)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.root)  # A tk.DrawingArea.

        # pack_toolbar=False will make it easier to use a layout manager later on.
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.root, pack_toolbar=False)

        self.canvas.mpl_connect("key_press_event", mplib_key_press_handler)

        # Packing order is important. Widgets are processed sequentially and if there
        # is no space left, because the window is too small, they are not displayed.
        # The canvas is rather flexible in its size, so we pack it last which makes
        # sure the UI controls are displayed as long as possible.
        self.toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.progbar.pack(side=tk.BOTTOM, fill=tk.X, expand=True)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.keep_running = True
        self.start_time = 0
        self.end_time = 0

        self._last_up = None

        self.calc_th = threading.Thread(target=partial(AlgoWindow.calculate, self))

    def start(self):
        self.start_time = time.time()
        self.calc_th.start()

    def stop(self):
        self.keep_running = False
        print("please wait while {} terminates...".format(self.name_v))
        if self.start_time != 0: self.calc_th.join()
        self.end_time = time.time()
        print("{} terminated!".format(self.name_v))

    def close(self):
        def __close():
            self.stop()
            self.root.destroy()
        self.root.after(1, __close) # YES this is very needed for some reason!
        # I guess because it runs the functions on this windows thread
    
    def upprogressbar(self, p):
        if 'normal' != self.root.state(): return
        now = time.time()
        time_left = (now-self.start_time)/p*(1-p)
        self.progbar_txt['text'] = "{:.1f}% - {:.1f}s".format(int(p*100), time_left)
        self.progbar['value'] = p * 100
        self.root.update()

    def calc_up(self, tup):
        ## limit gui update speed to 24 fps
        now = time.time()
        if self._last_up and now-self._last_up < 1/24: return self.keep_running
        self._last_up = now

        if tup and self.keep_running: self.upprogressbar(tup[0])
        return self.keep_running

    def calculate(self):
        self.contours_f(
            figure=self.figure,
            matrix=self.matrix_v, 
            eps=self.eps_v, 
            step=self.step_v,
            update=partial(AlgoWindow.calc_up, self),
            progresstick=0.003
            )
        if not self.keep_running: return
        self.canvas.draw()
        self.progbar.pack_forget()

        self.end_time = time.time()
        print("{} execution time was {}s".format(self.name_v, self.end_time - self.start_time))

