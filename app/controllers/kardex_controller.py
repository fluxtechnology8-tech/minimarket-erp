from services.kardex_service import KardexService


class KardexController:
    def __init__(self, kardex_service: KardexService = None):
        self.service = kardex_service or KardexService()

    def get_all(self, producto_id: int = None, limit: int = 100) -> list[dict]:
        return self.service.get_all(producto_id, limit)

    def get_productos(self) -> list[dict]:
        return self.service.get_productos()

    def registrar_movimiento(self, producto_id: int, tipo: str, cantidad: int, precio_unitario: float = 0, motivo: str = "", documento_ref: str = "") -> dict:
        return self.service.registrar_movimiento(producto_id, tipo, cantidad, precio_unitario, motivo, documento_ref)