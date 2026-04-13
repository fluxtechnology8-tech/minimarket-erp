from __future__ import annotations

import flet as ft

from views.components.ui import StatCard, empty_state, section_card, card
from views.ui.theme import AppTheme
from views.ui.utils import money


class ReportesView(ft.Column):
    def __init__(self, page: ft.Page, controller):
        super().__init__(expand=True, scroll=ft.ScrollMode.AUTO, spacing=20)
        self._page = page
        self.controller = controller
        self.padding = 24
        self.build_view()

    def build_view(self) -> None:
        metrics = self.controller.get_report_metrics()

        def _build_pdf_card(title, subtitle, icon, on_click):
            return ft.Container(
                padding=16,
                border_radius=AppTheme.R_LG,
                bgcolor=AppTheme.INPUT_BG,
                content=ft.Column(
                    [
                        ft.Container(
                            padding=12,
                            bgcolor=AppTheme.PRIMARY_LIGHT,
                            border_radius=AppTheme.R_MD,
                            content=ft.Icon(icon, color=AppTheme.PRIMARY, size=28),
                        ),
                        ft.Text(
                            title,
                            size=14,
                            weight=ft.FontWeight.W_600,
                            color=AppTheme.TEXT_PRIMARY,
                        ),
                        ft.Text(subtitle, size=11, color=AppTheme.TEXT_MUTED),
                    ],
                    spacing=8,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                on_click=on_click,
            )

        if metrics.get("top_productos"):
            top_controls = [
                ft.ListTile(
                    leading=ft.Icon(
                        ft.Icons.STAR_BORDER_ROUNDED, color=AppTheme.PRIMARY
                    ),
                    title=ft.Text(item["nombre"]),
                    subtitle=ft.Text(
                        f"Cantidad: {item.get('cantidad_vendida', 0)} | {money(float(item.get('total_vendido') or 0))}"
                    ),
                )
                for item in metrics["top_productos"]
            ]
        else:
            top_controls = [
                empty_state(
                    "Aún no hay ventas para analizar",
                    "Cuando se registren boletas aparecerán los productos más vendidos.",
                    ft.Icons.QUERY_STATS_OUTLINED,
                )
            ]

        self.controls = [
            ft.Text("Reportes", size=28, weight=ft.FontWeight.BOLD),
            section_card(
                "Generar reportes PDF",
                [
                    ft.ResponsiveRow(
                        [
                            ft.Column(
                                [
                                    _build_pdf_card(
                                        "Inventario",
                                        "Listado completo",
                                        ft.Icons.INVENTORY_2,
                                        self.generate_inventario_pdf,
                                    )
                                ],
                                col={"sm": 12, "md": 4},
                            ),
                            ft.Column(
                                [
                                    _build_pdf_card(
                                        "Ventas",
                                        "Reporte del mes",
                                        ft.Icons.RECEIPT_LONG,
                                        self.generate_ventas_pdf,
                                    )
                                ],
                                col={"sm": 12, "md": 4},
                            ),
                            ft.Column(
                                [
                                    _build_pdf_card(
                                        "Gastos",
                                        "Resumen mensual",
                                        ft.Icons.PAYMENTS,
                                        self.generate_gastos_pdf,
                                    )
                                ],
                                col={"sm": 12, "md": 4},
                            ),
                            ft.Column(
                                [
                                    _build_pdf_card(
                                        "Movimientos",
                                        "Entradas y salidas",
                                        ft.Icons.SWAP_HORIZ,
                                        self.generate_movimientos_pdf,
                                    )
                                ],
                                col={"sm": 12, "md": 4},
                            ),
                            ft.Column(
                                [
                                    _build_pdf_card(
                                        "Resumen general",
                                        "Estado financiero",
                                        ft.Icons.ASSESSMENT,
                                        self.generate_resumen_pdf,
                                    )
                                ],
                                col={"sm": 12, "md": 4},
                            ),
                        ],
                        spacing=16,
                        run_spacing=16,
                    ),
                ],
                "Exporta los datos en formato PDF.",
            ),
            ft.ResponsiveRow(
                [
                    ft.Column(
                        [
                            StatCard(
                                "Unidades en stock",
                                str(metrics.get("total_stock", 0)),
                                ft.Icons.WAREHOUSE_ROUNDED,
                                AppTheme.PRIMARY,
                            )
                        ],
                        col={"sm": 6, "md": 3},
                    ),
                    ft.Column(
                        [
                            StatCard(
                                "Valor inventario",
                                money(metrics.get("valor_inventario", 0)),
                                ft.Icons.INVENTORY_ROUNDED,
                                AppTheme.SUCCESS,
                            )
                        ],
                        col={"sm": 6, "md": 3},
                    ),
                    ft.Column(
                        [
                            StatCard(
                                "Ventas del mes",
                                money(metrics.get("ventas_mes", 0)),
                                ft.Icons.POINT_OF_SALE_ROUNDED,
                                AppTheme.PRIMARY_CONTAINER,
                            )
                        ],
                        col={"sm": 6, "md": 3},
                    ),
                    ft.Column(
                        [
                            StatCard(
                                "Utilidad estimada",
                                money(metrics.get("utilidad_estimada", 0)),
                                ft.Icons.INSIGHTS_ROUNDED,
                                AppTheme.WARNING,
                            )
                        ],
                        col={"sm": 6, "md": 3},
                    ),
                ],
                spacing=12,
                run_spacing=12,
            ),
            section_card(
                "Resumen financiero",
                [
                    ft.Text(
                        f"Gastos del mes: {money(metrics.get('gastos_mes', 0))}",
                        size=14,
                    ),
                    ft.Text(
                        "La utilidad estimada se calcula como ventas del mes menos gastos del mes.",
                        size=12,
                        color=AppTheme.TEXT_MUTED,
                    ),
                ],
            ),
            section_card("Productos más vendidos", top_controls),
        ]

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
