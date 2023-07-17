import strawberry


@strawberry.type
class ProductBase():
    title: str
    description: str | None = None


@strawberry.type
class ProductCreate(ProductBase):
    pass


@strawberry.type
class Product(ProductBase):
    id: int
    category_id: int


@strawberry.type
class CategoryBase():
    title: str
    description: str | None = None 


@strawberry.type
class CategoryCreate(CategoryBase):
    pass  


@strawberry.type
class Category(CategoryBase):
    id: int
    products : list[Product] = []