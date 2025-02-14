from fastapi import APIRouter, status
from foundation import (url_webhook, b24rest_request, method_deal_add, method_contact_list, 
                        method_contact_update, method_contact_add, method_products_set)
from routers.anotations import OrderAddSerializer
from data_base.orm_query import add_order, select_client, select_carts_purch_arenda, delete_user_carts
from data_base.models import Order


order_router = APIRouter(prefix='/order', tags=['Заказы'])


@order_router.post('/add/', summary='Добавить заказ',
                   status_code=status.HTTP_201_CREATED)
async def order_add(order_in: OrderAddSerializer):
    await add_order(order_in=order_in)
    order = Order(**order_in.model_dump())
    # client = await select_client(user_id=order.user_id)
    # user_carts = await select_carts_purch_arenda(user_id=order.user_id)
    # client_city = client.client_city
    # client_address = client.address
    # client_phone = client.phone
    # tittle = client.user.full_name
    # linc = "не указан"
    # user_name = client.user.user_name

    # if user_name is not None:
    #     linc = f"https://t.me/{user_name}"
    
    # parametr_contact_list = {
	# 	'filter': {"PHONE": client_phone},
	# 	'select': ["ID", "NAME"]
	# }

    # response4 = await b24rest_request(url_webhook, method_contact_list, parametr_contact_list)

    # if response4.get('result') != []:

    #     contact_id = response4.get('result')[-1].get('ID')
    #     contact_name = response4.get('result')[-1].get('NAME')
    #     if contact_name == 'Без имени':
    #         parametr_contact_update = {
    #             "id": contact_id,
    #             "fields": {'NAME': tittle}
    #         }

    #         await b24rest_request(url_webhook, method_contact_update, parametr_contact_update)
    # else:
    #     parametr_contact_add = {"fields": {
    #                 "NAME": tittle,
    #                 "PHONE": [{'VALUE': client_phone, "VALUE_TYPE": "WORK"}],
    #                 "ADDRESS": client_address,
    #                 "ADDRESS_2": linc,
    #                 "ADDRESS_CITY": client_city,
    #                 "IM": [{
    #                     "VALUE": "Telegram",	
    #                     "VALUE_TYPE": "Telegram"}],
    #                 "SOURCE_ID": "UC_SLN7SG"
    #                 }}
        
    #     response2 = await b24rest_request(url_webhook, method_contact_add, parametr_contact_add)

    #     contact_id = str(response2.get('result'))
        

    # parametr_deal_add = {"fields": {
    #                 "TITLE": tittle,
    #                 "STAGE_ID": "NEW",
    #                 "SOURCE_ID": "UC_SLN7SG",
    #                 "CONTACT_ID": contact_id,
    #                 "UF_CRM_1708511776232": client_city,
    #                 "ASSIGNED_BY_ID": '7311',
    #                 "COMMENTS": order.order_text}}
    
    # response = await b24rest_request(url_webhook, method_deal_add, parametr_deal_add)

    # deal_id = str(response.get('result'))
    # poses = []

    # purchases = user_carts.get('goods')
    # arenda = user_carts.get('arenda_goods')

    # if purchases != []:
    #     for ret in purchases:
    #         quantity = ret.quantity
    #         price = ret.good.price

    #         pos = {"PRODUCT_ID": ret.good.b_id,
    #             "PRICE": float(price),
    #             "QUANTITY": quantity
    #             }
    #         poses.append(pos)
    
    # if arenda != []:
    #     for ret in arenda:
    #         quantity = ret.quantity
    #         price = ret.good.price

    #         for i in range(quantity):
    #             i = {"PRODUCT_ID": ret.good.b_id,
    #                     "PRICE": float(price),
    #                     "QUANTITY": ret.arenda_time,
    #                     "MEASURE_CODE": 323
    #                     }
    #             poses.append(i)
    
    # parametr_products_set = {
    #     "id": deal_id,
    #     "rows": poses}

    # await b24rest_request(url_webhook, method_products_set, parametr_products_set)
    await delete_user_carts(user_id=order.user_id)
    return {'res': 'ok'}
