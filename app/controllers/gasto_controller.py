from services.gasto_service import GastoService


class GastoController:
    def __init__(self, gasto_service: GastoService = None):
        self.service = gasto_service or GastoService()

    def get_all(self, limit: int = 100) -> list[dict]:
        return self.service.get_all(limit)

    def create(self, data: dict) -> dict:
        return self.service.create(data)