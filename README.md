# Sistema de Recomendação de Notícias do G1

Este projeto tem como objetivo desenvolver um sistema de recomendação para notícias do G1, utilizando técnicas de Machine Learning Engineering.

## Estrutura do Projeto

- `data/`: Armazena dados brutos e processados.
- `notebooks/`: Contém notebooks de análise exploratória e experimentação.
- `src/`: Código fonte do projeto.
- `tests/`: Testes unitários e de integração.
- `Dockerfile`: Para empacotar a aplicação.

## Como Executar

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Pré-processe os dados:
   ```bash
   python src/models/train_model.py
   ```

3. Treine o modelo:
   ```bash
   python src/models/train_model.py
   ```

4. Execute a API:
   ```bash
   python src/api/app.py
   ```

5. Teste a API:
   ```bash
    curl -X POST -H "Content-Type: application/json" -d '{"timeOnPageHistory": 0.5, "numberOfClicksHistory": 0.3, "scrollPercentageHistory": 0.8, "recency_weight": 0.2}' http://localhost:5000/predict
   ```

## Deploy com Docker

1. Construa a imagem Docker:
   ```bash
   docker build -t g1_recommendation .
   ```

2. Execute o container:
   ```bash
   docker run -p 5000:5000 g1_recommendation
   ```