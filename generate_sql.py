# generate_sql.py
import os
from dotenv import load_dotenv
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.schema import CreateTable

# Carrega config do .env para a string de conexão temporária
load_dotenv()
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
# Use localhost:5432 se estiver rodando o postgres localmente para este script
db_host = 'localhost' 
db_name = os.getenv('DB_NAME')
# String de conexão TEMPORÁRIA para PostgreSQL (pode ser um banco local ou qualquer um)
temp_db_uri = f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'

# Importe TODOS os seus modelos SQLAlchemy
from src.Infrastructuree.vendedor_model import VendedorModel
from src.Infrastructuree.produto_model import ProdutoModel
from src.Infrastructuree.venda_model import VendaModel
from src.Infrastructuree.token_blocklist_model import TokenBlocklistModel

# Crie um engine temporário do SQLAlchemy
engine = create_engine(temp_db_uri)

print("-- Script SQL para PostgreSQL --\n")

# Gera e imprime o comando CREATE TABLE para cada modelo
print(str(CreateTable(VendedorModel.__table__).compile(engine)))
print(";\n") # Adiciona ponto e vírgula entre as tabelas
print(str(CreateTable(ProdutoModel.__table__).compile(engine)))
print(";\n")
print(str(CreateTable(VendaModel.__table__).compile(engine)))
print(";\n")
print(str(CreateTable(TokenBlocklistModel.__table__).compile(engine)))
print(";\n")

print("-- Fim do Script --")