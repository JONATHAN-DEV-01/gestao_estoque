from flask import request, jsonify, make_response
from src.application.Service.venda_service import VendaService
from flask_jwt_extended import get_jwt_identity

class VendaController:
    @staticmethod
    def registrar_venda():
        service = VendaService()
        vendedor_id = int(get_jwt_identity())
        data = request.get_json()

        if 'produtos' not in data or not isinstance(data['produtos'], list):
            return make_response(jsonify({"erro": "O corpo da requisição deve conter uma lista de 'produtos'."}), 400)

        try:
            vendas = service.registrar_venda_carrinho(data, vendedor_id)
            return make_response(jsonify({
                "mensagem": "Venda registrada com sucesso!",
                "transacao_id": vendas[0].transacao_id if vendas else None,
                "itens_vendidos": [v.to_dict() for v in vendas]
            }), 201)
        except (ValueError, PermissionError) as e:
            return make_response(jsonify({"erro": str(e)}), 400)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)
    
    @staticmethod
    def get_dashboard_summary():
        service = VendaService()
        vendedor_id = int(get_jwt_identity()) # Pega o vendedor logado
        
        try:
            summary_data = service.get_dashboard_summary(vendedor_id)
            return make_response(jsonify(summary_data), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)
    @staticmethod
    def listar_vendas():
        service = VendaService()
        vendedor_id = int(get_jwt_identity())
        try:
            # O repositório já retorna uma lista de dicionários formatada
            vendas = service.listar_minhas_vendas(vendedor_id)
            return make_response(jsonify(vendas), 200)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)

    @staticmethod
    def cancelar_venda(venda_id):
        service = VendaService()
        vendedor_id = int(get_jwt_identity())
        try:
            service.cancelar_venda(venda_id, vendedor_id)
            return make_response(jsonify({"mensagem": "Venda cancelada e estoque estornado com sucesso!"}), 200)
        except (ValueError, PermissionError) as e:
            return make_response(jsonify({"erro": str(e)}), 400) # Erro de cliente (não achou ou sem permissão)
        except Exception as e:
            return make_response(jsonify({"erro": str(e)}), 500)