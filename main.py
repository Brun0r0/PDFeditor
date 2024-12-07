import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilenames
from tkinter import messagebox
import PyPDF2    
from pathlib import Path

class App(tk.Tk):

    def __init__(self, title, size):

        #main setup
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

#Ainda precisa de um refinamento visual no Menu
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

        tk.Button(self, text='Voltar', command= lambda: self.parent.showFrame(Menu)).place(relx=0.02, rely=0.92)

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
            merger = PyPDF2.PdfMerger()

            for arq in lista_arquivos:
                merger.append(arq)

            merger.write("PDF Gerado.pdf")

            messagebox.showinfo('Concluído', 'Foi realizada a junção')
            self.listBox.delete(0, tk.END)
        
        else:
            messagebox.showerror('NULL', 'Lista vazia')

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

        self.separar = tk.Button(self, text='Separar', command= self.separarPDF, state='disable')
        self.separar.place(relx=0.75, rely=0.73)

        tk.Button(self, text='Voltar', command= lambda: self.parent.showFrame(Menu)).place(relx=0.02, rely=0.92)

    #Funcs
    def selArq(self):
        caminho = self.parent.selecionarArq()

        self.label_arq.configure(text=caminho, fg='black')

        reader = PyPDF2.PdfReader(caminho)
        tam = len(reader.pages)

        valores = [i for i in range(1,tam+1)]

        self.comboBox1.configure(values=valores, state='readonly')
        self.comboBox1.set('1')

        self.comboBox2.configure(values=valores, state='readonly')
        self.comboBox2.set(str(tam))

        self.separar.configure(state='normal')


    def separarPDF(self):
        reader = PyPDF2.PdfReader(self.label_arq.cget('text'))

        inicio = int(self.comboBox1.get()) - 1
        fim = int(self.comboBox2.get())

        if(inicio > fim):
            messagebox.showerror('ERRO', 'Início maior que o fim')
            return

        writer = PyPDF2.PdfWriter()
        
        for pg in range(inicio,fim):
            writer.add_page(reader.pages[pg])

        saida =  self.nomeArq.get('1.0', tk.END).rstrip() + '.pdf'

        with open(saida, 'wb') as arqSaida:
            writer.write(arqSaida)
        
            

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

        tk.Button(self, text='Deletar página', command= lambda: self.listBox.delete(tk.ACTIVE)).place(relx=0.42, rely=0.8)

        tk.Button(self, text='Confirmar', command= self.gerarPDF).place(relx=0.8, rely=0.9)

        tk.Button(self, text='Voltar', command= lambda: self.parent.showFrame(Menu)).place(relx=0.02, rely=0.92)
    
    #funcs
    def selecionarPDF(self):
        self.listBox.delete(0, tk.END)

        caminho = self.parent.selecionarArq()

        self.nomeArq.configure(text=caminho, fg='black')

        reader = PyPDF2.PdfReader(caminho)

        tam = len(reader.pages)
        
        for i in range(1,tam+1):
            self.listBox.insert(tk.END, str(i))

    def gerarPDF(self):
        if(self.listBox.size() == 0):
            messagebox.showerror('Operação inviável', 'Não há como criar um PDF sem páginas')
            return

        lista = list(self.listBox.get(0, tk.END))

        reader = PyPDF2.PdfReader(self.nomeArq.cget('text'))

        writer = PyPDF2.PdfWriter()

        for page in lista:
            pg = int(page) - 1
            print(type(pg))
            writer.add_page(reader.pages[pg])

        saida =  self.parent.caminho2nome(self.nomeArq.cget('text').rstrip())

        with open(saida, 'wb') as arqSaida:
            writer.write(arqSaida)

        messagebox.showinfo('Concluído', 'O PDF foi modificado com sucesso')
       



App('PDFeditor', (500,500))