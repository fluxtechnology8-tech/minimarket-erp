from __future__ import annotations

import flet as ft
from views.components.ui import empty_state
from views.ui.theme import AppTheme
from views.ui.utils import money, parse_float, parse_int


class ProductosView(ft.Container):
    def __init__(self, page: ft.Page, producto_controller, kardex_controller, is_mobile: bool = False):
        super().__init__(expand=True, padding=0)
        self._page = page
        self.producto_controller = producto_controller
        self.kardex_controller = kardex_controller
        self.is_mobile = is_mobile
        self.search_text = ""
        self.list_view = ft.GridView(
            expand=True,
            spacing=12,
            run_spacing=12,
            max_extent=200 if is_mobile else 220,
        )
        self.search_field = ft.TextField(
            prefix_icon=ft.Icons.SEARCH,
            hint_text="Buscar por nombre, código o categoría",
            filled=True,
            bgcolor=AppTheme.SURFACE_CONTAINER_LOWEST,
            border_radius=18,
            on_change=self.on_search_change,
        )
        self.build_view()

    def build_view(self) -> None:
        self.refresh_products()
        self.content = ft.ListView(
            [
                self._build_header(),
                self._build_search(),
                self._build_product_grid(),
            ],
            expand=True,
            spacing=20,
            padding=ft.padding.only(bottom=80),
        )

    def _build_header(self) -> ft.Container:
        action_button = (
            ft.Container()
            if self.is_mobile
            else ft.Container(
                padding=ft.padding.symmetric(horizontal=20, vertical=12),
                bgcolor=AppTheme.PRIMARY,
                border_radius=24,
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.ADD, color=ft.Colors.WHITE, size=20),
                        ft.Text(
                            "Nuevo producto",
                            size=14,
                            weight=ft.FontWeight.W_600,
                            color=ft.Colors.WHITE,
                        ),
                    ],
                    spacing=8,
                ),
                on_click=self.open_form,
            )
        )
        return ft.Container(
            content=ft.Row(
                [
                    ft.Column(
                        [
                            ft.Text(
                                "Catálogo de Productos",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                            ft.Text(
                                "Gestión integral de suministros"
                                if not self.is_mobile
                                else "Solo visualización",
                                size=13,
                                color=AppTheme.TEXT_SECONDARY,
                            ),
                        ],
                        tight=True,
                    ),
                    ft.Container(expand=True),
                    action_button,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )

    def _build_search(self) -> ft.Container:
        search_width = 280 if self.is_mobile else 400
        return ft.Container(
            width=search_width,
            content=self.search_field,
        )

    def _build_product_grid(self) -> ft.Container:
        return ft.Container(
            expand=True,
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(
                                    "Todos los productos",
                                    size=16,
                                    weight=ft.FontWeight.W_600,
                                    color=AppTheme.TEXT_PRIMARY,
                                ),
                                ft.Container(expand=True),
                                ft.Text(
                                    "Ordenar: Más recientes",
                                    size=12,
                                    color=AppTheme.TEXT_SECONDARY,
                                ),
                                ft.Icon(
                                    ft.Icons.EXPAND_MORE,
                                    size=16,
                                    color=AppTheme.TEXT_SECONDARY,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        margin=ft.margin.only(bottom=16),
                    ),
                    ft.Container(
                        expand=True,
                        content=self.list_view,
                    ),
                ]
            ),
        )

    def on_search_change(self, e) -> None:
        self.search_text = (e.control.value or "").strip().lower()
        self.refresh_products()
        self.update()

    def get_filtered_products(self) -> list[dict]:
        productos = self.producto_controller.get_all()
        if not self.search_text:
            return productos
        return [
            producto
            for producto in productos
            if self.search_text
            in " ".join(
                [
                    str(producto.get("codigo", "")),
                    str(producto.get("nombre", "")),
                    str(producto.get("categoria", "")),
                ]
            ).lower()
        ]

    def refresh_products(self) -> None:
        productos = self.get_filtered_products()
        if not productos:
            self.list_view.controls = [
                ft.Container(
                    content=empty_state(
                        "No hay productos para mostrar",
                        "Agrega el primer producto o ajusta la búsqueda.",
                    ),
                    col={"sm": 12},
                )
            ]
            return

        cards: list[ft.Control] = []
        for producto in productos:
            stock = int(producto["stock"] or 0)
            minimo = int(producto["stock_minimo"] or 0)
            stock_color = (
                AppTheme.SUCCESS
                if stock > minimo
                else AppTheme.WARNING
                if stock > 0
                else AppTheme.DANGER
            )

            cards.append(self._build_product_card(producto, stock, stock_color))

        self.list_view.controls = cards

    def _build_product_card(
        self, producto: dict, stock: int, stock_color: str
    ) -> ft.Container:
        return ft.Container(
            padding=16,
            border_radius=20,
            bgcolor=AppTheme.SURFACE_CONTAINER_LOWEST,
            content=ft.Column(
                [
                    ft.Container(
                        height=100,
                        bgcolor=AppTheme.SURFACE_CONTAINER,
                        border_radius=12,
                        content=ft.Icon(
                            ft.Icons.INVENTORY_2_ROUNDED,
                            size=40,
                            color=AppTheme.TEXT_SECONDARY,
                        ),
                    ),
                    ft.Column(
                        [
                            ft.Text(
                                producto["nombre"],
                                size=14,
                                weight=ft.FontWeight.W_600,
                                color=AppTheme.TEXT_PRIMARY,
                                max_lines=2,
                            ),
                            ft.Text(
                                f"SKU: {producto['codigo']}",
                                size=11,
                                color=AppTheme.TEXT_SECONDARY,
                            ),
                            ft.Row(
                                [
                                    ft.Text(
                                        money(float(producto.get("precio_venta") or 0)),
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color=AppTheme.PRIMARY,
                                    ),
                                    ft.Container(expand=True),
                                ]
                            ),
                            ft.Row(
                                [
                                    ft.Container(
                                        width=8,
                                        height=8,
                                        border_radius=4,
                                        bgcolor=stock_color,
                                    ),
                                    ft.Text(
                                        f"{stock} en stock",
                                        size=12,
                                        color=stock_color,
                                        weight=ft.FontWeight.W_500,
                                    ),
                                ]
                            ),
                        ],
                        spacing=4,
                    ),
                ],
                spacing=8,
            ),
        )

    def open_form(self, e) -> None:
        codigo = ft.TextField(label="Código", autofocus=True)
        nombre = ft.TextField(label="Nombre")
        categoria = ft.TextField(label="Categoría")
        precio_compra = ft.TextField(label="Precio compra", value="0")
        precio_venta = ft.TextField(label="Precio venta", value="0")
        stock = ft.TextField(label="Stock inicial", value="0")
        stock_minimo = ft.TextField(label="Stock mínimo", value="5")
        unidad = ft.TextField(label="Unidad", value="unidad")
        descripcion = ft.TextField(
            label="Descripción", multiline=True, min_lines=2, max_lines=4
        )
        error_text = ft.Text("", color=AppTheme.DANGER, visible=False)

        def close_dialog(_):
            dialog.open = False
            self._page.update()

        def save_product(_):
            try:
                cantidad_inicial = parse_int(stock.value)
                precio_compra_val = parse_float(precio_compra.value)
                result = self.producto_controller.create_with_stock_inicial(
                    {
                        "codigo": codigo.value.strip(),
                        "nombre": nombre.value.strip(),
                        "categoria": categoria.value.strip(),
                        "precio_compra": precio_compra_val,
                        "precio_venta": parse_float(precio_venta.value),
                        "stock": 0,
                        "stock_minimo": parse_int(stock_minimo.value, 5),
                        "unidad": unidad.value.strip() or "unidad",
                        "descripcion": descripcion.value.strip(),
                    },
                    cantidad_inicial,
                    precio_compra_val,
                )
                dialog.open = False
                self.refresh_products()
                self.update()
                self._page.snack_bar = ft.SnackBar(
                    ft.Text("Producto registrado correctamente.")
                )
                self._page.snack_bar.open = True
                self._page.update()
            except Exception as exc:
                error_text.value = f"No se pudo guardar: {exc}"
                error_text.visible = True
                self._page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nuevo producto"),
            content=ft.Container(
                width=500,
                content=ft.Column(
                    [
                        codigo,
                        nombre,
                        categoria,
                        ft.ResponsiveRow(
                            [
                                ft.Column([precio_compra], col={"sm": 12, "md": 6}),
                                ft.Column([precio_venta], col={"sm": 12, "md": 6}),
                            ],
                            run_spacing=10,
                        ),
                        descripcion,
                        error_text,
                    ],
                    tight=True,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.FilledButton("Guardar", on_click=save_product),
            ],
        )
        self._page.dialog = dialog
        dialog.open = True
        self._page.update()
