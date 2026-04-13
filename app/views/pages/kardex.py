from __future__ import annotations

import flet as ft
from views.components.ui import (
    empty_state,
    section_card,
    card,
    app_input,
    app_dropdown,
    primary_btn,
    badge,
)
from views.ui.theme import AppTheme
from views.ui.utils import money, short_datetime


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
        self.padding = 24
        self.search_text = ""
        self.filter_tipo = "TODOS"
        self.movimientos_container = ft.Column(spacing=10)
        self.build_view()

    def build_view(self) -> None:
        self.refresh_rows()
        self.search_field = ft.TextField(
            prefix_icon=ft.Icons.SEARCH_ROUNDED,
            hint_text="Buscar por producto o código",
            filled=True,
            bgcolor=AppTheme.INPUT_BG,
            border_radius=AppTheme.R_PILL,
            on_change=self.on_search_change,
            width=300 if not self.is_mobile else 200,
        )

        if self.is_mobile:
            self.controls = [
                ft.Text("Movimientos", size=28, weight=ft.FontWeight.BOLD),
                self._build_filters(),
                section_card(
                    "Lista de movimientos",
                    [self.movimientos_container],
                    "Solo visualización.",
                ),
            ]
        else:
            self.controls = [
                ft.Text("Kardex", size=28, weight=ft.FontWeight.BOLD),
                self._build_metrics(),
                self._build_form_section(),
                self._build_filters(),
                self._build_history(),
            ]

    def _build_metrics(self) -> ft.Container:
        movimientos = self.kardex_controller.get_all(limit=100)
        entradas = sum(1 for m in movimientos if m.get("tipo") == "ENTRADA")
        salidas = sum(1 for m in movimientos if m.get("tipo") == "SALIDA")

        def kmetric(value, label, is_primary=False):
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            value,
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color="#FFFFFF" if is_primary else AppTheme.TEXT_PRIMARY,
                        ),
                        ft.Text(
                            label,
                            size=10,
                            color="#FFFFFF99" if is_primary else AppTheme.TEXT_MUTED,
                            weight=ft.FontWeight.W_600,
                        ),
                    ],
                    spacing=3,
                ),
                bgcolor=AppTheme.PRIMARY if is_primary else AppTheme.CARD_BG,
                border_radius=AppTheme.R_LG,
                padding=16,
                border=ft.Border.all(
                    0.5, AppTheme.CARD_BORDER if not is_primary else "transparent"
                ),
                expand=1,
            )

        return ft.Row(
            [
                kmetric(str(entradas), "ENTRADAS MES", True),
                kmetric(str(salidas), "SALIDAS MES", False),
            ],
            spacing=12,
        )

    def _build_form_section(self) -> ft.Container:
        return card(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.EDIT_NOTE_ROUNDED,
                                color=AppTheme.PRIMARY,
                                size=18,
                            ),
                            ft.Text(
                                "Registrar Movimiento",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=12),
                    ft.Text(
                        "PRODUCTO",
                        size=10,
                        color=AppTheme.TEXT_MUTED,
                        weight=ft.FontWeight.W_600,
                    ),
                    ft.Container(height=4),
                    app_dropdown(
                        "", "Seleccionar producto", ["Producto 1", "Producto 2"]
                    ),
                    ft.Container(height=10),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "TIPO",
                                        size=10,
                                        color=AppTheme.TEXT_MUTED,
                                        weight=ft.FontWeight.W_600,
                                    ),
                                    ft.Container(height=4),
                                    ft.Row(
                                        controls=[
                                            self._build_tipo_btn("ENTRADA", True),
                                            self._build_tipo_btn("SALIDA", False),
                                        ],
                                        spacing=6,
                                    ),
                                ],
                                expand=True,
                            ),
                            ft.Container(
                                content=app_input(
                                    "CANTIDAD",
                                    value="0",
                                    keyboard_type=ft.KeyboardType.NUMBER,
                                    width=90,
                                )
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "MOTIVO / DOCUMENTO",
                        size=10,
                        color=AppTheme.TEXT_MUTED,
                        weight=ft.FontWeight.W_600,
                    ),
                    ft.Container(height=4),
                    ft.TextField(
                        hint_text="Ej: Compra según factura F-001...",
                        multiline=True,
                        min_lines=2,
                        max_lines=3,
                        border_radius=AppTheme.R_MD,
                        border_color=AppTheme.INPUT_BORDER,
                        focused_border_color=AppTheme.INPUT_FOCUSED,
                        fill_color=AppTheme.INPUT_BG,
                        filled=True,
                        content_padding=ft.padding.all(12),
                    ),
                    ft.Container(height=12),
                    primary_btn(
                        "Confirmar Registro",
                        ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                        on_click=self.open_form,
                        expand=True,
                    ),
                ],
                spacing=0,
            ),
        )

    def _build_tipo_btn(self, tipo, is_active):
        if tipo == "ENTRADA":
            return ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.ADD_CIRCLE_ROUNDED, color=AppTheme.SUCCESS, size=14
                        ),
                        ft.Text(
                            "ENTRADA",
                            size=12,
                            weight=ft.FontWeight.W_700,
                            color=AppTheme.SUCCESS,
                        ),
                    ],
                    spacing=4,
                    tight=True,
                ),
                bgcolor=AppTheme.SUCCESS_LT if is_active else AppTheme.INPUT_BG,
                border=ft.Border.all(
                    1, AppTheme.SUCCESS if is_active else AppTheme.CARD_BORDER
                ),
                border_radius=AppTheme.R_MD,
                padding=ft.padding.symmetric(horizontal=14, vertical=7),
                expand=1,
                alignment=ft.Alignment(0, 0),
                ink=True,
            )
        else:
            return ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(
                            ft.Icons.REMOVE_CIRCLE_OUTLINED,
                            color=AppTheme.TEXT_MUTED,
                            size=14,
                        ),
                        ft.Text(
                            "SALIDA",
                            size=12,
                            weight=ft.FontWeight.W_600,
                            color=AppTheme.TEXT_MUTED,
                        ),
                    ],
                    spacing=4,
                    tight=True,
                ),
                bgcolor=AppTheme.INPUT_BG,
                border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
                border_radius=AppTheme.R_MD,
                padding=ft.padding.symmetric(horizontal=14, vertical=7),
                expand=1,
                alignment=ft.Alignment(0, 0),
                ink=True,
            )

    def _build_filters(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                [self.search_field, self._build_filter_dropdown()], spacing=10
            ),
            margin=ft.Margin.only(bottom=10),
        )

    def _build_filter_dropdown(self) -> ft.Row:
        return ft.Row(
            [
                ft.Container(
                    content=ft.Text("Todos", size=12),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                    border_radius=AppTheme.R_PILL,
                    bgcolor=AppTheme.PRIMARY
                    if self.filter_tipo == "TODOS"
                    else AppTheme.INPUT_BG,
                    on_click=lambda _: self._set_filter("TODOS"),
                ),
                ft.Container(
                    content=ft.Text("Entrada", size=12),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                    border_radius=AppTheme.R_PILL,
                    bgcolor=AppTheme.PRIMARY
                    if self.filter_tipo == "ENTRADA"
                    else AppTheme.INPUT_BG,
                    on_click=lambda _: self._set_filter("ENTRADA"),
                ),
                ft.Container(
                    content=ft.Text("Salida", size=12),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                    border_radius=AppTheme.R_PILL,
                    bgcolor=AppTheme.PRIMARY
                    if self.filter_tipo == "SALIDA"
                    else AppTheme.INPUT_BG,
                    on_click=lambda _: self._set_filter("SALIDA"),
                ),
            ],
            spacing=8,
        )

    def _build_history(self) -> ft.Container:
        return card(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Historial de Movimientos",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                            ft.Container(expand=True),
                            ft.Row(
                                controls=[
                                    primary_btn("Todos", variant="filled"),
                                    primary_btn("Entrada", variant="outline"),
                                    primary_btn("Salida", variant="outline"),
                                ],
                                spacing=6,
                            ),
                        ]
                    ),
                    ft.Container(height=10),
                    self.search_field,
                    ft.Container(height=10),
                    ft.Container(
                        content=self.movimientos_container,
                        bgcolor=AppTheme.INPUT_BG,
                        border_radius=AppTheme.R_MD,
                        border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
                        padding=16,
                    ),
                ]
            ),
        )

    def _set_filter(self, tipo) -> None:
        self.filter_tipo = tipo
        self.refresh_rows()
        self.update()

    def on_search_change(self, e) -> None:
        self.search_text = (e.control.value or "").strip().lower()
        self.refresh_rows()
        self.update()

    def get_filtered_movimientos(self):
        movimientos = self.kardex_controller.get_all(limit=100)
        if self.filter_tipo != "TODOS":
            movimientos = [m for m in movimientos if m.get("tipo") == self.filter_tipo]
        if not self.search_text:
            return movimientos
        return [
            m
            for m in movimientos
            if self.search_text in str(m.get("producto_nombre", "")).lower()
        ]

    def open_form(self, e) -> None:
        producto_dropdown = app_dropdown("Producto", "", ["Producto 1", "Producto 2"])
        tipo_dropdown = app_dropdown("Tipo", "ENTRADA", ["ENTRADA", "SALIDA"])
        cantidad_field = app_input("Cantidad", value="1")
        precio_field = app_input("Precio unitario", value="0")
        motivo_field = app_input("Motivo", expand=True)
        documento_field = app_input("Documento ref.")
        error_text = ft.Text("", color=AppTheme.DANGER, visible=False)

        def close_dialog(_):
            self._page.pop_dialog()

        def save_movimiento(_):
            try:
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

    def refresh_rows(self) -> None:
        movimientos = self.get_filtered_movimientos()
        if not movimientos:
            self.movimientos_container.controls = [
                empty_state(
                    "Sin movimientos registrados",
                    "Registra el primer movimiento.",
                    ft.Icons.SWAP_HORIZ_ROUNDED,
                )
            ]
            return
        self.movimientos_container.controls = [
            ft.Container(
                padding=12,
                border=ft.Border(bottom=ft.BorderSide(0.5, AppTheme.CARD_BORDER)),
                content=ft.Row(
                    [
                        ft.Column(
                            [ft.Text("Fecha", size=12, color=AppTheme.TEXT_MUTED)],
                            spacing=0,
                            tight=True,
                        ),
                        ft.Container(width=16),
                        ft.Text(
                            m.get("producto_nombre", "-"),
                            size=13,
                            color=AppTheme.TEXT_PRIMARY,
                            expand=True,
                        ),
                        badge(
                            m.get("tipo", "-"), AppTheme.SUCCESS, AppTheme.SUCCESS_LT
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            )
            for m in movimientos
        ]
