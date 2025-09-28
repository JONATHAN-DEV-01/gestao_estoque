# src/application/controllers/vendedor_controller.py

from flask import request, jsonify, make_response
from src.application.Service.vendedor_service import VendedorService
from flask_jwt_extended import get_jwt

class VendedorController:

    @staticmethod
    def create_vendedor():
        service = VendedorService()
        try:
            data = request.get_json()
            if not all(k in data for k in ['nome', 'cnpj', 'email', 'celular', 'senha']):
                return make_response(jsonify({"erro": "Campos obrigatórios: nome, cnpj, email, celular, senha"}), 400)

            vendedor = service.create_vendedor(data)
            return make_response(jsonify({
                "mensagem": "Vendedor cadastrado com sucesso",
                "vendedor": vendedor.to_dict()
            }), 201)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def login_vendedor():
        service = VendedorService()
        try:
            data = request.get_json()
            email = data.get("email")
            senha = data.get("senha")

            if not email or not senha:
                return jsonify({"erro": "Email e senha são obrigatórios"}), 400

            response = service.login_vendedor(email, senha)
            return make_response(jsonify(response), 200)
        except ValueError as e: # Captura erros de negócio, como senha errada
            return make_response(jsonify({"erro": str(e)}), 401)
        except Exception as e: # Captura outros erros inesperados
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def logout():
        try:
            jti = get_jwt()["jti"]
            VendedorService.logout(jti)
            return make_response(jsonify({"mensagem": "Logout bem-sucedido"}), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def activate_vendedor():
        service = VendedorService()
        try:
            data = request.get_json()
            vendedor_id = data.get("vendedor_id")
            codigo = data.get("codigo")

            vendedor = service.activate_vendedor(vendedor_id, codigo)
            return make_response(jsonify({
                "mensagem": "Conta ativada com sucesso",
                "vendedor": vendedor.to_dict()
            }), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def get_all_vendedores():
        service = VendedorService()
        try:
            vendedores = service.get_all_vendedores()
            vendedores_list = [v.to_dict() for v in vendedores]
            return make_response(jsonify(vendedores_list), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def get_vendedor(vendedor_id):
        service = VendedorService()
        try:
            vendedor = service.get_vendedor(vendedor_id)
            return make_response(jsonify(vendedor.to_dict()), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def update_vendedor(vendedor_id):
        service = VendedorService()
        try:
            data = request.get_json()
            vendedor_atualizado = service.update_vendedor(vendedor_id, data)
            return make_response(jsonify(vendedor_atualizado.to_dict()), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)
    
    @staticmethod
    def deactivate_vendedor(vendedor_id):
        service = VendedorService()
        try:
            vendedor = service.deactivate_vendedor(vendedor_id)
            return make_response(jsonify({
                "mensagem": "Vendedor desativado com sucesso",
                "vendedor": vendedor.to_dict()
            }), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def delete_vendedor(vendedor_id):
        service = VendedorService()
        try:
            service.delete_vendedor(vendedor_id)
            return make_response(jsonify({"mensagem": "Vendedor excluído com sucesso"}), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)