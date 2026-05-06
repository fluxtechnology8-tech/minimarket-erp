"""
Main application shell.
Desktop: Sidebar + TopBar layout (Papelería Pro style).
Mobile:  NavigationBar (unchanged).
"""

from __future__ import annotations

import flet as ft
from core.init_db import init_db
from views.ui.theme import AppTheme, LightPalette, DarkPalette, set_theme, NAV_ITEMS
from views.ui import theme
from views.components.sidebar import Sidebar
from views.components.topbar import TopBar
from views.pages import (
    BoletasView,
    DashboardView,
    GastosView,
    KardexView,
    ProductosView,
    ReportesView,
    SyncView,
)

from repositories import (
    ProductoRepository,
    KardexRepository,
    GastoRepository,
    VentaRepository,
    ReporteRepository,
    SyncRepository,
)

from services import (
    ProductoService,
    KardexService,
    GastoService,
    VentaService,
    ReporteService,
    SyncService,
)

from controllers import (
    ProductoController,
    KardexController,
    GastoController,
    VentaController,
    ReporteController,
    SyncController,
)


# Map view-key strings to numeric indices
_VIEW_KEY_TO_INDEX = {item[2]: item[3] for item in NAV_ITEMS}
_INDEX_TO_VIEW_KEY = {v: k for k, v in _VIEW_KEY_TO_INDEX.items()}


class MinimarketApp:
    def __init__(self):
        init_db()
        self._init_dependencies()

    def _init_dependencies(self):
        producto_repo = ProductoRepository()
        kardex_repo = KardexRepository()
        gasto_repo = GastoRepository()
        venta_repo = VentaRepository()
        reporte_repo = ReporteRepository()
        sync_repo = SyncRepository()

        producto_service = ProductoService(producto_repo, kardex_repo)
        kardex_service = KardexService(kardex_repo, producto_repo)
        gasto_service = GastoService(gasto_repo)
        venta_service = VentaService(venta_repo, producto_repo, kardex_repo)
        reporte_service = ReporteService(reporte_repo)
        sync_service = SyncService(sync_repo)

        self.producto_controller = ProductoController(producto_service)
        self.kardex_controller = KardexController(kardex_service)
        self.gasto_controller = GastoController(gasto_service)
        self.venta_controller = VentaController(venta_service)
        self.reporte_controller = ReporteController(reporte_service)
        self.sync_controller = SyncController(sync_service)

        self.page: ft.Page | None = None
        self.content_area: ft.Container | None = None
        self.sidebar: Sidebar | None = None
        self.current_view_key = "dashboard"
        self.current_index = 0
        self.is_dark = False
        self.is_mobile = False
        self.mobile_destinations = [0, 1, 2, 4, 6]

    def run(self) -> None:
        import os

        assets_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        ft.run(self.main, assets_dir=assets_path)

    def main(self, page: ft.Page) -> None:
        self.page = page
        page.title = "Papelería Pro — Gestión de Inventario"
        page.padding = 0
        page.spacing = 0
        page.appbar = None
        page.navigation_bar = None
        page.on_resized = self._on_resize

        self._apply_theme()
        self._build_layout()
        page.update()

    # ── Theme ────────────────────────────────

    def _apply_theme(self) -> None:
        set_theme(self.is_dark)
        self.page.theme_mode = ft.ThemeMode.DARK if self.is_dark else ft.ThemeMode.LIGHT
        self.page.bgcolor = theme.T.PAGE_BG
        self.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=theme.T.PRIMARY,
                primary_container=theme.T.PRIMARY_LIGHT,
                secondary="#466270",
                surface=theme.T.CARD_BG,
                on_primary=ft.Colors.WHITE,
                on_secondary=ft.Colors.WHITE,
                on_surface=theme.T.TEXT_H,
            ),
            font_family="Inter",
        )
        self.page.dark_theme = self.page.theme

    def _toggle_theme(self) -> None:
        self.is_dark = not self.is_dark
        set_theme(self.is_dark)

        self.page.theme_mode = ft.ThemeMode.DARK if self.is_dark else ft.ThemeMode.LIGHT
        self.page.theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=theme.T.PRIMARY,
                primary_container=theme.T.PRIMARY_LIGHT,
                secondary="#466270",
                surface=theme.T.CARD_BG,
                on_primary=ft.Colors.WHITE,
                on_secondary=ft.Colors.WHITE,
                on_surface=theme.T.TEXT_H,
            ),
            font_family="Inter",
        )
        self.page.dark_theme = self.page.theme
        self.page.bgcolor = theme.T.PAGE_BG
        
        # Clean and rebuild entire layout to ensure all components use new theme
        self.page.clean()
        self.sidebar = None
        self.content_area = None
        self._build_layout()
        self.page.update()

    # ── Resize ───────────────────────────────

    def _on_resize(self, e) -> None:
        next_is_mobile = self.page.width < 768 if self.page.width else True
        if next_is_mobile != self.is_mobile:
            self.page.clean()
            self._build_layout()
            self.page.update()

    # ── Layout ───────────────────────────────

    def _build_layout(self) -> None:
        self.is_mobile = self.page.width < 768 if self.page.width else True
        self.content_area = ft.Container(
            expand=True,
            content=self.get_view(self.current_index),
            bgcolor=theme.T.PAGE_BG,
            padding=ft.Padding.symmetric(
                horizontal=12 if self.is_mobile else 20,
                vertical=12 if self.is_mobile else 16,
            ),
        )

        if self.is_mobile:
            self._build_mobile_layout()
        else:
            self._build_desktop_layout()

    def _build_desktop_layout(self) -> None:
        page = self.page
        page.appbar = None
        page.navigation_bar = None
        page.floating_action_button = None

        topbar = TopBar(page)

        self.sidebar = Sidebar(
            page=page,
            current_view=self.current_view_key,
            on_navigate=self._navigate_by_key,
            on_theme_toggle=self._toggle_theme,
        )

        page.add(
            ft.Column(
                controls=[
                    topbar,
                    ft.Row(
                        controls=[
                            self.sidebar,
                            ft.Container(width=0.5, bgcolor=theme.T.DIVIDER),
                            self.content_area,
                        ],
                        spacing=0,
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            )
        )

    def _build_mobile_layout(self) -> None:
        page = self.page
        page.appbar = None
        mobile_index = self._get_mobile_nav_index()

        page.navigation_bar = ft.NavigationBar(
            selected_index=mobile_index,
            on_change=self.on_mobile_navigation_change,
            bgcolor=theme.T.CARD_BG,
            indicator_color=theme.T.PRIMARY,
            height=65,
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Inicio"),
                ft.NavigationBarDestination(
                    icon=ft.Icons.INVENTORY_2, label="Productos"
                ),
                ft.NavigationBarDestination(icon=ft.Icons.SWAP_HORIZ, label="Kardex"),
                ft.NavigationBarDestination(icon=ft.Icons.PAYMENTS, label="Gastos"),
                ft.NavigationBarDestination(icon=ft.Icons.SYNC, label="Sync"),
            ],
        )

        header = ft.Container(
            bgcolor=theme.T.CARD_BG,
            padding=ft.Padding.only(left=16, right=16, top=42, bottom=12),
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                "Papelería Pro",
                                size=18,
                                weight=ft.FontWeight.W_800,
                                color=theme.T.TEXT_H,
                            ),
                            ft.Text(
                                self._get_mobile_subtitle(),
                                size=11,
                                color=theme.T.TEXT_MUTED,
                            ),
                        ],
                        tight=True,
                        spacing=0,
                    ),
                    ft.Container(expand=True),
                    ft.IconButton(
                        icon=ft.Icons.LIGHT_MODE
                        if self.is_dark
                        else ft.Icons.DARK_MODE,
                        icon_color=theme.T.TEXT_H,
                        on_click=lambda _: self._toggle_theme(),
                        tooltip="Cambiar tema",
                        scale=0.9,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

        page.floating_action_button = None
        page.add(
            ft.Column(
                expand=True,
                spacing=0,
                controls=[header, self.content_area],
            )
        )

    # ── Navigation ───────────────────────────

    def _navigate_by_key(self, view_key: str) -> None:
        """Called by the Sidebar when the user clicks a nav item."""
        idx = _VIEW_KEY_TO_INDEX.get(view_key, 0)
        self.current_view_key = view_key
        self.current_index = idx
        if self.content_area:
            self.content_area.content = self.get_view(idx)
            self.content_area.bgcolor = theme.T.PAGE_BG
        if self.sidebar:
            self.sidebar.update_view(view_key)
        self.page.update()

    def on_mobile_navigation_change(self, e) -> None:
        selected_mobile_index = e.control.selected_index
        self.current_index = self.mobile_destinations[selected_mobile_index]
        self.current_view_key = _INDEX_TO_VIEW_KEY.get(self.current_index, "dashboard")
        self.page.clean()
        self._build_layout()
        self.page.update()

    def _get_mobile_nav_index(self) -> int:
        if self.current_index in self.mobile_destinations:
            return self.mobile_destinations.index(self.current_index)
        return 0

    def _get_mobile_subtitle(self) -> str:
        labels = {
            0: "Dashboard móvil",
            1: "Gestión de productos",
            2: "Movimientos de inventario",
            4: "Gastos y administración",
            6: "Sincronización y respaldos",
        }
        return labels.get(self.current_index, "Panel móvil")

    # ── View factory (unchanged logic) ───────

    def get_view(self, index: int) -> ft.Control:
        if not self.page:
            return ft.Text("Inicializando...")

        is_mobile = self.is_mobile
        views = {
            0: DashboardView(self.reporte_controller, is_mobile),
            1: ProductosView(
                self.page, self.producto_controller, self.kardex_controller, is_mobile
            ),
            2: KardexView(
                self.page, self.kardex_controller, self.producto_controller, is_mobile
            ),
            3: BoletasView(self.page, self.venta_controller),
            4: GastosView(self.page, self.gasto_controller, is_mobile),
            5: ReportesView(self.page, self.reporte_controller),
            6: SyncView(self.page, self.sync_controller, is_mobile),
        }
        return views.get(index, DashboardView(self.reporte_controller, is_mobile))


if __name__ == "__main__":
    app = MinimarketApp()
    ft.run()
