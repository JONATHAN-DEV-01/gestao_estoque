# src/Infrastructure/venda_repository.py (Versão Corrigida)
from sqlalchemy import func, desc
from datetime import date
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
    
    
    def get_sales_summary(self, vendedor_id: int) -> dict:
        """
        Calcula o resumo de vendas (Total de vendas, Valor Total, Ticket Médio)
        para um vendedor específico.
        """
        # Calcula a soma dos totais das vendas
        total_value_query = db.session.query(
            func.sum(VendaModel.preco_unitario_venda * VendaModel.quantidade)
        ).filter(VendaModel.vendedor_id == vendedor_id)
        
        # Calcula o número de transações (grupos de venda)
        total_sales_query = db.session.query(
            func.count(func.distinct(VendaModel.transacao_id))
        ).filter(VendaModel.vendedor_id == vendedor_id)

        # --- NOVA CONSULTA PARA VENDAS HOJE ---
        vendas_hoje_query = db.session.query(
            func.count(func.distinct(VendaModel.transacao_id))
        ).filter(
            VendaModel.vendedor_id == vendedor_id,
            # Compara se a data da coluna 'data_venda' é igual à data de hoje
            func.date(VendaModel.data_venda) == date.today()
        )
        # ------------------------------------

        valor_total = total_value_query.scalar() or 0
        total_vendas = total_sales_query.scalar() or 0
        vendas_hoje = vendas_hoje_query.scalar() or 0 # <-- LINHA ATUALIZADA
        
        ticket_medio = (valor_total / total_vendas) if total_vendas > 0 else 0

        return {
            "totalVendas": total_vendas,
            "valorTotal": valor_total,
            "ticketMedio": ticket_medio,
            "vendaHoje": vendas_hoje # <-- Agora envia o valor real
        }

    def get_top_selling_products(self, vendedor_id: int) -> list:
        """
        Retorna os 5 produtos mais vendidos por valor total para um vendedor.
        """
        query = db.session.query(
            ProdutoModel.nome,
            func.sum(VendaModel.quantidade).label('vendas'),
            func.sum(VendaModel.preco_unitario_venda * VendaModel.quantidade).label('valor')
        ).join(
            ProdutoModel, VendaModel.produto_id == ProdutoModel.id
        ).filter(
            VendaModel.vendedor_id == vendedor_id
        ).group_by(
            ProdutoModel.id, ProdutoModel.nome
        ).order_by(
            desc('valor') # Ordena pelo valor total
        ).limit(5)
        
        top_products_raw = query.all()
        
        # Converte o resultado para o formato de dicionário que o front-end espera
        return [
            {"nome": nome, "vendas": int(vendas), "valor": float(valor)}
            for nome, vendas, valor in top_products_raw
        ]
    def get_all_by_vendedor(self, vendedor_id: int):
        """
        Busca todas as vendas de um vendedor, trazendo também o nome do produto.
        """
        # Fazemos um JOIN para pegar o nome do produto na mesma consulta
        results = db.session.query(VendaModel, ProdutoModel.nome).join(
            ProdutoModel, VendaModel.produto_id == ProdutoModel.id
        ).filter(
            VendaModel.vendedor_id == vendedor_id
        ).order_by(
            desc(VendaModel.data_venda)
        ).all()
        
        # Formatamos a saída para facilitar o uso no front-end
        lista_vendas = []
        for venda, produto_nome in results:
            venda_dict = {
                "id": venda.id,
                "transacao_id": venda.transacao_id,
                "produto_id": venda.produto_id,
                "produto_nome": produto_nome, # Nome do produto
                "quantidade": venda.quantidade,
                "preco_unitario": venda.preco_unitario_venda,
                "total": venda.quantidade * venda.preco_unitario_venda,
                "data_venda": venda.data_venda.isoformat()
            }
            lista_vendas.append(venda_dict)
            
        return lista_vendas

    def cancelar_venda(self, venda_id: int, vendedor_id: int):
        """
        Cancela uma venda: Deleta o registro e devolve os produtos ao estoque.
        """
        try:
            # 1. Busca a venda garantindo que pertence ao vendedor
            venda = db.session.get(VendaModel, venda_id)
            
            if not venda:
                raise ValueError("Venda não encontrada.")
            
            if venda.vendedor_id != vendedor_id:
                raise PermissionError("Você não tem permissão para cancelar esta venda.")

            # 2. Busca o produto para devolver o estoque
            produto = db.session.get(ProdutoModel, venda.produto_id)
            
            if produto:
                # AQUI ACONTECE O ESTORNO
                produto.quantidade += venda.quantidade
            
            # 3. Deleta o registro da venda
            db.session.delete(venda)
            
            # 4. Confirma a transação (Estorno + Delete)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback() # Desfaz tudo se der erro
            raise e