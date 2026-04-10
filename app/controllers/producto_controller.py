from services.producto_service import ProductoService


class ProductoController:
    def __init__(self, producto_service: ProductoService = None):
        self.service = producto_service or ProductoService()

    def get_all(self, activos_only: bool = True) -> list[dict]:
        return self.service.get_all(activos_only)

    def get_by_id(self, producto_id: int) -> dict | None:
        return self.service.get_by_id(producto_id)

    def create(self, data: dict) -> dict:
        return self.service.create(data)

    def create_with_stock_inicial(self, data: dict, cantidad_inicial: int = 0, precio_compra: float = 0) -> dict:
        return self.service.create_with_stock_inicial(data, cantidad_inicial, precio_compra)

    def search(self, query: str) -> list[dict]:
        return self.service.search(query)