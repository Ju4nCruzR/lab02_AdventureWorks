from src.extract.extractor_base import ExtractorBase
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SQLExtractor(ExtractorBase):
    
    def __init__(self, connection):
        super().__init__(connection)
    
    def extract(self, query: str):
        try:
            with self.connection.cursor() as cur:
                logger.info(f"Ejecutando query: {query[:80]}...")
                cur.execute(query)
                data = cur.fetchall()
                logger.info(f"Extraídos {len(data)} registros")
                return data
        except Exception as e:
            logger.error(f"Error en extracción: {e}")
            raise
    
    def extract_table(self, schema: str, table: str):
        query = f"SELECT * FROM {schema}.{table}"
        return self.extract(query)
    
    def extract_with_params(self, query: str, params: tuple):
        try:
            with self.connection.cursor() as cur:
                cur.execute(query, params)
                return cur.fetchall()
        except Exception as e:
            logger.error(f"Error en extracción con parámetros: {e}")
            raise