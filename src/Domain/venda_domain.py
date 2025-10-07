from datetime import datetime

class Venda:
    def __init__(self, produto_id, vendedor_id, quantidade, preco_unitario, transacao_id, id=None, data_venda=None):
        self.id = id
        self.produto_id = produto_id
        self.vendedor_id = vendedor_id
        self.quantidade = quantidade
        self.preco_unitario = preco_unitario
        self.preco_total = preco_unitario * quantidade
        self.data_venda = data_venda or datetime.utcnow()
        self.transacao_id = transacao_id 

    def to_dict(self):
        return {
            "id": self.id,
            "transacao_id": self.transacao_id,
            "produto_id": self.produto_id,
            "vendedor_id": self.vendedor_id,
            "quantidade": self.quantidade,
            "preco_unitario": self.preco_unitario,
            "preco_total": self.preco_total,
            "data_venda": self.data_venda.isoformat()
        }