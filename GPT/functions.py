import json

from functions import encode_image
from .config import client


def get_products_by_image(image_path):
    print('image was sent')
    base64_image = encode_image(image_path)

    categories = ','.join(['Еда и напитки', 'Транспорт', 'Одежда', 'Лекарства и гигиена',
                            'Образование', 'Домашние товары', 'Развлечения и досуг',
                            'Путешествия', 'Связь и интернет', 'Домашние животные',
                            ])

    messages = [
        {'role': 'system', 'content':
            'Переведи данные фотографии чека формата'
            '{"products": [{"name": название, "price": цена float, "category": категория товара}], '
            ' "shop_name": название заведения где был выдан чек}, '
            ' "shop_address": адрес заведения, '
            ' "currency": (alfa-3) код валюты (если она не указана явно, то определи ее, по местоположению), '
            '}.'
            'Категория товаров может быть исключительно одна из этого списка:'
            f'{categories}'            
            'Ты должен дать исключительно список покупок без другой информации в формате JSON. '
            'Так же, в некоторых магазинах, после строки с товаром е его ценой, пишут как эта цена получилась,'
            'например: "0,62 kg x 9 EUR/kg" или подобные записи.'
            'Они не должны учитываться.'
        },
        {
          'role': 'user',
          'content': [
            # {
            #   'type': 'text',
            #   'text': f'Данные для уточнения и проверки:\n{image_text}'
            # },
            {
              'type': 'image_url',
              'image_url': {
                'url': f'data:image/jpeg;base64,{base64_image}'
              }
            }
          ]
        }
    ]
    response = client.chat.completions.create(
        model='gpt-4o',
        response_format={'type': 'json_object'},
        messages=messages,
    )

    data = json.loads(response.choices[0].message.content)
    data['total'] = sum([i['price'] for i in data['products'] if type(i['price']) in [int, float]])

    return data
