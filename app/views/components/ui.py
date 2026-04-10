from __future__ import annotations

import flet as ft
from app.views.ui.theme import AppTheme

class StatCard(ft.Container):
    def __init__(self, title: str, value: str, icon: ft.IconData, color: str):
        super().__init__(
            bgcolor=AppTheme.SURFACE_CONTAINER_LOWEST,
            border_radius=20,
            padding=20,
            content=ft.Column(
                [
                    ft.Container(
                        width=44,
                        height=44,
                        border_radius=12,
                        bgcolor=ft.Colors.with_opacity(0.12, color),
                        content=ft.Icon(icon, color=color, size=24),
                    ),
                    ft.Text(
                        title,
                        size=13,
                        weight=ft.FontWeight.W_500,
                        color=AppTheme.TEXT_SECONDARY,
                    ),
                    ft.Text(
                        value,
                        size=28,
                        weight=ft.FontWeight.W_900,
                        color=AppTheme.TEXT_PRIMARY,
                    ),
                ],
                spacing=12,
            ),
        )


def section_card(
    title: str, controls: list[ft.Control], subtitle: str = None
) -> ft.Container:
    header = ft.Column(
        [
            ft.Text(
                title, size=20, weight=ft.FontWeight.BOLD, color=AppTheme.TEXT_PRIMARY
            )
        ]
    )
    if subtitle:
        header.controls.append(
            ft.Text(subtitle, size=13, color=AppTheme.TEXT_SECONDARY)
        )

    return ft.Container(
        bgcolor=AppTheme.SURFACE_CONTAINER_LOW,
        border_radius=24,
        padding=24,
        content=ft.Column([header] + controls, spacing=16),
    )

def empty_state(
    title: str, subtitle: str, icon: ft.IconData = ft.Icons.INBOX_OUTLINED
) -> ft.Container:
    return ft.Container(
        padding=24,
        border_radius=16,
        bgcolor=AppTheme.SURFACE_CONTAINER_LOWEST,
        content=ft.Column(
            [
                ft.Icon(icon, size=40, color=AppTheme.ACCENT),
                ft.Text(
                    title,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.Text(
                    subtitle,
                    size=13,
                    color=AppTheme.TEXT_SECONDARY,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )
