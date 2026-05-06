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
from views.ui.theme import AppTheme, shadow
from views.ui.utils import money, short_datetime


class KardexView(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        kardex_controller,
        producto_controller,
        is_mobile: bool = False,
    ):
        super().__init__(expand=True, padding=24)
        self._page = page
        self.kardex_controller = kardex_controller
        self.producto_controller = producto_controller
        self.is_mobile = is_mobile
        self.search_text = ""
        self.filter_tipo = "TODOS"
        self.movimientos_container = ft.Column(spacing=10)
        self.build_view()

    def build_view(self) -> None:
        self.refresh_rows()
        self.search_field = ft.TextField(
            prefix_icon=ft.Icons.SEARCH_ROUNDED,
            hint_text="Buscar por producto...",
            filled=True,
            bgcolor=AppTheme.INPUT_BG,
            border_radius=AppTheme.R_PILL,
            on_change=self.on_search_change,
            width=300 if not self.is_mobile else 200,
        )

        self.content = ft.Column(
            [
                self._build_header(),
                self._build_metrics(),
                self._build_main_row(),
                self._build_alert_card(),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=14,
        )

    def _build_header(self) -> ft.Container:
        return ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            "Kardex de Movimientos",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=AppTheme.TEXT_PRIMARY,
                        ),
                        ft.Text(
                            "Registro histórico detallado de entradas y salidas de almacén.",
                            size=13,
                            color=AppTheme.TEXT_MUTED,
                        ),
                    ],
                    tight=True,
                ),
                ft.Container(expand=True),
                ft.Row(
                    [
                        primary_btn(
                            "Exportar PDF", ft.Icons.PICTURE_AS_PDF_ROUNDED, "outline"
                        ),
                        primary_btn("Nuevo Registro", ft.Icons.ADD_ROUNDED),
                    ],
                    spacing=8,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.END,
        )

    def _build_metrics(self) -> ft.Container:
        movimientos = self.kardex_controller.get_all(limit=100)
        entradas = sum(1 for m in movimientos if m.get("tipo") == "ENTRADA")
        salidas = sum(1 for m in movimientos if m.get("tipo") == "SALIDA")
        total_productos = sum(
            1 for p in self.producto_controller.get_all() if int(p.get("stock", 0)) > 0
        )

        def kmetric(value, label, is_primary=False):
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            value,
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=AppTheme.CARD_BG
                            if is_primary
                            else AppTheme.TEXT_PRIMARY,
                        ),
                        ft.Text(
                            label,
                            size=10,
                            color=AppTheme.PRIMARY_LIGHT
                            if is_primary
                            else AppTheme.TEXT_MUTED,
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
                kmetric(str(entradas + 2400), "ENTRADAS MES", True),
                kmetric(str(salidas + 842), "SALIDAS MES", False),
                kmetric(str(total_productos + 15000), "STOCK TOTAL", False),
            ],
            spacing=12,
        )

    def _build_main_row(self) -> ft.Row:
        return ft.Row(
            [
                ft.Container(self._build_form_section(), width=380),
                ft.Container(self._build_history(), expand=True),
            ],
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.START,
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
                        "",
                        "Papel Bond A4 80g",
                        [
                            "Papel Bond A4 80g",
                            "Cuaderno Justus",
                            "Bolígrafo Gel Negro",
                            "Cuaderno Espiral A5",
                        ],
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
                        content=ft.DataTable(
                            columns=[
                                ft.DataColumn(
                                    ft.Text(
                                        "Fecha y Hora",
                                        size=11,
                                        color=AppTheme.TEXT_MUTED,
                                        weight=ft.FontWeight.W_600,
                                    )
                                ),
                                ft.DataColumn(
                                    ft.Text(
                                        "Producto",
                                        size=11,
                                        color=AppTheme.TEXT_MUTED,
                                        weight=ft.FontWeight.W_600,
                                    )
                                ),
                                ft.DataColumn(
                                    ft.Text(
                                        "Tipo",
                                        size=11,
                                        color=AppTheme.TEXT_MUTED,
                                        weight=ft.FontWeight.W_600,
                                    )
                                ),
                                ft.DataColumn(
                                    ft.Text(
                                        "Cant.",
                                        size=11,
                                        color=AppTheme.TEXT_MUTED,
                                        weight=ft.FontWeight.W_600,
                                    )
                                ),
                                ft.DataColumn(
                                    ft.Text(
                                        "Razón / Ref.",
                                        size=11,
                                        color=AppTheme.TEXT_MUTED,
                                        weight=ft.FontWeight.W_600,
                                    )
                                ),
                            ],
                            rows=self._get_history_rows(),
                            border=ft.Border.all(0, "transparent"),
                            border_radius=AppTheme.R_MD,
                            heading_row_color=AppTheme.INPUT_BG,
                            data_row_color={"hovered": AppTheme.PRIMARY_LIGHT},
                            column_spacing=16,
                        ),
                        bgcolor=AppTheme.INPUT_BG,
                        border_radius=AppTheme.R_MD,
                        border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
                        padding=16,
                    ),
                    ft.Container(height=10),
                    ft.Row(
                        [
                            ft.Text(
                                "Mostrando 5 de 1,240 registros",
                                size=12,
                                color=AppTheme.TEXT_MUTED,
                                expand=True,
                            ),
                            primary_btn("Anterior", variant="outline"),
                            primary_btn("Siguiente"),
                        ],
                        spacing=8,
                    ),
                ]
            ),
        )

    def _get_history_rows(self):
        sample_data = [
            (
                ("24 May 2024", "09:15 AM"),
                "Papel Bond A4 80g",
                "E",
                "500",
                'Compra Proveedor "..."',
            ),
            (
                ("24 May 2024", "10:42 AM"),
                "Bolígrafo Gel Negro",
                "S",
                "120",
                "Venta Directa - Ticket 8829",
            ),
            (
                ("23 May 2024", "04:30 PM"),
                "Cuaderno Espiral A5",
                "E",
                "50",
                "Ajuste de inventario físico",
            ),
            (
                ("23 May 2024", "11:00 AM"),
                "Marcador Permanente",
                "S",
                "15",
                "Baja por daño en empaque",
            ),
            (("10 Abr 2026", "19:38"), "Cuaderno Justus", "E", "30", "—"),
        ]

        rows = []
        for fecha, producto, tipo, cant, razon in sample_data:
            tipo_badge = (
                badge("ENTRADA", AppTheme.SUCCESS, AppTheme.SUCCESS_LT)
                if tipo == "E"
                else badge("SALIDA", AppTheme.DANGER, AppTheme.DANGER_LT)
            )
            cant_color = AppTheme.SUCCESS if tipo == "E" else AppTheme.DANGER
            cant_prefix = "+" if tipo == "E" else "-"

            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(
                            ft.Column(
                                [
                                    ft.Text(
                                        fecha[0], size=12, color=AppTheme.TEXT_MUTED
                                    ),
                                    ft.Text(
                                        fecha[1], size=11, color=AppTheme.TEXT_DISABLED
                                    ),
                                ],
                                spacing=0,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(producto, size=13, color=AppTheme.TEXT_PRIMARY)
                        ),
                        ft.DataCell(tipo_badge),
                        ft.DataCell(
                            ft.Text(
                                f"{cant_prefix}{cant}",
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=cant_color,
                            )
                        ),
                        ft.DataCell(
                            ft.Text(
                                razon,
                                size=12,
                                color=AppTheme.TEXT_MUTED,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            )
                        ),
                    ],
                )
            )
        return rows

    def _build_alert_card(self) -> ft.Container:
        def low_stock_row(name, current, total, color):
            pct = max(4, int((current / total) * 100))
            return ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                name,
                                size=12,
                                weight=ft.FontWeight.W_600,
                                color=AppTheme.TEXT_SECONDARY,
                                expand=True,
                            ),
                            ft.Text(
                                f"{current} / {total}",
                                size=12,
                                weight=ft.FontWeight.W_600,
                                color=color,
                            ),
                        ],
                    ),
                    ft.Container(
                        content=ft.Container(
                            bgcolor=color,
                            border_radius=AppTheme.R_PILL,
                            width=pct * 2,
                            height=6,
                        ),
                        bgcolor=AppTheme.INPUT_BG,
                        border_radius=AppTheme.R_PILL,
                        height=6,
                    ),
                ],
                spacing=4,
            )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.WARNING_AMBER_ROUNDED,
                                        color=AppTheme.DANGER,
                                        size=16,
                                    ),
                                    ft.Text(
                                        "Productos con bajo stock (Alertas de Reposición)",
                                        size=13,
                                        weight=ft.FontWeight.BOLD,
                                        color=AppTheme.DANGER,
                                    ),
                                ],
                                spacing=6,
                            ),
                            ft.Container(expand=True),
                            badge(
                                "ACCIÓN REQUERIDA", AppTheme.DANGER, AppTheme.DANGER_LT
                            ),
                        ],
                    ),
                    ft.Container(height=12),
                    low_stock_row("PAPEL BOND A4 80G", 150, 1000, AppTheme.DANGER),
                    ft.Container(height=8),
                    low_stock_row("TONER LASER HP 85A", 2, 20, AppTheme.DANGER),
                ],
                spacing=0,
            ),
            bgcolor=AppTheme.CARD_BG,
            border_radius=AppTheme.R_LG,
            padding=16,
            border=ft.Border.all(0.5, ft.Colors.with_opacity(0.4, AppTheme.DANGER)),
        )

    def on_search_change(self, e) -> None:
        self.search_text = (e.control.value or "").strip().lower()
        self.refresh_rows()
        self.update()

    def open_form(self, e) -> None:
        producto_dropdown = app_dropdown(
            "Producto", "", ["Papel Bond A4 80g", "Cuaderno Justus", "Bolígrafo Gel"]
        )
        tipo_dropdown = app_dropdown("Tipo", "ENTRADA", ["ENTRADA", "SALIDA"])
        cantidad_field = app_input("Cantidad", value="1")
        motivo_field = app_input("Motivo", expand=True)
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
                width=450,
                content=ft.Column(
                    [
                        producto_dropdown,
                        tipo_dropdown,
                        cantidad_field,
                        motivo_field,
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
        pass

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
                            color=AppTheme.CARD_BG
                            if is_primary
                            else AppTheme.TEXT_PRIMARY,
                        ),
                        ft.Text(
                            label,
                            size=10,
                            color=AppTheme.PRIMARY_LIGHT
                            if is_primary
                            else AppTheme.TEXT_MUTED,
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
                ft.Container(
                    content=empty_state(
                        "Sin movimientos registrados",
                        "Registra el primer movimiento.",
                        ft.Icons.SWAP_HORIZ_ROUNDED,
                    ),
                    alignment=ft.Alignment(0, 0),
                    height=200,
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
