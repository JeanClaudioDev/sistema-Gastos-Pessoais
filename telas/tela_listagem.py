import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mg
from tkcalendar import DateEntry
from datetime import datetime as dt
from utils.json_menager import carregar_gastos
from services.gasto_service import deletar_gasto
from components.topbar import TopBar


class TelaListagem(tk.Frame):

    def __init__(self, master, controller):
        super().__init__(master, bg=master['bg'])
        self.controller = controller

        topbar = TopBar(self, controller)
        topbar.pack(fill="x")

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#0f172a",
            foreground="white",
            fieldbackground="#0f172a",
            borderwidth=0,
            font=("Segoe UI", 11)
        )

        style.configure(
            "Treeview.Heading",
            background="#1e293b",
            foreground="white",
            font=("Segoe UI", 11, "bold")
        )

        style.configure(
            "TLabel",
            font=("Segoe UI", 13)
        )

        self.frame_principal = tk.Frame(self, bg=master['bg'])
        self.frame_principal.pack(fill="both", expand=True)

        # topo
        self.frame_topo = tk.Frame(self.frame_principal, bg="#0f172a")
        self.frame_topo.pack(fill="x", padx=30, pady=20)

        self.frame_topo.columnconfigure(0, weight=1)
        self.frame_topo.columnconfigure(1, weight=1)

        ttk.Label(
            self.frame_topo,
            text='Meus Gastos',
            background='#0f172a',
            foreground='#10b981',
            font=("Segoe UI", 24, "bold")
        ).grid(row=0, column=0, sticky='w')

        ttk.Label(
            self.frame_topo,
            text="Gerencie suas despesas",
            background='#0f172a',
            foreground='#10b981',
            font=("Segoe UI", 18)
        ).grid(row=1, column=0, sticky='w')

        self.total_valor_label = ttk.Label(
            self.frame_topo,
            text='Total Filtrado',
            background='#0f172a',
            foreground="#10b981",
            font=("Segoe UI", 22, "bold")
        )

        self.total_valor_label.grid(row=0, column=1, sticky='e')

        self.total_valor = ttk.Label(
            self.frame_topo,
            text="R$ 0,00",
            background='#0f172a',
            foreground='#10b981',
            font=("Segoe UI", 20)
        )

        self.total_valor.grid(row=1, column=1, sticky='e')

        # filtros
        self.frame_filtros = tk.Frame(self.frame_principal, bg='#1e293b')
        self.frame_filtros.pack(fill='x', padx=30, pady=10)

        for i in range(4):
            self.frame_filtros.columnconfigure(i, weight=1)

        self.data_inicio_entry = self._criar_filtro_date("Data Início", 0, 0)
        self.data_fim_entry = self._criar_filtro_date("Data Fim", 0, 1)
        self.buscar_entry = self._criar_filtro_entry("Buscar", 0, 2)
        self.box_categoria = self._criar_filtro_combobox("Categoria", 0, 3)

        # botoes
        self.button_limpar = tk.Button(
            self.frame_filtros,
            text='Limpar',
            bg='#1e293b',
            fg='white',
            font=("Segoe UI", 12, "bold"),
            command=self.limpar_filtros
        )

        self.button_limpar.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.botao_excluir = tk.Button(
            self.frame_filtros,
            text="Excluir Selecionado",
            bg="#ef4444",
            fg="white",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            command=self.excluir
        )

        self.botao_excluir.grid(row=1, column=2, columnspan=2, sticky="ew", padx=10, pady=10)

        # lista
        self.frame_lista = tk.Frame(self.frame_principal, bg="#0f172a")
        self.frame_lista.pack(fill="both", expand=True)

        self.frame_vazio = tk.Frame(self.frame_lista, bg='#0f172a')
        self.frame_vazio.pack()

        ttk.Label(
            self.frame_vazio,
            text="📋",
            background='#0f172a',
            font=("Segoe UI", 40)
        ).pack()

        ttk.Label(
            self.frame_vazio,
            text="Nenhum gasto encontrado",
            background='#0f172a',
            foreground='white',
            font=("Segoe UI", 16, "bold")
        ).pack()

        ttk.Label(
            self.frame_vazio,
            text="Adicione gastos para vê-los aqui",
            background='#0f172a',
            foreground='#94a3b8',
            font=("Segoe UI", 13)
        ).pack()

        # tabela

        self.frame_tabela = tk.Frame(self.frame_lista, bg="#0f172a")
        self.frame_tabela.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = ttk.Scrollbar(self.frame_tabela)
        scrollbar.pack(side="right", fill="y")

        colunas = ("descricao", "valor", "categoria", "data", "id")

        self.tabela = ttk.Treeview(
            self.frame_tabela,
            columns=colunas,
            show="headings",
            yscrollcommand=scrollbar.set
        )

        scrollbar.config(command=self.tabela.yview)

        for c in colunas:
            self.tabela.heading(c, text=c.capitalize())

        self.tabela.column("descricao", width=280)
        self.tabela.column("valor", width=120)
        self.tabela.column("categoria", width=180)
        self.tabela.column("data", width=120)
        self.tabela.column("id", width=0, stretch=False)

        self.tabela.pack(fill="both", expand=True)

        # eventos filtro automatico
        self.buscar_entry.bind("<KeyRelease>", lambda e: self.filtrar())
        self.box_categoria.bind("<<ComboboxSelected>>", lambda e: self.filtrar())
        self.data_inicio_entry.bind("<<DateEntrySelected>>", lambda e: self.filtrar())
        self.data_fim_entry.bind("<<DateEntrySelected>>", lambda e: self.filtrar())

        self.carregar_lista()
        self.atualizar_total()

    # criar entry
    def _criar_filtro_entry(self, texto, row, col):

        frame = tk.Frame(self.frame_filtros, bg='#1e293b')
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

        ttk.Label(
            frame,
            text=texto,
            background='#1e293b',
            foreground='white',
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w")

        entry = ttk.Entry(frame, font=("Segoe UI", 12))
        entry.pack(fill="x")

        return entry

    # criar combobox
    def _criar_filtro_combobox(self, texto, row, col):

        frame = tk.Frame(self.frame_filtros, bg='#1e293b')
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

        ttk.Label(
            frame,
            text=texto,
            background='#1e293b',
            foreground='white',
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w")

        combo = ttk.Combobox(
            frame,
            values=[
                "Todos",
                "🍕 Alimentação",
                "🚗 Transporte",
                "🏠 Moradia",
                "💡 Contas",
                "🎬 Lazer",
                "🛒 Compras",
                "🏥 Saúde",
                "🎓 Educação",
                "👕 Roupas",
                "💻 Tecnologia",
                "🐶 Pets",
                "✈️ Viagem",
                "📦 Outros"
            ],
            state="readonly",
            font=("Segoe UI", 12)
        )

        combo.pack(fill="x")
        return combo

    # criar date
    def _criar_filtro_date(self, texto, row, col):

        frame = tk.Frame(self.frame_filtros, bg='#1e293b')
        frame.grid(row=row, column=col, padx=10, pady=10, sticky="ew")

        ttk.Label(
            frame,
            text=texto,
            background='#1e293b',
            foreground='white',
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w")

        date_entry = DateEntry(frame, date_pattern='dd/mm/yyyy', font=("Segoe UI", 12))
        date_entry.pack(fill="x")

        return date_entry

    # limpar
    def limpar_filtros(self):

        self.buscar_entry.delete(0, tk.END)
        self.box_categoria.set("")

        self.data_inicio_entry.set_date(dt.today())
        self.data_fim_entry.set_date(dt.today())

        self.carregar_lista()
        self.atualizar_total()

    # excluir
    def excluir(self):

        selecionado = self.tabela.selection()

        if not selecionado:
            mg.showwarning("Aviso", "Selecione um gasto.")
            return

        item = self.tabela.item(selecionado)
        id_gasto = item["values"][4]

        deletar_gasto(id_gasto)

        self.carregar_lista()
        self.atualizar_total()

    # filtrar
    def filtrar(self):

        data_inicio = self.data_inicio_entry.get_date()
        data_fim = self.data_fim_entry.get_date()

        texto = self.buscar_entry.get().lower().strip()
        categoria_selecionada = self.box_categoria.get().strip()

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        gastos = carregar_gastos()
        usuario = self.controller.usuario_logado["usuario"]

        total = 0
        encontrou = False

        for gasto in gastos:

            if gasto.get("usuario") != usuario:
                continue

            descricao = gasto["descricao"].lower()
            categoria_item = gasto["categoria"]
            data_gasto = dt.strptime(gasto["data"], "%d/%m/%Y").date()

            if data_gasto < data_inicio or data_gasto > data_fim:
                continue

            if texto and texto not in descricao:
                continue

            if categoria_selecionada and categoria_selecionada != "Todos":
                if categoria_selecionada.lower() not in categoria_item.lower():
                    continue

            self.tabela.insert(
                "",
                "end",
                values=(
                    gasto["descricao"],
                    f"R$ {float(gasto['valor']):.2f}",
                    gasto["categoria"],
                    gasto["data"],
                    gasto["id"]
                )
            )

            total += float(gasto["valor"])
            encontrou = True

        self.total_valor.config(text=f"R$ {total:.2f}")

        if not encontrou:
            self.frame_vazio.pack()
        else:
            self.frame_vazio.pack_forget()

    # carregar
    def carregar_lista(self):

        for item in self.tabela.get_children():
            self.tabela.delete(item)

        gastos = carregar_gastos()
        usuario = self.controller.usuario_logado["usuario"]

        total = 0
        encontrou = False

        for gasto in gastos:

            if gasto.get("usuario") != usuario:
                continue

            self.tabela.insert(
                "",
                "end",
                values=(
                    gasto["descricao"],
                    f"R$ {float(gasto['valor']):.2f}",
                    gasto["categoria"],
                    gasto["data"],
                    gasto["id"]
                )
            )

            total += float(gasto["valor"])
            encontrou = True

        self.total_valor.config(text=f"R$ {total:.2f}")

        if encontrou:
            self.frame_vazio.pack_forget()
        else:
            self.frame_vazio.pack()

    # atualizar total
    def atualizar_total(self):

        gastos = carregar_gastos()
        usuario = self.controller.usuario_logado["usuario"]

        total = sum(
            float(g["valor"])
            for g in gastos
            if g.get("usuario") == usuario
        )

        self.total_valor.config(text=f"R$ {total:.2f}")