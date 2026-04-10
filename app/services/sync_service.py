import json
from pathlib import Path
from app.repositories.sync_repository import SyncRepository


class SyncService:
    def __init__(self, sync_repo: SyncRepository = None):
        self.sync_repo = sync_repo or SyncRepository()

    def get_export_bytes(self) -> bytes:
        return self.sync_repo.get_export_bytes()

    def export_data(self, output_path: str) -> dict:
        try:
            data = self.sync_repo.export_all()
            path = Path(output_path)
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
            return {"success": True, "path": str(path)}
        except Exception as e:
            raise ValueError(f"No se pudo exportar: {str(e)}")

    def import_data(self, input_path: str, merge: bool = True) -> dict:
        try:
            path = Path(input_path)
            if not path.exists():
                raise ValueError(f"El archivo {input_path} no existe.")
            data = json.loads(path.read_text(encoding="utf-8"))
            self.sync_repo.import_all(data, merge)
            return {"success": True, "mode": "fusionado" if merge else "reemplazado"}
        except json.JSONDecodeError:
            raise ValueError("El archivo no es un JSON válido.")
        except Exception as e:
            raise ValueError(f"No se pudo importar: {str(e)}")