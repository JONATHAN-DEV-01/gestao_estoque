from flask import jsonify, make_response, request
from src.application.controllers.vendedor_controller import VendedorController
from flask_jwt_extended import jwt_required, get_jwt_identity

def init_routes(app):
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)

    @app.route('/login', methods=['POST'])
    def login_vendedor():
        return VendedorController.login_vendedor()

    # --- ROTA DE LOGOUT ADICIONADA ---
    @app.route('/logout', methods=['POST'])
    @jwt_required() # O usuário precisa estar logado (enviar um token válido) para poder deslogar
    def logout():
        return VendedorController.logout()
    # -----------------------------------

    @app.route('/vendedores', methods=['POST'])
    def create_vendedor():
        return VendedorController.create_vendedor()

    @app.route('/vendedores/activate', methods=['POST'])
    def activate_vendedor():
        return VendedorController.activate_vendedor()

    @app.route('/vendedores', methods=['GET'])
    @jwt_required()
    def get_all_vendedores():
        return VendedorController.get_all_vendedores()

    @app.route('/vendedores/<int:vendedor_id>', methods=['GET'])
    @jwt_required()
    def get_vendedor(vendedor_id):
        # Lógica de validação do ID no controller
        return VendedorController.get_vendedor(vendedor_id)

    @app.route('/vendedores/<int:vendedor_id>', methods=['PUT'])
    @jwt_required()
    def update_vendedor(vendedor_id):
        # Lógica de validação do ID no controller
        return VendedorController.update_vendedor(vendedor_id)

    @app.route('/vendedores/<int:vendedor_id>', methods=['DELETE'])
    @jwt_required()
    def delete_vendedor(vendedor_id):
        # Lógica de validação do ID no controller
        return VendedorController.delete_vendedor(vendedor_id)