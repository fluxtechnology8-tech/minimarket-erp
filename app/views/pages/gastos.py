from __future__ import annotations

import flet as ft

from views.components.ui import (
    empty_state,
    section_card,
    card,
    app_input,
    searchbar,
    primary_btn,
)
from views.ui.theme import AppTheme, shadow
from views.ui.utils import money, parse_float, short_datetime


class GastosView(ft.Column):
    def __init__(self, page: ft.Page, controller, is_mobile: bool = False):
        super().__init__(expand=True, scroll=ft.ScrollMode.AUTO, spacing=20)
        self._page = page
        self.controller = controller
        self.is_mobile = is_mobile
        self.padding = 24
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

        if self.is_mobile:
            self.controls = [
                ft.Text("Gastos", size=28, weight=ft.FontWeight.BOLD),
                self._build_filters(),
                section_card(
                    "Lista de gastos",
                    [self.gastos_container],
                    "Solo visualización.",
                ),
            ]
        else:
            self.controls = [
                ft.Text("Gastos", size=28, weight=ft.FontWeight.BOLD),
                section_card(
                    "Registrar gasto",
                    [
                        ft.Container(
                            content=ft.Row(
                                [
                                    ft.Icon(
                                        ft.Icons.ADD_ROUNDED, color="#FFFFFF", size=15
                                    ),
                                    ft.Text(
                                        "Registrar gasto",
                                        size=12,
                                        weight=ft.FontWeight.W_600,
                                        color="#FFFFFF",
                                    ),
                                ],
                                spacing=6,
                            ),
                            bgcolor=AppTheme.PRIMARY,
                            border_radius=AppTheme.R_PILL,
                            padding=ft.padding.symmetric(horizontal=16, vertical=10),
                            on_click=self.open_form,
                        ),
                    ],
                    "Control básico de egresos del negocio.",
                ),
                section_card(
                    "Lista de gastos",
                    [
                        ft.Row(
                            [self.search_field, self._build_filter_dropdown()],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        self.gastos_container,
                    ],
                    "Historial de gastos del negocio.",
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
