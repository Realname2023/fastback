from fastapi import APIRouter
from data_base.orm_query import create_superuser


admin_router = APIRouter(prefix='/add_admin', tags=['Админы'])


@admin_router.post('/', summary='Добавить админа')
async def add_admin(username:str, password: str):
    await create_superuser(username=username, password=password)
    return {'res':'ok'}
