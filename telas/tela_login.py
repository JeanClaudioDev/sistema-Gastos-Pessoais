import tkinter as tk
from tkinter import ttk
from services.auth_service import autenticar
from tkinter import messagebox as mg

class TelaLogin(tk.Frame):

    def __init__(self, master, controller):
        super().__init__(master, bg="#0f172a")
        self.pack(fill="both", expand=True)
        self.controller = controller

        self.tela_login()


    def tela_login(self):

        # container central
        frame_login = tk.Frame(self, bg="#1e293b")
        frame_login.place(relx=0.5, rely=0.5, anchor="center", width=350, height=320)

        # título
        titulo = tk.Label(
            frame_login,
            text="Sistema de Gastos",
            font=("Segoe UI", 16, "bold"),
            bg="#1e293b",
            fg="white"
        )
        titulo.pack(pady=(20,10))

        subtitulo = tk.Label(
            frame_login,
            text="Faça login para continuar",
            font=("Segoe UI", 10),
            bg="#1e293b",
            fg="#cbd5e1"
        )
        subtitulo.pack(pady=(0,20))


        # usuário
        label_usuario = tk.Label(
            frame_login,
            text="Usuário",
            bg="#1e293b",
            fg="white",
            font=("Segoe UI", 10)
        )
        label_usuario.pack(anchor="w", padx=30)

        self.entry_usuario = ttk.Entry(frame_login)
        self.entry_usuario.pack(fill="x", padx=30, pady=5)


        # senha
        label_senha = tk.Label(
            frame_login,
            text="Senha",
            bg="#1e293b",
            fg="white",
            font=("Segoe UI", 10)
        )
        label_senha.pack(anchor="w", padx=30, pady=(10,0))

        self.entry_senha = ttk.Entry(frame_login, show="*")
        self.entry_senha.pack(fill="x", padx=30, pady=5)


        # botão login
        botao_login = tk.Button(
            frame_login,
            text="Entrar",
            bg="#10b981",
            fg="white",
            font=("Segoe UI", 11, "bold"),
            relief="flat",
            command=self.login
        )
        botao_login.pack(fill="x", padx=30, pady=20)


    def login(self):

        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()

        user = autenticar(usuario, senha)
        if user:
            self.controller.usuario_logado = user
            mg.showinfo("Sucesso", "Login realizado!")
            self.controller.mostrar_principal()
        else:
            mg.showerror("Erro", "Usuario ou Senha invalidos!")
