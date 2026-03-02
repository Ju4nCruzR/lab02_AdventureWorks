from src.utils.logger import get_logger

logger = get_logger(__name__)

class LoaderBase:
    
    def __init__(self, connection):
        self.connection = connection
    
    def load(self, table: str, data: list, columns: list):
        if not data:
            logger.warning(f"No hay datos para cargar en {table}")
            return 0
        try:
            with self.connection.cursor() as cur:
                placeholders = ','.join(['%s'] * len(columns))
                col_names = ','.join(columns)
                query = f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})"
                cur.executemany(query, data)
            self.connection.commit()
            logger.info(f"Cargados {len(data)} registros en {table}")
            return len(data)
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Error cargando {table}: {e}")
            raise