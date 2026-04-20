from __future__ import annotations

import flet as ft

from views.components.ui import (
    StatCard,
    empty_state,
    section_card,
    card,
    badge,
    primary_btn,
)
from views.ui.theme import AppTheme, shadow
from views.ui.utils import money


class ReportesView(ft.Container):
    def __init__(self, page: ft.Page, controller):
        super().__init__(expand=True, padding=24)
        self._page = page
        self.controller = controller
        self.build_view()

    def build_view(self) -> None:
        metrics = self.controller.get_report_metrics()

        self.content = ft.Column(
            [
                self._build_header(),
                self._build_main_content(metrics),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=14,
        )

    def _build_header(self) -> ft.Container:
        return ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            "Reportes y Analítica",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=AppTheme.TEXT_PRIMARY,
                        ),
                        ft.Text(
                            "Visualiza el rendimiento de tu papelería con datos precisos.",
                            size=13,
                            color=AppTheme.TEXT_MUTED,
                        ),
                    ],
                    tight=True,
                ),
                ft.Container(expand=True),
                ft.Row(
                    [
                        primary_btn("Este Mes"),
                        primary_btn("Trimestre", variant="outline"),
                        primary_btn("Año 2024", variant="outline"),
                    ],
                    spacing=6,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.END,
        )

    def _build_main_content(self, metrics: dict) -> ft.Column:
        def report_stat(tag, tag_color, tag_bg, label, value, diff, diff_color):
            return ft.Container(
                content=ft.Column(
                    [
                        badge(tag, tag_color, tag_bg),
                        ft.Container(height=6),
                        ft.Text(label, size=12, color=AppTheme.TEXT_MUTED),
                        ft.Text(
                            value,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=AppTheme.TEXT_PRIMARY,
                        ),
                        ft.Text(diff, size=11, color=diff_color),
                    ],
                    spacing=3,
                ),
                bgcolor=AppTheme.CARD_BG,
                border_radius=AppTheme.R_LG,
                padding=16,
                border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
                shadow=shadow(AppTheme.PRIMARY, 4, 1),
            )

        stats_col = ft.Column(
            [
                report_stat(
                    "EXISTENCIAS",
                    AppTheme.PRIMARY,
                    AppTheme.PRIMARY_LIGHT,
                    "Ventas Totales",
                    "S/ 45,280.00",
                    "↑ +12.5% vs mes anterior",
                    AppTheme.SUCCESS,
                ),
                ft.Container(height=10),
                report_stat(
                    "MARGEN",
                    AppTheme.SUCCESS,
                    AppTheme.SUCCESS_LT,
                    "Utilidad Neta",
                    "S/ 12,840.50",
                    "↑ +5.2% vs mes anterior",
                    AppTheme.SUCCESS,
                ),
                ft.Container(height=10),
                ft.Container(
                    content=ft.Column(
                        [
                            badge("CRÍTICO", AppTheme.DANGER, AppTheme.DANGER_LT),
                            ft.Container(height=6),
                            ft.Text(
                                "Productos Sin Stock",
                                size=12,
                                color=AppTheme.TEXT_MUTED,
                            ),
                            ft.Text(
                                "24 Items",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                            ft.Text(
                                "Requiere reposición inmediata",
                                size=11,
                                color=AppTheme.TEXT_MUTED,
                            ),
                        ],
                        spacing=3,
                    ),
                    bgcolor=AppTheme.CARD_BG,
                    border_radius=AppTheme.R_LG,
                    padding=16,
                    border=ft.Border.all(
                        0.5, ft.Colors.with_opacity(0.4, AppTheme.DANGER)
                    ),
                    shadow=shadow(AppTheme.DANGER, 4, 1),
                ),
            ],
            spacing=0,
            width=230,
        )

        trend_card = card(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Tendencias de Venta Diaria",
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=AppTheme.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        "Visualización del flujo de caja durante los últimos 30 días",
                                        size=11,
                                        color=AppTheme.TEXT_MUTED,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Row(
                                [
                                    ft.Row(
                                        [
                                            ft.Container(
                                                width=8,
                                                height=8,
                                                bgcolor=AppTheme.PRIMARY,
                                                border_radius=AppTheme.R_PILL,
                                            ),
                                            ft.Text(
                                                "Ventas",
                                                size=11,
                                                color=AppTheme.TEXT_MUTED,
                                            ),
                                        ],
                                        spacing=4,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Container(
                                                width=8,
                                                height=8,
                                                bgcolor=AppTheme.PRIMARY_LIGHT,
                                                border_radius=AppTheme.R_PILL,
                                            ),
                                            ft.Text(
                                                "Proyectado",
                                                size=11,
                                                color=AppTheme.TEXT_MUTED,
                                            ),
                                        ],
                                        spacing=4,
                                    ),
                                ],
                                spacing=12,
                            ),
                        ],
                    ),
                    ft.Container(height=12),
                    self._build_chart(),
                ],
            ),
        )

        def cat_row_item(color, label, amount):
            return ft.Row(
                [
                    ft.Container(
                        width=10,
                        height=10,
                        bgcolor=color,
                        border_radius=AppTheme.R_PILL,
                    ),
                    ft.Text(label, size=12, color=AppTheme.TEXT_SECONDARY, expand=True),
                    ft.Text(
                        amount,
                        size=12,
                        weight=ft.FontWeight.W_600,
                        color=AppTheme.TEXT_PRIMARY,
                    ),
                ],
                spacing=8,
            )

        categ_card = card(
            ft.Column(
                [
                    ft.Text(
                        "Desempeño por Categoría",
                        size=13,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_PRIMARY,
                    ),
                    ft.Container(height=10),
                    ft.Stack(
                        controls=[
                            ft.Container(
                                width=80,
                                height=80,
                                border_radius=40,
                                border=ft.Border.all(10, AppTheme.INPUT_BG),
                                bgcolor="transparent",
                            ),
                            ft.Container(
                                content=ft.Text(
                                    "65%",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=AppTheme.TEXT_PRIMARY,
                                ),
                                width=80,
                                height=80,
                                alignment=ft.Alignment(0, 0),
                            ),
                        ],
                        width=80,
                        height=80,
                    ),
                    ft.Container(height=10),
                    cat_row_item(AppTheme.PRIMARY, "Útiles de Oficina", "S/ 24.5k"),
                    cat_row_item(AppTheme.PRIMARY_LIGHT, "Arte y Diseño", "S/ 12.1k"),
                    cat_row_item(AppTheme.PRIMARY_MID, "Papelería Fina", "S/ 5.4k"),
                    cat_row_item(AppTheme.INPUT_BG, "Otros", "S/ 3.2k"),
                ],
                spacing=4,
            ),
        )

        def margin_row(name, pct):
            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                name,
                                size=12,
                                color=AppTheme.TEXT_SECONDARY,
                                expand=True,
                            ),
                            ft.Text(
                                f"{pct}%",
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.PRIMARY,
                            ),
                        ],
                    ),
                    ft.Container(
                        content=ft.Container(
                            bgcolor=AppTheme.PRIMARY,
                            border_radius=AppTheme.R_PILL,
                            width=int(pct * 2.2),
                            height=5,
                        ),
                        bgcolor=AppTheme.INPUT_BG,
                        border_radius=AppTheme.R_PILL,
                        height=5,
                    ),
                ],
                spacing=4,
            )

        margin_card = card(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Margen por Proveedor",
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                                expand=True,
                            ),
                            ft.Text("VER TODO ›", size=11, color=AppTheme.PRIMARY),
                        ],
                    ),
                    ft.Container(height=10),
                    margin_row("Faber-Castell", 42),
                    ft.Container(height=6),
                    margin_row("Artesco", 38),
                    ft.Container(height=6),
                    margin_row("Pilot Corporation", 31),
                    ft.Container(height=6),
                    margin_row("Ledesma S.A.", 27),
                    ft.Container(height=10),
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.INFO_OUTLINE_ROUNDED,
                                    color=AppTheme.INFO,
                                    size=13,
                                ),
                                ft.Container(width=6),
                                ft.Text(
                                    "El margen promedio ha subido un 2.4% "
                                    "por nueva negociación con distribuidores locales.",
                                    size=11,
                                    color=AppTheme.INFO,
                                    italic=True,
                                    expand=True,
                                ),
                            ],
                        ),
                        bgcolor=AppTheme.INFO_LT,
                        border_radius=AppTheme.R_MD,
                        padding=10,
                    ),
                ],
                spacing=0,
            ),
        )

        def alert_row(
            emoji,
            name,
            ref,
            stock,
            stock_color,
            minimo,
            estado,
            estado_color,
            estado_bg,
        ):
            return ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Row(
                            controls=[
                                ft.Text(emoji, size=16),
                                ft.Text(name, size=12, color=AppTheme.TEXT_PRIMARY),
                            ],
                            spacing=6,
                        )
                    ),
                    ft.DataCell(ft.Text(ref, size=11, color=AppTheme.TEXT_MUTED)),
                    ft.DataCell(
                        ft.Text(
                            stock, size=12, weight=ft.FontWeight.BOLD, color=stock_color
                        )
                    ),
                    ft.DataCell(
                        ft.Text(str(minimo), size=12, color=AppTheme.TEXT_SECONDARY)
                    ),
                    ft.DataCell(badge(estado, estado_color, estado_bg)),
                    ft.DataCell(
                        ft.Icon(
                            ft.Icons.SHOPPING_CART_OUTLINED,
                            color=AppTheme.PRIMARY,
                            size=16,
                        )
                    ),
                ],
            )

        alert_table = ft.DataTable(
            columns=[
                ft.DataColumn(
                    ft.Text(
                        "Producto",
                        size=11,
                        color=AppTheme.TEXT_MUTED,
                        weight=ft.FontWeight.W_600,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Referencia",
                        size=11,
                        color=AppTheme.TEXT_MUTED,
                        weight=ft.FontWeight.W_600,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Stock Actual",
                        size=11,
                        color=AppTheme.TEXT_MUTED,
                        weight=ft.FontWeight.W_600,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Mínimo",
                        size=11,
                        color=AppTheme.TEXT_MUTED,
                        weight=ft.FontWeight.W_600,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Estado",
                        size=11,
                        color=AppTheme.TEXT_MUTED,
                        weight=ft.FontWeight.W_600,
                    )
                ),
                ft.DataColumn(
                    ft.Text(
                        "Acción",
                        size=11,
                        color=AppTheme.TEXT_MUTED,
                        weight=ft.FontWeight.W_600,
                    )
                ),
            ],
            rows=[
                alert_row(
                    "✒️",
                    "Pluma Estilográfica Premium",
                    "PC-992-BLK",
                    "2 unidades",
                    AppTheme.DANGER,
                    10,
                    "AGOTÁNDOSE",
                    AppTheme.WARNING,
                    AppTheme.WARNING_LT,
                ),
                alert_row(
                    "📄",
                    "Papel Bond 80g A4 (500h)",
                    "PB-A4-500",
                    "0 unidades",
                    AppTheme.DANGER,
                    50,
                    "SIN STOCK",
                    AppTheme.DANGER,
                    AppTheme.DANGER_LT,
                ),
            ],
            border=ft.Border.all(0, "transparent"),
            heading_row_color=AppTheme.INPUT_BG,
            data_row_color={"hovered": AppTheme.PRIMARY_LIGHT},
            column_spacing=14,
        )

        alerts_card = card(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Alerta de Existencias (Crítico)",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                                expand=True,
                            ),
                            primary_btn(
                                "Descargar Reporte PDF",
                                ft.Icons.PICTURE_AS_PDF_ROUNDED,
                                "outline",
                            ),
                        ],
                    ),
                    ft.Container(height=10),
                    ft.Container(
                        content=alert_table,
                        bgcolor=AppTheme.INPUT_BG,
                        border_radius=AppTheme.R_MD,
                        border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
                    ),
                ],
            ),
        )

        return ft.Column(
            [
                ft.Row(
                    [
                        stats_col,
                        ft.Container(
                            content=ft.Column(
                                [
                                    trend_card,
                                    ft.Container(height=12),
                                    ft.Row(
                                        [
                                            ft.Container(categ_card, expand=1),
                                            ft.Container(margin_card, expand=1),
                                        ],
                                        spacing=12,
                                    ),
                                ],
                                spacing=0,
                            ),
                            expand=True,
                        ),
                    ],
                    spacing=14,
                    vertical_alignment=ft.CrossAxisAlignment.START,
                ),
                ft.Container(height=14),
                alerts_card,
            ],
        )

    def _build_chart(self):
        weeks = [[40, 45, 60, 50], [70, 80, 95, 75], [55, 65, 88, 92], [60, 72, 65, 45]]
        proj = [[50, 55, 65, 60], [75, 85, 90, 80], [60, 70, 85, 88], [65, 75, 70, 50]]
        all_vals = [v for row in weeks + proj for v in row]
        max_v = max(all_vals)

        bar_cols = []
        for wi, (wvals, pvals) in enumerate(zip(weeks, proj)):
            week_bars = ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Container(
                                bgcolor=AppTheme.PRIMARY_LIGHT,
                                border_radius=ft.BorderRadius(3, 3, 0, 0),
                                width=12,
                                height=int((pvals[di] / max_v) * 160),
                            ),
                            ft.Container(
                                bgcolor=AppTheme.PRIMARY,
                                border_radius=ft.BorderRadius(3, 3, 0, 0),
                                width=12,
                                height=int((wvals[di] / max_v) * 160),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=2,
                    )
                    for di in range(4)
                ],
                spacing=3,
                vertical_alignment=ft.CrossAxisAlignment.END,
            )
            bar_cols.append(
                ft.Column(
                    controls=[
                        week_bars,
                        ft.Text(f"SEMANA 0{wi + 1}", size=9, color=AppTheme.TEXT_MUTED),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                )
            )

        return ft.Row(
            bar_cols,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.END,
        )

    def generate_inventario_pdf(self, e):
        self._show_pdf_message("Generando reporte de inventario...")

    def generate_ventas_pdf(self, e):
        self._show_pdf_message("Generando reporte de ventas...")

    def generate_gastos_pdf(self, e):
        self._show_pdf_message("Generando reporte de gastos...")

    def generate_movimientos_pdf(self, e):
        self._show_pdf_message("Generando reporte de movimientos...")

    def generate_resumen_pdf(self, e):
        self._show_pdf_message("Generando resumen general...")

    def _show_pdf_message(self, message: str) -> None:
        if hasattr(self, "_page"):
            self._page.snack_bar = ft.SnackBar(ft.Text(message))
            self._page.snack_bar.open = True
            self._page.update()
