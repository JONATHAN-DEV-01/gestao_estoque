import os
from flask_sqlalchemy import SQLAlchemy

# A instância do SQLAlchemy continua a ser criada aqui
db = SQLAlchemy()

def init_db(app):
    """
    Lê as variáveis de ambiente e configura o banco de dados para a aplicação Flask.
    """
    # Carrega as credenciais do banco de dados a partir do .env
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST', 'db')
    db_name = os.getenv('DB_NAME')

    # Validação para garantir que as variáveis foram carregadas
    if not all([db_user, db_password, db_host, db_name]):
        raise ValueError("Erro: Variáveis de ambiente do banco de dados não foram configuradas.")

    # Constrói a string de conexão do banco de dados
    database_uri = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}'

    # Aplica as configurações ao objeto da aplicação Flask
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o SQLAlchemy com a aplicação, conectando tudo
    db.init_app(app)