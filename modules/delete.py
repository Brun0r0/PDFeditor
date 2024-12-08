import tkinter as tk
from tkinter import messagebox
from PyPDF2 import PdfReader, PdfWriter



class Delete(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(background='gray')

        #ListBox
        self.listBox = tk.Listbox(self, width=15, height=13)
        self.listBox.place(relx=0.41, rely=0.36)

        #Labels
        tk.Label(self, text='Selecione o PDF que deseja modificar', background='gray', fg='white').place(relx=0.31, rely=0.1)
        
        tk.Label(self, text='Pagínas', background='white').place(relx=0.46, rely=0.31)

        tk.Label(self, text='Arquivo:', background='gray', fg='white').place(relx=0.12, rely=0.23)

        self.nomeArq = tk.Label(self, text='Selecione um PDF', background='white', fg='gray', width=40)
        self.nomeArq.place(relx=0.23, rely=0.23)

        #Buttons
        tk.Button(self, text='Selecionar PDF', command= self.selecionarPDF).place(relx=0.41, rely=0.16)

        tk.Button(self, text='Deletar página', command= lambda: self.listBox.delete(tk.ACTIVE), background='firebrick1').place(relx=0.42, rely=0.8)

        tk.Button(self, text='Confirmar', command= self.gerarPDF, background='lime green').place(relx=0.8, rely=0.9)

        tk.Button(self, text='Voltar', command= self.parent.voltar).place(relx=0.02, rely=0.92)
    
    #funcs
    def selecionarPDF(self):
        self.listBox.delete(0, tk.END)

        caminho = self.parent.selecionarArq()

        self.nomeArq.configure(text=caminho, fg='black')

        reader = PdfReader(caminho)

        tam = len(reader.pages)
        
        for i in range(1,tam+1):
            self.listBox.insert(tk.END, str(i))

    def gerarPDF(self):
        if(self.listBox.size() == 0):
            messagebox.showerror('Operação inviável', 'Não há como criar um PDF sem páginas')
            return

        lista = list(self.listBox.get(0, tk.END))

        reader = PdfReader(self.nomeArq.cget('text'))

        writer = PdfWriter()

        for page in lista:
            pg = int(page) - 1
            print(type(pg))
            writer.add_page(reader.pages[pg])

        saida =  self.parent.caminho2nome(self.nomeArq.cget('text').rstrip())

        with open(saida, 'wb') as arqSaida:
            writer.write(arqSaida)

        messagebox.showinfo('Concluído', 'O PDF foi modificado com sucesso')