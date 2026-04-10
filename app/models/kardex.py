from core.database import Base

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from datetime import datetime

class Kardex(Base):
    __tablename__ = "kardex"

    id = Column(Integer, primary_key=True, autoincrement=True)
    producto_id = Column(Integer, ForeignKey("productos.id"))
    tipo = Column(String, nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float)
    total = Column(Float)
    motivo = Column(String)
    documento_ref = Column(String)
    fecha = Column(DateTime, default=datetime.now)
    saldo_stock = Column(Integer)

    producto = relationship("Producto", back_populates="kardex")