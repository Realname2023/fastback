from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from admin.utils import hash_password
from data_base.engine import session_maker
from data_base.models import Good, Adminer, Category, User, City, Cart, Client, Order
from routers.anotations import (CartAddSerializer, ClientUpdateSerializer, OrderAddSerializer)


async def create_superuser(username: str, password: str):
    async with session_maker() as session:
        query = select(Adminer).where(Adminer.username == username)
        result = await session.execute(query)
        if result.first() is None:
            hashed_password = hash_password(password)
            session.add(
                Adminer(username=username, password=hashed_password, is_superuser=True)
            )
            await session.commit()


async def select_superuser(username: str):
    async with session_maker() as session:
        query = select(Adminer).where(Adminer.username == username)
        result = await session.execute(query)
        return result.scalar()


async def orm_add_user(
    session: AsyncSession,
    user_id: int,
    full_name: str | None = None,
    user_name: str | None = None,
):
    
    query = select(User).where(User.user_id == user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(
            User(user_id=user_id, full_name=full_name, user_name=user_name)
        )
        await session.commit()


# async def add_client(client_in: ClientAddBase):
#     async with session_maker() as session:
#         client = Client(**client_in.model_dump())
#         query = select(Client).where(Client.user_id == client.user_id)
#         result = await session.execute(query)
#         if result.first() is None:
#             session.add(client)
#             await session.commit()
#             return client


async def add_client(session: AsyncSession, user_id: int, org_name: str, phone: str):
    query = select(Client).where(Client.user_id == user_id)
    result = await session.execute(query)
    if result.first() is None:
        session.add(Client(user_id=user_id, org_name=org_name, phone=phone))
        await session.commit()

# async def select_user(session: AsyncSession, user_id: int):
#     query = select(User).where(User.user_id == user_id)
#     result = await session.execute(query)
#     user = result.first()
#     return user

async def select_client_by_bot(session: AsyncSession, user_id: int):
    query = select(Client).options(joinedload(Client.user)).where(Client.user_id == user_id)
    result = await session.execute(query)
    return result.scalar()


async def select_client(user_id: int):
    async with session_maker() as session:
        query = select(Client).options(joinedload(Client.user)).where(Client.user_id == user_id)
        result = await session.execute(query)
        return result.scalar()


async def update_client(client_in: ClientUpdateSerializer):
    async with session_maker() as session:
        client = Client(**client_in.model_dump())
        query = update(Client).where(Client.user_id == client.user_id).values(
            {Client.org_name: client.org_name, Client.client_city: client.client_city,
             Client.address: client.address, Client.phone: client.phone,
             Client.is_contract:client.is_contract}
        ).returning(Client)
        result = await session.execute(query)
        updated_client = result.scalar()
        await session.commit() 
        return updated_client



async def get_all_categories():
    async with session_maker() as session:
        query = select(Category).order_by(Category.id)
        result = await session.execute(query)
        return result.scalars().all()
    

async def select_all_cities():
    async with session_maker() as session:
        query = select(City).order_by(City.id)
        result = await session.execute(query)
        return result.scalars().all()


async def select_goods_by_category(category_id: int):
    async with session_maker() as session:
        query = select(Good).options(joinedload(Good.city)).where(
            Good.category_id == category_id).order_by(Good.id)
        result = await session.execute(query)
        return result.scalars().all()
    

async def select_arenda_goods():
    async with session_maker() as session:
        query = select(Good).options(joinedload(Good.city)).where(
            Good.category_id == 5).order_by(Good.id)
        result = await session.execute(query)
        return result.scalars().all()


async def select_goods_by_category_city(category_id: int, city_id: int):
    async with session_maker() as session:
        query = select(Good).options(joinedload(Good.city)).where(Good.category_id == category_id,
                                   Good.city_id == city_id).order_by(Good.id)
        result = await session.execute(query)
        return result.scalars().all()


async def select_product(good_id: int):
    async with session_maker() as session:
        query = select(Good).options(joinedload(Good.city)).where(Good.id == good_id)
        result = await session.execute(query)
        return result.scalar()


async def select_carts(user_id: int):
    async with session_maker() as session:
        query = select(Cart).options(joinedload(Cart.good)).where(Cart.user_id==user_id)
        result = await session.execute(query)
        return result.scalars().all()


async def select_carts_purch_arenda(user_id: int):
    async with session_maker() as session:
        query1 = select(Cart).options(joinedload(Cart.good)).where(Cart.user_id==user_id,
                                                                  Cart.is_arenda == False)
        query2 = select(Cart).options(joinedload(Cart.good)).where(Cart.user_id==user_id,
                                                                  Cart.is_arenda == True)
        result1 = await session.execute(query1)
        result2 = await session.execute(query2)
        goods = result1.scalars().all()
        arenda_goods = result2.scalars().all()
        return {'goods': goods, 'arenda_goods': arenda_goods}



async def select_cart(user_id: int, good_id):
    async with session_maker() as session:
        query = select(Cart).where(Cart.user_id == user_id, Cart.good_id == good_id)
        result = await session.execute(query)
        return result.scalar()


async def add_cart(cart_in: CartAddSerializer):
    async with session_maker() as session:
        cart = Cart(**cart_in.model_dump())
        query = select(Cart).where(Cart.user_id == cart.user_id, 
                                   Cart.good_id == cart.good_id)
        result = await session.execute(query)
        user_cart = result.scalar()
        if user_cart:
            for name, value in cart_in.model_dump(exclude_unset=True).items():
                setattr(user_cart, name, value)
        else:
            user_cart = cart
            session.add(user_cart)
        
        await session.commit()
        return user_cart  


async def update_cart(cart_in: CartAddSerializer):
    async with session_maker() as session:
        cart = Cart(**cart_in.model_dump())
        query = update(Cart).where(Cart.user_id == cart.user_id, 
                                   Cart.good_id == cart.good_id).values(
                                       {Cart.quantity: cart.quantity,
                                        Cart.arenda_time: cart.arenda_time,
                                        Cart.is_delivery: cart.is_delivery,
                                        Cart.is_contract: cart.is_contract,
                                        Cart.total_price: cart.total_price}
                                   ).returning(Cart)
        result = await session.execute(query)
        user_cart = result.scalar()
        await session.commit() 
        return user_cart
    

async def delete_cart(user_id: int, good_id: int):
    async with session_maker() as session:
        query = delete(Cart).where(Cart.user_id == user_id, Cart.good_id == good_id)
        await session.execute(query)
        await session.commit()


async def delete_user_carts(user_id: int):
    async with session_maker() as session:
        query = delete(Cart).where(Cart.user_id == user_id)
        await session.execute(query)
        await session.commit()


async def add_order(order_in: OrderAddSerializer):
    async with session_maker() as session:
        order = Order(**order_in.model_dump())
        session.add(order)
        await session.commit()
