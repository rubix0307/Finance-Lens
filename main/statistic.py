from collections import defaultdict
from django.db import connection



def get_section_statistic(section):
    result = defaultdict(
        lambda: defaultdict(lambda: {'category': None, 'base_currency': None, 'total_base_currency': 0,
                                     'currencies': defaultdict(int)}))

    query = f'''
    SELECT 
        to_char(r.date, 'YYYY-MM') AS date,
        SUM(p.price) AS total_receipt_price,
        c1.code AS receipt_currency_code,
        SUM(pp.price) AS total_section_price,
        c.code AS section_currency_code,
        pc.name AS product_category_name
        
    FROM public.main_section as s
    
    LEFT JOIN main_receipt AS r ON r.section_id = s.id
    LEFT JOIN main_product AS p ON p.receipt_id = r.id
    LEFT JOIN main_productprice AS pp ON pp.product_id = p.id AND s.currency_id = pp.currency_id
    LEFT JOIN main_currency AS c ON c.id = pp.currency_id
    LEFT JOIN main_currency AS c1 ON c1.id = r.currency_id
    LEFT JOIN main_productcategory AS pc ON pc.id = p.category_id
    
    GROUP BY r.currency_id, pp.currency_id, date, pc.name, pc.id, c.code, c1.code
    
    ORDER BY date DESC, pc.id DESC;
    '''
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]


    for item in data:
        category = item['product_category_name']
        if category:
            result[item['date']][category]['category'] = category
            result[item['date']][category]['base_currency'] = item['section_currency_code']
            result[item['date']][category]['total_base_currency'] += item['total_section_price']
            result[item['date']][category]['currencies'][item['receipt_currency_code']] += item['total_receipt_price']

    return [{'month': k, 'categories': v} for k, v in result.items()]
