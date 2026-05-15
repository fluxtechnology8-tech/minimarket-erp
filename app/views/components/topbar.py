"""
TopBar component — rich header bar with logo, search, notifications, and user avatar.
Pure visual component.
"""

from __future__ import annotations

import flet as ft
from views.ui import theme
from views.ui.theme import shadow


class TopBar(ft.Container):
    """Rich top bar matching the main2.py Papelería Pro design."""

    def __init__(self, page: ft.Page, usuario=None, on_logout=None):
        super().__init__()
        T = theme.T

        nombre_usuario = usuario.get("nombre", "Usuario") if usuario else "Usuario"
        rol_usuario = usuario.get("rol", "") if usuario else ""
        iniciales = nombre_usuario[:2].upper()

        rol_display = "Administrador" if rol_usuario == "admin" else "Empleado"

        self.content = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.STOREFRONT_ROUNDED, color=T.PRIMARY, size=20),
                        ft.Column(
                            controls=[
                                ft.Text(
                                    "Minimarket ERP",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=T.TEXT_H,
                                ),
                                ft.Text(
                                    "Gestión de Inventario", size=10, color=T.TEXT_MUTED
                                ),
                            ],
                            spacing=0,
                        ),
                    ],
                    spacing=8,
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(
                                ft.Icons.SEARCH_ROUNDED, color=T.TEXT_DISABLED, size=16
                            ),
                            ft.Text(
                                "Buscar productos, ventas o registros...",
                                size=13,
                                color=T.TEXT_DISABLED,
                            ),
                        ],
                        spacing=8,
                    ),
                    bgcolor=T.INPUT_BG,
                    border=ft.Border.all(0.5, T.INPUT_BORDER),
                    border_radius=T.R_PILL,
                    padding=ft.padding.symmetric(horizontal=16, vertical=8),
                    width=320,
                ),
                ft.Container(expand=True),
                ft.Row(
                    controls=[
                        ft.Stack(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.NOTIFICATIONS_OUTLINED,
                                        color=T.TEXT_MUTED,
                                        size=18,
                                    ),
                                    width=36,
                                    height=36,
                                    bgcolor=T.INPUT_BG,
                                    border=ft.Border.all(0.5, T.CARD_BORDER),
                                    border_radius=T.R_PILL,
                                    alignment=ft.Alignment(0, 0),
                                ),
                                ft.Container(
                                    width=9,
                                    height=9,
                                    bgcolor=T.ERROR,
                                    border_radius=T.R_PILL,
                                    right=2,
                                    top=2,
                                ),
                            ],
                            width=36,
                            height=36,
                        ),
                        ft.Container(
                            content=ft.Icon(
                                ft.Icons.SETTINGS_OUTLINED, color=T.TEXT_MUTED, size=18
                            ),
                            width=36,
                            height=36,
                            bgcolor=T.INPUT_BG,
                            border=ft.Border.all(0.5, T.CARD_BORDER),
                            border_radius=T.R_PILL,
                            alignment=ft.Alignment(0, 0),
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Text(
                                            iniciales,
                                            size=11,
                                            weight=ft.FontWeight.BOLD,
                                            color=T.CARD_BG,
                                        ),
                                        bgcolor=T.PRIMARY,
                                        width=28,
                                        height=28,
                                        border_radius=T.R_PILL,
                                        alignment=ft.Alignment(0, 0),
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Text(
                                                nombre_usuario,
                                                size=12,
                                                weight=ft.FontWeight.W_600,
                                                color=T.TEXT_H,
                                            ),
                                            ft.Text(
                                                rol_display,
                                                size=10,
                                                color=T.TEXT_MUTED,
                                            ),
                                        ],
                                        spacing=0,
                                    ),
                                    ft.Container(
                                        content=ft.IconButton(
                                            icon=ft.Icons.LOGOUT,
                                            icon_size=16,
                                            icon_color=T.TEXT_MUTED,
                                            on_click=on_logout,
                                            tooltip="Cerrar sesión",
                                        ),
                                    ),
                                ],
                                spacing=8,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            bgcolor=T.INPUT_BG,
                            border=ft.Border.all(0.5, T.CARD_BORDER),
                            border_radius=T.R_PILL,
                            padding=ft.padding.symmetric(horizontal=10, vertical=4),
                        ),
                    ],
                    spacing=8,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.bgcolor = T.TOPBAR_BG
        self.padding = ft.padding.symmetric(horizontal=24, vertical=10)
        self.border = ft.Border(bottom=ft.BorderSide(0.5, T.TOPBAR_BORDER))
        self.shadow = shadow(T.TEXT_H, 4, 1)
