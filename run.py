from flask import Flask, jsonify
from src.config.database import db
from src.routes import init_routes
import os
from dotenv import load_dotenv
from src.Infrastructuree.vendedor_model import VendedorModel
# --- ADICIONADO ---
from src.Infrastructuree.token_blocklist_model import TokenBlocklistModel
# --------------------
from flask_jwt_extended import JWTManager
    
    

# --- 1. Inicialização e Carregamento de Configurações ---
load_dotenv()
app = Flask(__name__)

# --- 2. Configuração do Banco de Dados ---
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST', 'db') # Usar 'db' como padrão para Docker
db_name = os.getenv('DB_NAME')

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_user}:{db_password}@{db_host}:3306/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- 3. Configuração do JWT (JSON Web Token) ---
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "fallback_super_secret_key")
app.config["JWT_BLOCKLIST_ENABLED"] = True
app.config["JWT_BLOCKLIST_TOKEN_CHECKS"] = ["access"] # Verifica a blocklist para tokens de acesso
jwt = JWTManager(app)

# --- Callbacks do JWT ---

@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    """
    Callback que verifica se um token está na blocklist a cada requisição protegida.
    """
    jti = jwt_payload["jti"]
    token = TokenBlocklistModel.query.filter_by(jti=jti).first()
    return token is not None

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    """
    Define a resposta que será enviada quando um token revogado (na blocklist) for usado.
    """
    return jsonify({"msg": "Token has been revoked"}), 422

# --- 4. Inicialização dos Componentes da Aplicação ---
db.init_app(app)
init_routes(app)

# Cria as tabelas do banco de dados, se não existirem.
# Em um ambiente de produção, é melhor usar uma ferramenta de migração como Flask-Migrate.
with app.app_context():
    db.create_all()

# --- 5. Ponto de Entrada para Execução ---
if __name__ == '__main__':
    # O debug=True é ideal para desenvolvimento, mas deve ser False em produção.
    app.run(host='0.0.0.0', port=5000, debug=True)