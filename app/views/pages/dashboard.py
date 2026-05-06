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
        bar_width = 28 if self.is_mobile else 28
        max_height = 110 if self.is_mobile else 110

        days = ["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"]
        actuals = [42, 65, 38, 88, 72, 34, 20]
        projections = [55, 70, 50, 80, 75, 45, 35]
        chart_max = max(actuals + projections)

        for i, (day, actual, proj) in enumerate(zip(days, actuals, projections)):
            bar_h = 110
            chart_bars.append(
                ft.Column(
                    [
                        ft.Stack(
                            controls=[
                                ft.Container(
                                    width=28,
                                    height=int((proj / chart_max) * bar_h),
                                    bgcolor=AppTheme.PRIMARY_LIGHT,
                                    border_radius=ft.BorderRadius(3, 3, 0, 0),
                                ),
                                ft.Container(
                                    width=28,
                                    height=int((actual / chart_max) * bar_h),
                                    bgcolor=AppTheme.PRIMARY,
                                    border_radius=ft.BorderRadius(3, 3, 0, 0),
                                ),
                            ],
                            height=bar_h,
                        ),
                        ft.Text(
                            day,
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
                ft.Row(
                    [
                        ft.Container(self._build_top_products(), expand=2),
                        ft.Container(
                            self._build_low_stock_section(low_stock_list), expand=1
                        ),
                    ],
                    spacing=14,
                    expand=True,
                ),
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
                        "Bienvenido de nuevo, Administrador. Aquí está el resumen de hoy.",
                        size=13,
                        color=AppTheme.TEXT_MUTED,
                    ),
                ],
                tight=True,
            ),
        )

    def _build_stats_grid(self, metrics: dict) -> ft.Container:
        def metric(
            icon, icon_color, icon_bg, tag_text, tag_color, tag_bg, label, value
        ):
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Container(
                                    content=ft.Icon(icon, color=icon_color, size=20),
                                    width=40,
                                    height=40,
                                    bgcolor=icon_bg,
                                    border_radius=AppTheme.R_MD,
                                    alignment=ft.Alignment(0, 0),
                                ),
                                ft.Container(expand=True),
                                badge(tag_text, tag_color, tag_bg),
                            ],
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            label,
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

        return ft.Row(
            [
                metric(
                    ft.Icons.CREDIT_CARD_OUTLINED,
                    AppTheme.PRIMARY,
                    AppTheme.PRIMARY_LIGHT,
                    "+12.5%",
                    AppTheme.PRIMARY,
                    AppTheme.PRIMARY_LIGHT,
                    "Total de Ventas",
                    money(metrics.get("ventas_hoy", 45280.00)),
                ),
                metric(
                    ft.Icons.INVENTORY_2_OUTLINED,
                    AppTheme.PRIMARY,
                    AppTheme.PRIMARY_LIGHT,
                    "842 SKU",
                    AppTheme.TEXT_MUTED,
                    AppTheme.INPUT_BG,
                    "Productos Activos",
                    str(metrics.get("total_productos", 1248)),
                ),
                metric(
                    ft.Icons.WARNING_AMBER_ROUNDED,
                    AppTheme.DANGER,
                    AppTheme.DANGER_LT,
                    "Urgente",
                    AppTheme.DANGER,
                    AppTheme.DANGER_LT,
                    "Stock Bajo",
                    f"{metrics.get('stock_bajo', 14)} Items",
                ),
                metric(
                    ft.Icons.SHOPPING_CART_OUTLINED,
                    AppTheme.WARNING,
                    AppTheme.WARNING_LT,
                    "-2% vs mes ant.",
                    AppTheme.WARNING,
                    AppTheme.WARNING_LT,
                    "Gastos Mensuales",
                    money(metrics.get("gastos_mes", 8420.50)),
                ),
            ],
            spacing=14,
        )

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
                                        "Ventas brutas vs Proyecciones",
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
                                            "Meses", size=11, color=AppTheme.CARD_BG
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

    def _build_top_products(self) -> ft.Container:
        return card(
            ft.Column(
                [
                    ft.Text(
                        "Productos más Vendidos",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_PRIMARY,
                    ),
                    ft.Container(height=6),
                    self._prod_row(
                        "✒️",
                        "Pluma Estilográfica",
                        "Escritura de lujo",
                        "S/ 2,450",
                        "124 VTAS",
                    ),
                    self._prod_row(
                        "📄",
                        "Papel Canson",
                        "Artístico / Acuarela",
                        "S/ 1,820",
                        "98 VTAS",
                    ),
                    self._prod_row(
                        "🖊️", "Marcadores", "Tinta pigmentada", "S/ 1,140", "82 VTAS"
                    ),
                    self._prod_row(
                        "📓", "Cuaderno Premium", "Hojas de 90g", "S/ 940", "65 VTAS"
                    ),
                    ft.Container(height=6),
                    ft.Container(
                        content=ft.Text(
                            "Ver Catálogo Completo",
                            size=12,
                            color=AppTheme.PRIMARY,
                            weight=ft.FontWeight.W_600,
                        ),
                        alignment=ft.Alignment(0, 0),
                        bgcolor=AppTheme.PRIMARY_LIGHT,
                        border_radius=AppTheme.R_MD,
                        padding=ft.padding.symmetric(vertical=9),
                        ink=True,
                    ),
                ],
                spacing=0,
            ),
        )

    def _prod_row(self, emoji, name, cat, amount, vtas):
        return ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Text(emoji, size=20),
                        width=40,
                        height=40,
                        bgcolor=AppTheme.INPUT_BG,
                        border_radius=AppTheme.R_MD,
                        alignment=ft.Alignment(0, 0),
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                name,
                                size=13,
                                weight=ft.FontWeight.W_600,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                            ft.Text(cat, size=11, color=AppTheme.TEXT_MUTED),
                        ],
                        spacing=1,
                        expand=True,
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                amount,
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.PRIMARY,
                            ),
                            ft.Text(vtas, size=10, color=AppTheme.TEXT_MUTED),
                        ],
                        spacing=1,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            border=ft.Border(bottom=ft.BorderSide(0.5, AppTheme.CARD_BORDER)),
            padding=ft.padding.symmetric(vertical=8),
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
                self._crit_item(
                    producto.get("nombre", "Producto"),
                    f"{producto.get('stock', 0)} unidades restantes",
                    min(
                        80,
                        max(
                            10,
                            int(
                                (
                                    producto.get("stock", 0)
                                    / (producto.get("stock_minimo", 10))
                                )
                                * 100
                            ),
                        ),
                    ),
                    AppTheme.DANGER
                    if producto.get("stock", 0) < 5
                    else AppTheme.WARNING,
                )
            )
        return items

    def _crit_item(self, name, amount, pct, color):
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            name, size=12, color=AppTheme.TEXT_SECONDARY, expand=True
                        ),
                        ft.Text(
                            amount, size=12, weight=ft.FontWeight.W_600, color=color
                        ),
                    ],
                ),
                ft.Container(
                    content=ft.Container(
                        bgcolor=color,
                        border_radius=AppTheme.R_PILL,
                        width=max(pct * 2, 20),
                        height=6,
                    ),
                    bgcolor=AppTheme.INPUT_BG,
                    border_radius=AppTheme.R_PILL,
                    height=6,
                ),
            ],
            spacing=4,
        )

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
                    self._crit_item(
                        "Resmas Papel Bond A4 (80g)",
                        "12 unidades restantes",
                        50,
                        AppTheme.DANGER,
                    ),
                    ft.Container(height=10),
                    self._crit_item(
                        "Tinta Epson Cyan 544",
                        "8 unidades restantes",
                        80,
                        AppTheme.WARNING,
                    ),
                ],
            ),
        )
