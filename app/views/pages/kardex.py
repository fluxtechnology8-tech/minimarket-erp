from __future__ import annotations

import flet as ft
import flet_datatable2 as ftd

from views.components.ui import empty_state, section_card
from views.ui.theme import AppTheme
from views.ui.utils import money, parse_float, parse_int, short_datetime


class KardexView(ft.Column):
    def __init__(
        self,
        page: ft.Page,
        kardex_controller,
        producto_controller,
        is_mobile: bool = False,
    ):
        super().__init__(expand=True, scroll=ft.ScrollMode.AUTO, spacing=20)
        self._page = page
        self.kardex_controller = kardex_controller
        self.producto_controller = producto_controller
        self.is_mobile = is_mobile
        self.padding = 20
        self.search_text = ""
        self.filter_tipo = "TODOS"
        self.data_table: ftd.DataTable2 | None = None
        self.movimientos_data = []
        self.build_view()

    def build_view(self) -> None:
        self.refresh_rows()

        self.search_field = ft.TextField(
            prefix_icon=ft.Icons.SEARCH,
            hint_text="Buscar por producto o código",
            filled=True,
            bgcolor=AppTheme.SURFACE_CONTAINER_LOWEST,
            border_radius=18,
            on_change=self.on_search_change,
            width=300 if not self.is_mobile else 200,
        )

        if self.is_mobile:
            self.controls = [
                ft.Text("Movimientos", size=28, weight=ft.FontWeight.BOLD),
                self._build_filters(),
                section_card(
                    "Lista de movimientos",
                    [self._build_table_container()],
                    "Solo visualización.",
                ),
            ]
        else:
            self.controls = [
                ft.Text("Movimientos", size=28, weight=ft.FontWeight.BOLD),
                section_card(
                    "Registrar movimiento",
                    [
                        ft.FilledButton(
                            "Registrar movimiento",
                            icon=ft.Icons.ADD,
                            on_click=self.open_form,
                        ),
                    ],
                    "Entradas y salidas conectadas al stock actual.",
                ),
                section_card(
                    "Lista de movimientos",
                    [
                        ft.Row(
                            [self.search_field, self._build_filter_dropdown()],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        self._build_table_container(),
                    ],
                    "Historial de movimientos del inventario.",
                ),
            ]

    def _build_filters(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                [self.search_field, self._build_filter_dropdown()],
                spacing=10,
            ),
            margin=ft.Margin.only(bottom=10),
        )

    def _build_filter_dropdown(self) -> ft.Row:
        return ft.Row(
            [
                ft.Container(
                    content=ft.Text("Todos", size=12),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                    border_radius=16,
                    bgcolor=AppTheme.PRIMARY
                    if self.filter_tipo == "TODOS"
                    else AppTheme.SURFACE_CONTAINER_LOW,
                    on_click=lambda _: self._set_filter("TODOS"),
                ),
                ft.Container(
                    content=ft.Text("Entrada", size=12),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                    border_radius=16,
                    bgcolor=AppTheme.PRIMARY
                    if self.filter_tipo == "ENTRADA"
                    else AppTheme.SURFACE_CONTAINER_LOW,
                    on_click=lambda _: self._set_filter("ENTRADA"),
                ),
                ft.Container(
                    content=ft.Text("Salida", size=12),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                    border_radius=16,
                    bgcolor=AppTheme.PRIMARY
                    if self.filter_tipo == "SALIDA"
                    else AppTheme.SURFACE_CONTAINER_LOW,
                    on_click=lambda _: self._set_filter("SALIDA"),
                ),
            ],
            spacing=8,
        )

    def _set_filter(self, tipo: str) -> None:
        self.filter_tipo = tipo
        self.refresh_rows()
        self.update()

    def _build_table_container(self) -> ft.Container:
        self.data_table = ftd.DataTable2(
            expand=True,
            heading_row_color=ft.Colors.SECONDARY_CONTAINER,
            horizontal_margin=12,
            min_width=600,
            columns=self._get_columns(),
            rows=self._get_rows(),
        )
        return ft.Container(
            content=self.data_table, height=400 if self.is_mobile else 500
        )

    def _get_columns(self) -> list[ftd.DataColumn2]:
        return [
            ftd.DataColumn2(
                label=ft.Text("Fecha", weight=ft.FontWeight.BOLD),
                size=ftd.DataColumnSize.M,
            ),
            ftd.DataColumn2(
                label=ft.Text("Producto", weight=ft.FontWeight.BOLD),
                size=ftd.DataColumnSize.L,
            ),
            ftd.DataColumn2(
                label=ft.Text("Tipo", weight=ft.FontWeight.BOLD),
                size=ftd.DataColumnSize.S,
            ),
            ftd.DataColumn2(
                label=ft.Text("Cant.", weight=ft.FontWeight.BOLD),
                numeric=True,
                size=ftd.DataColumnSize.S,
            ),
            ftd.DataColumn2(
                label=ft.Text("P.Unit", weight=ft.FontWeight.BOLD),
                numeric=True,
                size=ftd.DataColumnSize.S,
            ),
            ftd.DataColumn2(
                label=ft.Text("Total", weight=ft.FontWeight.BOLD),
                numeric=True,
                size=ftd.DataColumnSize.S,
            ),
            ftd.DataColumn2(
                label=ft.Text("Saldo", weight=ft.FontWeight.BOLD),
                numeric=True,
                size=ftd.DataColumnSize.S,
            ),
        ]

    def _get_rows(self) -> list[ftd.DataRow2]:
        return [
            ftd.DataRow2(
                specific_row_height=50,
                cells=[
                    ft.DataCell(
                        content=ft.Text(short_datetime(m.get("fecha")), size=12)
                    ),
                    ft.DataCell(
                        content=ft.Text(m.get("producto_nombre", "-"), size=12)
                    ),
                    ft.DataCell(
                        content=ft.Container(
                            content=ft.Text(
                                m["tipo"],
                                size=11,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE
                                if m["tipo"] == "ENTRADA"
                                else ft.Colors.WHITE,
                            ),
                            padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                            border_radius=8,
                            bgcolor=AppTheme.SUCCESS
                            if m["tipo"] == "ENTRADA"
                            else AppTheme.DANGER,
                        )
                    ),
                    ft.DataCell(content=ft.Text(str(m["cantidad"]), size=12)),
                    ft.DataCell(
                        content=ft.Text(
                            money(float(m.get("precio_unitario") or 0)), size=12
                        )
                    ),
                    ft.DataCell(
                        content=ft.Text(money(float(m.get("total") or 0)), size=12)
                    ),
                    ft.DataCell(
                        content=ft.Text(
                            str(m.get("saldo_stock", "-")),
                            size=12,
                            weight=ft.FontWeight.BOLD,
                        )
                    ),
                ],
            )
            for m in self.movimientos_data
        ]

    def on_search_change(self, e) -> None:
        self.search_text = (e.control.value or "").strip().lower()
        self.refresh_rows()
        self.update()

    def on_filter_change(self, e) -> None:
        self.filter_tipo = e.control.value
        self.refresh_rows()
        self.update()

    def get_filtered_movimientos(self) -> list[dict]:
        movimientos = self.kardex_controller.get_all(limit=100)

        if self.filter_tipo != "TODOS":
            movimientos = [m for m in movimientos if m["tipo"] == self.filter_tipo]

        if not self.search_text:
            return movimientos

        return [
            m
            for m in movimientos
            if self.search_text in str(m.get("producto_nombre", "")).lower()
            or self.search_text in str(m.get("codigo", "")).lower()
        ]

    def open_form(self, e) -> None:
        self._product_options_cache = self._product_options()

        producto_dropdown = ft.Dropdown(
            label="Producto",
            options=self._product_options_cache,
            expand=True,
            autofocus=True,
        )
        tipo_dropdown = ft.Dropdown(
            label="Tipo",
            value="ENTRADA",
            options=[ft.dropdown.Option("ENTRADA"), ft.dropdown.Option("SALIDA")],
        )
        cantidad_field = ft.TextField(label="Cantidad", value="1")
        precio_field = ft.TextField(label="Precio unitario", value="0")
        motivo_field = ft.TextField(label="Motivo", expand=True)
        documento_field = ft.TextField(label="Documento ref.")
        error_text = ft.Text("", color=AppTheme.DANGER, visible=False)

        def close_dialog(_):
            self._page.pop_dialog()

        def save_movimiento(_):
            try:
                self.kardex_controller.registrar_movimiento(
                    producto_id=int(producto_dropdown.value),
                    tipo=tipo_dropdown.value,
                    cantidad=parse_int(cantidad_field.value, 1),
                    precio_unitario=parse_float(precio_field.value),
                    motivo=(motivo_field.value or "").strip(),
                    documento_ref=(documento_field.value or "").strip(),
                )
                self._page.pop_dialog()
                self.refresh_rows()
                self.update()
                self._page.snack_bar = ft.SnackBar(
                    ft.Text("Movimiento registrado correctamente.")
                )
                self._page.snack_bar.open = True
                self._page.update()
            except Exception as exc:
                error_text.value = f"No se pudo registrar: {exc}"
                error_text.visible = True
                self._page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nuevo movimiento"),
            content=ft.Container(
                width=500,
                content=ft.Column(
                    [
                        producto_dropdown,
                        ft.ResponsiveRow(
                            [
                                ft.Column([tipo_dropdown], col={"sm": 12, "md": 6}),
                                ft.Column([cantidad_field], col={"sm": 6, "md": 3}),
                                ft.Column([precio_field], col={"sm": 6, "md": 3}),
                            ],
                            run_spacing=10,
                        ),
                        ft.ResponsiveRow(
                            [
                                ft.Column([motivo_field], col={"sm": 12, "md": 9}),
                                ft.Column([documento_field], col={"sm": 12, "md": 3}),
                            ],
                            run_spacing=10,
                        ),
                        error_text,
                    ],
                    tight=True,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.FilledButton("Aceptar", on_click=save_movimiento),
            ],
        )
        self._page.show_dialog(dialog)

    def _product_options(self) -> list[ft.dropdown.Option]:
        return [
            ft.dropdown.Option(
                str(producto["id"]), f"{producto['codigo']} - {producto['nombre']}"
            )
            for producto in self.producto_controller.get_all()
        ]

    def refresh_rows(self) -> None:
        self.movimientos_data = self.get_filtered_movimientos()

        if not self.movimientos_data:
            self.movimientos_data = []

        if self.data_table:
            self.data_table.rows = self._get_rows()
            self.data_table.update()
