"""
TopBar component — rich header bar with logo, search, notifications, and user avatar.
Pure visual component.
"""

from __future__ import annotations

import flet as ft
from views.ui.theme import T, shadow


class TopBar(ft.Container):
    """Rich top bar matching the main2.py Papelería Pro design."""

    def __init__(self, page: ft.Page):
        super().__init__()
        self.content = ft.Row(
            controls=[
                # ── Brand ──
                ft.Row(
                    controls=[
                        ft.Icon(ft.Icons.STOREFRONT_ROUNDED, color=T.PRIMARY, size=20),
                        ft.Column(
                            controls=[
                                ft.Text("Papelería Pro", size=14,
                                        weight=ft.FontWeight.BOLD, color=T.TEXT_H),
                                ft.Text("Gestión de Inventario", size=10,
                                        color=T.TEXT_MUTED),
                            ],
                            spacing=0,
                        ),
                    ],
                    spacing=8,
                ),
                ft.Container(expand=True),
                # ── Search (decorative) ──
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SEARCH_ROUNDED, color=T.TEXT_DISABLED,
                                    size=16),
                            ft.Text("Buscar productos, ventas o registros...",
                                    size=13, color=T.TEXT_DISABLED),
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
                # ── Right controls ──
                ft.Row(
                    controls=[
                        # Notification bell
                        ft.Stack(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(ft.Icons.NOTIFICATIONS_OUTLINED,
                                                    color=T.TEXT_MUTED, size=18),
                                    width=36, height=36, bgcolor=T.INPUT_BG,
                                    border=ft.Border.all(0.5, T.CARD_BORDER),
                                    border_radius=T.R_PILL,
                                    alignment=ft.Alignment(0, 0),
                                ),
                                ft.Container(
                                    width=9, height=9, bgcolor=T.ERROR,
                                    border_radius=T.R_PILL, right=2, top=2,
                                ),
                            ],
                            width=36, height=36,
                        ),
                        # Settings
                        ft.Container(
                            content=ft.Icon(ft.Icons.SETTINGS_OUTLINED,
                                            color=T.TEXT_MUTED, size=18),
                            width=36, height=36, bgcolor=T.INPUT_BG,
                            border=ft.Border.all(0.5, T.CARD_BORDER),
                            border_radius=T.R_PILL,
                            alignment=ft.Alignment(0, 0),
                        ),
                        # User avatar
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Container(
                                        content=ft.Text("AD", size=11,
                                                        weight=ft.FontWeight.BOLD,
                                                        color="#FFFFFF"),
                                        bgcolor=T.PRIMARY, width=28, height=28,
                                        border_radius=T.R_PILL,
                                        alignment=ft.Alignment(0, 0),
                                    ),
                                    ft.Column(
                                        controls=[
                                            ft.Text("Admin Papelería", size=12,
                                                    weight=ft.FontWeight.W_600,
                                                    color=T.TEXT_H),
                                            ft.Text("Gerente de Tienda", size=10,
                                                    color=T.TEXT_MUTED),
                                        ],
                                        spacing=0,
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
