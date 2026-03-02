from src.utils.logger import get_logger

logger = get_logger(__name__)

class TransformerBase:

    def transform(self, data: list) -> list:
        raise NotImplementedError

    def clean_string(self, value) -> str:
        if value is None:
            return None
        return str(value).strip()

    def clean_numeric(self, value, default=0.0) -> float:
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            return default

    def clean_date(self, value):
        if value is None:
            return None
        return value