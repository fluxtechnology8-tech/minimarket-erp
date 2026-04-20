"""
Sidebar component — collapsible navigation panel with the Papelería Pro branding.
Pure visual component.  Navigation is delegated via the ``on_navigate`` callback.
"""

from __future__ import annotations

import flet as ft
from views.ui.theme import T, LightPalette, NAV_ITEMS


class Sidebar(ft.Container):
    """Collapsible sidebar matching main2.py design."""

    def __init__(
        self,
        page: ft.Page,
        current_view: str,
        on_navigate,
        on_theme_toggle,
    ):
        super().__init__()
        self._page = page
        self._current = current_view
        self._navigate = on_navigate
        self._theme_toggle = on_theme_toggle
        self._expanded = True
        self._build()

    # ── public API ────────────────────────────

    def update_view(self, view: str) -> None:
        self._current = view
        self._build()
        if self._page:
            self._page.update()

    # ── internal ──────────────────────────────

    def _toggle(self, _=None):
        self._expanded = not self._expanded
        self._build()
        if self._page:
            self._page.update()

    def _build(self):
        w = 210 if self._expanded else 64

        # ── Logo ──────────────────────────────
        logo = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.STOREFRONT_ROUNDED, color="#FFFFFF", size=18),
                        bgcolor=T.SIDEBAR_LOGO_BG, width=36, height=36,
                        border_radius=T.R_MD, alignment=ft.Alignment(0, 0),
                    ),
                    *(
                        [ft.Column(
                            controls=[
                                ft.Text("Papelería Pro", color="#FFFFFF", size=13,
                                        weight=ft.FontWeight.BOLD),
                                ft.Text("GESTIÓN DE INVENTARIO", color=T.SIDEBAR_TEXT,
                                        size=9, weight=ft.FontWeight.W_600),
                            ],
                            spacing=0,
                        )]
                        if self._expanded else []
                    ),
                ],
                spacing=10, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=14, vertical=14),
            border=ft.Border(
                bottom=ft.BorderSide(0.5, ft.Colors.with_opacity(0.1, "#FFFFFF"))
            ),
        )

        # ── Nav items ─────────────────────────
        items: list[ft.Control] = []
        for label, icon, key, _idx in NAV_ITEMS:
            active = key == self._current
            icon_color = T.SIDEBAR_ICON_ACT if active else T.SIDEBAR_ICON
            text_color = T.SIDEBAR_TEXT_ACT if active else T.SIDEBAR_TEXT
            bg = ft.Colors.with_opacity(0.15, "#FFFFFF") if active else "transparent"

            row_ctrl: list[ft.Control] = [
                ft.Container(
                    content=ft.Icon(icon, color=icon_color, size=18),
                    width=36, height=36,
                    border_radius=T.R_MD,
                    alignment=ft.Alignment(0, 0),
                ),
            ]
            if self._expanded:
                row_ctrl.append(
                    ft.Text(label, color=text_color, size=13,
                            weight=ft.FontWeight.W_700 if active else ft.FontWeight.W_400)
                )

            left_accent = ft.Container(
                width=3, height=28,
                bgcolor=T.SIDEBAR_ICON_ACT if active else "transparent",
                border_radius=ft.BorderRadius(0, 3, 3, 0),
            )

            item = ft.Container(
                content=ft.Row(
                    controls=[
                        left_accent,
                        ft.Container(
                            content=ft.Row(row_ctrl, spacing=10,
                                           vertical_alignment=ft.CrossAxisAlignment.CENTER),
                            bgcolor=bg,
                            border_radius=T.R_MD,
                            padding=ft.padding.symmetric(horizontal=8, vertical=6),
                            expand=True,
                            ink=True,
                            on_click=lambda e, k=key: self._navigate(k),
                        ),
                    ],
                    spacing=0, vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                margin=ft.margin.symmetric(vertical=1),
                animate=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
            )
            items.append(item)

        # ── User row at bottom ────────────────
        user_row = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Text("AP", size=11, weight=ft.FontWeight.BOLD,
                                        color="#FFFFFF"),
                        bgcolor=T.SIDEBAR_LOGO_BG, width=32, height=32,
                        border_radius=T.R_PILL, alignment=ft.Alignment(0, 0),
                    ),
                    *(
                        [ft.Column(
                            controls=[
                                ft.Text("Admin Papelería", color="#FFFFFF", size=12,
                                        weight=ft.FontWeight.W_600),
                                ft.Text("Control Total", color=T.SIDEBAR_TEXT, size=10),
                            ],
                            spacing=0,
                        )]
                        if self._expanded else []
                    ),
                ],
                spacing=8, vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=10, vertical=10),
        )

        # ── Theme toggle + collapse ──────────
        is_light = T is LightPalette
        bottom_controls = [
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.DARK_MODE_ROUNDED if is_light
                            else ft.Icons.LIGHT_MODE_ROUNDED,
                            color=T.SIDEBAR_TEXT, size=16,
                        ),
                        *(
                            [ft.Text(
                                "Modo oscuro" if is_light else "Modo claro",
                                color=T.SIDEBAR_TEXT, size=11,
                            )]
                            if self._expanded else []
                        ),
                    ],
                    spacing=8,
                ),
                padding=ft.padding.symmetric(horizontal=14, vertical=7),
                border_radius=T.R_MD,
                ink=True,
                on_click=lambda e: self._theme_toggle(),
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.MENU_OPEN_ROUNDED if self._expanded
                            else ft.Icons.MENU_ROUNDED,
                            color=T.SIDEBAR_TEXT, size=16,
                        ),
                        *(
                            [ft.Text("Colapsar", color=T.SIDEBAR_TEXT, size=11)]
                            if self._expanded else []
                        ),
                    ],
                    spacing=8,
                ),
                padding=ft.padding.symmetric(horizontal=14, vertical=7),
                border_radius=T.R_MD,
                ink=True,
                on_click=self._toggle,
            ),
        ]

        # ── Assemble ─────────────────────────
        self.content = ft.Column(
            controls=[
                logo,
                ft.Container(
                    content=ft.Column(controls=items, spacing=0),
                    padding=ft.padding.symmetric(horizontal=4, vertical=8),
                    expand=True,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Divider(
                                height=0.5,
                                color=ft.Colors.with_opacity(0.1, "#FFFFFF"),
                            ),
                            user_row,
                            ft.Divider(
                                height=0.5,
                                color=ft.Colors.with_opacity(0.1, "#FFFFFF"),
                            ),
                            ft.Container(
                                content=ft.Column(controls=bottom_controls, spacing=2),
                                padding=ft.padding.symmetric(horizontal=4, vertical=6),
                            ),
                        ],
                        spacing=0,
                    ),
                ),
            ],
            spacing=0, expand=True,
        )
        self.width = w
        self.bgcolor = T.SIDEBAR_BG
        self.animate = ft.Animation(200, ft.AnimationCurve.EASE_IN_OUT)
