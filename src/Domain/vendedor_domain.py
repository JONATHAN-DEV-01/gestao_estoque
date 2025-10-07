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
        self.id = None  
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj,
            "email": self.email,
            "celular": self.celular,
            "status": self.status
        }