from __future__ import annotations

import flet as ft

from app.views.components.ui import StatCard, empty_state, section_card
from app.views.ui.theme import AppTheme
from app.views.ui.utils import money


class ReportesView(ft.Column):
    def __init__(self, db):
        super().__init__(expand=True, scroll=ft.ScrollMode.AUTO, spacing=20)
        self.db = db
        self.padding = 20
        self.build_view()

    def build_view(self) -> None:
        metrics = self.db.get_report_metrics()
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
