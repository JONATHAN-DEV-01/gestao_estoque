from flask import jsonify, make_response
from src.application.controllers.vendedor_controller import VendedorController

def init_routes(app):
    @app.route('/api', methods=['GET'])
    def health():
        return make_response(jsonify({
            "mensagem": "API - OK; Docker - Up",
        }), 200)

    @app.route('/vendedores', methods=['POST'])
    def create_vendedor():
        return VendedorController.create_vendedor()

    @app.route('/vendedores/activate', methods=['POST'])
    def activate_vendedor():
        return VendedorController.activate_vendedor()

    @app.route('/vendedores', methods=['GET'])
    def get_all_vendedores():
        return VendedorController.get_all_vendedores()

    @app.route('/vendedores/<string:vendedor_id>', methods=['GET'])
    def get_vendedor(vendedor_id):
        return VendedorController.get_vendedor(vendedor_id)

    @app.route('/vendedores/<string:vendedor_id>', methods=['PUT'])
    def update_vendedor(vendedor_id):
        return VendedorController.update_vendedor(vendedor_id)

    @app.route('/vendedores/<string:vendedor_id>', methods=['DELETE'])
    def delete_vendedor(vendedor_id):
        return VendedorController.delete_vendedor(vendedor_id)