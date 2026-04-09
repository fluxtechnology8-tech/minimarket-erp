from app.models.product import Product

def create_product(name: str):
    product = Product(name=name)
    return product