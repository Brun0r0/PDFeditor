import tkinter as tk
from tkinter.filedialog import askopenfilenames
from tkinter import messagebox
from pathlib import Path
from modules.menu import Menu


class App(tk.Tk):

    def __init__(self, title, size):
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}') 
        self.resizable(False, False)

        self.currentFrame = None

        self.showFrame(Menu)
        
        #run
        self.mainloop()

    #funcs
    def showFrame(self, frame_class):
        if self.currentFrame is not None:
            self.currentFrame.destroy()

        self.currentFrame = frame_class(self)
        self.currentFrame.place(x=0, y=0, relwidth=1, relheight=1)

    def voltar(self):
        self.showFrame(Menu)
    
    def selecionarArq(self):
        arquivo_select = askopenfilenames(title='Selecione o PDF')
        arquivo = arquivo_select[0]
        if(arquivo.lower().endswith('.pdf')):
            return arquivo
        else:
            messagebox.showerror('Type Error', 'somente arquivos do tipo PDF')

        return None
    
    def caminho2nome(self, caminho):
        return Path(caminho).name
