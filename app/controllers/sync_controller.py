from services.sync_service import SyncService


class SyncController:
    def __init__(self, sync_service: SyncService = None):
        self.service = sync_service or SyncService()

    def get_export_bytes(self) -> bytes:
        return self.service.get_export_bytes()

    def export_data(self, output_path: str) -> dict:
        return self.service.export_data(output_path)

    def import_data(self, input_path: str, merge: bool = True) -> dict:
        return self.service.import_data(input_path, merge)