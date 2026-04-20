from __future__ import annotations

import flet as ft

from views.components.ui import (
    empty_state,
    section_card,
    card,
    app_input,
    app_dropdown,
    searchbar,
    primary_btn,
    badge,
)
from views.ui.theme import AppTheme, shadow
from views.ui.utils import money, parse_float, short_datetime


class GastosView(ft.Container):
    def __init__(self, page: ft.Page, controller, is_mobile: bool = False):
        super().__init__(expand=True, padding=24)
        self._page = page
        self.controller = controller
        self.is_mobile = is_mobile
        self.search_text = ""
        self.filter_categoria = "TODOS"
        self.gastos_container = ft.Column(spacing=10)
        self.build_view()

    def build_view(self) -> None:
        self.refresh_gastos()

        self.search_field = ft.TextField(
            prefix_icon=ft.Icons.SEARCH_ROUNDED,
            hint_text="Buscar por concepto",
            filled=True,
            bgcolor=AppTheme.INPUT_BG,
            border_radius=AppTheme.R_PILL,
            on_change=self.on_search_change,
            width=250 if not self.is_mobile else 180,
        )

        self.content = ft.Column(
            [
                self._build_header(),
                self._build_metrics_row(),
                self._build_main_row(),
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
                            "Libro de Gastos",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=AppTheme.TEXT_PRIMARY,
                        ),
                        ft.Text(
                            "Control de egresos y presupuesto de suministros.",
                            size=13,
                            color=AppTheme.TEXT_MUTED,
                        ),
                    ],
                    tight=True,
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.CALENDAR_TODAY_ROUNDED,
                                color=AppTheme.TEXT_MUTED,
                                size=14,
                            ),
                            ft.Text("Octubre 2023", size=13, color=AppTheme.TEXT_MUTED),
                        ],
                        spacing=6,
                    ),
                    bgcolor=AppTheme.INPUT_BG,
                    border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
                    border_radius=AppTheme.R_MD,
                    padding=ft.padding.symmetric(horizontal=14, vertical=7),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.END,
        )

    def _build_metrics_row(self) -> ft.Row:
        def gmetric(label, tag, value, sub_text, sub_color, pct):
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Text(label, size=12, color=AppTheme.TEXT_MUTED),
                                ft.Container(width=6),
                                badge(tag, AppTheme.PRIMARY, AppTheme.PRIMARY_LIGHT),
                            ],
                        ),
                        ft.Text(
                            value,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=AppTheme.TEXT_PRIMARY,
                        ),
                        ft.Container(
                            content=ft.Container(
                                bgcolor=AppTheme.PRIMARY,
                                border_radius=AppTheme.R_PILL,
                                width=pct * 2,
                                height=5,
                            ),
                            bgcolor=AppTheme.INPUT_BG,
                            border_radius=AppTheme.R_PILL,
                            height=5,
                        ),
                        ft.Text(sub_text, size=11, color=sub_color),
                    ],
                    spacing=6,
                ),
                bgcolor=AppTheme.CARD_BG,
                border_radius=AppTheme.R_LG,
                padding=16,
                border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
                expand=1,
            )

        return ft.Row(
            [
                gmetric(
                    "Gasto Diario",
                    "HOY",
                    "S/ 1,420.50",
                    "15% más que ayer",
                    AppTheme.SUCCESS,
                    65,
                ),
                gmetric(
                    "Presupuesto Restante",
                    "MENSUAL",
                    "S/ 8,579.50",
                    "75% utilizado",
                    AppTheme.TEXT_MUTED,
                    75,
                ),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Resumen de Categorías",
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color="#FFFFFF",
                            ),
                            ft.Text(
                                "Mayor gasto en Suministros de Oficina",
                                size=11,
                                color=ft.Colors.with_opacity(0.7, "#FFFFFF"),
                            ),
                            ft.Container(height=8),
                            ft.Row(
                                [
                                    ft.Container(
                                        bgcolor=ft.Colors.with_opacity(0.6, "#FFFFFF"),
                                        border_radius=AppTheme.R_SM,
                                        height=40,
                                        width=30,
                                    ),
                                    ft.Container(
                                        bgcolor=ft.Colors.with_opacity(0.5, "#FFFFFF"),
                                        border_radius=AppTheme.R_SM,
                                        height=55,
                                        width=30,
                                    ),
                                    ft.Container(
                                        bgcolor=ft.Colors.with_opacity(0.4, "#FFFFFF"),
                                        border_radius=AppTheme.R_SM,
                                        height=35,
                                        width=30,
                                    ),
                                    ft.Container(
                                        bgcolor=ft.Colors.with_opacity(0.9, "#FFFFFF"),
                                        border_radius=AppTheme.R_SM,
                                        height=70,
                                        width=30,
                                    ),
                                    ft.Container(
                                        bgcolor=ft.Colors.with_opacity(0.35, "#FFFFFF"),
                                        border_radius=AppTheme.R_SM,
                                        height=28,
                                        width=30,
                                    ),
                                ],
                                alignment=ft.MainAxisAlignment.END,
                                vertical_alignment=ft.CrossAxisAlignment.END,
                                spacing=4,
                            ),
                        ],
                        spacing=3,
                    ),
                    bgcolor=AppTheme.SIDEBAR_BG,
                    border_radius=AppTheme.R_LG,
                    padding=16,
                    expand=1,
                ),
            ],
            spacing=12,
        )

    def _build_main_row(self) -> ft.Row:
        return ft.Row(
            [
                ft.Container(self._build_form_card(), width=290),
                ft.Container(self._build_list_card(), expand=True),
            ],
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def _build_form_card(self) -> ft.Container:
        return card(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.ADD_CIRCLE_ROUNDED,
                                color=AppTheme.PRIMARY,
                                size=18,
                            ),
                            ft.Text(
                                "Nuevo Gasto",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Container(height=12),
                    ft.Text(
                        "CONCEPTO O PRODUCTO",
                        size=10,
                        color=AppTheme.TEXT_MUTED,
                        weight=ft.FontWeight.W_600,
                    ),
                    ft.Container(height=4),
                    app_input("", hint="Ej: Resmas de papel A4"),
                    ft.Container(height=10),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(
                                        "CATEGORÍA",
                                        size=10,
                                        color=AppTheme.TEXT_MUTED,
                                        weight=ft.FontWeight.W_600,
                                    ),
                                    ft.Container(height=4),
                                    app_dropdown(
                                        "",
                                        "Suministros",
                                        [
                                            "Suministros",
                                            "Logística",
                                            "Servicios",
                                            "Mantenimiento",
                                        ],
                                    ),
                                ],
                                expand=True,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        "MONTO (S/)",
                                        size=10,
                                        color=AppTheme.TEXT_MUTED,
                                        weight=ft.FontWeight.W_600,
                                    ),
                                    ft.Container(height=4),
                                    app_input(
                                        "",
                                        value="0.00",
                                        keyboard_type=ft.KeyboardType.NUMBER,
                                        width=100,
                                    ),
                                ],
                            ),
                        ],
                        spacing=10,
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "FECHA",
                        size=10,
                        color=AppTheme.TEXT_MUTED,
                        weight=ft.FontWeight.W_600,
                    ),
                    ft.Container(height=4),
                    app_input(
                        "",
                        hint="mm/dd/yyyy",
                        prefix_icon=ft.Icons.CALENDAR_TODAY_ROUNDED,
                    ),
                    ft.Container(height=14),
                    primary_btn("Registrar Gasto", ft.Icons.ADD_ROUNDED, expand=True),
                    ft.Container(height=12),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Icon(
                                            ft.Icons.LIGHTBULB_OUTLINE_ROUNDED,
                                            color=AppTheme.INFO,
                                            size=14,
                                        ),
                                        ft.Text(
                                            "Tip de Gestión",
                                            size=12,
                                            weight=ft.FontWeight.BOLD,
                                            color=AppTheme.INFO,
                                        ),
                                    ],
                                    spacing=6,
                                ),
                                ft.Text(
                                    "Considera comprar al por mayor las resmas de papel "
                                    "para ahorrar un 12% mensual basado en tu historial.",
                                    size=11,
                                    color=AppTheme.TEXT_MUTED,
                                    italic=True,
                                ),
                            ],
                            spacing=6,
                        ),
                        bgcolor=AppTheme.INFO_LT,
                        border_radius=AppTheme.R_MD,
                        padding=12,
                    ),
                ],
                spacing=0,
            ),
        )

    def _build_list_card(self) -> ft.Container:
        return card(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Gastos Recientes",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                                expand=True,
                            ),
                            ft.Text(
                                "Ver todo el historial", size=12, color=AppTheme.PRIMARY
                            ),
                        ],
                    ),
                    ft.Container(height=10),
                    self._gasto_row(
                        "🚚",
                        "Envío Proveedor FABER",
                        "Referencia #9021",
                        "LOGÍSTICA",
                        AppTheme.PRIMARY,
                        AppTheme.PRIMARY_LIGHT,
                        "Hoy, 10:45",
                        "S/ 45.00",
                    ),
                    self._gasto_row(
                        "🖨️",
                        "Cartuchos de Tinta Pro",
                        "Insumos de impresión",
                        "SUMINISTROS",
                        AppTheme.TEXT_MUTED,
                        AppTheme.INPUT_BG,
                        "Ayer",
                        "S/ 320.00",
                    ),
                    self._gasto_row(
                        "⚡",
                        "Recibo de Luz - Local A",
                        "Pago de servicios",
                        "SERVICIOS",
                        AppTheme.WARNING,
                        AppTheme.WARNING_LT,
                        "22 Oct",
                        "S/ 1,055.50",
                    ),
                    self._gasto_row(
                        "🧹",
                        "Materiales de Limpieza",
                        "Mantenimiento mensual",
                        "SUMINISTROS",
                        AppTheme.TEXT_MUTED,
                        AppTheme.INPUT_BG,
                        "20 Oct",
                        "S/ 85.00",
                    ),
                    ft.Container(height=10),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text(
                                            "UTILIZACIÓN DE PRESUPUESTO SEMANAL",
                                            size=11,
                                            color=AppTheme.TEXT_MUTED,
                                            weight=ft.FontWeight.W_600,
                                            expand=True,
                                        ),
                                        ft.Text(
                                            "S/ 3,450 / S/ 5,000",
                                            size=12,
                                            weight=ft.FontWeight.BOLD,
                                            color=AppTheme.PRIMARY,
                                        ),
                                    ],
                                ),
                                ft.Container(
                                    content=ft.Container(
                                        bgcolor=AppTheme.PRIMARY,
                                        border_radius=AppTheme.R_PILL,
                                        width=240,
                                        height=6,
                                    ),
                                    bgcolor=AppTheme.INPUT_BG,
                                    border_radius=AppTheme.R_PILL,
                                    height=6,
                                ),
                                ft.Text(
                                    "Tendencia basada en compras de almacén",
                                    size=11,
                                    color=AppTheme.TEXT_MUTED,
                                ),
                            ],
                            spacing=6,
                        ),
                        bgcolor=AppTheme.INPUT_BG,
                        border_radius=AppTheme.R_MD,
                        padding=12,
                    ),
                ],
                spacing=0,
            ),
        )

    def _gasto_row(self, emoji, nombre, ref, cat, cat_color, cat_bg, fecha, monto):
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
                                nombre,
                                size=13,
                                weight=ft.FontWeight.W_600,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                            ft.Text(ref, size=11, color=AppTheme.TEXT_MUTED),
                        ],
                        spacing=2,
                        expand=True,
                    ),
                    ft.Column(
                        [badge(cat, cat_color, cat_bg)],
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                    ft.Container(width=10),
                    ft.Column(
                        [
                            ft.Text(
                                monto,
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                            ft.Text(fecha, size=11, color=AppTheme.TEXT_MUTED),
                        ],
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            ),
            border=ft.Border(bottom=ft.BorderSide(0.5, AppTheme.CARD_BORDER)),
            padding=ft.padding.symmetric(vertical=10),
        )

    def on_search_change(self, e) -> None:
        self.search_text = (e.control.value or "").strip().lower()
        self.refresh_gastos()
        self.update()

    def open_form(self, e) -> None:
        concepto = app_input("Concepto", expand=True)
        monto = app_input("Monto", value="0")
        categoria = app_input("Categoria")

        def close_dialog(_):
            self._page.pop_dialog()

        def save_gasto(_):
            try:
                self.controller.create(
                    {
                        "concepto": (concepto.value or "").strip(),
                        "monto": parse_float(monto.value),
                        "categoria": (categoria.value or "").strip(),
                    }
                )
                self._page.pop_dialog()
                self.refresh_gastos()
                self.update()
                self._page.snack_bar = ft.SnackBar(
                    ft.Text("Gasto registrado correctamente.")
                )
                self._page.snack_bar.open = True
                self._page.update()
            except Exception:
                pass

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nuevo gasto"),
            content=ft.Column([concepto, monto, categoria], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.FilledButton("Aceptar", on_click=save_gasto),
            ],
        )
        self._page.show_dialog(dialog)

    def refresh_gastos(self) -> None:
        pass

    def _build_filters(self) -> ft.Container:
        return ft.Container(
            content=ft.Row(
                [self.search_field, self._build_filter_dropdown()],
                spacing=10,
            ),
            margin=ft.Margin.only(bottom=10),
        )

    def _build_filter_dropdown(self) -> ft.Row:
        categorias = self._get_categorias()
        chips = [
            ft.Container(
                content=ft.Text("Todos", size=12),
                padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                border_radius=AppTheme.R_PILL,
                bgcolor=AppTheme.PRIMARY
                if self.filter_categoria == "TODOS"
                else AppTheme.INPUT_BG,
                on_click=lambda _: self._set_filter("TODOS"),
            )
        ]
        for c in categorias[:5]:
            chips.append(
                ft.Container(
                    content=ft.Text(c[:15], size=12),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                    border_radius=AppTheme.R_PILL,
                    bgcolor=AppTheme.PRIMARY
                    if self.filter_categoria == c
                    else AppTheme.INPUT_BG,
                    on_click=lambda _, cat=c: self._set_filter(cat),
                )
            )
        return ft.Row(chips, spacing=8)

    def _set_filter(self, categoria: str) -> None:
        self.filter_categoria = categoria
        self.refresh_gastos()
        self.update()

    def _get_categorias(self) -> list[str]:
        gastos = self.controller.get_all(limit=100)
        categorias = set()
        for g in gastos:
            cat = g.get("categoria")
            if cat:
                categorias.add(cat)
        return sorted(list(categorias))

    def on_search_change(self, e) -> None:
        self.search_text = (e.control.value or "").strip().lower()
        self.refresh_gastos()
        self.update()

    def get_filtered_gastos(self) -> list[dict]:
        gastos = self.controller.get_all(limit=100)
        if self.filter_categoria != "TODOS":
            gastos = [g for g in gastos if g.get("categoria") == self.filter_categoria]
        if not self.search_text:
            return gastos
        return [
            g for g in gastos if self.search_text in str(g.get("concepto", "")).lower()
        ]

    def open_form(self, e) -> None:
        concepto = app_input("Concepto", expand=True)
        monto = app_input("Monto", value="0")
        categoria = app_input("Categoria")
        observaciones = ft.TextField(
            label="Observaciones",
            multiline=True,
            min_lines=2,
            max_lines=4,
            border_radius=AppTheme.R_MD,
            border_color=AppTheme.INPUT_BORDER,
            focused_border_color=AppTheme.INPUT_FOCUSED,
            fill_color=AppTheme.INPUT_BG,
            filled=True,
            content_padding=ft.padding.all(12),
        )
        error_text = ft.Text("", color=AppTheme.DANGER, visible=False)

        def close_dialog(_):
            self._page.pop_dialog()

        def save_gasto(_):
            try:
                self.controller.create(
                    {
                        "concepto": (concepto.value or "").strip(),
                        "monto": parse_float(monto.value),
                        "categoria": (categoria.value or "").strip(),
                        "observaciones": (observaciones.value or "").strip(),
                    }
                )
                self._page.pop_dialog()
                self.refresh_gastos()
                self.update()
                self._page.snack_bar = ft.SnackBar(
                    ft.Text("Gasto registrado correctamente.")
                )
                self._page.snack_bar.open = True
                self._page.update()
            except Exception as exc:
                error_text.value = f"No se pudo guardar: {exc}"
                error_text.visible = True
                self._page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nuevo gasto"),
            content=ft.Container(
                width=450,
                content=ft.Column(
                    [
                        concepto,
                        ft.ResponsiveRow(
                            [
                                ft.Column([monto], col={"sm": 12, "md": 6}),
                                ft.Column([categoria], col={"sm": 12, "md": 6}),
                            ],
                            run_spacing=10,
                        ),
                        observaciones,
                        error_text,
                    ],
                    tight=True,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.FilledButton("Aceptar", on_click=save_gasto),
            ],
        )
        self._page.show_dialog(dialog)

    def refresh_gastos(self) -> None:
        gastos = self.get_filtered_gastos()
        if not gastos:
            self.gastos_container.controls = [
                empty_state(
                    "Sin gastos registrados",
                    "Agrega un gasto para llevar el control del mes.",
                    ft.Icons.PAYMENTS_OUTLINED,
                )
            ]
            return

        controls = []
        total = 0.0
        for gasto in gastos:
            total += float(gasto.get("monto") or 0)
            controls.append(
                card(
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Text(
                                                gasto["concepto"],
                                                size=13,
                                                weight=ft.FontWeight.BOLD,
                                                color=AppTheme.TEXT_PRIMARY,
                                            ),
                                            ft.Text(
                                                f"{gasto.get('categoria') or 'Sin categoria'} | {short_datetime(gasto.get('fecha'))}",
                                                size=11,
                                                color=AppTheme.TEXT_MUTED,
                                            ),
                                        ],
                                        expand=True,
                                        spacing=2,
                                    ),
                                    ft.Text(
                                        money(float(gasto.get("monto") or 0)),
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=AppTheme.DANGER,
                                    ),
                                ]
                            ),
                            ft.Text(
                                gasto.get("observaciones") or "Sin observaciones.",
                                size=11,
                                color=AppTheme.TEXT_MUTED,
                            ),
                        ],
                        spacing=8,
                    ),
                )
            )

        if not self.is_mobile and len(controls) > 0:
            controls.append(
                card(
                    ft.Row(
                        [
                            ft.Text(
                                "TOTAL",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                            ft.Container(expand=True),
                            ft.Text(
                                money(total),
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.DANGER,
                            ),
                        ]
                    )
                )
            )

        self.gastos_container.controls = controls
