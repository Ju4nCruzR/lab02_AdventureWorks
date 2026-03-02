import os

OLTP_CONFIG = {
    "host": os.getenv("OLTP_HOST", "localhost"),
    "port": int(os.getenv("OLTP_PORT", 5432)),
    "database": os.getenv("OLTP_DB", "adventureworks_oltp"),
    "user": os.getenv("OLTP_USER", "adventure"),
    "password": os.getenv("OLTP_PASSWORD", "adventure123"),
}

OLAP_CONFIG = {
    "host": os.getenv("OLAP_HOST", "localhost"),
    "port": int(os.getenv("OLAP_PORT", 5432)),
    "database": os.getenv("OLAP_DB", "adventureworks_oltp"),
    "user": os.getenv("OLAP_USER", "adventure"),
    "password": os.getenv("OLAP_PASSWORD", "adventure123"),
}