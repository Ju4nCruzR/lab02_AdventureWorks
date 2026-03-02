class ETLException(Exception):
    """Excepción base para errores del ETL"""
    pass

class ExtractException(ETLException):
    """Error durante la extracción de datos"""
    pass

class TransformException(ETLException):
    """Error durante la transformación de datos"""
    pass

class LoadException(ETLException):
    """Error durante la carga de datos"""
    pass

class ConnectionException(ETLException):
    """Error de conexión a base de datos"""
    pass