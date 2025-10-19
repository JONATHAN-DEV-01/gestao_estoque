# src/config/database.py

import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST', 'db')
    db_name = os.getenv('DB_NAME')

    if not all([db_user, db_password, db_host, db_name]):
        raise ValueError("Erro: Variáveis de ambiente do banco de dados não foram configuradas.")

    # --- ALTERAÇÃO PRINCIPAL AQUI ---
    # Trocando o formato da URI de conexão para PostgreSQL
    database_uri = f'postgresql://{db_user}:{db_password}@{db_host}:5432/{db_name}'

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)