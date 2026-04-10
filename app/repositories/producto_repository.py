from core.database import get_session_manager
from models.producto import Producto


class ProductoRepository:
    def __init__(self, session_manager=None):
        self._sm = session_manager or get_session_manager()

    def get_all(self, activos_only: bool = True) -> list[dict]:
        with self._sm.get_session() as session:
            query = session.query(Producto)
            if activos_only:
                query = query.filter(Producto.activo == 1)
            productos = query.order_by(Producto.nombre).all()
            return [self._to_dict(p) for p in productos]

    def get_by_id(self, producto_id: int) -> dict | None:
        with self._sm.get_session() as session:
            producto = session.query(Producto).filter(Producto.id == producto_id).first()
            return self._to_dict(producto) if producto else None

    def create(self, data: dict) -> int:
        with self._sm.get_session() as session:
            producto = Producto(
                codigo=data["codigo"],
                nombre=data["nombre"],
                categoria=data.get("categoria", ""),
                precio_compra=data.get("precio_compra", 0),
                precio_venta=data.get("precio_venta", 0),
                stock=data.get("stock", 0),
                stock_minimo=data.get("stock_minimo", 5),
                unidad=data.get("unidad", "unidad"),
                descripcion=data.get("descripcion", ""),
            )
            session.add(producto)
            session.flush()
            return producto.id

    def update_stock(self, producto_id: int, nuevo_stock: int) -> bool:
        with self._sm.get_session() as session:
            producto = session.query(Producto).filter(Producto.id == producto_id).first()
            if producto:
                producto.stock = nuevo_stock
                return True
            return False

    def _to_dict(self, p: Producto) -> dict:
        return {
            "id": p.id,
            "codigo": p.codigo,
            "nombre": p.nombre,
            "categoria": p.categoria,
            "precio_compra": p.precio_compra,
            "precio_venta": p.precio_venta,
            "stock": p.stock,
            "stock_minimo": p.stock_minimo,
            "unidad": p.unidad,
            "descripcion": p.descripcion,
            "fecha_creacion": p.fecha_creacion,
            "activo": p.activo,
        }