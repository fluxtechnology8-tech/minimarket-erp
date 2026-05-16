from services.venta_service import VentaService


class VentaController:
    def __init__(self, venta_service: VentaService = None):
        self.service = venta_service or VentaService()

    def get_all(self, limit: int = 50) -> list[dict]:
        return self.service.get_all(limit)

    def get_productos(self) -> list[dict]:
        return self.service.get_productos()

    def get_productos_con_stock(self) -> list[dict]:
        return self.service.get_productos_con_stock()

    def get_producto(self, producto_id: int) -> dict | None:
        return self.service.get_producto(producto_id)

    def generar_boleta(self, items: list[dict], cliente_nombre: str = "", cliente_documento: str = "") -> dict:
        return self.service.generar_boleta(items, cliente_nombre, cliente_documento)

    def get_by_numero_boleta(self, numero_boleta: str) -> dict | None:
        return self.service.get_by_numero_boleta(numero_boleta)

    def get_by_cliente_documento(self, cliente_documento: str) -> list[dict]:
        return self.service.get_by_cliente_documento(cliente_documento)