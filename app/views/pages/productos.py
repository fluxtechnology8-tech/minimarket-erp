from __future__ import annotations

import flet as ft
import asyncio
import base64
from views.components.ui import (
    empty_state,
    card,
    searchbar,
    app_dropdown,
    primary_btn,
    badge,
)
from views.ui.theme import AppTheme, shadow
from views.ui.utils import money, parse_float, parse_int


class ProductosView(ft.Container):
    def __init__(
        self,
        page: ft.Page,
        producto_controller,
        kardex_controller,
        is_mobile: bool = False,
    ):
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
            prefix_icon=ft.Icons.SEARCH_ROUNDED,
            hint_text="Buscar por nombre, código o categoría",
            filled=True,
            bgcolor=AppTheme.INPUT_BG,
            border_radius=AppTheme.R_PILL,
            on_change=self.on_search_change,
        )
        self.build_view()

    @staticmethod
    def _bytes_to_src(data: bytes, filename: str) -> str:
        """Convierte bytes a data URI en base64 para compatibilidad web/desktop."""
        ext = filename.rsplit(".", 1)[-1].lower()
        mime = {
            "jpg": "image/jpeg",
            "jpeg": "image/jpeg",
            "png": "image/png",
            "gif": "image/gif",
            "webp": "image/webp",
            "bmp": "image/bmp",
        }.get(ext, "image/png")
        b64 = base64.b64encode(data).decode("utf-8")
        return f"data:{mime};base64,{b64}"

    def build_view(self) -> None:
        self.refresh_products()
        self.content = ft.ListView(
            [
                self._build_header(),
                self._build_stats(),
                self._build_search(),
                self._build_product_grid(),
            ],
            expand=True,
            spacing=14,
            padding=24,
        )

    def _build_header(self) -> ft.Container:
        action_button = (
            ft.Container()
            if self.is_mobile
            else ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.ADD_ROUNDED, color="#FFFFFF", size=15),
                        ft.Text(
                            "Nuevo Producto",
                            size=12,
                            weight=ft.FontWeight.W_600,
                            color="#FFFFFF",
                        ),
                    ],
                    spacing=6,
                ),
                bgcolor=AppTheme.PRIMARY,
                border_radius=AppTheme.R_PILL,
                padding=ft.padding.symmetric(horizontal=16, vertical=10),
                on_click=self.open_form,
            )
        )
        return ft.Row(
            [
                ft.Column(
                    [
                        ft.Text(
                            "Catálogo de Productos",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=AppTheme.TEXT_PRIMARY,
                        ),
                        ft.Text(
                            "Gestión de inventario y precios",
                            size=13,
                            color=AppTheme.TEXT_MUTED,
                        ),
                    ],
                    tight=True,
                ),
                ft.Container(expand=True),
                action_button,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def _build_stats(self) -> ft.Container:
        productos = self.producto_controller.get_all()
        total = len(productos)
        con_stock = sum(1 for p in productos if int(p.get("stock") or 0) > 0)
        agotados = sum(1 for p in productos if int(p.get("stock") or 0) <= 0)

        def stat_box(value, label, bg):
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Text(
                            value,
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=AppTheme.TEXT_PRIMARY,
                        ),
                        ft.Text(label, size=11, color=AppTheme.TEXT_MUTED),
                    ],
                    spacing=2,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                bgcolor=bg,
                border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
                border_radius=AppTheme.R_MD,
                padding=ft.padding.symmetric(horizontal=20, vertical=10),
            )

        return ft.Row(
            [
                stat_box(str(total), "Total", AppTheme.INPUT_BG),
                stat_box(str(con_stock), "Con stock", AppTheme.SUCCESS_LT),
                stat_box(str(agotados), "Agotados", AppTheme.DANGER_LT),
            ],
            spacing=10,
        )

    def _build_search(self) -> ft.Container:
        return ft.Container(
            content=searchbar(
                "Buscar por nombre, SKU o categoría...", on_change=self.on_search_change
            ),
            width=400,
        )

    def _build_product_grid(self) -> ft.Container:
        return card(
            ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Todos los productos",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=AppTheme.TEXT_PRIMARY,
                            ),
                            ft.Container(expand=True),
                            app_dropdown(
                                "Ordenar",
                                "Más recientes",
                                ["Más recientes", "Nombre A-Z", "Precio menor"],
                                width=160,
                            ),
                        ],
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=14),
                    ft.Container(expand=True, content=self.list_view),
                ],
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
            stock_text = f"{stock} en stock" if stock > 0 else "Agotado"
            stock_bg = (
                AppTheme.SUCCESS_LT
                if stock > minimo
                else AppTheme.WARNING_LT
                if stock > 0
                else AppTheme.DANGER_LT
            )

            cards.append(
                self._build_product_card(
                    producto, stock, stock_color, stock_text, stock_bg
                )
            )

        self.list_view.controls = cards

    def _build_product_card(
        self,
        producto: dict,
        stock: int,
        stock_color: str,
        stock_text: str,
        stock_bg: str,
    ) -> ft.Container:
        precio = producto.get("precio_venta") or 0

        def on_edit(e):
            self.open_edit_form(producto)

        def on_delete(e):
            self._show_delete_confirmation(producto)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        height=90,
                        bgcolor=AppTheme.PRIMARY_LIGHT,
                        border_radius=AppTheme.R_MD,
                        content=ft.Stack(
                            controls=[
                                ft.Container(
                                    content=ft.Icon(
                                        ft.Icons.INVENTORY_2_OUTLINED,
                                        size=40,
                                        color=AppTheme.PRIMARY,
                                    ),
                                    alignment=ft.Alignment(0, 0),
                                    height=90,
                                ),
                            ],
                        ),
                    ),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Text(
                                    producto["nombre"],
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                    color=AppTheme.TEXT_PRIMARY,
                                    max_lines=2,
                                ),
                                ft.Text(
                                    f"SKU: {producto['codigo']}",
                                    size=11,
                                    color=AppTheme.TEXT_MUTED,
                                ),
                                ft.Container(height=4),
                                ft.Row(
                                    [
                                        ft.Text(
                                            money(float(precio))
                                            if precio and float(precio) > 0
                                            else "Sin precio",
                                            size=18,
                                            weight=ft.FontWeight.BOLD
                                            if precio and float(precio) > 0
                                            else ft.FontWeight.W_400,
                                            color=AppTheme.PRIMARY
                                            if precio and float(precio) > 0
                                            else AppTheme.TEXT_MUTED,
                                        ),
                                        ft.Container(expand=True),
                                        badge(stock_text, stock_color, stock_bg),
                                    ],
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Container(height=8),
                                ft.Row(
                                    [
                                        primary_btn(
                                            "Editar",
                                            ft.Icons.EDIT_ROUNDED,
                                            "ghost",
                                            on_click=on_edit,
                                        ),
                                        ft.Container(
                                            content=ft.Icon(
                                                ft.Icons.MORE_VERT_ROUNDED,
                                                color=AppTheme.TEXT_MUTED,
                                                size=16,
                                            ),
                                            width=32,
                                            height=32,
                                            bgcolor=AppTheme.INPUT_BG,
                                            border=ft.Border.all(
                                                0.5, AppTheme.CARD_BORDER
                                            ),
                                            border_radius=AppTheme.R_MD,
                                            alignment=ft.Alignment(0, 0),
                                            on_click=on_delete,
                                        ),
                                    ],
                                ),
                            ],
                            spacing=3,
                        ),
                        padding=12,
                    ),
                ],
                spacing=0,
            ),
            bgcolor=AppTheme.CARD_BG,
            border_radius=AppTheme.R_LG,
            border=ft.Border.all(0.5, AppTheme.CARD_BORDER),
            shadow=shadow(AppTheme.PRIMARY, 6, 2),
            expand=1,
            ink=True,
        )

    def open_form(self, e) -> None:
        codigo = ft.TextField(label="Código", autofocus=True)
        nombre = ft.TextField(label="Nombre")
        categoria = ft.TextField(label="Categoría")
        unidad = ft.TextField(label="Unidad", value="unidad")
        descripcion = ft.TextField(
            label="Descripción", multiline=True, min_lines=2, max_lines=4
        )

        imagen_preview = ft.Container(
            width=100,
            height=100,
            border_radius=AppTheme.R_MD,
            bgcolor=AppTheme.INPUT_BG,
            content=ft.Icon(ft.Icons.IMAGE, size=40, color=AppTheme.TEXT_MUTED),
        )

        imagen_path = {"src": None, "name": None}
        error_text = ft.Text("", color=AppTheme.DANGER, visible=False)

        async def seleccionar_imagen(e_):
            try:
                files = await ft.FilePicker().pick_files(
                    file_type=ft.FilePickerFileType.IMAGE,
                    allow_multiple=False,
                    with_data=True,
                )

                if not files:
                    return

                archivo = files[0]
                data_uri = None

                if archivo.bytes:
                    data_uri = self._bytes_to_src(archivo.bytes, archivo.name)
                elif archivo.path:
                    with open(archivo.path, "rb") as f:
                        data_uri = self._bytes_to_src(f.read(), archivo.name)

                if data_uri:
                    imagen_path["src"] = data_uri
                    imagen_path["name"] = archivo.name
                    imagen_preview.content = ft.Image(
                        src=data_uri,
                        width=100,
                        height=100,
                        fit=ft.BoxFit.COVER,
                        border_radius=AppTheme.R_MD,
                    )
                    error_text.visible = False
                else:
                    error_text.value = "No se pudo procesar la imagen"
                    error_text.visible = True

                self._page.update()
            except Exception as exc:
                error_text.value = f"Error al cargar imagen: {exc}"
                error_text.visible = True
                self._page.update()

        def close_dialog(_):
            self._page.pop_dialog()

        def save_product(_):
            try:
                self.producto_controller.create(
                    {
                        "codigo": codigo.value.strip(),
                        "nombre": nombre.value.strip(),
                        "categoria": categoria.value.strip(),
                        "precio_compra": 0,
                        "precio_venta": 0,
                        "stock": 0,
                        "stock_minimo": 5,
                        "unidad": unidad.value.strip() or "unidad",
                        "descripcion": descripcion.value.strip(),
                        "imagen": imagen_path["src"],
                    }
                )
                self._page.pop_dialog()
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
                        ft.Row(
                            [
                                ft.Column(
                                    [imagen_preview],
                                    alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Column([codigo, nombre, categoria], expand=True),
                            ],
                            spacing=16,
                        ),
                        unidad,
                        descripcion,
                        ft.Button(
                            "Cargar Imagen",
                            icon=ft.Icons.UPLOAD_FILE,
                            on_click=seleccionar_imagen,
                            expand=True,
                        ),
                        error_text,
                    ],
                    tight=True,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.FilledButton("Aceptar", on_click=save_product),
            ],
        )
        self._page.show_dialog(dialog)

    def open_edit_form(self, producto: dict) -> None:
        codigo = ft.TextField(
            label="Código", value=producto.get("codigo", ""), disabled=True
        )
        nombre = ft.TextField(label="Nombre", value=producto.get("nombre", ""))
        categoria = ft.TextField(label="Categoría", value=producto.get("categoria", ""))
        unidad = ft.TextField(label="Unidad", value=producto.get("unidad", "unidad"))
        descripcion = ft.TextField(
            label="Descripción",
            value=producto.get("descripcion", ""),
            multiline=True,
            min_lines=2,
            max_lines=4,
        )

        imagen_path = {"src": producto.get("imagen"), "name": None}

        imagen_preview = ft.Container(
            width=100,
            height=100,
            border_radius=AppTheme.R_MD,
            bgcolor=AppTheme.INPUT_BG,
        )

        if producto.get("imagen"):
            imagen_preview.content = ft.Image(
                src=producto["imagen"],
                fit=ft.BoxFit.COVER,
                width=100,
                height=100,
                border_radius=AppTheme.R_MD,
            )
        else:
            imagen_preview.content = ft.Icon(
                ft.Icons.IMAGE, size=40, color=AppTheme.TEXT_MUTED
            )

        error_text = ft.Text("", color=AppTheme.DANGER, visible=False)

        async def seleccionar_imagen(e_):
            try:
                files = await ft.FilePicker().pick_files(
                    file_type=ft.FilePickerFileType.IMAGE,
                    allow_multiple=False,
                    with_data=True,
                )

                if not files:
                    return

                archivo = files[0]
                data_uri = None

                if archivo.bytes:
                    data_uri = self._bytes_to_src(archivo.bytes, archivo.name)
                elif archivo.path:
                    with open(archivo.path, "rb") as f:
                        data_uri = self._bytes_to_src(f.read(), archivo.name)

                if data_uri:
                    imagen_path["src"] = data_uri
                    imagen_path["name"] = archivo.name
                    imagen_preview.content = ft.Image(
                        src=data_uri,
                        width=100,
                        height=100,
                        fit=ft.BoxFit.COVER,
                        border_radius=AppTheme.R_MD,
                    )
                    error_text.visible = False
                else:
                    error_text.value = "No se pudo procesar la imagen"
                    error_text.visible = True

                self._page.update()
            except Exception as exc:
                error_text.value = f"Error al cargar imagen: {exc}"
                error_text.visible = True
                self._page.update()

        def close_dialog(_):
            self._page.pop_dialog()

        def save_changes(_):
            try:
                self.producto_controller.update(
                    producto["id"],
                    {
                        "nombre": nombre.value.strip(),
                        "categoria": categoria.value.strip(),
                        "unidad": unidad.value.strip() or "unidad",
                        "descripcion": descripcion.value.strip(),
                        "imagen": imagen_path["src"],
                    },
                )
                self._page.pop_dialog()
                self.refresh_products()
                self.update()
                self._page.snack_bar = ft.SnackBar(
                    ft.Text("Producto actualizado correctamente.")
                )
                self._page.snack_bar.open = True
                self._page.update()
            except Exception as exc:
                error_text.value = f"No se pudo actualizar: {exc}"
                error_text.visible = True
                self._page.update()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar producto"),
            content=ft.Container(
                width=500,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Column(
                                    [imagen_preview],
                                    alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Column([codigo, nombre, categoria], expand=True),
                            ],
                            spacing=16,
                        ),
                        unidad,
                        descripcion,
                        ft.Button(
                            "Cambiar Imagen",
                            icon=ft.Icons.UPLOAD_FILE,
                            on_click=seleccionar_imagen,
                            expand=True,
                        ),
                        error_text,
                    ],
                    tight=True,
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dialog),
                ft.FilledButton("Guardar", on_click=save_changes),
            ],
        )
        self._page.show_dialog(dialog)

    def _show_delete_confirmation(self, producto: dict) -> None:
        def on_confirm(_):
            try:
                self.producto_controller.delete(producto["id"])
                self._page.pop_dialog()
                self.refresh_products()
                self.update()
                self._page.snack_bar = ft.SnackBar(
                    ft.Text("Producto eliminado correctamente.")
                )
                self._page.snack_bar.open = True
                self._page.update()
            except Exception as exc:
                self._page.snack_bar = ft.SnackBar(ft.Text(f"Error al eliminar: {exc}"))
                self._page.snack_bar.open = True
                self._page.update()

        def on_cancel(_):
            self._page.pop_dialog()

        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(
                f"¿Estás seguro de eliminar el producto '{producto['nombre']}'?"
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=on_cancel),
                ft.TextButton("Eliminar", on_click=on_confirm, color=AppTheme.DANGER),
            ],
        )
        self._page.show_dialog(dialog)
