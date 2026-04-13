import tkinter as tk
from tkinter import ttk
from components.topbar import TopBar
from services.gasto_service import ultimos_gastos
from services.gasto_service import carregar_gastos


class TelaPrincipal(tk.Frame):

    def __init__(self, master, controller):
        super().__init__(master, bg=master['bg'])
        self.controller = controller
        
        topbar = TopBar(self, controller)
        topbar.pack(fill="x")
        
        self.criar_header()
        self.criar_estatisticas()
        self.criar_ultimos()
        self.criar_menu()


    # header

    def criar_header(self):

        self.frame_header = tk.Frame(self, bg=self['bg'])
        self.frame_header.pack(fill='both', padx=15, pady=10)

        ttk.Label(
            self.frame_header,
            text='Controle de Gastos',
            background='#0f172a',
            foreground='white',
            font=("Segoe UI", 22, "bold")
        ).pack(anchor='w')
            
        ttk.Label(
            self.frame_header,
            text='Olá, bem-vindo!',
            background='#0f172a',
            foreground='#cbd5e1',
            font=("Segoe UI", 13)
        ).pack(anchor='w')

        ttk.Label(
            self.frame_header,
            text='O que deseja fazer hoje?',
            background='#0f172a',
            foreground='white',
            font=("Segoe UI", 18, "bold")
        ).pack(anchor='w', pady=(10,0))


    # estatisticas

    def criar_estatisticas(self):

        self.frame_estatisticas = tk.Frame(self, bg=self['bg'])
        self.frame_estatisticas.pack(fill='x', padx=5, pady=5)

        self.frame_estatisticas.columnconfigure(0, weight=1)
        self.frame_estatisticas.columnconfigure(1, weight=1)

        usuario = self.controller.usuario_logado["usuario"]

        gastos = carregar_gastos()

        gastos_usuario = []

        for gasto in gastos:
            if gasto.get("usuario") == usuario:
                gastos_usuario.append(gasto)

        total = sum(float(g["valor"]) for g in gastos_usuario)

        # card total gasto
        self.frame_card_gastos = tk.Frame(self.frame_estatisticas, bg='#1e293b')
        self.frame_card_gastos.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        ttk.Label(
            self.frame_card_gastos,
            text='Total gasto',
            background='#1e293b',
            foreground='#94a3b8',
            font=("Segoe UI", 13)
        ).grid(row=0, column=0, padx=10, pady=(10,0), sticky='w')

        ttk.Label(
            self.frame_card_gastos,
            text=f'R$ {total:.2f}',
            background='#1e293b',
            foreground='#10b981',
            font=("Segoe UI",22,"bold")
        ).grid(row=1, column=0, padx=10, pady=(0,10), sticky='w')

        # card total registros
        self.frame_card_registro = tk.Frame(self.frame_estatisticas, bg='#1e293b')
        self.frame_card_registro.grid(row=0, column=1, sticky='nsew', padx=10, pady=10)

        ttk.Label(
            self.frame_card_registro,
            text='Total de Registros',
            background='#1e293b',
            foreground='#94a3b8',
            font=("Segoe UI", 13)
        ).grid(row=0, column=0, padx=10, pady=(10,0), sticky='w')
        
        ttk.Label(
            self.frame_card_registro,
            text=f'{len(gastos_usuario)}',
            background='#1e293b',
            foreground='#10b981',
            font=("Segoe UI",22,"bold")
        ).grid(row=1, column=0, padx=10, pady=(0,10), sticky='w')

    # ultimos gastos
    def criar_ultimos(self):

        usuario = self.controller.usuario_logado["usuario"]

        self.frame_ultimos = tk.Frame(self, bg='#1e293b')
        self.frame_ultimos.pack(fill='x', padx=10, pady=10)

        ttk.Label(
            self.frame_ultimos,
            text='Últimos gastos',
            background='#1e293b',
            foreground='white',
            font=("Segoe UI",16,"bold")
        ).pack(anchor='w', padx=10, pady=(10,5))

        ultimos = ultimos_gastos(usuario)

        if not ultimos:

            ttk.Label(
                self.frame_ultimos,
                text='Nenhum gasto cadastrado',
                background='#1e293b',
                foreground='#94a3b8'
            ).pack(anchor='w', padx=10, pady=(0,10))

            return

        for gasto in ultimos:

            linha = tk.Frame(self.frame_ultimos, bg='#1e293b')
            linha.pack(fill='x', padx=10, pady=2)

            ttk.Label(
                linha,
                text=gasto["descricao"],
                background='#1e293b',
                foreground='white',
                font=("Segoe UI",12)
            ).pack(side='left')

            ttk.Label(
                linha,
                text=f'R$ {float(gasto["valor"]):.2f}',
                background='#1e293b',
                foreground='#10b981',
                font=("Segoe UI",12,"bold")
            ).pack(side='right')

    # menu
    def criar_menu(self):

        ttk.Label(
            self,
            text="Menu Principal",
            background='#0f172a',
            foreground='#94a3b8',
            font=("Segoe UI", 14, "bold")
        ).pack(anchor='w', padx=15, pady=(10,0))

        self.frame_menu = tk.Frame(self, bg=self['bg'])
        self.frame_menu.pack(fill='both')

        # card cadastro

        self.frame_cadastro = tk.Frame(self.frame_menu, bg='#1e293b')
        self.frame_cadastro.pack(fill='x', padx=10, pady=10)
        self.frame_cadastro.bind("<Button-1>", self.abrir_cadastro)

        ttk.Label(
            self.frame_cadastro,
            text='➕',
            background='#1e293b',
            font=("Segoe UI",18)
        ).grid(row=0,column=0,rowspan=2,padx=10)

        ttk.Label(
            self.frame_cadastro,
            text="Cadastrar Gasto",
            background='#1e293b',
            foreground='white',
            font=("Segoe UI",17,"bold")
        ).grid(row=0,column=1,sticky='w')

        ttk.Label(
            self.frame_cadastro,
            text='Adicione uma nova despesa',
            background='#1e293b',
            foreground='#94a3b8',
            font=("Segoe UI",13)
        ).grid(row=1,column=1,sticky='w')

        # card listar

        self.frame_listar = tk.Frame(self.frame_menu, bg='#1e293b')
        self.frame_listar.pack(fill='x', padx=10, pady=10)
        self.frame_listar.bind("<Button-1>", self.abrir_listagem)

        ttk.Label(
            self.frame_listar,
            text='📋',
            background='#1e293b',
            font=("Segoe UI",18)
        ).grid(row=0,column=0,rowspan=2,padx=10)

        ttk.Label(
            self.frame_listar,
            text='Listar Gastos',
            background='#1e293b',
            foreground='white',
            font=("Segoe UI",17,"bold")
        ).grid(row=0,column=1,sticky='w')

        ttk.Label(
            self.frame_listar,
            text="Visualize todos os registros",
            background='#1e293b',
            foreground='#94a3b8',
            font=("Segoe UI",13)
        ).grid(row=1,column=1,sticky='w')


    def abrir_cadastro(self, event):
        self.controller.mostrar_cadastro()


    def abrir_listagem(self, event):
        self.controller.mostrar_listagem()