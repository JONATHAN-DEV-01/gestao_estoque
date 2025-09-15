from flask import Flask
from src.config.database import db
from src.routes import init_routes
import os
from dotenv import load_dotenv
from src.Infrastructuree.vendedor_model import VendedorModel
from flask_jwt_extended import JWTManager

# Carrega variáveis de ambiente
load_dotenv()

# Cria a instância da aplicação
app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "chave_super_secreta_trocar")  
jwt = JWTManager(app)

# Configurações do banco de dados MySQL via variáveis de ambiente
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

# Cria tabelas automaticamente (apenas em dev)
with app.app_context():
    db.create_all()

# Gunicorn usa 'app' como entrypoint
if __name__ == '__main__':
    app.run(debug=True)