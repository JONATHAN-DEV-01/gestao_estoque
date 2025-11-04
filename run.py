import os
from dotenv import load_dotenv
from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from src.config.database import db, init_db
from src.routes import init_routes
# As importações dos modelos não são mais necessárias aqui, pois `db.create_all()` foi removido.
# from src.Infrastructure.token_blocklist_model import TokenBlocklistModel

# --- 1. Inicialização ---
load_dotenv()
app = Flask(__name__)


# --- 2. Configuração do CORS (Cross-Origin Resource Sharing) ---
# Substitua pela URL real do seu deploy no Vercel.
VERCEL_URL = "https://stockflow-for-sellers.vercel.app" 

# Configura o CORS para permitir requisições APENAS do seu site no Vercel
# e do seu ambiente local (para você continuar testando).
CORS(app, resources={r"/*": {"origins": [VERCEL_URL, "http://localhost:8080"]}})


# --- 3. Configuração do Banco de Dados ---
init_db(app)


# --- 4. Configuração do JWT (JSON Web Token) ---
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "fallback_super_secret_key")
app.config["JWT_BLOCKLIST_ENABLED"] = True
app.config["JWT_BLOCKLIST_TOKEN_CHECKS"] = ["access"]
jwt = JWTManager(app)


# --- Callbacks do JWT ---
@jwt.token_in_blocklist_loader
def check_if_token_in_blocklist(jwt_header, jwt_payload):
    # Importa o modelo aqui para evitar importação circular e manter o escopo limpo.
    from src.Infrastructuree.token_blocklist_model import TokenBlocklistModel
    jti = jwt_payload["jti"]
    token = TokenBlocklistModel.query.filter_by(jti=jti).first()
    return token is not None

@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    return jsonify({"msg": "Token has been revoked"}), 422


# --- 5. Inicialização das Rotas ---
init_routes(app)

# A seção `with app.app_context(): db.create_all()` foi REMOVIDA.
# Em um ambiente de produção, o esquema do banco de dados é gerenciado
# por ferramentas de migração (neste caso, a Supabase CLI que já usamos).
# Manter `db.create_all()` aqui é redundante e pode causar inconsistências.


# --- 6. Ponto de Entrada para Execução ---
if __name__ == '__main__':
    # O modo debug é lido da variável de ambiente FLASK_DEBUG para flexibilidade.
    # Em produção (Render/Gunicorn), esta seção não é executada.
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() in ["true", "1"]
    app.run(host='0.0.0.0', port=5000, debug=debug_mode)