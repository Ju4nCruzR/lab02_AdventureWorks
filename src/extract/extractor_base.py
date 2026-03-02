from abc import ABC, abstractmethod
from src.utils.logger import get_logger

logger = get_logger(__name__)

class ExtractorBase(ABC):
    
    def __init__(self, connection):
        self.connection = connection
    
    @abstractmethod
    def extract(self, query: str):
        pass
    
    def validate(self, data) -> bool:
        if data is None:
            logger.warning("Los datos extraídos son None")
            return False
        if len(data) == 0:
            logger.warning("Los datos extraídos están vacíos")
            return False
        return True