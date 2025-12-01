import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_db(app):
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST', 'db')
    db_name = os.getenv('DB_NAME')
    
    # --- ALTERAÇÃO AQUI ---
    # Adicionamos uma variável para a porta. Se não existir no .env, usa 5432 (padrão local).
    # No Render, você adicionará a variável de ambiente DB_PORT com valor 6543.
    db_port = os.getenv('DB_PORT', '5432') 

    if not all([db_user, db_password, db_host, db_name]):
        raise ValueError("Erro: Variáveis de ambiente do banco de dados não foram configuradas.")

    # Usamos a variável db_port na string de conexão
    database_uri = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)