from core.database import Base

from sqlalchemy import Column, Integer, String, DateTime

from datetime import datetime


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    rol = Column(String, nullable=False)  # "admin" o "empleado"
    activo = Column(Integer, default=1)
    fecha_creacion = Column(DateTime, default=datetime.now)
