import flet as ft


class AppTheme:
    PRIMARY = "#00658D"
    PRIMARY_CONTAINER = "#00A3E0"
    PRIMARY_LIGHT = "#38BDF8"
    SECONDARY = "#466270"
    SECONDARY_LIGHT = "#C6E4F4"
    BACKGROUND = "#F7FAFC"
    SURFACE = "#FFFFFF"
    SURFACE_CONTAINER = "#EBEEF0"
    SURFACE_CONTAINER_LOW = "#F1F4F6"
    SURFACE_CONTAINER_LOWEST = "#FFFFFF"
    TEXT_PRIMARY = "#181C1E"
    TEXT_SECONDARY = "#3E4850"
    ACCENT = "#536067"
    SUCCESS = "#10B981"
    WARNING = "#F59E0B"
    DANGER = "#BA1A1A"

    GRADIENT_START = "#00658D"
    GRADIENT_END = "#00A3E0"

    DARK_PRIMARY = "#38BDF8"
    DARK_PRIMARY_CONTAINER = "#0EA5E9"
    DARK_BACKGROUND = "#121220"
    DARK_SURFACE = "#1E1E2E"
    DARK_SURFACE_CONTAINER = "#2A2A3A"
    DARK_SURFACE_CONTAINER_LOW = "#252538"
    DARK_SURFACE_CONTAINER_LOWEST = "#1A1A2E"
    DARK_TEXT_PRIMARY = "#FFFFFF"
    DARK_TEXT_SECONDARY = "#A0A0B0"
    DARK_ACCENT = "#6B7280"
    DARK_SUCCESS = "#34D399"
    DARK_WARNING = "#FBBF24"
    DARK_DANGER = "#F87171"

    _LIGHT_PALETTE = {
        "PRIMARY": PRIMARY,
        "PRIMARY_CONTAINER": PRIMARY_CONTAINER,
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
    }

    _DARK_PALETTE = {
        "PRIMARY": DARK_PRIMARY,
        "PRIMARY_CONTAINER": DARK_PRIMARY_CONTAINER,
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
    }

    @staticmethod
    def palette(is_dark: bool = False) -> dict[str, str]:
        return dict(AppTheme._DARK_PALETTE if is_dark else AppTheme._LIGHT_PALETTE)

    @staticmethod
    def apply_mode(is_dark: bool = False) -> dict[str, str]:
        palette = AppTheme.palette(is_dark)
        for key, value in palette.items():
            setattr(AppTheme, key, value)
        return palette

    @staticmethod
    def get_color(color_name: str, is_dark: bool = False) -> str:
        palette = AppTheme.palette(is_dark)
        return palette.get(color_name, palette["TEXT_PRIMARY"])

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
