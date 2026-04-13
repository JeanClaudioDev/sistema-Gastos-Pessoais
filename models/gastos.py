from uuid import uuid4
from datetime import datetime

class Gasto:
    def __init__(self, descricao, valor, data, categoria, id=None):

        if isinstance(data, str):
            data = datetime.strptime(data, "%d/%m/%Y")

        self.descricao = descricao
        self.valor = float(valor)
        self.data = data
        self.categoria = categoria
        self.id = id if id else str(uuid4())

    def to_dict(self):
        return {
            "descricao": self.descricao,
            "valor": self.valor,
            "data": self.data.strftime("%d/%m/%Y"),
            "categoria": self.categoria,
            "id": self.id
        }

    @classmethod
    def from_dict(cls, dados):
        return cls(
            dados["descricao"],
            dados["valor"],
            dados["data"],
            dados["categoria"],
            dados["id"]
        )