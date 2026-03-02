import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipelines.sales_pipeline import SalesPipeline
from src.pipelines.customer_pipeline import CustomerPipeline
from src.utils.logger import get_logger

logger = get_logger(__name__)

def main():
    logger.info("Iniciando ETL AdventureWorks -> OLAP")
    
    try:
        logger.info("Ejecutando pipeline de clientes...")
        customer_pipeline = CustomerPipeline()
        customer_pipeline.run()
        
        logger.info("Ejecutando pipeline de ventas...")
        sales_pipeline = SalesPipeline()
        sales_pipeline.run()
        
        logger.info("ETL completado exitosamente")
    except Exception as e:
        logger.error(f"Error en ETL: {e}")
        raise

if __name__ == "__main__":
    main()