import json
import sqlite3
from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
)
from sqlalchemy.orm import Session, relationship, declarative_base, sessionmaker

Base = declarative_base()


class Producto(Base):
    __tablename__ = "productos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    codigo = Column(String, unique=True, nullable=False)
    nombre = Column(String, nullable=False)
    categoria = Column(String)
    precio_compra = Column(Float, default=0)
    precio_venta = Column(Float, default=0)
    stock = Column(Integer, default=0)
    stock_minimo = Column(Integer, default=5)
    unidad = Column(String, default="unidad")
    descripcion = Column(String)
    fecha_creacion = Column(DateTime, default=datetime.now)
    activo = Column(Integer, default=1)

    kardex = relationship("Kardex", back_populates="producto")
    venta_detalles = relationship("VentaDetalle", back_populates="producto")


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


class Gasto(Base):
    __tablename__ = "gastos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    concepto = Column(String, nullable=False)
    monto = Column(Float, nullable=False)
    categoria = Column(String)
    fecha = Column(DateTime, default=datetime.now)
    observaciones = Column(String)


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


class VentaDetalle(Base):
    __tablename__ = "venta_detalles"

    id = Column(Integer, primary_key=True, autoincrement=True)
    venta_id = Column(Integer, ForeignKey("ventas.id"))
    producto_id = Column(Integer, ForeignKey("productos.id"))
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    venta = relationship("Venta", back_populates="detalles")
    producto = relationship("Producto", back_populates="venta_detalles")


class Database:
    def __init__(self, db_path: str = "data/database.db"):
        self.db_path = db_path
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self.engine = create_engine(f"sqlite:///{db_path}", echo=False)
        Base.metadata.create_all(bind=self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def get_productos(self, activos_only: bool = True) -> list[dict]:
        with self.SessionLocal() as session:
            query = session.query(Producto)
            if activos_only:
                query = query.filter(Producto.activo == 1)
            productos = query.order_by(Producto.nombre).all()
            return [self._producto_to_dict(p) for p in productos]

    def get_producto(self, producto_id: int) -> dict | None:
        with self.SessionLocal() as session:
            producto = (
                session.query(Producto).filter(Producto.id == producto_id).first()
            )
            return self._producto_to_dict(producto) if producto else None

    def add_producto(self, data: dict) -> int:
        with self.SessionLocal() as session:
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
            session.commit()
            return producto.id

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
            "fecha_creacion": p.fecha_creacion,
            "activo": p.activo,
        }

    def registrar_movimiento(
        self,
        producto_id: int,
        tipo: str,
        cantidad: int,
        precio_unitario: float = 0,
        motivo: str = "",
        documento_ref: str = "",
    ) -> int:
        with self.SessionLocal() as session:
            producto = (
                session.query(Producto)
                .filter(Producto.id == producto_id, Producto.activo == 1)
                .first()
            )
            if not producto:
                raise ValueError("Producto no encontrado.")

            stock_actual = producto.stock or 0
            if tipo == "ENTRADA":
                nuevo_stock = stock_actual + cantidad
            else:
                nuevo_stock = stock_actual - cantidad
                if nuevo_stock < 0:
                    raise ValueError(
                        "No hay stock suficiente para registrar la salida."
                    )

            total = cantidad * (precio_unitario or 0)
            producto.stock = nuevo_stock

            movimiento = Kardex(
                producto_id=producto_id,
                tipo=tipo,
                cantidad=cantidad,
                precio_unitario=precio_unitario,
                total=total,
                motivo=motivo,
                documento_ref=documento_ref,
                saldo_stock=nuevo_stock,
            )
            session.add(movimiento)
            session.commit()
            return nuevo_stock

    def get_kardex(
        self, producto_id: int | None = None, limit: int = 100
    ) -> list[dict]:
        with self.SessionLocal() as session:
            query = session.query(Kardex).join(Producto)
            if producto_id:
                query = query.filter(Kardex.producto_id == producto_id)
            movimientos = (
                query.order_by(Kardex.fecha.desc(), Kardex.id.desc()).limit(limit).all()
            )
            return [
                {
                    "id": m.id,
                    "producto_id": m.producto_id,
                    "tipo": m.tipo,
                    "cantidad": m.cantidad,
                    "precio_unitario": m.precio_unitario,
                    "total": m.total,
                    "motivo": m.motivo,
                    "documento_ref": m.documento_ref,
                    "fecha": m.fecha,
                    "saldo_stock": m.saldo_stock,
                    "codigo": m.producto.codigo if m.producto else None,
                    "producto_nombre": m.producto.nombre if m.producto else None,
                }
                for m in movimientos
            ]

    def add_gasto(self, data: dict) -> int:
        with self.SessionLocal() as session:
            gasto = Gasto(
                concepto=data["concepto"],
                monto=data["monto"],
                categoria=data.get("categoria", ""),
                observaciones=data.get("observaciones", ""),
            )
            session.add(gasto)
            session.commit()
            return gasto.id

    def get_gastos(self, limit: int = 100) -> list[dict]:
        with self.SessionLocal() as session:
            gastos = (
                session.query(Gasto)
                .order_by(Gasto.fecha.desc(), Gasto.id.desc())
                .limit(limit)
                .all()
            )
            return [
                {
                    "id": g.id,
                    "concepto": g.concepto,
                    "monto": g.monto,
                    "categoria": g.categoria,
                    "fecha": g.fecha,
                    "observaciones": g.observaciones,
                }
                for g in gastos
            ]

    def generar_boleta(
        self, items: list[dict], cliente_nombre: str = "", cliente_documento: str = ""
    ) -> str:
        if not items:
            raise ValueError("Debe agregar al menos un producto.")

        with self.SessionLocal() as session:
            total = sum(item["cantidad"] * item["precio_unitario"] for item in items)
            secuencia = session.query(Venta).count() + 1
            fecha_actual = datetime.now()
            numero = f"BOL-{fecha_actual.strftime('%Y%m%d')}-{int(secuencia):04d}"

            venta = Venta(
                numero_boleta=numero,
                cliente_nombre=cliente_nombre,
                cliente_documento=cliente_documento,
                total=total,
            )
            session.add(venta)
            session.flush()

            for item in items:
                producto = (
                    session.query(Producto)
                    .filter(Producto.id == item["producto_id"], Producto.activo == 1)
                    .first()
                )
                if not producto:
                    session.rollback()
                    raise ValueError("Uno de los productos ya no existe.")
                if (producto.stock or 0) < item["cantidad"]:
                    session.rollback()
                    raise ValueError("Stock insuficiente para completar la venta.")

                subtotal = item["cantidad"] * item["precio_unitario"]
                detalle = VentaDetalle(
                    venta_id=venta.id,
                    producto_id=item["producto_id"],
                    cantidad=item["cantidad"],
                    precio_unitario=item["precio_unitario"],
                    subtotal=subtotal,
                )
                session.add(detalle)

                nuevo_stock = producto.stock - item["cantidad"]
                producto.stock = nuevo_stock

                movimiento = Kardex(
                    producto_id=item["producto_id"],
                    tipo="SALIDA",
                    cantidad=item["cantidad"],
                    precio_unitario=item["precio_unitario"],
                    total=subtotal,
                    motivo="Venta",
                    documento_ref=numero,
                    saldo_stock=nuevo_stock,
                )
                session.add(movimiento)

            session.commit()
            return numero

    def get_ventas(self, limit: int = 50) -> list[dict]:
        with self.SessionLocal() as session:
            ventas = (
                session.query(Venta)
                .order_by(Venta.fecha.desc(), Venta.id.desc())
                .limit(limit)
                .all()
            )
            return [
                {
                    "id": v.id,
                    "numero_boleta": v.numero_boleta,
                    "cliente_nombre": v.cliente_nombre,
                    "cliente_documento": v.cliente_documento,
                    "total": v.total,
                    "fecha": v.fecha,
                    "estado": v.estado,
                    "cantidad_items": len(v.detalles),
                }
                for v in ventas
            ]

    def get_dashboard_metrics(self) -> dict:
        with self.SessionLocal() as session:
            total_productos = (
                session.query(Producto).filter(Producto.activo == 1).count()
            )
            stock_bajo = (
                session.query(Producto)
                .filter(Producto.activo == 1, Producto.stock <= Producto.stock_minimo)
                .count()
            )
            ventas_hoy = (
                session.query(Venta)
                .filter(
                    Venta.fecha
                    >= datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
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

            return {
                "total_productos": total_productos,
                "stock_bajo": stock_bajo,
                "ventas_hoy": float(ventas_hoy_total),
                "gastos_mes": float(gastos_mes_total),
                "low_stock": [self._producto_to_dict(p) for p in low_stock],
                "daily_sales": daily_sales,
            }

    def get_report_metrics(self) -> dict:
        with self.SessionLocal() as session:
            productos = session.query(Producto).filter(Producto.activo == 1).all()
            total_stock = sum(p.stock or 0 for p in productos)
            valor_inventario = sum(
                (p.stock or 0) * (p.precio_compra or 0) for p in productos
            )

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
                session.query(
                    Producto.nombre,
                    VentaDetalle.cantidad,
                    VentaDetalle.subtotal,
                )
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

    def export_data(self, output_path: str | Path) -> Path:
        with self.SessionLocal() as session:
            data = {
                "productos": [
                    self._producto_to_dict(p) for p in session.query(Producto).all()
                ],
                "kardex": [
                    {
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
                    for k in session.query(Kardex).all()
                ],
                "gastos": [
                    {
                        "id": g.id,
                        "concepto": g.concepto,
                        "monto": g.monto,
                        "categoria": g.categoria,
                        "fecha": g.fecha.isoformat() if g.fecha else None,
                        "observaciones": g.observaciones,
                    }
                    for g in session.query(Gasto).all()
                ],
                "ventas": [
                    {
                        "id": v.id,
                        "numero_boleta": v.numero_boleta,
                        "cliente_nombre": v.cliente_nombre,
                        "cliente_documento": v.cliente_documento,
                        "total": v.total,
                        "fecha": v.fecha.isoformat() if v.fecha else None,
                        "estado": v.estado,
                    }
                    for v in session.query(Venta).all()
                ],
                "venta_detalles": [
                    {
                        "id": d.id,
                        "venta_id": d.venta_id,
                        "producto_id": d.producto_id,
                        "cantidad": d.cantidad,
                        "precio_unitario": d.precio_unitario,
                        "subtotal": d.subtotal,
                    }
                    for d in session.query(VentaDetalle).all()
                ],
            }

        path = Path(output_path)
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return path

    def get_export_bytes(self) -> bytes:
        conn = self.get_connection()
        data = {}
        for table in ["productos", "kardex", "gastos", "ventas", "venta_detalles"]:
            rows = conn.execute(f"SELECT * FROM {table}").fetchall()
            data[table] = [dict(row) for row in rows]
        conn.close()
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        return json_str.encode("utf-8")

    def import_data(self, input_path: str | Path, merge: bool = True) -> None:
        path = Path(input_path)
        data = json.loads(path.read_text(encoding="utf-8"))
        with self.SessionLocal() as session:
            if not merge:
                session.query(VentaDetalle).delete()
                session.query(Venta).delete()
                session.query(Kardex).delete()
                session.query(Gasto).delete()
                session.query(Producto).delete()

            for prod_data in data.get("productos", []):
                prod_data.pop("id", None)
                existing = (
                    session.query(Producto)
                    .filter(Producto.codigo == prod_data.get("codigo"))
                    .first()
                )
                if not existing:
                    producto = Producto(**prod_data)
                    session.add(producto)

            session.commit()
