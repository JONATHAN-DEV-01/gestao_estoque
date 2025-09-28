import os
import random
from flask_jwt_extended import create_access_token
from src.Domain.vendedor_domain import Vendedor
from src.Infrastructuree.vendedor_repository import VendedorRepository
from src.Infrastructuree.token_blocklist_model import TokenBlocklistModel
from src.Infrastructuree.whatsapp.twilio import TwilioService
from src.config.database import db 

class VendedorService:
    def __init__(self):
        self.repository = VendedorRepository()

    def create_vendedor(self, array):
        codigo_ativacao = str(random.randint(1000, 9999))
        
        # ### ALTERAÇÃO ###: Cria um objeto de DOMÍNIO, não de MODEL
        novo_vendedor_domain = Vendedor(
            nome=array["nome"],
            cnpj=array["cnpj"],
            email=array["email"],
            celular=array["celular"],
            senha=array["senha"],
            codigo_ativacao=codigo_ativacao
        )

        # ### ALTERAÇÃO ###: Delega a persistência para o repositório
        vendedor_criado = self.repository.add(novo_vendedor_domain)

        try:
            twilio_service = TwilioService()
            verified_phone_number = os.getenv('VERIFIED_PHONE_NUMBER')
            twilio_service.send_whatsapp_code(verified_phone_number, codigo_ativacao)
        except Exception as e:
            print(f"ERRO ao chamar o TwilioService: {e}")

        return vendedor_criado

    def login_vendedor(self, email, senha):
        vendedor = self.repository.get_by_email(email)

        if not vendedor or vendedor.senha != senha:
            raise ValueError("Email ou senha incorretos.")

        if vendedor.status != "Ativo":
            raise ValueError("Conta ainda não ativada.")

        access_token = create_access_token(identity=str(vendedor.id))
        return { "mensagem": "Login bem-sucedido!", "access_token": access_token }
    
    def activate_vendedor(self, vendedor_id, codigo_ativacao):
        vendedor = self.repository.get_by_id(vendedor_id)
        
        if not vendedor:
            raise ValueError("Vendedor não encontrado.")
        if vendedor.status == "Ativo":
            raise ValueError("Conta já está ativa.")
        if vendedor.codigo_ativacao != codigo_ativacao:
            raise ValueError("Código de ativação incorreto.")
        
        vendedor.status = "Ativo"
        self.repository.update(vendedor) # Delega a atualização
        return vendedor

    def deactivate_vendedor(self, vendedor_id):
        vendedor = self.repository.get_by_id(vendedor_id)

        if not vendedor:
            raise ValueError("Vendedor não encontrado.")
        if vendedor.status == "Inativo":
            raise ValueError("Esta conta já está inativa.")

        vendedor.status = "Inativo"
        self.repository.update(vendedor) # Delega a atualização
        return vendedor

    def get_all_vendedores(self):
        return self.repository.get_all()

    def get_vendedor(self, vendedor_id):
        vendedor = self.repository.get_by_id(vendedor_id)
        if not vendedor:
            raise ValueError("Vendedor não encontrado.")
        return vendedor

    def update_vendedor(self, vendedor_id, data):
        vendedor = self.repository.get_by_id(vendedor_id)
        if not vendedor:
            raise ValueError("Vendedor não encontrado.")
        
        # Atualiza o objeto de domínio com os novos dados
        for key, value in data.items():
            if hasattr(vendedor, key):
                setattr(vendedor, key, value)
        
        self.repository.update(vendedor) # Delega a atualização
        return vendedor

    def delete_vendedor(self, vendedor_id):
        vendedor = self.repository.get_by_id(vendedor_id)
        if not vendedor:
            raise ValueError("Vendedor não encontrado.")
        self.repository.delete(vendedor_id)
        return True

    # Este método ainda usa o db.session, poderia ser refatorado também
    @staticmethod
    def logout(jti):
        token_blocklist = TokenBlocklistModel(jti=jti)
        db.session.add(token_blocklist)
        db.session.commit()