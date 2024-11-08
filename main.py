import tkinter as tk    
from tkinter.filedialog import askopenfilenames
from tkinter import messagebox
import PyPDF2    

class App(tk.Tk):

    def __init__(self, title, size):

        #main setup
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}') 
        self.minsize(size[0],size[1])
        
        #widgets
        self.menu = Menu(self)

        #run
        self.mainloop()

class Menu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x=0, y=0, relheight=1, relwidth=1)
        self.createWidgets()



        
    def janelaJuntar(self):

        def selecionarArq():
            arquivo_select = askopenfilenames(title='Selecione o PDF')
            box_arq.insert(tk.END, arquivo_select)

        def GrudarPDF():
            merger = PyPDF2.PdfMerger()
            lista = box_arq.get(0, tk.END)
            lista_arquivos = list(lista)
            for arq in lista_arquivos:
                merger.append(arq[0])
            merger.write("PDF Grudado.pdf")

        janela2 = tk.Toplevel()
        janela2.title("Juntador de PDFs")
        janela2.minsize(width=500, height=500)
        
        label_entrada = tk.Label(janela2, text='Selecione os arquivos que deseja juntar e deixe na sequencia correta')
        label_entrada.place(relx=0.15, rely=0.05)

        buttom_sel = tk.Button(janela2, text='Selecionar Arquivo', command= selecionarArq)
        buttom_sel.place(relx=0.4, rely=0.2)

        box_arq = tk.Listbox(janela2, height = 15, width=50)
        box_arq.place(relx=0.21, rely=0.3)

        buttom_conc = tk.Button(janela2, text="Grudar", command= GrudarPDF)
        buttom_conc.place(relx=0.5, rely=0.8)

    def createWidgets(self):
        menu_button1 = tk.Button(self, text='Juntar', command= self.janelaJuntar)
        menu_button2 = tk.Button(self, text='Converter')
        menu_button3 = tk.Button(self, text='Editar')
        menu_button4 = tk.Button(self, text='Remover paginas')
        menu_button5 = tk.Button(self, text='Separar paginas')

        menu_button1.place(relx=0.35, rely=0.1)
        menu_button2.place(relx=0.35, rely=0.18)
        menu_button3.place(relx=0.35, rely=0.26)
        menu_button4.place(relx=0.35, rely=0.34)
        menu_button5.place(relx=0.35, rely=0.42)




        
        

App('PDFediter', (400,400))