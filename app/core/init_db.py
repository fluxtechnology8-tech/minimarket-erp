from app.core.database import Base, engine

from app.models.producto import Producto
from app.models.gasto import Gasto
from app.models.kardex import Kardex
from app.models.venta_detalle import VentaDetalle
from app.models.venta import Venta


def init_db():
    Base.metadata.create_all(bind=engine)
    print("Base de datos inicializada y tablas creadas.")