from app.models.producto import Product
from app.helpers.get_db import get_db
from app.schemas.product_schema import ProductCreateSchema
import random

# Funcion temporal
def generate_barcode():
    return str(random.randint(100000000000, 999999999999))  # 12 dígitos

def create_product(name, price, stock):
    data = ProductCreateSchema(name, price, stock)
    barcode = generate_barcode()
    
    with get_db() as db:
        product = Product(
            name=data.name,
            price=data.price,
            stock=data.stock,
            barcode=barcode
        )

        db.add(product)
        db.commit()
        db.refresh(product)

        return product