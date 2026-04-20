from __future__ import annotations

import flet as ft
from views.components.ui import empty_state, card, app_input, primary_btn, badge
from views.ui.theme import AppTheme, shadow
from views.ui.utils import money, parse_int, parse_float, short_datetime


class BoletasView(ft.Container):
    def __init__(self, page: ft.Page, controller):
        super().__init__(expand=True, padding=24)
        self._page = page
        self.controller = controller
        self._cart = {}
        self._cart_col = ft.Column(spacing=0, expand=True)
        self._cart_total_col = ft.Column(spacing=0)
        self._cart_count_badge = None
        self.build_view()

    def build_view(self) -> None:
        self.refresh_cart()
        self.content = ft.Column(
            [
                self._build_header(),
                self._build_main_row(),
            ],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=14,
        )

    def _build_header(self) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        "Venta en Curso",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_PRIMARY,
                    ),
                    ft.Text(
                        "Seleccione productos para la boleta actual",
                        size=13,
                        color=AppTheme.TEXT_MUTED,
                    ),
                ],
                tight=True,
            ),
        )

    def _build_main_row(self) -> ft.Row:
        return ft.Row(
            [
                ft.Container(self._build_product_grid(), expand=True),
                ft.Container(self._build_cart_panel(), width=290),
            ],
            spacing=14,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

    def _build_product_grid(self) -> ft.Container:
        products = [
            ("Pluma Estilográfica Premium", "✒️", 12.50, 34, "Tinta negra, punta fina"),
            ("Cuaderno de Cuero A5", "📔", 24.00, 5, "Hojas punteadas, 120g"),
            ("Set Cintas Washi Pastel", "🎀", 8.20, 120, "Paquete de 6 unidades"),
            ("Pack Resaltadores Neon", "🖊️", 5.90, 45, "4 colores de alta visibilidad"),
            ("Agenda Ejecutiva 2024", "📅", 18.00, 1, "Diseño minimalista gris"),
            ("Marcadores Caligráficos", "🎨", 14.30, 28, "Set de 12 gradientes azules"),
        ]

        def prod_tile(name, emoji, price, stock, desc):
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Stack(
                            controls=[
                                ft.Container(
                                    content=ft.Text(emoji, size=36),
                                    bgcolor=AppTheme.INPUT_BG,
                                    height=80,
                                    alignment=ft.Alignment(0, 0),
                                    border_radius=ft.BorderRadius(
                                        AppTheme.R_LG, AppTheme.R_LG, 0, 0
                                    ),
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        f"{stock} unid.",
                                        size=9,
                                        weight=ft.FontWeight.BOLD,
                                        color="#FFFFFF",
                                    ),
                                    bgcolor=AppTheme.PRIMARY,
                                    border_radius=AppTheme.R_PILL,
                                    padding=ft.padding.symmetric(
                                        horizontal=6, vertical=2
                                    ),
                                    top=6,
                                    right=6,
                                ),
                            ],
                        ),
                        ft.Container(
                            content=ft.Column(
                                [
                                    ft.Text(
                                        name,
                                        size=12,
                                        weight=ft.FontWeight.BOLD,
                                        color=AppTheme.TEXT_PRIMARY,
                                        max_lines=2,
                                    ),
                                    ft.Text(desc, size=10, color=AppTheme.TEXT_MUTED),
                                    ft.Container(height=4),
                                    ft.Row(
                                        [
                                            ft.Text(
                                                f"${price:.2f}",
                                                size=16,
                                                weight=ft.FontWeight.BOLD,
                                                color=AppTheme.PRIMARY,
                                            ),
                                            ft.Container(expand=True),
                                            ft.Container(
                                                content=ft.Icon(
                                                    ft.Icons.SHOPPING_CART_OUTLINED,
                                                    color=AppTheme.TEXT_MUTED,
                                                    size=16,
                                                ),
                                                width=30,
                                                height=30,
                                                bgcolor=AppTheme.INPUT_BG,
                                                border=ft.Border.all(
                                                    0.5, AppTheme.CARD_BORDER
                                                ),
                                                border_radius=AppTheme.R_MD,
                                                alignment=ft.Alignment(0, 0),
                                            ),
                                        ],
                                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                    ),
                                ],
                                spacing=3,
                            ),
                            padding=10,
                        ),
                    ],
                    spacing=0,
                ),
                bgcolor=AppTheme.CARD_BG,
                border_radius=AppTheme.R_LG,
                border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
                shadow=shadow(AppTheme.PRIMARY, 4, 1),
                on_click=lambda e, n=name, em=emoji, pr=price: self._add_to_cart(
                    n, em, pr
                ),
                ink=True,
                expand=1,
            )

        grid_rows = []
        for i in range(0, len(products), 3):
            grid_rows.append(
                ft.Row(
                    controls=[prod_tile(*p) for p in products[i : i + 3]],
                    spacing=10,
                )
            )

        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Container(
                            content=ft.Text(
                                "PAPELERÍA",
                                size=11,
                                weight=ft.FontWeight.W_700,
                                color="#FFFFFF",
                            ),
                            bgcolor=AppTheme.PRIMARY,
                            border_radius=AppTheme.R_PILL,
                            padding=ft.padding.symmetric(horizontal=12, vertical=5),
                        ),
                        ft.Container(
                            content=ft.Text(
                                "OFICINA", size=11, color=AppTheme.TEXT_MUTED
                            ),
                            border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
                            border_radius=AppTheme.R_PILL,
                            padding=ft.padding.symmetric(horizontal=12, vertical=5),
                        ),
                        ft.Container(
                            content=ft.Text("ARTE", size=11, color=AppTheme.TEXT_MUTED),
                            border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
                            border_radius=AppTheme.R_PILL,
                            padding=ft.padding.symmetric(horizontal=12, vertical=5),
                        ),
                    ],
                    spacing=8,
                ),
                ft.Container(height=12),
                *grid_rows,
                ft.Container(height=12),
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(
                                ft.Icons.TRENDING_UP_ROUNDED,
                                color=AppTheme.PRIMARY,
                                size=14,
                            ),
                            ft.Text(
                                "OCUPACIÓN DE CAJA",
                                size=10,
                                weight=ft.FontWeight.W_600,
                                color=AppTheme.TEXT_MUTED,
                                expand=True,
                            ),
                            ft.Text(
                                "75%",
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.PRIMARY,
                            ),
                        ],
                        spacing=6,
                    ),
                    padding=ft.padding.only(bottom=8),
                ),
                ft.Container(
                    content=ft.Container(
                        bgcolor=AppTheme.PRIMARY,
                        border_radius=AppTheme.R_PILL,
                        height=8,
                        width=310,
                    ),
                    bgcolor=AppTheme.INPUT_BG,
                    border_radius=AppTheme.R_PILL,
                    height=8,
                ),
                ft.Text("Capacidad diaria", size=10, color=AppTheme.TEXT_MUTED),
            ],
            spacing=10,
            expand=True,
        )

    def _build_cart_panel(self) -> ft.Container:
        cart_count = ft.Container(
            content=ft.Text(
                "0 Items", size=10, weight=ft.FontWeight.W_600, color=AppTheme.PRIMARY
            ),
            bgcolor=AppTheme.PRIMARY_LIGHT,
            padding=ft.padding.symmetric(horizontal=8, vertical=3),
            border_radius=AppTheme.R_PILL,
        )
        self._cart_count_badge = cart_count

        ventas_recientes = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "Ventas Recientes",
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=AppTheme.TEXT_PRIMARY,
                            expand=True,
                        ),
                        ft.Text("VER TODO", size=11, color=AppTheme.PRIMARY),
                    ],
                ),
                ft.Container(height=6),
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "#BOL-00452",
                                size=12,
                                weight=ft.FontWeight.W_600,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                            ft.Text(
                                "Cliente: Arturo P.", size=11, color=AppTheme.TEXT_MUTED
                            ),
                            ft.Text(
                                "$12.00",
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.PRIMARY,
                            ),
                        ],
                        spacing=2,
                    ),
                    bgcolor=AppTheme.INPUT_BG,
                    border_radius=AppTheme.R_MD,
                    padding=10,
                    border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
                ),
            ],
            spacing=0,
        )

        return card(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Carrito de Venta",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                                expand=True,
                            ),
                            cart_count,
                        ],
                    ),
                    ft.Container(height=10),
                    self._cart_col,
                    ft.Container(height=4),
                    self._cart_total_col,
                    ft.Container(height=10),
                    primary_btn("🧾  Generar Boleta", icon=None, expand=True),
                    ft.Container(height=6),
                    primary_btn("Cancelar", variant="outline", expand=True),
                    ft.Divider(height=14, color=AppTheme.DIVIDER),
                    ventas_recientes,
                ],
                spacing=0,
            ),
        )

    def _add_to_cart(self, name, emoji, price):
        if name in self._cart:
            self._cart[name]["qty"] += 1
        else:
            self._cart[name] = {"emoji": emoji, "price": price, "qty": 1}
        self.refresh_cart()
        if self._page:
            self._page.update()

    def _remove_from_cart(self, name):
        if name in self._cart:
            del self._cart[name]
        self.refresh_cart()
        if self._page:
            self._page.update()

    def _change_qty(self, name, delta):
        if name in self._cart:
            self._cart[name]["qty"] += delta
            if self._cart[name]["qty"] <= 0:
                del self._cart[name]
        self.refresh_cart()
        if self._page:
            self._page.update()

    def refresh_cart(self) -> None:
        self._cart_col.controls.clear()
        self._cart_total_col.controls.clear()

        if not self._cart:
            self._cart_col.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.Icons.SHOPPING_CART_OUTLINED,
                                size=40,
                                color=AppTheme.TEXT_DISABLED,
                            ),
                            ft.Text(
                                "Haz clic en un producto\npara agregarlo",
                                size=12,
                                color=AppTheme.TEXT_MUTED,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    height=120,
                    alignment=ft.Alignment(0, 0),
                    bgcolor=AppTheme.INPUT_BG,
                    border_radius=AppTheme.R_MD,
                    border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
                )
            )
            if self._cart_count_badge:
                self._cart_count_badge.content = ft.Text(
                    "0 Items",
                    size=10,
                    weight=ft.FontWeight.W_600,
                    color=AppTheme.PRIMARY,
                )
            return

        items = list(self._cart.items())
        total = 0.0
        for name, v in items:
            subtotal = v["price"] * v["qty"]
            total += subtotal
            self._cart_col.controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(v["emoji"], size=22),
                            ft.Column(
                                [
                                    ft.Text(
                                        name,
                                        size=12,
                                        weight=ft.FontWeight.W_600,
                                        color=AppTheme.TEXT_PRIMARY,
                                        max_lines=1,
                                    ),
                                    ft.Text(
                                        f"${v['price']:.2f} c/u",
                                        size=11,
                                        color=AppTheme.TEXT_MUTED,
                                    ),
                                ],
                                spacing=1,
                                expand=True,
                            ),
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Text(
                                            "−", size=14, color=AppTheme.TEXT_MUTED
                                        ),
                                        width=24,
                                        height=24,
                                        bgcolor=AppTheme.INPUT_BG,
                                        border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
                                        border_radius=6,
                                        alignment=ft.Alignment(0, 0),
                                        ink=True,
                                        on_click=lambda e, n=name: self._change_qty(
                                            n, -1
                                        ),
                                    ),
                                    ft.Text(
                                        str(v["qty"]),
                                        size=12,
                                        width=20,
                                        text_align=ft.TextAlign.CENTER,
                                    ),
                                    ft.Container(
                                        content=ft.Text(
                                            "+", size=14, color=AppTheme.TEXT_MUTED
                                        ),
                                        width=24,
                                        height=24,
                                        bgcolor=AppTheme.INPUT_BG,
                                        border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
                                        border_radius=6,
                                        alignment=ft.Alignment(0, 0),
                                        ink=True,
                                        on_click=lambda e, n=name: self._change_qty(
                                            n, 1
                                        ),
                                    ),
                                ],
                                spacing=4,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    "✕", size=12, color=AppTheme.TEXT_MUTED
                                ),
                                ink=True,
                                on_click=lambda e, n=name: self._remove_from_cart(n),
                                padding=4,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    border=ft.Border(bottom=ft.BorderSide(0.5, AppTheme.CARD_BORDER)),
                    padding=ft.padding.symmetric(vertical=8),
                )
            )

        igv = total * 0.18
        self._cart_total_col.controls += [
            ft.Row(
                [
                    ft.Text(
                        "Subtotal", size=13, color=AppTheme.TEXT_MUTED, expand=True
                    ),
                    ft.Text(f"${total:.2f}", size=13, color=AppTheme.TEXT_SECONDARY),
                ],
            ),
            ft.Row(
                [
                    ft.Text(
                        "IGV (18%)", size=13, color=AppTheme.TEXT_MUTED, expand=True
                    ),
                    ft.Text(f"${igv:.2f}", size=13, color=AppTheme.TEXT_SECONDARY),
                ],
            ),
            ft.Divider(height=0.5, color=AppTheme.DIVIDER),
            ft.Row(
                [
                    ft.Text(
                        "Total",
                        size=15,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.TEXT_PRIMARY,
                        expand=True,
                    ),
                    ft.Text(
                        f"${total + igv:.2f}",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=AppTheme.PRIMARY,
                    ),
                ],
            ),
        ]

        count = sum(v["qty"] for v in self._cart.values())
        if self._cart_count_badge:
            self._cart_count_badge.content = ft.Text(
                f"{count} Items",
                size=10,
                weight=ft.FontWeight.W_600,
                color=AppTheme.PRIMARY,
            )
