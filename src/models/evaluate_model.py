from sklearn.metrics import precision_score, recall_score, f1_score
from src.utils.helpers import load_model, load_data
from src.monitoring.logger import log

def evaluate_model(model_path, test_data_path):
    """
    Avalia o modelo usando métricas de precisão, recall e F1-score.
    
    Args:
        model_path (str): Caminho para o modelo salvo.
        test_data_path (str): Caminho para os dados de teste.
    """
    log("Carregando modelo e dados de teste...")
    model = load_model(model_path)
    test_data = load_data(test_data_path)

    log("Preparando dados...")
    X_test = test_data[['timeOnPageHistory', 'numberOfClicksHistory', 'scrollPercentageHistory', 'recency_weight']]
    y_test = test_data['history']

    log("Fazendo previsões...")
    y_pred = model.predict(X_test)

    log("Calculando métricas...")
    precision = precision_score(y_test, y_pred, average='weighted')
    recall = recall_score(y_test, y_pred, average='weighted')
    f1 = f1_score(y_test, y_pred, average='weighted')

    log(f"Precisão: {precision:.2f}, Recall: {recall:.2f}, F1-score: {f1:.2f}")

if __name__ == "__main__":
    evaluate_model(
        model_path="data/models/recommendation_model.pkl",
        test_data_path="data/processed/test_data.csv"
    )