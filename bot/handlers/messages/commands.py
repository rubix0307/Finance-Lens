from aiogram import types
from aiogram.types import FSInputFile
from aiogram.utils.markdown import hlink, hpre

from bot.run import bot, dp
from GPT.functions import get_products_by_image


@dp.message()
async def message_handler(message: types.Message) -> None:
    try:
        if message.photo or message.document:

            if message.photo:
                image_path = f"budget_lens/media/bot/{message.chat.id}_{message.photo[-1].file_id}.jpg"
                file = message.photo[-1]
            else:
                image_path = f"budget_lens/media/bot/{message.chat.id}_{message.document.file_id}.jpg"
                file = message.document

            await bot.download(file, destination=image_path)
            await bot.send_chat_action(chat_id=message.chat.id,action='typing')
            data = get_products_by_image(image_path)

            is_translation = True
            for i in range(2):
                try:
                    texts = [
                        f'Магазин: {data["shop_name"]}',
                        f'Адрес: {hlink(data["shop_address"], "https://www.google.com/maps/search/"+str(data["shop_address"]).replace(" ", "+"))}',
                        f'Товары:',
                    ]
                    space = 25
                    for product in data['products']:
                        row = f'ㅤ{product["name"].ljust(space, " ")} {product["price"]}'
                        if is_translation:
                            row += "\n" + product["name_translation"].ljust(space, " ")
                        texts.append(hpre(row))

                    texts.append(hpre(f'ㅤВсего:'.ljust(space, " ")+f' {round(data["total"], 2)} {data["currency"]}'))

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
                    break
                except Exception as ex:
                    is_translation = False
                    continue
    except Exception as ex:
        print(ex)



