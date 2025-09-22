import pytest
import json
from unittest.mock import patch
from src.config.database import db
from src.Infrastructuree.vendedor_model import VendedorModel

# --- Fixture Principal: Prepara todo o ambiente uma única vez ---

@pytest.fixture(scope="session")
def initial_setup(client, init_database):
    """
    Executado uma vez por sessão. Cria, ativa e faz login de dois vendedores
    para serem usados em todos os testes.
    """
    with patch('src.application.Service.vendedor_service.TwilioService') as mock_twilio:
        mock_instance = mock_twilio.return_value
        mock_instance.send_whatsapp_code.return_value = None

        # --- Vendedor 1 (Admin) ---
        admin_data = {
            "nome": "Vendedor Admin", "cnpj": "11.111.111/0001-11",
            "email": "admin@teste.com", "celular": "+5511911111111", "senha": "senhaAdmin"
        }
        response = client.post('/vendedores', data=json.dumps(admin_data), content_type='application/json')
        assert response.status_code == 201
        admin_id = response.json['vendedor']['id']
        
        admin_user = db.session.get(VendedorModel, admin_id)
        admin_user.status = "Ativo"
        db.session.commit()

        login_resp_admin = client.post('/login', data=json.dumps({"email": admin_data['email'], "senha": admin_data['senha']}), content_type='application/json')
        admin_token = login_resp_admin.json['access_token']

        # --- Vendedor 2 (Comum) ---
        comum_data = {
            "nome": "Vendedor Comum", "cnpj": "22.222.222/0001-22",
            "email": "comum@teste.com", "celular": "+5511922222222", "senha": "senhaComum"
        }
        response = client.post('/vendedores', data=json.dumps(comum_data), content_type='application/json')
        assert response.status_code == 201
        comum_id = response.json['vendedor']['id']

        comum_user = db.session.get(VendedorModel, comum_id)
        comum_user.status = "Ativo"
        db.session.commit()
        
        login_resp_comum = client.post('/login', data=json.dumps({"email": comum_data['email'], "senha": comum_data['senha']}), content_type='application/json')
        comum_token = login_resp_comum.json['access_token']

        # Retorna todos os dados preparados para os testes
        yield {
            "admin": {"id": admin_id, "token": admin_token, "data": admin_data},
            "comum": {"id": comum_id, "token": comum_token, "data": comum_data}
        }

# --- Testes que usam os dados preparados ---

def test_health_check(client):
    """Testa a rota de status da API."""
    response = client.get('/api')
    assert response.status_code == 200

def test_get_all_vendedores(client, initial_setup):
    """Testa se a listagem de vendedores funciona e retorna os 2 criados."""
    admin_headers = {'Authorization': f'Bearer {initial_setup["admin"]["token"]}'}
    response = client.get('/vendedores', headers=admin_headers)
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) >= 2 # Pelo menos 2 que criamos

def test_get_one_vendedor(client, initial_setup):
    """Testa a busca de um vendedor específico."""
    admin_headers = {'Authorization': f'Bearer {initial_setup["admin"]["token"]}'}
    comum_id = initial_setup["comum"]["id"]
    response = client.get(f'/vendedores/{comum_id}', headers=admin_headers)
    assert response.status_code == 200
    assert response.json['id'] == comum_id

def test_update_vendedor(client, initial_setup):
    """Testa a atualização de um vendedor."""
    admin_headers = {'Authorization': f'Bearer {initial_setup["admin"]["token"]}'}
    comum_id = initial_setup["comum"]["id"]
    update_data = {"nome": "Vendedor Comum (Nome Alterado)"}
    
    response = client.put(f'/vendedores/{comum_id}', headers=admin_headers, data=json.dumps(update_data), content_type='application/json')
    assert response.status_code == 200
    assert response.json['nome'] == "Vendedor Comum (Nome Alterado)"

def test_deactivate_vendedor(client, initial_setup):
    """Testa a desativação de uma conta."""
    admin_headers = {'Authorization': f'Bearer {initial_setup["admin"]["token"]}'}
    comum_id = initial_setup["comum"]["id"]
    
    response = client.post(f'/vendedores/{comum_id}/deactivate', headers=admin_headers)
    assert response.status_code == 200
    assert response.json['vendedor']['status'] == "Inativo"

def test_login_fails_after_deactivation(client, initial_setup):
    """Testa que o login falha para uma conta desativada."""
    comum_data = initial_setup["comum"]["data"]
    login_data = {"email": comum_data['email'], "senha": comum_data['senha']}
    response = client.post('/login', data=json.dumps(login_data), content_type='application/json')
    assert response.status_code == 401
    assert "Conta ainda não ativada" in response.json['erro']


def test_delete_vendedor(client, initial_setup):
    """Testa a exclusão de um vendedor usando o token de outro."""
    # O Vendedor Admin deleta o Vendedor Comum
    admin_headers = {'Authorization': f'Bearer {initial_setup["admin"]["token"]}'}
    comum_id = initial_setup["comum"]["id"]

    # Deleta o vendedor "comum"
    response = client.delete(f'/vendedores/{comum_id}', headers=admin_headers)
    assert response.status_code == 200
    
    # Verifica se ele foi realmente deletado
    response_after = client.get(f'/vendedores/{comum_id}', headers=admin_headers)
    assert response_after.status_code == 404

def test_acesso_negado_sem_token(client):
    """Testa a segurança da rota, que não deve permitir acesso sem token."""
    response = client.get('/vendedores')
    assert response.status_code == 401
    
def test_logout(client, initial_setup):
    """Testa o logout e a invalidação do token."""
    admin_headers = {'Authorization': f'Bearer {initial_setup["admin"]["token"]}'}
    
    # Faz o logout
    response = client.post('/logout', headers=admin_headers)
    assert response.status_code == 200
    
    # Tenta usar o mesmo token
    response_after = client.get('/vendedores', headers=admin_headers)
    assert response_after.status_code == 422 # Token revogado

def test_create_vendedor_com_dados_faltando(client):
    """Testa a validação de erro para dados incompletos."""
    vendedor_incompleto = {"nome": "Incompleto", "senha": "123"}
    response = client.post('/vendedores', data=json.dumps(vendedor_incompleto), content_type='application/json')
    assert response.status_code == 400