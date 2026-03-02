from src.utils.db import get_oltp_connection, get_olap_connection
from src.utils.logger import get_logger

logger = get_logger(__name__)

class SalesPipeline:
    def run(self):
        self.load_fact_sales()

    def load_fact_sales(self):
        logger.info("Cargando fact_sales...")
        oltp = get_oltp_connection()
        olap = get_olap_connection()
        try:
            with oltp.cursor() as cur:
                cur.execute("""
                    SELECT
                        soh.salesorderid,
                        sod.salesorderdetailid,
                        soh.orderdate::date,
                        soh.duedate::date,
                        soh.shipdate::date,
                        soh.customerid,
                        sod.productid,
                        COALESCE(soh.territoryid, 1),
                        sod.orderqty,
                        sod.unitprice,
                        p.standardcost,
                        sod.unitpricediscount,
                        sod.linetotal,
                        soh.onlineorderflag
                    FROM sales.salesorderheader soh
                    JOIN sales.salesorderdetail sod ON soh.salesorderid = sod.salesorderid
                    JOIN production.product p ON sod.productid = p.productid
                """)
                rows = cur.fetchall()

            with olap.cursor() as cur:
                cur.execute("TRUNCATE olap.fact_sales CASCADE")
                batch = []
                for row in rows:
                    order_id, detail_id, order_date, due_date, ship_date, \
                    customer_id, product_id, territory_id, qty, unit_price, \
                    unit_cost, discount, line_total, is_online = row

                    date_key = int(order_date.strftime('%Y%m%d'))
                    line_cost = float(unit_cost) * float(qty)
                    line_margin = float(line_total) - line_cost
                    margin_pct = (line_margin / float(line_total) * 100) if float(line_total) > 0 else 0
                    discount_amount = float(unit_price) * float(qty) * float(discount)

                    batch.append((
                        order_id, detail_id, date_key, customer_id,
                        product_id, territory_id, qty, unit_price,
                        unit_cost, discount_amount, line_total,
                        line_cost, line_margin, margin_pct,
                        order_date, due_date, ship_date, is_online
                    ))

                    if len(batch) >= 1000:
                        cur.executemany("""
                            INSERT INTO olap.fact_sales (
                                order_id, order_detail_id, date_key, customer_key,
                                product_key, territory_key, order_quantity, unit_price,
                                unit_cost, discount_amount, line_total,
                                line_cost, line_margin, margin_pct,
                                order_date, due_date, ship_date, is_online_order
                            ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        """, batch)
                        batch = []

                if batch:
                    cur.executemany("""
                        INSERT INTO olap.fact_sales (
                            order_id, order_detail_id, date_key, customer_key,
                            product_key, territory_key, order_quantity, unit_price,
                            unit_cost, discount_amount, line_total,
                            line_cost, line_margin, margin_pct,
                            order_date, due_date, ship_date, is_online_order
                        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    """, batch)

            olap.commit()
            logger.info(f"fact_sales cargada con {len(rows)} registros")
        finally:
            oltp.close()
            olap.close()