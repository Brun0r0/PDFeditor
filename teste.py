import tkinter as tk

class App(tk.Tk):
    def __init__(self, title, size):
        # Configurações principais
        super().__init__()
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self.resizable(False, False)

        # Armazena o frame atual exibido na janela
        self.current_frame = None

        # Exibe o menu inicial
        self.show_frame(Menu)

        # Executa o loop principal
        self.mainloop()

    def show_frame(self, frame_class):
        # Destroi o frame atual se existir
        if self.current_frame is not None:
            self.current_frame.destroy()

        # Cria um novo frame e exibe na janela
        self.current_frame = frame_class(self)
        self.current_frame.place(x=0, y=0, relwidth=1, relheight=1)

class Menu(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(background='gray')
        label = tk.Label(self, text='Bem-vindo ao PDFeditor', font='Arial')
        label.pack(pady=20)

        # Botão para abrir a janela de “Juntar PDFs”
        join_button = tk.Button(self, text="Juntar PDFs", command=lambda: parent.show_frame(JanelaJoin))
        join_button.pack(pady=10)

class JanelaJoin(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.configure(background='lightblue')
        label = tk.Label(self, text='Janela de Juntar PDFs', font='Arial')
        label.pack(pady=20)

        # Botão para voltar ao menu principal
        back_button = tk.Button(self, text="Voltar", command=lambda: parent.show_frame(Menu))
        back_button.pack(pady=10)

# Código principal
if __name__ == "__main__":
    app = App("PDFeditor", (500, 500))
