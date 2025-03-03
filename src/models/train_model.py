import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from src.utils.helpers import save_model, load_data
from src.monitoring.logger import log
import mlflow
import mlflow.sklearn

def train_model(data_path, model_save_path):
    """
    Treina o modelo de recomendação e registra no MLflow.
    
    Args:
        data_path (str): Caminho para os dados processados.
        model_save_path (str): Caminho para salvar o modelo.
    """
    log("Carregando dados processados...")
    data = load_data(data_path)

    log("Dividindo dados em features e target...")
    X = data[['timeOnPageHistory', 'numberOfClicksHistory', 'scrollPercentageHistory', 'recency_weight']]
    y = data['history']

    log("Dividindo em treino e teste...")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    log("Iniciando experimento no MLflow...")
    mlflow.set_experiment("G1_Recommendation")
    with mlflow.start_run():
        log("Treinando modelo...")
        param_grid = {'n_estimators': [50, 100, 200], 'max_depth': [None, 10, 20]}
        grid_search = GridSearchCV(RandomForestClassifier(), param_grid, cv=5)
        grid_search.fit(X_train, y_train)

        log("Avaliando modelo...")
        y_pred = grid_search.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        log(f"Acurácia do modelo: {accuracy:.2f}")

        log("Salvando modelo...")
        save_model(grid_search.best_estimator_, model_save_path)

        log("Registrando métricas no MLflow...")
        mlflow.log_metric("accuracy", accuracy)
        mlflow.sklearn.log_model(grid_search.best_estimator_, "model")

if __name__ == "__main__":
    train_model(
        data_path="data/processed/processed_data.csv",
        model_save_path="data/models/recommendation_model.pkl"
    )