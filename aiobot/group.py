from aiogram import types, Router, F
from aiogram.enums import ChatType
from aiogram.types import FSInputFile, ChatMemberUpdated
from aiogram.filters.chat_member_updated import ChatMemberUpdatedFilter, MEMBER
from sqlalchemy.ext.asyncio import AsyncSession
from aiobot.client_kb import group_kb
from data_base.orm_query import orm_add_user

group_router = Router()


@group_router.chat_member(ChatMemberUpdatedFilter(member_status_changed=MEMBER))
async def greet_new_member(event: ChatMemberUpdated, session: AsyncSession):
    photo = FSInputFile('media/VTG.png')
    if event:
        user = event.new_chat_member.user
        await orm_add_user(
        session,
        user_id=user.id,
        full_name=user.full_name,
        user_name=user.username,
    )
        await event.answer_photo(photo=photo,
            caption=f'Добро пожаловать в группу ТОО "ВостокТехГаз" {user.full_name}!'
            'Вы можете заказать товары либо написать оператору',
            reply_markup=group_kb
        )
