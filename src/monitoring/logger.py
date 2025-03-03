import logging

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log(message: str):
    """
    Registra uma mensagem no log.
    
    Args:
        message (str): Mensagem a ser registrada.
    """
    logging.info(message)