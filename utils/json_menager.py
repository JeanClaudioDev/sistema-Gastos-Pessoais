import json

ARQUIVO = "data/gastos.json"


def carregar_gastos():

    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except FileNotFoundError:
        return []


def salvar_gastos(lista_gasto):

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(lista_gasto, arquivo, indent=4, ensure_ascii=False)


def adicionar_gasto(gasto):

    gastos = carregar_gastos()

    gastos.append(gasto)

    salvar_gastos(gastos)


def listar_gastos():

    return carregar_gastos()