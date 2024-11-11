import tkinter as tk    
from tkinter.filedialog import askopenfilenames
from tkinter import messagebox
import PyPDF2    
from PIL import Image, ImageTk

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


    def showFrame(self, frame_class):
        if self.currentFrame is not None:
            self.currentFrame.destroy()

        self.currentFrame = frame_class(self)
        self.currentFrame.place(x=0, y=0, relwidth=1, relheight=1)

class Menu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(background='gray')

        self.createWidgets()


    def createWidgets(self):
        tk.Button(self, text='Juntar', command=lambda: self.parent.showFrame(Join)).pack(pady=30)
        tk.Button(self, text='Separar paginas').pack(pady=30)
        tk.Button(self, text='Remover paginas').pack(pady=30)
        tk.Button(self, text='Converter').pack(pady=30)
        tk.Button(self, text='Editar').pack(pady=30)


class Join(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(background='gray')
        self.createWidgets()

        #ListBox
        self.listBox = tk.Listbox(self, height = 20, width=58)
        self.listBox.place(relx=0.15, rely=0.2)

    #widgets
    def createWidgets(self):
        tk.Label(self, text='Selecione os arquivos que deseja juntar e deixe na sequência correta', background='gray').place(relx=0.15, rely=0.05)
        
        tk.Button(self, text='Selecionar Arquivo', command= self.selecionarArq).place(relx=0.4, rely=0.12)

        tk.Button(self, text='Limpar', command= lambda: self.listBox.delete(0, tk.END), background='red2').place(relx=0.5, rely=0.86)

        tk.Button(self, text='Deletar', command= lambda: self.listBox.delete(tk.ACTIVE), background='firebrick1').place(relx=0.63, rely=0.86)

        tk.Button(self, text="Juntar", command= self.GrudarPDF, background='lime green').place(relx=0.76, rely=0.86)

        tk.Button(self, text='↑', command=self.arqUp).place(relx=0.86, rely=0.47)

        tk.Button(self, text='↓', command=self.arqDown).place(relx=0.86, rely=0.52)

        tk.Button(self, text='Voltar', command= lambda: self.parent.showFrame(Menu)).place(relx=0.02, rely=0.92)

    #funcs
    def selecionarArq(self):
        arquivo_select = askopenfilenames(title='Selecione o PDF')
        nome_arquivo = arquivo_select[0]
        if(nome_arquivo.lower().endswith('.pdf')):
            self.listBox.insert(tk.END, nome_arquivo)
        elif(arquivo_select):
            messagebox.showerror('Type Error', 'somente arquivos do tipo PDF')


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

        
    def GrudarPDF(self):
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


App('PDFeditor', (500,500))