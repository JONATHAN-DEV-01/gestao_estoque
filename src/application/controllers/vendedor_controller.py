# src/Presentation/Controller/vendedor_controller.py

from flask import request, jsonify, make_response
from src.application.Service.vendedor_service import VendedorService

class VendedorController:

    @staticmethod
    def create_vendedor():
        try:
            data = request.get_json()
            nome = data.get('nome')  # Use 'nome' para manter a consistência
            cnpj = data.get('cnpj')
            email = data.get('email')
            celular = data.get('celular')
            senha = data.get('senha')

            # Validação simples
            if not nome or not cnpj or not email or not celular or not senha:
                return make_response(jsonify({
                    "erro": "Campos obrigatórios: nome, cnpj, email, celular, senha"
                }), 400)

            # Chama o Service -> cria vendedor com status "Inativo"
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
    def activate_vendedor():
        try:
            data = request.get_json()
            vendedor_id = data.get("vendedor_id")
            codigo = data.get("codigo")  # Use 'codigo' para refletir o domain

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

    # Métodos restantes para a consistência
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