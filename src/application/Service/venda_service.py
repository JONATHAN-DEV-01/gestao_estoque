# src/Application/Service/venda_service.py (Versão Simplificada e Corrigida)

from src.Infrastructuree.venda_repository import VendaRepository
from src.Infrastructuree.vendedor_repository import VendedorRepository

class VendaService:
    def __init__(self):
        self.venda_repo = VendaRepository()
        self.vendedor_repo = VendedorRepository()

    def registrar_venda_carrinho(self, carrinho_data, vendedor_id):
        # Validação de negócio inicial: O vendedor pode vender?
        vendedor = self.vendedor_repo.get_by_id(vendedor_id)
        if not vendedor or vendedor.status != "Ativo":
            raise PermissionError("Vendedor inativo ou não encontrado. Não pode realizar vendas.")

        # Delega a transação complexa e as validações de produto para o repositório
        vendas_realizadas = self.venda_repo.registrar_venda_carrinho(carrinho_data, vendedor_id)
        
        return vendas_realizadas