# Sistema de Recomendação de Notícias do G1

Este projeto é um sistema de recomendação de notícias personalizadas para usuários do G1. Ele utiliza técnicas de **Processamento de Linguagem Natural (NLP)**, como TF-IDF e similaridade de cosseno, combinadas com aprendizado de máquina para prever quais notícias um usuário pode querer ler com base em seu histórico de leitura.

---

## Técnicas de NLP Utilizadas

1. **TF-IDF (Term Frequency-Inverse Document Frequency)**:
   - Transforma o conteúdo das notícias (título, corpo e legenda) em vetores numéricos, destacando as palavras mais relevantes para cada notícia.

2. **Similaridade de Cosseno**:
   - Compara a semelhança entre os vetores TF-IDF das notícias para recomendar conteúdos semelhantes ao que o usuário já leu.

3. **Decaimento Temporal**:
   - Aplica um fator de decaimento para reduzir a relevância de notícias antigas, garantindo que as recomendações sejam sempre oportunas.

---

## Objetivos do Projeto

Este projeto foi desenvolvido para atender aos seguintes objetivos principais:

1. **Cold Start**:
   - Recomenda notícias populares e recentes para novos usuários ou itens sem histórico, garantindo que todos tenham uma experiência personalizada desde o início.

2. **Recência**:
   - Prioriza notícias recentes e aplica um decaimento temporal para reduzir a relevância de notícias antigas, garantindo que as recomendações sejam sempre oportunas.

3. **Treinamento do Modelo**:
   - Utiliza TF-IDF para extrair features do conteúdo das notícias e calcula scores de popularidade com base no histórico de interações dos usuários.

4. **Salvamento do Modelo**:
   - Salva o modelo treinado em um arquivo `.pkl`, permitindo recarregá-lo sem a necessidade de retreinamento.

5. **Criação de uma API**:
   - Disponibiliza o modelo por meio de uma API RESTful usando FastAPI, com endpoints para recomendações personalizadas, notícias populares e recarregamento do modelo.

6. **Empacotamento com Docker**:
   - Facilita a execução do projeto em diferentes ambientes por meio de um contêiner Docker.

7. **Testes e Validação**:
   - Inclui testes unitários e de integração para garantir a qualidade do código e do modelo.

8. **Deploy**:
   - Oferece instruções detalhadas para implantação local ou na nuvem, tornando o sistema pronto para uso em produção.

---


## Requisitos

Antes de começar, certifique-se de que você tem os seguintes requisitos instalados:

- **Python 3.9** ou superior.
- **Docker** (opcional, para empacotamento e execução em contêineres).
- **Git** (para clonar o repositório).

---

## Instalação

Siga os passos abaixo para configurar o projeto em sua máquina:

1. Clone o repositório:
   ```bash
   git clone https://github.com/AleksandroSantos/datathon-recommendation.git
   cd datathon-recommendation
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure o PYTHONPATH (se necessário):
Para garantir que o Python reconheça o diretório src como um pacote, adicione o diretório raiz do projeto ao PYTHONPATH:

   - Linux/Mac:
   ```bash
   export PYTHONPATH="${PYTHONPATH}:$(pwd)"
   ```

   - Windows:
   ```bash
   set PYTHONPATH=%PYTHONPATH%;%cd%
   ```


## Instalação

### 1. Executando Localmente

Para rodar a API localmente, siga os passos abaixo:

   1. Baixe os dados necessários:
      ```bash
      python src/data/data_downloader.py
      ```

   2. Carregue e prepare os dados:
      ```bash
      python src/data/data_loader.py
      ```

   3. Inicie a API:
      ```bash
      uvicorn src.api.main:app --reload
      ```

   4. Acesse a API no navegador ou via ferramentas como Postman:
   - URL base: http://localhost:8000
   - Documentação Swagger: http://localhost:8000/docs

### 2. Executando com Docker

Se você preferir rodar o projeto em um contêiner Docker, siga os passos abaixo:

   1. Construa a imagem Docker:
      ```bash
      docker build -t news-recommender-api .
      ```

   2. Execute o contêiner:
      ```bash
      docker run -p 8000:8000 news-recommender-api
      ```

## Estrutura do Projeto

A estrutura do projeto é organizada da seguinte forma:
```
   datathon-recommendation/
   ├── src/
   │   ├── api/
   │   │   ├── endpoints.py
   │   │   └── main.py
   │   ├── data/
   │   │   ├── data_downloader.py
   │   │   └── data_loader.py
   │   ├── models/
   │   │   └── recommender.py
   │   └── utils/
   │       ├── config.py
   │       └── logger.py
   ├── tests/
   │   ├── test_api.py
   │   ├── test_data_downloader.py
   │   ├── test_data_loader.py
   │   ├── test_endpoints.py
   │   └── testtest_recommender_api.py
   ├── data/
   ├── Dockerfile
   ├── docker-compose.yml
   ├── requirements.txt
   └── README.md
```

## Endpoints da API

A API possui os seguintes endpoints:

- `GET /`: Retorna informações básicas sobre a API.
- `GET /health`: Verifica a saúde da API.
- `GET /recommend/{user_id}`: Retorna recomendações personalizadas para um usuário.
  - Parâmetros:
    -  **user_id** (string): ID do usuário.
    -  **n** (int, opcional): Número de recomendações (padrão: 5).
- `GET /popular`: Retorna as notícias mais populares.
  - Parâmetros:
    - **n** (int, opcional): Número de notícias (padrão: 5).
- `GET /recent`: Para listar notícias recentes.
- `POST /train-model`: Para treinar o modelo.
- `GET /reload-model`: Recarrega o modelo de recomendação.
- `POST /add-news`: Para adicionar novas notícias.

## Empacotamento com Docker
O projeto pode ser empacotado e executado usando Docker. Siga os passos abaixo:

1. Construa a imagem Docker:
   ```bash
   docker build -t news-recommender-api .
   ```

2. Execute o contêiner:
   ```bash
   docker run -p 8000:8000 news-recommender-api
   ```

3. Acesse a API em `http://localhost:8000`.

## Testes
Para garantir a qualidade do código, siga os passos abaixo para executar os testes:

1. Instale as dependências de desenvolvimento:
   ```bash
   pip install -r requirements-dev.txt
   ```

2. Execute os testes:
   ```bash
   pytest tests/
   ```
