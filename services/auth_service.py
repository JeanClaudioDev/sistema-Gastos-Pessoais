import json

ARQUIVO_USUARIOS = "data/usuarios.json"


def autenticar(usuario, senha):

    try:
        with open(ARQUIVO_USUARIOS, "r", encoding="utf-8") as f:
            usuarios = json.load(f)
    except:
        return None

    for u in usuarios:
        if u["usuario"] == usuario and u["senha"] == senha:
            return u

    return None