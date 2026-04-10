from core.database import get_session_manager
from models.gasto import Gasto


class GastoRepository:
    def __init__(self, session_manager=None):
        self._sm = session_manager or get_session_manager()

    def get_all(self, limit: int = 100) -> list[dict]:
        with self._sm.get_session() as session:
            gastos = session.query(Gasto).order_by(Gasto.fecha.desc(), Gasto.id.desc()).limit(limit).all()
            return [self._to_dict(g) for g in gastos]

    def create(self, data: dict) -> int:
        with self._sm.get_session() as session:
            gasto = Gasto(
                concepto=data["concepto"],
                monto=data["monto"],
                categoria=data.get("categoria", ""),
                observaciones=data.get("observaciones", ""),
            )
            session.add(gasto)
            session.flush()
            return gasto.id

    def _to_dict(self, g: Gasto) -> dict:
        return {
            "id": g.id,
            "concepto": g.concepto,
            "monto": g.monto,
            "categoria": g.categoria,
            "fecha": g.fecha,
            "observaciones": g.observaciones,
        }