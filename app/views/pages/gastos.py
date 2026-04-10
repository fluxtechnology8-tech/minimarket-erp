from __future__ import annotations

import flet as ft

from app.views.components.ui import empty_state, section_card
from app.views.ui.theme import AppTheme
from app.views.ui.utils import money, parse_float, short_datetime


class GastosView(ft.Column):
    def __init__(self, page: ft.Page, db, is_mobile: bool = False):
        super().__init__(expand=True, scroll=ft.ScrollMode.AUTO, spacing=20)
        self._page = page
        self.db = db
        self.is_mobile = is_mobile
        self.padding = 20
        self.gastos_container = ft.Column(spacing=10)
        self.build_view()

    def build_view(self) -> None:
        if not self.is_mobile:
            self.concepto = ft.TextField(label="Concepto", expand=True)
            self.monto = ft.TextField(label="Monto", width=180, value="0")
            self.categoria = ft.TextField(label="Categoria", width=180)
            self.observaciones = ft.TextField(
                label="Observaciones", multiline=True, min_lines=2, max_lines=4
            )

        self.refresh_gastos()

        if self.is_mobile:
            self.controls = [
                ft.Text("Gastos", size=28, weight=ft.FontWeight.BOLD),
                section_card(
                    "Ultimos gastos",
                    [self.gastos_container],
                    "Solo visualización de gastos.",
                ),
            ]
        else:
            self.controls = [
                ft.Text("Gastos", size=28, weight=ft.FontWeight.BOLD),
                section_card(
                    "Registrar gasto",
                    [
                        ft.ResponsiveRow(
                            [
                                ft.Column([self.concepto], col={"sm": 12, "md": 5}),
                                ft.Column([self.monto], col={"sm": 6, "md": 2}),
                                ft.Column([self.categoria], col={"sm": 6, "md": 2}),
                                ft.Column(
                                    [
                                        ft.FilledButton(
                                            "Guardar",
                                            icon=ft.Icons.SAVE,
                                            on_click=self.save_gasto,
                                        )
                                    ],
                                    col={"sm": 12, "md": 3},
                                ),
                            ],
                            run_spacing=10,
                        ),
                        self.observaciones,
                    ],
                    "Control basico de egresos del negocio.",
                ),
                section_card(
                    "Ultimos gastos",
                    [self.gastos_container],
                    "Historial reciente para seguimiento rapido.",
                ),
            ]

    def refresh_gastos(self) -> None:
        gastos = self.db.get_gastos(limit=30)
        if not gastos:
            self.gastos_container.controls = [
                empty_state(
                    "Sin gastos registrados",
                    "Agrega un gasto para llevar el control del mes.",
                    ft.Icons.PAYMENTS_OUTLINED,
                )
            ]
            return

        controls: list[ft.Control] = []
        for gasto in gastos:
            controls.append(
                ft.Card(
                    elevation=1,
                    content=ft.Container(
                        padding=16,
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Column(
                                            [
                                                ft.Text(
                                                    gasto["concepto"],
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                                ft.Text(
                                                    f"{gasto.get('categoria') or 'Sin categoria'} | {short_datetime(gasto.get('fecha'))}",
                                                    size=12,
                                                    color=AppTheme.TEXT_SECONDARY,
                                                ),
                                            ],
                                            expand=True,
                                        ),
                                        ft.Text(
                                            money(float(gasto.get("monto") or 0)),
                                            color=AppTheme.DANGER,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                    ]
                                ),
                                ft.Text(
                                    gasto.get("observaciones") or "Sin observaciones.",
                                    size=12,
                                    color=AppTheme.TEXT_SECONDARY,
                                ),
                            ],
                            spacing=10,
                        ),
                    ),
                )
            )
        self.gastos_container.controls = controls

    def save_gasto(self, e) -> None:
        try:
            self.db.add_gasto(
                {
                    "concepto": (self.concepto.value or "").strip(),
                    "monto": parse_float(self.monto.value),
                    "categoria": (self.categoria.value or "").strip(),
                    "observaciones": (self.observaciones.value or "").strip(),
                }
            )
            self.concepto.value = ""
            self.monto.value = "0"
            self.categoria.value = ""
            self.observaciones.value = ""
            self.refresh_gastos()
            self.update()
            self._page.snack_bar = ft.SnackBar(
                ft.Text("Gasto registrado correctamente.")
            )
            self._page.snack_bar.open = True
            self._page.update()
        except Exception as exc:
            self._page.snack_bar = ft.SnackBar(
                ft.Text(f"No se pudo guardar el gasto: {exc}")
            )
            self._page.snack_bar.open = True
            self._page.update()
