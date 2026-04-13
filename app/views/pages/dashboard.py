from __future__ import annotations

import flet as ft
from views.components.ui import StatCard, empty_state, section_card, card, badge
from views.ui.theme import AppTheme, shadow
from views.ui.utils import money


class DashboardView(ft.Container):
    def __init__(self, controller, is_mobile: bool = False):
        super().__init__(expand=True, padding=0)
        self.controller = controller
        self.is_mobile = is_mobile
        self.build_view()

    def build_view(self) -> None:
        metrics = self.controller.get_dashboard_metrics()
        max_total = (
            max([item["total"] for item in metrics["daily_sales"]], default=0) or 1
        )

        chart_bars: list[ft.Control] = []
        bar_width = 28 if self.is_mobile else 32
        max_height = 110 if self.is_mobile else 120
        for item in metrics["daily_sales"]:
            height = (
                max(20, int((item["total"] / max_total) * max_height))
                if item["total"]
                else 20
            )
            chart_bars.append(
                ft.Column(
                    [
                        ft.Stack(
                            controls=[
                                ft.Container(
                                    width=bar_width,
                                    height=height,
                                    bgcolor=AppTheme.PRIMARY_LIGHT,
                                    border_radius=ft.BorderRadius(3, 3, 0, 0),
                                ),
                                ft.Container(
                                    width=bar_width,
                                    height=height,
                                    bgcolor=AppTheme.PRIMARY,
                                    border_radius=ft.BorderRadius(3, 3, 0, 0),
                                ),
                            ],
                        ),
                        ft.Text(
                            item["date"].strftime("%a"),
                            size=10,
                            color=AppTheme.TEXT_MUTED,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=4,
                )
            )

        low_stock_list = self._build_low_stock(metrics.get("low_stock", []))

        self.content = ft.ListView(
            [
                self._build_header(),
                self._build_stats_grid(metrics),
                self._build_chart_section(chart_bars),
                self._build_low_stock_section(low_stock_list),
                self._build_actions_section(),
            ],
            expand=True,
            spacing=24,
            padding=ft.Padding.only(bottom=80),
        )

    def _build_header(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Panel de Control",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_PRIMARY,
                    ),
                    ft.Text(
                        "Bienvenido de nuevo. Aquí está el resumen de hoy.",
                        size=13,
                        color=AppTheme.TEXT_MUTED,
                    ),
                ],
                tight=True,
            ),
        )

    def _build_stats_grid(self, metrics: dict) -> ft.Container:
        metrics_data = [
            (
                "Productos activos",
                str(metrics["total_productos"]),
                ft.Icons.INVENTORY_2_OUTLINED,
                AppTheme.PRIMARY,
                AppTheme.PRIMARY_LIGHT,
            ),
            (
                "Stock bajo",
                str(metrics["stock_bajo"]),
                ft.Icons.WARNING_AMBER_ROUNDED,
                AppTheme.DANGER,
                AppTheme.DANGER_LT,
            ),
            (
                "Ventas de hoy",
                money(metrics["ventas_hoy"]),
                ft.Icons.TRENDING_UP_ROUNDED,
                AppTheme.SUCCESS,
                AppTheme.SUCCESS_LT,
            ),
            (
                "Gastos del mes",
                money(metrics["gastos_mes"]),
                ft.Icons.PAYMENTS_ROUNDED,
                AppTheme.WARNING,
                AppTheme.WARNING_LT,
            ),
        ]

        cards = []
        for title, value, icon, color, bg in metrics_data:
            cards.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Icon(icon, color=color, size=20),
                                        width=40,
                                        height=40,
                                        bgcolor=bg,
                                        border_radius=AppTheme.R_MD,
                                        alignment=ft.Alignment(0, 0),
                                    ),
                                    ft.Container(expand=True),
                                ],
                            ),
                            ft.Container(height=8),
                            ft.Text(
                                title,
                                size=12,
                                color=AppTheme.TEXT_MUTED,
                            ),
                            ft.Text(
                                value,
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                        ],
                        spacing=3,
                    ),
                    bgcolor=AppTheme.CARD_BG,
                    border_radius=AppTheme.R_LG,
                    padding=16,
                    border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
                    shadow=shadow(AppTheme.PRIMARY, 6, 2),
                    expand=1,
                )
            )

        return ft.Row(cards, spacing=14)

    def _build_chart_section(self, chart_bars: list[ft.Control]) -> ft.Container:
        return card(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Rendimiento Semanal",
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=AppTheme.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        "Ventas brutas de la semana",
                                        size=11,
                                        color=AppTheme.TEXT_MUTED,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Text(
                                            "Semanas",
                                            size=11,
                                            color=AppTheme.TEXT_MUTED,
                                        ),
                                        padding=ft.padding.symmetric(
                                            horizontal=12, vertical=5
                                        ),
                                        border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
                                        border_radius=AppTheme.R_PILL,
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            "Meses", size=11, color="#FFFFFF"
                                        ),
                                        bgcolor=AppTheme.PRIMARY,
                                        padding=ft.padding.symmetric(
                                            horizontal=12, vertical=5
                                        ),
                                        border_radius=AppTheme.R_PILL,
                                    ),
                                ],
                                spacing=6,
                            ),
                        ],
                    ),
                    ft.Container(height=8),
                    ft.Row(
                        [
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        width=10,
                                        height=10,
                                        bgcolor=AppTheme.PRIMARY,
                                        border_radius=2,
                                    ),
                                    ft.Text(
                                        "Ventas", size=11, color=AppTheme.TEXT_MUTED
                                    ),
                                ],
                                spacing=4,
                            ),
                            ft.Row(
                                controls=[
                                    ft.Container(
                                        width=10,
                                        height=10,
                                        bgcolor=AppTheme.PRIMARY_LIGHT,
                                        border_radius=2,
                                    ),
                                    ft.Text(
                                        "Proyectado", size=11, color=AppTheme.TEXT_MUTED
                                    ),
                                ],
                                spacing=4,
                            ),
                        ],
                        spacing=14,
                    ),
                    ft.Container(height=8),
                    ft.Row(
                        chart_bars,
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                ],
            ),
        )

    def _build_low_stock(self, low_stock: list) -> list[ft.Control]:
        if not low_stock:
            return [
                empty_state(
                    "No hay alertas de stock",
                    "Cuando un producto quede por debajo del mínimo aparecerá aquí.",
                    ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                )
            ]

        items = []
        for producto in low_stock:
            items.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.INVENTORY_2_OUTLINED,
                                    size=20,
                                    color=AppTheme.PRIMARY,
                                ),
                                width=40,
                                height=40,
                                bgcolor=AppTheme.INPUT_BG,
                                border_radius=AppTheme.R_MD,
                                alignment=ft.Alignment(0, 0),
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        producto["nombre"],
                                        size=13,
                                        weight=ft.FontWeight.W_600,
                                        color=AppTheme.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        f"Stock: {producto['stock']}",
                                        size=11,
                                        color=AppTheme.DANGER,
                                    ),
                                ],
                                expand=True,
                                spacing=1,
                            ),
                            ft.Icon(
                                ft.Icons.ADD_SHOPPING_CART,
                                size=18,
                                color=AppTheme.PRIMARY,
                            ),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    border=ft.Border(bottom=ft.BorderSide(0.5, AppTheme.CARD_BORDER)),
                    padding=ft.padding.symmetric(vertical=8),
                )
            )
        return items

    def _build_low_stock_section(self, items: list[ft.Control]) -> ft.Container:
        return card(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                                color=AppTheme.PRIMARY,
                                size=16,
                            ),
                            ft.Text(
                                "Estado de Existencias Críticas",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=12),
                    ft.Column(items, spacing=0),
                ],
            ),
        )

    def _build_actions_section(self) -> ft.Container:
        return ft.Row(
            [
                card(
                    ft.Column(
                        [
                            ft.Text(
                                "Reporte de Existencias",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                            ft.Text(
                                "Genera un análisis detallado del movimiento.",
                                size=12,
                                color=AppTheme.TEXT_MUTED,
                                max_lines=2,
                            ),
                            ft.Container(height=12),
                            ft.Container(
                                content=ft.Row(
                                    [
                                        ft.Icon(
                                            ft.Icons.PICTURE_AS_PDF,
                                            size=16,
                                            color=AppTheme.PRIMARY,
                                        ),
                                        ft.Text(
                                            "Generar PDF",
                                            size=12,
                                            weight=ft.FontWeight.W_600,
                                            color=AppTheme.PRIMARY,
                                        ),
                                    ],
                                    spacing=6,
                                ),
                                padding=ft.padding.symmetric(
                                    horizontal=16, vertical=10
                                ),
                                bgcolor=AppTheme.PRIMARY_LIGHT,
                                border_radius=AppTheme.R_MD,
                            ),
                        ],
                        spacing=8,
                    ),
                ),
                card(
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Text(
                                                "Sincronización",
                                                size=14,
                                                weight=ft.FontWeight.BOLD,
                                                color=AppTheme.TEXT_PRIMARY,
                                            ),
                                            ft.Row(
                                                [
                                                    ft.Container(
                                                        width=8,
                                                        height=8,
                                                        border_radius=4,
                                                        bgcolor=AppTheme.SUCCESS,
                                                    ),
                                                    ft.Text(
                                                        "Cloud Sync Activo",
                                                        size=12,
                                                        color=AppTheme.SUCCESS,
                                                    ),
                                                ],
                                                spacing=8,
                                            ),
                                            ft.Text(
                                                "Última sync: hace 3 min",
                                                size=11,
                                                color=AppTheme.TEXT_MUTED,
                                            ),
                                        ],
                                        spacing=4,
                                        tight=True,
                                    ),
                                    ft.Container(
                                        width=40,
                                        height=40,
                                        bgcolor=AppTheme.INPUT_BG,
                                        border_radius=AppTheme.R_MD,
                                        content=ft.Icon(
                                            ft.Icons.CLOUD_DONE,
                                            size=20,
                                            color=AppTheme.PRIMARY,
                                        ),
                                        alignment=ft.Alignment(0, 0),
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                        ],
                        spacing=8,
                    ),
                ),
            ],
            spacing=14,
        )
