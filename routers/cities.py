from fastapi import APIRouter
from data_base.orm_query import select_all_cities
from routers.anotations import CitySerializer


city_router = APIRouter(prefix='/cities', tags=['Города'])


@city_router.get('/', summary='Все города', response_model=list[CitySerializer])
async def get_cities():
    cities = await select_all_cities()
    return cities