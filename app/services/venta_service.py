from datetime import datetime
from app.repositories.venta_repository import VentaRepository
from app.repositories.producto_repository import ProductoRepository
from app.repositories.kardex_repository import KardexRepository


class VentaService:
    def __init__(
        self,
        venta_repo: VentaRepository = None,
        producto_repo: ProductoRepository = None,
        kardex_repo: KardexRepository = None
    ):
        self.venta_repo = venta_repo or VentaRepository()
        self.producto_repo = producto_repo or ProductoRepository()
        self.kardex_repo = kardex_repo or KardexRepository()

    def get_all(self, limit: int = 50) -> list[dict]:
        return self.venta_repo.get_all(limit)

    def get_productos(self) -> list[dict]:
        return self.producto_repo.get_all()

    def get_productos_con_stock(self) -> list[dict]:
        productos = self.producto_repo.get_all()
        return [p for p in productos if p.get("stock", 0) > 0]

    def get_producto(self, producto_id: int) -> dict | None:
        return self.producto_repo.get_by_id(producto_id)

    def generar_boleta(
        self,
        items: list[dict],
        cliente_nombre: str = "",
        cliente_documento: str = ""
    ) -> dict:
        if not items:
            raise ValueError("Debe agregar al menos un producto.")

        for item in items:
            producto = self.producto_repo.get_by_id(item["producto_id"])
            if not producto:
                raise ValueError(f"Producto con ID {item['producto_id']} no encontrado.")

            stock = producto.get("stock", 0)
            if item["cantidad"] > stock:
                raise ValueError(f"Stock insuficiente para '{producto['nombre']}'. Stock: {stock}")

        total = sum(item["cantidad"] * item["precio_unitario"] for item in items)

        secuencia = self.venta_repo.get_secuencia()
        fecha_actual = datetime.now()
        numero = f"BOL-{fecha_actual.strftime('%Y%m%d')}-{int(secuencia):04d}"

        venta_id = self.venta_repo.create({
            "numero_boleta": numero,
            "cliente_nombre": cliente_nombre,
            "cliente_documento": cliente_documento,
            "total": total,
        })

        for item in items:
            subtotal = item["cantidad"] * item["precio_unitario"]

            self.venta_repo.create_detalle({
                "venta_id": venta_id,
                "producto_id": item["producto_id"],
                "cantidad": item["cantidad"],
                "precio_unitario": item["precio_unitario"],
                "subtotal": subtotal,
            })

            producto = self.producto_repo.get_by_id(item["producto_id"])
            nuevo_stock = producto["stock"] - item["cantidad"]
            self.producto_repo.update_stock(item["producto_id"], nuevo_stock)

            self.kardex_repo.create({
                "producto_id": item["producto_id"],
                "tipo": "SALIDA",
                "cantidad": item["cantidad"],
                "precio_unitario": item["precio_unitario"],
                "total": subtotal,
                "motivo": "Venta",
                "documento_ref": numero,
                "saldo_stock": nuevo_stock,
            })

        return {"success": True, "numero_boleta": numero}