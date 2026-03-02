import logging
import os

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        
        # File handler
        os.makedirs('logs', exist_ok=True)
        fh = logging.FileHandler('logs/etl.log', encoding='utf-8')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
    
    return logger