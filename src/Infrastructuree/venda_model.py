from src.config.database import db
from datetime import datetime

class VendaModel(db.Model):
    __tablename__ = 'vendas'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    transacao_id = db.Column(db.String(36), nullable=False, index=True) # <-- ADICIONADO
    quantidade = db.Column(db.Integer, nullable=False)
    preco_unitario_venda = db.Column(db.Float, nullable=False)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)

    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    vendedor_id = db.Column(db.Integer, db.ForeignKey('vendedores.id'), nullable=False)