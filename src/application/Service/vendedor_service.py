# src/Application/Service/vendedor_service.py

import random
from ...config.database import db
from src.Infrastructuree.vendedor_model import VendedorModel

class VendedorService:
    @staticmethod
    def create_vendedor(nome, cnpj, email, celular, senha):
        """Cria um novo vendedor no banco de dados."""
        codigo_ativacao = str(random.randint(1000, 9999))
        
        # Cria a instância do modelo do banco de dados
        novo_vendedor = VendedorModel(
            nome=nome,
            cnpj=cnpj,
            email=email,
            celular=celular,
            senha=senha,
            codigo_ativacao=codigo_ativacao
        )

        # Adiciona o novo vendedor à sessão do banco de dados e salva
        db.session.add(novo_vendedor)
        db.session.commit()
        
        print(f"Código de ativação para o vendedor '{nome}' enviado para o celular '{celular}': {codigo_ativacao}")
        
        return novo_vendedor

    @staticmethod
    def activate_vendedor(vendedor_id, codigo_ativacao):
        """Ativa a conta do vendedor verificando o código de ativação."""
        vendedor = VendedorModel.query.get(vendedor_id)

        if not vendedor:
            raise ValueError("Vendedor não encontrado.")

        if vendedor.status == "Ativo":
            raise ValueError("Conta já está ativa.")
        
        if vendedor.codigo_ativacao != codigo_ativacao:
            raise ValueError("Código de ativação incorreto.")

        vendedor.status = "Ativo"
        db.session.commit()
        return vendedor

    @staticmethod
    def get_all_vendedores():
        """Retorna todos os vendedores do banco de dados."""
        return VendedorModel.query.all()

    @staticmethod
    def get_vendedor(vendedor_id):
        """Busca um vendedor específico pelo ID."""
        vendedor = VendedorModel.query.get(vendedor_id)
        if not vendedor:
            raise ValueError("Vendedor não encontrado.")
        return vendedor

    @staticmethod
    def update_vendedor(vendedor_id, data):
        """Atualiza os dados de um vendedor existente."""
        vendedor = VendedorModel.query.get(vendedor_id)
        if not vendedor:
            raise ValueError("Vendedor não encontrado.")
        
        for key, value in data.items():
            setattr(vendedor, key, value)
        
        db.session.commit()
        return vendedor

    @staticmethod
    def delete_vendedor(vendedor_id):
        """Deleta um vendedor pelo ID."""
        vendedor = VendedorModel.query.get(vendedor_id)
        if vendedor:
            db.session.delete(vendedor)
            db.session.commit()
            return True
        else:
            raise ValueError("Vendedor não encontrado.")