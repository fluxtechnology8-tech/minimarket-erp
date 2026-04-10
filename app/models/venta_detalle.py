from app.core.database import Base

from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

class VentaDetalle(Base):
    __tablename__ = "venta_detalles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="venta_detalles")