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


#OBS: isso aqui está ruim mesmo, somente salvando o progresso para a partir de mais estudos aperfeiçoar
        
    def janelaJuntar(self):

        def deletarSel():
            box_arq.delete(tk.ACTIVE)

        def selecionarArq():
            arquivo_select = askopenfilenames(title='Selecione o PDF')
            nome_arquivo = arquivo_select[0]
            if(nome_arquivo[-1] == 'f' and nome_arquivo[-2] == 'd' and nome_arquivo[-3] == 'p' and nome_arquivo[-4] == '.'):
                box_arq.insert(tk.END, arquivo_select)
            elif(arquivo_select != ''):
                messagebox.showerror('Type Error', 'somente arquivos do tipo PDF')
            

        def GrudarPDF():
            lista = box_arq.get(0, tk.END)
            lista_arquivos = list(lista)
            tamList = len(lista_arquivos)
            if(tamList == 0):
                messagebox.showerror('NULL', 'Lista vazia')
            else:
                merger = PyPDF2.PdfMerger()
                for arq in lista_arquivos:
                    merger.append(arq[0])
                merger.write("PDF Grudado.pdf")
                messagebox.showinfo('Concluído', 'Foi realizada a junção')
                janela2.quit()

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
        buttom_conc.place(relx=0.3, rely=0.8)

        buttom_del = tk.Button(janela2, text='Deletar', command=deletarSel)
        buttom_del.place(relx=0.7, rely=0.8)

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