from pydantic import BaseModel


class ProductBase(BaseModel):
    title: str
    description: str | None = None


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    category_id: int

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    title: str
    description: str | None = None 


class CategoryCreate(CategoryBase):
    pass  


class Category(CategoryBase):
    id: int
    products : list[Product] = []

    class Config:
        orm_mode = True
