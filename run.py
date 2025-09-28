# run.py (Refatorado)

import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from src.config.database import db, init_db
from src.routes import init_routes
from src.Infrastructuree.vendedor_model import VendedorModel
from src.Infrastructuree.token_blocklist_model import TokenBlocklistModel

# --- 1. Inicialização ---
load_dotenv()
app = Flask(__name__)


# --- 2. Configuração do Banco de Dados ---
# ### ALTERAÇÃO ###: A lógica complexa foi removida מכאן e substituída por uma única chamada de função
init_db(app)


# --- 3. Configuração do JWT (JSON Web Token) ---
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "fallback_super_secret_key")
app.config["JWT_BLOCKLIST_ENABLED"] = True
app.config["JWT_BLOCKLIST_TOKEN_CHECKS"] = ["access"]
jwt = JWTManager(app)


# --- Callbacks do JWT ---
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    token = TokenBlocklistModel.query.filter_by(jti=jti).first()
    return token is not None

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"msg": "Token has been revoked"}), 422


# --- 4. Inicialização das Rotas e Tabelas ---
init_routes(app)

with app.app_context():
    db.create_all()


# --- 5. Ponto de Entrada para Execução ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)