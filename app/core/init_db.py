from core.database import Base, engine

from models.producto import Producto
from models.gasto import Gasto
from models.kardex import Kardex
from models.venta_detalle import VentaDetalle
from models.venta import Venta
from models.usuario import Usuario


def init_db():
    Base.metadata.create_all(bind=engine)

    from core.database import SessionLocal

    session = SessionLocal()
    try:
        existing_users = session.query(Usuario).count()
        if existing_users == 0:
            admin = Usuario(
                username="admin",
                password="admin123",
                nombre="Administrador",
                rol="admin",
            )
            empleado = Usuario(
                username="empleado",
                password="emp123",
                nombre="Empleado",
                rol="empleado",
            )
            session.add(admin)
            session.add(empleado)
            session.commit()
            print("Usuarios por defecto creados: admin, empleado")
    except Exception as e:
        session.rollback()
        print(f"Error al crear usuarios: {e}")
    finally:
        session.close()

    print("Base de datos inicializada y tablas creadas.")
