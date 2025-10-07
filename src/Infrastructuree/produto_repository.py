from sqlalchemy import select
from src.config.database import db
from src.Domain.produto_domain import Produto
from src.Infrastructuree.produto_model import ProdutoModel

class ProdutoRepository:
    def add(self, produto_domain: Produto) -> Produto:
        novo_produto_db = ProdutoModel(
            nome=produto_domain.nome,
            preco=produto_domain.preco,
            quantidade=produto_domain.quantidade,
            status=produto_domain.status,
            imagem=produto_domain.imagem,
            vendedor_id=produto_domain.vendedor_id
        )
        db.session.add(novo_produto_db)
        db.session.commit()
        produto_domain.id = novo_produto_db.id
        return produto_domain

    def get_by_id_and_vendedor(self, produto_id: int, vendedor_id: int) -> Produto or None:
        stmt = select(ProdutoModel).where(ProdutoModel.id == produto_id, ProdutoModel.vendedor_id == vendedor_id)
        produto_db = db.session.execute(stmt).scalar_one_or_none()
        if produto_db:
            return self._to_domain(produto_db)
        return None

    def get_all_by_vendedor(self, vendedor_id: int) -> list[Produto]:
        stmt = select(ProdutoModel).where(ProdutoModel.vendedor_id == vendedor_id)
        produtos_db = db.session.execute(stmt).scalars().all()
        return [self._to_domain(p) for p in produtos_db]

    def update(self, produto_domain: Produto):
        produto_db = db.session.get(ProdutoModel, produto_domain.id)
        if produto_db and produto_db.vendedor_id == produto_domain.vendedor_id:
            produto_db.nome = produto_domain.nome
            produto_db.preco = produto_domain.preco
            produto_db.quantidade = produto_domain.quantidade
            produto_db.status = produto_domain.status
            produto_db.imagem = produto_domain.imagem
            db.session.commit()

    def _to_domain(self, produto_db: ProdutoModel) -> Produto:
        return Produto(
            id=produto_db.id,
            nome=produto_db.nome,
            preco=produto_db.preco,
            quantidade=produto_db.quantidade,
            status=produto_db.status,
            imagem=produto_db.imagem,
            vendedor_id=produto_db.vendedor_id
        )