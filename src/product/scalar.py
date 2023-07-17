import strawberry
from pydantic import Field, typing


@strawberry.type
class Product:
    id: int
    title: typing.Optional[str] = ""
    description : typing.Optional[str] = ""
    category_id: typing.Optional[int] = Field(description="Category id")


@strawberry.type
class ProductNotFound:
    message: str = "Couldn't find product with the supplied id"


@strawberry.type
class ProductDeleted:
    message: str = "Product deleted"


@strawberry.type
class CategoryFound:
    message: str = "Couldn't find category with the supplied id"
