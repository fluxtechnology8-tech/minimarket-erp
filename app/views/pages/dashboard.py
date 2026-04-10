from __future__ import annotations

import flet as ft
from app.views.components.ui import StatCard, empty_state, section_card
from app.views.ui.theme import AppTheme
from app.views.ui.utils import money


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
        bar_width = 32 if self.is_mobile else 42
        max_height = 140 if self.is_mobile else 160
        for item in metrics["daily_sales"]:
            height = (
                max(20, int((item["total"] / max_total) * max_height))
                if item["total"]
                else 20
            )
            chart_bars.append(
                ft.Column(
                    [
                        ft.Text(
                            money(item["total"]),
                            size=9 if self.is_mobile else 10,
                            color=AppTheme.TEXT_SECONDARY,
                        ),
                        ft.Container(
                            width=bar_width,
                            height=height,
                            bgcolor=AppTheme.PRIMARY_CONTAINER,
                            border_radius=8,
                        ),
                        ft.Text(
                            item["date"].strftime("%a"),
                            size=10 if self.is_mobile else 11,
                            color=AppTheme.TEXT_SECONDARY,
                        ),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    spacing=6,
                    alignment=ft.MainAxisAlignment.END,
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
            padding=ft.padding.only(bottom=80),
        )

    def _build_header(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Minimarket ERP",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_PRIMARY,
                    ),
                    ft.Text(
                        "Dashboard de gestión", size=14, color=AppTheme.TEXT_SECONDARY
                    ),
                ],
                tight=True,
            ),
        )

    def _build_stats_grid(self, metrics: dict) -> ft.Container:
        return ft.Container(
            padding=0,
            content=ft.ResponsiveRow(
                [
                    ft.Column(
                        [
                            StatCard(
                                "Productos activos",
                                str(metrics["total_productos"]),
                                ft.Icons.INVENTORY_2_ROUNDED,
                                AppTheme.PRIMARY,
                            )
                        ],
                        col={"sm": 6, "md": 3},
                    ),
                    ft.Column(
                        [
                            StatCard(
                                "Stock bajo",
                                str(metrics["stock_bajo"]),
                                ft.Icons.WARNING_AMBER_ROUNDED,
                                AppTheme.WARNING,
                            )
                        ],
                        col={"sm": 6, "md": 3},
                    ),
                    ft.Column(
                        [
                            StatCard(
                                "Ventas de hoy",
                                money(metrics["ventas_hoy"]),
                                ft.Icons.TRENDING_UP_ROUNDED,
                                AppTheme.SUCCESS,
                            )
                        ],
                        col={"sm": 6, "md": 3},
                    ),
                    ft.Column(
                        [
                            StatCard(
                                "Gastos del mes",
                                money(metrics["gastos_mes"]),
                                ft.Icons.PAYMENTS_ROUNDED,
                                AppTheme.DANGER,
                            )
                        ],
                        col={"sm": 6, "md": 3},
                    ),
                ],
                spacing=16,
                run_spacing=16,
            ),
        )

    def _build_chart_section(self, chart_bars: list[ft.Control]) -> ft.Container:
        bar_width = 36 if self.is_mobile else 42
        chart_row = ft.Row(
            chart_bars,
            alignment=ft.MainAxisAlignment.SPACE_AROUND,
            vertical_alignment=ft.CrossAxisAlignment.END,
            spacing=8,
        )
        return ft.Container(
            bgcolor=AppTheme.SURFACE_CONTAINER_LOW,
            border_radius=24,
            padding=16 if self.is_mobile else 24,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Ventas de la semana",
                                        size=18 if not self.is_mobile else 16,
                                        weight=ft.FontWeight.BOLD,
                                        color=AppTheme.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        "Rendimiento de los últimos 7 días",
                                        size=12 if not self.is_mobile else 11,
                                        color=AppTheme.TEXT_SECONDARY,
                                    ),
                                ],
                                tight=True,
                            ),
                            ft.Container(expand=True),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Container(
                        height=180 if self.is_mobile else 220,
                        margin=ft.margin.only(top=12, left=4, right=4),
                        content=chart_row,
                    ),
                ],
                spacing=8,
            ),
        )

    def _build_low_stock(self, low_stock: list) -> list[ft.Control]:
        if not low_stock:
            return [
                empty_state(
                    "No hay alertas de stock",
                    "Cuando un producto quede por debajo del mínimo aparecerá aquí.",
                    ft.Icons.CHECK_CIRCLE_OUTLINE,
                )
            ]

        items = []
        for producto in low_stock:
            items.append(
                ft.Container(
                    padding=16,
                    border_radius=16,
                    bgcolor=AppTheme.SURFACE_CONTAINER_LOWEST,
                    content=ft.Row(
                        [
                            ft.Container(
                                width=48,
                                height=48,
                                border_radius=12,
                                bgcolor=AppTheme.SURFACE_CONTAINER,
                                content=ft.Icon(
                                    ft.Icons.INVENTORY_2_OUTLINED,
                                    size=24,
                                    color=AppTheme.PRIMARY,
                                ),
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        producto["nombre"],
                                        size=14,
                                        weight=ft.FontWeight.W_600,
                                        color=AppTheme.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        f" Stock: {producto['stock']}",
                                        size=12,
                                        color=AppTheme.DANGER,
                                    ),
                                ],
                                expand=True,
                                tight=True,
                            ),
                            ft.Icon(
                                ft.Icons.ADD_SHOPPING_CART,
                                size=20,
                                color=AppTheme.PRIMARY,
                            ),
                        ],
                        spacing=12,
                    ),
                )
            )
        return items

    def _build_low_stock_section(self, items: list[ft.Control]) -> ft.Container:
        return ft.Container(
            bgcolor=AppTheme.SURFACE_CONTAINER_LOW,
            border_radius=24,
            padding=24,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "Productos con stock bajo",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color=AppTheme.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        "Acción requerida inmediata",
                                        size=12,
                                        color=AppTheme.TEXT_SECONDARY,
                                    ),
                                ],
                                tight=True,
                            ),
                            ft.Container(expand=True),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    ft.Column(items, spacing=12, margin=ft.margin.only(top=16)),
                ],
                spacing=8,
            ),
        )

    def _build_actions_section(self) -> ft.Container:
        return ft.Container(
            content=ft.ResponsiveRow(
                [
                    ft.Column(
                        [
                            ft.Container(
                                padding=24,
                                border_radius=24,
                                bgcolor=AppTheme.SURFACE_CONTAINER_LOW,
                                content=ft.Column(
                                    [
                                        ft.Text(
                                            "Reporte de Existencias",
                                            size=18,
                                            weight=ft.FontWeight.BOLD,
                                            color=AppTheme.TEXT_PRIMARY,
                                        ),
                                        ft.Text(
                                            "Genera un análisis detallado del movimiento.",
                                            size=12,
                                            color=AppTheme.TEXT_SECONDARY,
                                            max_lines=2,
                                        ),
                                        ft.Container(
                                            margin=ft.margin.only(top=16),
                                            padding=ft.padding.symmetric(
                                                horizontal=20, vertical=12
                                            ),
                                            bgcolor=AppTheme.PRIMARY,
                                            border_radius=24,
                                            content=ft.Text(
                                                "Generar PDF",
                                                size=14,
                                                weight=ft.FontWeight.W_600,
                                                color=ft.Colors.WHITE,
                                            ),
                                        ),
                                    ],
                                    tight=True,
                                ),
                            ),
                        ],
                        col={"md": 6},
                    ),
                    ft.Column(
                        [
                            ft.Container(
                                padding=24,
                                border_radius=24,
                                bgcolor=AppTheme.SURFACE_CONTAINER_LOW,
                                content=ft.Row(
                                    [
                                        ft.Column(
                                            [
                                                ft.Text(
                                                    "Sincronización",
                                                    size=18,
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
                                                    color=AppTheme.TEXT_SECONDARY,
                                                ),
                                            ],
                                            tight=True,
                                        ),
                                        ft.Container(
                                            width=64,
                                            height=64,
                                            border_radius=16,
                                            bgcolor=AppTheme.SURFACE_CONTAINER_LOWEST,
                                            content=ft.Icon(
                                                ft.Icons.CLOUD_DONE,
                                                size=32,
                                                color=AppTheme.PRIMARY,
                                            ),
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                ),
                            ),
                        ],
                        col={"md": 6},
                    ),
                ],
                spacing=16,
                run_spacing=16,
            ),
        )
