from __future__ import annotations

import flet as ft
import asyncio
import base64
from views.components.ui import empty_state
from views.ui.theme import AppTheme
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
            prefix_icon=ft.Icons.SEARCH,
            hint_text="Buscar por nombre, código o categoría",
            filled=True,
            bgcolor=AppTheme.SURFACE_CONTAINER_LOWEST,
            border_radius=18,
            on_change=self.on_search_change,
        )
        self.build_view()

    @staticmethod
    def _bytes_to_src(data: bytes, filename: str) -> str:
        """Convierte bytes a data URI en base64 para compatibilidad web/desktop."""
        ext = filename.rsplit(".", 1)[-1].lower()
        mime = {
            "jpg": "image/jpeg", "jpeg": "image/jpeg",
            "png": "image/png", "gif": "image/gif",
            "webp": "image/webp", "bmp": "image/bmp",
        }.get(ext, "image/png")
        b64 = base64.b64encode(data).decode("utf-8")
        return f"data:{mime};base64,{b64}"

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
            padding=ft.Padding.only(bottom=80),
        )

    def _build_header(self) -> ft.Container:
        action_button = (
            ft.Container()
            if self.is_mobile
            else ft.Container(
                padding=ft.Padding.symmetric(horizontal=20, vertical=12),
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
                        margin=ft.Margin.only(bottom=16),
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
        precio = producto.get("precio_venta") or 0
        imagen = producto.get("imagen")

        def on_edit(e):
            self.open_edit_form(producto)

        def on_delete(e):
            self._show_delete_confirmation(producto)

        imagen_content = (
            ft.Image(
                src=imagen,
                fit=ft.BoxFit.COVER,
                width=100,
                height=100,
                border_radius=ft.BorderRadius(10, 10, 0, 0),
                error_content=ft.Icon(
                    ft.Icons.INVENTORY_2_ROUNDED,
                    size=40,
                    color=AppTheme.TEXT_SECONDARY,
                ),
            )
            if imagen
            else ft.Icon(
                ft.Icons.INVENTORY_2_ROUNDED,
                size=40,
                color=AppTheme.TEXT_SECONDARY,
            )
        )

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
                        content=imagen_content,
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
                            ft.Text(
                                money(float(precio))
                                if precio and float(precio) > 0
                                else "Sin precio",
                                size=14,
                                weight=ft.FontWeight.BOLD
                                if precio and float(precio) > 0
                                else ft.FontWeight.W_400,
                                color=AppTheme.PRIMARY
                                if precio and float(precio) > 0
                                else AppTheme.TEXT_SECONDARY,
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
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.IconButton(
                                            icon=ft.Icons.EDIT,
                                            icon_color=AppTheme.PRIMARY,
                                            on_click=on_edit,
                                            tooltip="Editar",
                                        ),
                                        padding=5,
                                    ),
                                    ft.Container(
                                        content=ft.IconButton(
                                            icon=ft.Icons.DELETE,
                                            icon_color=AppTheme.DANGER,
                                            on_click=on_delete,
                                            tooltip="Eliminar",
                                        ),
                                        padding=5,
                                    ),
                                ],
                                spacing=0,
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
        unidad = ft.TextField(label="Unidad", value="unidad")
        descripcion = ft.TextField(
            label="Descripción", multiline=True, min_lines=2, max_lines=4
        )

        imagen_preview = ft.Container(
            width=100,
            height=100,
            border_radius=12,
            bgcolor=AppTheme.SURFACE_CONTAINER,
            content=ft.Icon(ft.Icons.IMAGE, size=40, color=AppTheme.TEXT_SECONDARY),
        )

        imagen_path = {"src": None, "name": None}
        error_text = ft.Text("", color=AppTheme.DANGER, visible=False)

        async def seleccionar_imagen(e_):
            try:
                # ✅ Nuevo patrón Flet 0.84: instanciar FilePicker en el await
                files = await ft.FilePicker().pick_files(
                    file_type=ft.FilePickerFileType.IMAGE,
                    allow_multiple=False,
                    with_data=True,
                )

                if not files:
                    return

                archivo = files[0]
                data_uri = None

                # Intentar obtener data_uri de bytes (web) o path (desktop)
                if archivo.bytes:
                    data_uri = self._bytes_to_src(archivo.bytes, archivo.name)
                elif archivo.path:
                    with open(archivo.path, "rb") as f:
                        data_uri = self._bytes_to_src(f.read(), archivo.name)

                if data_uri:
                    imagen_path["src"] = data_uri
                    imagen_path["name"] = archivo.name

                    # Actualizar preview
                    imagen_preview.content = ft.Image(
                        src=data_uri,
                        width=100,
                        height=100,
                        fit=ft.BoxFit.COVER,
                        border_radius=ft.BorderRadius(8, 8, 8, 8),
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
                                ft.Column(
                                    [
                                        codigo,
                                        nombre,
                                        categoria,
                                    ],
                                    expand=True,
                                ),
                            ],
                            spacing=16,
                            run_spacing=16,
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
            border_radius=12,
            bgcolor=AppTheme.SURFACE_CONTAINER,
        )

        if producto.get("imagen"):
            imagen_preview.content = ft.Image(
                src=producto["imagen"],
                fit=ft.BoxFit.COVER,
                width=100,
                height=100,
                border_radius=ft.BorderRadius(8, 8, 8, 8),
            )
        else:
            imagen_preview.content = ft.Icon(
                ft.Icons.IMAGE, size=40, color=AppTheme.TEXT_SECONDARY
            )

        error_text = ft.Text("", color=AppTheme.DANGER, visible=False)

        async def seleccionar_imagen(e_):
            try:
                # ✅ Nuevo patrón Flet 0.84: instanciar FilePicker en el await
                files = await ft.FilePicker().pick_files(
                    file_type=ft.FilePickerFileType.IMAGE,
                    allow_multiple=False,
                    with_data=True,
                )

                if not files:
                    return

                archivo = files[0]
                data_uri = None

                # Intentar obtener data_uri de bytes (web) o path (desktop)
                if archivo.bytes:
                    data_uri = self._bytes_to_src(archivo.bytes, archivo.name)
                elif archivo.path:
                    with open(archivo.path, "rb") as f:
                        data_uri = self._bytes_to_src(f.read(), archivo.name)

                if data_uri:
                    imagen_path["src"] = data_uri
                    imagen_path["name"] = archivo.name

                    # Actualizar preview
                    imagen_preview.content = ft.Image(
                        src=data_uri,
                        width=100,
                        height=100,
                        fit=ft.BoxFit.COVER,
                        border_radius=ft.BorderRadius(8, 8, 8, 8),
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
                                ft.Column(
                                    [
                                        codigo,
                                        nombre,
                                        categoria,
                                    ],
                                    expand=True,
                                ),
                            ],
                            spacing=16,
                            run_spacing=16,
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
