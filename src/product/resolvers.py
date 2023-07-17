from sqlalchemy import delete, select, update
from sqlalchemy.orm import load_only

from src.product.helper import get_only_selected_fields, get_valid_data
from src.product import models
from src.settings.database import get_async_session
from src.product.scalar import Product, ProductDeleted, ProductNotFound, CategoryFound


async def get_products(info):
    selected_fields = get_only_selected_fields(models.Product, info)
    async with get_async_session() as s:
        sql = (
            select(models.Product)
            .options(load_only(*selected_fields))
            .order_by(models.Product.id)
        )
        db_products = (await s.execute(sql)).scalars().unique().all()

    product_data_list = []
    for product_note in db_products:
        product_dict = get_valid_data(product_note, models.Product)
        product_data_list.append(Product(**product_dict))

    return product_data_list


async def get_product(product_id, info):
    selected_fields = get_only_selected_fields(models.Product, info)
    async with get_async_session() as s:
        sql = (
            select(models.Product)
            .options(load_only(*selected_fields))
            .filter(models.Product.id == product_id)
            .order_by(models.Product.id)
        )
        db_product = (await s.execute(sql)).scalars().unique().one()

    product_dict = get_valid_data(db_product, models.Product)
    return Product(**product_dict)


async def add_stickynotes(title, category_id):
    async with get_async_session() as s:
        db_category = None
        sql = select(models.Category).where(models.Category.id == category_id)
        db_category = (await s.execute(sql)).scalars().first()
        if not db_category:
            return CategoryFound()

        db_products = models.Product(title=title, category_id=db_category.id)
        s.add(db_products)
        await s.commit()

    db_products_serialize_data = db_products.as_dict()
    return Product(**db_products_serialize_data)


async def delete_stickynotes(product_id):
    """Delete stickynotes resolver"""
    async with get_async_session() as s:
        sql = select(models.Product).where(models.Product.id == product_id)
        existing_db_product = (await s.execute(sql)).first()
        if existing_db_product is None:
            return ProductNotFound()

        query = delete(models.Product).where(models.Product.id == product_id)
        await s.execute(query)
        await s.commit()

    return ProductDeleted()