import pymssql

conn = pymssql.connect(
    server='localhost',
    port=1433,
    user='SA',
    password='Admin1234!',
    database='AdventureWorks'
)
cursor = conn.cursor()

cursor.execute("""
    SELECT TABLE_SCHEMA, TABLE_NAME 
    FROM INFORMATION_SCHEMA.TABLES 
    WHERE TABLE_TYPE='BASE TABLE'
    ORDER BY TABLE_SCHEMA, TABLE_NAME
""")
tables = cursor.fetchall()

output = []
output.append("-- AdventureWorks OLTP Data for PostgreSQL")
output.append("-- Generated from SQL Server 2025\n")

for schema, table in tables:
    pg_schema = schema.lower()
    pg_table = table.lower()
    
    print(f"Exportando {schema}.{table}...")
    
    # Obtener columnas
    cursor.execute(f"""
        SELECT COLUMN_NAME, DATA_TYPE
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_SCHEMA = '{schema}' AND TABLE_NAME = '{table}'
        ORDER BY ORDINAL_POSITION
    """)
    columns = cursor.fetchall()
    col_names = [c[0] for c in columns]
    col_types = [c[1] for c in columns]
    
    # Obtener datos
    cursor.execute(f"SELECT * FROM [{schema}].[{table}]")
    rows = cursor.fetchall()
    
    if not rows:
        continue
    
    col_list = ", ".join([c.lower() for c in col_names])
    output.append(f"-- {schema}.{table}")
    
    for row in rows:
        values = []
        for val, dtype in zip(row, col_types):
            if val is None:
                values.append("NULL")
            elif dtype.lower() in ('int', 'bigint', 'smallint', 'tinyint', 'float', 'real', 'decimal', 'numeric', 'money', 'smallmoney'):
                values.append(str(val))
            elif dtype.lower() == 'bit':
                values.append('TRUE' if val else 'FALSE')
            elif dtype.lower() in ('varbinary', 'binary', 'image', 'timestamp'):
                values.append("NULL")
            else:
                escaped = str(val).replace("'", "''")
                values.append(f"'{escaped}'")
        
        val_str = ", ".join(values)
        output.append(f"INSERT INTO {pg_schema}.{pg_table} ({col_list}) VALUES ({val_str});")
    
    output.append("")

with open('db/oltp/oltp_datos.sql', 'w', encoding='utf-8') as f:
    f.write("\n".join(output))

print("\nDatos exportados exitosamente a db/oltp/oltp_datos.sql")
cursor.close()
conn.close()