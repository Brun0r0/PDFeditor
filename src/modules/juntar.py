import tkinter as tk
from tkinter import messagebox
from PyPDF2 import PdfMerger

class Join(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(background='gray')
        

        #Labels
        tk.Label(self, text='Selecione os arquivos que deseja juntar e deixe na sequência correta', background='gray', fg='white').place(relx=0.15, rely=0.05)

        #Buttons
        tk.Button(self, text='Selecionar Arquivo', command= self.selArq).place(relx=0.4, rely=0.12)

        tk.Button(self, text='Limpar', command= lambda: self.listBox.delete(0, tk.END), background='red2').place(relx=0.5, rely=0.86)

        tk.Button(self, text='Deletar', command= lambda: self.listBox.delete(tk.ACTIVE), background='firebrick1').place(relx=0.63, rely=0.86)

        tk.Button(self, text="Juntar", command= self.juntarPDF, background='lime green').place(relx=0.76, rely=0.86)

        tk.Button(self, text='↑', command=self.arqUp).place(relx=0.86, rely=0.47)

        tk.Button(self, text='↓', command=self.arqDown).place(relx=0.86, rely=0.52)

        tk.Button(self, text='Voltar', command= self.parent.voltar).place(relx=0.02, rely=0.92)

        #ListBox
        self.listBox = tk.Listbox(self, height = 20, width=58)
        self.listBox.place(relx=0.15, rely=0.2)

        
    #Funcs
    def selArq(self):
        caminho = self.parent.selecionarArq()
        
        self.listBox.insert(tk.END, caminho)


    def arqUp(self):
        posList = self.listBox.curselection()
        
        if not posList:
            return

        for pos in posList:
            if pos == 0:
                continue

            text = self.listBox.get(pos)
            self.listBox.delete(pos)
            self.listBox.insert(pos-1, text)


    def arqDown(self):
        posList = self.listBox.curselection()
        
        if not posList:
            return

        for pos in posList:
            if pos == self.listBox.size() - 1:
                continue

            text = self.listBox.get(pos)
            self.listBox.delete(pos)
            self.listBox.insert(pos+1, text)

        
    def juntarPDF(self):
        lista = self.listBox.get(0, tk.END)
        lista_arquivos = list(lista)

        if(lista_arquivos):
            merger = PdfMerger()

            for arq in lista_arquivos:
                merger.append(arq)

            merger.write("PDF Gerado.pdf")

            messagebox.showinfo('Concluído', 'Foi realizada a junção')
            self.listBox.delete(0, tk.END)
        
        else:
            messagebox.showerror('NULL', 'Lista vazia')