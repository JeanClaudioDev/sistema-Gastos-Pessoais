from utils.json_menager import adicionar_gasto, salvar_gastos, carregar_gastos
from models.gastos import Gasto
from tkinter import messagebox as mg


def cadastrar_gasto(descricao, valor, data, categoria, usuario):

    try:

        gasto = Gasto(descricao, valor, data, categoria)

        dados = gasto.to_dict()

        dados["usuario"] = usuario

        adicionar_gasto(dados)

        mg.showinfo("Sucesso", "Gasto cadastrado com sucesso!")

    except Exception as e:

        mg.showerror("Erro", f"Erro ao cadastrar gasto\n{e}")


def calcular_total_gastos(gastos):

    total = 0

    for gasto in gastos:

        total += float(gasto["valor"])

    return total


def deletar_gasto(id):

    gastos = carregar_gastos()

    novos = []

    for gasto in gastos:

        if gasto["id"] != id:

            novos.append(gasto)

    salvar_gastos(novos)


def limpar_historico(usuario):

    gastos = carregar_gastos()

    novos = []

    for gasto in gastos:

        if gasto.get("usuario") != usuario:

            novos.append(gasto)

    salvar_gastos(novos)


def listar_gastos_usuario(usuario):

    gastos = carregar_gastos()

    gastos_usuario = []

    for gasto in gastos:

        if gasto.get("usuario") == usuario:

            gastos_usuario.append(gasto)

    return gastos_usuario

def ultimos_gastos(usuario, limite=5):

    gastos = carregar_gastos()

    lista_usuario = []

    for gasto in gastos:
        if gasto.get("usuario") == usuario:
            lista_usuario.append(gasto)

    lista_usuario.sort(key=lambda g: g["data"], reverse=True)

    return lista_usuario[:limite]