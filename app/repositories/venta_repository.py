from core.database import get_session_manager
from models.venta import Venta
from models.venta_detalle import VentaDetalle


class VentaRepository:
    def __init__(self, session_manager=None):
        self._sm = session_manager or get_session_manager()

    def get_all(self, limit: int = 50) -> list[dict]:
        with self._sm.get_session() as session:
            ventas = session.query(Venta).order_by(Venta.fecha.desc(), Venta.id.desc()).limit(limit).all()
            return [self._to_dict(v) for v in ventas]

    def get_by_id(self, venta_id: int) -> dict | None:
        with self._sm.get_session() as session:
            venta = session.query(Venta).filter(Venta.id == venta_id).first()
            return self._to_dict(venta) if venta else None

    def create(self, data: dict) -> int:
        with self._sm.get_session() as session:
            venta = Venta(
                numero_boleta=data["numero_boleta"],
                cliente_nombre=data.get("cliente_nombre", ""),
                cliente_documento=data.get("cliente_documento", ""),
                total=data["total"],
            )
            session.add(venta)
            session.flush()
            return venta.id

    def create_detalle(self, data: dict) -> int:
        with self._sm.get_session() as session:
            detalle = VentaDetalle(
                venta_id=data["venta_id"],
                producto_id=data["producto_id"],
                cantidad=data["cantidad"],
                precio_unitario=data["precio_unitario"],
                subtotal=data["subtotal"],
            )
            session.add(detalle)
            session.flush()
            return detalle.id

    def get_secuencia(self) -> int:
        with self._sm.get_session() as session:
            count = session.query(Venta).count()
            return count + 1

    def _to_dict(self, v: Venta) -> dict:
        return {
            "id": v.id,
            "numero_boleta": v.numero_boleta,
            "cliente_nombre": v.cliente_nombre,
            "cliente_documento": v.cliente_documento,
            "total": v.total,
            "fecha": v.fecha,
            "estado": v.estado,
            "cantidad_items": len(v.detalles) if v.detalles else 0,
        }