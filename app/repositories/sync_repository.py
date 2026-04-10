import json
import sqlite3
from pathlib import Path

from app.core.database import get_session_manager
from app.models.producto import Producto
from app.models.kardex import Kardex
from app.models.gasto import Gasto
from app.models.venta import Venta
from app.models.venta_detalle import VentaDetalle


class SyncRepository:
    def __init__(self, session_manager=None):
        self._sm = session_manager or get_session_manager()

    def export_all(self) -> dict:
        with self._sm.get_session() as session:
            return {
                "productos": [self._producto_to_dict(p) for p in session.query(Producto).all()],
                "kardex": [self._kardex_to_dict(k) for k in session.query(Kardex).all()],
                "gastos": [self._gasto_to_dict(g) for g in session.query(Gasto).all()],
                "ventas": [self._venta_to_dict(v) for v in session.query(Venta).all()],
                "venta_detalles": [self._detalle_to_dict(d) for d in session.query(VentaDetalle).all()],
            }

    def import_all(self, data: dict, merge: bool = True) -> None:
        with self._sm.get_session() as session:
            if not merge:
                session.query(VentaDetalle).delete()
                session.query(Venta).delete()
                session.query(Kardex).delete()
                session.query(Gasto).delete()
                session.query(Producto).delete()

            for prod_data in data.get("productos", []):
                prod_data.pop("id", None)
                existing = session.query(Producto).filter(Producto.codigo == prod_data.get("codigo")).first()
                if not existing:
                    producto = Producto(**prod_data)
                    session.add(producto)

    def get_export_bytes(self) -> bytes:
        conn = sqlite3.connect("data/database.db")
        conn.row_factory = sqlite3.Row
        data = {}
        for table in ["productos", "kardex", "gastos", "ventas", "venta_detalles"]:
            rows = conn.execute(f"SELECT * FROM {table}").fetchall()
            data[table] = [dict(row) for row in rows]
        conn.close()
        return json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")

    def _producto_to_dict(self, p: Producto) -> dict:
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
            "fecha_creacion": p.fecha_creacion.isoformat() if p.fecha_creacion else None,
            "activo": p.activo,
        }

    def _kardex_to_dict(self, k: Kardex) -> dict:
        return {
            "id": k.id,
            "producto_id": k.producto_id,
            "tipo": k.tipo,
            "cantidad": k.cantidad,
            "precio_unitario": k.precio_unitario,
            "total": k.total,
            "motivo": k.motivo,
            "documento_ref": k.documento_ref,
            "fecha": k.fecha.isoformat() if k.fecha else None,
            "saldo_stock": k.saldo_stock,
        }

    def _gasto_to_dict(self, g: Gasto) -> dict:
        return {
            "id": g.id,
            "concepto": g.concepto,
            "monto": g.monto,
            "categoria": g.categoria,
            "fecha": g.fecha.isoformat() if g.fecha else None,
            "observaciones": g.observaciones,
        }

    def _venta_to_dict(self, v: Venta) -> dict:
        return {
            "id": v.id,
            "numero_boleta": v.numero_boleta,
            "cliente_nombre": v.cliente_nombre,
            "cliente_documento": v.cliente_documento,
            "total": v.total,
            "fecha": v.fecha.isoformat() if v.fecha else None,
            "estado": v.estado,
        }

    def _detalle_to_dict(self, d: VentaDetalle) -> dict:
        return {
            "id": d.id,
            "venta_id": d.venta_id,
            "producto_id": d.producto_id,
            "cantidad": d.cantidad,
            "precio_unitario": d.precio_unitario,
            "subtotal": d.subtotal,
        }