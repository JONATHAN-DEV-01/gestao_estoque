# tests/test_vendedores.py (Versão Corrigida e Refatorada)

import pytest
import json
from unittest.mock import patch
from src.config.database import db

# --- Fixtures: Funções de ajuda que preparam o ambiente para os testes ---

@pytest.fixture(scope="module")
def vendedor_data():
    """Fornece dados consistentes para o vendedor em todos os testes do módulo."""
    return {
        "nome": "Vendedor de Teste Refatorado",
        "cnpj": "55.666.777/0001-88",
        "email": "teste-refatorado@vendedor.com",
        "celular": "+5511977776666",
        "senha": "senhaSegura456"
    }

@pytest.fixture(scope="module")
def vendedor_id(client, init_database, vendedor_data):
    """
    Cria um vendedor no início dos testes e retorna seu ID.
    O mock é aplicado aqui para afetar apenas a criação.
    """
    with patch('src.application.Service.vendedor_service.TwilioService') as mock_twilio:
        mock_instance = mock_twilio.return_value
        mock_instance.send_whatsapp_code.return_value = None
        
        response = client.post('/vendedores', data=json.dumps(vendedor_data), content_type='application/json')
        assert response.status_code == 201
        return response.json['vendedor']['id']

@pytest.fixture(scope="module")
def active_vendedor(init_database, vendedor_id):
    """Ativa a conta do vendedor para permitir o login nos testes seguintes."""
    from src.Infrastructuree.vendedor_model import VendedorModel
    vendedor = db.session.get(VendedorModel, vendedor_id)
    vendedor.status = "Ativo"
    init_database.session.commit()
    return vendedor_id

@pytest.fixture(scope="module")
def auth_headers(client, vendedor_data, active_vendedor):
    """Faz o login do vendedor ativado e retorna os headers de autorização."""
    login_data = {"email": vendedor_data['email'], "senha": vendedor_data['senha']}
    response = client.post('/login', data=json.dumps(login_data), content_type='application/json')
    assert response.status_code == 200
    access_token = response.json['access_token']
    return {'Authorization': f'Bearer {access_token}'}


# --- Testes Granulares: Uma função para cada rota/cenário ---

def test_health_check(client):
    """Testa se a rota /api está funcionando."""
    response = client.get('/api')
    assert response.status_code == 200
    assert response.json['mensagem'] == "API - OK; Docker - Up"

def test_create_vendedor_route_works(vendedor_id):
    """Testa se a criação do vendedor (feita na fixture) funcionou."""
    assert vendedor_id is not None

def test_login_vendedor_route_works(auth_headers):
    """Testa se o login (feito na fixture) e a geração de token funcionaram."""
    assert 'Authorization' in auth_headers
    assert 'Bearer' in auth_headers['Authorization']

def test_get_all_vendedores_protected(client, auth_headers):
    """Testa se a rota GET /vendedores está protegida e retorna uma lista."""
    response = client.get('/vendedores', headers=auth_headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_vendedor_by_id_protected(client, auth_headers, vendedor_id):
    """Testa se a rota GET /vendedores/<id> retorna o vendedor correto."""
    response = client.get(f'/vendedores/{vendedor_id}', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['id'] == vendedor_id

def test_logout(client, auth_headers):
    """Testa se a rota de logout funciona e invalida o token."""
    # Faz o logout
    response = client.post('/logout', headers=auth_headers)
    assert response.status_code == 200
    assert response.json['mensagem'] == "Logout bem-sucedido"

    # Tenta usar o mesmo token novamente
    response = client.get('/vendedores', headers=auth_headers)
    assert response.status_code == 422 # Espera "Token revogado"
    assert response.json['msg'] == 'Token has been revoked'

def test_delete_vendedor(client, vendedor_data, active_vendedor):
    """Testa se um vendedor pode ser deletado e se ele realmente some."""
    # Precisa de um novo token, pois o anterior foi invalidado no teste de logout
    login_data = {"email": vendedor_data['email'], "senha": vendedor_data['senha']}
    response = client.post('/login', data=json.dumps(login_data), content_type='application/json')
    new_token = response.json['access_token']
    headers = {'Authorization': f'Bearer {new_token}'}

    # Deleta o vendedor
    response = client.delete(f'/vendedores/{active_vendedor}', headers=headers)
    assert response.status_code == 200
    assert response.json['mensagem'] == "Vendedor excluído com sucesso"

    # Verifica se ele não existe mais
    response = client.get(f'/vendedores/{active_vendedor}', headers=headers)
    assert response.status_code == 404

def test_acesso_negado_sem_token(client):
    """Testa se as rotas protegidas retornam 401 Unauthorized sem um token."""
    response = client.get('/vendedores')
    assert response.status_code == 401