# Usa uma imagem base do Python 3.9
FROM python:3.9-slim

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências para o contêiner
COPY requirements.txt .

# Instala as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código do projeto para o contêiner
COPY . .

# Expõe a porta 8000 (a mesma que a API usa)
EXPOSE 8000

# Comando para rodar a API quando o contêiner for iniciado
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]