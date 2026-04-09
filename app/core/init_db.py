from app.core.database import engine, Base

from app.models.product import Product

def init_db():
    Base.metadata.create_all(bind=engine)