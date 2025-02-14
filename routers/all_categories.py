from fastapi import APIRouter
from data_base.orm_query import get_all_categories
from routers.anotations import CategorySerializer

cat_router = APIRouter(tags=['Категории'])


@cat_router.get('/', summary='Все категории', response_model=list[CategorySerializer])
async def get_catalog():
    catalog = await get_all_categories()
    return catalog
