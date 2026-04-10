from repositories.reporte_repository import ReporteRepository


class ReporteService:
    def __init__(self, reporte_repo: ReporteRepository = None):
        self.reporte_repo = reporte_repo or ReporteRepository()

    def get_dashboard_metrics(self) -> dict:
        return self.reporte_repo.get_dashboard_metrics()

    def get_report_metrics(self) -> dict:
        return self.reporte_repo.get_report_metrics()