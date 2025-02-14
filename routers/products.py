from fastapi import APIRouter
from data_base.orm_query import (select_goods_by_category, select_goods_by_category_city, 
                                 select_product)
from routers.anotations import GoodSerializer


good_router = APIRouter(prefix='/catalog', tags=['Каталог'])


@good_router.get('/good/{good_id}', summary='Получить товар', response_model=GoodSerializer)
async def get_product(good_id: int):
    good = await select_product(good_id=good_id)
    return good


@good_router.get('/{category_id}/', summary='Категория товаров', 
                response_model=list[GoodSerializer])
async def get_category_by_id(category_id: int):
    goods = await select_goods_by_category(category_id=category_id)
    return goods


@good_router.get('/{category_id}/{city_id}', summary='Категория товаров в городе', 
                response_model=list[GoodSerializer])
async def get_goods_by_category_city(category_id: int, city_id: int):
    goods = await select_goods_by_category_city(category_id=category_id, city_id=city_id)
    return goods
