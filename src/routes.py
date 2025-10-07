from flask import jsonify, make_response, request
from src.application.controllers.vendedor_controller import VendedorController
from src.application.controllers.produto_controller import ProdutoController
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
    
    @app.route('/vendedores/<int:vendedor_id>/deactivate', methods=['POST'])
    @jwt_required()
    def deactivate_vendedor(vendedor_id):
        return VendedorController.deactivate_vendedor(vendedor_id)
    



    # ROTAS DOS PRODUTOS




    @app.route('/produtos', methods=['POST'])
    @jwt_required()
    def create_produto():
        return ProdutoController.create_produto()

    @app.route('/produtos', methods=['GET'])
    @jwt_required()
    def get_all_produtos():
        return ProdutoController.get_all_produtos()

    @app.route('/produtos/<int:produto_id>', methods=['GET'])
    @jwt_required()
    def get_produto_by_id(produto_id):
        return ProdutoController.get_produto_by_id(produto_id)

    @app.route('/produtos/<int:produto_id>', methods=['PUT'])
    @jwt_required()
    def update_produto(produto_id):
        return ProdutoController.update_produto(produto_id)

    @app.route('/produtos/<int:produto_id>/inativar', methods=['POST'])
    @jwt_required()
    def inativar_produto(produto_id):
        return ProdutoController.inativar_produto(produto_id)
    
    @app.route('/produtos/<int:produto_id>/ativar', methods=['POST'])
    @jwt_required()
    def ativar_produto(produto_id):
        return ProdutoController.ativar_produto(produto_id)