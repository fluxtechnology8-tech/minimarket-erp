from __future__ import annotations

import flet as ft
from views.components.ui import empty_state
from views.ui.theme import AppTheme
from views.ui.utils import money, parse_int, short_datetime


class BoletasView(ft.Container):
    def __init__(self, page: ft.Page, controller):
        super().__init__(expand=True, padding=0)
        self._page = page
        self.controller = controller
        self.carrito = []
        self.cart_list = ft.ListView(spacing=8, expand=True)
        self.ventas_list = ft.ListView(spacing=8, expand=True)
        self.total_text = ft.Text(
            "S/ 0.00", size=24, weight=ft.FontWeight.BOLD, color=AppTheme.PRIMARY
        )
        self.build_view()

    def build_view(self) -> None:
        self.cliente_nombre = ft.TextField(
            label="Nombre / razón social",
            filled=True,
            bgcolor=AppTheme.SURFACE_CONTAINER_LOWEST,
            border_radius=14,
        )
        self.cliente_documento = ft.TextField(
            label="DNI / RUC",
            filled=True,
            bgcolor=AppTheme.SURFACE_CONTAINER_LOWEST,
            border_radius=14,
        )
        self.product_dropdown = ft.Dropdown(
            label="Producto",
            options=self._product_options(),
            filled=True,
            bgcolor=AppTheme.SURFACE_CONTAINER_LOWEST,
            border_radius=14,
        )
        self.cantidad_field = ft.TextField(
            label="Cantidad",
            value="1",
            width=100,
            filled=True,
            bgcolor=AppTheme.SURFACE_CONTAINER_LOWEST,
            border_radius=14,
        )

        self.refresh_cart()
        self.refresh_sales()

        self.content = ft.ListView(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "Nueva venta",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                            ft.Text(
                                "Registra una nueva transacción",
                                size=13,
                                color=AppTheme.TEXT_SECONDARY,
                            ),
                        ],
                        tight=True,
                    ),
                ),
                self._build_new_sale_form(),
                self._build_cart_section(),
                self._build_recent_sales(),
            ],
            expand=True,
            spacing=20,
            padding=ft.padding.only(bottom=80),
        )

    def _build_new_sale_form(self) -> ft.Container:
        return ft.Container(
            padding=20,
            border_radius=24,
            bgcolor=AppTheme.SURFACE_CONTAINER_LOW,
            content=ft.Column(
                [
                    ft.ResponsiveRow(
                        [
                            ft.Column([self.cliente_nombre], col={"md": 8}),
                            ft.Column([self.cliente_documento], col={"md": 4}),
                        ],
                        run_spacing=12,
                    ),
                    ft.ResponsiveRow(
                        [
                            ft.Column([self.product_dropdown], col={"md": 9}),
                            ft.Column([self.cantidad_field], col={"md": 2}),
                            ft.Column(
                                [
                                    ft.Container(
                                        padding=12,
                                        bgcolor=AppTheme.PRIMARY,
                                        border_radius=24,
                                        content=ft.Row(
                                            [
                                                ft.Icon(
                                                    ft.Icons.ADD_SHOPPING_CART,
                                                    color=ft.Colors.WHITE,
                                                    size=18,
                                                ),
                                                ft.Text(
                                                    "Agregar",
                                                    size=13,
                                                    weight=ft.FontWeight.W_600,
                                                    color=ft.Colors.WHITE,
                                                ),
                                            ],
                                            spacing=6,
                                        ),
                                        on_click=self.add_to_cart,
                                    ),
                                ],
                                col={"md": 1},
                            ),
                        ],
                        run_spacing=12,
                    ),
                ],
                spacing=16,
            ),
        )

    def _build_cart_section(self) -> ft.Container:
        return ft.Container(
            padding=20,
            border_radius=24,
            bgcolor=AppTheme.SURFACE_CONTAINER_LOW,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Carrito",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                            ft.Container(expand=True),
                            ft.Container(
                                padding=ft.padding.symmetric(horizontal=12, vertical=6),
                                bgcolor=AppTheme.SECONDARY_LIGHT,
                                border_radius=16,
                                content=ft.Text(
                                    f"{len(self.carrito)} items",
                                    size=12,
                                    weight=ft.FontWeight.W_500,
                                    color=AppTheme.PRIMARY,
                                ),
                            ),
                        ]
                    ),
                    ft.Container(height=200, content=self.cart_list),
                    ft.Container(
                        padding=16,
                        border_radius=16,
                        bgcolor=AppTheme.SURFACE_CONTAINER_LOWEST,
                        content=ft.Row(
                            [
                                ft.Text(
                                    "TOTAL",
                                    size=14,
                                    weight=ft.FontWeight.W_500,
                                    color=AppTheme.TEXT_SECONDARY,
                                ),
                                ft.Container(expand=True),
                                self.total_text,
                            ]
                        ),
                    ),
                    ft.Container(
                        padding=14,
                        bgcolor=AppTheme.PRIMARY,
                        border_radius=24,
                        content=ft.Row(
                            [
                                ft.Icon(
                                    ft.Icons.RECEIPT_LONG,
                                    color=ft.Colors.WHITE,
                                    size=20,
                                ),
                                ft.Text(
                                    "Generar boleta",
                                    size=14,
                                    weight=ft.FontWeight.W_600,
                                    color=ft.Colors.WHITE,
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        on_click=self.generate_sale,
                    ),
                ],
                spacing=12,
            ),
        )

    def _build_recent_sales(self) -> ft.Container:
        return ft.Container(
            padding=20,
            border_radius=24,
            bgcolor=AppTheme.SURFACE_CONTAINER_LOW,
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Boletas recientes",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                            ft.Container(expand=True),
                            ft.Text("Ver todo", size=12, color=AppTheme.PRIMARY),
                        ]
                    ),
                    ft.Container(height=300, content=self.ventas_list),
                ],
                spacing=12,
            ),
        )

    def _product_options(self):
        options = []
        for producto in self.controller.get_productos_con_stock():
            if int(producto.get("stock") or 0) <= 0:
                continue
            label = f"{producto['codigo']} - {producto['nombre']} ({money(float(producto['precio_venta'] or 0))})"
            options.append(ft.dropdown.Option(str(producto["id"]), label))
        return options

    def add_to_cart(self, e) -> None:
        if not self.product_dropdown.value:
            self.show_message("Seleccione un producto.")
            return
        producto = self.controller.get_producto(int(self.product_dropdown.value))
        if not producto:
            self.show_message("El producto ya no existe.")
            return
        cantidad = parse_int(self.cantidad_field.value, 1)
        if cantidad <= 0:
            self.show_message("La cantidad debe ser mayor a cero.")
            return
        if cantidad > int(producto.get("stock") or 0):
            self.show_message("No hay stock suficiente.")
            return

        existing = next(
            (item for item in self.carrito if item["producto_id"] == producto["id"]),
            None,
        )
        if existing:
            nueva_cantidad = existing["cantidad"] + cantidad
            if nueva_cantidad > int(producto.get("stock") or 0):
                self.show_message("La cantidad total supera el stock disponible.")
                return
            existing["cantidad"] = nueva_cantidad
        else:
            self.carrito.append(
                {
                    "producto_id": producto["id"],
                    "nombre": producto["nombre"],
                    "cantidad": cantidad,
                    "precio_unitario": float(producto.get("precio_venta") or 0),
                }
            )
        self.refresh_cart()
        self.update()

    def refresh_cart(self) -> None:
        if not self.carrito:
            self.cart_list.controls = [
                empty_state("Carrito vacío", "Agrega productos para empezar la venta.")
            ]
            self.total_text.value = "S/ 0.00"
            return

        rows = []
        total = 0.0
        for item in self.carrito:
            subtotal = item["cantidad"] * item["precio_unitario"]
            total += subtotal
            rows.append(
                ft.Container(
                    padding=12,
                    border_radius=12,
                    bgcolor=AppTheme.SURFACE_CONTAINER_LOWEST,
                    content=ft.Row(
                        [
                            ft.Container(
                                width=40,
                                height=40,
                                border_radius=10,
                                bgcolor=AppTheme.SURFACE_CONTAINER,
                                content=ft.Icon(
                                    ft.Icons.SHOPPING_BAG,
                                    color=AppTheme.PRIMARY_CONTAINER,
                                    size=20,
                                ),
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        item["nombre"],
                                        size=13,
                                        weight=ft.FontWeight.W_600,
                                        color=AppTheme.TEXT_PRIMARY,
                                    ),
                                    ft.Text(
                                        f"Cant: {item['cantidad']} x {money(item['precio_unitario'])}",
                                        size=11,
                                        color=AppTheme.TEXT_SECONDARY,
                                    ),
                                ],
                                expand=True,
                                tight=True,
                            ),
                            ft.Text(
                                money(subtotal), size=14, weight=ft.FontWeight.BOLD
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                icon_color=AppTheme.DANGER,
                                on_click=lambda _, pid=item["producto_id"]: (
                                    self.remove_item(pid)
                                ),
                            ),
                        ],
                        spacing=12,
                    ),
                )
            )
        self.cart_list.controls = rows
        self.total_text.value = money(total)

    def remove_item(self, producto_id: int) -> None:
        self.carrito = [
            item for item in self.carrito if item["producto_id"] != producto_id
        ]
        self.refresh_cart()
        self.update()

    def refresh_sales(self) -> None:
        ventas = self.controller.get_all(limit=12)
        if not ventas:
            self.ventas_list.controls = [
                empty_state(
                    "Sin boletas registradas", "Las ventas completadas aparecerán aquí."
                )
            ]
            return

        controls = []
        for venta in ventas:
            controls.append(
                ft.Container(
                    padding=12,
                    border_radius=12,
                    bgcolor=AppTheme.SURFACE_CONTAINER_LOWEST,
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        venta["numero_boleta"],
                                        size=13,
                                        weight=ft.FontWeight.BOLD,
                                        color=AppTheme.PRIMARY,
                                    ),
                                    ft.Container(expand=True),
                                    ft.Text(
                                        money(float(venta.get("total") or 0)),
                                        size=13,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ]
                            ),
                            ft.Text(
                                f"{venta.get('cliente_nombre') or 'Cliente'} | {short_datetime(venta.get('fecha'))}",
                                size=11,
                                color=AppTheme.TEXT_SECONDARY,
                            ),
                        ],
                        tight=True,
                        spacing=2,
                    ),
                )
            )
        self.ventas_list.controls = controls

    def generate_sale(self, e) -> None:
        try:
            result = self.controller.generar_boleta(
                self.carrito,
                cliente_nombre=(self.cliente_nombre.value or "").strip(),
                cliente_documento=(self.cliente_documento.value or "").strip(),
            )
            numero = result.get("numero_boleta", "")
            self.carrito = []
            self.cliente_nombre.value = ""
            self.cliente_documento.value = ""
            self.product_dropdown.options = self._product_options()
            self.product_dropdown.value = None
            self.refresh_cart()
            self.refresh_sales()
            self.update()
            self.show_message(f"Boleta generada: {numero}")
        except Exception as exc:
            self.show_message(f"No se pudo generar la boleta: {exc}")

    def show_message(self, message: str) -> None:
        self._page.snack_bar = ft.SnackBar(ft.Text(message))
        self._page.snack_bar.open = True
        self._page.update()
