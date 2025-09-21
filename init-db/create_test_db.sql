-- Cria o banco de dados de desenvolvimento se ele não existir
CREATE DATABASE IF NOT EXISTS gestao_estoque_db;

-- Cria o banco de dados de teste se ele não existir
CREATE DATABASE IF NOT EXISTS gestao_estoque_test_db;

-- Concede todas as permissões ao usuário no banco de dados de teste
GRANT ALL PRIVILEGES ON `gestao_estoque_test_db`.* TO 'gestao_estoque_user'@'%';