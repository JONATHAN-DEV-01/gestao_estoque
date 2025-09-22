# src/Application/Service/vendedor_service.py
import os
import random
from sqlalchemy import select
from src.config.database import db
from src.Infrastructuree.vendedor_model import VendedorModel
from src.Infrastructuree.token_blocklist_model import TokenBlocklistModel 
from flask_jwt_extended import create_access_token
from src.Infrastructuree.whatsapp.twilio import TwilioService

class VendedorService:
    @staticmethod
    def create_vendedor(array):
        codigo_ativacao = str(random.randint(1000, 9999))
        novo_vendedor = VendedorModel(
            nome=array["nome"],
            cnpj=array["cnpj"],
            email=array["email"],
            celular=array["celular"],
            senha=array["senha"],
            codigo_ativacao=codigo_ativacao
        )
        db.session.add(novo_vendedor)
        db.session.commit()

        try:
            twilio_service = TwilioService()
            verified_phone_number = os.getenv('VERIFIED_PHONE_NUMBER')
            twilio_service.send_whatsapp_code(verified_phone_number, codigo_ativacao)
        except Exception as e:
            print(f"ERRO ao chamar o TwilioService: {e}")

        return novo_vendedor
    
    @staticmethod
    def login_vendedor(email, senha):
        # ### ALTERADO ###: Usando o novo estilo de consulta
        stmt = select(VendedorModel).where(VendedorModel.email == email)
        vendedor = db.session.execute(stmt).scalar_one_or_none()

        if not vendedor or vendedor.senha != senha:
            raise ValueError("Email ou senha incorretos.")

        if vendedor.status != "Ativo":
            raise ValueError("Conta ainda não ativada.")

        access_token = create_access_token(identity=str(vendedor.id))
        
        return {
            "mensagem": "Login bem-sucedido!",
            "access_token": access_token
        }
    
    @staticmethod
    def logout(jti):
        # (Este método não usa consultas, então permanece igual)
        token_blocklist = TokenBlocklistModel(jti=jti)
        db.session.add(token_blocklist)
        db.session.commit()

    @staticmethod
    def activate_vendedor(vendedor_id, codigo_ativacao):
        # ### ALTERADO ###: Usando o novo estilo de consulta para buscar por ID
        vendedor = db.session.get(VendedorModel, vendedor_id)
        
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
        # ### ALTERADO ###: Usando o novo estilo de consulta
        stmt = select(VendedorModel)
        return db.session.execute(stmt).scalars().all()

    @staticmethod
    def get_vendedor(vendedor_id):
        # ### ALTERADO ###: Usando o novo estilo de consulta para buscar por ID
        vendedor = db.session.get(VendedorModel, vendedor_id)
        
        if not vendedor:
            raise ValueError("Vendedor não encontrado.")
        return vendedor

    @staticmethod
    def update_vendedor(vendedor_id, data):
        # ### ALTERADO ###: Usando o novo estilo de consulta para buscar por ID
        vendedor = db.session.get(VendedorModel, vendedor_id)

        if not vendedor:
            raise ValueError("Vendedor não encontrado.")
        
        for key, value in data.items():
            setattr(vendedor, key, value)
        
        db.session.commit()
        return vendedor

   
    @staticmethod
    def deactivate_vendedor(vendedor_id):
        """Desativa a conta de um vendedor, mudando seu status para 'Inativo'."""
        vendedor = db.session.get(VendedorModel, vendedor_id)

        if not vendedor:
            raise ValueError("Vendedor não encontrado.")

        if vendedor.status == "Inativo":
            raise ValueError("Esta conta já está inativa.")

        vendedor.status = "Inativo"
        db.session.commit()
        return vendedor

    @staticmethod
    def delete_vendedor(vendedor_id):
        # ### ALTERADO ###: Usando o novo estilo de consulta para buscar por ID
        vendedor = db.session.get(VendedorModel, vendedor_id)
        
        if vendedor:
            db.session.delete(vendedor)
            db.session.commit()
            return True
        else:
            raise ValueError("Vendedor não encontrado.")