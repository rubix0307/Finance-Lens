import time

from aiogram import types
from aiogram.types import FSInputFile
from aiogram.utils.markdown import hlink, hpre

from bot.run import bot, dp
from GPT.functions import get_products_by_image
from main.models import Currency, Product, ProductCategory, Receipt


@dp.message()
async def message_handler(message: types.Message) -> None:
    try:
        if message.photo or message.document:

            if message.photo:
                image_name = f"{message.chat.id}_{message.photo[-1].file_id}.jpg"
                image_path = f"budget_lens/media/bot/{image_name}"
                file = message.photo[-1]
            else:
                image_name = f"{message.chat.id}_{message.document.file_id}.jpg"
                image_path = f"budget_lens/media/bot/{image_name}"
                file = message.document

            await bot.download(file, destination=image_path)
            await bot.send_chat_action(chat_id=message.chat.id,action='typing')
            data = get_products_by_image(image_path)

            currency, is_created = await Currency.objects.aget_or_create(code=data['currency'])
            receipt = Receipt(
                shop_name=data['shop_name'],
                shop_address=data['shop_address'],
                currency=currency,
                photo=f'bot/{image_name}',
                date=time.time(),
            )
            await receipt.asave()
            products = []
            for p in data['products']:
                try:
                    category = await ProductCategory.objects.aget(name=p['category'])
                except ProductCategory.DoesNotExist:
                    category = ProductCategory(name=p['category'])
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

            texts = [
                f'Магазин: {receipt.shop_name}',
                f'Адрес: {hlink(receipt.shop_address, f"https://www.google.com/maps/search/{receipt.shop_address}".replace(" ", "+"))}',
                f'Товары:',
            ]
            space = 25
            for product in products:
                row = f'ㅤ{product.name.ljust(space, " ")} {product.price}'
                texts.append(hpre(row))

            total = sum(p.price for p in products)
            texts.append(hpre(f'ㅤВсего:'.ljust(space, " ")+f' {round(total, 2)} {currency.code}'))

            answer = await bot.send_photo(
                photo=FSInputFile(image_path),
                chat_id=message.chat.id,
                caption='\n'.join(texts),
                parse_mode='HTML',
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


    except Exception as ex:
        print(ex)



