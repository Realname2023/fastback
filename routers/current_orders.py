from fastapi import APIRouter, status, Body
from data_base.orm_query import (select_carts, add_cart, update_cart, delete_cart, 
                                 select_carts_purch_arenda, delete_user_carts)
from routers.anotations import CartSerializer, CartAddSerializer, CartGetSerializer


cart_router = APIRouter(prefix='/cart', tags=['Корзины'])


@cart_router.get('/get/{user_id}', summary='Корзины пользователя', 
                 response_model=list[CartSerializer])
async def get_user_carts(user_id: int):
    carts = await select_carts(user_id=user_id)
    return carts


@cart_router.get('/get_carts/{user_id}', summary='Корзины покупка и аренда',
                 response_model=CartGetSerializer)
async def get_user_prch_arenda(user_id: int):
    carts = await select_carts_purch_arenda(user_id=user_id)
    return carts


@cart_router.post('/add/', summary='Добавить корзину',
                  response_model=CartAddSerializer,
                  status_code=status.HTTP_201_CREATED)
async def cart_add(cart_in: CartAddSerializer):
    cart = await add_cart(cart_in=cart_in)
    return cart


@cart_router.patch('/update/', summary='Обновить корзину',
                   response_model=CartSerializer)
async def cart_update(cart_in: CartAddSerializer):
    updated_cart = await update_cart(cart_in=cart_in)
    return updated_cart


@cart_router.delete('/delete/', summary='Удалить корзину', 
                    status_code=status.HTTP_204_NO_CONTENT)
async def cart_delete(user_id: int = Body(), good_id: int = Body()):
    await delete_cart(user_id=user_id, good_id=good_id)


@cart_router.delete('/delete_carts/', summary='Удалить корзины',
                    status_code=status.HTTP_204_NO_CONTENT)
async def carts_delete(user_id: int = Body()):
    await delete_user_carts(user_id=user_id)

