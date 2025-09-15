# src/application/controllers/vendedor_controller.py

from flask import request, jsonify, make_response
from src.application.Service.vendedor_service import VendedorService

class VendedorController:
    @staticmethod
    def create_vendedor():
        try:
            data = request.get_json()
            nome = data.get('nome')
            cnpj = data.get('cnpj')
            email = data.get('email')
            celular = data.get('celular')
            senha = data.get('senha')

            if not nome or not cnpj or not email or not celular or not senha:
                return make_response(jsonify({
                    "erro": "Campos obrigatórios: nome, cnpj, email, celular, senha"
                }), 400)
                
                a

            vendedor = VendedorService.create_vendedor(nome, cnpj, email, celular, senha)

            return make_response(jsonify({
                "mensagem": "Vendedor cadastrado com sucesso",
                "vendedor": vendedor.to_dict()
            }), 201)

        except Exception as e:
            return make_response(jsonify({
                "erro": str(e)
            }), 500)

    @staticmethod
    def login_vendedor():
        try:
            data = request.get_json()
            email = data.get("email")
            senha = data.get("senha")

            if not email or not senha:
                return jsonify({"erro": "Email e senha são obrigatórios"}), 400

            response = VendedorService.login_vendedor(email, senha)
            return make_response(jsonify(response), 200)
        
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 401)

    @staticmethod
    def activate_vendedor():
        try:
            data = request.get_json()
            vendedor_id = data.get("vendedor_id")
            codigo = data.get("codigo")

            if not vendedor_id or not codigo:
                return make_response(jsonify({
                    "erro": "Campos obrigatórios: vendedor_id, codigo"
                }), 400)

            vendedor = VendedorService.activate_vendedor(vendedor_id, codigo)

            return make_response(jsonify({
                "mensagem": "Conta ativada com sucesso",
                "vendedor": vendedor.to_dict()
            }), 200)

        except Exception as e:
            return make_response(jsonify({
                "erro": str(e)
            }), 500)

    @staticmethod
    def get_all_vendedores():
        try:
            vendedores = VendedorService.get_all_vendedores()
            vendedores_list = [v.to_dict() for v in vendedores]
            return make_response(jsonify(vendedores_list), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def get_vendedor(vendedor_id):
        try:
            vendedor = VendedorService.get_vendedor(vendedor_id)
            return make_response(jsonify(vendedor.to_dict()), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def update_vendedor(vendedor_id):
        try:
            data = request.get_json()
            vendedor_atualizado = VendedorService.update_vendedor(vendedor_id, data)
            return make_response(jsonify(vendedor_atualizado.to_dict()), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def delete_vendedor(vendedor_id):
        try:
            VendedorService.delete_vendedor(vendedor_id)
            return make_response(jsonify({"mensagem": "Vendedor excluído com sucesso"}), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)