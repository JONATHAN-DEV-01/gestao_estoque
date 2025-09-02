from flask import Flask
from src.config.database import db
from src.routes import init_routes
import os
from dotenv import load_dotenv

# Importa o modelo no escopo global para que o SQLAlchemy o reconheça
from src.Infrastructuree.vendedor_model import VendedorModel

# Carrega as variáveis de ambiente no escopo global
load_dotenv()

# Cria a instância da aplicação no escopo global
app = Flask(__name__)

# Configuração do banco de dados MySQL via variáveis de ambiente
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = 'db'
db_name = os.getenv('DB_NAME')

# String de conexão do SQLAlchemy para MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy e as rotas
db.init_app(app)
init_routes(app)

# Executa db.create_all() ao iniciar a aplicação no contêiner
with app.app_context():
    db.create_all()

# O Gunicorn usará este objeto 'app'
# O bloco 'if __name__ == '__main__'' é apenas para testes locais
if __name__ == '__main__':
    app.run(debug=True)