from core.database import Base

from sqlalchemy import Column, Integer, String, Float, DateTime

from datetime import datetime

class Gasto(Base):
    __tablename__ = "gastos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    concepto = Column(String, nullable=False)
    monto = Column(Float, nullable=False)
    categoria = Column(String)
    fecha = Column(DateTime, default=datetime.now)
    observaciones = Column(String)