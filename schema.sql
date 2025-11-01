-- Script SQL para PostgreSQL --


CREATE TABLE vendedores (
        id SERIAL NOT NULL, 
        nome VARCHAR(100) NOT NULL, 
        cnpj VARCHAR(18) NOT NULL, 
        email VARCHAR(120) NOT NULL, 
        celular VARCHAR(20) NOT NULL, 
        senha VARCHAR(200) NOT NULL, 
        status VARCHAR(20), 
        codigo_ativacao VARCHAR(4), 
        PRIMARY KEY (id), 
        UNIQUE (cnpj), 
        UNIQUE (email)
)


;


CREATE TABLE produtos (
        id SERIAL NOT NULL,
        nome VARCHAR(100) NOT NULL,]

    
        preco FLOAT NOT NULL,
        quantidade INTEGER NOT NULL,
        status VARCHAR(20),
        imagem VARCHAR(255),
        vendedor_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(vendedor_id) REFERENCES vendedores (id)
)


;


CREATE TABLE vendas (
        id SERIAL NOT NULL,
        transacao_id VARCHAR(36) NOT NULL,
        quantidade INTEGER NOT NULL,
        preco_unitario_venda FLOAT NOT NULL,
        data_venda TIMESTAMP WITHOUT TIME ZONE,
        produto_id INTEGER NOT NULL,
        vendedor_id INTEGER NOT NULL,
        PRIMARY KEY (id),
        FOREIGN KEY(produto_id) REFERENCES produtos (id),
        FOREIGN KEY(vendedor_id) REFERENCES vendedores (id)
)


;


CREATE TABLE token_blocklist (
        id SERIAL NOT NULL,
        jti VARCHAR(36) NOT NULL,
        created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (jti)
)


;

-- Fim do Script --