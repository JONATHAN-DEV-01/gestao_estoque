from flask import Flask
from src.config.database import db
from src.routes import init_routes
import os

# Configurações do banco de dados SQLite
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'database.db')

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializa o SQLAlchemy
    db.init_app(app)

    # Inicializa as rotas
    init_routes(app)

    return app

if __name__ == '__main__':
    app = create_app()

    # Cria as tabelas do banco de dados
    with app.app_context():
        db.create_all()

    app.run(debug=True)