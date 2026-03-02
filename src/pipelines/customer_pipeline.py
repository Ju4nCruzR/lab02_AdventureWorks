from src.utils.db import get_oltp_connection, get_olap_connection
from src.utils.logger import get_logger

logger = get_logger(__name__)

class CustomerPipeline:
    def run(self):
        self.load_dim_date()
        self.load_dim_territory()
        self.load_dim_customer()
        self.load_dim_product()

    def load_dim_date(self):
        logger.info("Cargando dim_date...")
        oltp = get_oltp_connection()
        olap = get_olap_connection()
        try:
            with oltp.cursor() as cur:
                cur.execute("""
                    SELECT DISTINCT orderdate::date FROM sales.salesorderheader
                    UNION
                    SELECT DISTINCT duedate::date FROM sales.salesorderheader WHERE duedate IS NOT NULL
                    UNION
                    SELECT DISTINCT shipdate::date FROM sales.salesorderheader WHERE shipdate IS NOT NULL
                    ORDER BY 1
                """)
                dates = cur.fetchall()

            with olap.cursor() as cur:
                cur.execute("TRUNCATE olap.dim_date CASCADE")
                for (d,) in dates:
                    if d is None:
                        continue
                    date_key = int(d.strftime('%Y%m%d'))
                    cur.execute("""
                        INSERT INTO olap.dim_date (
                            date_key, full_date, day, month, month_name,
                            quarter, year, week_of_year, day_of_week,
                            day_name, is_weekend, year_month
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ON CONFLICT (date_key) DO NOTHING
                    """, (
                        date_key, d,
                        d.day, d.month,
                        d.strftime('%B'),
                        (d.month - 1) // 3 + 1,
                        d.year,
                        int(d.strftime('%W')),
                        d.weekday(),
                        d.strftime('%A'),
                        d.weekday() >= 5,
                        d.strftime('%Y-%m')
                    ))
            olap.commit()
            logger.info(f"dim_date cargada con {len(dates)} fechas")
        finally:
            oltp.close()
            olap.close()

    def load_dim_territory(self):
        logger.info("Cargando dim_territory...")
        oltp = get_oltp_connection()
        olap = get_olap_connection()
        try:
            with oltp.cursor() as cur:
                cur.execute("""
                    SELECT territoryid, name, countryregioncode, "group"
                    FROM sales.salesterritory
                """)
                rows = cur.fetchall()

            with olap.cursor() as cur:
                cur.execute("TRUNCATE olap.dim_territory CASCADE")
                for row in rows:
                    cur.execute("""
                        INSERT INTO olap.dim_territory (
                            territory_key, territory_id, territory_name,
                            country_region, territory_group
                        ) VALUES (%s,%s,%s,%s,%s)
                    """, (row[0], row[0], row[1], row[2], row[3]))
            olap.commit()
            logger.info(f"dim_territory cargada con {len(rows)} territorios")
        finally:
            oltp.close()
            olap.close()

    def load_dim_customer(self):
        logger.info("Cargando dim_customer...")
        oltp = get_oltp_connection()
        olap = get_olap_connection()
        try:
            with oltp.cursor() as cur:
                cur.execute("""
                    SELECT
                        c.customerid,
                        p.firstname,
                        p.lastname,
                        COALESCE(p.firstname || ' ' || p.lastname, s.name) as full_name,
                        ea.emailaddress,
                        CASE WHEN c.personid IS NOT NULL THEN 'Individual' ELSE 'Store' END,
                        s.name,
                        st.name,
                        st.countryregioncode,
                        MIN(soh.orderdate)::date as first_purchase
                    FROM sales.customer c
                    LEFT JOIN person.person p ON c.personid = p.businessentityid
                    LEFT JOIN sales.store s ON c.storeid = s.businessentityid
                    LEFT JOIN sales.salesterritory st ON c.territoryid = st.territoryid
                    LEFT JOIN person.emailaddress ea ON c.personid = ea.businessentityid
                    LEFT JOIN sales.salesorderheader soh ON c.customerid = soh.customerid
                    GROUP BY c.customerid, p.firstname, p.lastname,
                             COALESCE(p.firstname || ' ' || p.lastname, s.name),
                             ea.emailaddress,
                             CASE WHEN c.personid IS NOT NULL THEN 'Individual' ELSE 'Store' END,
                             s.name, st.name, st.countryregioncode
                """)
                rows = cur.fetchall()

            with olap.cursor() as cur:
                cur.execute("TRUNCATE olap.dim_customer CASCADE")
                for row in rows:
                    first_purchase = row[9]
                    cohort = first_purchase.strftime('%Y-%m') if first_purchase else None
                    cur.execute("""
                        INSERT INTO olap.dim_customer (
                            customer_key, customer_id, first_name, last_name,
                            full_name, email, customer_type, store_name,
                            territory, country, first_purchase_date, cohort_year_month
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, (row[0], row[0], row[1], row[2], row[3], row[4],
                          row[5], row[6], row[7], row[8], first_purchase, cohort))
            olap.commit()
            logger.info(f"dim_customer cargada con {len(rows)} clientes")
        finally:
            oltp.close()
            olap.close()

    def load_dim_product(self):
        logger.info("Cargando dim_product...")
        oltp = get_oltp_connection()
        olap = get_olap_connection()
        try:
            with oltp.cursor() as cur:
                cur.execute("""
                    SELECT
                        p.productid,
                        p.productid,
                        p.name,
                        p.productnumber,
                        pc.name as category,
                        ps.name as subcategory,
                        pm.name as model,
                        p.color,
                        p.size,
                        p.weight,
                        p.listprice,
                        p.standardcost
                    FROM production.product p
                    LEFT JOIN production.productsubcategory ps ON p.productsubcategoryid = ps.productsubcategoryid
                    LEFT JOIN production.productcategory pc ON ps.productcategoryid = pc.productcategoryid
                    LEFT JOIN production.productmodel pm ON p.productmodelid = pm.productmodelid
                """)
                rows = cur.fetchall()

            with olap.cursor() as cur:
                cur.execute("TRUNCATE olap.dim_product CASCADE")
                for row in rows:
                    cur.execute("""
                        INSERT INTO olap.dim_product (
                            product_key, product_id, product_name, product_number,
                            category, subcategory, model, color, size, weight,
                            list_price, standard_cost
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, row)
            olap.commit()
            logger.info(f"dim_product cargada con {len(rows)} productos")
        finally:
            oltp.close()
            olap.close()