from aiogram import types, Router, F
from aiogram.types import FSInputFile
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from data_base.orm_query import orm_add_user, add_client, select_client_by_bot
from aiobot.client_kb import kb_client, phone_button_kb


class FSMClient(StatesGroup):
    org_name = State()
    phone = State()


start_router=Router()

@start_router.message(CommandStart())
async def command_start_handler(message: types.Message, state: FSMContext,
                                session: AsyncSession) -> None:
    photo = FSInputFile('media/VTG.png')
    user = message.from_user
    await orm_add_user(
        session=session,
        user_id=user.id,
        full_name=user.full_name,
        user_name=user.username,
    )

    client = await select_client_by_bot(session=session, user_id=user.id)
    
    if client is None:
        await message.answer_photo(photo=photo,
                            caption='Здравствуйте. Вы написали в компанию ТОО "ВостокТехГаз". Вы можете оставить вашу заявку  и мы обработаем ее в течение часа.')
        await message.answer('Зарегистрируйтесь. Укажите как к вам обращаться')
        await state.set_state(FSMClient.org_name)
    else:
        await message.answer_photo(photo=photo,
                            caption='Здравствуйте. Вы написали в компанию ТОО "ВостокТехГаз". Вы можете оставить вашу заявку  и мы обработаем ее в течение часа.', 
                            reply_markup=kb_client)



@start_router.message(FSMClient.org_name, F.text)
async def set_client_org_name(message: types.Message, state: FSMContext):
    org_name = message.text
    await state.update_data(org_name=org_name)
    await message.answer("Для обратной связи поделитесь контактом. Нажмите /Поделиться_контактом", 
                         reply_markup=phone_button_kb)
    await state.set_state(FSMClient.phone)


@start_router.message(FSMClient.phone)
async def indicate_phone(message: types.Message, state: FSMContext, session: AsyncSession):
    await message.edit_reply_markup()
    phone = message.contact.phone_number
    user_id = message.from_user.id
    data = await state.get_data()
    org_name = data.get("org_name")
    await add_client(session=session, user_id=user_id, org_name=org_name, phone=phone)
    await state.clear()
    await message.answer('ВЫ успешно зарегистрировались', reply_markup=kb_client)
