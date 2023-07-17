import strawberry
from strawberry.types import Info
from pydantic import typing

from src.product.scalar import Product
from src.product.resolvers import get_products, get_product


@strawberry.type
class Query:

    @strawberry.field
    async def products(self, info:Info) -> typing.List[Product]:
        products_data_list = await get_products(info)
        return products_data_list

    @strawberry.field
    async def product(self, info:Info, product_id: int) -> Product:
        product_dict = await get_product(product_id, info)
        return product_dict