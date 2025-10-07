class Produto:
    def __init__(self, nome, preco, quantidade, imagem, vendedor_id, status="Ativo", id=None):
        self.id = id
        self.nome = nome
        self.preco = preco
        self.quantidade = quantidade
        self.status = status
        self.imagem = imagem
        self.vendedor_id = vendedor_id  

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "quantidade": self.quantidade,
            "status": self.status,
            "imagem": self.imagem,
            "vendedor_id": self.vendedor_id
        }