from services.reporte_service import ReporteService


class ReporteController:
    def __init__(self, reporte_service: ReporteService = None):
        self.service = reporte_service or ReporteService()

    def get_dashboard_metrics(self) -> dict:
        return self.service.get_dashboard_metrics()

    def get_report_metrics(self) -> dict:
        return self.service.get_report_metrics()