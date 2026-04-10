from app.repositories.kardex_repository import KardexRepository
from app.repositories.producto_repository import ProductoRepository


class KardexService:
    def __init__(self, kardex_repo: KardexRepository = None, producto_repo: ProductoRepository = None):
        self.kardex_repo = kardex_repo or KardexRepository()
        self.producto_repo = producto_repo or ProductoRepository()

    def get_all(self, producto_id: int = None, limit: int = 100) -> list[dict]:
        return self.kardex_repo.get_all(producto_id, limit)

    def get_productos(self) -> list[dict]:
        return self.producto_repo.get_all()

    def registrar_movimiento(
        self,
        producto_id: int,
        tipo: str,
        cantidad: int,
        precio_unitario: float = 0,
        motivo: str = "",
        documento_ref: str = ""
    ) -> dict:
        if tipo not in ("ENTRADA", "SALIDA"):
            raise ValueError("El tipo debe ser 'ENTRADA' o 'SALIDA'.")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser mayor a cero.")

        producto = self.producto_repo.get_by_id(producto_id)
        if not producto:
            raise ValueError("Producto no encontrado.")

        stock_actual = producto.get("stock", 0)

        if tipo == "SALIDA":
            if cantidad > stock_actual:
                raise ValueError(f"No hay stock suficiente. Stock actual: {stock_actual}")
            nuevo_stock = stock_actual - cantidad
        else:
            nuevo_stock = stock_actual + cantidad

        total = cantidad * precio_unitario

        self.kardex_repo.create({
            "producto_id": producto_id,
            "tipo": tipo,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
            "total": total,
            "motivo": motivo,
            "documento_ref": documento_ref,
            "saldo_stock": nuevo_stock,
        })

        self.producto_repo.update_stock(producto_id, nuevo_stock)

        return {"success": True, "nuevo_stock": nuevo_stock}