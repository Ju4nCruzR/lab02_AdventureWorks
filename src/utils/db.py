import psycopg2
from config.settings import OLTP_CONFIG, OLAP_CONFIG

def get_oltp_connection():
    return psycopg2.connect(**OLTP_CONFIG)

def get_olap_connection():
    return psycopg2.connect(**OLAP_CONFIG)