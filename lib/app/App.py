from turtle import bgcolor
from lib.algo import list_algos, load_mod, rescan_algos
from lib.algo.grid3D import init_figure
import lib.app.defaults as app_defaults

import tkinter as tk
from tkinter import ttk
from lib.app.AlgoWindow import AlgoWindow

import numpy as np

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        # self = tk.Tk()
        self.title("Pseudospectra")
        self.minsize(250, 100)

        style = ttk.Style(self)
        # print(style.theme_names())
        theme = "xpnative"
        if theme in style.theme_names(): style.theme_use(theme)

        grid = ttk.Frame(self, relief=tk.FLAT)
        grid.pack(side=tk.TOP, padx=10, fill=tk.X)

        algos_label = ttk.Label(grid, text="algorithm: ")
        algos_label.grid(row=0, column=0, sticky="E")
        algos = list_algos()
        self.algo_o = tk.StringVar(self)
        # algo_o.set(ADefs.startup["algorithm"])
        algo_chs = ttk.OptionMenu(grid, self.algo_o, app_defaults.startup["algorithm"], *algos)
        algo_chs.grid(row=0, column=1, sticky='W')

        matnames_label = ttk.Label(grid, text="matrix: ")
        matnames_label.grid(row=1, column=0, sticky="E")
        matnames = app_defaults.matrix_associated.keys()
        self.matnames_o = tk.StringVar(self)
        # matnames_o.set(ADefs.startup["matrix"])
        matnames_chs = ttk.OptionMenu(grid, self.matnames_o, app_defaults.startup["matrix"], *matnames)
        matnames_chs.grid(row=1, column=1, sticky='W')

        matrix_settings_label = ttk.Label(self, text="matrix settings: ", justify=tk.CENTER, background="silver")
        matrix_settings_label.pack(side=tk.TOP, pady=5)
        self.matrix_settings = ttk.Frame(self, relief=tk.FLAT)
        self.matrix_settings.pack(side=tk.TOP, pady=5, padx=10, fill=tk.X)

        algorithm_settings_label = ttk.Label(self, text="algorithm settings: ", justify=tk.CENTER, background="silver")
        algorithm_settings_label.pack(side=tk.TOP, pady=5)
        self.algorithm_settings = ttk.Frame(self, relief=tk.FLAT)
        self.algorithm_settings.pack(side=tk.TOP, pady=5, padx=10, fill=tk.X)

        _, self.n_entry = self.make_setting(self.matrix_settings, "size (n)")
        _, self.step_entry = self.make_setting(self.algorithm_settings, "step (τ)")
        _, self.eps_entry = self.make_setting(self.algorithm_settings, "epsilon (ε)") 

        load_defaults_button = ttk.Button(self, text="use defaults of matrix", command=self.load_defaults)
        load_defaults_button.pack(side=tk.TOP)

        show_matrix_btn = ttk.Button(self, text="show matrix", command=self.show_matrix)
        show_matrix_btn.pack(side=tk.TOP)


        self.additional_matrix_settings = []
        self.matnames_o.trace_add("write", self.update_additional_matrix_settings)   

        self.additional_algorithm_settings = []
        self.algo_o.trace_add("write", self.update_additional_algorithm_settings) 

        self.winpos = None
        self.wins = []

        btn_frame = ttk.Frame(self, relief=tk.RAISED, borderwidth=1)
        btn_frame.pack(fill=tk.BOTH, side=tk.BOTTOM, expand=False)
        start_btn = ttk.Button(btn_frame, text="start!", command=self.start_algo)
        start_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        reload_btn = ttk.Button(btn_frame, text="reload", command=self.reload_last)
        reload_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        self.protocol("WM_DELETE_WINDOW", self.close)

    def close(self):
        def __close():
            for w in self.wins:
                w.stop()
            self.destroy()
        self.after(1, __close) # YES this is very needed for some reason!


    def start_algo(self):
        name = self.algo_o.get()
        module = load_mod(name)
        matname = self.matnames_o.get()
        mat_defaults = app_defaults.matrix_associated[matname]

        size = int(self.n_entry.get())
        # eps = [float(self.eps_entry.get())]
        eps = [float(x) for x in self.eps_entry.get().split(",")]
        eps.sort()
        step = float(self.step_entry.get())
        additional_matrix = {}
        for (_, entry, nm, util) in self.additional_matrix_settings:
            additional_matrix[nm] = util["parse"](entry.get())
        matrix = np.array(mat_defaults["func"](size, **additional_matrix))
        additional_algorithm = {}
        for (_, entry, nm, util) in self.additional_algorithm_settings:
            additional_algorithm[nm] = util["parse"](entry.get())


        def onclose():
            self.wins.remove(win)
        win = AlgoWindow(
            name_v=name, 
            main_f=module.main, 
            main_args_v={
                "matrix": matrix,
                "step": step,
                "eps": eps,
                **additional_algorithm,
            },
            onclose_f=onclose,
            initplot_f=module.init_figure if hasattr(module, 'init_figure') else None,
            startwinpos_v=self.winpos,
            )
        win.start()
        self.wins.append(win)

    def reload_last(self):
        if len(self.wins) == 0: return
        self.winpos = self.wins[-1].get_win_position()
        self.wins[-1].stop()
        self.wins[-1].close()
        self.start_algo()
        self.winpos = None

    def load_defaults(self):
        matname = self.matnames_o.get()
        mat_defaults = app_defaults.matrix_associated[matname]
        
        self.n_entry.delete(0, tk.END)
        self.n_entry.insert(0, mat_defaults["n"])
        self.eps_entry.delete(0, tk.END)
        self.eps_entry.insert(0, mat_defaults["eps"])
        self.step_entry.delete(0, tk.END)
        self.step_entry.insert(0, mat_defaults["step"])

    def update_additional_matrix_settings(self, *args):
        for (row, entry, _, _) in self.additional_matrix_settings:
            row.pack_forget()
        self.additional_matrix_settings = []
        
        matname = self.matnames_o.get()
        for (k, v) in app_defaults.matrix_additional[matname].items():
            p = self.make_setting(self.matrix_settings, k)
            p[1].delete(0, tk.END)
            p[1].insert(0, v["serialize"](v["default"]))
            self.additional_matrix_settings.append((*p, k, v))

    def update_additional_algorithm_settings(self, *args):
        for (row, entry, _, _) in self.additional_algorithm_settings:
            row.pack_forget()
        self.additional_algorithm_settings = []

        algname = self.algo_o.get()
        for (k, v) in app_defaults.algorithm_additional[algname].items():
            p = self.make_setting(self.algorithm_settings, k)
            p[1].delete(0, tk.END)
            p[1].insert(0, v["serialize"](v["default"]))
            self.additional_algorithm_settings.append((*p, k, v))


    def make_setting(self, master, name):
        ret = ttk.Frame(master=master, relief=tk.FLAT)
        label = ttk.Label(ret, text=name+": ", width=11, anchor='e')
        entry = ttk.Entry(ret)
        ret.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        label.pack(side=tk.LEFT)
        entry.pack(side=tk.RIGHT, fill=tk.X, expand=True)
        return (ret, entry)

    def show_matrix(self):
        matname = self.matnames_o.get()
        mat_defaults = app_defaults.matrix_associated[matname]

        size = int(self.n_entry.get())
        additional_matrix = {}
        for (_, entry, nm, util) in self.additional_matrix_settings:
            additional_matrix[nm] = util["parse"](entry.get())
        matrix = mat_defaults["func"](size, **additional_matrix)

        cellw = 14

        win = tk.Toplevel(self)
        win.title(f"matrix {matname}")
        mxabs = max([max(abs(x)) for x in matrix])
        for y, line in enumerate(matrix):
            for x, cell in enumerate(line):
                scale = abs(cell)/mxabs
                color = "silver" if cell==0 else f"#{int(scale*255):2x}aadd"
                lab = ttk.Label(win, text=f"{cell:.2f}", width=cellw, borderwidth=1, relief=tk.RIDGE, background=color)
                lab.grid(row=y, column=x)