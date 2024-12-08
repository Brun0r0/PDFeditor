import tkinter as tk
from modules.juntar import Join
from modules.separar import Break
from modules.delete import Delete

class Menu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(background='gray')

        #Buttons
        tk.Button(self, text='Juntar', command=lambda: self.parent.showFrame(Join)).pack(pady=30)
        tk.Button(self, text='Separar paginas', command= lambda: self.parent.showFrame(Break)).pack(pady=30)
        tk.Button(self, text='Remover paginas', command= lambda: self.parent.showFrame(Delete)).pack(pady=30)
        #tk.Button(self, text='Converter').pack(pady=30)
        #tk.Button(self, text='Editar').pack(pady=30)