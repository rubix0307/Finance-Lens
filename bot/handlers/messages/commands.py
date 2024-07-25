import datetime
import time

from aiogram import types
from aiogram.types import FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hlink, hpre
from django.contrib.auth import get_user_model
from dateutil import parser

from bot.run import bot, dp
from GPT.functions import get_products_by_image
from main.models import Currency, Product, ProductCategory, Receipt


async def parse_receipt(message: types.Message, image_path, image_name) -> bool | Receipt:
    data = get_products_by_image(image_path)

    if not data:
        return False

    user, created = await get_user_model().objects.aget_or_create(
        telegram_id=message.from_user.id,
        defaults={
            'first_name': message.from_user.first_name,
            'language_code': message.from_user.language_code,
            'last_name': message.from_user.last_name,
            'username': message.from_user.username,
        }
    )

    currency, is_created = await Currency.objects.aget_or_create(code=data['currency'])

    try:
        date = parser.parse(data.get('date'))
    except TypeError as e:
        date = datetime.datetime.fromtimestamp(time.time())

    receipt = Receipt(
        shop_name=data['shop_name'],
        shop_address=data['shop_address'],
        currency=currency,
        photo=f'bot/{image_name}',
        date=date,
        owner=user,
    )
    await receipt.asave()
    products = []
    for p in data['products']:
        try:
            try:
                category = await ProductCategory.objects.aget(name_ru=p['category_ru'])
            except ProductCategory.DoesNotExist:
                category = ProductCategory(
                    name=p['category_ru'],
                    name_en=p['category_en'],
                    name_ru=p['category_ru'],
                    name_ua=p['category_ua'],
                )
                await category.asave()

            product = Product(
                name=p['name_original'].capitalize(),
                name_original=p['name_original'].capitalize(),
                name_en=p['name_en'].capitalize(),
                name_ru=p['name_ru'].capitalize(),
                name_ua=p['name_ua'].capitalize(),
                price=p['price'],
                category=category,
                receipt=receipt,
            )
            await product.asave()
            products.append(product)

        except Exception as ex:
            continue

    return receipt

async def save_message_media(message: types.Message):
    if message.photo:
        image_name = f"{message.chat.id}_{message.photo[-1].file_id}.jpg"
        image_path = f"budget_lens/media/bot/{image_name}"
        file = message.photo[-1]
    elif message.document:
        image_name = f"{message.chat.id}_{message.document.file_id}.jpg"
        image_path = f"budget_lens/media/bot/{image_name}"
        file = message.document
    else:
        return

    saved_file = await bot.download(file, destination=image_path)
    return image_name, image_path, saved_file

@dp.message()
async def message_handler(message: types.Message) -> None:
    try:
        if message.photo or message.document:
            message_media = await save_message_media(message)

            if message_media:
                image_name, image_path, *_ = await save_message_media(message)
                receipt = await parse_receipt(message, image_path, image_name)
                await bot.send_chat_action(chat_id=message.chat.id,action='typing')
                texts = [
                    'Фото было обработано'
                ]
                if receipt.shop_name and receipt.shop_address:
                    texts += [
                        f'Магазин: {receipt.shop_name}',
                        f'Адрес: {hlink(receipt.shop_address, f"https://www.google.com/maps/search/{receipt.shop_address}".replace(" ", "+"))}',
                    ]

                builder = InlineKeyboardBuilder()
                builder.row(InlineKeyboardButton(
                    text="Смотреть чек",
                    web_app=WebAppInfo(url="https://finance-lens.online/telegram-auth/web-app/")
                ))
                answer = await bot.send_photo(
                    photo=FSInputFile(image_path),
                    chat_id=message.chat.id,
                    caption='\n'.join(texts),
                    parse_mode='HTML',
                    reply_markup=builder.as_markup(),
                )

                if answer:
                    await message.delete()


                admin_id = 887832606
                if message.chat.id != admin_id:
                    await bot.send_photo(
                        photo=FSInputFile(image_path),
                        chat_id=admin_id,
                        caption='\n'.join(texts),
                        parse_mode='HTML',
                    )
            else:
                await message.answer('Произошла ошибка в сохранении медиа файла, проверьте что это именно фото.')
        else:
            await message.answer('Вы должны отправить фотографию чека')

    except Exception as ex:
        print(ex)



