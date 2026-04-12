from core.database import Base

from sqlalchemy import Column, Integer, String, Float, DateTime, LargeBinary
from sqlalchemy.orm import relationship

from datetime import datetime


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    categoria = Column(String)
    precio_compra = Column(Float, default=0)
    precio_venta = Column(Float, default=0)
    stock = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=5)
    unidad = Column(String, default="unidad")
    descripcion = Column(String)
    imagen = Column(String)  # Guardar como base64
    fecha_creacion = Column(DateTime, default=datetime.now)
    activo = Column(Integer, default=1)

    kardex = relationship("Kardex", back_populates="producto")
    venta_detalles = relationship("VentaDetalle", back_populates="producto")
