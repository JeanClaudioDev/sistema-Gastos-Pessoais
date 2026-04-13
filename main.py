import tkinter as tk

from telas.tela_principal import TelaPrincipal
from telas.tela_cadastro import TelaCadastro
from telas.tela_listagem import TelaListagem
from telas.tela_login import TelaLogin

COR_FUNDO = "#0f172a"
class App:

    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Gastos")
        self.root.geometry("1400x800")
        self.root.state('zoomed')
        self.usuario_logado = None
        # container onde as telas aparecem
        self.container = tk.Frame(root, bg=COR_FUNDO)
        self.container.pack(fill="both", expand=True)   

        self.criar_menu()

        # primeira tela
        self.mostrar_login()

    def limpar_tela(self):
        for widget in self.container.winfo_children():
            widget.destroy()
    
    def mostrar_login(self):
        self.limpar_tela()
        tela = TelaLogin(self.container, controller=self)
        tela.pack(fill='both', expand=True)

    def mostrar_principal(self):
        self.limpar_tela()
        tela = TelaPrincipal(self.container, controller=self)
        tela.pack(fill="both", expand=True)

    def mostrar_cadastro(self):
        self.limpar_tela()
        tela = TelaCadastro(self.container, controller=self)
        tela.pack(fill="both", expand=True)

    def mostrar_listagem(self):
        self.limpar_tela()
        tela = TelaListagem(self.container, controller=self)
        tela.pack(fill="both", expand=True)

    def criar_menu(self):

        menubar = tk.Menu(self.root)

        menu = tk.Menu(menubar, tearoff=0)

        menu.add_command(label="Tela Principal", command=self.mostrar_principal)
        menu.add_command(label="Cadastro", command=self.mostrar_cadastro)
        menu.add_command(label="Listagem", command=self.mostrar_listagem)
        menu.add_separator()
        menu.add_command(label="Sair", command=self.root.quit)

        menubar.add_cascade(label="Menu", menu=menu)

        self.root.config(menu=menubar)


root = tk.Tk()
app = App(root)
root.mainloop()