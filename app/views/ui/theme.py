"""
Theme system with dynamic Light / Dark palettes.
The singleton ``T`` always points to the active palette so every UI file can
do ``from views.ui.theme import T`` and use ``T.PAGE_BG``, ``T.SIDEBAR_BG``, etc.
``AppTheme`` is kept as a thin compatibility layer that mirrors ``T``.
"""

from __future__ import annotations

import flet as ft


# ─────────────────────────────────────────────
# PALETA DE COLORES (Light / Dark)
# ─────────────────────────────────────────────


class LightPalette:
    PAGE_BG = "#F1F5F9"
    SIDEBAR_BG = "#1E3A8A"
    SIDEBAR_HOVER = "#2563EB"
    SIDEBAR_SELECTED = "#2563EB"
    SIDEBAR_ITEM_SEL = "#FFFFFF1A"
    SIDEBAR_TEXT = "#BFDBFE"
    SIDEBAR_TEXT_ACT = "#FFFFFF"
    SIDEBAR_ICON = "#93C5FD"
    SIDEBAR_ICON_ACT = "#FFFFFF"
    SIDEBAR_LOGO_BG = "#2563EB"
    TOPBAR_BG = "#FFFFFF"
    TOPBAR_BORDER = "#E2E8F0"
    CARD_BG = "#FFFFFF"
    CARD_BORDER = "#E2E8F0"
    TEXT_H = "#0F172A"
    TEXT_BODY = "#334155"
    TEXT_MUTED = "#64748B"
    TEXT_DISABLED = "#CBD5E1"
    PRIMARY = "#2563EB"
    PRIMARY_DARK = "#1D4ED8"
    PRIMARY_LIGHT = "#DBEAFE"
    PRIMARY_MID = "#3B82F6"
    ACCENT_CYAN = "#06B6D4"
    SUCCESS = "#059669"
    SUCCESS_LT = "#D1FAE5"
    WARNING = "#D97706"
    WARNING_LT = "#FEF3C7"
    ERROR = "#DC2626"
    ERROR_LT = "#FEE2E2"
    INFO = "#0284C7"
    INFO_LT = "#E0F2FE"
    INPUT_BG = "#F8FAFC"
    INPUT_BORDER = "#CBD5E1"
    INPUT_FOCUSED = "#2563EB"
    DIVIDER = "#E2E8F0"
    R_SM = 6
    R_MD = 10
    R_LG = 14
    R_XL = 20
    R_PILL = 999


class DarkPalette:
    PAGE_BG = "#1E1E24"
    SIDEBAR_BG = "#252530"
    SIDEBAR_HOVER = "#2F2F3A"
    SIDEBAR_SELECTED = "#3B3B4F"
    SIDEBAR_ITEM_SEL = "#FFFFFF10"
    SIDEBAR_TEXT = "#A0A0B0"
    SIDEBAR_TEXT_ACT = "#FFFFFF"
    SIDEBAR_ICON = "#9090A0"
    SIDEBAR_ICON_ACT = "#FFFFFF"
    SIDEBAR_LOGO_BG = "#4F46E5"
    TOPBAR_BG = "#252530"
    TOPBAR_BORDER = "#3A3A45"
    CARD_BG = "#2A2A35"
    CARD_BORDER = "#3A3A45"
    TEXT_H = "#E8E8EC"
    TEXT_BODY = "#C8C8D0"
    TEXT_MUTED = "#808090"
    TEXT_DISABLED = "#505060"
    PRIMARY = "#6366F1"
    PRIMARY_DARK = "#5558D0"
    PRIMARY_LIGHT = "#303045"
    PRIMARY_MID = "#7070E0"
    ACCENT_CYAN = "#22D3EE"
    SUCCESS = "#34D399"
    SUCCESS_LT = "#1A3A2F"
    WARNING = "#FBBF24"
    WARNING_LT = "#3D3520"
    ERROR = "#F87171"
    ERROR_LT = "#3D2020"
    INFO = "#38BDF8"
    INFO_LT = "#1D303D"
    INPUT_BG = "#252530"
    INPUT_BORDER = "#404050"
    INPUT_FOCUSED = "#6366F1"
    DIVIDER = "#3A3A45"
    R_SM = 6
    R_MD = 10
    R_LG = 14
    R_XL = 20
    R_PILL = 999


# Active palette singleton — starts as Light
T = LightPalette


def set_theme(is_dark: bool) -> type:
    """Switch the active palette and return it."""
    global T
    T = DarkPalette if is_dark else LightPalette
    # Also sync AppTheme so all existing views stay compatible
    AppTheme._sync_from_T()
    return T


# ─────────────────────────────────────────────
# NAV_ITEMS
# ─────────────────────────────────────────────
NAV_ITEMS = [
    ("Dashboard", ft.Icons.DASHBOARD_OUTLINED, "dashboard", 0),
    ("Catálogo", ft.Icons.INVENTORY_2_OUTLINED, "catalogo", 1),
    ("Kardex", ft.Icons.SWAP_HORIZ_ROUNDED, "kardex", 2),
    ("Boletas", ft.Icons.RECEIPT_LONG_OUTLINED, "boletas", 3),
    ("Gastos", ft.Icons.ACCOUNT_BALANCE_WALLET_OUTLINED, "gastos", 4),
    ("Reportes", ft.Icons.BAR_CHART_ROUNDED, "reportes", 5),
    ("Sincronización", ft.Icons.SYNC_ROUNDED, "sync", 6),
]


# ─────────────────────────────────────────────
# AppTheme — backward-compat layer
# ─────────────────────────────────────────────
class AppTheme:
    """Thin wrapper that always reflects the active palette ``T``.

    Existing view code does ``AppTheme.PRIMARY``, ``AppTheme.CARD_BG``, etc.
    and it will automatically get the colours of the current theme.
    """

    # We mirror the *light* values as class-level defaults so IDE autocomplete
    # works.  ``_sync_from_T()`` keeps them updated at runtime.
    PRIMARY = LightPalette.PRIMARY
    PRIMARY_DARK = LightPalette.PRIMARY_DARK
    PRIMARY_LIGHT = LightPalette.PRIMARY_LIGHT
    PRIMARY_MID = LightPalette.PRIMARY_MID
    PRIMARY_CONTAINER = LightPalette.PRIMARY_LIGHT
    SECONDARY = "#466270"
    SECONDARY_LIGHT = "#E0F2FE"
    ACCENT_CYAN = LightPalette.ACCENT_CYAN
    SUCCESS = LightPalette.SUCCESS
    SUCCESS_LT = LightPalette.SUCCESS_LT
    WARNING = LightPalette.WARNING
    WARNING_LT = LightPalette.WARNING_LT
    DANGER = LightPalette.ERROR
    DANGER_LT = LightPalette.ERROR_LT
    INFO = LightPalette.INFO
    INFO_LT = LightPalette.INFO_LT

    BACKGROUND = LightPalette.PAGE_BG
    SURFACE = LightPalette.CARD_BG
    SURFACE_CONTAINER = LightPalette.CARD_BORDER
    SURFACE_CONTAINER_LOW = LightPalette.INPUT_BG
    SURFACE_CONTAINER_LOWEST = LightPalette.CARD_BG
    TEXT_PRIMARY = LightPalette.TEXT_H
    TEXT_SECONDARY = LightPalette.TEXT_BODY
    TEXT_MUTED = LightPalette.TEXT_MUTED
    TEXT_DISABLED = LightPalette.TEXT_DISABLED
    ACCENT = "#536067"

    INPUT_BG = LightPalette.INPUT_BG
    INPUT_BORDER = LightPalette.INPUT_BORDER
    INPUT_FOCUSED = LightPalette.INPUT_FOCUSED
    DIVIDER = LightPalette.DIVIDER

    CARD_BG = LightPalette.CARD_BG
    CARD_BORDER = LightPalette.CARD_BORDER

    SIDEBAR_BG = LightPalette.SIDEBAR_BG
    SIDEBAR_HOVER = LightPalette.SIDEBAR_HOVER
    SIDEBAR_SELECTED = LightPalette.SIDEBAR_SELECTED
    SIDEBAR_TEXT = LightPalette.SIDEBAR_TEXT
    SIDEBAR_TEXT_ACT = LightPalette.SIDEBAR_TEXT_ACT
    SIDEBAR_ICON = LightPalette.SIDEBAR_ICON
    SIDEBAR_ICON_ACT = LightPalette.SIDEBAR_ICON_ACT
    SIDEBAR_LOGO_BG = LightPalette.SIDEBAR_LOGO_BG

    TOPBAR_BG = LightPalette.TOPBAR_BG
    TOPBAR_BORDER = LightPalette.TOPBAR_BORDER

    R_SM = 6
    R_MD = 10
    R_LG = 14
    R_XL = 20
    R_PILL = 999

    GRADIENT_START = "#2563EB"
    GRADIENT_END = "#3B82F6"

    @classmethod
    def _sync_from_T(cls):
        """Synchronise all class attributes with the currently-active palette ``T``."""
        cls.PRIMARY = T.PRIMARY
        cls.PRIMARY_DARK = T.PRIMARY_DARK
        cls.PRIMARY_LIGHT = T.PRIMARY_LIGHT
        cls.PRIMARY_MID = T.PRIMARY_MID
        cls.PRIMARY_CONTAINER = T.PRIMARY_LIGHT
        cls.ACCENT_CYAN = T.ACCENT_CYAN
        cls.SUCCESS = T.SUCCESS
        cls.SUCCESS_LT = T.SUCCESS_LT
        cls.WARNING = T.WARNING
        cls.WARNING_LT = T.WARNING_LT
        cls.DANGER = T.ERROR
        cls.DANGER_LT = T.ERROR_LT
        cls.INFO = T.INFO
        cls.INFO_LT = T.INFO_LT
        cls.BACKGROUND = T.PAGE_BG
        cls.SURFACE = T.CARD_BG
        cls.SURFACE_CONTAINER = T.CARD_BORDER
        cls.SURFACE_CONTAINER_LOW = T.INPUT_BG
        cls.SURFACE_CONTAINER_LOWEST = T.CARD_BG
        cls.TEXT_PRIMARY = T.TEXT_H
        cls.TEXT_SECONDARY = T.TEXT_BODY
        cls.TEXT_MUTED = T.TEXT_MUTED
        cls.TEXT_DISABLED = T.TEXT_DISABLED
        cls.INPUT_BG = T.INPUT_BG
        cls.INPUT_BORDER = T.INPUT_BORDER
        cls.INPUT_FOCUSED = T.INPUT_FOCUSED
        cls.DIVIDER = T.DIVIDER
        cls.CARD_BG = T.CARD_BG
        cls.CARD_BORDER = T.CARD_BORDER
        cls.SIDEBAR_BG = T.SIDEBAR_BG
        cls.SIDEBAR_HOVER = T.SIDEBAR_HOVER
        cls.SIDEBAR_SELECTED = T.SIDEBAR_SELECTED
        cls.SIDEBAR_TEXT = T.SIDEBAR_TEXT
        cls.SIDEBAR_TEXT_ACT = T.SIDEBAR_TEXT_ACT
        cls.SIDEBAR_ICON = T.SIDEBAR_ICON
        cls.SIDEBAR_ICON_ACT = T.SIDEBAR_ICON_ACT
        cls.SIDEBAR_LOGO_BG = T.SIDEBAR_LOGO_BG
        cls.TOPBAR_BG = T.TOPBAR_BG
        cls.TOPBAR_BORDER = T.TOPBAR_BORDER

    @staticmethod
    def palette(is_dark: bool = False) -> dict[str, str]:
        pal = DarkPalette if is_dark else LightPalette
        return {
            "PRIMARY": pal.PRIMARY,
            "PRIMARY_CONTAINER": pal.PRIMARY_LIGHT,
            "BACKGROUND": pal.PAGE_BG,
            "SURFACE": pal.CARD_BG,
            "SURFACE_CONTAINER": pal.CARD_BORDER,
            "SURFACE_CONTAINER_LOW": pal.INPUT_BG,
            "SURFACE_CONTAINER_LOWEST": pal.CARD_BG,
            "TEXT_PRIMARY": pal.TEXT_H,
            "TEXT_SECONDARY": pal.TEXT_BODY,
            "ACCENT": "#536067" if not is_dark else "#6B7280",
            "SUCCESS": pal.SUCCESS,
            "WARNING": pal.WARNING,
            "DANGER": pal.ERROR,
            "INPUT_BG": pal.INPUT_BG,
            "INPUT_BORDER": pal.INPUT_BORDER,
            "INPUT_FOCUSED": pal.INPUT_FOCUSED,
            "CARD_BG": pal.CARD_BG,
            "CARD_BORDER": pal.CARD_BORDER,
        }

    @staticmethod
    def apply_mode(is_dark: bool = False) -> dict[str, str]:
        set_theme(is_dark)
        return AppTheme.palette(is_dark)

    @staticmethod
    def get_color(color_name: str, is_dark: bool = False) -> str:
        pal = AppTheme.palette(is_dark)
        return pal.get(color_name, pal["TEXT_PRIMARY"])

    @staticmethod
    def gradient() -> list[str]:
        return [AppTheme.GRADIENT_START, AppTheme.GRADIENT_END]

    @staticmethod
    def get_theme() -> ft.Theme:
        return ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=AppTheme.PRIMARY_LIGHT,
                primary_container=AppTheme.PRIMARY_CONTAINER,
                secondary=AppTheme.SECONDARY,
                surface=AppTheme.SURFACE,
                on_primary=ft.Colors.WHITE,
                on_secondary=ft.Colors.WHITE,
            ),
            font_family="Inter",
            visual_density=ft.VisualDensity.STANDARD,
        )


# ─────────────────────────────────────────────
# Utilities
# ─────────────────────────────────────────────


def shadow(color: str, blur: int = 8, y: int = 2):
    return ft.BoxShadow(
        blur_radius=blur,
        offset=ft.Offset(0, y),
        color=ft.Colors.with_opacity(0.10, color),
        spread_radius=0,
    )
