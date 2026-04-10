from __future__ import annotations

import flet as ft
from app.core.init_db import init_db
from app.views.ui.theme import AppTheme
from app.views.pages import (
    BoletasView,
    DashboardView,
    GastosView,
    KardexView,
    ProductosView,
    ReportesView,
    SyncView,
)

from app.repositories import (
    ProductoRepository,
    KardexRepository,
    GastoRepository,
    VentaRepository,
    ReporteRepository,
    SyncRepository,
)

from app.services import (
    ProductoService,
    KardexService,
    GastoService,
    VentaService,
    ReporteService,
    SyncService,
)

from app.controllers import (
    ProductoController,
    KardexController,
    GastoController,
    VentaController,
    ReporteController,
    SyncController,
)


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
        self.nav_rail: ft.NavigationRail | None = None
        self.theme_toggle: ft.IconButton | None = None
        self.current_view_control: ft.Control | None = None
        self.current_index = 0
        self.is_dark = False
        self.is_mobile = False
        self.mobile_destinations = [0, 1, 2, 4, 6]

    def run(self) -> None:
        ft.run(self.main, assets_dir="assets")

    def main(self, page: ft.Page) -> None:
        self.page = page
        page.title = "Minimarket ERP"
        page.theme = AppTheme.get_theme()
        page.dark_theme = AppTheme.get_theme()
        page.theme_mode = ft.ThemeMode.LIGHT
        self._apply_theme()
        page.padding = 0
        page.spacing = 0
        page.appbar = None
        page.navigation_bar = None
        page.on_resized = self._on_resize

        self._build_layout()
        page.update()

    def _get_colors(self) -> dict:
        palette = AppTheme.palette(self.is_dark)
        return {
            "bg": palette["BACKGROUND"],
            "surface": palette["SURFACE"],
            "surface_container": palette["SURFACE_CONTAINER"],
            "surface_low": palette["SURFACE_CONTAINER_LOW"],
            "surface_lowest": palette["SURFACE_CONTAINER_LOWEST"],
            "text": palette["TEXT_PRIMARY"],
            "text_secondary": palette["TEXT_SECONDARY"],
            "accent": palette["ACCENT"],
            "primary": palette["PRIMARY"],
            "primary_container": palette["PRIMARY_CONTAINER"],
        }

    def _apply_theme(self) -> None:
        AppTheme.apply_mode(self.is_dark)
        colors = self._get_colors()
        theme = ft.Theme(
            color_scheme=ft.ColorScheme(
                primary=AppTheme.PRIMARY,
                primary_container=AppTheme.PRIMARY_CONTAINER,
                secondary="#466270",
                surface=colors["surface"],
                on_primary=ft.Colors.WHITE,
                on_secondary=ft.Colors.WHITE,
                on_surface=colors["text"],
            ),
            font_family="Inter",
        )
        self.page.theme = theme
        self.page.dark_theme = theme
        self.page.theme_mode = ft.ThemeMode.DARK if self.is_dark else ft.ThemeMode.LIGHT
        self.page.bgcolor = colors["bg"]

    def _toggle_theme(self, e) -> None:
        self.is_dark = not self.is_dark
        self._apply_theme()
        if self.theme_toggle:
            self.theme_toggle.icon = (
                ft.Icons.LIGHT_MODE if self.is_dark else ft.Icons.DARK_MODE
            )

        self.page.clean()
        self._build_layout()
        self.page.update()

    def _on_resize(self, e) -> None:
        next_is_mobile = self.page.width < 768 if self.page.width else True
        if next_is_mobile != self.is_mobile:
            self.page.clean()
            self._build_layout()
            self.page.update()

    def _build_layout(self) -> None:
        self.is_mobile = self.page.width < 768 if self.page.width else True
        self.current_view_control = self.get_view(self.current_index)
        self.content_area = ft.Container(
            expand=True,
            content=self.current_view_control,
            padding=ft.padding.symmetric(
                horizontal=12 if self.is_mobile else 20,
                vertical=12 if self.is_mobile else 16,
            ),
        )

        if self.is_mobile:
            self._build_mobile_layout()
        else:
            self._build_desktop_layout()

    def _build_mobile_layout(self) -> None:
        page = self.page
        colors = self._get_colors()
        mobile_index = self._get_mobile_nav_index()

        page.appbar = None

        page.navigation_bar = ft.NavigationBar(
            selected_index=mobile_index,
            on_change=self.on_mobile_navigation_change,
            bgcolor=colors["surface"],
            indicator_color=colors["primary"],
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

        theme_btn = ft.IconButton(
            icon=ft.Icons.LIGHT_MODE if self.is_dark else ft.Icons.DARK_MODE,
            icon_color=colors["text"],
            on_click=self._toggle_theme,
            tooltip="Cambiar tema",
            scale=0.9,
        )
        self.theme_toggle = theme_btn

        header = ft.Container(
            bgcolor=colors["surface"],
            padding=ft.padding.only(left=16, right=16, top=42, bottom=12),
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                "Minimarket ERP",
                                size=18,
                                weight=ft.FontWeight.W_800,
                                color=colors["text"],
                            ),
                            ft.Text(
                                self._get_mobile_subtitle(),
                                size=11,
                                color=colors["text_secondary"],
                            ),
                        ],
                        tight=True,
                        spacing=0,
                    ),
                    ft.Container(expand=True),
                    theme_btn,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )
        page.floating_action_button = self._build_mobile_fab()

        page.add(
            ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    header,
                    self.content_area,
                ],
            )
        )

    def _build_desktop_layout(self) -> None:
        page = self.page
        colors = self._get_colors()
        page.appbar = None
        page.navigation_bar = None
        page.floating_action_button = None

        theme_btn = ft.IconButton(
            icon=ft.Icons.LIGHT_MODE if self.is_dark else ft.Icons.DARK_MODE,
            icon_color=colors["text"],
            on_click=self._toggle_theme,
            tooltip="Cambiar tema",
        )
        self.theme_toggle = theme_btn

        header = ft.Container(
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            bgcolor=colors["surface"],
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                "Minimarket ERP",
                                size=18,
                                weight=ft.FontWeight.W_800,
                                color=colors["text"],
                            ),
                            ft.Text(
                                "Gestion de inventario",
                                size=9,
                                color=colors["text_secondary"],
                            ),
                        ],
                        tight=True,
                    ),
                    ft.Container(expand=True),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=12, vertical=6),
                        border_radius=16,
                        bgcolor=colors["surface_low"],
                        content=ft.Text(
                            "Buscar...", size=12, color=colors["text_secondary"]
                        ),
                    ),
                    ft.Container(width=8),
                    ft.IconButton(
                        icon=ft.Icons.NOTIFICATIONS_OUTLINED,
                        icon_color=colors["text"],
                        scale=0.85,
                    ),
                    theme_btn,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )

        self.nav_rail = ft.NavigationRail(
            selected_index=self.current_index,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            group_alignment=-0.85,
            bgcolor=colors["surface_container"],
            indicator_color=colors["primary"],
            on_change=self.on_navigation_change,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.HOME_OUTLINED,
                    selected_icon=ft.Icons.HOME,
                    label="Dashboard",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.INVENTORY_2_OUTLINED,
                    selected_icon=ft.Icons.INVENTORY_2,
                    label="Productos",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SWAP_HORIZ_OUTLINED,
                    selected_icon=ft.Icons.SWAP_HORIZ,
                    label="Kardex",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.RECEIPT_OUTLINED,
                    selected_icon=ft.Icons.RECEIPT,
                    label="Ventas",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.PAYMENTS_OUTLINED,
                    selected_icon=ft.Icons.PAYMENTS,
                    label="Gastos",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.QUERY_STATS_OUTLINED,
                    selected_icon=ft.Icons.QUERY_STATS,
                    label="Reportes",
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SYNC_OUTLINED,
                    selected_icon=ft.Icons.SYNC,
                    label="Sync",
                ),
            ],
        )

        page.add(
            ft.Column(
                [
                    ft.Container(content=header, height=64),
                    ft.Row(
                        [self.nav_rail, self.content_area],
                        expand=True,
                        spacing=0,
                    ),
                ],
                expand=True,
                spacing=0,
            )
        )

    def on_navigation_change(self, e) -> None:
        self.current_index = e.control.selected_index
        if not self.content_area:
            return
        self.content_area.content = self.get_view(e.control.selected_index)
        self.page.update()

    def on_mobile_navigation_change(self, e) -> None:
        selected_mobile_index = e.control.selected_index
        self.current_index = self.mobile_destinations[selected_mobile_index]
        self.page.clean()
        self._build_layout()
        self.page.update()

    def _build_mobile_fab(self) -> ft.FloatingActionButton | None:
        return None

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

    def get_view(self, index: int) -> ft.Control:
        if not self.page:
            return ft.Text("Inicializando...")

        is_mobile = self.is_mobile
        views = {
            0: DashboardView(self.reporte_controller, is_mobile),
            1: ProductosView(self.page, self.producto_controller, self.kardex_controller, is_mobile),
            2: KardexView(self.page, self.kardex_controller, self.producto_controller, is_mobile),
            3: BoletasView(self.page, self.venta_controller),
            4: GastosView(self.page, self.gasto_controller, is_mobile),
            5: ReportesView(self.reporte_controller),
            6: SyncView(self.page, self.sync_controller, is_mobile),
        }
        return views.get(index, DashboardView(self.reporte_controller, is_mobile))


if __name__ == "__main__":
    app = MinimarketApp()
    app.run()
