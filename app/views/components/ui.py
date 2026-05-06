from __future__ import annotations

import flet as ft
from views.ui.theme import AppTheme, shadow


class StatCard(ft.Container):
    def __init__(self, title: str, value: str, icon: ft.IconData, color: str):
        super().__init__(
            bgcolor=AppTheme.CARD_BG,
            border_radius=AppTheme.R_LG,
            padding=16,
            border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
            shadow=shadow(AppTheme.PRIMARY, 6, 2),
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                width=40,
                                height=40,
                                border_radius=AppTheme.R_MD,
                                bgcolor=ft.Colors.with_opacity(0.12, color),
                                content=ft.Icon(icon, color=color, size=20),
                            ),
                            ft.Container(expand=True),
                        ],
                    ),
                    ft.Text(
                        title,
                        size=12,
                        color=AppTheme.TEXT_MUTED,
                    ),
                    ft.Text(
                        value,
                        size=22,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_PRIMARY,
                    ),
                ],
                spacing=3,
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
        header.controls.append(ft.Text(subtitle, size=13, color=AppTheme.TEXT_MUTED))

    return ft.Container(
        bgcolor=AppTheme.CARD_BG,
        border_radius=AppTheme.R_LG,
        padding=16,
        border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
        shadow=shadow(AppTheme.PRIMARY, 6, 2),
        content=ft.Column([header] + controls, spacing=16),
    )


def empty_state(
    title: str, subtitle: str, icon: ft.IconData = ft.Icons.INBOX_OUTLINED
) -> ft.Container:
    return ft.Container(
        padding=24,
        border_radius=AppTheme.R_LG,
        bgcolor=AppTheme.INPUT_BG,
        content=ft.Column(
            [
                ft.Icon(icon, size=40, color=AppTheme.TEXT_MUTED),
                ft.Text(
                    title,
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER,
                    color=AppTheme.TEXT_PRIMARY,
                ),
                ft.Text(
                    subtitle,
                    size=13,
                    color=AppTheme.TEXT_MUTED,
                    text_align=ft.TextAlign.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
        ),
    )


def badge(text: str, color: str, bg: str) -> ft.Container:
    return ft.Container(
        content=ft.Text(text, size=10, weight=ft.FontWeight.W_700, color=color),
        bgcolor=bg,
        padding=ft.padding.symmetric(horizontal=8, vertical=3),
        border_radius=AppTheme.R_PILL,
    )


def card(content, padding=16):
    return ft.Container(
        content=content,
        bgcolor=AppTheme.CARD_BG,
        border_radius=AppTheme.R_LG,
        padding=padding,
        border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
        shadow=shadow(AppTheme.PRIMARY, 6, 2),
    )


def app_input(
    label,
    value="",
    hint="",
    prefix_icon=None,
    keyboard_type=None,
    expand=False,
    width=None,
    on_change=None,
):
    return ft.TextField(
        label=label,
        value=value,
        hint_text=hint,
        prefix_icon=prefix_icon,
        keyboard_type=keyboard_type,
        expand=expand,
        width=width,
        on_change=on_change,
        border_radius=AppTheme.R_MD,
        border_color=AppTheme.INPUT_BORDER,
        focused_border_color=AppTheme.INPUT_FOCUSED,
        fill_color=AppTheme.INPUT_BG,
        filled=True,
        label_style=ft.TextStyle(color=AppTheme.TEXT_MUTED, size=12),
        content_padding=ft.padding.symmetric(horizontal=14, vertical=12),
    )


def searchbar(hint="Buscar...", on_change=None, expand=True):
    return ft.TextField(
        hint_text=hint,
        hint_style=ft.TextStyle(color=AppTheme.TEXT_DISABLED, size=13),
        prefix_icon=ft.Icons.SEARCH_ROUNDED,
        border_radius=AppTheme.R_PILL,
        border_color=AppTheme.INPUT_BORDER,
        focused_border_color=AppTheme.INPUT_FOCUSED,
        fill_color=AppTheme.INPUT_BG,
        filled=True,
        content_padding=ft.padding.symmetric(horizontal=18, vertical=10),
        on_change=on_change,
        expand=expand,
    )


def app_dropdown(label, value, options, width=None, expand=False):
    return ft.Dropdown(
        label=label,
        value=value,
        options=[ft.dropdown.Option(o) for o in options],
        width=width,
        expand=expand,
        border_radius=AppTheme.R_MD,
        border_color=AppTheme.INPUT_BORDER,
        focused_border_color=AppTheme.INPUT_FOCUSED,
        fill_color=AppTheme.INPUT_BG,
        filled=True,
        label_style=ft.TextStyle(color=AppTheme.TEXT_MUTED, size=12),
    )


def primary_btn(text, icon=None, variant="filled", on_click=None, expand=False):
    if variant == "filled":
        bg, fg, border = AppTheme.PRIMARY, "#FFFFFF", "transparent"
    elif variant == "outline":
        bg, fg, border = "transparent", AppTheme.PRIMARY, AppTheme.PRIMARY
    else:
        bg, fg, border = AppTheme.PRIMARY_LIGHT, AppTheme.PRIMARY, "transparent"
    return ft.ElevatedButton(
        content=ft.Row(
            [ft.Icon(icon, color=fg, size=15)]
            + [ft.Text(text, size=12, weight=ft.FontWeight.W_600, color=fg)]
            if icon
            else [ft.Text(text, size=12, weight=ft.FontWeight.W_600, color=fg)],
            spacing=6,
            tight=True,
        ),
        bgcolor=bg,
        elevation=0,
        on_click=on_click,
        expand=expand,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=AppTheme.R_PILL),
            padding=ft.padding.symmetric(horizontal=16, vertical=10),
            side=ft.BorderSide(1, border),
        ),
    )


def section_header(title, subtitle=""):
    controls = [
        ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=AppTheme.TEXT_PRIMARY)
    ]
    if subtitle:
        controls.append(ft.Text(subtitle, size=13, color=AppTheme.TEXT_MUTED))
    return ft.Column(controls=controls, spacing=3)
