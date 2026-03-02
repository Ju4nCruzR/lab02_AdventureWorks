# Taller 02 - ETL AdventureWorks

ETL desde una base de datos OLTP (AdventureWorks en SQL Server 2025) hacia un modelo ROLAP en PostgreSQL 18, con una aplicación web para visualizar los resultados de las preguntas de negocio.

## Requisitos
- Python 3.13+
- Docker o Podman
- podman-compose o docker compose

## Estructura del Proyecto
```
lab02_AdventureWorks/
├── app/            # Aplicación web Flask
├── config/         # Configuración y settings
├── db/
│   ├── bak/        # Backup de SQL Server
│   ├── oltp/       # Scripts OLTP (schema + datos)
│   └── olap/       # Script OLAP (star schema)
├── src/
│   ├── extract/    # Módulos de extracción
│   ├── transform/  # Módulos de transformación
│   ├── load/       # Módulos de carga
│   ├── models/     # Modelos SQLAlchemy ORM
│   ├── pipelines/  # Pipelines ETL
│   └── utils/      # Utilidades
├── tests/          # Pruebas unitarias
└── podman/         # compose.yaml
```

## Instalación

1. Clonar el repositorio
2. Instalar dependencias:
```bash
pip install -r requirements.txt
```
3. Levantar los contenedores:
```bash
cd podman
podman compose up -d
```
4. Restaurar el backup en SQL Server y cargar el OLTP en PostgreSQL
5. Ejecutar el ETL:
```bash
python -m src.main
```
6. Iniciar la aplicación web:
```bash
python app/app.py
```
7. Abrir http://localhost:5000

## Preguntas de Negocio

- **P1** — Clientes recurrentes vs únicos: porción de ingresos por tipo de cliente
- **P2** — Varianza de margen por producto: productos para compra navideña
- **P3** — Análisis de canasta: top 10 parejas de productos comprados juntos
- **P4** — Análisis de cohortes: top 3 cohortes por margen