# src/Application/Service/venda_service.py (Modificado)

from src.Infrastructuree.venda_repository import VendaRepository
from src.Infrastructuree.vendedor_repository import VendedorRepository
from src.Infrastructuree.produto_repository import ProdutoRepository

class VendaService:
    def __init__(self):
        self.venda_repo = VendaRepository()
        self.vendedor_repo = VendedorRepository()
        self.produto_repo = ProdutoRepository()

    def registrar_venda_carrinho(self, carrinho_data, vendedor_id):
        # ... (seu método existente para registrar vendas) ...
        vendedor = self.vendedor_repo.get_by_id(vendedor_id)
        if not vendedor or vendedor.status != "Ativo":
            raise PermissionError("Vendedor inativo ou não encontrado. Não pode realizar vendas.")
        vendas_realizadas = self.venda_repo.registrar_venda_carrinho(carrinho_data, vendedor_id)
        return vendas_realizadas

    # --- NOVO MÉTODO DE DASHBOARD ADICIONADO ---
    def get_dashboard_summary(self, vendedor_id):
        """
        Busca e calcula todos os dados necessários para o dashboard do vendedor.
        """
        # 1. Busca os dados de resumo de vendas
        sales_data = self.venda_repo.get_sales_summary(vendedor_id)
        
        # 2. Busca os dados de resumo de produtos
        product_data = self.produto_repo.get_product_summary(vendedor_id)
        
        # 3. Busca os produtos mais vendidos
        top_products = self.venda_repo.get_top_selling_products(vendedor_id)

        # 4. Combina tudo em um único objeto de resposta
        return {
            "salesData": sales_data,
            "productData": product_data,
            "topProducts": top_products
        }