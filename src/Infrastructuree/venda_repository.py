# src/Infrastructure/venda_repository.py (Versão Corrigida)

import uuid
from sqlalchemy import select
from src.config.database import db
from src.Domain.venda_domain import Venda
from src.Infrastructuree.venda_model import VendaModel
from src.Infrastructuree.produto_model import ProdutoModel

class VendaRepository:
    def registrar_venda_carrinho(self, carrinho_data: dict, vendedor_id: int) -> list[Venda]:
        """
        Executa a transação completa de uma venda de múltiplos produtos.
        Valida, atualiza o estoque e registra as vendas de forma atômica.
        """
        transacao_id = str(uuid.uuid4())
        vendas_realizadas_domain = []
        
        try:
            # 1. Buscar todos os produtos do carrinho de uma vez para otimizar
            produtos_ids = [item['produto_id'] for item in carrinho_data['produtos']]
            produtos_db = db.session.query(ProdutoModel).filter(ProdutoModel.id.in_(produtos_ids)).all()
            produtos_map = {p.id: p for p in produtos_db}

            for item in carrinho_data['produtos']:
                produto_id = item.get('produto_id')
                quantidade = item.get('quantidade')
                
                produto_db = produtos_map.get(produto_id)

                # 2. Validações dentro da transação
                if not produto_db or produto_db.vendedor_id != vendedor_id:
                    raise ValueError(f"Produto com ID {produto_id} não encontrado ou não pertence a este vendedor.")
                if produto_db.status != "Ativo":
                    raise ValueError(f"Produto '{produto_db.nome}' está inativo.")
                if produto_db.quantidade < quantidade:
                    raise ValueError(f"Estoque insuficiente para '{produto_db.nome}'. Disponível: {produto_db.quantidade}")

                # 3. Atualiza o estoque no objeto do SQLAlchemy
                produto_db.quantidade -= quantidade

                # 4. Cria o registro da venda no SQLAlchemy
                nova_venda_db = VendaModel(
                    transacao_id=transacao_id,
                    produto_id=produto_id,
                    vendedor_id=vendedor_id,
                    quantidade=quantidade,
                    preco_unitario_venda=produto_db.preco
                )
                db.session.add(nova_venda_db)
                
                # Guarda o objeto de domínio para retornar ao usuário
                vendas_realizadas_domain.append(Venda(
                    id=None, # O ID só existirá após o commit
                    transacao_id=transacao_id,
                    produto_id=produto_id,
                    vendedor_id=vendedor_id,
                    quantidade=quantidade,
                    preco_unitario=produto_db.preco
                ))

            # 5. Se o loop terminou sem erros, commita tudo de uma vez
            db.session.commit()
            
            # Após o commit, os IDs são gerados, mas para esta resposta não é crucial retorná-los.
            return vendas_realizadas_domain

        except Exception as e:
            # 6. Se qualquer erro ocorreu, desfaz todas as alterações
            db.session.rollback()
            raise e # Levanta a exceção para a camada de serviço/controller tratar