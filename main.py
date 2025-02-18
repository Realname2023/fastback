import uvicorn
import asyncio
import logging
import sys
from aiogram.types.update import Update
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin
from run_bot import bot, dp, on_startup, on_shutdown
from aiobot.middlevares import DataBaseSession
from data_base.engine import engine, create_db, bot_session_maker
from admin.admin_panel import (GoodAdmin, CategoryAdmin, CityAdmin, 
                              UserAdmin, ClientAdmin, CartAdmin, OrderAdmin)
from admin.auth import authentication_backend
from routers.all_categories import cat_router
from routers.create_admin import admin_router
from routers.cities import city_router
from routers.products import good_router
from routers.current_orders import cart_router
from routers.client import client_router
from routers.order import order_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_db()
    webhook_url = 'https://9763-2-135-77-4.ngrok-free.app/webhook'
    # dp.startup.register(on_startup)
    # dp.shutdown.register(on_shutdown)
    dp.update.middleware(DataBaseSession(session_pool=bot_session_maker))
    await bot.set_webhook(
        url=webhook_url,
        allowed_updates=dp.resolve_used_update_types(),
        drop_pending_updates=True
    )
    logging.info(f"Webhook set to {webhook_url}")

    yield

    await bot.delete_webhook()
    logging.info("Webhook removed")



app = FastAPI(lifespan=lifespan)



app.include_router(admin_router)
app.include_router(good_router)
app.include_router(cat_router)
app.include_router(city_router)
app.include_router(cart_router)
app.include_router(client_router)
app.include_router(order_router)


admin = Admin(app, engine=engine, authentication_backend=authentication_backend)

admin.add_view(GoodAdmin)
admin.add_view(CategoryAdmin)
admin.add_view(ClientAdmin)
admin.add_view(CityAdmin)
admin.add_view(UserAdmin)
admin.add_view(CartAdmin)
admin.add_view(OrderAdmin)


@app.post("/webhook")
async def webhook(request: Request) -> None:
    logging.info("Received webhook request")
    update = Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)
    logging.info("Update processed")


origins = ['http://localhost:5173', 
           'http://127.0.0.1:5173']


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)



if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', reload=True)
