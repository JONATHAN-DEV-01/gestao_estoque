# src/Infrastructuree/token_blocklist_model.py

from src.config.database import db
from datetime import datetime

class TokenBlocklistModel(db.Model):
    """
    Modelo para armazenar os JTIs dos tokens que sofreram logout.
    """
    __tablename__ = 'token_blocklist'
    
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"<TokenBlocklist {self.jti}>"