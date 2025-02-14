from aiogram import types, Router, F
from aiobot.client_kb import kb_client


client_router = Router()


@client_router.callback_query(F.data=='addres')
async def show_place(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Адреса:\nг. Семей, ул. Джангильдина 82/1, район областной больницы\n"
        "https://go.2gis.com/us0av\n"
        "\n"
        "г. Усть-Каменогорск, ул. Абая 181, возле рынка 'Дина'\n"
        "https://go.2gis.com/o9b30v\n"
        "\n"
        "г. Павлодар, ул. Малая объездная 9/1, за ТЦ 'Батырмолл'\n"
        "https://go.2gis.com/hdsq0\n"
        "\n"
        "г. Астана, проспект Абая 99/1, бывшая база ВторЧерМет\n"
        "https://go.2gis.com/xhrt6\n"
        "\n"
        "Контакты:\n"
        "Единый номер: +7 777 954 5000 WhatsApp\n",
                                        reply_markup=kb_client)
    await call.answer()


@client_router.callback_query(F.data=='worktime')
async def show_work_time(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer(
        '                                                            '
        'Семей 08.30 - 17.00,\nУсть-Каменогорск 08.00 - 17.00.\nПавлодар 08.30 - 17.30,\nАстана 08.30 - 17.00',
        reply_markup=kb_client)
    await call.answer()


@client_router.callback_query(F.data=='voices')
async def voices(call: types.CallbackQuery):
    await call.message.edit_reply_markup()
    await call.message.answer("Полезные ссылки:\n"
                              "WhatsApp\n"
                              "https://wa.me/77779545000\n"
                              "Instagram\n"
                              "https://www.instagram.com/vtg_gaz/\n"
                              "email\n"
                              "vostoktehgaz@mail.ru\n"
                              "\n"
                              "Отзывы можно оставить по ссылкам:\n"
                              "Семей:\n"
                              "https://go.2gis.com/us0av\n"
                              "Усть-Каменогорск:\n"
                              "https://go.2gis.com/o9b30v\n"
                              "Павлодар:\n"
                              "https://go.2gis.com/hdsq0\n"
                              "Астана:\n"
                              "https://go.2gis.com/xhrt6",
                              reply_markup=kb_client)
    
