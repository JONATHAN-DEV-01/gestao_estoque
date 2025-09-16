# src/Application/Service/vendedor_service.py
import os
import random
from src.config.database import db
from src.Infrastructuree.vendedor_model import VendedorModel
from flask_jwt_extended import create_access_token
from src.Infrastructuree.whatsapp.twilio import TwilioService 

twilio_service = TwilioService()
verified_phone_number = os.getenv('VERIFIED_PHONE_NUMBER')


class VendedorService:
    @staticmethod
    def create_vendedor(array):
        """Cria um novo vendedor e envia um código de ativação via WhatsApp."""
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

        twilio_service.send_whatsapp_code(verified_phone_number, codigo_ativacao)

        return novo_vendedor

    @staticmethod
    def login_vendedor(email, senha):
        vendedor = VendedorModel.query.filter_by(email=email).first()

        if not vendedor:
            raise ValueError("Email ou senha incorretos.")
        if vendedor.senha != senha:
            raise ValueError("Email ou senha incorretos.")

        if vendedor.status != "Ativo":
            raise ValueError("Conta ainda não ativada.")

        access_token = create_access_token(identity={"id": vendedor.id, "email": vendedor.email})
        return {
            "mensagem": "Login bem-sucedido!",
            "access_token": access_token
        }

    @staticmethod
    def activate_vendedor(vendedor_id, codigo_ativacao):
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
        return VendedorModel.query.all()

    @staticmethod
    def get_vendedor(vendedor_id):
        vendedor = VendedorModel.query.get(vendedor_id)
        if not vendedor:
            raise ValueError("Vendedor não encontrado.")
        return vendedor

    @staticmethod
    def update_vendedor(vendedor_id, data):
        vendedor = VendedorModel.query.get(vendedor_id)
        if not vendedor:
            raise ValueError("Vendedor não encontrado.")

        # Atualiza os campos normalmente (sem hash)
        for key, value in data.items():
            setattr(vendedor, key, value)

        db.session.commit()
        return vendedor

    @staticmethod
    def delete_vendedor(vendedor_id):
        vendedor = VendedorModel.query.get(vendedor_id)
        if vendedor:
            db.session.delete(vendedor)
            db.session.commit()
            return True
        else:
            raise ValueError("Vendedor não encontrado.")
