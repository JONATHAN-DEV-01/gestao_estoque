# Usa uma imagem base leve e segura
FROM python:3.11-slim-bookworm

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# --- ALTERAÇÃO 1: SEGURANÇA ---
# Cria um usuário não-root chamado 'appuser' para rodar a aplicação
RUN useradd --create-home appuser
# Define o proprietário do diretório de trabalho para o novo usuário
RUN chown -R appuser:appuser /app

# Copia o arquivo de dependências
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código da aplicação
COPY run.py .
COPY src ./src

# --- MAIS DA ALTERAÇÃO 1: SEGURANÇA ---
# Muda para o usuário não-root antes de iniciar a aplicação
USER appuser

# Expõe a porta que a aplicação vai usar
EXPOSE 5000

# --- ALTERAÇÃO 2: PERFORMANCE ---
# Comando para iniciar a aplicação com 3 workers para melhor performance
CMD ["gunicorn", "--workers=3", "--bind=0.0.0.0:5000", "run:app"]