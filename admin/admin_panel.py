from sqladmin import ModelView
from data_base.models import Good, Category, City, User, Client, Cart, Order


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.user_id, User.full_name]
    column_details_list = '__all__'
    can_create = False
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True


class ClientAdmin(ModelView, model=Client):
    column_list = [Client.id, Client.org_name, Client.phone, Client.address,
                   Client.user]
    column_details_list = '__all__'
    can_create = False
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True


class CategoryAdmin(ModelView, model=Category):
    column_list = [Category.name]
    column_details_list = '__all__'
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True

    form_create_rules = ['name', 'verbose_name', 'photo']


class CityAdmin(ModelView, model=City):
    column_list = [Category.name]
    column_details_list = '__all__'
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True

    form_create_rules = ['name', 'verbose_name']


class GoodAdmin(ModelView, model=Good):
    column_list = [Good.id, Good.b_id, Good.category, Good.name, Good.price, 
                   Good.delivery_price, Good.city]
    column_details_list = '__all__'
    column_type_formatters = dict(ModelView.column_type_formatters)
    column_labels = {Good.name: 'Название'}
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True
    form_create_rules = ['name', 'category', 'city', 'photo', 'verbose_name', 'unit', 
                         'description', 'is_arenda', 'is_delivery', 'price',  'delivery_price',
                         'arenda_contract', 'delivery_terms', 'arenda_terms', 'b_id']


class CartAdmin(ModelView, model=Cart):
    column_list = [Cart.user_id, Cart.user, Cart.good, Cart.arenda_time, 
                   Cart.is_delivery, Cart.total_price]
    column_details_list = '__all__'
    can_create = False
    can_edit = False
    can_delete = True
    can_view_details = True
    can_export = True


class OrderAdmin(ModelView, model=Order):
    column_list = [Order.id, Order.user_id]
    column_details_list = '__all__'
    can_create = False
    can_edit = True
    can_delete = True
    can_view_details = True
    can_export = True
