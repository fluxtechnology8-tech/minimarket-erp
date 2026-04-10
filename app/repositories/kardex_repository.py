from datetime import datetime
from core.database import get_session_manager
from models.kardex import Kardex
from models.producto import Producto


class KardexRepository:
    def __init__(self, session_manager=None):
        self._sm = session_manager or get_session_manager()

    def get_all(self, producto_id: int = None, limit: int = 100) -> list[dict]:
        with self._sm.get_session() as session:
            query = session.query(Kardex).join(Producto)
            if producto_id:
                query = query.filter(Kardex.producto_id == producto_id)
            movimientos = query.order_by(Kardex.fecha.desc(), Kardex.id.desc()).limit(limit).all()
            return [self._to_dict(m) for m in movimientos]

    def create(self, data: dict) -> int:
        with self._sm.get_session() as session:
            movimiento = Kardex(
                producto_id=data["producto_id"],
                tipo=data["tipo"],
                cantidad=data["cantidad"],
                precio_unitario=data.get("precio_unitario", 0),
                total=data.get("total", 0),
                motivo=data.get("motivo", ""),
                documento_ref=data.get("documento_ref", ""),
                saldo_stock=data.get("saldo_stock", 0),
            )
            session.add(movimiento)
            session.flush()
            return movimiento.id

    def _parse_fecha(self, fecha):
        if fecha is None:
            return None
        if isinstance(fecha, datetime):
            return fecha
        if isinstance(fecha, str):
            for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
                try:
                    return datetime.strptime(fecha, fmt)
                except ValueError:
                    continue
        return fecha

    def _to_dict(self, m: Kardex) -> dict:
        return {
            "id": m.id,
            "producto_id": m.producto_id,
            "tipo": m.tipo,
            "cantidad": m.cantidad,
            "precio_unitario": m.precio_unitario,
            "total": m.total,
            "motivo": m.motivo,
            "documento_ref": m.documento_ref,
            "fecha": self._parse_fecha(m.fecha),
            "saldo_stock": m.saldo_stock,
            "codigo": m.producto.codigo if m.producto else None,
            "producto_nombre": m.producto.nombre if m.producto else None,
        }