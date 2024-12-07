import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilenames
from tkinter import messagebox
import PyPDF2    

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

#Ainda precisa de um refinamento visual no Menu

    def createWidgets(self):
        tk.Button(self, text='Juntar', command=lambda: self.parent.showFrame(Join)).pack(pady=30)
        tk.Button(self, text='Separar paginas', command= lambda: self.parent.showFrame(Break)).pack(pady=30)
        tk.Button(self, text='Remover paginas', command= lambda: self.parent.showFrame(Delete)).pack(pady=30)
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
        tk.Label(self, text='Selecione os arquivos que deseja juntar e deixe na sequência correta', background='gray', fg='white').place(relx=0.15, rely=0.05)
        
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

class Break(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.configure(background= 'gray')

        #Labels

        tk.Label(self, text= 'Selecione o PDF que deseja separar', background= 'gray').place(relx=0.31, rely=0.1)

        tk.Label(self, text='Selecione a página inicial e final que serão separadas', background='gray', fg='white').place(relx=0.2, rely=0.4)
        tk.Label(self, text='(A página selecionada seja mantida no PDF)', background='gray', fg='red4').place(relx=0.25, rely=0.44)

        tk.Label(self, text='Ínicio', background='gray').place(relx=0.35, rely=0.49)
        tk.Label(self, text='Fim',background='gray').place(relx=0.5, rely=0.49)

        tk.Label(self, text='Nome do novo arquivo:', background='gray').place(relx=0.15, rely=0.65)

        
        self.label_arq = tk.Label(self, text='Nenhum PDF selecionado', background='white', width= 40, fg='gray')
        self.label_arq.place(relx=0.22, rely=0.25) 

        #comboBox
        self.comboBox1 = ttk.Combobox(self, state='disabled', width=5)
        self.comboBox1.place(relx= 0.35, rely= 0.54)
        self.comboBox2 = ttk.Combobox(self, state='disabled', width=5)
        self.comboBox2.place(relx= 0.5, rely= 0.54)

        #text
        self.nomeArq = tk.Text(self, font=('Arial', 10), width=30, height=1)
        self.nomeArq.place(relx=0.42, rely=0.65)

        #buttons
        tk.Button(self, text= 'Selecionar PDF', command= self.selecionarPDF).place(relx=0.42, rely=0.18)

        tk.Button(self, text='Limpar', command= self.limpar).place(relx=0.7, rely=0.31)

        self.separar = tk.Button(self, text='Separar', command= self.separarPDF, state='disable')
        self.separar.place(relx=0.75, rely=0.73)

        tk.Button(self, text='Voltar', command= lambda: self.parent.showFrame(Menu)).place(relx=0.02, rely=0.92)

    #funcs
    def selecionarPDF(self):
        arquivo = askopenfilenames(title='Selecione o PDF')
        nome_arquivo = arquivo[0]

        if(nome_arquivo.lower().endswith('.pdf')):
            self.label_arq.configure(text=nome_arquivo, fg='black')

            reader = PyPDF2.PdfReader(nome_arquivo)

            tam = len(reader.pages)

            valores = [i for i in range(1,tam+1)]

            self.comboBox1.configure(values=valores, state='readonly')
            self.comboBox1.set('1')

            self.comboBox2.configure(values=valores, state='readonly')
            self.comboBox2.set(str(tam))

            self.separar.configure(state='normal')

            
        elif(arquivo):
            messagebox.showerror('Type Error', 'somente arquivos do tipo PDF')

    def limpar(self):
        self.label_arq.configure(text='Nenhum PDF selecionado', fg='gray')
        self.separar.configure(state='disable')

        self.comboBox1.configure(values=[], state='disable')
        self.comboBox1.set('')
        self.comboBox2.configure(values=[], state='disable')
        self.comboBox2.set('')



    def separarPDF(self):
        reader = PyPDF2.PdfReader(self.label_arq.cget('text'))

        inicio = int(self.comboBox1.get()) - 1
        fim = int(self.comboBox2.get())

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
        self.createWidgets()

        self.listBox = tk.Listbox(self, width=57, height=15)
        self.listBox.place(relx=0.15, rely=0.28)

    def createWidgets(self):
        
        tk.Label(self, text='Selecione o PDF que deseja modificar', background='gray').place(relx=0.31, rely=0.1)

        tk.Button(self, text='Selecionar PDF').place(relx=0.42, rely=0.18)

        tk.Button(self, text='Voltar', command= lambda: self.parent.showFrame(Menu)).place(relx=0.02, rely=0.92)

        #funcs




App('PDFeditor', (500,500))