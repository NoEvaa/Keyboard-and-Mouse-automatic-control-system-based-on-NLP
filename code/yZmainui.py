# -*- coding: utf-8 -*-
"""
Welcome to Noah's Ark
"""
import tkinter as tk

from yZagguisenior import YzUltimateGui

class YzMainUi(tk.Frame, YzUltimateGui):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master) #初始化
        YzUltimateGui.__init__(self, self.master)
        self.master.focus_force()
        self.master.title('别动，我 自 己 来 ————————————————')
        self.master.geometry('1000x750')
        self.master.resizable(0,0)
if __name__ == '__main__':
    ui = YzMainUi()
    ui.mainloop()
