from __future__ import annotations

import flet as ft

from views.components.ui import StatCard, empty_state, section_card
from views.ui.theme import AppTheme
from views.ui.utils import money


class ReportesView(ft.Column):
    def __init__(self, page: ft.Page, controller):
        super().__init__(expand=True, scroll=ft.ScrollMode.AUTO, spacing=20)
        self._page = page
        self.controller = controller
        self.padding = 20
        self.build_view()

    def build_view(self) -> None:
        metrics = self.controller.get_report_metrics()
        if metrics["top_productos"]:
            top_controls = [
                ft.ListTile(
                    leading=ft.Icon(
                        ft.Icons.STAR_BORDER_ROUNDED, color=AppTheme.PRIMARY
                    ),
                    title=ft.Text(item["nombre"]),
                    subtitle=ft.Text(
                        f"Cantidad vendida: {item.get('cantidad_vendida', 0)} | Ingreso: {money(float(item.get('total_vendido') or 0))}"
                    ),
                )
                for item in metrics["top_productos"]
            ]
        else:
            top_controls = [
                empty_state(
                    "Aun no hay ventas para analizar",
                    "Cuando se registren boletas aparecerán los productos mas vendidos.",
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
                                    self._build_pdf_card(
                                        "Inventario",
                                        "Listado completo de productos en stock",
                                        ft.Icons.INVENTORY_2,
                                        self.generate_inventario_pdf,
                                    )
                                ],
                                col={"sm": 12, "md": 4},
                            ),
                            ft.Column(
                                [
                                    self._build_pdf_card(
                                        "Ventas",
                                        "Reporte de ventas del mes",
                                        ft.Icons.RECEIPT_LONG,
                                        self.generate_ventas_pdf,
                                    )
                                ],
                                col={"sm": 12, "md": 4},
                            ),
                            ft.Column(
                                [
                                    self._build_pdf_card(
                                        "Gastos",
                                        "Resumen de gastos del mes",
                                        ft.Icons.PAYMENTS,
                                        self.generate_gastos_pdf,
                                    )
                                ],
                                col={"sm": 12, "md": 4},
                            ),
                            ft.Column(
                                [
                                    self._build_pdf_card(
                                        "Movimientos",
                                        "Historial de entradas y salidas",
                                        ft.Icons.SWAP_HORIZ,
                                        self.generate_movimientos_pdf,
                                    )
                                ],
                                col={"sm": 12, "md": 4},
                            ),
                            ft.Column(
                                [
                                    self._build_pdf_card(
                                        "Resumen general",
                                        "Estado financiero completo",
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
                "Exporta los datos en formato PDF para imprimir o compartir.",
            ),
            ft.ResponsiveRow(
                [
                    ft.Column(
                        [
                            StatCard(
                                "Unidades en stock",
                                str(metrics["total_stock"]),
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
                                money(metrics["valor_inventario"]),
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
                                money(metrics["ventas_mes"]),
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
                                money(metrics["utilidad_estimada"]),
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
                    ft.Text(f"Gastos del mes: {money(metrics['gastos_mes'])}", size=14),
                    ft.Text(
                        "La utilidad estimada se calcula como ventas del mes menos gastos del mes.",
                        size=12,
                        color=AppTheme.TEXT_SECONDARY,
                    ),
                ],
            ),
            section_card("Productos mas vendidos", top_controls),
        ]

    def _build_pdf_card(
        self, title: str, subtitle: str, icon: ft.Icons, on_click
    ) -> ft.Container:
        return ft.Container(
            padding=16,
            border_radius=16,
            bgcolor=AppTheme.SURFACE_CONTAINER_LOW,
            content=ft.Column(
                [
                    ft.Container(
                        padding=12,
                        bgcolor=AppTheme.PRIMARY_CONTAINER,
                        border_radius=12,
                        content=ft.Icon(icon, color=AppTheme.PRIMARY, size=28),
                    ),
                    ft.Text(
                        title,
                        size=14,
                        weight=ft.FontWeight.W_600,
                        color=AppTheme.TEXT_PRIMARY,
                    ),
                    ft.Text(
                        subtitle,
                        size=11,
                        color=AppTheme.TEXT_SECONDARY,
                    ),
                ],
                spacing=8,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            on_click=on_click,
        )

    def generate_inventario_pdf(self, e) -> None:
        self._show_pdf_message("Generando reporte de inventario...")

    def generate_ventas_pdf(self, e) -> None:
        self._show_pdf_message("Generando reporte de ventas...")

    def generate_gastos_pdf(self, e) -> None:
        self._show_pdf_message("Generando reporte de gastos...")

    def generate_movimientos_pdf(self, e) -> None:
        self._show_pdf_message("Generando reporte de movimientos...")

    def generate_resumen_pdf(self, e) -> None:
        self._show_pdf_message("Generando resumen general...")

    def _show_pdf_message(self, message: str) -> None:
        if hasattr(self, "_page"):
            self._page.snack_bar = ft.SnackBar(ft.Text(message))
            self._page.snack_bar.open = True
            self._page.update()
