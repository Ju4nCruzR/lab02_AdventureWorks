import pymssql
import re

conn = pymssql.connect(
    server='localhost',
    port=1433,
    user='SA',
    password='Admin1234!',
    database='AdventureWorks'
)
cursor = conn.cursor()

# Obtener todas las tablas
cursor.execute("""
    SELECT TABLE_SCHEMA, TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE='BASE TABLE'
    ORDER BY TABLE_SCHEMA, TABLE_NAME
""")
tables = cursor.fetchall()

# Mapeo de tipos SQL Server a PostgreSQL
type_map = {
    'int': 'INTEGER',
    'bigint': 'BIGINT',
    'smallint': 'SMALLINT',
    'tinyint': 'SMALLINT',
    'bit': 'BOOLEAN',
    'decimal': 'DECIMAL',
    'numeric': 'NUMERIC',
    'money': 'NUMERIC(19,4)',
    'smallmoney': 'NUMERIC(10,4)',
    'float': 'DOUBLE PRECISION',
    'real': 'REAL',
    'datetime': 'TIMESTAMP',
    'datetime2': 'TIMESTAMP',
    'smalldatetime': 'TIMESTAMP',
    'date': 'DATE',
    'time': 'TIME',
    'char': 'CHAR',
    'varchar': 'VARCHAR',
    'nchar': 'CHAR',
    'nvarchar': 'VARCHAR',
    'text': 'TEXT',
    'ntext': 'TEXT',
    'uniqueidentifier': 'UUID',
    'varbinary': 'BYTEA',
    'binary': 'BYTEA',
    'image': 'BYTEA',
    'xml': 'XML',
    'hierarchyid': 'VARCHAR(100)',
    'geography': 'TEXT',
    'geometry': 'TEXT',
}

output = []
output.append("-- AdventureWorks OLTP Schema for PostgreSQL")
output.append("-- Generated from SQL Server 2025\n")

# Crear schemas
schemas = set([t[0] for t in tables])
for schema in schemas:
    output.append(f"CREATE SCHEMA IF NOT EXISTS {schema.lower()};")
output.append("")

for schema, table in tables:
    pg_schema = schema.lower()
    pg_table = table.lower()
    
    cursor.execute(f"""
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            CHARACTER_MAXIMUM_LENGTH,
            NUMERIC_PRECISION,
            NUMERIC_SCALE,
            IS_NULLABLE,
            COLUMN_DEFAULT
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table}'
        ORDER BY ORDINAL_POSITION
    """)
    columns = cursor.fetchall()
    
    col_defs = []
    for col in columns:
        col_name, data_type, char_len, num_prec, num_scale, nullable, default = col
        
        pg_type = type_map.get(data_type.lower(), 'TEXT')
        
        if data_type.lower() in ('varchar', 'nvarchar', 'char', 'nchar'):
            if char_len and char_len > 0:
                pg_type = f"{pg_type}({char_len})"
            else:
                pg_type = 'TEXT'
        elif data_type.lower() in ('decimal', 'numeric'):
            if num_prec:
                pg_type = f"NUMERIC({num_prec},{num_scale or 0})"
        
        null_str = "NOT NULL" if nullable == 'NO' else "NULL"
        safe_col = f'"{col_name.lower()}"'
        col_defs.append(f"    {safe_col} {pg_type} {null_str}")
    
    output.append(f"CREATE TABLE IF NOT EXISTS {pg_schema}.{pg_table} (")
    output.append(",\n".join(col_defs))
    output.append(");\n")

with open('db/oltp/oltp_schema.sql', 'w', encoding='utf-8') as f:
    f.write("\n".join(output))

print("Schema exportado exitosamente a db/oltp/oltp_schema.sql")
cursor.close()
conn.close()