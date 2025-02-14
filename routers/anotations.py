from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class ClientBase(BaseModel):
    user_id: int
    org_name: str
    client_city: Optional[str]
    address: Optional[str]
    phone: str
    is_contract: bool = False


class ClientUpdateSerializer(ClientBase):
    pass


class ClientSerializer(ClientBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


# class ClientAddBase(BaseModel):
#     user_id: int
#     org_name: str
#     phone: str


class CategoryBase(BaseModel):

    photo: str
    name: str
    verbose_name: Optional[str]


class GoodBase(BaseModel):
        
    category_id: int
    city_id: int
    photo: Optional[str]
    name: str
    verbose_name: Optional[str]
    unit: str
    description: Optional[str]
    is_delivery: bool
    is_arenda: bool
    price: int
    delivery_price: Optional[int]
    arenda_contract: Optional[int]
    delivery_terms: Optional[str]
    arenda_terms: Optional[str]
    b_id: str


class CityBase(BaseModel):
    name: str
    verbose_name: Optional[str]


class CartBase(BaseModel):
    
    user_id: int
    good_id: int
    quantity: int
    arenda_time: Optional[int]
    is_arenda: bool
    is_delivery: bool = False
    is_contract: bool = False
    total_price: int


class OrderBase(BaseModel):
    user_id: int
    order_text: str


class CitySerializer(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CategorySerializer(CategoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class GoodSerializer(GoodBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city: CitySerializer

    # class Config:
    #     from_attributes = True

# class CartDelete(BaseModel):
#     user_id: int
#     good_id: int


class CartAddSerializer(CartBase):
    pass


class GoodForCarts(GoodBase):
    model_config = ConfigDict(from_attributes=True)

    city: CitySerializer


class CartSerializer(CartBase):
    model_config = ConfigDict(from_attributes=True)

    good: GoodForCarts

    id: int


class CartGetSerializer(BaseModel):
    goods: List[CartSerializer]
    arenda_goods: List[CartSerializer]


class OrderAddSerializer(OrderBase):
    pass


class OrderSerializer(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
