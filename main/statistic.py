import json
from django.db import connection



def get_section_statistic(section, currency, month: int = None, year: int = None):
    month_filter = f"WHERE month = '{year}-{'0' if int(month) < 10 else ''}{month}'" if month and year else ''
    query = f'''
        WITH product_prices_with_currency AS (
        SELECT
            TO_CHAR(r.date, 'YYYY-MM') AS month,
            r.currency_id AS currency_id,
            SUM(p.price) AS receipt_currency_total_price,
            pc.name AS category_name,
            ROUND(SUM(crh_last2.per_usd * (p.price / crh_last.per_usd)), 2) AS selected_currency_total_price,
            c.code AS selected_currency_code
        
        FROM public.main_section as s
            LEFT JOIN main_receipt AS r ON r.section_id = s.id
            LEFT JOIN main_product AS p ON p.receipt_id = r.id
            
            LEFT JOIN LATERAL (
                SELECT crh.*
                FROM main_currencyratehistory AS crh
                WHERE crh.currency_id = r.currency_id
                AND crh.date <= CAST(r.date AS DATE)
                ORDER BY crh.date DESC
                LIMIT 1
            ) AS crh_last ON TRUE
            LEFT JOIN LATERAL (
                SELECT crh2.*
                FROM main_currencyratehistory AS crh2
                WHERE crh2.currency_id = {currency.id}
                AND crh2.date <= crh_last.date
                ORDER BY crh2.date DESC
                LIMIT 1
            ) AS crh_last2 ON TRUE
            LEFT JOIN main_productcategory AS pc ON pc.id = category_id
            LEFT JOIN main_currency AS c ON c.id = {currency.id}
        
        WHERE s.id = {section.id}
        
        GROUP BY month, r.currency_id, pc.name, c.code
        ORDER BY month DESC, category_name, selected_currency_total_price DESC
        )
        
        SELECT
            month,
            jsonb_object_agg(
            category_name,
            jsonb_build_object(
                'name', category_name,
                'currencies', agg_currencies,
                'selected_currency_total_price', selected_currency_total_price
            )
            ) AS categories
        FROM (
            SELECT
                month,
                category_name,
                jsonb_object_agg(code, receipt_currency_total_price) AS agg_currencies,
                SUM(selected_currency_total_price) AS selected_currency_total_price
            FROM product_prices_with_currency AS p
                LEFT JOIN main_currency AS c ON c.id = p.currency_id
                GROUP BY month, category_name
                HAVING category_name IS NOT NULL
        ) AS subquery
        {month_filter}
        GROUP BY month;

    '''
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

    for d in data:
        d['categories'] = json.loads(d['categories'])
        d['base_currency'] = currency.code

    return data
