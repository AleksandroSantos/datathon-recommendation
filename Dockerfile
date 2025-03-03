# Usar uma imagem base do Python
FROM python:3.9-slim

# Definir diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código fonte
COPY . .

# Expor a porta da API
EXPOSE 5000

# Comando para rodar a API
CMD ["uvicorn", "src.api.app:app", "--host", "0.0.0.0", "--port", "5000"]