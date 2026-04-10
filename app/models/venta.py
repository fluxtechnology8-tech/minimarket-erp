from core.database import Base

from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship

from datetime import datetime

class Venta(Base):
    __tablename__ = "ventas"

    id = Column(Integer, primary_key=True, autoincrement=True)
    numero_boleta = Column(String, unique=True, nullable=False)
    cliente_nombre = Column(String)
    cliente_documento = Column(String)
    total = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.now)
    estado = Column(String, default="COMPLETADA")

    detalles = relationship("VentaDetalle", back_populates="venta")