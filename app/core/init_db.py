from core.database import Base, engine

from models.producto import Producto
from models.gasto import Gasto
from models.kardex import Kardex
from models.venta_detalle import VentaDetalle
from models.venta import Venta


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada y tablas creadas.")