from __future__ import annotations

import flet as ft

from views.components.ui import empty_state, section_card
from views.ui.theme import AppTheme
from views.ui.utils import money, parse_float, parse_int, short_datetime


class KardexView(ft.Column):
    def __init__(self, page: ft.Page, kardex_controller, producto_controller, is_mobile: bool = False):
        super().__init__(expand=True, scroll=ft.ScrollMode.AUTO, spacing=20)
        self._page = page
        self.kardex_controller = kardex_controller
        self.producto_controller = producto_controller
        self.is_mobile = is_mobile
        self.padding = 20
        self.rows_container = ft.Column(spacing=10)
        self.build_view()

    def build_view(self) -> None:
        if not self.is_mobile:
            self.product_dropdown = ft.Dropdown(
                label="Producto", options=self._product_options(), expand=True
            )
            self.tipo_dropdown = ft.Dropdown(
                label="Tipo",
                value="ENTRADA",
                width=160,
                options=[ft.dropdown.Option("ENTRADA"), ft.dropdown.Option("SALIDA")],
            )
            self.cantidad_field = ft.TextField(label="Cantidad", value="1", width=120)
            self.precio_field = ft.TextField(
                label="Precio unitario", value="0", width=140
            )
            self.motivo_field = ft.TextField(label="Motivo", expand=True)
            self.documento_field = ft.TextField(label="Documento ref.", width=180)
            self.error_text = ft.Text("", color=AppTheme.DANGER, visible=False)

        self.refresh_rows()

        if self.is_mobile:
            self.controls = [
                ft.Text("Kardex", size=28, weight=ft.FontWeight.BOLD),
                section_card(
                    "Movimientos recientes",
                    [self.rows_container],
                    "Solo visualización de movimientos.",
                ),
            ]
        else:
            self.controls = [
                ft.Text("Kardex", size=28, weight=ft.FontWeight.BOLD),
                section_card(
                    "Registrar movimiento",
                    [
                        ft.ResponsiveRow(
                            [
                                ft.Column(
                                    [self.product_dropdown], col={"sm": 12, "md": 5}
                                ),
                                ft.Column(
                                    [self.tipo_dropdown], col={"sm": 12, "md": 2}
                                ),
                                ft.Column(
                                    [self.cantidad_field], col={"sm": 6, "md": 2}
                                ),
                                ft.Column([self.precio_field], col={"sm": 6, "md": 3}),
                                ft.Column([self.motivo_field], col={"sm": 12, "md": 6}),
                                ft.Column(
                                    [self.documento_field], col={"sm": 12, "md": 3}
                                ),
                                ft.Column(
                                    [
                                        ft.FilledButton(
                                            "Registrar",
                                            icon=ft.Icons.SAVE,
                                            on_click=self.save_movimiento,
                                        )
                                    ],
                                    col={"sm": 12, "md": 3},
                                ),
                            ],
                            run_spacing=10,
                        ),
                        self.error_text,
                    ],
                    "Entradas y salidas conectadas al stock actual.",
                ),
                section_card(
                    "Movimientos recientes",
                    [self.rows_container],
                    "Ultimos registros del inventario.",
                ),
            ]

    def _product_options(self) -> list[ft.dropdown.Option]:
        return [
            ft.dropdown.Option(
                str(producto["id"]), f"{producto['codigo']} - {producto['nombre']}"
            )
            for producto in self.producto_controller.get_all()
        ]

    def refresh_rows(self) -> None:
        movimientos = self.kardex_controller.get_all(limit=50)
        if not movimientos:
            self.rows_container.controls = [
                empty_state(
                    "Sin movimientos registrados",
                    "Cuando ingrese o salga mercaderia se mostrará aquí.",
                    ft.Icons.SWAP_HORIZ_ROUNDED,
                )
            ]
            return

        controls: list[ft.Control] = []
        for movimiento in movimientos:
            tipo_color = (
                AppTheme.SUCCESS if movimiento["tipo"] == "ENTRADA" else AppTheme.DANGER
            )
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
                                                    movimiento["producto_nombre"],
                                                    weight=ft.FontWeight.BOLD,
                                                    size=16,
                                                ),
                                                ft.Text(
                                                    f"{movimiento['codigo']} | {short_datetime(movimiento.get('fecha'))}",
                                                    size=12,
                                                    color=AppTheme.TEXT_SECONDARY,
                                                ),
                                            ],
                                            expand=True,
                                        ),
                                        ft.Container(
                                            padding=ft.Padding.symmetric(
                                                horizontal=12, vertical=8
                                            ),
                                            border_radius=16,
                                            bgcolor=ft.Colors.with_opacity(
                                                0.12, tipo_color
                                            ),
                                            content=ft.Text(
                                                movimiento["tipo"],
                                                color=tipo_color,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                        ),
                                    ]
                                ),
                                ft.Row(
                                    [
                                        ft.Text(f"Cantidad: {movimiento['cantidad']}"),
                                        ft.Text(
                                            f"P.Unit: {money(float(movimiento.get('precio_unitario') or 0))}"
                                        ),
                                        ft.Text(
                                            f"Total: {money(float(movimiento.get('total') or 0))}"
                                        ),
                                        ft.Text(
                                            f"Saldo: {movimiento.get('saldo_stock', '-')}",
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                    ],
                                    wrap=True,
                                    spacing=18,
                                ),
                                ft.Text(
                                    f"Motivo: {movimiento.get('motivo') or '-'} | Ref: {movimiento.get('documento_ref') or '-'}",
                                    size=12,
                                    color=AppTheme.TEXT_SECONDARY,
                                ),
                            ],
                            spacing=10,
                        ),
                    ),
                )
            )
        self.rows_container.controls = controls

    def save_movimiento(self, e) -> None:
        try:
            self.kardex_controller.registrar_movimiento(
                producto_id=int(self.product_dropdown.value),
                tipo=self.tipo_dropdown.value,
                cantidad=parse_int(self.cantidad_field.value, 1),
                precio_unitario=parse_float(self.precio_field.value),
                motivo=(self.motivo_field.value or "").strip(),
                documento_ref=(self.documento_field.value or "").strip(),
            )
            self.error_text.visible = False
            self.product_dropdown.options = self._product_options()
            self.refresh_rows()
            self._page.snack_bar = ft.SnackBar(
                ft.Text("Movimiento registrado correctamente.")
            )
            self._page.snack_bar.open = True
            self._page.update()
            self.update()
        except Exception as exc:
            self.error_text.value = f"No se pudo registrar: {exc}"
            self.error_text.visible = True
            self.update()
