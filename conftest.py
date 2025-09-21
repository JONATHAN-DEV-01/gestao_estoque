import pytest
from run import app as flask_app 
from src.config.database import db

@pytest.fixture(scope='session')
def app():
    print("\nDEBUG: Configurando a aplicação para teste...")
    flask_app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "mysql+pymysql://gestao_estoque_user:Impacta1234@db:3306/gestao_estoque_test_db"
    })
    print("DEBUG: Configuração da aplicação CONCLUÍDA.")
    yield flask_app

@pytest.fixture(scope='session')
def client(app):
    print("DEBUG: Criando o cliente de teste...")
    return app.test_client()

@pytest.fixture(scope='session')
def init_database(app):
    print("DEBUG: Entrando na fixture init_database...")
    with app.app_context():
        print("DEBUG: Entrando no app_context...")
        print("DEBUG: Executando db.create_all()... (Pode travar aqui)")
        db.create_all()
        print("DEBUG: db.create_all() CONCLUÍDO.")
        yield db
        print("DEBUG: Iniciando db.drop_all()...")
        db.drop_all()
        print("DEBUG: db.drop_all() CONCLUÍDO.")