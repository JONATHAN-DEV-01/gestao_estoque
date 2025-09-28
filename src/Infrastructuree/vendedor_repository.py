# src/Infrastructure/vendedor_repository.py

from sqlalchemy import select
from src.config.database import db
from src.Domain.vendedor_domain import Vendedor
from src.Infrastructuree.vendedor_model import VendedorModel

class VendedorRepository:
    def add(self, vendedor_domain: Vendedor) -> Vendedor:
        """Adiciona um novo Vendedor ao banco de dados."""
        novo_vendedor_db = VendedorModel(
            nome=vendedor_domain.nome,
            cnpj=vendedor_domain.cnpj,
            email=vendedor_domain.email,
            celular=vendedor_domain.celular,
            senha=vendedor_domain.senha, # Lembrete: senha em texto puro
            status=vendedor_domain.status,
            codigo_ativacao=vendedor_domain.codigo_ativacao
        )
        db.session.add(novo_vendedor_db)
        db.session.commit()
        vendedor_domain.id = novo_vendedor_db.id # Atualiza o objeto de domínio com o ID do banco
        return vendedor_domain

    def get_by_email(self, email: str) -> Vendedor or None:
        """Busca um vendedor pelo email e retorna um objeto de domínio."""
        stmt = select(VendedorModel).where(VendedorModel.email == email)
        vendedor_db = db.session.execute(stmt).scalar_one_or_none()
        if vendedor_db:
            return self._to_domain(vendedor_db)
        return None

    def get_by_id(self, vendedor_id: int) -> Vendedor or None:
        """Busca um vendedor pelo ID e retorna um objeto de domínio."""
        vendedor_db = db.session.get(VendedorModel, vendedor_id)
        if vendedor_db:
            return self._to_domain(vendedor_db)
        return None

    def get_all(self) -> list[Vendedor]:
        """Retorna todos os vendedores como uma lista de objetos de domínio."""
        stmt = select(VendedorModel)
        vendedores_db = db.session.execute(stmt).scalars().all()
        return [self._to_domain(v) for v in vendedores_db]
    
    def update(self, vendedor_domain: Vendedor):
        """Atualiza um vendedor no banco de dados."""
        vendedor_db = db.session.get(VendedorModel, vendedor_domain.id)
        if vendedor_db:
            vendedor_db.nome = vendedor_domain.nome
            vendedor_db.cnpj = vendedor_domain.cnpj
            vendedor_db.email = vendedor_domain.email
            vendedor_db.celular = vendedor_domain.celular
            vendedor_db.status = vendedor_domain.status
            # Adicione outros campos que podem ser atualizados
            db.session.commit()

    def delete(self, vendedor_id: int):
        """Deleta um vendedor do banco de dados."""
        vendedor_db = db.session.get(VendedorModel, vendedor_id)
        if vendedor_db:
            db.session.delete(vendedor_db)
            db.session.commit()

    def _to_domain(self, vendedor_db: VendedorModel) -> Vendedor:
        """Converte um VendedorModel (SQLAlchemy) em um objeto Vendedor (Domínio)."""
        vendedor_domain = Vendedor(
            nome=vendedor_db.nome,
            cnpj=vendedor_db.cnpj,
            email=vendedor_db.email,
            celular=vendedor_db.celular,
            senha=vendedor_db.senha,
            status=vendedor_db.status,
            codigo_ativacao=vendedor_db.codigo_ativacao
        )
        vendedor_domain.id = vendedor_db.id
        return vendedor_domain