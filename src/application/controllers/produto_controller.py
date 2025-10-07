from flask import request, jsonify, make_response
from src.application.Service.produto_service import ProdutoService
from flask_jwt_extended import get_jwt_identity

class ProdutoController:
    @staticmethod
    def create_produto():
        service = ProdutoService()
        vendedor_id = get_jwt_identity() # Pega o ID do vendedor logado
        data = request.get_json()
        
        if not all(k in data for k in ['nome', 'preco', 'quantidade']):
            return make_response(jsonify({"erro": "Campos obrigatórios: nome, preco, quantidade"}), 400)
        
        try:
            produto = service.create_produto(data, vendedor_id)
            return make_response(jsonify(produto.to_dict()), 201)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def get_all_produtos():
        service = ProdutoService()
        vendedor_id = get_jwt_identity()
        try:
            produtos = service.get_all_produtos_by_vendedor(vendedor_id)
            return make_response(jsonify([p.to_dict() for p in produtos]), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)
    
    @staticmethod
    def get_produto_by_id(produto_id):
        service = ProdutoService()
        vendedor_id = get_jwt_identity()
        try:
            produto = service.get_produto_by_id(produto_id, vendedor_id)
            return make_response(jsonify(produto.to_dict()), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def update_produto(produto_id):
        service = ProdutoService()
        vendedor_id = get_jwt_identity()
        data = request.get_json()
        try:
            produto = service.update_produto(produto_id, data, vendedor_id)
            return make_response(jsonify(produto.to_dict()), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def inativar_produto(produto_id):
        service = ProdutoService()
        vendedor_id = get_jwt_identity()
        try:
            produto = service.inativar_produto(produto_id, vendedor_id)
            return make_response(jsonify(produto.to_dict()), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)
        

    @staticmethod
    def ativar_produto(produto_id):
        service = ProdutoService()
        vendedor_id = get_jwt_identity()
        try:
            produto = service.ativar_produto(produto_id, vendedor_id)
            return make_response(jsonify(produto.to_dict()), 200)
        except ValueError as e:
            return make_response(jsonify({"erro": str(e)}), 404)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)