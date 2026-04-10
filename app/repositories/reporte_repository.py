from datetime import datetime, timedelta

from core.database import get_session_manager
from models.producto import Producto
from models.venta import Venta
from models.venta_detalle import VentaDetalle
from models.gasto import Gasto


class ReporteRepository:
    def __init__(self, session_manager=None):
        self._sm = session_manager or get_session_manager()

    def get_dashboard_metrics(self) -> dict:
        with self._sm.get_session() as session:
            total_productos = session.query(Producto).filter(Producto.activo == 1).count()
            stock_bajo = (
                session.query(Producto)
                .filter(Producto.activo == 1, Producto.stock <= Producto.stock_minimo)
                .count()
            )
            ventas_hoy = (
                session.query(Venta)
                .filter(
                    Venta.fecha >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                )
                .all()
            )
            ventas_hoy_total = sum(v.total for v in ventas_hoy)

            gastos_mes = session.query(Gasto).all()
            hoy = datetime.now()
            gastos_mes_total = sum(
                g.monto
                for g in gastos_mes
                if g.fecha and g.fecha.year == hoy.year and g.fecha.month == hoy.month
            )

            low_stock = (
                session.query(Producto)
                .filter(Producto.activo == 1, Producto.stock <= Producto.stock_minimo)
                .order_by(Producto.stock.asc(), Producto.nombre.asc())
                .limit(6)
                .all()
            )

            daily_sales = []
            today = datetime.now().date()
            for offset in range(6, -1, -1):
                day = today - timedelta(days=offset)
                day_start = datetime.combine(day, datetime.min.time())
                day_end = datetime.combine(day, datetime.max.time())
                ventas_del_dia = (
                    session.query(Venta)
                    .filter(Venta.fecha >= day_start, Venta.fecha <= day_end)
                    .all()
                )
                total = sum(v.total for v in ventas_del_dia)
                daily_sales.append({"date": day, "total": float(total)})

            from repositories.producto_repository import ProductoRepository
            producto_repo = ProductoRepository(self._sm)

            return {
                "total_productos": total_productos,
                "stock_bajo": stock_bajo,
                "ventas_hoy": float(ventas_hoy_total),
                "gastos_mes": float(gastos_mes_total),
                "low_stock": [producto_repo._to_dict(p) for p in low_stock],
                "daily_sales": daily_sales,
            }

    def get_report_metrics(self) -> dict:
        with self._sm.get_session() as session:
            productos = session.query(Producto).filter(Producto.activo == 1).all()
            total_stock = sum(p.stock or 0 for p in productos)
            valor_inventario = sum((p.stock or 0) * (p.precio_compra or 0) for p in productos)

            hoy = datetime.now()
            ventas_mes = (
                session.query(Venta)
                .filter(Venta.fecha >= datetime(hoy.year, hoy.month, 1))
                .all()
            )
            ventas_mes_total = sum(v.total for v in ventas_mes)

            gastos_mes = session.query(Gasto).all()
            gastos_mes_total = sum(
                g.monto
                for g in gastos_mes
                if g.fecha and g.fecha.year == hoy.year and g.fecha.month == hoy.month
            )

            top_productos_data = (
                session.query(Producto.nombre, VentaDetalle.cantidad, VentaDetalle.subtotal)
                .join(VentaDetalle)
                .group_by(Producto.id)
                .order_by(VentaDetalle.cantidad.desc())
                .limit(5)
                .all()
            )

            return {
                "total_stock": total_stock,
                "valor_inventario": float(valor_inventario),
                "ventas_mes": float(ventas_mes_total),
                "gastos_mes": float(gastos_mes_total),
                "utilidad_estimada": float(ventas_mes_total) - float(gastos_mes_total),
                "top_productos": [
                    {
                        "nombre": p.nombre,
                        "cantidad_vendida": p.cantidad,
                        "total_vendido": p.subtotal,
                    }
                    for p in top_productos_data
                ],
            }