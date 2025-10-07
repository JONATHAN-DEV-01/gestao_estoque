from src.Domain.produto_domain import Produto
from src.Infrastructuree.produto_repository import ProdutoRepository

class ProdutoService:
    def __init__(self):
        self.repository = ProdutoRepository()

    def create_produto(self, data, vendedor_id):
        # A regra de que o produto pertence ao vendedor é aplicada aqui
        produto_domain = Produto(
            nome=data.get('nome'),
            preco=data.get('preco'),
            quantidade=data.get('quantidade'),
            imagem=data.get('imagem'),
            vendedor_id=vendedor_id # ID do vendedor logado
        )
        return self.repository.add(produto_domain)

    def get_all_produtos_by_vendedor(self, vendedor_id):
        return self.repository.get_all_by_vendedor(vendedor_id)

    def get_produto_by_id(self, produto_id, vendedor_id):
        produto = self.repository.get_by_id_and_vendedor(produto_id, vendedor_id)
        if not produto:
            raise ValueError("Produto não encontrado ou não pertence a este vendedor.")
        return produto

    def update_produto(self, produto_id, data, vendedor_id):
        produto = self.repository.get_by_id_and_vendedor(produto_id, vendedor_id)
        if not produto:
            raise ValueError("Produto não encontrado ou não pertence a este vendedor.")
        
        # Atualiza os campos do objeto de domínio
        produto.nome = data.get('nome', produto.nome)
        produto.preco = data.get('preco', produto.preco)
        produto.quantidade = data.get('quantidade', produto.quantidade)
        produto.imagem = data.get('imagem', produto.imagem)

        self.repository.update(produto)
        return produto

    def inativar_produto(self, produto_id, vendedor_id):
        produto = self.repository.get_by_id_and_vendedor(produto_id, vendedor_id)
        if not produto:
            raise ValueError("Produto não encontrado ou não pertence a este vendedor.")

        produto.status = "Inativo"
        self.repository.update(produto)
        return produto
    
    def ativar_produto(self, produto_id, vendedor_id):
        produto = self.repository.get_by_id_and_vendedor(produto_id, vendedor_id)
        if not produto:
            raise ValueError("Produto não encontrado ou não pertence a este vendedor.")

        produto.status = "Ativo"
        self.repository.update(produto)
        return produto