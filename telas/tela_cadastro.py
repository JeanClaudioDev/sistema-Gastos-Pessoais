import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mg
from datetime import datetime
from tkcalendar import DateEntry
from components.topbar import TopBar
from models.gastos import Gasto
from utils.json_menager import carregar_gastos
from services.gasto_service import (
    cadastrar_gasto,
    deletar_gasto,
    limpar_historico
)


class TelaCadastro(tk.Frame):
    def __init__(self, master, controller):
        super().__init__(master, bg=master.cget('bg'))
        self.controller = controller
        self.aplicar_estilo()

        topbar = TopBar(self, controller)
        topbar.pack(fill="x")

        # frame principal
        self.frame_principal = tk.Frame(self, bg=self['bg'])
        self.frame_principal.pack(fill="both", expand=True)

        # título
        self.frame_titulo = tk.Frame(self.frame_principal, bg="#0f172a")
        self.frame_titulo.pack(fill="x", padx=20, pady=20)

        ttk.Label(
            self.frame_titulo,
            text="Controle de Gastos",
            background="#0f172a",
            foreground="#10b981",
            font=("Segoe UI", 24, "bold")
        ).pack(anchor="w")

        # total
        self.frame_total = tk.Frame(self.frame_principal, bg="#1e293b")
        self.frame_total.pack(fill="x", padx=20, pady=10)

        self.label_total = tk.Label(
            self.frame_total,
            text="Total de Gastos: R$ 0.00",
            bg="#1e293b",
            fg="#10b981",
            font=("Segoe UI", 22, "bold")
        )
        self.label_total.pack(pady=20)

        # formulário
        self.frame_form = tk.Frame(self.frame_principal, bg="#1e293b")
        self.frame_form.pack(fill="x", padx=20, pady=10)

        self.frame_form.columnconfigure(0, weight=1)
        self.frame_form.columnconfigure(1, weight=1)

        # descrição
        ttk.Label(
            self.frame_form,
            text="Descrição",
            background="#1e293b",
            foreground="white",
            font=("Segoe UI", 13, "bold")
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=15, pady=5)

        self.entry_descricao = ttk.Entry(self.frame_form, font=("Segoe UI", 12))
        self.entry_descricao.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=5)

        # valor
        ttk.Label(
            self.frame_form,
            text="Valor (R$)",
            background="#1e293b",
            foreground="white",
            font=("Segoe UI", 13, "bold")
        ).grid(row=2, column=0, sticky="w", padx=15, pady=5)

        self.entry_valor = ttk.Entry(self.frame_form, font=("Segoe UI", 12))
        self.entry_valor.grid(row=3, column=0, sticky="ew", padx=15, pady=5)

        # categoria
        ttk.Label(
            self.frame_form,
            text="Categoria",
            background="#1e293b",
            foreground="white",
            font=("Segoe UI", 13, "bold")
        ).grid(row=2, column=1, sticky="w", padx=15, pady=5)

        self.combo_categoria = ttk.Combobox(
            self.frame_form,
            values=["Todas",
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
        self.combo_categoria.grid(row=3, column=1, sticky="ew", padx=15, pady=5)

        # data
        ttk.Label(
            self.frame_form,
            text="Data (dd/mm/yyyy)",
            background="#1e293b",
            foreground="white",
            font=("Segoe UI", 13, "bold")
        ).grid(row=4, column=0, sticky="w", padx=15, pady=5)

        self.data_entry = DateEntry(
            self.frame_form,
            date_pattern="dd/mm/yyyy",
            font=("Segoe UI", 12),
            background="#1e293b",
            foreground="white",
            borderwidth=2
        )

        self.data_entry.grid(row=5, column=0, sticky="w", padx=15, pady=5)

        # botões
        self.botao_adicionar = tk.Button(
            self.frame_form,
            text="Adicionar Gasto",
            bg="#10b981",
            fg="white",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            command=self.cadastrar
        )
        self.botao_adicionar.grid(row=6, column=0, columnspan=2, sticky="ew", padx=15, pady=15)

        self.botao_deletar = tk.Button(
            self.frame_form,
            text="Deletar Selecionado",
            bg="#ef4444",
            fg="white",
            relief="flat",
            font=("Segoe UI", 12, "bold"),
            command=self.deletar
        )
        self.botao_deletar.grid(row=7, column=0, columnspan=2, sticky="ew", padx=15, pady=10)

        self.botao_limpar = tk.Button(
            self.frame_form,
            text="Limpar Histórico",
            bg='#f50e0b',
            fg='white',
            relief='flat',
            font=('Segoe UI', 12, "bold"),
            command=self.limpar_historico_tela
        )
        self.botao_limpar.grid(row=8, column=0, columnspan=2, sticky='ew', padx=15, pady=10)

        # histórico
        self.frame_historico = tk.Frame(self.frame_principal, bg="#1e293b")
        self.frame_historico.pack(fill="both", expand=True, padx=20, pady=10)

        ttk.Label(
            self.frame_historico,
            text="Histórico de Gastos",
            background="#1e293b",
            foreground="white",
            font=("Segoe UI", 16, "bold")
        ).pack(pady=10)

        # tabela

        self.frame_tabela = tk.Frame(self.frame_historico, bg="#0f172a")
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

        self.atualizar_historico()
        self.atualizar_total()

    def atualizar_total(self):
        gastos = carregar_gastos()
        usuario = self.controller.usuario_logado["usuario"]

        total = sum(
            float(g["valor"]) for g in gastos
            if g.get("usuario") == usuario
        )

        self.label_total.config(text=f"Total de Gastos: R$ {total:.2f}")

    def atualizar_historico(self):
        for item in self.tabela.get_children():
            self.tabela.delete(item)

        gastos = carregar_gastos()
        usuario = self.controller.usuario_logado["usuario"]

        for gasto in gastos:
            if gasto.get("usuario") == usuario:
                self.tabela.insert(
                    "",
                    "end",
                    values=(
                        gasto["descricao"],
                        f'R$ {float(gasto["valor"]):.2f}',
                        gasto["data"],
                        gasto["categoria"],
                        gasto["id"]
                    )
                )

    def deletar(self):
        selecionado = self.tabela.selection()

        if not selecionado:
            mg.showwarning("Aviso", "Selecione um gasto")
            return

        item = self.tabela.item(selecionado)
        id_gasto = item["values"][4]

        deletar_gasto(id_gasto)

        self.atualizar_total()
        self.atualizar_historico()

    def limpar_historico_tela(self):
        if mg.askyesno("Confirmar", "Deseja limpar o histórico?"):
            usuario = self.controller.usuario_logado["usuario"]

            limpar_historico(usuario)

            self.atualizar_total()
            self.atualizar_historico()

    def limpar_form(self):
        self.entry_descricao.delete(0, tk.END)
        self.entry_valor.delete(0, tk.END)
        self.combo_categoria.set("")
        self.data_entry.delete(0, tk.END)

    def cadastrar(self):

        descricao = self.entry_descricao.get()
        valor = self.entry_valor.get()
        data = self.data_entry.get()
        categoria = self.combo_categoria.get()

        if descricao == "":
            mg.showerror("Erro", "Digite uma descrição")
            return

        if valor == "":
            mg.showerror("Erro", "Digite um valor")
            return

        try:
            valor = float(valor)
        except:
            mg.showerror("Erro", "Valor inválido")
            return

        if categoria == "":
            mg.showerror("Erro", "Selecione uma categoria")
            return

        gasto = Gasto(descricao, valor, data, categoria)
        gasto_dict = gasto.to_dict()

        gasto_dict["usuario"] = self.controller.usuario_logado["usuario"]

        cadastrar_gasto(
            gasto_dict["descricao"],
            gasto_dict["valor"],
            gasto_dict["data"],
            gasto_dict["categoria"],
            gasto_dict["usuario"]
        )

        self.limpar_form()
        self.atualizar_total()
        self.atualizar_historico()

    def aplicar_estilo(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="#0f172a",
            foreground="white",
            fieldbackground="#0f172a",
            borderwidth=0,
            relief="flat",
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
            font=("Segoe UI", 12)
        )

        style.map(
            "Treeview",
            background=[("selected", "#10b981")]
        )