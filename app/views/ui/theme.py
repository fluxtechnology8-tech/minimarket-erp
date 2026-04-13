import flet as ft
from typing import Callable


class AppTheme:
    PRIMARY = "#2563EB"
    PRIMARY_DARK = "#1D4ED8"
    PRIMARY_LIGHT = "#DBEAFE"
    PRIMARY_MID = "#3B82F6"
    PRIMARY_CONTAINER = "#DBEAFE"
    SECONDARY = "#466270"
    SECONDARY_LIGHT = "#E0F2FE"
    ACCENT_CYAN = "#06B6D4"
    SUCCESS = "#059669"
    SUCCESS_LT = "#D1FAE5"
    WARNING = "#D97706"
    WARNING_LT = "#FEF3C7"
    DANGER = "#DC2626"
    DANGER_LT = "#FEE2E2"
    INFO = "#0284C7"
    INFO_LT = "#E0F2FE"

    BACKGROUND = "#F1F5F9"
    SURFACE = "#FFFFFF"
    SURFACE_CONTAINER = "#E2E8F0"
    SURFACE_CONTAINER_LOW = "#F8FAFC"
    SURFACE_CONTAINER_LOWEST = "#FFFFFF"
    TEXT_PRIMARY = "#0F172A"
    TEXT_SECONDARY = "#334155"
    TEXT_MUTED = "#64748B"
    TEXT_DISABLED = "#CBD5E1"
    ACCENT = "#536067"

    INPUT_BG = "#F8FAFC"
    INPUT_BORDER = "#CBD5E1"
    INPUT_FOCUSED = "#2563EB"
    DIVIDER = "#E2E8F0"

    CARD_BG = "#FFFFFF"
    CARD_BORDER = "#E2E8F0"

    SIDEBAR_BG = "#1E3A8A"
    SIDEBAR_HOVER = "#2563EB"
    SIDEBAR_SELECTED = "#2563EB"
    SIDEBAR_TEXT = "#BFDBFE"
    SIDEBAR_TEXT_ACT = "#FFFFFF"
    SIDEBAR_ICON = "#93C5FD"
    SIDEBAR_ICON_ACT = "#FFFFFF"
    SIDEBAR_LOGO_BG = "#2563EB"

    TOPBAR_BG = "#FFFFFF"
    TOPBAR_BORDER = "#E2E8F0"

    R_SM = 6
    R_MD = 10
    R_LG = 14
    R_XL = 20
    R_PILL = 999

    GRADIENT_START = "#2563EB"
    GRADIENT_END = "#3B82F6"

    DARK_PRIMARY = "#4F46E5"
    DARK_PRIMARY_DARK = "#4338CA"
    DARK_PRIMARY_LIGHT = "#1E1B4B"
    DARK_PRIMARY_MID = "#6366F1"
    DARK_PRIMARY_CONTAINER = "#1E1B4B"
    DARK_ACCENT_CYAN = "#22D3EE"
    DARK_SUCCESS = "#10B981"
    DARK_SUCCESS_LT = "#064E3B"
    DARK_WARNING = "#F59E0B"
    DARK_WARNING_LT = "#451A03"
    DARK_DANGER = "#EF4444"
    DARK_DANGER_LT = "#450A0A"
    DARK_INFO = "#38BDF8"
    DARK_INFO_LT = "#0C2340"

    DARK_BACKGROUND = "#0F0E17"
    DARK_SURFACE = "#1C1A2E"
    DARK_SURFACE_CONTAINER = "#2D2755"
    DARK_SURFACE_CONTAINER_LOW = "#14112A"
    DARK_SURFACE_CONTAINER_LOWEST = "#1C1A2E"
    DARK_TEXT_PRIMARY = "#E0E7FF"
    DARK_TEXT_SECONDARY = "#C7D2FE"
    DARK_TEXT_MUTED = "#6366F1"
    DARK_TEXT_DISABLED = "#3730A3"
    DARK_ACCENT = "#6B7280"

    DARK_INPUT_BG = "#14112A"
    DARK_INPUT_BORDER = "#312E81"
    DARK_INPUT_FOCUSED = "#4F46E5"
    DARK_DIVIDER = "#2D2755"

    DARK_CARD_BG = "#1C1A2E"
    DARK_CARD_BORDER = "#2D2755"

    DARK_SIDEBAR_BG = "#120F24"
    DARK_SIDEBAR_HOVER = "#3730A3"
    DARK_SIDEBAR_SELECTED = "#4F46E5"
    DARK_SIDEBAR_TEXT = "#A5B4FC"
    DARK_SIDEBAR_TEXT_ACT = "#FFFFFF"
    DARK_SIDEBAR_ICON = "#818CF8"
    DARK_SIDEBAR_ICON_ACT = "#FFFFFF"
    DARK_SIDEBAR_LOGO_BG = "#4338CA"

    DARK_TOPBAR_BG = "#1A1730"
    DARK_TOPBAR_BORDER = "#2D2755"

    _LIGHT_PALETTE = {
        "PRIMARY": PRIMARY,
        "PRIMARY_CONTAINER": PRIMARY_LIGHT,
        "BACKGROUND": BACKGROUND,
        "SURFACE": SURFACE,
        "SURFACE_CONTAINER": SURFACE_CONTAINER,
        "SURFACE_CONTAINER_LOW": SURFACE_CONTAINER_LOW,
        "SURFACE_CONTAINER_LOWEST": SURFACE_CONTAINER_LOWEST,
        "TEXT_PRIMARY": TEXT_PRIMARY,
        "TEXT_SECONDARY": TEXT_SECONDARY,
        "ACCENT": ACCENT,
        "SUCCESS": SUCCESS,
        "WARNING": WARNING,
        "DANGER": DANGER,
        "INPUT_BG": INPUT_BG,
        "INPUT_BORDER": INPUT_BORDER,
        "INPUT_FOCUSED": INPUT_FOCUSED,
        "CARD_BG": CARD_BG,
        "CARD_BORDER": CARD_BORDER,
    }

    _DARK_PALETTE = {
        "PRIMARY": DARK_PRIMARY,
        "PRIMARY_CONTAINER": DARK_PRIMARY_LIGHT,
        "BACKGROUND": DARK_BACKGROUND,
        "SURFACE": DARK_SURFACE,
        "SURFACE_CONTAINER": DARK_SURFACE_CONTAINER,
        "SURFACE_CONTAINER_LOW": DARK_SURFACE_CONTAINER_LOW,
        "SURFACE_CONTAINER_LOWEST": DARK_SURFACE_CONTAINER_LOWEST,
        "TEXT_PRIMARY": DARK_TEXT_PRIMARY,
        "TEXT_SECONDARY": DARK_TEXT_SECONDARY,
        "ACCENT": DARK_ACCENT,
        "SUCCESS": DARK_SUCCESS,
        "WARNING": DARK_WARNING,
        "DANGER": DARK_DANGER,
        "INPUT_BG": DARK_INPUT_BG,
        "INPUT_BORDER": DARK_INPUT_BORDER,
        "INPUT_FOCUSED": DARK_INPUT_FOCUSED,
        "CARD_BG": DARK_CARD_BG,
        "CARD_BORDER": DARK_CARD_BORDER,
    }

    @staticmethod
    def palette(is_dark: bool = False) -> dict[str, str]:
        return dict(AppTheme._DARK_PALETTE if is_dark else AppTheme._LIGHT_PALETTE)

    @staticmethod
    def apply_mode(is_dark: bool = False) -> dict[str, str]:
        pal = AppTheme.palette(is_dark)
        for key, value in pal.items():
            setattr(AppTheme, key, value)
        return pal

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


def shadow(color: str, blur: int = 8, y: int = 2):
    return ft.BoxShadow(
        blur_radius=blur,
        offset=ft.Offset(0, y),
        color=ft.Colors.with_opacity(0.10, color),
        spread_radius=0,
    )
