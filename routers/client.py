from fastapi import APIRouter
from data_base.orm_query import select_client, update_client
from routers.anotations import ClientSerializer, ClientUpdateSerializer


client_router = APIRouter(prefix='/client', tags=['Клиенты'])


# @client_router.post('/add/')
# async def client_add(client_in: ClientAddBase):
#     client = await add_client(client_in=client_in)
#     if client is not None:
#         return client
#     else:
#         return {'res': 'false'}


@client_router.get('/get/{user_id}', summary='Данные клиента', response_model=ClientSerializer)
async def get_client(user_id: int):
    client = await select_client(user_id=user_id)
    return client


@client_router.patch('/update/', summary='Обновить клиента', response_model=ClientSerializer)
async def client_update(client_in: ClientUpdateSerializer):
    client = await update_client(client_in=client_in)
    return client
