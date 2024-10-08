import json
from datetime import datetime

from functions import encode_image
from main.models import ProductCategory
from .config import client


def get_products_by_image(image_path):
    print('image was sent')
    base64_image = encode_image(image_path)

    content = [
        {
            'type': 'image_url',
            'image_url': {
                'url': f'data:image/jpeg;base64,{base64_image}'
            }
        }
    ]

    categories = ', '.join(list(f'{c[0]}="{c[1]}"' for c in ProductCategory.objects.values_list('id', 'name')))

    messages = [
        {
            'role': 'system',
            'content': (
                'Переведи данные фотографии чека формата '
                '{ is_recipe: bool - является ли фотография чеком или на ней есть информация об оплаченных товарах/услугах '
                'или имеет ли какую-то информацию о товарах или услугах, которую можно использовать в ответе. Уведомления '
                'о подписках на различные сервисы - является чеком. '
                '"products": список товаров или услуг = [ '
                    '{"name_original": название товара/услуги на языке оригинала, '
                    '"name_en": перевод name_original на англ, '
                    '"name_ru": перевод name_original на русский, '
                    '"name_ua": перевод name_original на украинский, '
                    '"price": цена float, '
                    '"category_id": id категории из списка'
                '}], '
                '"shop_name": название заведения, где был выдан чек (если ее нет - null), '
                '"shop_address": адрес заведения (если ее нет - null), '
                'date: str = (год из чека, если отсутствует - текущий год; месяц из чека, если отсутствует - текущий месяц; '
                'день из чека, если отсутствует - date=null; час из чека, если отсутствует - не указывай), '
                '"currency": (alfa-3) код валюты (если она не указана явно, то определи ее по местоположению) '
                '}. '
                'Категория товаров может быть исключительно одна из этого списка: '
                f'{categories}. '
                'Ты должен дать исключительно список покупок без другой информации в формате JSON. '
                'Также, в некоторых магазинах, после строки с товаром и его ценой, пишут как эта цена получилась, '
                'например: "0,62 kg x 9 EUR/kg" или подобные записи. '
                'Они не должны учитываться. '
                'Также ты должен заполнять названия с учётом языковых ожиданий поля. Если явно указано "name_ru", то название, '
                'если оно не на русском языке, должно быть переведено. '
                
                'Если у тебя на изображении просто перевод денег, или что-то подобное, то скорее всего это относится к категории Кредиты и займы, products заполни соответствующе.'
                f'Сегодня: {datetime.now().strftime("%Y-%m-%d")}'
            )
        },
        {
            'role': 'user',
            'content': content,
        }
    ]

    response = client.chat.completions.create(
        model='gpt-4o',
        response_format={'type': 'json_object'},
        messages=messages,
    )

    data = json.loads(response.choices[0].message.content)
    data['total'] = sum([i['price'] for i in data.get('products', []) if type(i['price']) in [int, float]])

    return data if data.get('is_recipe') else {}
