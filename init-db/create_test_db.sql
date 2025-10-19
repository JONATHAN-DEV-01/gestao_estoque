-- O banco principal 'gestao_estoque_db' já é criado pelo Docker Compose.
-- Este script agora só precisa criar o banco de teste e dar as permissões.

-- Cria o banco de dados de teste (sem o "IF NOT EXISTS")
CREATE DATABASE gestao_estoque_test_db;

-- Concede todas as permissões ao nosso usuário no banco de dados de teste
GRANT ALL PRIVILEGES ON DATABASE gestao_estoque_test_db TO gestao_estoque_user;