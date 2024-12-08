import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from PyPDF2 import PdfReader, PdfWriter


class Break(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(background= 'gray')

        #Labels
        tk.Label(self, text= 'Selecione o PDF que deseja separar', background= 'gray', fg='white').place(relx=0.31, rely=0.1)

        tk.Label(self, text='Selecione a página inicial e final que serão separadas', background='gray', fg='white').place(relx=0.23, rely=0.35)

        tk.Label(self, text='Início', background='gray', fg='white').place(relx=0.35, rely=0.42)
        tk.Label(self, text='Fim',background='gray', fg='white').place(relx=0.5, rely=0.42)

        tk.Label(self, text='Qual será o nome do PDF?', background='gray', fg='white').place(relx=0.23, rely=0.55)

        
        self.label_arq = tk.Label(self, text='Nenhum PDF selecionado', background='white', width= 40, fg='gray')
        self.label_arq.place(relx=0.22, rely=0.25) 

        #ComboBox
        self.comboBox1 = ttk.Combobox(self, state='disabled', width=5)
        self.comboBox1.place(relx= 0.35, rely= 0.46)
        self.comboBox2 = ttk.Combobox(self, state='disabled', width=5)
        self.comboBox2.place(relx= 0.5, rely= 0.46)

        #text
        self.nomeArq = tk.Text(self, font=('Arial', 10), width=30, height=1)
        self.nomeArq.place(relx=0.28, rely=0.60)

        #Buttons
        tk.Button(self, text= 'Selecionar PDF', command= self.selArq).place(relx=0.42, rely=0.18)

        self.separar = tk.Button(self, text='Separar', command= self.separarPDF, state='disable', background='lime green')
        self.separar.place(relx=0.75, rely=0.73)

        tk.Button(self, text='Voltar', command= self.parent.voltar).place(relx=0.02, rely=0.92)

    #Funcs
    def selArq(self):
        caminho = self.parent.selecionarArq()

        self.label_arq.configure(text=caminho, fg='black')

        reader = PdfReader(caminho)
        tam = len(reader.pages)

        valores = [i for i in range(1,tam+1)]

        self.comboBox1.configure(values=valores, state='readonly')
        self.comboBox1.set('1')

        self.comboBox2.configure(values=valores, state='readonly')
        self.comboBox2.set(str(tam))

        self.separar.configure(state='normal')


    def separarPDF(self):
        reader = PdfReader(self.label_arq.cget('text'))

        inicio = int(self.comboBox1.get()) - 1
        fim = int(self.comboBox2.get())

        if(inicio > fim):
            messagebox.showerror('ERRO', 'Início maior que o fim')
            return

        writer = PdfWriter()
        
        for pg in range(inicio,fim):
            writer.add_page(reader.pages[pg])

        saida =  self.nomeArq.get('1.0', tk.END).rstrip() + '.pdf'

        with open(saida, 'wb') as arqSaida:
            writer.write(arqSaida)