from app.repositories.producto_repository import ProductoRepository
from app.repositories.kardex_repository import KardexRepository


class ProductoService:
    def __init__(self, producto_repo: ProductoRepository = None, kardex_repo: KardexRepository = None):
        self.producto_repo = producto_repo or ProductoRepository()
        self.kardex_repo = kardex_repo or KardexRepository()

    def get_all(self, activos_only: bool = True) -> list[dict]:
        return self.producto_repo.get_all(activos_only)

    def get_by_id(self, producto_id: int) -> dict | None:
        return self.producto_repo.get_by_id(producto_id)

    def create(self, data: dict) -> dict:
        codigo = data.get("codigo", "").strip()
        if not codigo:
            raise ValueError("El código del producto es obligatorio.")

        existentes = self.producto_repo.get_all(activos_only=False)
        if any(p["codigo"] == codigo for p in existentes):
            raise ValueError(f"Ya existe un producto con el código '{codigo}'.")

        precio_venta = data.get("precio_venta", 0)
        if precio_venta < 0:
            raise ValueError("El precio de venta no puede ser negativo.")

        precio_compra = data.get("precio_compra", 0)
        if precio_compra < 0:
            raise ValueError("El precio de compra no puede ser negativo.")

        producto_id = self.producto_repo.create(data)
        return {"success": True, "id": producto_id}

    def create_with_stock_inicial(self, data: dict, cantidad_inicial: int, precio_compra: float) -> dict:
        result = self.create(data)
        producto_id = result["id"]

        if cantidad_inicial > 0:
            self.kardex_repo.create({
                "producto_id": producto_id,
                "tipo": "ENTRADA",
                "cantidad": cantidad_inicial,
                "precio_unitario": precio_compra,
                "total": cantidad_inicial * precio_compra,
                "motivo": "Stock inicial",
                "documento_ref": "ALTA",
                "saldo_stock": cantidad_inicial,
            })
            self.producto_repo.update_stock(producto_id, cantidad_inicial)

        return result

    def search(self, query: str) -> list[dict]:
        query_lower = query.strip().lower()
        productos = self.get_all()
        if not query_lower:
            return productos
        return [
            p for p in productos
            if query_lower in str(p.get("codigo", "")).lower()
            or query_lower in str(p.get("nombre", "")).lower()
            or query_lower in str(p.get("categoria", "")).lower()
        ]