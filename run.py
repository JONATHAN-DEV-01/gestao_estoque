from flask import Flask
from src.config.database import db
from src.routes import init_routes
import os
from dotenv import load_dotenv


load_dotenv()

# Cria a instância da aplicação no escopo global
app = Flask(__name__)

# Configurações do banco de dados MySQL via variáveis de ambiente
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = 'db'  # Nome do serviço no docker-compose.yml
db_name = os.getenv('DB_NAME')

# String de conexão do SQLAlchemy para MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inicializa o SQLAlchemy e as rotas
db.init_app(app)
init_routes(app)

# Opcional: Para ambientes de produção, crie a tabela aqui
# com app.app_context():
#    db.create_all()

if __name__ == '__main__':
    # Este bloco só será executado quando você rodar 'python run.py'
    with app.app_context():
        db.create_all()
    app.run(debug=True)