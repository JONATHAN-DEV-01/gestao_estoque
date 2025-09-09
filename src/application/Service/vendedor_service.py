# src/Application/Service/vendedor_service.py

import os
import random
import uuid
from twilio.rest import Client
from src.config.database import db
from src.Infrastructuree.vendedor_model import VendedorModel

# Variáveis do Twilio do seu arquivo .env
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_whatsapp_number = os.getenv('TWILIO_WHATSAPP_NUMBER')
# Adicione esta linha para ler o número verificado
verified_phone_number = os.getenv('VERIFIED_PHONE_NUMBER')

class VendedorService:
    @staticmethod
    def create_vendedor(nome, cnpj, email, celular, senha):
        """Cria um novo vendedor e envia um código de ativação via WhatsApp."""
        codigo_ativacao = str(random.randint(1000, 9999))
        
        novo_vendedor = VendedorModel(
            nome=nome,
            cnpj=cnpj,
            email=email,
            celular=celular,
            senha=senha,
            codigo_ativacao=codigo_ativacao
        )

        db.session.add(novo_vendedor)
        db.session.commit()
        
        client = Client(account_sid, auth_token)
        
        try:
            message = client.messages.create(
                from_=twilio_whatsapp_number,
                body=f'O código de ativação do Mini Mercado é: {codigo_ativacao}',
                # Use o número verificado aqui
                to=verified_phone_number
            )
            print(f"Mensagem enviada com sucesso! SID: {message.sid}")
        except Exception as e:
            print(f"Erro ao enviar mensagem via Twilio: {e}")
            raise RuntimeError("Não foi possível enviar o código de ativação. Tente novamente.")
        
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