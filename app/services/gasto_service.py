from repositories.gasto_repository import GastoRepository


class GastoService:
    def __init__(self, gasto_repo: GastoRepository = None):
        self.gasto_repo = gasto_repo or GastoRepository()

    def get_all(self, limit: int = 100) -> list[dict]:
        return self.gasto_repo.get_all(limit)

    def create(self, data: dict) -> dict:
        concepto = data.get("concepto", "").strip()
        if not concepto:
            raise ValueError("El concepto del gasto es obligatorio.")

        monto = data.get("monto", 0)
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a cero.")

        gasto_id = self.gasto_repo.create(data)
        return {"success": True, "id": gasto_id}