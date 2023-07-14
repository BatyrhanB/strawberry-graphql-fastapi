from sqlalchemy.orm import Session

from src.product import models


async def get_products(db: Session, skip: int = 0, limit: int = 100):
    return await db.query(models.Product).offset(skip).limit(limit).all()