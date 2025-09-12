# src/Domain/vendedor_domain.py

class Vendedor:
    def __init__(self, nome, cnpj, email, celular, senha, status="Inativo", codigo_ativacao=None):
        self.nome = nome
        self.cnpj = cnpj
        self.email = email
        self.celular = celular
        self.senha = senha
        self.status = status
        self.codigo_ativacao = codigo_ativacao
        self.id = None  # O ID será atribuído pelo repositório/banco de dados
    def to_dict(self):
        """Converte o objeto Vendedor em um dicionário para serialização JSON."""
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj,
            "email": self.email,
            "celular": self.celular,
            "status": self.status
        }